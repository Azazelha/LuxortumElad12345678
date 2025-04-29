"""
Luxortum - Платформа божественної симуляції
Оптимізований проект для демонстрації ключових функцій
"""
import os
import time
import json
import flask
import random
import datetime
from flask import Flask, send_from_directory, jsonify, request, redirect, g
from openai import OpenAI
from flask_apscheduler import APScheduler
from db_utils import (
    get_db, close_db, init_db, get_world_mood_from_db, save_world_mood_to_db,
    save_mood_history, get_mood_history, save_world_event, get_world_events
)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "luxortum_secret_key")

# --- Спрощена конфігурація APScheduler ---
app.config['SCHEDULER_API_ENABLED'] = True
app.config['SCHEDULER_TIMEZONE'] = 'UTC'

# Ініціалізуємо планувальник
scheduler = APScheduler()
scheduler.init_app(app)
# Планувальник буде запущено після ініціалізації всього додатка

# Ініціалізація клієнта OpenAI
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("OpenAI клієнт ініціалізовано")

# Реєстрація функцій для закриття з'єднання з БД
app.teardown_appcontext(close_db)

# Ініціалізація бази даних при запуску
with app.app_context():
    init_db(app)
    print("База даних ініціалізована")

# Дані для підказок
TOOLTIPS = [
    {
        "id": 1,
        "character_type": "guide",
        "text": "Дерево Життя є центральною концепцією кабалістичної традиції. Воно представляє структуру всесвіту та шлях до божественного.",
        "element_id": "tree_of_life",
        "context": "kabbalah_symbols"
    },
    {
        "id": 2,
        "character_type": "prophet",
        "text": "Коло Мудрості символізує нескінченну природу божественного знання. Заглибся в себе і знайди свій шлях до просвітлення.",
        "element_id": "wisdom_circle",
        "context": "kabbalah_symbols"
    },
    {
        "id": 3,
        "character_type": "lover",
        "text": "Священне Полум'я — це символ пристрасті до знання й істини. Відчуй жар цього полум'я в своєму серці.",
        "element_id": "sacred_flame",
        "context": "kabbalah_symbols"
    },
    {
        "id": 4,
        "character_type": "creator",
        "text": "Ти творець цього світу. Використовуй свою силу мудро і створюй гармонію в житті своїх творінь.",
        "element_id": "tree_of_life",
        "context": "kabbalah_symbols"
    },
    {
        "id": 5,
        "character_type": "destroyer",
        "text": "Навіть у руйнуванні є порядок і мета. Зі знищення старого народжується щось нове і прекрасне.",
        "element_id": "tree_of_life",
        "context": "kabbalah_symbols"
    },
    {
        "id": 6,
        "character_type": "guide",
        "text": "Коло Мудрості відображає нашу духовну подорож, від зовнішнього сприйняття до внутрішнього просвітлення.",
        "element_id": "wisdom_circle",
        "context": "kabbalah_symbols"
    },
    {
        "id": 7,
        "character_type": "prophet",
        "text": "Коли ти зазирнеш у Коло Мудрості, воно покаже тобі майбутнє. Але будь обережний — знання долі несе відповідальність.",
        "element_id": "wisdom_circle",
        "context": "kabbalah_symbols"
    },
    {
        "id": 8,
        "character_type": "lover",
        "text": "Коло Мудрості притягує до себе подібних. Знайди того, хто резонує з твоєю душею на тій же частоті.",
        "element_id": "wisdom_circle",
        "context": "kabbalah_symbols"
    },
    {
        "id": 9,
        "character_type": "creator",
        "text": "Священне Полум'я — це енергія творіння. Запали його в своєму світі, щоб наповнити його життям.",
        "element_id": "sacred_flame",
        "context": "kabbalah_symbols"
    },
    {
        "id": 10,
        "character_type": "destroyer",
        "text": "Священне Полум'я спалює все застаріле і непотрібне. Дозволь йому очистити твій світ від баласту.",
        "element_id": "sacred_flame",
        "context": "kabbalah_symbols"
    },
    {
        "id": 11,
        "character_type": "prophet",
        "text": "Священне Полум'я — провідник пророцтв. Дивлячись на нього, я бачу великі зміни у твоєму світі.",
        "element_id": "sacred_flame",
        "context": "kabbalah_symbols"
    }
]

# Дані для настрою світу
WORLD_MOOD = {
    "mood": "peaceful",
    "intensity": 0.6,
    "timestamp": int(time.time() * 1000),
    "events": [
        {
            "name": "Ініціалізація світу",
            "impact": "neutral",
            "timestamp": int(time.time() * 1000)
        }
    ],
    "trend": "stable",
    "effects": {
        "growth": 0.2,
        "creativity": 0.1,
        "harmony": 0.5,
        "chaos": -0.4
    }
}

# Маршрути сервера
@app.route('/')
def index():
    try:
        return send_from_directory('static', 'index.html')
    except:
        try:
            return send_from_directory('templates', 'index.html')
        except Exception as e:
            return f"""
            <html>
                <head><title>Luxortum</title></head>
                <body style="font-family: Arial, sans-serif; background-color: #1a0a2a; color: #ffffff; margin: 0; padding: 20px;">
                    <div style="max-width: 800px; margin: 0 auto; background-color: #4a2a8a; padding: 30px; border-radius: 15px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);">
                        <h1 style="color: #ffbb00; text-align: center; margin-bottom: 20px;">Вітаємо у Luxortum</h1>
                        <p style="text-align: center; font-size: 1.2em;">Платформа божественної симуляції</p>
                        
                        <h2 style="color: #ffbb00; margin-top: 30px;">Доступні демо-сторінки:</h2>
                        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 20px;">
                            <a href="/tooltip-demo" style="background-color: #6a4a9a; color: white; text-decoration: none; padding: 15px; border-radius: 10px; flex: 1 0 200px; text-align: center; margin: 5px;">Демо контекстних підказок</a>
                            <a href="/world-mood" style="background-color: #6a4a9a; color: white; text-decoration: none; padding: 15px; border-radius: 10px; flex: 1 0 200px; text-align: center; margin: 5px;">Демо настрою світу</a>
                            <a href="/creator-avatar" style="background-color: #6a4a9a; color: white; text-decoration: none; padding: 15px; border-radius: 10px; flex: 1 0 200px; text-align: center; margin: 5px;">Демо аватара творця</a>
                            <a href="/3d-scene" style="background-color: #6a4a9a; color: white; text-decoration: none; padding: 15px; border-radius: 10px; flex: 1 0 200px; text-align: center; margin: 5px;">Демо 3D сцени</a>
                        </div>
                        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 10px;">
                            <a href="/world-control-panel" style="background-color: #ffbb00; color: #1a0a2a; text-decoration: none; padding: 15px; border-radius: 10px; flex: 1 0 200px; text-align: center; margin: 5px; font-weight: bold;">Панель керування світом</a>
                            <a href="/world-control-panel-3d" style="background: linear-gradient(45deg, #ffbb00, #ff5500); color: #1a0a2a; text-decoration: none; padding: 15px; border-radius: 10px; flex: 1 0 200px; text-align: center; margin: 5px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">3D Панель керування світом</a>
                        </div>
                        
                        <p style="text-align: center; margin-top: 30px;"><a href="/hello" style="color: #ffbb00;">Тестовий маршрут</a></p>
                        
                        <p style="color:red; text-align: center; margin-top: 20px;">Помилка відображення головної сторінки: {str(e)}</p>
                    </div>
                </body>
            </html>
            """

@app.route('/tooltip-demo')
def tooltip_demo():
    return send_from_directory('static', 'new-tooltip-demo.html')

@app.route('/world-mood')
def world_mood_demo():
    return send_from_directory('static', 'new-world-mood-demo.html')

@app.route('/api/tooltips')
def api_tooltips():
    element_id = request.args.get('element_id')
    character_type = request.args.get('character_type')
    
    filtered_tooltips = TOOLTIPS
    
    if element_id:
        filtered_tooltips = [t for t in filtered_tooltips if t['element_id'] == element_id]
    
    if character_type:
        filtered_tooltips = [t for t in filtered_tooltips if t['character_type'] == character_type]
        
    return jsonify(filtered_tooltips)

@app.route('/api/world-mood', methods=['GET', 'POST'])
def api_world_mood():
    """
    API маршрут для отримання (GET) та оновлення (POST) настрою світу,
    використовуючи базу даних для зберігання стану.
    """
    # Отримуємо поточний стан світу з бази даних
    current_mood = get_world_mood_from_db()

    if request.method == 'POST':
        try:
            data = request.get_json()

            if data is None:
                 return jsonify({"status": "error", "message": "Невірний формат JSON"}), 400

            # Оновлюємо дані, базуючись на поточному стані з БД
            updated_mood = current_mood.copy() # Робимо копію, щоб не змінювати стан безпосередньо під час обробки

            if 'mood' in data and isinstance(data['mood'], str):
                updated_mood['mood'] = data['mood']
                # Зберігаємо зміну настрою в історії
                save_mood_history(data['mood'], updated_mood.get('intensity', 0.5))

            if 'intensity' in data and isinstance(data['intensity'], (int, float)):
                updated_mood['intensity'] = max(0.0, min(1.0, float(data['intensity'])))
                # Зберігаємо зміну інтенсивності в історії
                save_mood_history(updated_mood.get('mood', 'neutral'), data['intensity'])

            if 'events' in data and isinstance(data['events'], list):
                for event in data['events']:
                    if isinstance(event, dict) and 'name' in event and 'impact' in event:
                        valid_impacts = ['positive', 'negative', 'neutral']
                        if event['impact'] in valid_impacts:
                            event['timestamp'] = event.get('timestamp', int(time.time() * 1000))
                            updated_mood['events'].insert(0, event)
                            
                            # Зберігаємо подію в окремій таблиці подій
                            save_world_event(event['name'], event['impact'])
                        else:
                             print(f"Помилка: Невірне значення impact для події: {event.get('name')}")
                    else:
                        print(f"Помилка: Невірний формат події: {event}")

                # Обмежуємо кількість подій
                if len(updated_mood['events']) > 20:
                    updated_mood['events'] = updated_mood['events'][:20]

            # Перераховуємо ефекти на основі оновленого настрою
            mood_effects = {
                'ecstatic': {'growth': 0.4, 'creativity': 0.5, 'harmony': 0.5, 'chaos': -0.3},
                'joyful': {'growth': 0.3, 'creativity': 0.3, 'harmony': 0.4, 'chaos': -0.2},
                'peaceful': {'growth': 0.2, 'creativity': 0.1, 'harmony': 0.5, 'chaos': -0.4},
                'neutral': {'growth': 0, 'creativity': 0, 'harmony': 0, 'chaos': 0},
                'anxious': {'growth': -0.1, 'creativity': 0.2, 'harmony': -0.2, 'chaos': 0.3},
                'melancholic': {'growth': -0.2, 'creativity': 0.4, 'harmony': -0.1, 'chaos': 0.1},
                'sad': {'growth': -0.3, 'creativity': -0.1, 'harmony': -0.3, 'chaos': 0.2},
                'angry': {'growth': -0.2, 'creativity': -0.3, 'harmony': -0.5, 'chaos': 0.5},
                'chaotic': {'growth': -0.4, 'creativity': 0.1, 'harmony': -0.5, 'chaos': 0.6}
            }
            
            mood = updated_mood['mood']
            if mood in mood_effects:
                updated_mood['effects'] = mood_effects[mood]

            # Оновлюємо часову мітку
            updated_mood['timestamp'] = int(time.time() * 1000)

            # Оновлюємо тренд на основі останніх подій
            if len(updated_mood['events']) >= 2:
                # Аналізуємо останні події для визначення тренду
                impacts = {'positive': 0, 'negative': 0, 'neutral': 0}
                recent_events = updated_mood['events'][:5]  # Розглядаємо лише останні 5 подій (або менше)
                
                for event in recent_events:
                    impact = event.get('impact')
                    if impact in impacts:
                        impacts[impact] += 1
                
                if impacts['positive'] > impacts['negative']:
                    updated_mood['trend'] = 'improving'
                elif impacts['negative'] > impacts['positive']:
                    updated_mood['trend'] = 'worsening'
                else:
                    updated_mood['trend'] = 'stable'

            # Зберігаємо оновлений стан світу в базі даних
            save_world_mood_to_db(updated_mood)

            return jsonify({"status": "success", "data": updated_mood})

        except json.JSONDecodeError:
             return jsonify({"status": "error", "message": "Невірний формат JSON у тілі запиту"}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": f"Внутрішня помилка сервера: {str(e)}"}), 500

    else: # Обробка GET-запиту
        # Повертаємо поточний стан світу, отриманий з бази даних
        return jsonify(current_mood)

@app.route('/api/mood-history')
def api_mood_history():
    """
    API маршрут для отримання історії змін настрою світу.
    """
    limit = request.args.get('limit', 10, type=int)
    if limit > 100:  # Обмежуємо максимальну кількість записів для продуктивності
        limit = 100
        
    history = get_mood_history(limit)
    return jsonify({"status": "success", "data": history})

@app.route('/api/world-events')
def api_world_events():
    """
    API маршрут для отримання списку подій у світі.
    """
    limit = request.args.get('limit', 20, type=int)
    if limit > 100:  # Обмежуємо максимальну кількість записів для продуктивності
        limit = 100
        
    events = get_world_events(limit)
    return jsonify({"status": "success", "data": events})

@app.route('/health')
def health():
    return 'OK'

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Перенаправлення на нові маршрути для забезпечення сумісності зі старими URL
@app.route('/tooltip-demo.html')
def redirect_tooltip_demo():
    return redirect('/tooltip-demo')

@app.route('/world-mood-demo.html')
def redirect_world_mood_demo():
    return redirect('/world-mood')

# Додаємо тестовий маршрут для перевірки
@app.route('/hello')
def hello():
    return 'Привіт, Luxortum працює!'

@app.route('/3d-scene')
def threejs_scene_demo():
    """
    Обслуговує сторінку демо 3D сцени з використанням Three.js.
    """
    try:
        return send_from_directory('static', '3d-scene-demo.html')
    except Exception as e:
        return f"""
        <html>
            <head><title>Luxortum - Демо 3D сцени</title></head>
            <body>
                <h1>Демо 3D сцени</h1>
                <p>Не вдалося знайти 3d-scene-demo.html в директорії static.</p>
                <p>Будь ласка, переконайтеся, що файл існує за шляхом: /static/3d-scene-demo.html</p>
                <p>Технічна інформація про помилку: {str(e)}</p>
                <p><a href="/">На головну</a></p>
            </body>
        </html>
        """, 404
        
@app.route('/world-control-panel')
def world_control_panel():
    """
    Обслуговує сторінку панелі управління настроєм світу Luxortum.
    """
    try:
        return send_from_directory('static', 'world-control-panel.html')
    except Exception as e:
        return f"""
        <html>
            <head><title>Luxortum - Панель Управління Світом</title></head>
            <body>
                <h1>Панель Управління Світом</h1>
                <p>Не вдалося знайти world-control-panel.html в директорії static.</p>
                <p>Будь ласка, переконайтеся, що файл існує за шляхом: /static/world-control-panel.html</p>
                <p>Технічна інформація про помилку: {str(e)}</p>
                <p><a href="/">На головну</a></p>
            </body>
        </html>
        """, 404
        
@app.route('/world-control-panel-3d')
def world_control_panel_3d():
    """
    Обслуговує інтерактивну 3D панель управління настроєм світу Luxortum.
    """
    try:
        return send_from_directory('static', 'world-control-panel-3d.html')
    except Exception as e:
        return f"""
        <html>
            <head><title>Luxortum - 3D Панель Управління Світом</title></head>
            <body>
                <h1>3D Панель Управління Світом</h1>
                <p>Не вдалося знайти world-control-panel-3d.html в директорії static.</p>
                <p>Будь ласка, переконайтеся, що файл існує за шляхом: /static/world-control-panel-3d.html</p>
                <p>Технічна інформація про помилку: {str(e)}</p>
                <p><a href="/">На головну</a></p>
            </body>
        </html>
        """, 404
        
# --- Логіка Симуляції ---

# Визначення можливих типів подій та їх потенційного впливу
EVENT_TYPES = [
    {"name": "Божественне втручання", "impact": "positive", "base_description": "Світ отримав благословення. Відчувається приплив позитивної енергії."},
    {"name": "Прояв хаосу", "impact": "negative", "base_description": "Силами хаосу посіяно розбрат. Зростає напруженість."},
    {"name": "Гармонійне вирівнювання", "impact": "neutral", "base_description": "Енергії світу збалансовано. Відновлюється рівновага."},
    {"name": "Спалах творчості", "impact": "positive", "base_description": "Натхнення охопило світ. З'являються нові ідеї та форми."},
    {"name": "Занепад енергії", "impact": "negative", "base_description": "Життєва сила світу зменшується. Відчувається втома."},
    {"name": "Народження генія", "impact": "positive", "base_description": "У світі з'явилася нова видатна особистість. Розум, що змінить хід історії."},
    {"name": "Природний катаклізм", "impact": "negative", "base_description": "Стихійне лихо спричинило руйнування. Природа виходить з рівноваги."},
    {"name": "Наукове відкриття", "impact": "positive", "base_description": "Зроблено важливе наукове відкриття. Знання розширюються."},
    {"name": "Філософський діалог", "impact": "neutral", "base_description": "Проведено важливу філософську дискусію. Думки зіштовхуються."},
    {"name": "Вирівнювання зірок", "impact": "positive", "base_description": "Астрологічне явище сприяє позитивним змінам. Космос благоволить."},
    {"name": "Духовне просвітлення", "impact": "positive", "base_description": "Багато істот досягли вищого рівня свідомості. Душі піднімаються."},
    {"name": "Соціальний конфлікт", "impact": "negative", "base_description": "У суспільстві виникли серйозні протиріччя. Єдність порушується."},
    {"name": "Культурний розквіт", "impact": "positive", "base_description": "Спостерігається бурхливий розвиток мистецтв. Краса торжествує."},
    {"name": "Технологічний прорив", "impact": "neutral", "base_description": "Винайдено нову технологію з невідомими наслідками. Можливості розширюються."}
]

def generate_event_description_with_ai(event_name, event_impact, base_description):
    """
    Генерує більш детальний опис події за допомогою OpenAI.
    У разі проблем з API (включаючи вичерпання квоти) повертає базовий опис.
    """
    # Перевіряємо наявність ключа API
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY відсутній. Використовуємо базовий опис.")
        return f"{base_description} (Базовий опис)"
    
    # Якщо існує файл-прапорець про проблеми з API, не намагаємося робити запит
    if os.path.exists("openai_api_issues.flag"):
        print("Виявлено прапорець проблем з OpenAI API. Використовуємо базовий опис.")
        return f"{base_description} (Базовий опис через проблеми з API)"
    
    prompt = f"Напиши короткий, містичний опис для події у світі божественної симуляції. Подія: '{event_name}'. Її вплив: '{event_impact}'. Базовий опис: '{base_description}'. Опис має бути в українській мові, до 50 слів."

    try:
        # Виконуємо запит до OpenAI API
        chat_completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o", # Використовуємо найновішу модель
            max_tokens=100 # Обмежуємо довжину відповіді
        )
        # Отримуємо згенерований текст
        ai_description = chat_completion.choices[0].message.content.strip()
        return ai_description

    except Exception as e:
        error_message = str(e)
        print(f"Помилка під час генерації опису події за допомогою OpenAI: {error_message}")
        
        # Створюємо прапорець, якщо проблема пов'язана з квотою або API
        if "quota" in error_message or "API" in error_message:
            with open("openai_api_issues.flag", "w") as f:
                f.write(f"OpenAI API проблема виявлена: {error_message}")
            print("Створено прапорець проблем з API")
        
        # У випадку помилки повертаємо базовий опис
        return f"{base_description} (Базовий опис через помилку API)"


def generate_random_event():
    """
    Генерує випадкову подію, включаючи згенерований AI опис.
    """
    event_type = random.choice(EVENT_TYPES)
    base_description = event_type.get("base_description", "Подія відбулася.") # Отримуємо базовий опис

    # Генеруємо розширений опис за допомогою AI
    extended_description = generate_event_description_with_ai(
        event_type["name"],
        event_type["impact"],
        base_description
    )

    event = {
        "name": event_type["name"],
        "impact": event_type["impact"],
        "timestamp": int(time.time() * 1000),
        "description": extended_description  # Використовуємо розширений опис
    }
    return event

def apply_event_to_world(current_mood_data, event):
    """
    Застосовує вплив події до стану світу.
    Ця функція модифікує настрій, інтенсивність та інші параметри світу
    на основі події, що відбулася.
    """
    # Додаємо нову подію до списку подій
    MAX_EVENTS = 20 # Максимальна кількість подій для зберігання
    current_mood_data['events'].insert(0, event) # Додаємо на початок списку (найновіші події спочатку)
    if len(current_mood_data['events']) > MAX_EVENTS:
        current_mood_data['events'] = current_mood_data['events'][:MAX_EVENTS] # Залишаємо тільки останні події

    # Змінюємо настрій та інтенсивність на основі події
    # Позитивні події можуть покращити настрій або збільшити інтенсивність
    # Негативні - можуть погіршити або зменшити інтенсивність
    
    # Визначаємо можливі переходи між настроями (від кращого до гіршого)
    mood_levels = ['ecstatic', 'joyful', 'peaceful', 'neutral', 'anxious', 'melancholic', 'sad', 'angry', 'chaotic']
    
    # Знаходимо поточний рівень настрою
    current_index = mood_levels.index(current_mood_data['mood']) if current_mood_data['mood'] in mood_levels else 3 # Якщо невідомий, вважаємо "neutral"
    
    # Змінюємо настрій на основі впливу події
    if event['impact'] == 'positive':
        # Покращуємо настрій (рухаємось вгору по списку)
        if random.random() < 0.7: # 70% шанс зміни настрою
            new_index = max(0, current_index - 1) # Обмежуємо, щоб не вийти за межі списку
            current_mood_data['mood'] = mood_levels[new_index]
            
        # Збільшуємо інтенсивність
        current_mood_data['intensity'] = min(1.0, current_mood_data['intensity'] + random.uniform(0.05, 0.15))
        
    elif event['impact'] == 'negative':
        # Погіршуємо настрій (рухаємось вниз по списку)
        if random.random() < 0.7: # 70% шанс зміни настрою
            new_index = min(len(mood_levels) - 1, current_index + 1) # Обмежуємо, щоб не вийти за межі списку
            current_mood_data['mood'] = mood_levels[new_index]
            
        # Зменшуємо інтенсивність
        current_mood_data['intensity'] = max(0.0, current_mood_data['intensity'] - random.uniform(0.05, 0.15))
    
    # Нейтральні події мають невеликий випадковий вплив
    else:
        if random.random() < 0.3: # 30% шанс зміни настрою
            direction = random.choice([-1, 1])  # Випадковий напрямок зміни
            new_index = max(0, min(len(mood_levels) - 1, current_index + direction))
            current_mood_data['mood'] = mood_levels[new_index]
            
        # Невелика випадкова зміна інтенсивності
        intensity_change = random.uniform(-0.1, 0.1)
        current_mood_data['intensity'] = max(0.0, min(1.0, current_mood_data['intensity'] + intensity_change))

    # Зберігаємо зміну настрою в історії
    save_mood_history(current_mood_data['mood'], current_mood_data['intensity'])
    
    # Оновлюємо ефекти для нового настрою
    mood_effects = {
        'ecstatic': {'growth': 0.4, 'creativity': 0.5, 'harmony': 0.5, 'chaos': -0.3},
        'joyful': {'growth': 0.3, 'creativity': 0.3, 'harmony': 0.4, 'chaos': -0.2},
        'peaceful': {'growth': 0.2, 'creativity': 0.1, 'harmony': 0.5, 'chaos': -0.4},
        'neutral': {'growth': 0, 'creativity': 0, 'harmony': 0, 'chaos': 0},
        'anxious': {'growth': -0.1, 'creativity': 0.2, 'harmony': -0.2, 'chaos': 0.3},
        'melancholic': {'growth': -0.2, 'creativity': 0.4, 'harmony': -0.1, 'chaos': 0.1},
        'sad': {'growth': -0.3, 'creativity': -0.1, 'harmony': -0.3, 'chaos': 0.2},
        'angry': {'growth': -0.2, 'creativity': -0.3, 'harmony': -0.5, 'chaos': 0.5},
        'chaotic': {'growth': -0.4, 'creativity': 0.1, 'harmony': -0.5, 'chaos': 0.6}
    }
    
    if current_mood_data['mood'] in mood_effects:
        current_mood_data['effects'] = mood_effects[current_mood_data['mood']]

    # Оновлюємо тренд на основі останніх подій
    impacts = {'positive': 0, 'negative': 0, 'neutral': 0}
    recent_events = current_mood_data['events'][:5]  # Розглядаємо лише останні 5 подій
    
    for evt in recent_events:
        impact = evt.get('impact')
        if impact in impacts:
            impacts[impact] += 1
    
    if impacts['positive'] > impacts['negative']:
        current_mood_data['trend'] = 'improving'
    elif impacts['negative'] > impacts['positive']:
        current_mood_data['trend'] = 'worsening'
    else:
        current_mood_data['trend'] = 'stable'

    # Оновлюємо часову мітку
    current_mood_data['timestamp'] = int(time.time() * 1000)

    # Зберігаємо подію в окремій таблиці подій для історії
    save_world_event(event['name'], event['impact'])

    return current_mood_data


# --- Функція, яка буде виконуватися за розкладом ---
def run_autonomous_simulation_step():
    """
    Виконує один крок симуляції автономно.
    Ця функція викликається планувальником.
    """
    # Отримуємо контекст додатка, оскільки планувальник працює поза запитом
    with app.app_context():
        try:
            # Отримуємо поточний стан світу з БД
            current_mood_data = get_world_mood_from_db()

            # Генеруємо нову подію
            new_event = generate_random_event()
            print(f"Автономна симуляція: Згенеровано подію: {new_event['name']} ({new_event['impact']}) - {new_event['description']}") # Логуємо подію

            # Застосовуємо подію до стану світу
            updated_mood_data = apply_event_to_world(current_mood_data, new_event)

            # Зберігаємо оновлений стан світу в БД
            save_world_mood_to_db(updated_mood_data)

            print("Автономна симуляція: Крок виконано успішно.")

        except Exception as e:
            print(f"Автономна симуляція: Помилка під час виконання кроку: {str(e)}")
            # У випадку помилки автономної симуляції, можливо, варто записати її в лог
            # або повідомити адміністратора, але не зупиняти додаток.

# --- Новий маршрут для запуску симуляції ---
@app.route('/api/simulate', methods=['POST'])
def run_simulation_step():
    """
    Запускає один крок симуляції: генерує випадкову подію
    та застосовує її до стану світу в базі даних.
    """
    try:
        # Отримуємо поточний стан світу з БД
        current_mood_data = get_world_mood_from_db()

        # Генеруємо нову подію
        new_event = generate_random_event()
        print(f"Згенеровано подію: {new_event['name']} ({new_event['impact']})")

        # Застосовуємо подію до стану світу
        updated_mood_data = apply_event_to_world(current_mood_data, new_event)

        # Зберігаємо оновлений стан світу в БД
        save_world_mood_to_db(updated_mood_data)

        # Повертаємо оновлений стан світу
        return jsonify({"status": "success", "message": "Крок симуляції виконано", "data": updated_mood_data})

    except Exception as e:
        print(f"Помилка під час виконання кроку симуляції: {str(e)}")
        return jsonify({"status": "error", "message": f"Помилка симуляції: {str(e)}"}), 500

# --- Маршрут для запуску кількох кроків симуляції підряд ---
@app.route('/api/simulate-multiple', methods=['POST'])
def run_multiple_simulation_steps():
    """
    Запускає декілька кроків симуляції підряд.
    Кількість кроків вказується в параметрі запиту steps або за замовчуванням = 5.
    """
    try:
        data = request.get_json() or {}
        steps = int(data.get('steps', 5))
        steps = min(max(1, steps), 20)  # Обмежуємо між 1 і 20 кроками
        
        # Отримуємо поточний стан світу з БД
        current_mood_data = get_world_mood_from_db()
        
        # Для відстеження згенерованих подій
        events_generated = []
        
        # Виконуємо кроки симуляції
        for _ in range(steps):
            # Генеруємо нову подію
            new_event = generate_random_event()
            events_generated.append(new_event)
            print(f"Згенеровано подію: {new_event['name']} ({new_event['impact']})")
            
            # Застосовуємо подію до стану світу
            current_mood_data = apply_event_to_world(current_mood_data, new_event)
        
        # Зберігаємо фінальний стан світу в БД
        save_world_mood_to_db(current_mood_data)
        
        # Повертаємо оновлений стан світу та список згенерованих подій
        return jsonify({
            "status": "success", 
            "message": f"Виконано {steps} кроків симуляції", 
            "steps_executed": steps,
            "events_generated": events_generated,
            "data": current_mood_data
        })
        
    except Exception as e:
        print(f"Помилка під час виконання симуляції: {str(e)}")
        return jsonify({"status": "error", "message": f"Помилка симуляції: {str(e)}"}), 500

# Функція для налаштування і запуску планувальника
def setup_scheduler():
    try:
        # Додаємо завдання до планувальника
        scheduler.add_job(
            id='autonomous_simulation_job', # Унікальний ідентифікатор завдання
            func=run_autonomous_simulation_step, # Функція, яку потрібно виконати
            trigger='interval', # Тип тригера - інтервал
            minutes=5, # Інтервал - кожні 5 хвилин
            # seconds=30, # Для тестування можна встановити менший інтервал, наприклад, 30 секунд
        )

        # Запускаємо планувальник
        scheduler.start()
        print("Планувальник автономної симуляції запущено")
    except Exception as e:
        print(f"Помилка при налаштуванні планувальника: {str(e)}")
        # Не завершуємо роботу додатка при помилці планувальника

# Маршрут для запуску автономної симуляції без планувальника
@app.route('/api/run-autonomous-step', methods=['GET'])
def api_run_autonomous_step():
    """
    Запускає один крок автономної симуляції.
    Цей маршрут дозволяє тестувати функціональність автономної симуляції
    без необхідності налаштовувати планувальник.
    """
    try:
        # Отримуємо поточний стан світу з БД
        current_mood_data = get_world_mood_from_db()

        # Генеруємо нову подію
        new_event = generate_random_event()
        print(f"Ручний запуск автономної симуляції: Згенеровано подію: {new_event['name']} ({new_event['impact']})")

        # Застосовуємо подію до стану світу
        updated_mood_data = apply_event_to_world(current_mood_data, new_event)

        # Зберігаємо оновлений стан світу в БД
        save_world_mood_to_db(updated_mood_data)

        return jsonify({
            "status": "success", 
            "message": "Крок автономної симуляції успішно виконано", 
            "event": new_event,
            "current_world_state": updated_mood_data
        })

    except Exception as e:
        print(f"Помилка під час виконання кроку автономної симуляції: {str(e)}")
        return jsonify({"status": "error", "message": f"Помилка симуляції: {str(e)}"}), 500

# Викликаємо налаштування планувальника при запуску у Gunicorn
# Але не під час імпорту модуля в main.py, щоб уникнути помилок
if os.environ.get('GUNICORN_ENVIRONMENT') == 'true':
    setup_scheduler()

if __name__ == '__main__':
    # При безпосередньому запуску через python app.py
    setup_scheduler()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)