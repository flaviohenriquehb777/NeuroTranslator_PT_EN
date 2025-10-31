# Configuração MCP LangChain no Trae

## ✅ Status da Instalação
- **MCP Core**: ✅ Instalado
- **LangChain MCP Adapters**: ✅ Instalado  
- **LangGraph**: ✅ Instalado
- **Node.js**: ✅ v24.11.0
- **npm**: ✅ v11.6.1

## 📁 Arquivos Criados
- `mcp_config.json` - Configuração dos servidores MCP
- `mcp_langchain_example.py` - Exemplo de uso
- `TRAE_MCP_SETUP.md` - Este guia

## 🔧 Configuração no Trae

### Método 1: Usando o arquivo JSON
1. Abra as configurações do Trae
2. Vá para a seção MCP
3. Importe o arquivo `mcp_config.json`

### Método 2: Configuração Manual
Adicione esta configuração nas configurações do Trae:

```json
{
  "mcpServers": {
    "langchain-tools": {
      "command": "python",
      "args": ["-m", "mcp.server.fastmcp"],
      "transport": "stdio",
      "description": "LangChain MCP Tools Server"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "transport": "stdio",
      "description": "File system operations"
    }
  }
}
```

## 🚀 Testando a Instalação

Execute o script de teste:
```bash
python mcp_langchain_example.py
```

## 🛠️ Servidores MCP Disponíveis

### Já Instalados
- **filesystem**: Operações de arquivo
- **langchain-tools**: Ferramentas LangChain

### Servidores Adicionais (via npm)
```bash
# Busca web
npx -y @modelcontextprotocol/server-brave-search

# SQLite
npx -y @modelcontextprotocol/server-sqlite

# Git
npx -y @modelcontextprotocol/server-git

# Puppeteer (automação web)
npx -y @modelcontextprotocol/server-puppeteer
```

## 🔑 Configuração de API Keys

Para usar serviços externos, configure as variáveis de ambiente:

```bash
# Para Brave Search
set BRAVE_API_KEY=sua_chave_aqui

# Para OpenAI (agentes)
set OPENAI_API_KEY=sua_chave_aqui

# Para Anthropic
set ANTHROPIC_API_KEY=sua_chave_aqui
```

## 📝 Exemplo de Uso no Código

```python
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient

# Configurar cliente MCP
config = {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
        "transport": "stdio",
    }
}

client = MultiServerMCPClient(config)
tools = await client.get_tools()

# Usar com LangGraph
from langgraph.prebuilt import create_react_agent
agent = create_react_agent("openai:gpt-4", tools)
```

## 🐛 Solução de Problemas

### Erro: "Module not found"
```bash
pip install langchain-mcp-adapters langgraph "langchain[openai]"
```

### Erro: "npx command not found"
- Certifique-se que Node.js está instalado
- Reinicie o terminal

### Erro: "Permission denied"
- Execute como administrador
- Verifique permissões de pasta

## 📚 Recursos Adicionais

- [Documentação MCP](https://modelcontextprotocol.io/)
- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
- [Servidores MCP Oficiais](https://github.com/modelcontextprotocol/servers)

## ✅ Próximos Passos

1. ✅ Instalar dependências Python
2. ✅ Criar arquivos de configuração
3. ✅ Testar instalação básica
4. 🔄 Configurar no Trae (aguardando sua ação)
5. ⏳ Testar integração completa
6. ⏳ Configurar API keys conforme necessário

---

**Status**: MCP LangChain instalado e pronto para uso no Trae! 🎉