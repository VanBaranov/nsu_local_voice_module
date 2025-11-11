import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    """настройка логгера для всего приложения"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    #форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    #файловый обработчик с ротацией
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=5*1024*1024,  # 5 МБ
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # очистка старых обработчиков
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("=== Логирование инициализировано ===")