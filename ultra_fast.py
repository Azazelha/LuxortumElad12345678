"""
Luxortum - Ультра-швидка версія для миттєвого запуску в Replit
Мінімальна функціональність для забезпечення відкриття порту протягом дозволеного часу
"""

from flask import Flask, jsonify, request, redirect, send_from_directory
import os
import random
import sqlite3
import json
import threading
import logging
from datetime import datetime

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("luxortum")

app = Flask(__name__)

@app.route('/')
def index():
    """Головна сторінка"""
    return redirect('/static/index.html')

@app.route('/hello')
def hello():
    """Простий маршрут для перевірки роботи сервера"""
    return jsonify({
        "message": "Привіт від Luxortum!",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/static/<path:path>')
def serve_static(path):
    """Обслуговування статичних файлів"""
    return send_from_directory('static', path)

@app.route('/health')
def health():
    """Перевірка стану сервера для моніторингу"""
    return jsonify({
        "status": "healthy",
        "version": "ultra-fast-1.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/world-mood', methods=['GET', 'POST'])
def api_world_mood():
    """
    API маршрут для отримання (GET) та оновлення (POST) настрою світу,
    використовуючи базу даних для зберігання стану.
    """
    if request.method == 'GET':
        # Отримуємо поточний настрій світу
        try:
            mood_data = get_world_mood()
            return jsonify(mood_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        # Оновлюємо настрій світу
        try:
            data = request.get_json()
            mood = data.get('mood', 'neutral')
            
            # Отримуємо поточний стан для оновлення
            current_mood = get_world_mood()
            
            # Оновлюємо настрій
            current_mood['mood'] = mood
            current_mood['last_update'] = datetime.now().timestamp() * 1000
            
            # Зберігаємо оновлений настрій
            save_world_mood(current_mood)
            
            # Зберігаємо запис в історії
            save_mood_history(mood, current_mood['intensity'])
            
            return jsonify({
                "status": "success",
                "message": f"Настрій світу змінено на: {mood}",
                "data": current_mood
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Помилка при оновленні настрою світу: {str(e)}"
            }), 500

@app.route('/api/run-autonomous-step', methods=['GET'])
def api_run_autonomous_step():
    """
    Запускає один крок автономної симуляції.
    Спрощена версія, яка не використовує OpenAI.
    """
    try:
        # Отримуємо поточний настрій світу
        current_mood_data = get_world_mood()
        
        # Генеруємо випадкову подію
        event = {
            "name": f"Подія #{random.randint(1000, 9999)}",
            "description": "Автоматично згенерована подія під час автономної симуляції",
            "impact": random.choice(["positive", "neutral", "negative"]),
            "intensity": random.uniform(0.1, 0.5),
            "timestamp": datetime.now().timestamp() * 1000
        }
        
        # Застосовуємо вплив події на настрій світу
        if event["impact"] == "positive":
            # Позитивна подія покращує настрій
            mood_levels = ["sad", "melancholic", "anxious", "neutral", 
                        "peaceful", "joyful", "ecstatic"]
            current_index = mood_levels.index(current_mood_data["mood"]) \
                            if current_mood_data["mood"] in mood_levels else 3  # за замовчуванням - нейтральний
            
            new_index = min(current_index + 1, len(mood_levels) - 1)
            current_mood_data["mood"] = mood_levels[new_index]
            current_mood_data["intensity"] = min(current_mood_data["intensity"] + event["intensity"] * 0.2, 1.0)
            current_mood_data["trend"] = "ascending"
        
        elif event["impact"] == "negative":
            # Негативна подія погіршує настрій
            mood_levels = ["chaotic", "angry", "sad", "melancholic", "anxious", 
                        "neutral", "peaceful", "joyful", "ecstatic"]
            current_index = mood_levels.index(current_mood_data["mood"]) \
                            if current_mood_data["mood"] in mood_levels else 5  # за замовчуванням - нейтральний
            
            new_index = max(current_index - 1, 0)
            current_mood_data["mood"] = mood_levels[new_index]
            current_mood_data["intensity"] = min(current_mood_data["intensity"] + event["intensity"] * 0.2, 1.0)
            current_mood_data["trend"] = "descending"
        
        else:  # neutral impact
            # Нейтральна подія може трохи змінити інтенсивність, але не настрій
            intensity_change = event["intensity"] * 0.1 * (1 if random.random() > 0.5 else -1)
            current_mood_data["intensity"] = max(0.1, min(current_mood_data["intensity"] + intensity_change, 1.0))
            current_mood_data["trend"] = "stable"
        
        # Оновлюємо останні події
        if "events" not in current_mood_data:
            current_mood_data["events"] = []
        
        current_mood_data["events"].insert(0, {
            "name": event["name"],
            "impact": event["impact"],
            "timestamp": event["timestamp"]
        })
        
        # Обмежуємо кількість подій у списку
        current_mood_data["events"] = current_mood_data["events"][:20]
        
        # Оновлюємо час останнього оновлення
        current_mood_data["last_update"] = datetime.now().timestamp() * 1000
        
        # Зберігаємо оновлений настрій
        save_world_mood(current_mood_data)
        
        # Зберігаємо подію в базу даних
        save_world_event(event["name"], event["impact"])
        
        # Зберігаємо зміну настрою в історію
        save_mood_history(current_mood_data["mood"], current_mood_data["intensity"])
        
        return jsonify({
            "status": "success",
            "message": "Автономний крок симуляції виконано успішно",
            "event": event,
            "current_world_state": current_mood_data
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Помилка під час виконання автономної симуляції: {str(e)}"
        }), 500

# Функція для отримання з'єднання з базою даних
def get_db_connection():
    conn = sqlite3.connect('luxortum_world.db')
    conn.row_factory = sqlite3.Row
    return conn

# Функція для ініціалізації бази даних
def init_db():
    conn = get_db_connection()
    try:
        # Створюємо таблицю для настрою світу, якщо вона не існує
        conn.execute('''
            CREATE TABLE IF NOT EXISTS world_mood (
                id INTEGER PRIMARY KEY,
                data TEXT NOT NULL
            )
        ''')
        
        # Створюємо таблицю для історії зміни настрою
        conn.execute('''
            CREATE TABLE IF NOT EXISTS mood_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood TEXT NOT NULL,
                intensity REAL NOT NULL,
                timestamp INTEGER NOT NULL
            )
        ''')
        
        # Створюємо таблицю для подій у світі
        conn.execute('''
            CREATE TABLE IF NOT EXISTS world_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                impact TEXT NOT NULL,
                timestamp INTEGER NOT NULL
            )
        ''')
        
        conn.commit()
    finally:
        conn.close()

# Функція для отримання поточного настрою світу
def get_world_mood():
    conn = get_db_connection()
    try:
        # Спроба отримати запис з бази даних
        mood_record = conn.execute('SELECT data FROM world_mood WHERE id = 1').fetchone()
        
        if mood_record:
            # Розпакування JSON даних
            return json.loads(mood_record['data'])
        else:
            # Початковий стан, якщо запис не знайдено
            initial_mood = get_initial_world_mood()
            # Зберігаємо початковий стан
            save_world_mood(initial_mood)
            return initial_mood
    finally:
        conn.close()

# Функція для збереження настрою світу
def save_world_mood(mood_data):
    conn = get_db_connection()
    try:
        # Серіалізація даних у JSON
        mood_json = json.dumps(mood_data)
        
        # Перевірка, чи існує запис
        record_exists = conn.execute('SELECT 1 FROM world_mood WHERE id = 1').fetchone() is not None
        
        if record_exists:
            # Оновлення існуючого запису
            conn.execute('UPDATE world_mood SET data = ? WHERE id = 1', (mood_json,))
        else:
            # Створення нового запису
            conn.execute('INSERT INTO world_mood (id, data) VALUES (1, ?)', (mood_json,))
        
        conn.commit()
    finally:
        conn.close()

# Функція для отримання початкового стану настрою світу
def get_initial_world_mood():
    return {
        "mood": "neutral",
        "intensity": 0.5,
        "trend": "stable",
        "last_update": datetime.now().timestamp() * 1000,
        "events": [],
        "effects": {
            "happiness": 0,
            "stability": 0,
            "creativity": 0,
            "knowledge": 0,
            "harmony": 0
        }
    }

# Функція для збереження запису в історії зміни настрою
def save_mood_history(mood, intensity):
    conn = get_db_connection()
    try:
        timestamp = int(datetime.now().timestamp() * 1000)
        conn.execute(
            'INSERT INTO mood_history (mood, intensity, timestamp) VALUES (?, ?, ?)',
            (mood, intensity, timestamp)
        )
        conn.commit()
    finally:
        conn.close()

# Функція для збереження події у світі
def save_world_event(name, impact):
    conn = get_db_connection()
    try:
        timestamp = int(datetime.now().timestamp() * 1000)
        conn.execute(
            'INSERT INTO world_events (name, impact, timestamp) VALUES (?, ?, ?)',
            (name, impact, timestamp)
        )
        conn.commit()
    finally:
        conn.close()

# Ініціалізуємо базу даних при запуску
init_db()

# Функція для запуску Telegram бота
def run_telegram_bot():
    """
    Запускає Telegram бота у фоновому режимі
    """
    try:
        from telegram.ext import Application, CommandHandler
        import telegram_bot as tb

        logger.info("Запуск Telegram бота Luxortum...")
        
        # Отримання токена з змінних середовища
        TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
        
        if not TELEGRAM_TOKEN:
            logger.warning("Змінна оточення TELEGRAM_TOKEN не знайдена. Бот не буде запущено.")
            return
        
        # Запускаємо бота
        tb.main()
        
    except ImportError as e:
        logger.warning(f"Не вдалося імпортувати бібліотеку python-telegram-bot: {e}")
    except Exception as e:
        logger.error(f"Помилка при запуску Telegram бота: {e}")

if __name__ == '__main__':
    # За замовчуванням Flask використовує порт 5000
    # Або можна вказати порт через змінну оточення PORT для сумісності з хостингами
    port = int(os.environ.get('PORT', 5000))
    
    # Запускаємо Telegram бота у окремому потоці, якщо доступний токен
    telegram_thread = None
    if os.environ.get("TELEGRAM_TOKEN"):
        logger.info("Запуск Telegram бота у окремому потоці...")
        telegram_thread = threading.Thread(target=run_telegram_bot)
        telegram_thread.daemon = True  # Потік буде завершено разом з основним процесом
        telegram_thread.start()
    
    # Запускаємо сервер
    logger.info(f"Запуск Flask сервера на порту {port}...")
    app.run(host='0.0.0.0', port=port)