from __future__ import annotations

from fastapi.testclient import TestClient

import src.api.main as main


def test_health() -> None:
    c = TestClient(main.app)
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_models_has_pairs() -> None:
    c = TestClient(main.app)
    r = c.get("/models")
    assert r.status_code == 200
    data = r.json()
    assert "pairs" in data
    assert any(p["source"] == "pt" and p["target"] == "en" for p in data["pairs"])


def test_translate_mock(monkeypatch) -> None:
    def fake_translate_with_pivot(text: str, source: str, target: str):
        return "hello", "mock-model", 0.9, 12

    monkeypatch.setattr(main, "_translate_with_pivot", fake_translate_with_pivot)
    c = TestClient(main.app)
    r = c.post("/translate", json={"text": "olá", "source": "pt", "target": "en"})
    assert r.status_code == 200
    assert r.json()["translated_text"] == "hello"
    assert r.json()["model_used"] == "mock-model"

