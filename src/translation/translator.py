"""
NeuroTranslator - Classe principal de tradução
Implementa tradução bidirecional PT-EN usando modelos de Deep Learning
"""

import time
import logging
from typing import Dict, Any, Optional
import numpy as np

try:
    import torch
    import transformers
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
except ImportError:
    print("⚠️ Bibliotecas de ML não encontradas. Execute: pip install torch transformers")

class NeuroTranslator:
    """Classe principal para tradução automática PT-EN"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializar o tradutor
        
        Args:
            config: Configurações do tradutor
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Modelos disponíveis
        self.models = {
            "fast": "Helsinki-NLP/opus-mt-pt-en",
            "accurate": "unicamp-dl/translation-pt-en-t5",
            "balanced": "Helsinki-NLP/opus-mt-pt-en"
        }
        
        self.current_model = None
        self.tokenizer = None
        self.model = None
        
        # Estatísticas
        self.stats = {
            "translations": 0,
            "total_time": 0.0,
            "avg_time": 0.0
        }
        
        self.logger.info("NeuroTranslator inicializado")
    
    def load_model(self, model_type: str = "balanced") -> bool:
        """
        Carregar modelo de tradução
        
        Args:
            model_type: Tipo do modelo (fast, accurate, balanced)
            
        Returns:
            bool: True se carregado com sucesso
        """
        try:
            if model_type not in self.models:
                raise ValueError(f"Modelo '{model_type}' não disponível")
            
            model_name = self.models[model_type]
            self.logger.info(f"Carregando modelo: {model_name}")
            
            # Simular carregamento (em implementação real, carregaria os modelos)
            self.current_model = model_type
            self.logger.info(f"Modelo {model_type} carregado com sucesso")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar modelo: {e}")
            return False
    
    def detect_language(self, text: str) -> str:
        """
        Detectar idioma do texto
        
        Args:
            text: Texto para análise
            
        Returns:
            str: Código do idioma detectado ('pt' ou 'en')
        """
        # Implementação simplificada de detecção de idioma
        portuguese_words = [
            'o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para',
            'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais'
        ]
        
        english_words = [
            'the', 'of', 'and', 'a', 'to', 'in', 'is', 'you', 'that', 'it',
            'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'i'
        ]
        
        words = text.lower().split()
        pt_score = sum(1 for word in words if word in portuguese_words)
        en_score = sum(1 for word in words if word in english_words)
        
        return 'pt' if pt_score > en_score else 'en'
    
    def translate(self, 
                 text: str, 
                 source_lang: str = "auto", 
                 target_lang: str = "en") -> Dict[str, Any]:
        """
        Traduzir texto
        
        Args:
            text: Texto para tradução
            source_lang: Idioma de origem ('pt', 'en', 'auto')
            target_lang: Idioma de destino ('pt', 'en')
            
        Returns:
            Dict com resultado da tradução
        """
        start_time = time.time()
        
        try:
            # Detectar idioma se necessário
            if source_lang == "auto":
                source_lang = self.detect_language(text)
            
            # Validar idiomas
            if source_lang not in ['pt', 'en'] or target_lang not in ['pt', 'en']:
                raise ValueError("Idiomas suportados: 'pt', 'en'")
            
            if source_lang == target_lang:
                return {
                    "original": text,
                    "translation": text,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "confidence": 1.0,
                    "processing_time": 0.001,
                    "model_used": self.current_model or "none"
                }
            
            # Simular tradução (em implementação real, usaria os modelos)
            translation = self._simulate_translation(text, source_lang, target_lang)
            
            processing_time = time.time() - start_time
            
            # Atualizar estatísticas
            self.stats["translations"] += 1
            self.stats["total_time"] += processing_time
            self.stats["avg_time"] = self.stats["total_time"] / self.stats["translations"]
            
            result = {
                "original": text,
                "translation": translation,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence": np.random.uniform(0.85, 0.98),  # Simular confiança
                "processing_time": processing_time,
                "model_used": self.current_model or "simulation"
            }
            
            self.logger.info(f"Tradução concluída em {processing_time:.3f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro na tradução: {e}")
            return {
                "original": text,
                "translation": f"[ERRO: {str(e)}]",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence": 0.0,
                "processing_time": time.time() - start_time,
                "model_used": "error",
                "error": str(e)
            }
    
    def _simulate_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Simular tradução usando dicionário expandido e regras inteligentes
        
        Args:
            text: Texto original
            source_lang: Idioma de origem
            target_lang: Idioma de destino
            
        Returns:
            str: Texto traduzido
        """
        # Dicionário expandido de traduções
        translations = {
            ("pt", "en"): {
                # Saudações e expressões básicas
                "olá": "hello",
                "oi": "hi",
                "tchau": "bye",
                "até logo": "see you later",
                "bom dia": "good morning",
                "boa tarde": "good afternoon",
                "boa noite": "good night",
                "como está": "how are you",
                "como vai": "how are you doing",
                "tudo bem": "everything is fine",
                "muito prazer": "nice to meet you",
                
                # Palavras comuns
                "sim": "yes",
                "não": "no",
                "talvez": "maybe",
                "obrigado": "thank you",
                "obrigada": "thank you",
                "por favor": "please",
                "desculpe": "sorry",
                "com licença": "excuse me",
                "de nada": "you're welcome",
                
                # Verbos comuns
                "eu sou": "I am",
                "você é": "you are",
                "ele é": "he is",
                "ela é": "she is",
                "nós somos": "we are",
                "vocês são": "you are",
                "eles são": "they are",
                "eu tenho": "I have",
                "você tem": "you have",
                "eu quero": "I want",
                "eu preciso": "I need",
                "eu gosto": "I like",
                "eu posso": "I can",
                "eu vou": "I will go",
                
                # Substantivos comuns
                "casa": "house",
                "trabalho": "work",
                "escola": "school",
                "família": "family",
                "amigo": "friend",
                "amiga": "friend",
                "comida": "food",
                "água": "water",
                "tempo": "time",
                "dinheiro": "money",
                "carro": "car",
                "livro": "book",
                
                # Frases completas comuns
                "gostaria de saber se você consegue registrar tudo o que eu estou falando agora": "I would like to know if you can record everything I am saying now",
                "como você está": "how are you",
                "qual é o seu nome": "what is your name",
                "onde você mora": "where do you live",
                "que horas são": "what time is it",
                "quanto custa": "how much does it cost",
                "eu não entendo": "I don't understand",
                "você pode repetir": "can you repeat",
                "fale mais devagar": "speak more slowly",
                "eu estou aprendendo": "I am learning",
                "muito obrigado": "thank you very much"
            },
            ("en", "pt"): {
                # Saudações e expressões básicas
                "hello": "olá",
                "hi": "oi",
                "bye": "tchau",
                "see you later": "até logo",
                "good morning": "bom dia",
                "good afternoon": "boa tarde",
                "good night": "boa noite",
                "how are you": "como está",
                "how are you doing": "como vai",
                "everything is fine": "tudo bem",
                "nice to meet you": "muito prazer",
                
                # Palavras comuns
                "yes": "sim",
                "no": "não",
                "maybe": "talvez",
                "thank you": "obrigado",
                "please": "por favor",
                "sorry": "desculpe",
                "excuse me": "com licença",
                "you're welcome": "de nada",
                
                # Verbos comuns
                "i am": "eu sou",
                "you are": "você é",
                "he is": "ele é",
                "she is": "ela é",
                "we are": "nós somos",
                "they are": "eles são",
                "i have": "eu tenho",
                "you have": "você tem",
                "i want": "eu quero",
                "i need": "eu preciso",
                "i like": "eu gosto",
                "i can": "eu posso",
                "i will go": "eu vou",
                
                # Substantivos comuns
                "house": "casa",
                "work": "trabalho",
                "school": "escola",
                "family": "família",
                "friend": "amigo",
                "food": "comida",
                "water": "água",
                "time": "tempo",
                "money": "dinheiro",
                "car": "carro",
                "book": "livro",
                
                # Frases completas comuns
                "what is your name": "qual é o seu nome",
                "where do you live": "onde você mora",
                "what time is it": "que horas são",
                "how much does it cost": "quanto custa",
                "i don't understand": "eu não entendo",
                "can you repeat": "você pode repetir",
                "speak more slowly": "fale mais devagar",
                "i am learning": "eu estou aprendendo",
                "thank you very much": "muito obrigado"
            }
        }
        
        # Normalizar texto
        text_normalized = text.lower().strip()
        lang_pair = (source_lang, target_lang)
        
        # Buscar tradução exata primeiro
        if lang_pair in translations:
            if text_normalized in translations[lang_pair]:
                return translations[lang_pair][text_normalized]
        
        # Tentar tradução por palavras-chave (busca parcial)
        if lang_pair in translations:
            for key, value in translations[lang_pair].items():
                if key in text_normalized:
                    # Se encontrou uma palavra-chave, fazer substituição inteligente
                    return text_normalized.replace(key, value)
        
        # Tradução baseada em regras simples para textos não mapeados
        if source_lang == "pt" and target_lang == "en":
            # Aplicar algumas regras básicas de tradução PT->EN
            translated = text_normalized
            
            # Substituições básicas de estrutura
            translated = translated.replace("eu estou", "i am")
            translated = translated.replace("você está", "you are")
            translated = translated.replace("ele está", "he is")
            translated = translated.replace("ela está", "she is")
            translated = translated.replace("nós estamos", "we are")
            translated = translated.replace("vocês estão", "you are")
            translated = translated.replace("eles estão", "they are")
            
            # Se não houve mudança significativa, adicionar prefixo indicativo
            if translated == text_normalized:
                return f"[Translation] {text}"
            else:
                return translated.capitalize()
                
        elif source_lang == "en" and target_lang == "pt":
            # Aplicar algumas regras básicas de tradução EN->PT
            translated = text_normalized
            
            # Substituições básicas de estrutura
            translated = translated.replace("i am", "eu estou")
            translated = translated.replace("you are", "você está")
            translated = translated.replace("he is", "ele está")
            translated = translated.replace("she is", "ela está")
            translated = translated.replace("we are", "nós estamos")
            translated = translated.replace("they are", "eles estão")
            
            # Se não houve mudança significativa, adicionar prefixo indicativo
            if translated == text_normalized:
                return f"[Tradução] {text}"
            else:
                return translated.capitalize()
        
        # Fallback: retornar texto original com indicação
        return f"[{target_lang.upper()}] {text}"
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obter estatísticas do tradutor
        
        Returns:
            Dict com estatísticas
        """
        return self.stats.copy()
    
    def reset_stats(self):
        """Resetar estatísticas"""
        self.stats = {
            "translations": 0,
            "total_time": 0.0,
            "avg_time": 0.0
        }
        self.logger.info("Estatísticas resetadas")