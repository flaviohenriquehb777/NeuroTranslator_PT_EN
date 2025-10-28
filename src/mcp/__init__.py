"""
Módulo MCP (Model Context Protocol) para NeuroTranslator
Integração com serviços remotos de IA e processamento de linguagem natural
"""

from .mcp_client import MCPClient
from .voice_assistant import NeuroVoiceAssistant

__all__ = ['MCPClient', 'NeuroVoiceAssistant']