# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] - 2026-05-20

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

## [5.0.3] - 2026-05-20

### Fixed
- Reconhecimento de voz: melhor detecção de texto (interim results) e mensagens quando o microfone não inicia por permissão/bloqueio
- Leitura da tradução (TTS): aviso quando a voz não dispara no navegador/dispositivo
- Deploy HF Spaces: validação do `HF_TOKEN` (whoami) e erro mais explícito quando o push é recusado

## [5.0.2] - 2026-05-20

### Fixed
- Deploy da API no Hugging Face Spaces: alinhado para o Space `Flaviohb7/neurotranslator-api`
- Frontend: endpoint da API neural atualizado e cache-busting do PWA para evitar assets antigos
- Reconhecimento de voz: feedback quando o navegador não suporta a API

## [5.0.1] - 2026-05-20

### Fixed
- CI do backend Python: correção de import/path para execução do pytest em GitHub Actions

## [4.0.1] - 2026-XX-XX

### Changed
- Seletor de idiomas redesenhado (pills → dropdowns custom)

## [4.0.0] - 2026-XX-XX

### Added
- Suporte a 4 novos idiomas (Dinamarquês, Finlandês, Norueguês, Grego)
- Vozes neurais com classificação por qualidade
- Detecção automática de idioma via análise de trigramas
- Interface redesenhada com tema Deep Navy e glassmorphism
