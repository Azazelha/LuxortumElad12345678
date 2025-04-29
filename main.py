"""
Luxortum - Платформа божественної симуляції (спрощена версія)
"""

import sys
print("Python version:", sys.version)
print("Python path:", sys.path)

try:
    import flask
    print("Flask version:", flask.__version__)
except ImportError as e:
    print("Error importing Flask:", e)

# Створюємо простий додаток без імпорту складних модулів
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Luxortum - Божественна Симуляція</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }
            .nav-panel { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin: 20px 0; }
            .nav-btn { padding: 10px 15px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; }
            .sim-btn { background-color: #ff9800; }
            .title { color: #336699; }
            .section { margin: 40px 0; border-top: 1px solid #eee; padding-top: 20px; }
            .event-log { max-width: 600px; margin: 0 auto; text-align: left; background: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px; }
            #simulation-result { display: none; margin-top: 20px; padding: 15px; border-radius: 5px; }
            .success { background-color: #dff0d8; border: 1px solid #d6e9c6; color: #3c763d; }
            .error { background-color: #f2dede; border: 1px solid #ebccd1; color: #a94442; }
            h2 { color: #555; }
        </style>
        <script>
            function runSimulation() {
                const resultDiv = document.getElementById('simulation-result');
                resultDiv.innerHTML = "Запуск симуляції...";
                resultDiv.style.display = "block";
                resultDiv.className = "";
                
                fetch('/api/run-autonomous-step')
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            resultDiv.innerHTML = `
                                <strong>Симуляція успішна!</strong><br>
                                Подія: ${data.event.name}<br>
                                Опис: ${data.event.description}<br>
                                Вплив: ${data.event.impact === 'positive' ? 'Позитивний' : 'Негативний'}<br>
                                Поточний настрій світу: ${data.current_world_state.mood === 'positive' ? 'Позитивний' : 'Негативний'}<br>
                                Інтенсивність: ${data.current_world_state.intensity}
                            `;
                            resultDiv.className = "success";
                        } else {
                            resultDiv.innerHTML = `<strong>Помилка:</strong> ${data.message}`;
                            resultDiv.className = "error";
                        }
                    })
                    .catch(error => {
                        resultDiv.innerHTML = `<strong>Помилка підключення:</strong> ${error.message}`;
                        resultDiv.className = "error";
                    });
            }
        </script>
    </head>
    <body>
        <h1 class="title">Luxortum - Божественна Симуляція</h1>
        <p>Платформа для керування і спостереження за розвитком світу</p>
        
        <div class="nav-panel">
            <a href="/hello" class="nav-btn">Перевірка роботи</a>
            <a href="/static/world-control-panel.html" class="nav-btn">Панель керування світом</a>
            <a href="/static/world-control-panel-3d.html" class="nav-btn">3D Панель керування</a>
            <a href="/static/3d-scene-demo.html" class="nav-btn">3D Сцена</a>
        </div>
        
        <div class="section">
            <h2>Автономна Симуляція</h2>
            <p>Запустіть крок автономної симуляції щоб згенерувати випадкову подію і застосувати її вплив до світу:</p>
            <button onclick="runSimulation()" class="nav-btn sim-btn">Запустити крок симуляції</button>
            <div id="simulation-result"></div>
        </div>
    </body>
    </html>
    '''

@app.route('/hello')
def hello():
    return '<h1>Привіт, світе Luxortum!</h1><p>Luxortum успішно запущено</p>'

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/run-autonomous-step', methods=['GET'])
def api_run_autonomous_step():
    """
    Запускає один крок автономної симуляції.
    Спрощена версія, яка не використовує OpenAI.
    """
    try:
        import random
        import time
        import sqlite3
        
        # Функції для роботи з базою даних
        def get_db_connection():
            conn = sqlite3.connect('luxortum_world.db')
            conn.row_factory = sqlite3.Row
            return conn
            
        def get_world_mood():
            conn = get_db_connection()
            result = conn.execute('SELECT * FROM WORLD_MOOD LIMIT 1').fetchone()
            conn.close()
            
            if not result:
                # Якщо запис не знайдено, повертаємо початковий стан
                return {
                    "mood": "balanced",
                    "intensity": 50,
                    "updated": int(time.time() * 1000),
                    "effects": {}
                }
                
            # Перетворюємо рядок ефектів у словник
            effects = {}
            if result['effects']:
                for effect_item in result['effects'].split(','):
                    if ':' in effect_item:
                        key, value = effect_item.split(':')
                        effects[key.strip()] = int(value)
            
            return {
                "mood": result['mood'],
                "intensity": result['intensity'],
                "updated": result['updated'],
                "effects": effects
            }
            
        def save_world_mood(mood_data):
            conn = get_db_connection()
            
            # Перетворюємо словник ефектів у рядок
            effects_str = ""
            if mood_data.get("effects"):
                effects_str = ",".join([f"{k}:{v}" for k, v in mood_data["effects"].items()])
            
            # Оновлюємо або вставляємо запис
            conn.execute('''
                INSERT OR REPLACE INTO WORLD_MOOD (id, mood, intensity, updated, effects)
                VALUES (1, ?, ?, ?, ?)
            ''', (mood_data["mood"], mood_data["intensity"], mood_data["updated"], effects_str))
            
            conn.commit()
            conn.close()
            
        def save_world_event(name, impact):
            conn = get_db_connection()
            timestamp = int(time.time() * 1000)
            
            conn.execute('''
                INSERT INTO WORLD_EVENTS (timestamp, name, impact)
                VALUES (?, ?, ?)
            ''', (timestamp, name, impact))
            
            conn.commit()
            conn.close()
            
            return {
                "timestamp": timestamp,
                "name": name,
                "impact": impact
            }
        
        # Переконуємось, що таблиці існують
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS WORLD_MOOD (
                id INTEGER PRIMARY KEY,
                mood TEXT NOT NULL,
                intensity INTEGER NOT NULL,
                updated INTEGER NOT NULL,
                effects TEXT
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS WORLD_EVENTS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                name TEXT NOT NULL,
                impact TEXT NOT NULL
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS MOOD_HISTORY (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                mood TEXT NOT NULL,
                intensity INTEGER NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Отримуємо поточний стан світу
        current_mood_data = get_world_mood()
        
        # Генеруємо випадкову подію
        event_options = [
            {"name": "Свято світла", "impact": "positive", "description": "Промені світла пронизують хмари, наповнюючи світ енергією і радістю."},
            {"name": "Таємнича буря", "impact": "negative", "description": "Темні хмари заволоділи небом, несучи тривогу і смуток у серця жителів."},
            {"name": "Народження нової істоти", "impact": "positive", "description": "У світі з'явилася нова душа, чиста і сповнена потенціалу."},
            {"name": "Загадкове затемнення", "impact": "negative", "description": "Сонце зникло за темним диском, занурюючи світ у таємничу темряву."},
            {"name": "Гармонія стихій", "impact": "positive", "description": "Вода, вогонь, повітря і земля об'єдналися в чудовому танці рівноваги."}
        ]
        new_event = random.choice(event_options)
        new_event["id"] = str(int(time.time()))
        new_event["timestamp"] = int(time.time() * 1000)
        
        # Записуємо подію в історію
        save_world_event(new_event["name"], new_event["impact"])
        
        # Змінюємо стан світу відповідно до події
        if new_event["impact"] == "positive":
            current_mood_data["mood"] = "positive"
            current_mood_data["intensity"] = min(100, current_mood_data["intensity"] + 5)
        else:
            current_mood_data["mood"] = "negative"
            current_mood_data["intensity"] = max(1, current_mood_data["intensity"] - 5)
        
        current_mood_data["updated"] = int(time.time() * 1000)
        
        # Зберігаємо оновлений стан світу
        save_world_mood(current_mood_data)
        
        # Записуємо в історію настрою
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO MOOD_HISTORY (timestamp, mood, intensity)
            VALUES (?, ?, ?)
        ''', (int(time.time() * 1000), current_mood_data["mood"], current_mood_data["intensity"]))
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "success", 
            "message": "Крок автономної симуляції успішно виконано", 
            "event": new_event,
            "current_world_state": current_mood_data
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Помилка симуляції: {str(e)}"}), 500

print("Спрощений додаток Luxortum створено")

# Не запускаємо app.run тут, оскільки gunicorn робить це сам
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)