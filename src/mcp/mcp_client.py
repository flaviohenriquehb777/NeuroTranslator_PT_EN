"""
Cliente MCP (Model Context Protocol) para NeuroTranslator
Conecta com serviços remotos de IA para processamento avançado
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
import aiohttp
import openai
from datetime import datetime

class MCPClient:
    """Cliente para conectar com serviços MCP remotos"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializar cliente MCP
        
        Args:
            config: Configurações dos serviços
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Configurações dos serviços
        self.openai_api_key = self.config.get("openai_api_key", "")
        self.azure_endpoint = self.config.get("azure_endpoint", "")
        self.azure_api_key = self.config.get("azure_api_key", "")
        
        # Cliente OpenAI
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Estatísticas
        self.stats = {
            "requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0
        }
    
    async def process_natural_language(self, text: str, context: str = "") -> Dict[str, Any]:
        """
        Processar linguagem natural usando serviços remotos
        
        Args:
            text: Texto para processar
            context: Contexto adicional
            
        Returns:
            Resultado do processamento
        """
        try:
            self.stats["requests"] += 1
            
            # Prompt para entender comandos de tradução
            system_prompt = """
            Você é o assistente Neuro do NeuroTranslator. Analise o comando do usuário e extraia:
            1. Idioma de origem (se especificado)
            2. Idioma de destino
            3. Texto a ser traduzido
            4. Tipo de comando (tradução, detecção de idioma, etc.)
            
            Responda sempre em JSON com as chaves: source_lang, target_lang, text_to_translate, command_type, confidence
            """
            
            user_prompt = f"Comando: {text}\nContexto: {context}"
            
            # Usar OpenAI GPT para processamento
            if self.openai_api_key:
                response = await self._call_openai_api(system_prompt, user_prompt)
            else:
                # Fallback para processamento local
                response = self._process_locally(text)
            
            self.stats["successful_requests"] += 1
            return response
            
        except Exception as e:
            self.stats["failed_requests"] += 1
            self.logger.error(f"Erro no processamento NLP: {e}")
            return self._create_error_response(str(e))
    
    async def _call_openai_api(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Chamar API do OpenAI"""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            self.stats["total_tokens"] += response.usage.total_tokens
            
            # Tentar parsear JSON
            try:
                result = json.loads(content)
                return {
                    "success": True,
                    "data": result,
                    "source": "openai",
                    "timestamp": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                return self._process_locally(user_prompt)
                
        except Exception as e:
            self.logger.error(f"Erro na API OpenAI: {e}")
            return self._process_locally(user_prompt)
    
    def _process_locally(self, text: str) -> Dict[str, Any]:
        """Processamento local como fallback"""
        # Análise simples de padrões
        text_lower = text.lower()
        
        # Detectar idiomas
        source_lang = "auto"
        target_lang = "en"
        
        if "inglês" in text_lower or "english" in text_lower:
            target_lang = "en"
        elif "português" in text_lower or "portuguese" in text_lower:
            target_lang = "pt"
        elif "espanhol" in text_lower or "spanish" in text_lower:
            target_lang = "es"
        elif "francês" in text_lower or "french" in text_lower:
            target_lang = "fr"
        
        # Extrair texto após "frase:" ou similar
        text_to_translate = ""
        if "frase:" in text_lower:
            text_to_translate = text.split("frase:")[-1].strip()
        elif "texto:" in text_lower:
            text_to_translate = text.split("texto:")[-1].strip()
        else:
            # Tentar extrair após "traduza"
            parts = text.split("traduza")
            if len(parts) > 1:
                remaining = parts[-1]
                # Remover "para o inglês" etc.
                for lang in ["para o inglês", "para inglês", "to english", "para português", "to portuguese"]:
                    remaining = remaining.replace(lang, "")
                text_to_translate = remaining.strip()
        
        return {
            "success": True,
            "data": {
                "source_lang": source_lang,
                "target_lang": target_lang,
                "text_to_translate": text_to_translate,
                "command_type": "translation",
                "confidence": 0.7
            },
            "source": "local",
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_error_response(self, error_msg: str) -> Dict[str, Any]:
        """Criar resposta de erro"""
        return {
            "success": False,
            "error": error_msg,
            "data": {
                "source_lang": "auto",
                "target_lang": "en",
                "text_to_translate": "",
                "command_type": "error",
                "confidence": 0.0
            },
            "source": "error",
            "timestamp": datetime.now().isoformat()
        }
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detectar idioma do texto
        
        Args:
            text: Texto para análise
            
        Returns:
            Idioma detectado e confiança
        """
        try:
            # Usar serviços remotos se disponíveis
            if self.openai_api_key:
                prompt = f"Detecte o idioma do seguinte texto e responda apenas com o código do idioma (pt, en, es, fr): '{text}'"
                
                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=10,
                    temperature=0.1
                )
                
                detected_lang = response.choices[0].message.content.strip().lower()
                
                return {
                    "success": True,
                    "language": detected_lang,
                    "confidence": 0.9,
                    "source": "openai"
                }
            
            # Fallback local
            return self._detect_language_locally(text)
            
        except Exception as e:
            self.logger.error(f"Erro na detecção de idioma: {e}")
            return self._detect_language_locally(text)
    
    def _detect_language_locally(self, text: str) -> Dict[str, Any]:
        """Detecção local de idioma"""
        # Palavras comuns por idioma
        portuguese_words = ["o", "a", "de", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", "se", "na", "por", "mais"]
        english_words = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at"]
        spanish_words = ["el", "la", "de", "que", "y", "a", "en", "un", "es", "se", "no", "te", "lo", "le", "da", "su", "por", "son", "con", "para"]
        french_words = ["le", "de", "et", "à", "un", "il", "être", "et", "en", "avoir", "que", "pour", "dans", "ce", "son", "une", "sur", "avec", "ne", "se"]
        
        text_lower = text.lower()
        words = text_lower.split()
        
        scores = {
            "pt": sum(1 for word in words if word in portuguese_words),
            "en": sum(1 for word in words if word in english_words),
            "es": sum(1 for word in words if word in spanish_words),
            "fr": sum(1 for word in words if word in french_words)
        }
        
        detected_lang = max(scores, key=scores.get)
        confidence = scores[detected_lang] / len(words) if words else 0
        
        return {
            "success": True,
            "language": detected_lang,
            "confidence": min(confidence, 0.8),  # Máximo 80% para detecção local
            "source": "local"
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do cliente"""
        return {
            **self.stats,
            "success_rate": self.stats["successful_requests"] / max(self.stats["requests"], 1),
            "timestamp": datetime.now().isoformat()
        }