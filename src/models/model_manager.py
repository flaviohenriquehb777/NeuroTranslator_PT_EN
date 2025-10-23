"""
Gerenciador de Modelos do NeuroTranslator PT-EN
Responsável por carregar, cachear e gerenciar modelos de IA
"""

import os
import pickle
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    """Gerenciador de modelos de tradução e IA"""
    
    def __init__(self, cache_dir: str = "models/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_models: Dict[str, Any] = {}
        
    def get_model_path(self, model_name: str) -> Path:
        """Retorna o caminho para o cache do modelo"""
        return self.cache_dir / f"{model_name}.pkl"
        
    def load_model(self, model_name: str, model_loader_func=None) -> Any:
        """
        Carrega um modelo, usando cache se disponível
        
        Args:
            model_name: Nome do modelo
            model_loader_func: Função para carregar o modelo se não estiver em cache
            
        Returns:
            Modelo carregado
        """
        if model_name in self.loaded_models:
            logger.info(f"Modelo {model_name} já carregado na memória")
            return self.loaded_models[model_name]
            
        cache_path = self.get_model_path(model_name)
        
        # Tentar carregar do cache
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    model = pickle.load(f)
                self.loaded_models[model_name] = model
                logger.info(f"Modelo {model_name} carregado do cache")
                return model
            except Exception as e:
                logger.warning(f"Erro ao carregar modelo do cache: {e}")
                
        # Carregar modelo usando função fornecida
        if model_loader_func:
            try:
                model = model_loader_func()
                self.loaded_models[model_name] = model
                self.cache_model(model_name, model)
                logger.info(f"Modelo {model_name} carregado e cacheado")
                return model
            except Exception as e:
                logger.error(f"Erro ao carregar modelo {model_name}: {e}")
                raise
                
        raise ValueError(f"Não foi possível carregar o modelo {model_name}")
        
    def cache_model(self, model_name: str, model: Any) -> None:
        """
        Salva um modelo no cache
        
        Args:
            model_name: Nome do modelo
            model: Modelo a ser cacheado
        """
        try:
            cache_path = self.get_model_path(model_name)
            with open(cache_path, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"Modelo {model_name} salvo no cache")
        except Exception as e:
            logger.warning(f"Erro ao cachear modelo {model_name}: {e}")
            
    def clear_cache(self, model_name: Optional[str] = None) -> None:
        """
        Limpa o cache de modelos
        
        Args:
            model_name: Nome específico do modelo (None para limpar tudo)
        """
        if model_name:
            cache_path = self.get_model_path(model_name)
            if cache_path.exists():
                cache_path.unlink()
                logger.info(f"Cache do modelo {model_name} removido")
            if model_name in self.loaded_models:
                del self.loaded_models[model_name]
        else:
            # Limpar todo o cache
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()
            self.loaded_models.clear()
            logger.info("Todo o cache de modelos foi limpo")
            
    def get_cache_size(self) -> int:
        """Retorna o tamanho total do cache em bytes"""
        total_size = 0
        for cache_file in self.cache_dir.glob("*.pkl"):
            total_size += cache_file.stat().st_size
        return total_size
        
    def list_cached_models(self) -> list:
        """Lista todos os modelos em cache"""
        return [f.stem for f in self.cache_dir.glob("*.pkl")]