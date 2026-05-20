# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] - 2026-XX-XX

### Added
- API de tradução neural própria com FastAPI + Helsinki-NLP (Hugging Face Spaces)
- Pipeline CI/CD completo com GitHub Actions (frontend + backend + e2e + deploy)
- Testes E2E com Playwright
- Métricas reais (BLEU/latência) e endpoint `/metrics`
- ADRs (Architecture Decision Records) para decisões-chave de arquitetura
- Indicador visual da engine usada (Neural próprio vs Fallback)
- Warm-up automático do Hugging Face Space no carregamento da página

### Changed
- README reescrito para v5.0 com diagrama e links de documentação
- Estratégia de resiliência: MyMemory passa a ser fallback automático

## [4.0.1] - 2026-XX-XX

### Changed
- Seletor de idiomas redesenhado (pills → dropdowns custom)

## [4.0.0] - 2026-XX-XX

### Added
- Suporte a 4 novos idiomas (Dinamarquês, Finlandês, Norueguês, Grego)
- Vozes neurais com classificação por qualidade
- Detecção automática de idioma via análise de trigramas
- Interface redesenhada com tema Deep Navy e glassmorphism

