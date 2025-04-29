"""
Luxortum - Спрощена версія для розробки та тестування
"""

import os
import time
import random
from flask import Flask, jsonify, request, send_from_directory
from db_utils import (
    init_db, get_world_mood_from_db, save_world_mood_to_db,
    get_mood_history, save_world_event, get_world_events
)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "development_key")

# Ініціалізуємо базу даних при запуску 
init_db(app)
print("База даних ініціалізована")

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Luxortum - Божественна Симуляція</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }
            .nav-panel { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin: 20px 0; }
            .nav-btn { padding: 10px 15px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; }
            .status { margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>Luxortum - Божественна Симуляція</h1>
        <p>Ласкаво просимо до світу, яким ви можете керувати!</p>
        
        <div class="nav-panel">
            <a href="/hello" class="nav-btn">Перевірка роботи</a>
            <a href="/static/world-control-panel.html" class="nav-btn">Панель керування світом</a>
            <a href="/static/world-control-panel-3d.html" class="nav-btn">3D Панель керування</a>
            <a href="/static/3d-scene-demo.html" class="nav-btn">3D Сцена</a>
            <a href="/api/run-autonomous-step" class="nav-btn">Запустити автономну симуляцію</a>
        </div>
        
        <div class="status">
            <h3>Статус:</h3>
            <p>Сервер працює</p>
            <p>База даних ініціалізована</p>
        </div>
    </body>
    </html>
    """

@app.route('/hello')
def hello():
    return 'Привіт, Luxortum працює!'

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)
    
@app.route('/api/world-mood', methods=['GET', 'POST'])
def api_world_mood():
    """
    API маршрут для отримання (GET) та оновлення (POST) настрою світу,
    використовуючи базу даних для зберігання стану.
    """
    if request.method == 'GET':
        mood_data = get_world_mood_from_db()
        return jsonify(mood_data)
    elif request.method == 'POST':
        data = request.json
        save_world_mood_to_db(data)
        return jsonify({"status": "success", "message": "Настрій світу оновлено"})

@app.route('/api/mood-history', methods=['GET'])
def api_mood_history():
    """
    API маршрут для отримання історії змін настрою світу.
    """
    limit = request.args.get('limit', default=10, type=int)
    history = get_mood_history(limit)
    return jsonify(history)

@app.route('/api/world-events', methods=['GET'])
def api_world_events():
    """
    API маршрут для отримання списку подій у світі.
    """
    limit = request.args.get('limit', default=20, type=int)
    events = get_world_events(limit)
    return jsonify(events)

@app.route('/api/run-simulation', methods=['POST'])
def run_simulation_step():
    """
    Запускає один крок симуляції: генерує випадкову подію
    та застосовує її до стану світу в базі даних.
    """
    try:
        # Отримуємо поточний стан світу з БД
        current_mood_data = get_world_mood_from_db()
        
        # Створюємо фіктивну подію для тестування
        test_event = {
            "id": "99999",  # Тестовий ID
            "timestamp": str(int(time.time() * 1000)),
            "name": "Тестова подія симуляції",
            "description": "Це тестова подія для перевірки функціональності симуляції.",
            "impact": "positive" if current_mood_data["mood"] == "negative" else "negative",
            "intensity": str(min(100, current_mood_data["intensity"] + 5))
        }
        
        # Записуємо подію в історію
        save_world_event(test_event["name"], test_event["impact"])
        
        # Змінюємо стан світу на протилежний для тестування
        if current_mood_data["mood"] == "positive":
            current_mood_data["mood"] = "negative"
        else:
            current_mood_data["mood"] = "positive"
            
        # Змінюємо інтенсивність
        current_mood_data["intensity"] = test_event["intensity"]
        
        # Зберігаємо оновлений стан світу в БД
        save_world_mood_to_db(current_mood_data)
        
        return jsonify({
            "status": "success", 
            "message": "Крок симуляції успішно виконано", 
            "event": test_event,
            "current_world_state": current_mood_data
        })
        
    except Exception as e:
        print(f"Помилка під час виконання симуляції: {str(e)}")
        return jsonify({"status": "error", "message": f"Помилка симуляції: {str(e)}"}), 500

# Маршрут для запуску автономної симуляції вручну
@app.route('/api/run-autonomous-step', methods=['GET'])
def api_run_autonomous_step():
    """
    Запускає один крок автономної симуляції.
    Спрощена версія, яка не використовує OpenAI.
    """
    try:
        # Отримуємо поточний стан світу з БД
        current_mood_data = get_world_mood_from_db()
        
        # Генеруємо випадкову подію
        event_options = [
            {"name": "Свято світла", "impact": "positive"},
            {"name": "Таємнича буря", "impact": "negative"},
            {"name": "Народження нової істоти", "impact": "positive"},
            {"name": "Загадкове затемнення", "impact": "negative"},
            {"name": "Гармонія стихій", "impact": "positive"}
        ]
        new_event = random.choice(event_options)
        new_event["id"] = str(int(time.time()))
        new_event["timestamp"] = str(int(time.time() * 1000))
        new_event["description"] = f"Світ відчув вплив події '{new_event['name']}', це змінило настрій всесвіту."
        new_event["intensity"] = str(random.randint(1, 100))
        
        print(f"Ручний запуск автономної симуляції: Згенеровано подію: {new_event['name']} ({new_event['impact']})")
        
        # Записуємо подію в історію
        save_world_event(new_event["name"], new_event["impact"])
        
        # Змінюємо стан світу відповідно до події
        if new_event["impact"] == "positive":
            current_mood_data["mood"] = "positive"
            current_mood_data["intensity"] = min(100, current_mood_data["intensity"] + 5)
        else:
            current_mood_data["mood"] = "negative"
            current_mood_data["intensity"] = max(1, current_mood_data["intensity"] - 5)
        
        # Зберігаємо оновлений стан світу в БД
        save_world_mood_to_db(current_mood_data)
        
        return jsonify({
            "status": "success", 
            "message": "Крок автономної симуляції успішно виконано", 
            "event": new_event,
            "current_world_state": current_mood_data
        })
        
    except Exception as e:
        print(f"Помилка під час виконання кроку автономної симуляції: {str(e)}")
        return jsonify({"status": "error", "message": f"Помилка симуляції: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)