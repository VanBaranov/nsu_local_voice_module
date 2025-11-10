import requests
import logging
import tempfile
import os
from config import Config
from typing import Dict
from faster_whisper import WhisperModel

class STTService:
    def __init__(self):
        self.ngu_server_url = Config.NGU_SERVER_URL # URL сервера НГУ
        self._init_local_models()
    
    def _init_local_models(self):
        """Инициализация локальной модели Whisper"""
        try:
            self.model_whisper = WhisperModel(Config.WHISPER_MODEL_PATH, device=Config.WHISPER_DEVICE, compute_type="int8")
            logging.info("Локальная Whisper модель загружена")
        except Exception as e:
            logging.warning(f"Не удалось загрузить Whisper: {e}")
    
    def transcribe(self, audio_path: str) -> Dict:
        """
        Основной метод транскрибации с авто-переключением
        """
        # Сначала пробуем сервер НГУ
        if self._is_ngu_server_available():
            try:
                return self._transcribe_via_ngu(audio_path)
            except Exception as e:
                logging.warning(f"Сервер НГУ недоступен: {e}")
        
        # Fallback на локальную модель
        return self._transcribe_local(audio_path)
    
    def _is_ngu_server_available(self) -> bool:
        """Проверка доступности сервера НГУ"""
        try:
            response = requests.get(f"{self.ngu_server_url}/health", timeout=3)
            return response.status_code == 200
        except:
            #print('Чет не доступен сервер - се ля ви :()')
            return False
    
    def _transcribe_via_ngu(self, audio_path: str) -> Dict:
        """Транскрибация через сервер НГУ"""
        with open(audio_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.ngu_server_url}/stt",
                files=files,
                timeout=10
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Server error: {response.status_code}")
    
    def _transcribe_local(self, audio_path: str) -> Dict:
        """Локальная транскрибация с Whisper"""
        segments, info = self.model_whisper.transcribe(
            audio_path,
            beam_size=5
        )
        
        text = " ".join([segment.text for segment in segments])
        
        return {
            "text": text.strip(),
            "language": info.language
        }
