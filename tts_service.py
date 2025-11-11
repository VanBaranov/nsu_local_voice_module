import requests
import logging
import tempfile
import os
from config import Config
import torch
import soundfile as sf
import wave
from piper import PiperVoice

class TTSService:
    def __init__(self):
        self.ngu_server_url = Config.NGU_SERVER_URL
        self.local_models = {}
        self._init_local_models()
    
    def _init_local_models(self):
        """инициализация локальных TTS моделей"""
        # для английского и китайского использую Piper TTS
        try:
            model_ru = PiperVoice.load(Config.PIPER_MODEL_PATH_RU)
            model_en = PiperVoice.load(Config.PIPER_MODEL_PATH_EN)
            model_zh = PiperVoice.load(Config.PIPER_MODEL_PATH_ZH)
            self.local_models['piper_ru'] = model_ru
            self.local_models['piper_en'] = model_en
            self.local_models['piper_zh'] = model_zh
            logging.info("Локальная Piper TTS модель загружена")
        except Exception as e:
            logging.warning(f"Не удалось загрузить Piper TTS: {e}")
    
    def synthesize(self, text: str, language: str) -> str:
        """
        Синтез речи с авто-переключением
        Возвращает путь к аудио файлу
        """
        # сначала пробую соединиться с сервером НГУ
        if self._is_ngu_server_available():
            logging.info("Сервер НГУ доступен для tts")
            try:
                return self._synthesize_via_ngu(text, language)
            except Exception as e:
                logging.warning(f"Сервер НГУ недоступен: {e}")
        
        # переключение на локальные модели, если сервер недоступен
        logging.info("Использую локальную модель для tts")
        return self._synthesize_local(text, language)
    
    def _is_ngu_server_available(self) -> bool:
        """Проверка доступности сервера НГУ"""
        try:
            response = requests.get(f"{self.ngu_server_url}/health", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def _synthesize_via_ngu(self, text: str, language: str) -> str:
        """Синтез через сервер НГУ"""
        data = {
            'text': text,
            'language': language
        }
        
        response = requests.post(
            f"{self.ngu_server_url}/tts",
            json=data,
            timeout=15
        )
        
        if response.status_code == 200:
            # Сохраняем полученное аудио
            output_path = tempfile.mktemp(suffix='.wav')
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return output_path
        else:
            if 'output_path' in locals() and os.path.exists(output_path):
                os.remove(output_path)
            raise Exception(f"Server error: {response.status_code}")
    
    def _synthesize_local(self, text: str, language: str) -> str:
        """Локальный синтез речи"""
        output_path = tempfile.mktemp(suffix='.wav')
        
        if language == 'ru':
            # Piper_ru модель для английского
            model = self.local_models['piper_ru']
            with wave.open(output_path, "wb") as wav_file:
                model.synthesize_wav(text, wav_file)
            return output_path
            '''
            # Silero модель для русского
            model = self.local_models['silero_ru']
            audio = model.apply_tts(text, speaker='kseniya', sample_rate=24000)
            sf.write(output_path, audio, 24000)
            return output_path
            '''
                
        elif language == 'en':
            # Piper_en модель для английского
            model = self.local_models['piper_en']
            with wave.open(output_path, "wb") as wav_file:
                model.synthesize_wav(text, wav_file)
            return output_path
        
        elif language == 'zh':
            # Piper_zh модель для китайского
            model = self.local_models['piper_zh']
            with wave.open(output_path, "wb") as wav_file:
                model.synthesize_wav(text, wav_file)
            return output_path

        else:
            raise Exception("Нет доступных TTS моделей для указанного языка")
    
