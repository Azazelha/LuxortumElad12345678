"""
Найшвидша версія Luxortum для Replit
Абсолютний мінімум коду для максимальної швидкості запуску
"""
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

# Ініціалізуємо дуже простий стан світу в пам'яті
WORLD_STATE = {
    "mood": "neutral",
    "intensity": 0.5,
    "trend": "stable"
}

@app.route('/')
def index():
    """Повертає HTML-сторінку для швидкого відкриття порту"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Luxortum</title>
        <style>
            body { font-family: Arial; text-align: center; margin-top: 50px; }
            h1 { color: purple; }
        </style>
    </head>
    <body>
        <h1>Luxortum Server</h1>
        <p>Сервер запущено успішно!</p>
        <a href="/static/index.html">Перейти до основного додатку</a>
    </body>
    </html>
    """

@app.route('/static/<path:path>')
def serve_static(path):
    """Обслуговування статичних файлів"""
    return send_from_directory('static', path)

@app.route('/api/health')
def health():
    """Перевірка стану сервера"""
    return jsonify({"status": "ok"})

@app.route('/api/world-mood')
def world_mood():
    """Базовий API-маршрут для отримання настрою світу"""
    return jsonify(WORLD_STATE)

if __name__ == '__main__':
    # Повідомляємо про швидкий запуск
    print("Luxortum fast server starting...")
    app.run(host='0.0.0.0', port=5000, threaded=True)