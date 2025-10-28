"""
Assistente de Voz Neuro para NeuroTranslator
Implementa detecção de wake word "Vamos, Neuro!" e processamento de comandos
"""

import asyncio
import threading
import time
import queue
import numpy as np
from typing import Dict, Any, Optional, Callable, List
import logging
from datetime import datetime

try:
    import speech_recognition as sr
    import pyttsx3
    import pyaudio
    from pydub import AudioSegment
    from pydub.playback import play
    import io
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Bibliotecas de voz não encontradas. Execute: pip install speechrecognition pyttsx3 pydub")

from .mcp_client import MCPClient
from ..utils.logger import default_logger as logger

class NeuroVoiceAssistant:
    """Assistente de voz inteligente do NeuroTranslator"""
    
    def __init__(self, config: Optional[Dict] = None, translator=None):
        """
        Inicializar assistente de voz
        
        Args:
            config: Configurações do assistente
            translator: Instância do tradutor
        """
        self.config = config or {}
        self.translator = translator
        self.logger = logging.getLogger(__name__)
        
        # Wake word
        self.wake_word = "vamos neuro"
        self.wake_word_alternatives = ["vamos nero", "vamo neuro", "vamos neural"]
        
        # Estados
        self.is_listening = False
        self.is_active = False
        self.wake_word_detected = False
        self.command_timeout = 10  # segundos
        
        # Componentes
        self.mcp_client = MCPClient(config)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone() if VOICE_AVAILABLE else None
        
        # TTS Engine
        self.tts_engine = None
        if VOICE_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self._configure_tts()
            except Exception as e:
                self.logger.error(f"Erro ao inicializar TTS: {e}")
        
        # Callbacks
        self.on_wake_word_detected = None
        self.on_command_processed = None
        self.on_translation_complete = None
        
        # Threads
        self.listen_thread = None
        self.command_queue = queue.Queue()
        
        # Estatísticas
        self.stats = {
            "wake_words_detected": 0,
            "commands_processed": 0,
            "translations_completed": 0,
            "errors": 0,
            "session_start": datetime.now().isoformat()
        }
    
    def _configure_tts(self):
        """Configurar engine de síntese de voz"""
        if not self.tts_engine:
            return
        
        try:
            # Configurar voz
            voices = self.tts_engine.getProperty('voices')
            
            # Tentar encontrar voz em português
            for voice in voices:
                if 'portuguese' in voice.name.lower() or 'brasil' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            # Configurar velocidade e volume
            self.tts_engine.setProperty('rate', 180)  # Palavras por minuto
            self.tts_engine.setProperty('volume', 0.8)  # Volume (0.0 a 1.0)
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar TTS: {e}")
    
    def start_listening(self):
        """Iniciar escuta contínua para wake word"""
        if not VOICE_AVAILABLE:
            self.logger.error("Bibliotecas de voz não disponíveis")
            return False
        
        if self.is_listening:
            return True
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        self.logger.info("🎤 Assistente Neuro iniciado - aguardando 'Vamos, Neuro!'")
        return True
    
    def stop_listening(self):
        """Parar escuta"""
        self.is_listening = False
        self.is_active = False
        
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2)
        
        self.logger.info("🔇 Assistente Neuro parado")
    
    def _listen_loop(self):
        """Loop principal de escuta"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while self.is_listening:
            try:
                # Escutar por wake word
                if not self.is_active:
                    self._listen_for_wake_word()
                else:
                    # Escutar comando após wake word
                    self._listen_for_command()
                
                time.sleep(0.1)  # Pequena pausa para evitar uso excessivo de CPU
                
            except Exception as e:
                self.logger.error(f"Erro no loop de escuta: {e}")
                self.stats["errors"] += 1
                time.sleep(1)
    
    def _listen_for_wake_word(self):
        """Escutar especificamente pelo wake word"""
        try:
            with self.microphone as source:
                # Escuta com timeout curto para wake word
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
            
            # Reconhecer áudio
            text = self.recognizer.recognize_google(audio, language="pt-BR").lower()
            
            # Verificar wake word
            if self._is_wake_word(text):
                self.wake_word_detected = True
                self.is_active = True
                self.stats["wake_words_detected"] += 1
                
                self.logger.info(f"🎯 Wake word detectado: '{text}'")
                
                # Callback
                if self.on_wake_word_detected:
                    self.on_wake_word_detected(text)
                
                # Resposta de confirmação
                self.speak("Olá! Como posso ajudar com a tradução?")
                
                # Iniciar timeout para comando
                threading.Timer(self.command_timeout, self._reset_active_state).start()
        
        except sr.WaitTimeoutError:
            pass  # Timeout normal, continuar escutando
        except sr.UnknownValueError:
            pass  # Não conseguiu reconhecer, continuar
        except Exception as e:
            self.logger.error(f"Erro ao escutar wake word: {e}")
    
    def _listen_for_command(self):
        """Escutar comando após wake word"""
        try:
            with self.microphone as source:
                # Escuta mais longa para comando completo
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=10)
            
            # Reconhecer comando
            command_text = self.recognizer.recognize_google(audio, language="pt-BR")
            
            self.logger.info(f"🎤 Comando recebido: '{command_text}'")
            
            # Processar comando
            asyncio.run(self._process_command(command_text))
            
        except sr.WaitTimeoutError:
            pass  # Timeout, continuar escutando
        except sr.UnknownValueError:
            self.speak("Desculpe, não consegui entender. Pode repetir?")
        except Exception as e:
            self.logger.error(f"Erro ao escutar comando: {e}")
            self.speak("Ocorreu um erro. Tente novamente.")
    
    def _is_wake_word(self, text: str) -> bool:
        """Verificar se o texto contém o wake word"""
        text_clean = text.lower().strip()
        
        # Verificar wake word principal
        if self.wake_word in text_clean:
            return True
        
        # Verificar alternativas
        for alternative in self.wake_word_alternatives:
            if alternative in text_clean:
                return True
        
        return False
    
    async def _process_command(self, command_text: str):
        """Processar comando de tradução"""
        try:
            self.stats["commands_processed"] += 1
            
            # Usar MCP para processar linguagem natural
            nlp_result = await self.mcp_client.process_natural_language(
                command_text, 
                context="Comando de tradução do assistente Neuro"
            )
            
            if not nlp_result["success"]:
                self.speak("Desculpe, não consegui processar seu comando.")
                return
            
            data = nlp_result["data"]
            text_to_translate = data.get("text_to_translate", "")
            target_lang = data.get("target_lang", "en")
            source_lang = data.get("source_lang", "auto")
            
            if not text_to_translate:
                self.speak("Não consegui identificar o texto para traduzir. Pode repetir?")
                return
            
            # Callback para processamento
            if self.on_command_processed:
                self.on_command_processed(command_text, data)
            
            # Realizar tradução
            await self._perform_translation(text_to_translate, source_lang, target_lang)
            
        except Exception as e:
            self.logger.error(f"Erro ao processar comando: {e}")
            self.speak("Ocorreu um erro ao processar seu comando.")
            self.stats["errors"] += 1
        finally:
            # Reset do estado ativo
            self._reset_active_state()
    
    async def _perform_translation(self, text: str, source_lang: str, target_lang: str):
        """Realizar tradução e falar resultado"""
        try:
            if not self.translator:
                self.speak("Tradutor não disponível no momento.")
                return
            
            # Detectar idioma se necessário
            if source_lang == "auto":
                detection_result = await self.mcp_client.detect_language(text)
                if detection_result["success"]:
                    source_lang = detection_result["language"]
            
            # Traduzir
            translation_result = self.translator.translate(
                text=text,
                source_lang=source_lang,
                target_lang=target_lang
            )
            
            if translation_result["success"]:
                translated_text = translation_result["translated_text"]
                confidence = translation_result.get("confidence", 0)
                
                # Falar tradução
                response = f"Tradução: {translated_text}"
                self.speak(response)
                
                # Callback
                if self.on_translation_complete:
                    self.on_translation_complete({
                        "original": text,
                        "translated": translated_text,
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                        "confidence": confidence
                    })
                
                self.stats["translations_completed"] += 1
                self.logger.info(f"✅ Tradução concluída: '{text}' -> '{translated_text}'")
                
            else:
                error_msg = translation_result.get("error", "Erro desconhecido")
                self.speak(f"Erro na tradução: {error_msg}")
                
        except Exception as e:
            self.logger.error(f"Erro na tradução: {e}")
            self.speak("Ocorreu um erro durante a tradução.")
            self.stats["errors"] += 1
    
    def speak(self, text: str):
        """Falar texto usando TTS"""
        if not self.tts_engine:
            self.logger.warning("TTS não disponível")
            return
        
        try:
            self.logger.info(f"🔊 Falando: '{text}'")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Erro no TTS: {e}")
    
    def _reset_active_state(self):
        """Reset do estado ativo após timeout"""
        self.is_active = False
        self.wake_word_detected = False
        self.logger.info("⏰ Timeout - voltando ao modo de escuta de wake word")
    
    def set_callbacks(self, 
                     on_wake_word_detected: Optional[Callable] = None,
                     on_command_processed: Optional[Callable] = None,
                     on_translation_complete: Optional[Callable] = None):
        """Definir callbacks para eventos"""
        self.on_wake_word_detected = on_wake_word_detected
        self.on_command_processed = on_command_processed
        self.on_translation_complete = on_translation_complete
    
    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do assistente"""
        return {
            **self.stats,
            "is_listening": self.is_listening,
            "is_active": self.is_active,
            "wake_word": self.wake_word,
            "voice_available": VOICE_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }
    
    def update_config(self, config: Dict[str, Any]):
        """Atualizar configurações"""
        self.config.update(config)
        
        # Atualizar wake word se especificado
        if "wake_word" in config:
            self.wake_word = config["wake_word"].lower()
        
        # Atualizar timeout
        if "command_timeout" in config:
            self.command_timeout = config["command_timeout"]