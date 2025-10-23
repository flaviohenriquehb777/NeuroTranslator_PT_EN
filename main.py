#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeuroTranslator PT-EN - Sistema de Tradução Automática em Tempo Real
Autor: Flávio Henrique Barbosa
Email: flaviohenriquehb777@outlook.com
LinkedIn: https://www.linkedin.com/in/flávio-henrique-barbosa-38465938

Script principal para executar o NeuroTranslator PT-EN
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.ui.main_interface import NeuroTranslatorGUI
    from src.utils.logger import setup_logger
    from src.utils.config import load_config
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("📋 Certifique-se de que todas as dependências estão instaladas:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

def parse_arguments():
    """Parse argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="NeuroTranslator PT-EN - Sistema de Tradução em Tempo Real",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                    # Executar interface gráfica
  python main.py --mode cli         # Executar em modo linha de comando
  python main.py --debug           # Executar com logs detalhados
  python main.py --config custom.yaml  # Usar arquivo de configuração personalizado
        """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["gui", "cli", "demo"], 
        default="gui",
        help="Modo de execução (padrão: gui)"
    )
    
    parser.add_argument(
        "--config", 
        type=str, 
        default="config/default.yaml",
        help="Arquivo de configuração (padrão: config/default.yaml)"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Ativar logs detalhados para debug"
    )
    
    parser.add_argument(
        "--lang-from", 
        choices=["pt", "en", "auto"], 
        default="auto",
        help="Idioma de origem (padrão: auto)"
    )
    
    parser.add_argument(
        "--lang-to", 
        choices=["pt", "en"], 
        default="en",
        help="Idioma de destino (padrão: en)"
    )
    
    parser.add_argument(
        "--model", 
        choices=["fast", "accurate", "balanced"], 
        default="balanced",
        help="Modelo de tradução (padrão: balanced)"
    )
    
    return parser.parse_args()

def setup_environment():
    """Configurar ambiente de execução"""
    # Criar diretórios necessários
    directories = [
        "logs",
        "models/cache",
        "data/temp",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Verificar dependências críticas (sem pandas para evitar erro pyarrow)
    try:
        import torch
        import transformers
        import customtkinter
        import numpy as np
        import cv2
        import speech_recognition
        print("✅ Dependências principais verificadas")
    except ImportError as e:
        print(f"❌ Dependência crítica não encontrada: {e}")
        print("📋 Execute: pip install -r requirements.txt")
        return False
    
    return True

def run_gui_mode(config, args):
    """Executar modo interface gráfica"""
    print("🚀 Iniciando NeuroTranslator - Interface Gráfica...")
    
    try:
        app = NeuroTranslatorGUI(config=config)
        app.mainloop()
    except Exception as e:
        logging.error(f"Erro na interface gráfica: {e}")
        print(f"❌ Erro ao executar interface: {e}")
        return False
    
    return True

def run_cli_mode(config, args):
    """Executar modo linha de comando"""
    print("🚀 Iniciando NeuroTranslator - Modo CLI...")
    
    try:
        from src.translation.translator import NeuroTranslator
        
        translator = NeuroTranslator(config=config)
        
        print(f"📝 Tradução {args.lang_from} → {args.lang_to}")
        print("💡 Digite 'quit' para sair")
        print("-" * 50)
        
        while True:
            try:
                text = input("📝 Digite o texto: ").strip()
                
                if text.lower() in ['quit', 'exit', 'sair']:
                    break
                
                if not text:
                    continue
                
                result = translator.translate(
                    text=text,
                    source_lang=args.lang_from,
                    target_lang=args.lang_to
                )
                
                print(f"🔄 Tradução: {result['translation']}")
                print(f"📊 Confiança: {result['confidence']:.2%}")
                print(f"⏱️ Tempo: {result['processing_time']:.3f}s")
                print("-" * 50)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Erro na tradução: {e}")
    
    except Exception as e:
        logging.error(f"Erro no modo CLI: {e}")
        print(f"❌ Erro ao executar CLI: {e}")
        return False
    
    return True

def run_demo_mode(config, args):
    """Executar modo demonstração"""
    print("🚀 Iniciando NeuroTranslator - Modo Demonstração...")
    
    try:
        from src.utils.demo import run_interactive_demo
        run_interactive_demo(config)
    except Exception as e:
        logging.error(f"Erro no modo demo: {e}")
        print(f"❌ Erro ao executar demo: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    print("🧠 NeuroTranslator PT-EN v1.0")
    print("=" * 50)
    
    # Parse argumentos
    args = parse_arguments()
    
    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logger(level=log_level)
    
    # Setup ambiente
    if not setup_environment():
        sys.exit(1)
    
    # Carregar configuração
    try:
        config = load_config(args.config)
        logging.info(f"Configuração carregada: {args.config}")
    except Exception as e:
        logging.error(f"Erro ao carregar configuração: {e}")
        print(f"❌ Erro na configuração: {e}")
        sys.exit(1)
    
    # Executar modo selecionado
    success = False
    
    try:
        if args.mode == "gui":
            success = run_gui_mode(config, args)
        elif args.mode == "cli":
            success = run_cli_mode(config, args)
        elif args.mode == "demo":
            success = run_demo_mode(config, args)
        
        if success:
            print("✅ NeuroTranslator executado com sucesso!")
        else:
            print("❌ Erro durante a execução")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 NeuroTranslator finalizado pelo usuário")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()