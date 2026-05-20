# 005 — Bundle único IIFE (Vite)

## Contexto

O NeuroTranslator é distribuído via GitHub Pages e precisa ser simples de servir e cachear, mantendo o carregamento rápido.

## Decisão

Manter o build do frontend como um único arquivo IIFE gerado pelo Vite (sem chunks), publicado dentro de `web/assets/js/script-optimized.js`.

## Consequências

- ✅ Deploy extremamente simples (arquivo estático).
- ✅ Menos problemas com CORS/imports e paths relativos.
- ✅ Melhor previsibilidade de cache com um único artefato.
- ⚠️ Pode aumentar o tamanho do bundle se o projeto crescer muito.
- ⚠️ Perde benefícios de code-splitting.

## Alternativas consideradas

- ESM com imports/chunks: melhor escalabilidade, porém maior complexidade de deploy e cache.
- Framework SPA completo: aumentaria dependências e tamanho do bundle.

