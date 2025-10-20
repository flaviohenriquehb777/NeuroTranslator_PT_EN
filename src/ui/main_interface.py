"""
Interface Gráfica Principal do NeuroTranslator PT-EN
Implementa GUI moderna usando CustomTkinter
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
from typing import Optional, Dict, Any

try:
    import customtkinter as ctk
except ImportError:
    print("⚠️ CustomTkinter não encontrado. Execute: pip install customtkinter")
    import tkinter as ctk

from ..translation.translator import NeuroTranslator
from ..utils.logger import setup_logger

class NeuroTranslatorGUI:
    """Interface gráfica principal do NeuroTranslator"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializar interface gráfica
        
        Args:
            config: Configurações da aplicação
        """
        self.config = config or {}
        self.translator = NeuroTranslator(config)
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Criar janela principal
        self.root = ctk.CTk()
        self.root.title("🧠 NeuroTranslator PT-EN v1.0")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Variáveis
        self.is_translating = False
        self.translation_history = []
        
        # Criar interface
        self.create_widgets()
        self.setup_layout()
        
        # Carregar modelo padrão
        self.translator.load_model("balanced")
    
    def create_widgets(self):
        """Criar widgets da interface"""
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        
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
            values=["Rápido", "Preciso", "Balanceado"],
            state="readonly",
            command=self.on_model_change
        )
        self.model_combo.set("Balanceado")
        
        # Frame de tradução
        self.translation_frame = ctk.CTkFrame(self.main_frame)
        
        # Texto de entrada
        self.input_label = ctk.CTkLabel(self.translation_frame, text="Texto para traduzir:")
        self.input_text = ctk.CTkTextbox(
            self.translation_frame,
            height=100
        )
        self.input_text.insert("0.0", "Digite ou cole o texto aqui...")
        
        # Botões de ação
        self.button_frame = ctk.CTkFrame(self.translation_frame)
        
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
        
        # Texto de saída
        self.output_label = ctk.CTkLabel(self.translation_frame, text="Tradução:")
        self.output_text = ctk.CTkTextbox(
            self.translation_frame,
            height=100,
            state="disabled"
        )
        
        # Frame de informações
        self.info_frame = ctk.CTkFrame(self.main_frame)
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(self.info_frame)
        self.progress_bar.set(0)
        
        # Labels de informação
        self.status_label = ctk.CTkLabel(
            self.info_frame,
            text="✅ Pronto para traduzir",
            font=ctk.CTkFont(size=12)
        )
        
        self.stats_label = ctk.CTkLabel(
            self.info_frame,
            text="Traduções: 0 | Tempo médio: 0.000s",
            font=ctk.CTkFont(size=10)
        )
        
        # Menu
        self.create_menu()
    
    def create_menu(self):
        """Criar menu da aplicação"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Abrir arquivo...", command=self.open_file)
        file_menu.add_command(label="Salvar tradução...", command=self.save_translation)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(label="Histórico", command=self.show_history)
        tools_menu.add_command(label="Estatísticas", command=self.show_stats)
        tools_menu.add_command(label="Configurações", command=self.show_settings)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)
        help_menu.add_command(label="Documentação", command=self.show_docs)
    
    def setup_layout(self):
        """Configurar layout da interface"""
        
        # Frame principal
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.title_label.pack(pady=(0, 20))
        
        # Frame de configurações
        self.config_frame.pack(fill="x", pady=(0, 10))
        
        # Layout das configurações
        self.source_lang_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.source_lang_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.target_lang_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.target_lang_combo.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        self.model_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.model_combo.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        
        # Configurar colunas
        for i in range(6):
            self.config_frame.grid_columnconfigure(i, weight=1)
        
        # Frame de tradução
        self.translation_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Layout da tradução
        self.input_label.pack(anchor="w", padx=10, pady=(10, 5))
        self.input_text.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botões
        self.button_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.translate_button.pack(side="left", padx=(0, 5))
        self.clear_button.pack(side="left", padx=5)
        self.swap_button.pack(side="left", padx=5)
        
        # Saída
        self.output_label.pack(anchor="w", padx=10, pady=(10, 5))
        self.output_text.pack(fill="x", padx=10, pady=(0, 10))
        
        # Frame de informações
        self.info_frame.pack(fill="x", pady=(0, 10))
        
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.status_label.pack(pady=2)
        self.stats_label.pack(pady=2)
    
    def translate_text(self):
        """Traduzir texto em thread separada"""
        if self.is_translating:
            return
        
        text = self.input_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Aviso", "Digite um texto para traduzir")
            return
        
        # Iniciar tradução em thread separada
        thread = threading.Thread(target=self._translate_worker, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _translate_worker(self, text: str):
        """Worker para tradução em background"""
        self.is_translating = True
        
        try:
            # Atualizar UI
            self.root.after(0, self._update_ui_translating, True)
            
            # Mapear idiomas
            source_lang = self._map_language(self.source_lang_combo.get(), to_code=True)
            target_lang = self._map_language(self.target_lang_combo.get(), to_code=True)
            
            # Traduzir
            result = self.translator.translate(text, source_lang, target_lang)
            
            # Atualizar UI com resultado
            self.root.after(0, self._update_translation_result, result)
            
        except Exception as e:
            self.root.after(0, self._show_error, f"Erro na tradução: {str(e)}")
        
        finally:
            self.is_translating = False
            self.root.after(0, self._update_ui_translating, False)
    
    def _update_ui_translating(self, translating: bool):
        """Atualizar UI durante tradução"""
        if translating:
            self.translate_button.configure(text="⏳ Traduzindo...", state="disabled")
            self.status_label.configure(text="🔄 Traduzindo...")
            self.progress_bar.set(0.5)
        else:
            self.translate_button.configure(text="🔄 Traduzir", state="normal")
            self.progress_bar.set(0)
    
    def _update_translation_result(self, result: Dict[str, Any]):
        """Atualizar resultado da tradução"""
        # Mostrar tradução
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result["translation"])
        self.output_text.configure(state="disabled")
        
        # Atualizar status
        confidence = result.get("confidence", 0) * 100
        time_ms = result.get("processing_time", 0) * 1000
        
        self.status_label.configure(
            text=f"✅ Tradução concluída | Confiança: {confidence:.1f}% | Tempo: {time_ms:.0f}ms"
        )
        
        # Adicionar ao histórico
        self.translation_history.append(result)
        
        # Atualizar estatísticas
        self._update_stats()
    
    def _update_stats(self):
        """Atualizar estatísticas na UI"""
        stats = self.translator.get_stats()
        self.stats_label.configure(
            text=f"Traduções: {stats['translations']} | Tempo médio: {stats['avg_time']:.3f}s"
        )
    
    def _show_error(self, message: str):
        """Mostrar erro na UI"""
        self.status_label.configure(text=f"❌ {message}")
        messagebox.showerror("Erro", message)
    
    def _map_language(self, lang_display: str, to_code: bool = True) -> str:
        """Mapear entre nomes de idiomas e códigos"""
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
        history_window = ctk.CTkToplevel(self.root)
        history_window.title("📚 Histórico de Traduções")
        history_window.geometry("600x400")
        
        # Lista de histórico
        history_text = ctk.CTkTextbox(history_window)
        history_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Adicionar traduções ao histórico
        for i, translation in enumerate(self.translation_history[-10:], 1):
            history_text.insert("end", f"{i}. {translation['original']} → {translation['translation']}\n\n")
    
    def show_stats(self):
        """Mostrar estatísticas detalhadas"""
        stats = self.translator.get_stats()
        
        stats_text = f"""
📊 Estatísticas do NeuroTranslator

Traduções realizadas: {stats['translations']}
Tempo total: {stats['total_time']:.3f}s
Tempo médio por tradução: {stats['avg_time']:.3f}s
Modelo atual: {self.translator.current_model or 'Nenhum'}

Histórico: {len(self.translation_history)} traduções salvas
        """
        
        messagebox.showinfo("Estatísticas", stats_text)
    
    def show_settings(self):
        """Mostrar configurações"""
        messagebox.showinfo("Configurações", "Configurações avançadas em desenvolvimento...")
    
    def show_about(self):
        """Mostrar informações sobre o programa"""
        about_text = """
🧠 NeuroTranslator PT-EN v1.0

Sistema de Tradução Automática em Tempo Real
Português ↔ English

Desenvolvido por: Flávio Henrique Barbosa
Email: flaviohenriquehb777@outlook.com
LinkedIn: https://www.linkedin.com/in/flávio-henrique-barbosa-38465938

Tecnologias utilizadas:
• Python 3.8+
• PyTorch & Transformers
• CustomTkinter
• Deep Learning Models

© 2025 - Licença MIT
        """
        
        messagebox.showinfo("Sobre", about_text)
    
    def show_docs(self):
        """Mostrar documentação"""
        messagebox.showinfo("Documentação", "Consulte o README.md no repositório do projeto")
    
    def run(self):
        """Executar aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()