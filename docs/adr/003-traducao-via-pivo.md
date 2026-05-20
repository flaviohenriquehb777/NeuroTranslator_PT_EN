# 003 — Tradução via pivô em inglês

## Contexto

Nem todos os pares entre 13 idiomas possuem modelo direto disponível no OPUS-MT.

## Decisão

Quando não houver modelo direto para um par `(src, tgt)`, traduzir via pivô em inglês: `src → en → tgt`, desde que existam modelos para `src → en` e `en → tgt`.

## Consequências

- ✅ Cobertura total (ou quase total) de pares entre idiomas suportados.
- ✅ Implementação simples e previsível.
- ⚠️ Duas inferências aumentam latência.
- ⚠️ Erros/ambiguidade podem se acumular em duas etapas.

## Alternativas consideradas

- Buscar modelos diretos adicionais por par: aumenta complexidade de manutenção e cache.
- Fine-tuning de modelos: foge do escopo do free tier e demanda dataset e compute.

