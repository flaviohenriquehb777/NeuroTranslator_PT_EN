# 002 — Deploy da API em Hugging Face Spaces

## Contexto

O objetivo é hospedar uma API de tradução própria sem custo, mantendo o frontend em GitHub Pages.

## Decisão

Hospedar a API Python (FastAPI) em um Hugging Face Space público usando SDK Docker.

## Consequências

- ✅ Free tier com execução em CPU e integração direta com o Hugging Face Hub.
- ✅ Boa integração com CI/CD via GitHub Actions.
- ⚠️ Cold start é esperado em Spaces gratuitos (scale-to-zero).
- ⚠️ Limitações de hardware e tempo de inicialização exigem fallback no frontend.

## Alternativas consideradas

- Railway/Render/Fly.io: podem exigir billing ou limitar de forma mais agressiva.
- Vercel Functions: limitações para workloads pesados e dependências de ML.
- Hospedagem própria: custo e manutenção.

