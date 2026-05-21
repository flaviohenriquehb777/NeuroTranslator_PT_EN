# NeuroTranslator_PT_EN — Auditoria Técnica (SpeechRecognition, TTS, SW, Warm-up)

Data: 2026-05-21  
Branch: `fix/audit-voice-tts-sw-warmup`

## Escopo e objetivo

Objetivo: corrigir causas raiz dos problemas de SpeechRecognition e TTS (principalmente no GitHub Pages) e reduzir a percepção de cold start do backend (HF Space), entregando patches + checklist de validação.

## Fonte da Verdade (o que realmente roda no GitHub Pages)

| Área | Fonte da verdade no runtime (Pages) | Fonte no repo | Observação |
|---|---|---|---|
| Bootstrap/handlers UI | `web/assets/js/script-optimized.js` carregado via `<script ...>` | `web/assets/ts/script-optimized.ts` | O Pages nunca executa o TS; o TS é transpilado/bundlado no CI. |
| Entrada do app | `DOMContentLoaded → new NeuroTranslatorWeb()` | [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L1600-L1625) | Bootstrap e registro do Service Worker acontecem aqui. |
| SpeechRecognition | `initSpeechRecognition/toggleSpeech/...` | [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L850-L990) | Implementado no frontend; depende do suporte do navegador e permissões. |
| TTS | `VoiceEngine + speakOutTranslation()` | [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L140-L340) e [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L1240-L1295) | Depende de vozes instaladas no dispositivo e regras de user gesture do navegador. |
| Warm-up `/health` | `warmUpNeuralApi()` | [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L585-L675) | Dispara polling em background e ajusta UI/estado. |
| Fallback MyMemory | `fetch https://api.mymemory...` | [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L1120-L1180) | Fallback quando neural falha ou está em cold start. |
| Service Worker | `web/sw.js` | [sw.js](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/sw.js) | Controla caching/offline no Pages (ponto crítico para “funciona às vezes”). |
| Deploy Pages | `actions/upload-pages-artifact` com `path: ./web` | [ci.yml](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/.github/workflows/ci.yml#L81-L103) | O Pages publica o diretório `web/` gerado no job de build. |
| Build TS→JS | `npm run build` (Vite lib IIFE) | [vite.config.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/vite.config.ts#L1-L20) e [package.json](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/package.json#L5-L13) | Gera `web/assets/js/script-optimized.js`. |

## Reproduções no GitHub Pages (evidências coletadas)

Ambiente: execução automatizada (sem microfone real disponível).

### Evidência 1 — Service Worker interferindo e tentativa de carregar Vite dev client

Ao abrir o Pages com `?debug=1`, foi observado request para `https://flaviohenriquehb777.github.io/@vite/client` com falha (`net::ERR_ABORTED`), o que é típico de HTML/JS de modo dev (Vite) e não deveria existir no build de produção.

Evidência coletada via logs de rede (lista de requests iniciais inclui):
- `GET https://flaviohenriquehb777.github.io/@vite/client` (failed)
- múltiplos `GET https://flaviohb7-neurotranslator-api.hf.space/health` (warm-up)

Interpretação:
- o Service Worker anterior fazia precache com caminhos absolutos (`/index.html`, `/assets/...`) e interceptava **todo GET**, o que em GitHub Pages (site servido em subpath `/NeuroTranslator_PT_EN/`) pode levar a cache/arbitragem incorretos e servir HTML/JS antigo ou errado.

## Causas raiz e correções

### 1) SpeechRecognition — “network” e instabilidade (principalmente no Pages)

**Causa raiz**
- Ausência de state machine/anti-reentrância: `start()` podia ser chamado em condições pouco controladas (tap rápido, transições, onend/onerror chamando stop), o que aumenta ocorrência de erros como `network` e `aborted` em navegadores que são sensíveis a chamadas concorrentes.
- Tratamento de erro genérico: não diferenciava corretamente `network` (serviço de reconhecimento indisponível) de `not-allowed` (permissão) e `no-speech` (silêncio), gerando UX confusa.

**Correção implementada**
- Implementado state machine com estados: `idle | starting | listening | processing | error`.
- Regras:
  - `recognition.start()` só via gesto do usuário (click no botão “Falar”).
  - Sem chamadas concorrentes: se `starting/listening/processing`, o clique vira “parar”.
  - Backoff para `network` sem loop infinito (bloqueia tentativa por alguns segundos e orienta retry manual).
- Instrumentação sob `?debug=1` (não loga sempre): eventos `onstart/onaudiostart/onspeechstart/onresult/onerror/onend`.

Patch: [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L850-L1030)

### 2) TTS — voz “indisponível”, principalmente para Inglês (en-*)

**Causa raiz**
- `speechSynthesis.getVoices()` frequentemente retorna `[]` nas primeiras chamadas (carregamento assíncrono). O fluxo anterior não fazia uma espera estruturada e terminava em watchdog genérico.
- Quando não havia voz `en-*`, a UX era “bug genérico”, sem orientar que o dispositivo pode não ter vozes em inglês instaladas.

**Correção implementada**
- `VoiceEngine.ensureVoicesLoaded(timeout)` com polling até 3s (e aproveitando `voiceschanged`).
- Seleção de voz por idioma com fallback explícito:
  - Se existe `en-*`, usa.
  - Se não existe `en-*`, usa voz padrão do dispositivo e mostra instrução para instalar vozes “English”.
- Instrumentação sob `?debug=1` para logar voz escolhida (nome/lang/default).

Patch:
- [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L140-L260) (VoiceEngine)
- [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L1240-L1300) (speakOutTranslation)

### 3) Service Worker — inconsistência no Pages (“às vezes funciona”)

**Causa raiz**
- Precache usando caminhos absolutos (`/index.html`, `/assets/...`) em um site hospedado em subpath (`/NeuroTranslator_PT_EN/`), podendo cachear conteúdo fora do app (raiz do domínio) e servir recursos incorretos.
- Interceptação genérica de **todo GET** (incluindo cross-origin) aumentando risco de cache indevido e comportamento não determinístico.

**Correção implementada**
- Precache agora respeita o `scope` real do SW (`self.registration.scope`) e monta URLs via `new URL(path, scope)`.
- Estratégias:
  - `network-first` para navegação/HTML (evita “HTML antigo”).
  - `stale-while-revalidate` para assets (JS/CSS) dentro do scope.
  - Não intercepta requests fora do scope.
- Registro do SW com cache-busting (`sw.js?v=5.0.6`) para forçar atualização.

Patch:
- [sw.js](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/sw.js)
- [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L1600-L1625)

### 4) Warm-up / cold start (HF Space)

**Causa raiz**
- Warm-up fazia polling com delay fixo e a tradução neural podia “segurar” a UX por dezenas de segundos antes de cair no fallback.

**Correção implementada**
- `dns-prefetch` + `preconnect` no `index.html` para reduzir latência de handshake TLS.
- Warm-up com backoff no polling do `/health` e trava `warmUpInFlight`.
- “Fallback rápido”: quando o Space não está `ready`, o timeout da neural é curto (~3.5s) e cai no MyMemory com mensagem “provável cold start”, enquanto mantém warm-up em background.

Patch:
- [index.html](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/index.html#L46-L58)
- [script-optimized.ts](file:///c:/Users/flavi/Documents/GitHub/NeuroTranslator_PT_EN/web/assets/ts/script-optimized.ts#L585-L705)

## Como validar no GitHub Pages (checklist)

1) Abrir: `https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/?debug=1`
2) Hard refresh (Ctrl+Shift+R).
3) DevTools → Application → Service Workers:
   - Verificar SW ativo como `sw.js?v=5.0.6`.
4) DevTools → Application → Storage:
   - Limpar caches antigos (`nt-static-*`) e recarregar.
5) DevTools → Network:
   - Confirmar que **não existe** request para `/@vite/client`.
6) SpeechRecognition:
   - Permitir microfone (cadeado → Microfone → Permitir).
   - Clicar “Falar” e dizer uma frase; confirmar:
     - Botão vira “Iniciando…” → “Ouvindo…”.
     - Texto aparece no campo.
     - Ao finalizar fala, a tradução dispara.
   - Forçar erros (sem permissão / silêncio) e verificar mensagens específicas.
7) TTS:
   - Com texto traduzido, clicar em “Ouvir tradução”.
   - Se destino = Inglês e não houver voz `en-*`, verificar toast orientando instalar vozes e (se possível) fallback para voz padrão.
8) Warm-up:
   - Ao abrir o app, observar que o app não trava.
   - Em cold start, primeira tradução deve cair em fallback rápido com mensagem “provável cold start”.

## Arquivos alterados nesta branch

- `web/assets/ts/script-optimized.ts`
- `web/sw.js`
- `web/index.html`
- `web/manifest.json`
- `README.md`
- `CHANGELOG.md`
- `AUDIT_REPORT.md`

