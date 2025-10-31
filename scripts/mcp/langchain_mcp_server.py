#!/usr/bin/env python3
"""
Servidor MCP personalizado para LangChain
"""

from fastmcp import FastMCP
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio
import json

# Criar servidor MCP
mcp = FastMCP("LangChain MCP Server")

@mcp.tool()
def get_langchain_info() -> str:
    """Obter informações sobre LangChain MCP Adapters instalado"""
    try:
        import langchain_mcp_adapters
        import langgraph
        return json.dumps({
            "status": "✅ LangChain MCP Adapters instalado",
            "langchain_mcp_adapters": "✅ Disponível",
            "langgraph": "✅ Disponível",
            "description": "Sistema pronto para usar ferramentas MCP com LangChain"
        }, indent=2)
    except ImportError as e:
        return json.dumps({
            "status": "❌ Erro na instalação",
            "error": str(e)
        }, indent=2)

@mcp.tool()
def list_available_tools() -> str:
    """Listar ferramentas MCP disponíveis"""
    tools_info = {
        "filesystem": "Operações de arquivo e diretório",
        "langchain": "Ferramentas LangChain integradas",
        "web_search": "Busca na web (requer API key)",
        "git": "Operações Git",
        "sqlite": "Operações de banco de dados SQLite"
    }
    
    return json.dumps({
        "available_tools": tools_info,
        "note": "Use 'npx -y @modelcontextprotocol/server-[nome]' para instalar"
    }, indent=2)

@mcp.tool()
def create_langchain_agent_example() -> str:
    """Criar exemplo de código para agente LangChain com MCP"""
    example_code = '''
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

# Configurar cliente MCP
config = {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
        "transport": "stdio",
    }
}

async def create_agent():
    client = MultiServerMCPClient(config)
    tools = await client.get_tools()
    
    # Criar agente ReAct
    agent = create_react_agent("openai:gpt-4", tools)
    
    # Usar o agente
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "Liste os arquivos Python no diretório atual"}]
    })
    
    return response
'''
    
    return json.dumps({
        "example_code": example_code,
        "requirements": [
            "pip install langchain-mcp-adapters",
            "pip install langgraph",
            "pip install 'langchain[openai]'",
            "export OPENAI_API_KEY=sua_chave_aqui"
        ]
    }, indent=2)

if __name__ == "__main__":
    mcp.run()