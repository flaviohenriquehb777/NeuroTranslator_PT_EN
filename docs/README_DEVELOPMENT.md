# NeuroTranslator PT-EN - Documentação de Desenvolvimento

## 🏗️ Arquitetura do Projeto

### Estrutura de Diretórios

```
NeuroTranslator_PT_EN/
├── src/                    # Código fonte principal
│   ├── audio/             # Módulos de áudio e reconhecimento de fala
│   ├── models/            # Gerenciamento de modelos de IA
│   ├── translation/       # Lógica de tradução
│   ├── ui/               # Interface gráfica
│   └── utils/            # Utilitários (config, logging)
├── config/               # Arquivos de configuração
├── data/                 # Dados temporários e cache
├── docs/                 # Documentação
├── models/               # Cache de modelos
├── notebooks/            # Jupyter notebooks para desenvolvimento
├── tests/                # Testes unitários
└── logs/                 # Arquivos de log
```

## 🔧 Componentes Principais

### 1. Sistema de Tradução (`src/translation/`)
- **translator.py**: Classe principal para tradução de texto
- Suporte para múltiplos modelos (fast, accurate, balanced)
- Detecção automática de idioma

### 2. Interface Gráfica (`src/ui/`)
- **main_interface.py**: Interface principal com CustomTkinter
- Suporte para câmera ao vivo
- Tradução por texto e fala

### 3. Reconhecimento de Fala (`src/audio/`)
- **speech_recognition.py**: Captura e processamento de áudio
- Integração com câmera para tradução em tempo real

### 4. Gerenciamento de Modelos (`src/models/`)
- **model_manager.py**: Cache e otimização de modelos
- Carregamento inteligente de recursos

### 5. Utilitários (`src/utils/`)
- **config.py**: Gerenciamento de configurações
- **logger.py**: Sistema de logging

## 🚀 Funcionalidades

### Implementadas ✅
- Interface gráfica moderna
- Sistema de configuração
- Logging estruturado
- Estrutura modular

### Em Desenvolvimento 🔄
- Captura de câmera ao vivo
- Reconhecimento de fala em tempo real
- Tradução automática por voz
- Geração de executável standalone

### Planejadas 📋
- Testes unitários completos
- Documentação de API
- Suporte para mais idiomas
- Otimizações de performance

## 🛠️ Desenvolvimento

### Configuração do Ambiente
```bash
pip install -r requirements.txt
```

### Executar a Aplicação
```bash
python main.py --mode gui
```

### Executar Testes
```bash
python -m pytest tests/
```

### Gerar Executável
```bash
python build_executable.py
```

## 📝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 🐛 Debugging

### Logs
Os logs são salvos em `logs/neurotranslator_YYYYMMDD.log`

### Configuração de Debug
Use `--debug` para logs detalhados:
```bash
python main.py --debug
```

## 📊 Performance

### Cache de Modelos
- Modelos são cacheados em `models/cache/`
- Use `ModelManager` para gerenciar cache

### Otimizações
- GPU habilitada por padrão (se disponível)
- Threading para operações em tempo real
- Cache inteligente de recursos