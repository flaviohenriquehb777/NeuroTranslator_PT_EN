# 001 — Modelo Helsinki-NLP (OPUS-MT)

## Contexto

O NeuroTranslator v5.0 precisa de um modelo de tradução real, gratuito e fácil de operar em infraestrutura sem custo.

## Decisão

Usar modelos MarianMT do projeto OPUS-MT hospedados no Hugging Face sob o namespace `Helsinki-NLP`, selecionando modelos por par de idiomas (e pivô em inglês quando necessário).

## Consequências

- ✅ Gratuito e amplamente suportado no ecossistema Hugging Face/Transformers.
- ✅ Roda em CPU com custo zero em Hugging Face Spaces (com trade-off de cold start).
- ⚠️ Qualidade varia por par de idioma.
- ⚠️ Modelos são relativamente grandes, afetando cold start e memória.

## Alternativas consideradas

- APIs comerciais (Google/Azure/AWS): exigem billing e chaves.
- Modelos LLM generalistas: custo e latência maiores, além de dependência de provedores pagos.
- Execução 100% client-side (WebGPU/ONNX): complexidade maior e limitações de compatibilidade.

