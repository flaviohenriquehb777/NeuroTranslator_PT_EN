# 🚀 Guia de Instalação e Execução - NeuroTranslator PT-EN

Este guia fornece instruções detalhadas para instalar e executar o NeuroTranslator PT-EN em seu computador.

## 📋 Pré-requisitos

### Sistema Operacional
- **Windows**: 10/11 (64-bit)
- **macOS**: 10.14+ 
- **Linux**: Ubuntu 18.04+, CentOS 7+, ou distribuições equivalentes

### Software Necessário
- **Python**: 3.8 ou superior (recomendado: 3.9+)
- **Git**: Para clonar o repositório
- **Conexão com Internet**: Para download de modelos e dependências

### Hardware Recomendado
- **RAM**: Mínimo 8GB (recomendado: 16GB+)
- **Armazenamento**: 5GB livres
- **GPU**: Opcional (NVIDIA com CUDA para melhor performance)

## 🔧 Instalação

### Passo 1: Clonar o Repositório

```bash
# Clonar o repositório
git clone https://github.com/flaviohenriquehb777/NeuroTranslator_PT_EN.git

# Entrar no diretório
cd NeuroTranslator_PT_EN
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências básicas
pip install -r requirements.txt

# Para funcionalidades completas (opcional):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Passo 4: Verificar Instalação

```bash
# Testar instalação
python main.py --help
```

## 🎯 Como Usar

### Modo 1: Interface Gráfica (Recomendado)

```bash
# Executar interface gráfica
python main.py

# Ou especificamente:
python main.py --mode gui
```

**Funcionalidades da Interface:**
- ✅ Tradução bidirecional PT ↔ EN
- ✅ Seleção de modelos (Rápido/Preciso/Balanceado)
- ✅ Histórico de traduções
- ✅ Importar/Exportar arquivos de texto
- ✅ Estatísticas em tempo real

### Modo 2: Linha de Comando

```bash
# Tradução simples
python main.py --mode cli --text "Olá mundo" --target en

# Traduzir arquivo
python main.py --mode cli --file input.txt --output output.txt

# Especificar modelo
python main.py --mode cli --text "Hello world" --target pt --model accurate
```

### Modo 3: Demonstração

```bash
# Executar demonstração completa
python main.py --mode demo

# Demonstração específica
python -m jupyter notebook 07_final_demo.ipynb
```

## 📁 Estrutura do Projeto

```
NeuroTranslator_PT_EN/
├── main.py                 # Script principal
├── requirements.txt        # Dependências
├── config.json            # Configurações (criado automaticamente)
├── README.md              # Documentação principal
├── INSTALL.md             # Este guia
├── LICENSE.md             # Licença
├── src/                   # Código fonte
│   ├── __init__.py
│   ├── translation/       # Módulo de tradução
│   ├── ui/               # Interface gráfica
│   ├── audio/            # Processamento de áudio
│   └── utils/            # Utilitários
├── notebooks/            # Jupyter notebooks
├── data/                 # Dados (criado automaticamente)
├── models/              # Modelos (baixados automaticamente)
└── logs/                # Logs (criado automaticamente)
```

## ⚙️ Configuração Avançada

### Arquivo de Configuração

O arquivo `config.json` é criado automaticamente na primeira execução. Você pode editá-lo para personalizar:

```json
{
  "translation": {
    "default_model": "balanced",
    "max_length": 512,
    "cache_translations": true
  },
  "ui": {
    "theme": "dark",
    "window_size": "800x600"
  },
  "performance": {
    "use_gpu": true,
    "max_workers": 4
  }
}
```

### Modelos Disponíveis

| Modelo | Velocidade | Precisão | Uso de Memória | Recomendado Para |
|--------|------------|----------|----------------|------------------|
| **Rápido** | ⚡⚡⚡ | ⭐⭐ | 🔋 | Tradução rápida, textos curtos |
| **Balanceado** | ⚡⚡ | ⭐⭐⭐ | 🔋🔋 | Uso geral (padrão) |
| **Preciso** | ⚡ | ⭐⭐⭐⭐ | 🔋🔋🔋 | Textos importantes, documentos |

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError"

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: "CUDA not available"

```bash
# Instalar versão CPU do PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Interface não abre

```bash
# Verificar CustomTkinter
pip install customtkinter --upgrade

# Testar modo CLI
python main.py --mode cli --text "teste"
```

### Modelos não baixam

```bash
# Verificar conexão com internet
# Tentar novamente ou usar modelo local
python main.py --mode demo
```

### Performance lenta

1. **Use GPU se disponível:**
   ```json
   "performance": {"use_gpu": true}
   ```

2. **Reduza tamanho do modelo:**
   ```bash
   python main.py --model fast
   ```

3. **Feche outros programas** que usam muita memória

## 📊 Monitoramento

### Logs do Sistema

```bash
# Ver logs em tempo real
tail -f logs/neurotranslator_YYYYMMDD.log

# Windows:
Get-Content logs/neurotranslator_YYYYMMDD.log -Wait
```

### Estatísticas de Performance

- Acesse **Ferramentas > Estatísticas** na interface gráfica
- Ou use: `python main.py --mode cli --stats`

## 🔄 Atualizações

```bash
# Atualizar código
git pull origin main

# Atualizar dependências
pip install -r requirements.txt --upgrade
```

## 📱 Compartilhamento

### Para outro computador:

1. **Copie toda a pasta** do projeto
2. **Instale Python 3.8+** no computador de destino
3. **Execute os passos de instalação** neste guia
4. **Ou crie um executável:**

```bash
# Instalar PyInstaller
pip install pyinstaller

# Criar executável
pyinstaller --onefile --windowed main.py
```

### Para usuários sem Python:

1. Use o executável gerado com PyInstaller
2. Ou forneça um instalador com Python incluído
3. Ou use Docker (avançado)

## 🐳 Docker (Opcional)

```bash
# Construir imagem
docker build -t neurotranslator .

# Executar container
docker run -p 8080:8080 neurotranslator
```

## 🆘 Suporte

Se encontrar problemas:

1. **Consulte este guia** primeiro
2. **Verifique os logs** em `logs/`
3. **Teste com modo demo:** `python main.py --mode demo`
4. **Entre em contato:**
   - **Email:** flaviohenriquehb777@outlook.com
   - **LinkedIn:** https://www.linkedin.com/in/flávio-henrique-barbosa-38465938

## ✅ Lista de Verificação

- [ ] Python 3.8+ instalado
- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas
- [ ] Teste básico executado
- [ ] Interface gráfica funcionando
- [ ] Primeira tradução realizada

**🎉 Parabéns! O NeuroTranslator PT-EN está pronto para uso!**

---

*Desenvolvido por Flávio Henrique Barbosa | © 2025 - Licença MIT*