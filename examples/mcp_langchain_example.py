#!/usr/bin/env python3
"""
Exemplo de uso do MCP LangChain Adapters
Este script demonstra como integrar MCP servers com LangChain
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# Configuração para múltiplos servidores MCP
MCP_CONFIG = {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
        "transport": "stdio",
    },
    # Adicione mais servidores conforme necessário
}

async def example_single_server():
    """Exemplo com um único servidor MCP"""
    print("🔧 Exemplo: Servidor MCP Único")
    
    # Configuração do servidor
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "."],
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Inicializar conexão
                await session.initialize()
                
                # Carregar ferramentas MCP
                tools = await load_mcp_tools(session)
                print(f"✅ Carregadas {len(tools)} ferramentas MCP")
                
                # Listar ferramentas disponíveis
                for tool in tools:
                    print(f"  - {tool.name}: {tool.description}")
                
    except Exception as e:
        print(f"❌ Erro no servidor único: {e}")

async def example_multi_server():
    """Exemplo com múltiplos servidores MCP"""
    print("\n🔧 Exemplo: Múltiplos Servidores MCP")
    
    try:
        # Cliente para múltiplos servidores
        client = MultiServerMCPClient(MCP_CONFIG)
        
        # Carregar todas as ferramentas
        tools = await client.get_tools()
        print(f"✅ Carregadas {len(tools)} ferramentas de múltiplos servidores")
        
        # Listar ferramentas por servidor
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
            
        # Fechar conexões
        await client.close()
        
    except Exception as e:
        print(f"❌ Erro em múltiplos servidores: {e}")

async def example_with_agent():
    """Exemplo usando MCP tools com um agente LangGraph"""
    print("\n🤖 Exemplo: Agente com Ferramentas MCP")
    
    # Verificar se a chave da OpenAI está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY não configurada. Pulando exemplo do agente.")
        return
    
    try:
        # Cliente MCP
        client = MultiServerMCPClient(MCP_CONFIG)
        tools = await client.get_tools()
        
        if not tools:
            print("⚠️  Nenhuma ferramenta MCP disponível")
            return
        
        # Criar agente ReAct
        agent = create_react_agent("openai:gpt-4", tools)
        
        # Executar uma tarefa
        task = "Liste os arquivos no diretório atual"
        print(f"🎯 Executando tarefa: {task}")
        
        response = await agent.ainvoke({"messages": [{"role": "user", "content": task}]})
        print(f"🤖 Resposta do agente: {response}")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ Erro no agente: {e}")

async def check_mcp_installation():
    """Verificar se o MCP está instalado corretamente"""
    print("🔍 Verificando instalação do MCP...")
    
    try:
        import mcp
        import langchain_mcp_adapters
        import langgraph
        
        print("✅ Todas as dependências MCP estão instaladas:")
        print(f"  - mcp: ✅ Instalado")
        print(f"  - langchain-mcp-adapters: ✅ Instalado")
        print(f"  - langgraph: ✅ Instalado")
        
        return True
        
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

async def main():
    """Função principal"""
    print("🚀 Testando MCP LangChain Integration")
    print("=" * 50)
    
    # Verificar instalação
    if not await check_mcp_installation():
        print("\n💡 Para instalar as dependências:")
        print("pip install langchain-mcp-adapters langgraph 'langchain[openai]'")
        return
    
    # Executar exemplos
    await example_single_server()
    await example_multi_server()
    await example_with_agent()
    
    print("\n✅ Todos os exemplos executados!")
    print("\n💡 Próximos passos:")
    print("1. Configure OPENAI_API_KEY para usar o agente")
    print("2. Instale servidores MCP adicionais com 'npx'")
    print("3. Adicione mais servidores ao MCP_CONFIG")

if __name__ == "__main__":
    asyncio.run(main())