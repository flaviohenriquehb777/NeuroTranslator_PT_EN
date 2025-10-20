"""
Sistema de Logging do NeuroTranslator PT-EN
Configuração e gerenciamento de logs da aplicação
"""

import logging
import os
from datetime import datetime
from typing import Optional

def setup_logger(
    name: str = "NeuroTranslator",
    level: str = "INFO",
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configurar sistema de logging
    
    Args:
        name: Nome do logger
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Arquivo de log (opcional)
        console: Se deve mostrar logs no console
    
    Returns:
        Logger configurado
    """
    
    # Criar logger
    logger = logging.getLogger(name)
    
    # Garantir que level seja string
    if isinstance(level, int):
        level = logging.getLevelName(level)
    
    logger.setLevel(getattr(logging, level.upper()))
    
    # Limpar handlers existentes
    logger.handlers.clear()
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para console
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Handler para arquivo
    if log_file:
        # Criar diretório se não existir
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_default_log_file() -> str:
    """
    Obter caminho padrão do arquivo de log
    
    Returns:
        Caminho do arquivo de log
    """
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"logs/neurotranslator_{timestamp}.log"

# Logger padrão da aplicação
default_logger = setup_logger(
    name="NeuroTranslator",
    level="INFO",
    log_file=get_default_log_file(),
    console=True
)