"""
Sistema de Reconhecimento de Fala (ASR) do NeuroTranslator PT-EN
Converte áudio em texto usando modelos de deep learning
"""

import numpy as np
import time
from typing import Optional, Dict, Any, List
import warnings
warnings.filterwarnings("ignore")

try:
    import librosa
    import torch
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ Bibliotecas de áudio não encontradas. Execute: pip install librosa torch transformers")

from ..utils.logger import default_logger as logger

class SpeechRecognizer:
    """Sistema de reconhecimento de fala"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializar reconhecedor de fala
        
        Args:
            config: Configurações do sistema
        """
        self.config = config or {}
        self.model = None
        self.processor = None
        self.is_loaded = False
        
        # Configurações de áudio
        self.sample_rate = self.config.get("sample_rate", 16000)
        self.chunk_size = self.config.get("chunk_size", 1024)
        
        # Estatísticas
        self.stats = {
            "recognitions": 0,
            "total_time": 0.0,
            "errors": 0
        }
        
        logger.info("SpeechRecognizer inicializado")
    
    def load_model(self, model_name: str = "openai/whisper-base") -> bool:
        """
        Carregar modelo de reconhecimento de fala
        
        Args:
            model_name: Nome do modelo Whisper
        
        Returns:
            True se carregado com sucesso
        """
        if not AUDIO_AVAILABLE:
            logger.error("Bibliotecas de áudio não disponíveis")
            return False
        
        try:
            logger.info(f"Carregando modelo de ASR: {model_name}")
            
            # Carregar processador e modelo
            self.processor = WhisperProcessor.from_pretrained(model_name)
            self.model = WhisperForConditionalGeneration.from_pretrained(model_name)
            
            # Configurar dispositivo
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(device)
            
            self.is_loaded = True
            logger.info(f"Modelo ASR carregado com sucesso no {device}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo ASR: {e}")
            return False
    
    def recognize_from_file(self, audio_file: str, language: str = "pt") -> Dict[str, Any]:
        """
        Reconhecer fala de arquivo de áudio
        
        Args:
            audio_file: Caminho do arquivo de áudio
            language: Código do idioma (pt, en)
        
        Returns:
            Resultado do reconhecimento
        """
        if not self.is_loaded:
            if not self.load_model():
                return {"error": "Modelo não carregado"}
        
        start_time = time.time()
        
        try:
            # Carregar áudio
            audio, sr = librosa.load(audio_file, sr=self.sample_rate)
            
            # Reconhecer
            result = self._recognize_audio(audio, language)
            
            # Atualizar estatísticas
            processing_time = time.time() - start_time
            self.stats["recognitions"] += 1
            self.stats["total_time"] += processing_time
            
            result["processing_time"] = processing_time
            result["file"] = audio_file
            
            logger.info(f"Reconhecimento concluído em {processing_time:.3f}s")
            return result
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Erro no reconhecimento: {e}")
            return {"error": str(e)}
    
    def recognize_from_array(self, audio_array: np.ndarray, language: str = "pt") -> Dict[str, Any]:
        """
        Reconhecer fala de array numpy
        
        Args:
            audio_array: Array de áudio
            language: Código do idioma
        
        Returns:
            Resultado do reconhecimento
        """
        if not self.is_loaded:
            if not self.load_model():
                return {"error": "Modelo não carregado"}
        
        start_time = time.time()
        
        try:
            # Reconhecer
            result = self._recognize_audio(audio_array, language)
            
            # Atualizar estatísticas
            processing_time = time.time() - start_time
            self.stats["recognitions"] += 1
            self.stats["total_time"] += processing_time
            
            result["processing_time"] = processing_time
            
            return result
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Erro no reconhecimento: {e}")
            return {"error": str(e)}
    
    def _recognize_audio(self, audio: np.ndarray, language: str) -> Dict[str, Any]:
        """
        Reconhecer áudio usando modelo Whisper
        
        Args:
            audio: Array de áudio
            language: Código do idioma
        
        Returns:
            Resultado do reconhecimento
        """
        try:
            # Preprocessar áudio
            inputs = self.processor(
                audio,
                sampling_rate=self.sample_rate,
                return_tensors="pt"
            )
            
            # Mover para dispositivo
            device = next(self.model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Gerar transcrição
            with torch.no_grad():
                predicted_ids = self.model.generate(
                    inputs["input_features"],
                    language=language,
                    task="transcribe"
                )
            
            # Decodificar resultado
            transcription = self.processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]
            
            # Calcular confiança (simulada)
            confidence = self._calculate_confidence(transcription)
            
            return {
                "text": transcription.strip(),
                "language": language,
                "confidence": confidence,
                "model": "whisper"
            }
            
        except Exception as e:
            raise Exception(f"Erro na transcrição: {e}")
    
    def _calculate_confidence(self, text: str) -> float:
        """
        Calcular confiança da transcrição (simulada)
        
        Args:
            text: Texto transcrito
        
        Returns:
            Valor de confiança (0-1)
        """
        # Simulação simples baseada no comprimento e caracteres
        if not text or len(text.strip()) < 3:
            return 0.1
        
        # Fatores que aumentam confiança
        factors = []
        
        # Comprimento adequado
        length_score = min(len(text) / 50, 1.0)
        factors.append(length_score)
        
        # Presença de palavras comuns
        common_words_pt = ["o", "a", "de", "que", "e", "do", "da", "em", "um", "para"]
        common_words_en = ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to"]
        
        words = text.lower().split()
        common_count = sum(1 for word in words if word in common_words_pt + common_words_en)
        common_score = min(common_count / len(words), 1.0) if words else 0
        factors.append(common_score)
        
        # Ausência de caracteres estranhos
        clean_score = 1.0 - (sum(1 for c in text if not c.isalnum() and c not in " .,!?-'") / len(text))
        factors.append(max(clean_score, 0.1))
        
        # Média dos fatores
        confidence = sum(factors) / len(factors)
        return max(0.1, min(0.95, confidence))
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obter estatísticas do reconhecimento
        
        Returns:
            Estatísticas do sistema
        """
        avg_time = (
            self.stats["total_time"] / self.stats["recognitions"]
            if self.stats["recognitions"] > 0 else 0
        )
        
        return {
            "recognitions": self.stats["recognitions"],
            "total_time": self.stats["total_time"],
            "avg_time": avg_time,
            "errors": self.stats["errors"],
            "success_rate": (
                (self.stats["recognitions"] - self.stats["errors"]) / self.stats["recognitions"]
                if self.stats["recognitions"] > 0 else 0
            ),
            "model_loaded": self.is_loaded
        }
    
    def simulate_recognition(self, duration: float = 2.0, language: str = "pt") -> Dict[str, Any]:
        """
        Simular reconhecimento de fala para demonstração
        
        Args:
            duration: Duração simulada em segundos
            language: Idioma simulado
        
        Returns:
            Resultado simulado
        """
        import random
        
        # Textos de exemplo
        sample_texts = {
            "pt": [
                "Olá, como você está hoje?",
                "Este é um teste do sistema de reconhecimento de fala.",
                "O NeuroTranslator funciona muito bem.",
                "Tradução automática em tempo real.",
                "Inteligência artificial para todos."
            ],
            "en": [
                "Hello, how are you today?",
                "This is a test of the speech recognition system.",
                "The NeuroTranslator works very well.",
                "Real-time automatic translation.",
                "Artificial intelligence for everyone."
            ]
        }
        
        # Simular processamento
        time.sleep(min(duration, 1.0))
        
        # Selecionar texto aleatório
        texts = sample_texts.get(language, sample_texts["en"])
        text = random.choice(texts)
        
        # Atualizar estatísticas
        self.stats["recognitions"] += 1
        self.stats["total_time"] += duration
        
        return {
            "text": text,
            "language": language,
            "confidence": random.uniform(0.85, 0.98),
            "processing_time": duration,
            "model": "whisper-simulation"
        }