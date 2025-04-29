"""
Luxortum - Ультра-швидка версія для запуску у Replit
Фокус на миттєвому відкритті порта 5000
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Базова відповідь для швидкого відкриття порту"""
    return jsonify({
        "status": "ready",
        "message": "Luxortum Server готовий до роботи",
        "service": "ultra_faster"
    })

@app.route('/hello')
def hello():
    """Маршрут для тестування"""
    return jsonify({
        "message": "Привіт від Luxortum!",
        "services": ["базовий", "швидкий", "мінімальний"],
        "priority": "відкриття порту"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)