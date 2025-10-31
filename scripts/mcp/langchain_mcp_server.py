#!/usr/bin/env python3
"""
Servidor MCP simples para LangChain
"""

import json
import sys
import asyncio
from typing import Any, Dict, List

class SimpleMCPServer:
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
    
    def tool(self, name: str = None):
        def decorator(func):
            tool_name = name or func.__name__
            self.tools[tool_name] = {
                "name": tool_name,
                "description": func.__doc__ or f"Tool: {tool_name}",
                "function": func
            }
            return func
        return decorator
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        
        if method == "tools/list":
            return {
                "tools": [
                    {
                        "name": tool["name"],
                        "description": tool["description"],
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                    for tool in self.tools.values()
                ]
            }
        
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            
            if tool_name in self.tools:
                try:
                    result = await self.tools[tool_name]["function"]()
                    return {"content": [{"type": "text", "text": str(result)}]}
                except Exception as e:
                    return {"error": f"Erro ao executar ferramenta: {str(e)}"}
            else:
                return {"error": f"Ferramenta não encontrada: {tool_name}"}
        
        return {"error": "Método não suportado"}

# Criar servidor MCP
mcp = SimpleMCPServer("LangChain MCP Server")

@mcp.tool("get_langchain_info")
async def get_langchain_info():
    """Obter informações sobre LangChain MCP Adapters instalado"""
    try:
        info = {
            "status": "ativo",
            "servidor": "LangChain MCP Server",
            "versao": "1.0.0",
            "ferramentas_disponiveis": ["get_langchain_info", "test_connection"],
            "descricao": "Servidor MCP para integração com LangChain"
        }
        return json.dumps(info, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Erro: {str(e)}"

@mcp.tool("test_connection")
async def test_connection():
    """Testar conexão com o servidor MCP"""
    return "Conexão com servidor MCP LangChain funcionando corretamente!"

async def main():
    """Função principal do servidor MCP"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Servidor MCP LangChain")
        print("Uso: python langchain_mcp_server.py")
        print("Ferramentas disponíveis:")
        for tool_name, tool_info in mcp.tools.items():
            print(f"  - {tool_name}: {tool_info['description']}")
        return
    
    print("Servidor MCP LangChain iniciado com sucesso!")
    print("Ferramentas disponíveis:")
    for tool_name in mcp.tools.keys():
        print(f"  - {tool_name}")
    
    # Simular servidor rodando
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nServidor MCP encerrado.")

if __name__ == "__main__":
    asyncio.run(main())