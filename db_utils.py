"""
Утиліти для роботи з базою даних SQLite у проєкті Luxortum
"""
import sqlite3
import json
import time
import os
from flask import g

# --- Конфігурація Бази Даних ---
DATABASE = 'luxortum_world.db' # Ім'я файлу бази даних SQLite

def get_db():
    """
    Встановлює з'єднання з базою даних, якщо його ще немає,
    і зберігає його у спеціальному об'єкті g Flask.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # Дозволяє отримувати результати як словники
    return g.db

def close_db(e=None):
    """
    Закриває з'єднання з базою даних, якщо воно існує.
    Викликається автоматично після кожного запиту.
    """
    db = g.pop('db', None) # Отримуємо з'єднання з g, якщо воно там є

    if db is not None:
        db.close()

def init_db(app):
    """
    Ініціалізує базу даних: створює таблицю для WORLD_MOOD, якщо вона не існує.
    """
    try:
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("База даних успішно ініціалізована")
    except Exception as e:
        print(f"Помилка при ініціалізації бази даних: {e}")

# --- Функція для отримання стану світу з БД ---
def get_world_mood_from_db():
    """
    Отримує поточний стан WORLD_MOOD з бази даних.
    Якщо запис не знайдено, повертає початковий стан.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM world_mood LIMIT 1")
    row = cursor.fetchone()

    if row:
        # Десеріалізуємо JSON-рядок назад у словник
        try:
            mood_data = json.loads(row['state_data'])
            # Перевіряємо, чи всі необхідні ключі присутні, інакше повертаємо початковий стан
            if all(key in mood_data for key in ['mood', 'intensity', 'timestamp', 'events', 'trend', 'effects']):
                 return mood_data
            else:
                 print("Попередження: Дані в БД неповні, повертаємо початковий стан.")
                 return get_initial_world_mood() # Повертаємо початковий стан, якщо дані в БД неповні
        except json.JSONDecodeError:
            print("Попередження: Невірний формат JSON у базі даних, повертаємо початковий стан.")
            return get_initial_world_mood() # Повертаємо початковий стан, якщо JSON невірний
    else:
        # Якщо запис не знайдено, ініціалізуємо його в БД і повертаємо початковий стан
        initial_mood = get_initial_world_mood()
        save_world_mood_to_db(initial_mood)
        return initial_mood

# --- Функція для збереження стану світу в БД ---
def save_world_mood_to_db(mood_data):
    """
    Зберігає поточний стан WORLD_MOOD у базі даних.
    """
    db = get_db()
    cursor = db.cursor()
    # Серіалізуємо словник стану світу у JSON-рядок для зберігання
    state_data_json = json.dumps(mood_data)

    # Видаляємо старий запис (якщо є) і вставляємо новий
    # Це простий підхід для зберігання одного стану світу
    cursor.execute("DELETE FROM world_mood")
    cursor.execute("INSERT INTO world_mood (state_data) VALUES (?)", (state_data_json,))
    db.commit()

# --- Початковий стан світу (якщо БД порожня або дані невірні) ---
def get_initial_world_mood():
     """Повертає початковий стан WORLD_MOOD."""
     return {
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

# --- Додаткові функції для роботи з історією настрою ---
def save_mood_history(mood, intensity):
    """
    Зберігає запис в історії зміни настрою.
    """
    db = get_db()
    timestamp = int(time.time() * 1000)
    
    db.execute(
        "INSERT INTO mood_history (mood, intensity, timestamp) VALUES (?, ?, ?)",
        (mood, intensity, timestamp)
    )
    db.commit()

def get_mood_history(limit=10):
    """
    Отримує історію зміни настрою.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT mood, intensity, timestamp FROM mood_history ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    return [dict(row) for row in cursor.fetchall()]

def save_world_event(name, impact):
    """
    Зберігає подію у світі.
    """
    try:
        db = get_db()
        timestamp = int(time.time() * 1000)
        
        db.execute(
            "INSERT INTO world_events (name, impact, timestamp) VALUES (?, ?, ?)",
            (name, impact, timestamp)
        )
        db.commit()
        print(f"Подія '{name}' успішно збережена в базі даних")
    except Exception as e:
        print(f"Помилка при збереженні події: {e}")

def get_world_events(limit=20):
    """
    Отримує список подій у світі.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT name, impact, timestamp FROM world_events ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    return [dict(row) for row in cursor.fetchall()]