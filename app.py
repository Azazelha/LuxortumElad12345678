"""
Luxortum - Платформа божественної симуляції
Оптимізований проект для демонстрації ключових функцій
"""
import os
import time
import flask
from flask import Flask, send_from_directory, jsonify, request, redirect

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "luxortum_secret_key")

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
            return f"<h1>Luxortum</h1><p>Проект запущено. Помилка відображення головної сторінки: {str(e)}</p>"

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
    global WORLD_MOOD
    
    if request.method == 'POST':
        # Оновлення настрою світу
        try:
            data = request.json
            
            # Оновлюємо поля, якщо вони присутні
            if 'mood' in data:
                WORLD_MOOD['mood'] = data['mood']
                
            if 'intensity' in data:
                WORLD_MOOD['intensity'] = data['intensity']
                
            if 'events' in data and isinstance(data['events'], list):
                for event in data['events']:
                    if 'name' in event and 'impact' in event:
                        new_event = {
                            'name': event['name'],
                            'impact': event['impact'],
                            'timestamp': event.get('timestamp', int(time.time() * 1000))
                        }
                        WORLD_MOOD['events'].insert(0, new_event)
                        
                # Обмежуємо кількість подій
                if len(WORLD_MOOD['events']) > 20:
                    WORLD_MOOD['events'] = WORLD_MOOD['events'][:20]
            
            # Обчислюємо ефекти для нового настрою
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
            
            mood = WORLD_MOOD['mood']
            if mood in mood_effects:
                WORLD_MOOD['effects'] = mood_effects[mood]
            
            # Оновлюємо часову мітку
            WORLD_MOOD['timestamp'] = int(time.time() * 1000)
            
            return jsonify({"status": "success", "data": WORLD_MOOD})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        # Отримання поточного настрою світу
        return jsonify(WORLD_MOOD)

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)