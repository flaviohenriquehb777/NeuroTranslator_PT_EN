# 🧠 NeuroTranslator

Tradutor PT ↔ EN com interface web moderna, fallback múltiplo de serviços e proxy opcional para normalizar CORS. Reconhecimento de voz e síntese de fala integrados quando suportados pelo navegador.

## Sumário
- [Preview](#preview)
- [Visão Geral](#visão-geral)
- [Estrutura](#estrutura)
- [Instalação](#instalação)
- [Uso](#uso)
- [Funcionalidades](#funcionalidades)
- [Tradução e Proxy](#tradução-e-proxy)
- [Desenvolvimento](#desenvolvimento)
- [Testes](#testes)
- [Deploy](#deploy)
- [Contatos](#contatos)
- [Licença](#licença)

## Preview
- GitHub Pages: https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/web/

[![Abrir a aplicação](web/assets/images/preview.svg)](https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/web/)

## Visão Geral
- Tradução no frontend com cadeia de fallback: MyMemory → LibreTranslate (4 endpoints) → proxy local (opcional).
- Proxy Express com cache em memória e rate limit para uniformizar CORS e reduzir latência.
- Service Worker com precache e Stale-While-Revalidate para experiência estável.
- Acessibilidade: `aria-live`, `aria-busy`, foco visível e navegação por teclado.

## Estrutura
```
NeuroTranslator_PT_EN/
├── web/                      # Aplicação web
│   ├── assets/
│   │   ├── css/             # Estilos (styles.css)
│   │   ├── images/          # Imagens e miniaturas
│   │   ├── ts/              # Código TypeScript (fonte)
│   │   └── js/              # Bundle gerado (script-optimized.js)
│   ├── index.html
│   ├── manifest.json
│   └── sw.js
├── infra/                    # Artefatos de deploy e serviços auxiliares
│   ├── proxy/server.js      # Proxy Express (CORS/cache/rate limit)
│   └── vercel.json          # Configuração de roteamento (opcional)
├── web/tests/               # Testes Vitest (frontend)
├── package.json             # Scripts de build/lint/typecheck/test
├── tsconfig.json            # Configuração TypeScript
└── vite.config.ts           # Build com Vite
```

## Instalação
Requisitos: Node.js 18+, npm.

```bash
git clone https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN.git
cd NeuroTranslator_PT_EN
npm install
```

## Uso
```bash
npm run build
python -m http.server 8000 --directory web
# Abra http://localhost:8000/
```

Opcional (proxy local):
```bash
npm run proxy
# http://localhost:3000/translate
```

## Funcionalidades
- Tradução de texto com cadeia de fallback e preservação de capitalização do texto original.
- Reconhecimento de voz (Web Speech API) e síntese de fala (SpeechSynthesis).
- Layout escuro com estrelas, responsivo e acessível.

Limitações:
- Serviços públicos de tradução podem impor limites ou instabilidades.

## Tradução e Proxy
- Frontend tenta MyMemory (GET). Se falhar, tenta LibreTranslate em: `translate.astian.org`, `libretranslate.de`, `libretranslate.com`, `translate.argosopentech.com`.
- Em `localhost`, o frontend usa primeiro `http://localhost:3000/translate` (se o proxy estiver ativo).
- Proxy (`infra/proxy/server.js`) aplica cache curto e rate limit para estabilidade.

## Desenvolvimento
Scripts npm:
```bash
npm run build      # gera web/assets/js/script-optimized.js
npm run lint       # ESLint
npm run typecheck  # tsc --noEmit
npm test           # Vitest
npm run proxy      # inicia proxy local
```

Tecnologias:
- Vite + TypeScript no frontend; Web APIs para voz/fala; Express no proxy.

## Testes
- Teste de fallback de tradução em `web/tests/translation.test.ts`.
```bash
npm test
```

## Deploy
- Vercel (opcional): configurações em `infra/vercel.json` e `infra/vercel/project.json`.
- GitHub Pages: conteúdo servido de `web/`.

## Contatos
- GitHub: https://github.com/flaviohenriquehb777
- Issues: https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN/issues

## Licença
MIT. Veja `LICENSE.md`.