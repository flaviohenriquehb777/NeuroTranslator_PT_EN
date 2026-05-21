# 🧠 NeuroTranslator v5.0.5

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN/blob/main/LICENSE.md)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/)
[![Version](https://img.shields.io/badge/Version-5.0.5-6366f1)](https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN)
[![CI/CD](https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN/actions/workflows/ci.yml/badge.svg)](https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN/actions/workflows/ci.yml)
[![BLEU](https://img.shields.io/badge/BLEU-42.3-brightgreen)](docs/metrics.json)
[![Bundle](https://img.shields.io/badge/Bundle-10.1KB_gzipped-blue)](https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN/actions/workflows/ci.yml)
[![HF Space](https://img.shields.io/badge/%F0%9F%A4%97_HF_Space-Online-yellow)](https://huggingface.co/spaces/Flaviohb7/neurotranslator-api)

<div align="center">
  <a href="https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/">
    <img src="web/assets/images/preview.svg" alt="NeuroTranslator Web App" width="720" />
  </a>
</div>

<!-- DEMO_GIF: grave um GIF de 30s usando Screenity (Chrome) e substitua aqui -->

<div align="center">
  <a href="https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/"><strong>🚀 Acesse a Aplicação</strong></a>
  ·
  <a href="docs/"><strong>📖 Leia a Documentação</strong></a>
  ·
  <a href="https://flaviohb7-neurotranslator-api.hf.space/health"><strong>🤖 API ao vivo</strong></a>
</div>

## ✨ O que torna este projeto diferente

O **NeuroTranslator v5.0** não é apenas um frontend que chama APIs de terceiros: a tradução neural roda em **infra própria gratuita** com **FastAPI + Helsinki-NLP (OPUS-MT)** hospedado no **Hugging Face Spaces**, com **lazy loading de modelos**, **fallback automático** e **métricas reais** (BLEU/latência) integradas à UI e ao pipeline de CI/CD.

## 📊 Métricas Reais

| Métrica | Valor |
|---|---:|
| BLEU Score (PT→EN) | ~42 |
| Latência média (modelo) | < 300ms |
| Bundle size (gzipped) | ~10.1KB |
| Lighthouse Performance | 98 |
| Cobertura de testes | Em evolução |

## 🏗️ Arquitetura

```mermaid
flowchart LR
  U[Browser] -->|GitHub Pages| FE[Frontend (HTML/CSS/TS)]
  FE -->|POST /translate| API[HF Spaces API (FastAPI)]
  API -->|Transformers| M[Helsinki-NLP OPUS-MT]
  FE -->|Fallback| MM[MyMemory]
```

## 🧠 Por que Helsinki-NLP?

Decisões técnicas documentadas em ADRs:

- [001-modelo-helsinki-nlp.md](docs/adr/001-modelo-helsinki-nlp.md)
- [002-hugging-face-spaces.md](docs/adr/002-hugging-face-spaces.md)
- [003-traducao-via-pivo.md](docs/adr/003-traducao-via-pivo.md)
- [004-fallback-mymemory.md](docs/adr/004-fallback-mymemory.md)
- [005-vite-iife-bundle.md](docs/adr/005-vite-iife-bundle.md)

## 🚀 Como Funciona

1. 🧊 Ao abrir o app, ele faz warm-up no Space (`GET /health`) para reduzir cold start
2. 🧠 A tradução tenta primeiro a engine Neural própria (`POST /translate`)
3. ☁️ Se a API estiver offline/cold start, o app faz fallback automático para MyMemory
4. 🏷️ A UI mostra a engine usada e o modelo em tooltip
5. 📊 O painel de métricas (📊 no header) exibe BLEU, uptime e latência média da sessão

## 📁 Estrutura do Projeto

```text
NeuroTranslator_PT_EN/
├── web/
│   ├── index.html
│   ├── sw.js
│   ├── manifest.json
│   └── assets/
│       ├── css/styles.css
│       ├── ts/script-optimized.ts
│       └── js/script-optimized.js
├── src/api/
│   ├── main.py
│   ├── models_config.py
│   ├── requirements.txt
│   └── Dockerfile
├── scripts/
│   ├── deploy_to_hf_spaces.sh
│   └── benchmark.py
├── docs/
│   ├── metrics.json
│   ├── metrics_badge.svg
│   ├── SETUP_SECRETS.md
│   └── adr/
├── tests/
│   ├── translation_samples.json
│   └── e2e/translation.spec.ts
├── .github/workflows/ci.yml
├── playwright.config.ts
└── CHANGELOG.md
```

## ⚙️ Como Rodar Localmente

### Frontend

```bash
npm install
npm run dev
```

### API Python (FastAPI)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r src/api/requirements.txt
python -m uvicorn src.api.main:app --reload
```

## 🔄 CI/CD Pipeline

- Frontend: typecheck + lint + vitest + build + bundle-size gate
- E2E: Playwright (com mocks de rede para ficar determinístico)
- Backend: ruff + mypy + pytest
- Deploy:
  - GitHub Pages (frontend)
  - Hugging Face Spaces (API)

## 📹 Explicação da Arquitetura

<!-- LOOM_LINK: grave um vídeo de 3-5min explicando a arquitetura e substitua aqui -->
> 🎬 `https://loom.com/LINK_AQUI`

## 📝 Changelog

Veja [CHANGELOG.md](CHANGELOG.md).

## 🤝 Contribuição | 📄 Licença | 📞 Contato

- Contribuições são bem-vindas via Issues e Pull Requests
- Licença: MIT ([LICENSE.md](LICENSE.md))
- Contato: [@flaviohenriquehb777](https://github.com/flaviohenriquehb777)
