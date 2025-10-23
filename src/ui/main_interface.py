"""
Interface Gráfica Principal do NeuroTranslator PT-EN
Implementa GUI moderna usando CustomTkinter com suporte a câmera e fala
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
import cv2
import numpy as np
from PIL import Image, ImageTk
from typing import Optional, Dict, Any
import logging

try:
    import customtkinter as ctk
except ImportError:
    print("⚠️ CustomTkinter não encontrado. Execute: pip install customtkinter")
    import tkinter as ctk

class NeuroTranslatorGUI(ctk.CTk):
    """Interface gráfica principal do NeuroTranslator"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Inicializar interface gráfica"""
        self.config = config or {}
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Inicializar janela principal
        super().__init__()
        self.title("🧠 NeuroTranslator PT-EN v1.0 - Live Camera & Speech")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Estados da aplicação
        self.camera_active = False
        self.speech_active = False
        self.live_translation_active = False
        self.is_translating = False
        self.translation_history = []
        self.current_video_frame = None
        
        # Componentes (inicialização lazy)
        self.camera_manager = None
        self.speech_recognizer = None
        self.translator = None
        
        # Inicializar variáveis de controle ANTES de criar widgets
        self.auto_translate_var = ctk.BooleanVar(value=True)  # Ativado por padrão
        
        # Criar interface
        self.create_widgets()
        self.setup_layout()
        
        # Log de inicialização
        if hasattr(logging, 'info'):
            logging.info("Interface gráfica inicializada")
        
        print("🚀 DEBUG: Interface gráfica inicializada - componentes serão carregados sob demanda")

    def _lazy_init_camera(self):
        """Inicialização lazy da câmera"""
        if self.camera_manager is None:
            print("🔍 DEBUG: Inicializando câmera pela primeira vez...")
            from ..camera.camera_manager import CameraManager
            self.camera_manager = CameraManager()
        return self.camera_manager

    def _lazy_init_speech(self):
        """Inicialização lazy do reconhecimento de fala"""
        if self.speech_recognizer is None:
            print("🔍 DEBUG: Inicializando reconhecimento de fala pela primeira vez...")
            from ..audio.speech_recognition import SpeechRecognizer
            self.speech_recognizer = SpeechRecognizer()
        return self.speech_recognizer

    def _lazy_init_translator(self):
        """Inicialização lazy do tradutor"""
        if self.translator is None:
            print("🔍 DEBUG: Inicializando tradutor pela primeira vez...")
            from ..translation.translator import NeuroTranslator
            self.translator = NeuroTranslator(config=self.config)
            # Carregar modelo padrão
            self.translator.load_model("balanced")
        return self.translator
    def create_widgets(self):
        """Criar widgets da interface"""
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="🧠 NeuroTranslator PT-EN",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        
        # Frame de configurações
        self.config_frame = ctk.CTkFrame(self.main_frame)
        
        # Seleção de idiomas
        self.source_lang_label = ctk.CTkLabel(self.config_frame, text="Idioma de origem:")
        self.source_lang_combo = ctk.CTkComboBox(
            self.config_frame,
            values=["Auto", "Português", "English"],
            state="readonly"
        )
        self.source_lang_combo.set("Auto")
        
        self.target_lang_label = ctk.CTkLabel(self.config_frame, text="Idioma de destino:")
        self.target_lang_combo = ctk.CTkComboBox(
            self.config_frame,
            values=["English", "Português"],
            state="readonly"
        )
        self.target_lang_combo.set("English")
        
        # Seleção de modelo
        self.model_label = ctk.CTkLabel(self.config_frame, text="Modelo:")
        self.model_combo = ctk.CTkComboBox(
            self.config_frame,
            values=["Balanceado", "Rápido", "Preciso"],
            state="readonly",
            command=self.on_model_change
        )
        self.model_combo.set("Balanceado")
        
        # Frame de entrada de texto
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_label = ctk.CTkLabel(self.input_frame, text="📝 Texto para traduzir:")
        self.input_text = ctk.CTkTextbox(self.input_frame, height=120)
        
        # Frame de botões
        self.button_frame = ctk.CTkFrame(self.main_frame)
        
        self.translate_button = ctk.CTkButton(
            self.button_frame,
            text="🔄 Traduzir",
            command=self.translate_text,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="🗑️ Limpar",
            command=self.clear_text,
            fg_color="gray"
        )
        
        self.swap_button = ctk.CTkButton(
            self.button_frame,
            text="🔄 Inverter",
            command=self.swap_languages,
            fg_color="orange"
        )
        
        # Frame de saída
        self.output_frame = ctk.CTkFrame(self.main_frame)
        self.output_label = ctk.CTkLabel(self.output_frame, text="✅ Tradução:")
        self.output_text = ctk.CTkTextbox(self.output_frame, height=120, state="disabled")
        
        # Frame de funcionalidades ao vivo
        self.live_frame = ctk.CTkFrame(self.main_frame)
        self.live_title = ctk.CTkLabel(
            self.live_frame,
            text="🎥 Funcionalidades ao Vivo",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        # Botões de controle ao vivo
        self.live_controls_frame = ctk.CTkFrame(self.live_frame)
        
        self.camera_button = ctk.CTkButton(
            self.live_controls_frame,
            text="📹 Ativar Câmera",
            command=self.toggle_camera,
            fg_color="green"
        )
        
        self.speech_button = ctk.CTkButton(
            self.live_controls_frame,
            text="🎤 Ativar Fala",
            command=self.toggle_speech,
            fg_color="blue"
        )
        
        self.live_translate_button = ctk.CTkButton(
            self.live_controls_frame,
            text="⚡ Tradução ao Vivo",
            command=self.toggle_live_translation,
            fg_color="purple"
        )
        
        # Frame de vídeo
        self.video_frame = ctk.CTkFrame(self.live_frame)
        self.video_label = ctk.CTkLabel(
            self.video_frame,
            text="📹 Câmera desativada",
            width=320,
            height=240
        )
        
        # Status ao vivo
        self.live_status_label = ctk.CTkLabel(
            self.live_frame,
            text="Status: Aguardando ativação",
            font=ctk.CTkFont(size=12)
        )
        
        # Frame de menu
        self.menu_frame = ctk.CTkFrame(self.main_frame)
        
        self.open_file_button = ctk.CTkButton(
            self.menu_frame,
            text="📁 Abrir Arquivo",
            command=self.open_file,
            width=120
        )
        
        self.save_button = ctk.CTkButton(
            self.menu_frame,
            text="💾 Salvar",
            command=self.save_translation,
            width=120
        )
        
        self.history_button = ctk.CTkButton(
            self.menu_frame,
            text="📚 Histórico",
            command=self.show_history,
            width=120
        )
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="✅ Pronto para traduzir",
            font=ctk.CTkFont(size=12)
        )
        
        # Checkbox para tradução automática
        self.auto_translate_checkbox = ctk.CTkCheckBox(
            self.button_frame,
            text="🔄 Tradução Automática",
            variable=self.auto_translate_var
        )
    
    def setup_layout(self):
        """Configurar layout da interface"""
        
        # Layout principal
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.title_label.pack(pady=(0, 20))
        
        # Configurações
        self.config_frame.pack(fill="x", pady=(0, 10))
        
        # Layout das configurações
        self.source_lang_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.source_lang_combo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        self.target_lang_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.target_lang_combo.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        
        self.model_label.grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.model_combo.grid(row=0, column=5, padx=10, pady=5, sticky="ew")
        
        # Configurar colunas
        for i in range(6):
            self.config_frame.grid_columnconfigure(i, weight=1)
        
        # Entrada de texto
        self.input_frame.pack(fill="x", pady=(0, 10))
        self.input_label.pack(anchor="w", padx=10, pady=(10, 5))
        self.input_text.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botões
        self.button_frame.pack(fill="x", pady=(0, 10))
        self.translate_button.pack(side="left", padx=(10, 5))
        self.clear_button.pack(side="left", padx=5)
        self.swap_button.pack(side="left", padx=5)
        self.auto_translate_checkbox.pack(side="right", padx=10)
        
        # Saída
        self.output_frame.pack(fill="x", pady=(0, 10))
        self.output_label.pack(anchor="w", padx=10, pady=(10, 5))
        self.output_text.pack(fill="x", padx=10, pady=(0, 10))
        
        # Funcionalidades ao vivo
        self.live_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.live_title.pack(pady=(10, 10))
        
        # Controles ao vivo
        self.live_controls_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.camera_button.pack(side="left", padx=5)
        self.speech_button.pack(side="left", padx=5)
        self.live_translate_button.pack(side="left", padx=5)
        
        # Vídeo
        self.video_frame.pack(side="left", padx=10, pady=10)
        self.video_label.pack(padx=10, pady=10)
        
        # Status ao vivo
        self.live_status_label.pack(pady=5)
        
        # Menu
        self.menu_frame.pack(fill="x", pady=(0, 10))
        self.open_file_button.pack(side="left", padx=5)
        self.save_button.pack(side="left", padx=5)
        self.history_button.pack(side="left", padx=5)
        
        # Status
        self.status_label.pack(pady=5)
    
    def translate_text(self):
        """Traduzir texto inserido"""
        text = self.input_text.get("1.0", "end-1c").strip()
        
        print(f"🔄 DEBUG: translate_text chamado com texto: '{text}'")
        
        if not text:
            messagebox.showwarning("Aviso", "Digite um texto para traduzir")
            return
        
        # Inicializar tradutor se necessário
        self._lazy_init_translator()
        
        # Obter idiomas selecionados
        source_lang = self._map_language(self.source_lang_combo.get(), to_code=True)
        target_lang = self._map_language(self.target_lang_combo.get(), to_code=True)
        
        print(f"🔄 DEBUG: Idiomas - origem: {source_lang}, destino: {target_lang}")
        
        # Iniciar tradução em thread separada
        self.is_translating = True
        self.translate_button.configure(text="⏳ Traduzindo...", state="disabled")
        self.status_label.configure(text="🔄 Traduzindo...")
        
        thread = threading.Thread(
            target=self._translate_worker,
            args=(text, source_lang, target_lang),
            daemon=True
        )
        thread.start()
    
    def _translate_worker(self, text: str, source_lang: str, target_lang: str):
        """Worker thread para tradução"""
        try:
            print(f"🔄 DEBUG: _translate_worker iniciado - texto: '{text}', {source_lang} -> {target_lang}")
            
            start_time = time.time()
            
            # Realizar tradução
            result = self.translator.translate(
                text=text,
                source_lang=source_lang,
                target_lang=target_lang
            )
            
            print(f"🔄 DEBUG: Resultado da tradução: {result}")
            
            processing_time = time.time() - start_time
            
            # Atualizar interface na thread principal
            self.after(0, self._update_translation_result, result, processing_time)
            
        except Exception as e:
            print(f"❌ DEBUG: Erro no _translate_worker: {e}")
            import traceback
            traceback.print_exc()
            error_msg = f"Erro na tradução: {str(e)}"
            self.after(0, self._update_translation_error, error_msg)
    
    def _update_translation_result(self, result: Dict[str, Any], processing_time: float):
        """Atualizar resultado da tradução na interface"""
        try:
            # Atualizar texto de saída
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result["translation"])
            self.output_text.configure(state="disabled")
            
            # Atualizar status
            confidence = result.get("confidence", 0.0)
            status_text = f"✅ Traduzido em {processing_time:.2f}s (Confiança: {confidence:.1%})"
            self.status_label.configure(text=status_text)
            
            # Adicionar ao histórico
            self.translation_history.append({
                "original": self.input_text.get("1.0", "end-1c"),
                "translation": result["translation"],
                "confidence": confidence,
                "time": processing_time,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
        except Exception as e:
            self._update_translation_error(f"Erro ao atualizar resultado: {str(e)}")
        
        finally:
            # Reativar botão
            self.is_translating = False
            self.translate_button.configure(text="🔄 Traduzir", state="normal")
    
    def _update_translation_error(self, error_msg: str):
        """Atualizar interface com erro de tradução"""
        self.status_label.configure(text=f"❌ {error_msg}")
        self.is_translating = False
        self.translate_button.configure(text="🔄 Traduzir", state="normal")
        messagebox.showerror("Erro", error_msg)
    
    def _map_language(self, lang_display: str, to_code: bool = True) -> str:
        """Mapear idioma entre display e código"""
        mapping = {
            "Auto": "auto",
            "Português": "pt",
            "English": "en",
            "Rápido": "fast",
            "Preciso": "accurate",
            "Balanceado": "balanced"
        }
        
        reverse_mapping = {v: k for k, v in mapping.items()}
        
        if to_code:
            return mapping.get(lang_display, lang_display.lower())
        else:
            return reverse_mapping.get(lang_display, lang_display)
    
    def on_model_change(self, model_name: str):
        """Callback para mudança de modelo"""
        model_code = self._map_language(model_name, to_code=True)
        self.translator.load_model(model_code)
        self.status_label.configure(text=f"📊 Modelo alterado para: {model_name}")
    
    def clear_text(self):
        """Limpar textos"""
        self.input_text.delete("1.0", "end")
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        self.status_label.configure(text="✅ Textos limpos")
    
    def swap_languages(self):
        """Inverter idiomas de origem e destino"""
        source = self.source_lang_combo.get()
        target = self.target_lang_combo.get()
        
        if source != "Auto":
            self.source_lang_combo.set(target)
            self.target_lang_combo.set(source)
            
            # Trocar textos também
            input_text = self.input_text.get("1.0", "end-1c")
            output_text = self.output_text.get("1.0", "end-1c")
            
            if output_text:
                self.input_text.delete("1.0", "end")
                self.input_text.insert("1.0", output_text)
                
                self.output_text.configure(state="normal")
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", input_text)
                self.output_text.configure(state="disabled")
            
            self.status_label.configure(text="🔄 Idiomas invertidos")
    
    def open_file(self):
        """Abrir arquivo de texto"""
        file_path = filedialog.askopenfilename(
            title="Abrir arquivo",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("1.0", content)
                    self.status_label.configure(text=f"📁 Arquivo carregado: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir arquivo: {str(e)}")
    
    def save_translation(self):
        """Salvar tradução em arquivo"""
        translation = self.output_text.get("1.0", "end-1c")
        if not translation:
            messagebox.showwarning("Aviso", "Nenhuma tradução para salvar")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salvar tradução",
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(translation)
                    self.status_label.configure(text=f"💾 Tradução salva: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")
    
    def show_history(self):
        """Mostrar histórico de traduções"""
        if not self.translation_history:
            messagebox.showinfo("Histórico", "Nenhuma tradução no histórico")
            return
        
        # Criar janela de histórico
        history_window = ctk.CTkToplevel(self)
        history_window.title("📚 Histórico de Traduções")
        history_window.geometry("600x400")
        
        # Lista de histórico
        history_text = ctk.CTkTextbox(history_window, state="disabled")
        history_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Preencher histórico
        history_text.configure(state="normal")
        for i, entry in enumerate(reversed(self.translation_history[-10:]), 1):
            history_text.insert("end", f"{i}. [{entry['timestamp']}]\n")
            history_text.insert("end", f"   Original: {entry['original'][:100]}...\n")
            history_text.insert("end", f"   Tradução: {entry['translation'][:100]}...\n")
            history_text.insert("end", f"   Confiança: {entry['confidence']:.1%} | Tempo: {entry['time']:.2f}s\n\n")
        history_text.configure(state="disabled")
    
    def toggle_camera(self):
        """Ativar/desativar câmera"""
        print(f"🔍 DEBUG: Tentando {'ativar' if not self.camera_active else 'desativar'} câmera...")
        
        if not self.camera_active:
            # Ativar câmera
            print("🔍 DEBUG: Inicializando câmera...")
            camera_manager = self._lazy_init_camera()
            if camera_manager.start_capture(self.update_video_frame):
                self.camera_active = True
                self.camera_button.configure(text="📹 Desativar Câmera", fg_color="red")
                self.live_status_label.configure(text="Status: Câmera ativa")
                print("✅ DEBUG: Câmera ativada com sucesso!")
            else:
                print("❌ DEBUG: Falha ao ativar câmera")
                messagebox.showerror("Erro", "Não foi possível ativar a câmera.\n\nVerifique se:\n• A câmera não está sendo usada por outro programa\n• Os drivers da câmera estão instalados\n• Você tem permissão para acessar a câmera")
        else:
            # Desativar câmera
            print("🔍 DEBUG: Desativando câmera...")
            if self.camera_manager:
                self.camera_manager.stop_capture()
            self.camera_active = False
            self.camera_button.configure(text="📹 Ativar Câmera", fg_color="green")
            self.video_label.configure(text="📹 Câmera desativada", image=None)
            self.live_status_label.configure(text="Status: Câmera desativada")
            print("✅ DEBUG: Câmera desativada")
    
    def toggle_speech(self):
        """Ativar/desativar reconhecimento de fala"""
        print(f"🔍 DEBUG: Tentando {'ativar' if not self.speech_active else 'desativar'} reconhecimento de fala...")
        
        if not self.speech_active:
            # Ativar reconhecimento de fala
            print("🔍 DEBUG: Inicializando reconhecimento de fala...")
            speech_recognizer = self._lazy_init_speech()
            
            # Configurar idioma baseado na seleção atual
            current_lang = self._map_language(self.source_lang_combo.get(), to_code=True)
            recognition_lang = "pt-BR" if current_lang == "pt" else "en-US"
            
            print(f"🔍 DEBUG: Idioma de reconhecimento configurado: {recognition_lang}")
            
            if speech_recognizer.start_real_time_recognition(self.on_speech_recognized, recognition_lang):
                self.speech_active = True
                self.speech_button.configure(text="🎤 Desativar Fala", fg_color="red")
                self.live_status_label.configure(text="Status: Reconhecimento de fala ativo - Fale agora!")
                print("✅ DEBUG: Reconhecimento de fala ativado com sucesso!")
            else:
                print("❌ DEBUG: Falha ao ativar reconhecimento de fala")
                messagebox.showerror("Erro", "Não foi possível ativar o reconhecimento de fala.\n\nVerifique se:\n• O microfone está conectado e funcionando\n• Você tem permissão para acessar o microfone\n• As dependências de áudio estão instaladas\n\nTente executar: pip install pyaudio speech_recognition")
        else:
            # Desativar reconhecimento de fala
            print("🔍 DEBUG: Desativando reconhecimento de fala...")
            if self.speech_recognizer:
                self.speech_recognizer.stop_real_time_recognition()
            self.speech_active = False
            self.speech_button.configure(text="🎤 Ativar Fala", fg_color="blue")
            self.live_status_label.configure(text="Status: Reconhecimento de fala desativado")
            print("✅ DEBUG: Reconhecimento de fala desativado")

    def on_speech_recognized(self, text, confidence):
        """Callback para quando fala é reconhecida"""
        try:
            print(f"🔍 DEBUG: Fala reconhecida: '{text}' (confiança: {confidence:.2%})")
            
            # Inserir texto reconhecido no campo de entrada
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", text)
            
            # Detectar idioma automaticamente
            self._lazy_init_translator()
            detected_lang = self.translator.detect_language(text)
            print(f"🌐 DEBUG: Idioma detectado: {detected_lang}")
            
            # Atualizar seleção de idioma de origem automaticamente
            lang_display = "Português" if detected_lang == "pt" else "English"
            self.source_lang_combo.set(lang_display)
            
            # Definir idioma de destino automaticamente (oposto do detectado)
            target_lang_display = "English" if detected_lang == "pt" else "Português"
            self.target_lang_combo.set(target_lang_display)
            
            # Atualizar status
            self.status_label.configure(text=f"🎤 Fala reconhecida ({detected_lang.upper()}): {confidence:.1%} confiança")
            
            # Debug da checkbox de tradução automática
            auto_translate_enabled = self.auto_translate_var.get()
            print(f"🔄 DEBUG: Checkbox tradução automática: {auto_translate_enabled}")
            print(f"🔄 DEBUG: Tipo da variável: {type(self.auto_translate_var)}")
            
            # Traduzir automaticamente se habilitado
            if auto_translate_enabled:
                print("🔄 DEBUG: Tradução automática habilitada, iniciando tradução...")
                # Aguardar um pouco para garantir que a interface foi atualizada
                self.after(100, self.translate_text)
            else:
                print("🔄 DEBUG: Tradução automática desabilitada")
                
        except Exception as e:
            print(f"❌ DEBUG: Erro no callback de fala: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.configure(text=f"❌ Erro no reconhecimento: {str(e)}")

    def toggle_live_translation(self):
        """Ativar/desativar tradução ao vivo"""
        if not self.camera_active and not self.speech_active:
            messagebox.showwarning("Aviso", "Ative a câmera ou o reconhecimento de fala primeiro")
            return
            
        # Implementar lógica de tradução ao vivo
        self.live_status_label.configure(text="Status: Tradução ao vivo ativa")
    
    def update_video_frame(self, frame):
        """Atualizar frame de vídeo na interface"""
        try:
            # Redimensionar frame para caber na interface
            frame_resized = cv2.resize(frame, (320, 240))
            
            # Converter BGR para RGB
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            
            # Converter para PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Converter para PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            # Atualizar label de vídeo
            self.video_label.configure(image=photo, text="")
            self.video_label.image = photo  # Manter referência
            
        except Exception as e:
            print(f"❌ DEBUG: Erro ao atualizar frame de vídeo: {e}")
    
    def run(self):
        """Executar aplicação"""
        print("🚀 DEBUG: Iniciando interface gráfica...")
        try:
            self.mainloop()
        except Exception as e:
            print(f"❌ DEBUG: Erro na execução da interface: {e}")
            raise