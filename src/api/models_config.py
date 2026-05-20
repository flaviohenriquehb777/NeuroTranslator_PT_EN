from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    target_token: Optional[str] = None


MODELS_MAP: Dict[Tuple[str, str], ModelSpec] = {
    ("pt", "en"): ModelSpec("Helsinki-NLP/opus-mt-pt-en"),
    ("en", "pt"): ModelSpec("Helsinki-NLP/opus-mt-tc-big-en-pt", target_token="por"),
    ("es", "en"): ModelSpec("Helsinki-NLP/opus-mt-es-en"),
    ("en", "es"): ModelSpec("Helsinki-NLP/opus-mt-en-es"),
    ("fr", "en"): ModelSpec("Helsinki-NLP/opus-mt-fr-en"),
    ("en", "fr"): ModelSpec("Helsinki-NLP/opus-mt-en-fr"),
    ("de", "en"): ModelSpec("Helsinki-NLP/opus-mt-de-en"),
    ("en", "de"): ModelSpec("Helsinki-NLP/opus-mt-en-de"),
    ("it", "en"): ModelSpec("Helsinki-NLP/opus-mt-it-en"),
    ("en", "it"): ModelSpec("Helsinki-NLP/opus-mt-en-it"),
    ("ru", "en"): ModelSpec("Helsinki-NLP/opus-mt-ru-en"),
    ("en", "ru"): ModelSpec("Helsinki-NLP/opus-mt-en-ru"),
    ("zh", "en"): ModelSpec("Helsinki-NLP/opus-mt-zh-en"),
    ("en", "zh"): ModelSpec("Helsinki-NLP/opus-mt-en-zh"),
    ("ja", "en"): ModelSpec("Helsinki-NLP/opus-mt-ja-en"),
    ("en", "ja"): ModelSpec("Helsinki-NLP/opus-mt-en-jap"),
    ("da", "en"): ModelSpec("Helsinki-NLP/opus-mt-da-en"),
    ("en", "da"): ModelSpec("Helsinki-NLP/opus-mt-en-da"),
    ("fi", "en"): ModelSpec("Helsinki-NLP/opus-mt-fi-en"),
    ("en", "fi"): ModelSpec("Helsinki-NLP/opus-mt-en-fi"),
    ("nb", "en"): ModelSpec("Helsinki-NLP/opus-mt-gmq-en"),
    ("en", "nb"): ModelSpec("Helsinki-NLP/opus-mt-en-gmq", target_token="nob"),
    ("el", "en"): ModelSpec("Helsinki-NLP/opus-mt-el-en"),
    ("en", "el"): ModelSpec("Helsinki-NLP/opus-mt-en-el"),
}

