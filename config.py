import os

# Базовая директория проекта — текущая директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # настройки сервера
    HOST = '127.0.0.1'
    PORT = 8000
    DEBUG = True
    
    # настройки сервера НГУ
    NGU_SERVER_URL = os.getenv('NGU_SERVER_URL', 'http://84.237.50.68:22900/')
    
    #stt пути моделей
    WHISPER_MODEL_PATH = BASE_DIR + "/audio_nsu/models_stt/faster-whisper-base/"
    WHISPER_MODEL_SIZE = "small"  # base, small, medium, large
    WHISPER_DEVICE = "cpu"  # cpu or cuda
    
    #tts пути моделей
    PIPER_MODEL_PATH_RU = BASE_DIR + "/audio_nsu/models_tts/piper-model/ru/irina/ru_RU-irina-medium.onnx"
    PIPER_MODEL_PATH_EN = BASE_DIR + "/audio_nsu/models_tts/piper-model/en/ryan/en_US-ryan-high.onnx"
    PIPER_MODEL_PATH_ZH = BASE_DIR + "/audio_nsu/models_tts/piper-model/zh/huayan/zh_CN-huayan-medium.onnx"

    # настройки аудио
    AUDIO_SAMPLE_RATE = 16000
    SUPPORTED_LANGUAGES = ['ru', 'en', 'zh']
    
    # таймауты
    SERVER_TIMEOUT = 10
    HEALTH_CHECK_TIMEOUT = 3

