"""
Gerenciador de Câmera do NeuroTranslator PT-EN
Responsável por capturar e processar vídeo em tempo real
"""

import cv2
import numpy as np
import threading
import time
from typing import Optional, Callable, Tuple
import logging

logger = logging.getLogger(__name__)

class CameraManager:
    """Gerenciador de câmera para captura de vídeo em tempo real"""
    
    def __init__(self, camera_index: int = 0, resolution: Tuple[int, int] = (640, 480)):
        """
        Inicializa o gerenciador de câmera
        
        Args:
            camera_index: Índice da câmera (0 para câmera padrão)
            resolution: Resolução do vídeo (largura, altura)
        """
        self.camera_index = camera_index
        self.resolution = resolution
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.current_frame: Optional[np.ndarray] = None
        self.frame_callback: Optional[Callable] = None
        self.capture_thread: Optional[threading.Thread] = None
        self.fps = 30
        
    def initialize_camera(self) -> bool:
        """
        Inicializa a câmera
        
        Returns:
            True se a câmera foi inicializada com sucesso
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                logger.error(f"Não foi possível abrir a câmera {self.camera_index}")
                return False
                
            # Configurar resolução
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Verificar se as configurações foram aplicadas
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            logger.info(f"Câmera inicializada: {actual_width}x{actual_height} @ {actual_fps}fps")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar câmera: {e}")
            return False
            
    def start_capture(self, frame_callback: Optional[Callable] = None) -> bool:
        """
        Inicia a captura de vídeo
        
        Args:
            frame_callback: Função chamada para cada frame capturado
            
        Returns:
            True se a captura foi iniciada com sucesso
        """
        if not self.cap or not self.cap.isOpened():
            if not self.initialize_camera():
                return False
                
        self.frame_callback = frame_callback
        self.is_running = True
        
        # Iniciar thread de captura
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        
        logger.info("Captura de vídeo iniciada")
        return True
        
    def stop_capture(self) -> None:
        """Para a captura de vídeo"""
        self.is_running = False
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2.0)
            
        if self.cap:
            self.cap.release()
            self.cap = None
            
        logger.info("Captura de vídeo parada")
        
    def _capture_loop(self) -> None:
        """Loop principal de captura de frames"""
        frame_time = 1.0 / self.fps
        
        while self.is_running and self.cap and self.cap.isOpened():
            start_time = time.time()
            
            ret, frame = self.cap.read()
            
            if not ret:
                logger.warning("Falha ao capturar frame")
                continue
                
            # Espelhar horizontalmente para efeito de espelho
            frame = cv2.flip(frame, 1)
            
            self.current_frame = frame.copy()
            
            # Chamar callback se fornecido
            if self.frame_callback:
                try:
                    self.frame_callback(frame)
                except Exception as e:
                    logger.error(f"Erro no callback de frame: {e}")
                    
            # Controlar FPS
            elapsed = time.time() - start_time
            sleep_time = max(0, frame_time - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
                
    def get_current_frame(self) -> Optional[np.ndarray]:
        """
        Retorna o frame atual
        
        Returns:
            Frame atual ou None se não disponível
        """
        return self.current_frame.copy() if self.current_frame is not None else None
        
    def capture_single_frame(self) -> Optional[np.ndarray]:
        """
        Captura um único frame
        
        Returns:
            Frame capturado ou None se falhou
        """
        if not self.cap or not self.cap.isOpened():
            if not self.initialize_camera():
                return None
                
        ret, frame = self.cap.read()
        
        if ret:
            return cv2.flip(frame, 1)  # Espelhar horizontalmente
        else:
            logger.warning("Falha ao capturar frame único")
            return None
            
    def is_camera_available(self) -> bool:
        """
        Verifica se a câmera está disponível
        
        Returns:
            True se a câmera está disponível
        """
        return self.cap is not None and self.cap.isOpened()
        
    def get_camera_info(self) -> dict:
        """
        Retorna informações sobre a câmera
        
        Returns:
            Dicionário com informações da câmera
        """
        if not self.is_camera_available():
            return {"available": False}
            
        return {
            "available": True,
            "index": self.camera_index,
            "width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": int(self.cap.get(cv2.CAP_PROP_FPS)),
            "is_running": self.is_running
        }
        
    def set_resolution(self, width: int, height: int) -> bool:
        """
        Define a resolução da câmera
        
        Args:
            width: Largura em pixels
            height: Altura em pixels
            
        Returns:
            True se a resolução foi definida com sucesso
        """
        if not self.is_camera_available():
            return False
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Verificar se foi aplicado
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        success = actual_width == width and actual_height == height
        if success:
            self.resolution = (width, height)
            logger.info(f"Resolução alterada para {width}x{height}")
        else:
            logger.warning(f"Resolução solicitada {width}x{height} não suportada, usando {actual_width}x{actual_height}")
            
        return success
        
    def __del__(self):
        """Destrutor para garantir limpeza de recursos"""
        self.stop_capture()