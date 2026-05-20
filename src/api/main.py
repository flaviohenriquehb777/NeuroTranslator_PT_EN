from __future__ import annotations

import json
import time
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional, Tuple

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

try:
    from .models_config import MODELS_MAP, ModelSpec
except Exception:
    from models_config import MODELS_MAP, ModelSpec  # type: ignore


class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    source: str = Field(min_length=2, max_length=10)
    target: str = Field(min_length=2, max_length=10)


class TranslateResponse(BaseModel):
    translated_text: str
    model_used: str
    confidence: float
    latency_ms: int


def _memory_used_mb() -> Optional[float]:
    try:
        import resource  # type: ignore

        ru_maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if ru_maxrss <= 0:
            return None
        if ru_maxrss > 10_000_000:
            return round(ru_maxrss / 1024 / 1024, 2)
        return round(ru_maxrss / 1024, 2)
    except Exception:
        return None


MODEL_CACHE: Dict[str, Tuple[Any, Any]] = {}
MODEL_LOCK = Lock()
STARTED_AT = time.time()


def _load_model(model_id: str) -> Tuple[Any, Any]:
    cached = MODEL_CACHE.get(model_id)
    if cached:
        return cached

    with MODEL_LOCK:
        cached = MODEL_CACHE.get(model_id)
        if cached:
            return cached

        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
        model.eval()
        MODEL_CACHE[model_id] = (tokenizer, model)
        return tokenizer, model


def _build_input(text: str, spec: ModelSpec) -> str:
    if spec.target_token:
        return f">>{spec.target_token}<< {text}"
    return text


@torch.inference_mode()
def _translate_once(text: str, source: str, target: str) -> Tuple[str, str, float, int]:
    spec = MODELS_MAP.get((source, target))
    if not spec:
        raise ValueError("pair_not_supported")

    tokenizer, model = _load_model(spec.model_id)
    prepared = _build_input(text, spec)

    started = time.perf_counter()
    inputs = tokenizer(prepared, return_tensors="pt", padding=True, truncation=True)
    out = model.generate(
        **inputs,
        max_new_tokens=256,
        return_dict_in_generate=True,
        output_scores=True,
    )
    latency_ms = int((time.perf_counter() - started) * 1000)

    decoded = tokenizer.batch_decode(out.sequences, skip_special_tokens=True)
    translated = decoded[0] if decoded else ""

    confidence = 0.0
    try:
        scores = out.scores or []
        if scores:
            gen_tokens = out.sequences[0, -len(scores) :]
            probs: List[float] = []
            for i, step_scores in enumerate(scores):
                token_id = gen_tokens[i].item()
                step_logprobs = torch.log_softmax(step_scores[0], dim=-1)
                probs.append(float(step_logprobs[token_id].exp().item()))
            confidence = float(sum(probs) / len(probs))
    except Exception:
        confidence = 0.0

    return translated, spec.model_id, confidence, latency_ms


def _resolve_path(source: str, target: str) -> List[Tuple[str, str]]:
    if (source, target) in MODELS_MAP:
        return [(source, target)]
    if source != "en" and target != "en":
        if (source, "en") in MODELS_MAP and ("en", target) in MODELS_MAP:
            return [(source, "en"), ("en", target)]
    raise ValueError("pair_not_supported")


def _translate_with_pivot(text: str, source: str, target: str) -> Tuple[str, str, float, int]:
    if source == target:
        return text, "identity", 1.0, 0

    steps = _resolve_path(source, target)
    current = text
    model_used_parts: List[str] = []
    confidences: List[float] = []
    total_ms = 0
    for a, b in steps:
        translated, model_used, conf, ms = _translate_once(current, a, b)
        current = translated
        model_used_parts.append(model_used)
        confidences.append(conf)
        total_ms += ms

    return current, " | ".join(model_used_parts), float(sum(confidences) / len(confidences)), total_ms


def _models_supported_pairs() -> List[Dict[str, Any]]:
    langs = sorted({a for a, _ in MODELS_MAP.keys()} | {b for _, b in MODELS_MAP.keys()} | {"en"})
    pairs: List[Dict[str, Any]] = []
    for src in langs:
        for tgt in langs:
            if src == tgt:
                continue
            try:
                steps = _resolve_path(src, tgt)
            except Exception:
                continue
            pivot = len(steps) > 1
            models = [MODELS_MAP[s].model_id for s in steps if s in MODELS_MAP]
            pairs.append({"source": src, "target": tgt, "pivot": pivot, "models": models})
    return pairs


app = FastAPI(title="NeuroTranslator API", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://flaviohenriquehb777.github.io",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, Any]:
    mem_mb = _memory_used_mb()
    loaded = list(MODEL_CACHE.keys())
    return {
        "status": "ok",
        "loaded_models": loaded,
        "loaded_models_count": len(loaded),
        "memory_mb": mem_mb,
        "started_at": int(STARTED_AT),
        "uptime_s": int(time.time() - STARTED_AT),
        "timestamp": int(time.time()),
    }


@app.get("/models")
def models() -> Dict[str, Any]:
    return {"pairs": _models_supported_pairs()}


@app.get("/metrics")
def metrics() -> Dict[str, Any]:
    p = Path(__file__).resolve().parents[2] / "docs" / "metrics.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest) -> TranslateResponse:
    source = req.source.strip().lower()
    target = req.target.strip().lower()
    text = req.text.strip()

    try:
        translated_text, model_used, confidence, latency_ms = _translate_with_pivot(text, source, target)
    except ValueError:
        raise HTTPException(status_code=400, detail="Unsupported language pair") from None
    except Exception:
        raise HTTPException(status_code=500, detail="Translation failed") from None

    return TranslateResponse(
        translated_text=translated_text,
        model_used=model_used,
        confidence=confidence,
        latency_ms=latency_ms,
    )

