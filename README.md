# 🧠 NeuroTranslator PT-EN

<div align="center">
  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/YOUR_USERNAME/NeuroTranslator_PT_EN/blob/main/LICENSE.md)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://YOUR_USERNAME.github.io/NeuroTranslator_PT_EN/)
[![Version](https://img.shields.io/badge/Version-3.0-blue)](https://github.com/YOUR_USERNAME/NeuroTranslator_PT_EN)

</div>

## 📋 Sumário

- [Visão Geral](#-visão-geral)
- [Aplicação Web](#-aplicação-web)
- [Principais Funcionalidades](#-principais-funcionalidades)
- [Arquitetura do Sistema](#️-arquitetura-do-sistema)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Uso](#-instalação-e-uso)
- [Desenvolvimento](#-desenvolvimento)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

<div align="center">
  <a href="https://YOUR_USERNAME.github.io/NeuroTranslator_PT_EN/">
    <img src="https://raw.githubusercontent.com/YOUR_USERNAME/NeuroTranslator_PT_EN/main/web/assets/images/preview.svg" alt="NeuroTranslator Web App" width="600" />
  </a>
</div>

<div align="center">
  <strong>🚀 <a href="https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/">Acesse a Aplicação Web</a></strong>
</div>

## 🌟 Visão Geral

O **NeuroTranslator PT-EN** é um sistema avançado de tradução automática em tempo real que utiliza técnicas de Deep Learning e Processamento de Linguagem Natural para tradução multilíngue. O sistema oferece uma interface web moderna com reconhecimento de voz, síntese de fala e tradução de texto otimizada.

### 🎯 **Idiomas Suportados**
- 🇧🇷 **Português** (Brasil)
- 🇺🇸 **Inglês** (Estados Unidos)
- 🇪🇸 **Espanhol** (Espanha)
- 🇫🇷 **Francês** (França)
- 🇩🇪 **Alemão** (Alemanha)
- 🇨🇳 **Chinês** (Mandarim)

## 🌐 Aplicação Web

### 🎨 **Interface Moderna 2025**

A aplicação web apresenta um design profissional e moderno:

- **🌙 Tema Escuro**: Interface elegante com gradientes suaves
- **✨ Glass Morphism**: Efeitos de vidro translúcido e backdrop blur
- **📱 Design Responsivo**: Otimizado para desktop, tablet e mobile
- **⚡ Performance**: Carregamento rápido e interações fluidas

### 🔧 **Funcionalidades Web**

- 🎤 **Reconhecimento de Voz**: Captura de áudio em tempo real
- 🔊 **Síntese de Fala**: Vozes masculinas e femininas para cada idioma
- 💾 **Histórico Local**: Armazenamento das traduções no navegador
- 🔄 **Tradução Bidirecional**: Suporte completo para todos os idiomas
- 🎯 **Interface Focada**: Layout otimizado para produtividade

## ✨ Principais Funcionalidades

### 🎯 **Core Features**
- 🌐 **Tradução Multilíngue**: Suporte para 6 idiomas principais
- 🎤 **Reconhecimento de Voz**: Web Speech API com alta precisão
- 🔊 **Síntese de Fala**: Sistema de vozes fixas para consistência
- 📝 **Interface Otimizada**: Design focado em tradução eficiente

### 🏆 **Diferenciais Técnicos**
- **Latência Baixa**: Tradução rápida e responsiva
- **Vozes Consistentes**: Sistema de vozes fixas por idioma e gênero
- **Sem Overlay**: Interface limpa sem elementos desnecessários
- **Privacidade**: Processamento local quando possível

## 🏗️ Arquitetura do Sistema

### 💻 **Stack Tecnológico**

#### **Frontend Web**
- **HTML5**: Estrutura semântica moderna
- **CSS3**: Estilização avançada com glass morphism
- **JavaScript ES6+**: Lógica interativa e APIs modernas
- **Web APIs**: Speech Recognition, Speech Synthesis, WebRTC

#### **Backend & Processing**
- **Python 3.8+**: Linguagem principal
- **PyTorch/TensorFlow**: Frameworks de deep learning
- **Transformers**: Modelos de tradução neural
- **FastAPI**: API REST para serviços

#### **Audio & NLP**
- **Web Speech API**: Reconhecimento e síntese de voz
- **NLTK/spaCy**: Processamento de linguagem natural
- **LibROSA**: Análise de áudio (quando necessário)

## 📁 Estrutura do Projeto

```
NeuroTranslator_PT_EN/
├── 🌐 web/                          # Aplicação Web Principal
│   ├── index.html                   # Interface principal
│   ├── voice_diagnostic.html        # Diagnóstico de voz
│   ├── manifest.json               # PWA manifest
│   └── assets/
│       ├── css/
│       │   └── styles.css          # Estilos modernos
│       ├── js/
│       │   └── script.js           # Lógica da aplicação
│       ├── images/                 # Imagens e logos
│       └── icons/                  # Ícones da interface
│
├── 📊 src/                         # Código Fonte Principal
│   ├── audio/                      # Processamento de áudio
│   ├── translation/                # Módulos de tradução
│   ├── models/                     # Gerenciamento de modelos
│   ├── ui/                         # Interface do usuário
│   └── utils/                      # Utilitários gerais
│
├── 📝 scripts/                     # Scripts de Desenvolvimento
│   ├── mcp/                        # Scripts MCP (Model Control Protocol)
│   ├── utils/                      # Utilitários de desenvolvimento
│   └── maintenance/                # Scripts de manutenção
│
├── 📚 notebooks/                   # Jupyter Notebooks
│   ├── 01_data_exploration.ipynb   # Análise exploratória
│   ├── 02_model_training.ipynb     # Treinamento de modelos
│   └── ...                         # Outros notebooks
│
├── 📖 docs/                        # Documentação
│   ├── README_DEVELOPMENT.md       # Guia de desenvolvimento
│   ├── INSTALL.md                  # Instruções de instalação
│   └── ...                         # Documentação adicional
│
├── 🧪 tests/                       # Testes Automatizados
├── ⚙️ config/                      # Configurações
├── 📦 models/                      # Modelos treinados
└── 📄 requirements.txt             # Dependências Python
```

## 🚀 Instalação e Uso

### 📱 **Uso Web (Recomendado)**

1. **Acesso Direto**: [https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/](https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/)

2. **Servidor Local**:
   ```bash
   # Clone o repositório
   git clone https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN.git
   cd NeuroTranslator_PT_EN
   
   # Inicie o servidor local
   python -m http.server 8000 --directory web
   
   # Acesse: http://localhost:8000
   ```

### 🐍 **Instalação Python (Desenvolvimento)**

```bash
# Clone o repositório
git clone https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN.git
cd NeuroTranslator_PT_EN

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python main.py
```

## 🔧 Desenvolvimento

### 📋 **Pré-requisitos**
- Python 3.8+
- Node.js (para ferramentas de desenvolvimento)
- Navegador moderno com suporte a Web APIs

### 🛠️ **Scripts Úteis**

```bash
# Servidor de desenvolvimento
python scripts/utils/https_server.py

# Geração de favicons
python scripts/utils/generate_favicon.py

# Diagnóstico de voz
# Acesse: /voice_diagnostic.html
```

### 🧪 **Testes**

```bash
# Execute os testes
python -m pytest tests/

# Teste específico
python -m pytest tests/test_translation.py
```

## 🤝 Contribuição

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### 📝 **Diretrizes de Contribuição**
- Siga os padrões de código existentes
- Adicione testes para novas funcionalidades
- Atualize a documentação quando necessário
- Use commits semânticos

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## 🙏 Agradecimentos

- **Hugging Face** - Modelos de tradução neural
- **Google** - Web Speech API
- **Mozilla** - Ferramentas de desenvolvimento web
- **Comunidade Open Source** - Bibliotecas e frameworks utilizados

---

<div align="center">
  <strong>Desenvolvido com ❤️ por <a href="https://github.com/flaviohenriquehb777">Flávio Henrique</a></strong>
</div>

<div align="center">
  <a href="https://flaviohenriquehb777.github.io/NeuroTranslator_PT_EN/">🚀 Experimente Agora</a> •
  <a href="https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN/issues">🐛 Reportar Bug</a> •
  <a href="https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN/discussions">💬 Discussões</a>
</div>
