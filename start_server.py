"""
Спрощений файл для запуску сервера Luxortum
"""
from app import app

if __name__ == '__main__':
    # Запускаємо сервер у спрощеному режимі без додаткової ініціалізації
    app.run(host='0.0.0.0', port=5000)