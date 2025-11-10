from flask import Flask, Response, request, send_file, jsonify
import json
from stt_service import STTService
from tts_service import TTSService
import logging
import tempfile
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Инициализация сервисов
stt_service = STTService()
tts_service = TTSService()


def json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
        status=status
    )

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/stt', methods=['POST'])
def speech_to_text():
    """
    Распознавание речи из аудио
    Принимает: audio/wav файл
    Возвращает: {"text": "распознанный текст", "language": "ru"}
    """
    try:
        # проверяю наличие файла
        if 'audio' not in request.files:
            return json_response({"error": "No audio file provided"}, 400)
        
        audio_file = request.files['audio']
        
        # сохраняю временный файл
        temp_audio = tempfile.mktemp(suffix='.wav')
        audio_file.save(temp_audio)
        
        # распознается речь
        result = stt_service.transcribe(temp_audio)
        print(f"Распознанный текст: {result["text"]}")
        
        # удаляю временный файл
        os.unlink(temp_audio)
        
        return json_response({
            "text": result["text"],
            "language": result["language"]
        })
        
    except Exception as e:
        logging.error(f"STT error: {e}")
        return json_response({"error": str(e)}, 500)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    """
    Синтез речи из текста
    Принимает: {"text": "текст", "language": "ru"}
    Возвращает: audio/wav файл
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return json_response({"error": "No text provided"}, 400)
        
        text = data['text']
        language = data.get('language')  # ru, en, zh
        
        # синтезируется речь
        audio_path = tts_service.synthesize(text, language)
        
        return send_file(
            audio_path,
            as_attachment=True,
            download_name='response.wav',
            mimetype='audio/wav'
        )
        
    except Exception as e:
        logging.error(f"TTS error: {e}")
        return json_response({"error": str(e)}, 500)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)