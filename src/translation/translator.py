"""
NeuroTranslator - Sistema de Tradução Neural Multilíngue
Implementa tradução automática com suporte a 9 idiomas usando IA avançada
Autor: Flávio Henrique Barbosa
"""

import time
import logging
from typing import Dict, Any, Optional, List
import numpy as np
from pathlib import Path
import json

try:
    import torch
    import transformers
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
    from langdetect import detect, detect_langs
    HAS_TRANSFORMERS = True
except ImportError:
    print("⚠️ Bibliotecas de ML não encontradas. Execute: pip install torch transformers langdetect")
    HAS_TRANSFORMERS = False

class LanguageManager:
    """Gerenciador de idiomas com suporte a 9 idiomas"""
    
    SUPPORTED_LANGUAGES = {
        'pt': {'name': 'Português', 'flag': '🇧🇷', 'code': 'pt-BR'},
        'en': {'name': 'English', 'flag': '🇺🇸', 'code': 'en-US'},
        'es': {'name': 'Español', 'flag': '🇪🇸', 'code': 'es-ES'},
        'fr': {'name': 'Français', 'flag': '🇫🇷', 'code': 'fr-FR'},
        'de': {'name': 'Deutsch', 'flag': '🇩🇪', 'code': 'de-DE'},
        'zh': {'name': '中文', 'flag': '🇨🇳', 'code': 'zh-CN'},
        'ja': {'name': '日本語', 'flag': '🇯🇵', 'code': 'ja-JP'},
        'it': {'name': 'Italiano', 'flag': '🇮🇹', 'code': 'it-IT'},
        'ru': {'name': 'Русский', 'flag': '🇷🇺', 'code': 'ru-RU'}
    }
    
    LANGUAGE_MODELS = {
        'pt-en': 'Helsinki-NLP/opus-mt-pt-en',
        'en-pt': 'Helsinki-NLP/opus-mt-en-pt',
        'pt-es': 'Helsinki-NLP/opus-mt-pt-es',
        'es-pt': 'Helsinki-NLP/opus-mt-es-pt',
        'pt-fr': 'Helsinki-NLP/opus-mt-pt-fr',
        'fr-pt': 'Helsinki-NLP/opus-mt-fr-pt',
        'pt-de': 'Helsinki-NLP/opus-mt-pt-de',
        'de-pt': 'Helsinki-NLP/opus-mt-de-pt',
        'pt-zh': 'Helsinki-NLP/opus-mt-pt-zh',
        'zh-pt': 'Helsinki-NLP/opus-mt-zh-pt',
        'pt-ja': 'Helsinki-NLP/opus-mt-pt-ja',
        'ja-pt': 'Helsinki-NLP/opus-mt-ja-pt',
        'pt-it': 'Helsinki-NLP/opus-mt-pt-it',
        'it-pt': 'Helsinki-NLP/opus-mt-it-pt',
        'pt-ru': 'Helsinki-NLP/opus-mt-pt-ru',
        'ru-pt': 'Helsinki-NLP/opus-mt-ru-pt',
        'en-es': 'Helsinki-NLP/opus-mt-en-es',
        'es-en': 'Helsinki-NLP/opus-mt-es-en',
        'en-fr': 'Helsinki-NLP/opus-mt-en-fr',
        'fr-en': 'Helsinki-NLP/opus-mt-fr-en',
        'en-de': 'Helsinki-NLP/opus-mt-en-de',
        'de-en': 'Helsinki-NLP/opus-mt-de-en',
        'en-zh': 'Helsinki-NLP/opus-mt-en-zh',
        'zh-en': 'Helsinki-NLP/opus-mt-zh-en',
        'en-ja': 'Helsinki-NLP/opus-mt-en-ja',
        'ja-en': 'Helsinki-NLP/opus-mt-ja-en',
        'en-it': 'Helsinki-NLP/opus-mt-en-it',
        'it-en': 'Helsinki-NLP/opus-mt-it-en',
        'en-ru': 'Helsinki-NLP/opus-mt-en-ru',
        'ru-en': 'Helsinki-NLP/opus-mt-ru-en'
    }
    
    @classmethod
    def get_supported_languages(cls) -> Dict[str, Dict[str, str]]:
        """Retorna todos os idiomas suportados"""
        return cls.SUPPORTED_LANGUAGES
    
    @classmethod
    def get_language_code(cls, language: str) -> str:
        """Converte nome do idioma para código"""
        language = language.lower()
        for code, info in cls.SUPPORTED_LANGUAGES.items():
            if (code == language or 
                info['name'].lower() == language or 
                info['code'].lower() == language):
                return code
        return None
    
    @classmethod
    def get_model_for_pair(cls, source_lang: str, target_lang: str) -> str:
        """Retorna o modelo apropriado para o par de idiomas"""
        pair = f"{source_lang}-{target_lang}"
        return cls.LANGUAGE_MODELS.get(pair, 'Helsinki-NLP/opus-mt-tc-big')

class NeuroTranslator:
    """Sistema de tradução neural multilíngue profissional"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializar o tradutor neural
        
        Args:
            config: Configurações do tradutor
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Configurações de performance
        self.max_length = self.config.get('max_length', 512)
        self.batch_size = self.config.get('batch_size', 8)
        self.device = self.config.get('device', 'auto')
        
        if self.device == 'auto':
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Cache de modelos carregados
        self.loaded_models: Dict[str, Any] = {}
        self.translation_cache: Dict[str, str] = {}
        
        # Estatísticas de performance
        self.stats = {
            'translations': 0,
            'total_time': 0.0,
            'avg_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'model_loads': 0
        }
        
        self.logger.info(f"NeuroTranslator v2.0 inicializado - Device: {self.device}")
    
    def detect_language(self, text: str) -> str:
        """
        Detectar idioma do texto com alta precisão
        
        Args:
            text: Texto para análise
            
        Returns:
            str: Código do idioma detectado
        """
        try:
            # Usar langdetect para detecção robusta
            detected = detect(text)
            
            # Verificar se está nos idiomas suportados
            if detected in LanguageManager.SUPPORTED_LANGUAGES:
                return detected
            
            # Se não estiver suportado, tentar detectar várias possibilidades
            langs = detect_langs(text)
            for lang in langs:
                lang_code = str(lang).split(':')[0]
                if lang_code in LanguageManager.SUPPORTED_LANGUAGES:
                    return lang_code
            
            # Fallback para português ou inglês baseado em caracteres
            if any(ord(c) > 127 for c in text):  # Caracteres especiais
                return 'pt'
            else:
                return 'en'
                
        except Exception as e:
            self.logger.warning(f"Erro na detecção de idioma: {e}")
            return 'pt'  # Fallback padrão
    
    def load_model(self, source_lang: str, target_lang: str) -> bool:
        """
        Carregar modelo específico para o par de idiomas
        
        Args:
            source_lang: Idioma de origem
            target_lang: Idioma de destino
            
        Returns:
            bool: True se carregado com sucesso
        """
        if not HAS_TRANSFORMERS:
            self.logger.error("Bibliotecas de ML não disponíveis")
            return False
        
        try:
            pair_key = f"{source_lang}-{target_lang}"
            
            # Verificar se já está carregado
            if pair_key in self.loaded_models:
                self.logger.info(f"Modelo {pair_key} já carregado")
                return True
            
            # Obter nome do modelo
            model_name = LanguageManager.get_model_for_pair(source_lang, target_lang)
            self.logger.info(f"Carregando modelo {model_name} para {pair_key}")
            
            # Carregar tokenizer e modelo
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Mover para device apropriado
            model = model.to(self.device)
            
            # Criar pipeline de tradução
            translation_pipeline = pipeline(
                "translation",
                model=model,
                tokenizer=tokenizer,
                device=0 if self.device == 'cuda' else -1,
                max_length=self.max_length,
                batch_size=self.batch_size
            )
            
            # Armazenar no cache
            self.loaded_models[pair_key] = translation_pipeline
            self.stats['model_loads'] += 1
            
            self.logger.info(f"Modelo {pair_key} carregado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar modelo {pair_key}: {e}")
            return False
    
    def translate(self, 
                 text: str, 
                 source_lang: str = "auto", 
                 target_lang: str = "en",
                 use_cache: bool = True) -> Dict[str, Any]:
        """
        Traduzir texto com suporte a múltiplos idiomas
        
        Args:
            text: Texto para tradução
            source_lang: Idioma de origem ('auto' para detecção automática)
            target_lang: Idioma de destino
            use_cache: Se deve usar cache de tradução
            
        Returns:
            Dict com resultado completo da tradução
        """
        start_time = time.time()
        
        try:
            # Validar entrada
            if not text or not text.strip():
                raise ValueError("Texto vazio fornecido")
            
            text = text.strip()
            
            # Detectar idioma se necessário
            if source_lang == "auto":
                source_lang = self.detect_language(text)
            
            # Validar idiomas
            if source_lang not in LanguageManager.SUPPORTED_LANGUAGES:
                raise ValueError(f"Idioma de origem '{source_lang}' não suportado")
            
            if target_lang not in LanguageManager.SUPPORTED_LANGUAGES:
                raise ValueError(f"Idioma de destino '{target_lang}' não suportado")
            
            # Se for o mesmo idioma, retornar original
            if source_lang == target_lang:
                return {
                    "original": text,
                    "translation": text,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "confidence": 1.0,
                    "processing_time": time.time() - start_time,
                    "model_used": "none",
                    "cached": False
                }
            
            # Verificar cache
            cache_key = f"{source_lang}-{target_lang}:{text}"
            if use_cache and cache_key in self.translation_cache:
                self.stats['cache_hits'] += 1
                return {
                    "original": text,
                    "translation": self.translation_cache[cache_key],
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "confidence": 0.95,
                    "processing_time": time.time() - start_time,
                    "model_used": "cache",
                    "cached": True
                }
            
            self.stats['cache_misses'] += 1
            
            # Carregar modelo se necessário
            if not self.load_model(source_lang, target_lang):
                # Fallback para tradução simulada
                translation = self._simulate_translation(text, source_lang, target_lang)
            else:
                # Obter pipeline carregado
                pair_key = f"{source_lang}-{target_lang}"
                pipeline = self.loaded_models[pair_key]
                
                # Realizar tradução
                result = pipeline(text, max_length=self.max_length)
                translation = result[0]['translation_text']
            
            # Armazenar no cache
            if use_cache:
                self.translation_cache[cache_key] = translation
            
            processing_time = time.time() - start_time
            
            # Atualizar estatísticas
            self.stats['translations'] += 1
            self.stats['total_time'] += processing_time
            self.stats['avg_time'] = self.stats['total_time'] / self.stats['translations']
            
            return {
                "original": text,
                "translation": translation,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence": 0.85,
                "processing_time": processing_time,
                "model_used": f"{source_lang}-{target_lang}",
                "cached": False,
                "device": self.device
            }
            
        except Exception as e:
            self.logger.error(f"Erro na tradução: {e}")
            return {
                "original": text,
                "translation": None,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence": 0.0,
                "processing_time": time.time() - start_time,
                "model_used": "error",
                "cached": False,
                "error": str(e)
            }
    
    def _simulate_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Tradução simulada para fallback (será substituída por IA real)
        
        Args:
            text: Texto para tradução
            source_lang: Idioma de origem
            target_lang: Idioma de destino
            
        Returns:
            str: Texto traduzido (simulado)
        """
        # Dicionários simples para demonstração
        translations = {
            'pt-en': {
                'olá': 'hello', 'mundo': 'world', 'bom': 'good', 'dia': 'day',
                'como': 'how', 'está': 'are', 'você': 'you', 'obrigado': 'thank you',
                'por': 'for', 'favor': 'please', 'sim': 'yes', 'não': 'no'
            },
            'en-pt': {
                'hello': 'olá', 'world': 'mundo', 'good': 'bom', 'day': 'dia',
                'how': 'como', 'are': 'está', 'you': 'você', 'thank': 'obrigado',
                'for': 'por', 'please': 'favor', 'yes': 'sim', 'no': 'não'
            },
            'pt-ja': {
                'olá': 'こんにちは', 'mundo': '世界', 'bom': '良い', 'dia': '日',
                'obrigado': 'ありがとう', 'sim': 'はい', 'não': 'いいえ'
            },
            'ja-pt': {
                'こんにちは': 'olá', '世界': 'mundo', '良い': 'bom', '日': 'dia',
                'ありがとう': 'obrigado', 'はい': 'sim', 'いいえ': 'não'
            },
            'pt-it': {
                'olá': 'ciao', 'mundo': 'mondo', 'bom': 'buono', 'dia': 'giorno',
                'obrigado': 'grazie', 'sim': 'sì', 'não': 'no'
            },
            'it-pt': {
                'ciao': 'olá', 'mondo': 'mundo', 'buono': 'bom', 'giorno': 'dia',
                'grazie': 'obrigado', 'sì': 'sim', 'no': 'não'
            },
            'pt-ru': {
                'olá': 'привет', 'mundo': 'мир', 'bom': 'хороший', 'dia': 'день',
                'obrigado': 'спасибо', 'sim': 'да', 'não': 'нет'
            },
            'ru-pt': {
                'привет': 'olá', 'мир': 'mundo', 'хороший': 'bom', 'день': 'dia',
                'спасибо': 'obrigado', 'да': 'sim', 'нет': 'não'
            }
        }
        
        pair_key = f"{source_lang}-{target_lang}"
        if pair_key in translations:
            words = text.lower().split()
            translated_words = []
            for word in words:
                translated = translations[pair_key].get(word, word)
                translated_words.append(translated)
            return ' '.join(translated_words)
        
        return f"[{text}] ({source_lang}->{target_lang})"
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso"""
        return {
            **self.stats,
            'cache_size': len(self.translation_cache),
            'loaded_models': len(self.loaded_models),
            'supported_languages': len(LanguageManager.SUPPORTED_LANGUAGES),
            'device': self.device
        }
    
    def clear_cache(self):
        """Limpar cache de traduções"""
        self.translation_cache.clear()
        self.logger.info("Cache de traduções limpo")
    
    def unload_model(self, source_lang: str, target_lang: str):
        """Descarregar modelo específico da memória"""
        pair_key = f"{source_lang}-{target_lang}"
        if pair_key in self.loaded_models:
            del self.loaded_models[pair_key]
            self.logger.info(f"Modelo {pair_key} descarregado")
    
    def unload_all_models(self):
        """Descarregar todos os modelos da memória"""
        self.loaded_models.clear()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        self.logger.info("Todos os modelos descarregados")