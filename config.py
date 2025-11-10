import os

class Config:
    # настройки сервера
    HOST = '127.0.0.1'
    PORT = 8000
    DEBUG = True
    
    # настройки сервера НГУ
    NGU_SERVER_URL = os.getenv('NGU_SERVER_URL', 'https://172.17.0.9:8000')
    
    #stt пути моделей
    WHISPER_MODEL_PATH = "/Users/ivan/Desktop/audio_nsu/models_stt/faster-whisper-base/"
    WHISPER_MODEL_SIZE = "small"  # base, small, medium, large
    WHISPER_DEVICE = "cpu"  # cpu or cuda
    
    #tts пути моделей
    SILERO_MODEL_PATH = "/Users/ivan/Desktop/audio_nsu/models_tts/silero_model.pt"
    PIPER_MODEL_PATH_EN = "/Users/ivan/Desktop/audio_nsu/models_tts/piper-model/en/ryan/en_US-ryan-high.onnx"
    PIPER_MODEL_PATH_ZH = "/Users/ivan/Desktop/audio_nsu/models_tts/piper-model/zh/huayan/zh_CN-huayan-medium.onnx"



    # настройки аудио
    AUDIO_SAMPLE_RATE = 16000
    SUPPORTED_LANGUAGES = ['ru', 'en', 'zh']
    
    # таймауты
    SERVER_TIMEOUT = 10
    HEALTH_CHECK_TIMEOUT = 3


'''
# Health check (GET)
curl http://localhost:8000/health

# STT 
curl -X POST -F "audio=@output.wav" http://localhost:8000/stt

# TTS
curl -X POST -H "Content-Type: application/json" -d '{"text":"Hello world, my name ", "language":"en"}' http://localhost:8000/tts --output output.wav

tts запрос на русском
curl -X POST -H "Content-Type: application/json" -d '{"text":"На сайте вы можете увидеть информацию по форуму Золотая Долина. Также в меню есть ответы на наиболее часто встречающиеся вопросы. Стратегия развития НГУ предполагает построение модели научно-технологического университета, значительную роль в котором, наряду с образованием и исследованиями, будут играть технологии. Поэтому мы заинтересованы в тесном взаимодействии с индустриальными партнерами, передовыми предприятиями и высокотехнологичными компаниями, что помогает нам разрабатывать продукты, сервисы и решения, которые находят применение в реальном секторе экономики. Научно-производственный форум Золотая долина является площадкой для общения, обмена опытом, выработки новых идей и совместных проектов, в которых принимают участие представители образования, науки и бизнеса.", "language":"ru"}' http://localhost:8000/tts --output output.wav

tts запрос английский
curl -X POST -H "Content-Type: application/json" -d '{"text":"On the website, you can find information about the Golden Valley Forum. There are also answers to the most frequently asked questions in the menu. The NSU development strategy involves building a model of a science and technology university, where technology will play a significant role alongside education and research. Therefore, we are interested in working closely with industrial partners, advanced enterprises, and high-tech companies to develop products, services, and solutions that can be applied in the real economy. The Golden Valley Science and Production Forum is a platform for communication, exchange of experience, and the development of new ideas and joint projects involving representatives of education, science, and business.", "language":"en"}' http://localhost:8000/tts --output output.wav

tts запрос на китайском
curl -X POST -H "Content-Type: application/json" -d '{"text":"在网站上，您可以找到有关黄金谷论坛的信息。 菜单中还有最常见的问题的答案。 新西伯利亚国立大学的发展战略包括建立一个科技大学的模式，技术将在教育和研究方面发挥重要作用。 因此，我们有兴趣与工业合作伙伴，先进企业和高科技公司密切合作，开发可应用于实体经济的产品，服务和解决方案。 金谷科学与生产论坛是一个交流、交流经验、发展新思想和联合项目的平台，涉及教育、科学和商业的代表。", "language":"zh"}' http://localhost:8000/tts --output output.wav



在网站上，您可以找到有关黄金谷论坛的信息。 菜单中还有最常见的问题的答案。 新西伯利亚国立大学的发展战略包括建立一个科技大学的模式，技术将在教育和研究方面发挥重要作用。 因此，我们有兴趣与工业合作伙伴，先进企业和高科技公司密切合作，开发可应用于实体经济的产品，服务和解决方案。 金谷科学与生产论坛是一个交流、交流经验、发展新思想和联合项目的平台，涉及教育、科学和商业的代表。
On the website, you can find information about the Golden Valley Forum. There are also answers to the most frequently asked questions in the menu. The NSU development strategy involves building a model of a science and technology university, where technology will play a significant role alongside education and research. Therefore, we are interested in working closely with industrial partners, advanced enterprises, and high-tech companies to develop products, services, and solutions that can be applied in the real economy. The Golden Valley Science and Production Forum is a platform for communication, exchange of experience, and the development of new ideas and joint projects involving representatives of education, science, and business.
'''