# 004 — Fallback para MyMemory

## Contexto

Hugging Face Spaces no free tier pode ficar offline (scale-to-zero) e sofrer cold start, o que impacta a UX.

## Decisão

No frontend, tentar primeiro a API própria (Neural) e, em caso de falha/timeout, usar MyMemory como fallback automático.

## Consequências

- ✅ Resiliência: o usuário continua traduzindo mesmo se o Space estiver indisponível.
- ✅ UX consistente: evita “aplicação quebrada”.
- ⚠️ Qualidade e consistência variam por provedores públicos.
- ⚠️ Dependência de terceiros permanece como fallback.

## Alternativas consideradas

- Exigir sempre a API própria: UX degradada em cold start e indisponibilidades.
- Manter apenas LibreTranslate público: maior instabilidade e variação entre instâncias.

