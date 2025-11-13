# 🧠 NeuroTranslator

## Visão Geral

Aplicação de tradução PT ↔ EN com interface web moderna. A versão atual utiliza APIs públicas de tradução no frontend, reconhecimento de voz via Web Speech API e síntese de fala via SpeechSynthesis.

## Estrutura do Projeto

```
NeuroTranslator_PT_EN/
├── web/                 # Aplicação web
│   ├── assets/
│   │   ├── css/        # Estilos (styles.css)
│   │   ├── images/     # Logos/ícones
│   │   ├── ts/         # Código TypeScript (fonte)
│   │   └── js/         # Bundle gerado (script-optimized.js)
│   ├── index.html
│   ├── manifest.json
│   └── sw.js
├── src/                 # Código Python (módulos auxiliares)
├── docs/                # Documentação adicional
├── scripts/             # Scripts utilitários
├── notebooks/           # Notebooks Jupyter
├── package.json         # Scripts de build/lint/typecheck
├── tsconfig.json        # Configuração TypeScript
└── vite.config.ts       # Build com Vite
```

Observações:
- Não há `web/api/` nem `mobile.css` na versão atual.
- O arquivo `web/assets/js/script-optimized.js` é gerado a partir de `web/assets/ts/script-optimized.ts`.

## Instalação e Uso

Requisitos: Node.js 18+, npm.

```bash
git clone https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN.git
cd NeuroTranslator_PT_EN
npm install
npm run build

# Preview local
python -m http.server 8000 --directory web
# Abra http://localhost:8000/
```

Para recursos Python (opcionais):

```bash
pip install -r requirements.txt
python main.py
```

## Funcionalidades (Atual)

- Tradução de texto no frontend usando MyMemory com fallback LibreTranslate.
- Reconhecimento de voz (quando suportado pelo navegador).
- Síntese de fala do texto traduzido.
- Layout escuro com estrelas, responsivo.

Limitações:
- Tradução depende de serviços públicos (pode haver limites/instabilidade).
- Sem backend FastAPI ativo na pasta `web/`.

## Desenvolvimento

Scripts npm:

```bash
npm run build      # gera web/assets/js/script-optimized.js
npm run lint       # ESLint
npm run typecheck  # tsc --noEmit
npm run proxy      # inicia proxy local em http://localhost:3000/translate
```

Tecnologias:
- Vite + TypeScript no frontend; Web APIs para voz/fala.

Proxy opcional:
- Endpoint local: `http://localhost:3000/translate`
- Encaminha para MyMemory e LibreTranslate, normalizando CORS.

Deploy (Vercel, opcional):
- Configurações movidas para `infra/vercel.json` e `infra/vercel/project.json`.
- Use CLI com argumento `-c infra/vercel.json` para apontar o arquivo de configuração.

## Contribuição

Pull Requests são bem-vindos. Mantenha lint e typecheck passando e atualize este README quando alterar funcionalidades.

## Licença

MIT. Veja `LICENSE.md`.