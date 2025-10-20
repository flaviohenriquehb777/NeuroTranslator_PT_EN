"""
Sistema de Configurações do NeuroTranslator PT-EN
Gerenciamento de configurações da aplicação
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class Config:
    """Gerenciador de configurações da aplicação"""
    
    DEFAULT_CONFIG = {
        "app": {
            "name": "NeuroTranslator PT-EN",
            "version": "1.0.0",
            "author": "Flávio Henrique Barbosa",
            "email": "flaviohenriquehb777@outlook.com"
        },
        "translation": {
            "default_model": "balanced",
            "max_length": 512,
            "batch_size": 1,
            "cache_translations": True,
            "supported_languages": ["pt", "en"]
        },
        "models": {
            "fast": {
                "name": "Helsinki-NLP/opus-mt-pt-en",
                "type": "transformers",
                "max_length": 256
            },
            "accurate": {
                "name": "facebook/mbart-large-50-many-to-many-mmt",
                "type": "transformers", 
                "max_length": 512
            },
            "balanced": {
                "name": "Helsinki-NLP/opus-mt-mul-en",
                "type": "transformers",
                "max_length": 384
            }
        },
        "ui": {
            "theme": "dark",
            "color_theme": "blue",
            "window_size": "800x600",
            "min_size": "600x400",
            "font_size": 12
        },
        "audio": {
            "sample_rate": 16000,
            "chunk_size": 1024,
            "format": "wav",
            "channels": 1
        },
        "logging": {
            "level": "INFO",
            "console": True,
            "file": True,
            "max_files": 10
        },
        "performance": {
            "use_gpu": True,
            "max_workers": 4,
            "timeout": 30
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """Inicializa o gerenciador de configurações"""
        self.config_file = config_file or "config/config.json"
        self.config_path = Path(self.config_file)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self) -> None:
        """Carrega configurações do arquivo"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self._merge_config(self.config, user_config)
        except Exception as e:
            print(f"⚠️ Erro ao carregar configurações: {e}")
            print("📋 Usando configurações padrão")
    
    def save_config(self) -> None:
        """Salva configurações no arquivo"""
        try:
            # Criar diretório se não existir
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar configurações: {e}")
    
    def _merge_config(self, base: Dict, update: Dict) -> None:
        """Mescla configurações recursivamente"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração usando notação de ponto
        Exemplo: config.get('models.fast.name')
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Define valor de configuração usando notação de ponto
        Exemplo: config.set('ui.theme', 'light')
        """
        keys = key.split('.')
        config_ref = self.config
        
        # Navegar até o penúltimo nível
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        # Definir o valor final
        config_ref[keys[-1]] = value
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Obtém configuração de um modelo específico"""
        models = self.get('models', {})
        if model_name in models:
            return models[model_name]
        else:
            # Retornar modelo padrão se não encontrado
            default_model = self.get('translation.default_model', 'balanced')
            return models.get(default_model, models.get('balanced', {}))
    
    def get_supported_languages(self) -> list:
        """Obtém lista de idiomas suportados"""
        return self.get('translation.supported_languages', ['pt', 'en'])
    
    def is_gpu_enabled(self) -> bool:
        """Verifica se GPU está habilitada"""
        return self.get('performance.use_gpu', True)
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Obtém configurações da interface"""
        return self.get('ui', {})
    
    def get_audio_config(self) -> Dict[str, Any]:
        """Obtém configurações de áudio"""
        return self.get('audio', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Obtém configurações de logging"""
        return self.get('logging', {})
    
    def reset_to_defaults(self) -> None:
        """Restaura configurações padrão"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
    
    def __getitem__(self, key: str) -> Any:
        """Permite acesso via config['key']"""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Permite definição via config['key'] = value"""
        self.set(key, value)

# Instância global de configuração
config = Config()

def load_config(config_file: Optional[str] = None) -> Config:
    """Função para carregar configurações"""
    if config_file:
        return Config(config_file)
    return config
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Inicializar configurações
        
        Args:
            config_file: Arquivo de configuração (opcional)
        """
        self.config_file = config_file or "config.json"
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self) -> None:
        """Carregar configurações do arquivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self._merge_config(self.config, user_config)
            except Exception as e:
                print(f"⚠️ Erro ao carregar configurações: {e}")
                print("Usando configurações padrão")
    
    def save_config(self) -> None:
        """Salvar configurações no arquivo"""
        try:
            # Criar diretório se não existir
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar configurações: {e}")
    
    def _merge_config(self, base: Dict, update: Dict) -> None:
        """Mesclar configurações recursivamente"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obter valor de configuração usando notação de ponto
        
        Args:
            key: Chave da configuração (ex: "models.fast.name")
            default: Valor padrão se não encontrado
        
        Returns:
            Valor da configuração
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Definir valor de configuração usando notação de ponto
        
        Args:
            key: Chave da configuração (ex: "ui.theme")
            value: Novo valor
        """
        keys = key.split('.')
        config = self.config
        
        # Navegar até o penúltimo nível
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Definir valor
        config[keys[-1]] = value
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        Obter configuração de um modelo específico
        
        Args:
            model_name: Nome do modelo
        
        Returns:
            Configuração do modelo
        """
        return self.get(f"models.{model_name}", {})
    
    def get_supported_languages(self) -> list:
        """Obter lista de idiomas suportados"""
        return self.get("translation.supported_languages", ["pt", "en"])
    
    def is_gpu_enabled(self) -> bool:
        """Verificar se GPU está habilitada"""
        return self.get("performance.use_gpu", True)
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Obter configurações da interface"""
        return self.get("ui", {})
    
    def get_audio_config(self) -> Dict[str, Any]:
        """Obter configurações de áudio"""
        return self.get("audio", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Obter configurações de logging"""
        return self.get("logging", {})
    
    def reset_to_defaults(self) -> None:
        """Resetar configurações para os valores padrão"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
    
    def __getitem__(self, key: str) -> Any:
        """Permitir acesso via config[key]"""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Permitir definição via config[key] = value"""
        self.set(key, value)

# Instância global de configuração
config = Config()