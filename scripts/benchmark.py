from __future__ import annotations

import datetime as dt
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import sacrebleu
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def _load_samples(path: Path) -> List[Dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("translation_samples.json inválido")
    return data


@torch.inference_mode()
def _translate_batch(model_id: str, texts: List[str]) -> Tuple[List[str], float]:
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    model.eval()

    started = time.perf_counter()
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    out = model.generate(**inputs, max_new_tokens=256)
    preds = tokenizer.batch_decode(out, skip_special_tokens=True)
    elapsed = time.perf_counter() - started
    return preds, elapsed


def _try_google_translate(texts: List[str]) -> Optional[List[str]]:
    try:
        from deep_translator import GoogleTranslator

        t = GoogleTranslator(source="pt", target="en")
        return [t.translate(x) for x in texts]
    except Exception:
        return None


def _write_badge(path: Path, bleu: float) -> None:
    label = "BLEU"
    value = f"{bleu:.1f}"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="150" height="20" role="img" aria-label="{label}: {value}">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#fff" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="150" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="70" height="20" fill="#111827"/>
    <rect x="70" width="80" height="20" fill="#22c55e"/>
    <rect width="150" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="35" y="14">{label}</text>
    <text x="110" y="14">{value}</text>
  </g>
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    samples_path = repo_root / "tests" / "translation_samples.json"
    out_metrics = repo_root / "docs" / "metrics.json"
    out_badge = repo_root / "docs" / "metrics_badge.svg"

    samples = _load_samples(samples_path)
    src_texts = [s["source"] for s in samples]
    refs = [s["target"] for s in samples]

    model_id = "Helsinki-NLP/opus-mt-pt-en"
    preds, elapsed = _translate_batch(model_id, src_texts)

    bleu = float(sacrebleu.corpus_bleu(preds, [refs]).score)
    avg_latency_ms = int((elapsed / max(len(src_texts), 1)) * 1000)

    google_preds = _try_google_translate(src_texts)
    google_bleu: Optional[float] = None
    diff_percent: Optional[float] = None
    if google_preds:
        google_bleu = float(sacrebleu.corpus_bleu(google_preds, [refs]).score)
        if google_bleu > 0:
            diff_percent = float(((bleu - google_bleu) / google_bleu) * 100)

    payload: Dict[str, Any] = {
        "timestamp": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "bleu_score": round(bleu, 2),
        "avg_latency_ms": avg_latency_ms,
        "model": model_id,
        "test_samples": len(samples),
        "google_bleu_score": round(google_bleu, 2) if google_bleu is not None else None,
        "google_diff_percent": round(diff_percent, 2) if diff_percent is not None else None,
    }

    out_metrics.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_badge(out_badge, bleu)

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

