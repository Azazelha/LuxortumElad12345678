"""
Luxortum - Інтеграція з Telegram
Модуль для створення та керування ботом Telegram
"""

import os
import logging
import json
import sqlite3
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler
from telegram.constants import ParseMode

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Стани для ConversationHandler
(MAIN_MENU, MOOD_SELECTION, SIMULATION_MENU,
 EVENT_HISTORY, MOOD_HISTORY, SETTINGS) = range(6)

# Отримання токена з змінних середовища
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Функції для роботи з базою даних (ті самі, що й у ultra_fast.py)
def get_db_connection():
    conn = sqlite3.connect('luxortum_world.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_world_mood():
    conn = get_db_connection()
    try:
        mood_record = conn.execute('SELECT data FROM world_mood WHERE id = 1').fetchone()
        
        if mood_record:
            return json.loads(mood_record['data'])
        else:
            # Початковий стан, якщо запис не знайдено
            initial_mood = get_initial_world_mood()
            save_world_mood(initial_mood)
            return initial_mood
    finally:
        conn.close()

def save_world_mood(mood_data):
    conn = get_db_connection()
    try:
        mood_json = json.dumps(mood_data)
        
        record_exists = conn.execute('SELECT 1 FROM world_mood WHERE id = 1').fetchone() is not None
        
        if record_exists:
            conn.execute('UPDATE world_mood SET data = ? WHERE id = 1', (mood_json,))
        else:
            conn.execute('INSERT INTO world_mood (id, data) VALUES (1, ?)', (mood_json,))
        
        conn.commit()
    finally:
        conn.close()

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

def get_mood_history(limit=10):
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'SELECT mood, intensity, timestamp FROM mood_history ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        history = []
        for row in cursor:
            history.append({
                "mood": row['mood'],
                "intensity": row['intensity'],
                "timestamp": row['timestamp']
            })
        return history
    finally:
        conn.close()

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

def get_world_events(limit=20):
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'SELECT name, impact, timestamp FROM world_events ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        events = []
        for row in cursor:
            events.append({
                "name": row['name'],
                "impact": row['impact'],
                "timestamp": row['timestamp']
            })
        return events
    finally:
        conn.close()

# Функції для локалізації повідомлень та форматування
def get_mood_name(mood):
    mood_names = {
        'ecstatic': '🤩 Екстатичний',
        'joyful': '😊 Радісний',
        'peaceful': '😌 Мирний',
        'neutral': '😐 Нейтральний',
        'anxious': '😟 Тривожний',
        'melancholic': '😔 Меланхолійний',
        'sad': '😢 Сумний',
        'angry': '😠 Злий',
        'chaotic': '🌪️ Хаотичний'
    }
    return mood_names.get(mood, mood)

def get_trend_name(trend):
    trend_names = {
        'ascending': '📈 Покращується',
        'stable': '➡️ Стабільний',
        'descending': '📉 Погіршується',
        'fluctuating': '↕️ Коливається'
    }
    return trend_names.get(trend, trend)

def get_effect_name(effect):
    effect_names = {
        'happiness': 'Щастя',
        'stability': 'Стабільність',
        'creativity': 'Творчість',
        'knowledge': 'Знання',
        'harmony': 'Гармонія'
    }
    return effect_names.get(effect, effect)

def get_impact_emoji(impact):
    impact_emojis = {
        'positive': '✅',
        'neutral': '➖',
        'negative': '❌'
    }
    return impact_emojis.get(impact, '❓')

# Функції телеграм-бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Надсилає вітальне повідомлення та клавіатуру з опціями"""
    user = update.effective_user
    
    keyboard = [
        [
            InlineKeyboardButton("🌍 Стан світу", callback_data="world_state"),
            InlineKeyboardButton("🎭 Змінити настрій", callback_data="change_mood")
        ],
        [
            InlineKeyboardButton("🔮 Симуляція", callback_data="simulation"),
            InlineKeyboardButton("📊 Історія подій", callback_data="event_history")
        ],
        [
            InlineKeyboardButton("📈 Історія настрою", callback_data="mood_history"),
            InlineKeyboardButton("⚙️ Налаштування", callback_data="settings")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_html(
        f"Вітаю, {user.mention_html()}! Я бот <b>Luxortum</b> - платформи божественної симуляції.\n\n"
        f"Через мене ви можете керувати симуляцією світу та отримувати інформацію про його стан.\n\n"
        f"Що бажаєте зробити?",
        reply_markup=reply_markup
    )
    
    return MAIN_MENU

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Надсилає повідомлення з допомогою, коли надходить команда /help"""
    await update.message.reply_text(
        "Доступні команди:\n\n"
        "/start - Почати взаємодію з ботом\n"
        "/help - Отримати список команд\n"
        "/state - Дізнатися поточний стан світу\n"
        "/simulate - Запустити крок автономної симуляції\n"
        "/history - Переглянути історію подій\n"
        "/cancel - Скасувати поточну операцію"
    )

async def world_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показує поточний стан світу"""
    query = update.callback_query
    if query:
        await query.answer()
    
    try:
        mood_data = get_world_mood()
        
        # Форматуємо повідомлення з інформацією про стан світу
        message = "<b>🌍 ПОТОЧНИЙ СТАН СВІТУ</b>\n\n"
        message += f"<b>Настрій:</b> {get_mood_name(mood_data['mood'])}\n"
        message += f"<b>Інтенсивність:</b> {int(mood_data['intensity'] * 100)}%\n"
        message += f"<b>Тренд:</b> {get_trend_name(mood_data['trend'])}\n\n"
        
        # Додаємо інформацію про ефекти
        if 'effects' in mood_data and mood_data['effects']:
            message += "<b>ЕФЕКТИ:</b>\n"
            for effect, value in mood_data['effects'].items():
                modifier = "+" if value > 0 else ""
                message += f"• {get_effect_name(effect)}: {modifier}{value}\n"
            message += "\n"
        
        # Додаємо останні події (до 3)
        if 'events' in mood_data and mood_data['events']:
            message += "<b>ОСТАННІ ПОДІЇ:</b>\n"
            recent_events = mood_data['events'][:3]
            for event in recent_events:
                event_time = datetime.fromtimestamp(event['timestamp'] / 1000).strftime('%d.%m %H:%M')
                message += f"• {get_impact_emoji(event['impact'])} {event_time}: {event['name']}\n"
        
        # Додаємо час останнього оновлення
        if 'last_update' in mood_data:
            last_update = datetime.fromtimestamp(mood_data['last_update'] / 1000).strftime('%d.%m.%Y %H:%M:%S')
            message += f"\n<i>Останнє оновлення: {last_update}</i>"
        
        # Клавіатура з опціями
        keyboard = [
            [
                InlineKeyboardButton("🔄 Оновити", callback_data="world_state"),
                InlineKeyboardButton("🎭 Змінити настрій", callback_data="change_mood")
            ],
            [
                InlineKeyboardButton("🔮 Запустити симуляцію", callback_data="run_simulation"),
                InlineKeyboardButton("« Назад", callback_data="back_to_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Надсилаємо повідомлення
        if query:
            await query.edit_message_text(
                message, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_html(message, reply_markup=reply_markup)
    
    except Exception as e:
        error_message = f"Помилка при отриманні стану світу: {str(e)}"
        logger.error(error_message)
        
        if query:
            await query.edit_message_text(error_message)
        else:
            await update.message.reply_text(error_message)

async def change_mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показує опції для зміни настрою світу"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🤩 Екстатичний", callback_data="mood_ecstatic"),
            InlineKeyboardButton("😊 Радісний", callback_data="mood_joyful"),
            InlineKeyboardButton("😌 Мирний", callback_data="mood_peaceful")
        ],
        [
            InlineKeyboardButton("😐 Нейтральний", callback_data="mood_neutral"),
            InlineKeyboardButton("😟 Тривожний", callback_data="mood_anxious")
        ],
        [
            InlineKeyboardButton("😔 Меланхолійний", callback_data="mood_melancholic"),
            InlineKeyboardButton("😢 Сумний", callback_data="mood_sad")
        ],
        [
            InlineKeyboardButton("😠 Злий", callback_data="mood_angry"),
            InlineKeyboardButton("🌪️ Хаотичний", callback_data="mood_chaotic")
        ],
        [
            InlineKeyboardButton("« Назад", callback_data="back_to_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Оберіть новий настрій світу:",
        reply_markup=reply_markup
    )
    
    return MOOD_SELECTION

async def update_mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Оновлює настрій світу та показує поточний стан"""
    query = update.callback_query
    await query.answer()
    
    # Отримуємо вибраний настрій
    data = query.data
    if data.startswith("mood_"):
        selected_mood = data[5:]  # Видаляємо префікс "mood_"
        
        try:
            # Отримуємо поточні дані про настрій
            current_mood = get_world_mood()
            
            # Оновлюємо настрій
            current_mood['mood'] = selected_mood
            current_mood['last_update'] = datetime.now().timestamp() * 1000
            
            # Зберігаємо оновлений настрій
            save_world_mood(current_mood)
            
            # Зберігаємо запис в історії
            save_mood_history(selected_mood, current_mood['intensity'])
            
            await query.edit_message_text(
                f"✅ Настрій світу успішно змінено на: {get_mood_name(selected_mood)}!\n\n"
                "Зачекайте, отримую оновлені дані..."
            )
            
            # Показуємо оновлений стан світу
            await world_state(update, context)
            
        except Exception as e:
            await query.edit_message_text(
                f"❌ Помилка при оновленні настрою світу: {str(e)}\n\n"
                "Спробуйте пізніше."
            )
    
    return MAIN_MENU

async def simulation_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показує меню симуляції"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🔮 Запустити один крок", callback_data="run_simulation")
        ],
        [
            InlineKeyboardButton("🔄 Запустити 5 кроків", callback_data="run_multi_simulation")
        ],
        [
            InlineKeyboardButton("📊 Показати результати", callback_data="simulation_results")
        ],
        [
            InlineKeyboardButton("« Назад", callback_data="back_to_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="<b>🔮 МЕНЮ СИМУЛЯЦІЇ</b>\n\n"
             "Оберіть операцію симуляції, яку бажаєте виконати.\n\n"
             "<i>Запуск симуляції генерує випадкові події та змінює стан світу відповідно до їх впливу.</i>",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    
    return SIMULATION_MENU

async def run_simulation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запускає один крок автономної симуляції"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text("⏳ Запуск симуляції...")
    
    try:
        # Отримуємо поточний настрій світу
        current_mood_data = get_world_mood()
        
        # Імітуємо генерацію події (як у ultra_fast.py)
        import random
        
        event = {
            "name": f"Подія #{random.randint(1000, 9999)}",
            "description": "Автоматично згенерована подія через Telegram",
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
        
        # Формуємо повідомлення з результатами
        result_message = "<b>✅ КРОК СИМУЛЯЦІЇ ВИКОНАНО</b>\n\n"
        result_message += f"<b>Подія:</b> {event['name']}\n"
        result_message += f"<b>Опис:</b> {event['description']}\n"
        result_message += f"<b>Вплив:</b> {get_impact_emoji(event['impact'])} {event['impact']}\n"
        result_message += f"<b>Інтенсивність:</b> {int(event['intensity'] * 100)}%\n\n"
        
        result_message += "<b>НОВИЙ СТАН СВІТУ:</b>\n"
        result_message += f"<b>Настрій:</b> {get_mood_name(current_mood_data['mood'])}\n"
        result_message += f"<b>Інтенсивність:</b> {int(current_mood_data['intensity'] * 100)}%\n"
        result_message += f"<b>Тренд:</b> {get_trend_name(current_mood_data['trend'])}\n"
        
        # Клавіатура з опціями
        keyboard = [
            [
                InlineKeyboardButton("🔮 Запустити ще раз", callback_data="run_simulation")
            ],
            [
                InlineKeyboardButton("🌍 Стан світу", callback_data="world_state"),
                InlineKeyboardButton("« Назад до меню", callback_data="simulation")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            result_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await query.edit_message_text(
            f"❌ Помилка під час виконання симуляції: {str(e)}\n"
            "Спробуйте пізніше або зверніться до адміністратора системи."
        )
    
    return SIMULATION_MENU

async def run_multi_simulation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запускає кілька кроків автономної симуляції"""
    query = update.callback_query
    await query.answer()
    
    steps = 5  # Кількість кроків для виконання
    await query.edit_message_text(f"⏳ Запуск симуляції ({steps} кроків)...")
    
    try:
        events_generated = []
        
        # Виконуємо вказану кількість кроків симуляції
        for i in range(steps):
            # Отримуємо поточний настрій світу
            current_mood_data = get_world_mood()
            
            # Імітуємо генерацію події
            import random
            
            event = {
                "name": f"Подія #{random.randint(1000, 9999)}",
                "description": f"Автоматично згенерована подія через Telegram (крок {i+1}/{steps})",
                "impact": random.choice(["positive", "neutral", "negative"]),
                "intensity": random.uniform(0.1, 0.5),
                "timestamp": datetime.now().timestamp() * 1000
            }
            
            # Зберігаємо подію для звіту
            events_generated.append(event)
            
            # Застосовуємо вплив події на настрій світу (той самий код, що і для одного кроку)
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
        
        # Формуємо повідомлення з результатами
        result_message = f"<b>✅ ВИКОНАНО {steps} КРОКІВ СИМУЛЯЦІЇ</b>\n\n"
        
        result_message += "<b>ЗГЕНЕРОВАНІ ПОДІЇ:</b>\n"
        for idx, event in enumerate(events_generated[:3]):  # Показуємо перші 3 події
            result_message += f"{idx+1}. {get_impact_emoji(event['impact'])} {event['name']}\n"
        
        if len(events_generated) > 3:
            result_message += f"... та ще {len(events_generated) - 3} подій\n"
        
        result_message += "\n<b>НОВИЙ СТАН СВІТУ:</b>\n"
        result_message += f"<b>Настрій:</b> {get_mood_name(current_mood_data['mood'])}\n"
        result_message += f"<b>Інтенсивність:</b> {int(current_mood_data['intensity'] * 100)}%\n"
        result_message += f"<b>Тренд:</b> {get_trend_name(current_mood_data['trend'])}\n"
        
        # Клавіатура з опціями
        keyboard = [
            [
                InlineKeyboardButton("🔄 Запустити ще раз", callback_data="run_multi_simulation")
            ],
            [
                InlineKeyboardButton("🌍 Стан світу", callback_data="world_state"),
                InlineKeyboardButton("« Назад до меню", callback_data="simulation")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            result_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await query.edit_message_text(
            f"❌ Помилка під час виконання симуляції: {str(e)}\n"
            "Спробуйте пізніше або зверніться до адміністратора системи."
        )
    
    return SIMULATION_MENU

async def event_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показує історію подій"""
    query = update.callback_query
    await query.answer()
    
    try:
        events = get_world_events(10)  # Отримуємо останні 10 подій
        
        if events:
            message = "<b>📊 ІСТОРІЯ ПОДІЙ</b>\n\n"
            
            for idx, event in enumerate(events):
                event_time = datetime.fromtimestamp(event['timestamp'] / 1000).strftime('%d.%m %H:%M:%S')
                impact_emoji = get_impact_emoji(event['impact'])
                message += f"{idx+1}. {impact_emoji} <b>{event_time}</b> - {event['name']}\n"
        else:
            message = "📊 Історія подій порожня."
        
        keyboard = [
            [
                InlineKeyboardButton("🔄 Оновити", callback_data="event_history")
            ],
            [
                InlineKeyboardButton("« Назад", callback_data="back_to_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await query.edit_message_text(
            f"❌ Помилка при отриманні історії подій: {str(e)}\n"
            "Спробуйте пізніше або зверніться до адміністратора системи."
        )
    
    return EVENT_HISTORY

async def mood_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показує історію змін настрою"""
    query = update.callback_query
    await query.answer()
    
    try:
        history = get_mood_history(10)  # Отримуємо останні 10 записів історії
        
        if history:
            message = "<b>📈 ІСТОРІЯ ЗМІН НАСТРОЮ</b>\n\n"
            
            for idx, record in enumerate(history):
                history_time = datetime.fromtimestamp(record['timestamp'] / 1000).strftime('%d.%m %H:%M:%S')
                mood_name = get_mood_name(record['mood'])
                intensity = int(record['intensity'] * 100)
                message += f"{idx+1}. <b>{history_time}</b> - {mood_name} ({intensity}%)\n"
        else:
            message = "📈 Історія змін настрою порожня."
        
        keyboard = [
            [
                InlineKeyboardButton("🔄 Оновити", callback_data="mood_history")
            ],
            [
                InlineKeyboardButton("« Назад", callback_data="back_to_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await query.edit_message_text(
            f"❌ Помилка при отриманні історії настрою: {str(e)}\n"
            "Спробуйте пізніше або зверніться до адміністратора системи."
        )
    
    return MOOD_HISTORY

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показує налаштування бота"""
    query = update.callback_query
    await query.answer()
    
    message = "<b>⚙️ НАЛАШТУВАННЯ</b>\n\n"
    message += "Тут будуть доступні налаштування для бота."
    
    keyboard = [
        [
            InlineKeyboardButton("« Назад", callback_data="back_to_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    
    return SETTINGS

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Повертає до головного меню"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🌍 Стан світу", callback_data="world_state"),
            InlineKeyboardButton("🎭 Змінити настрій", callback_data="change_mood")
        ],
        [
            InlineKeyboardButton("🔮 Симуляція", callback_data="simulation"),
            InlineKeyboardButton("📊 Історія подій", callback_data="event_history")
        ],
        [
            InlineKeyboardButton("📈 Історія настрою", callback_data="mood_history"),
            InlineKeyboardButton("⚙️ Налаштування", callback_data="settings")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Головне меню Luxortum. Оберіть опцію:",
        reply_markup=reply_markup
    )
    
    return MAIN_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Скасовує поточну операцію та завершує розмову"""
    user = update.message.from_user
    logger.info("Користувач %s скасував розмову.", user.first_name)
    
    await update.message.reply_text(
        "Операцію скасовано. Щоб почати знову, надішліть /start"
    )
    
    return ConversationHandler.END

async def state_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє команду /state"""
    await world_state(update, context)

async def simulate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє команду /simulate"""
    # Створюємо фіктивний callback_query для run_simulation
    class MockQuery:
        async def answer(self):
            pass
        
        async def edit_message_text(self, text, reply_markup=None, parse_mode=None):
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    
    update.callback_query = MockQuery()
    await run_simulation(update, context)

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє команду /history"""
    # Створюємо фіктивний callback_query для event_history
    class MockQuery:
        async def answer(self):
            pass
        
        async def edit_message_text(self, text, reply_markup=None, parse_mode=None):
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    
    update.callback_query = MockQuery()
    await event_history(update, context)

def main() -> None:
    """Запуск бота"""
    # Створення додатку
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Додавання обробників для базових команд
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("state", state_command))
    application.add_handler(CommandHandler("simulate", simulate_command))
    application.add_handler(CommandHandler("history", history_command))
    
    # Додавання ConversationHandler для інтерактивного спілкування
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(world_state, pattern="^world_state$"),
                CallbackQueryHandler(change_mood, pattern="^change_mood$"),
                CallbackQueryHandler(simulation_menu, pattern="^simulation$"),
                CallbackQueryHandler(event_history, pattern="^event_history$"),
                CallbackQueryHandler(mood_history, pattern="^mood_history$"),
                CallbackQueryHandler(settings, pattern="^settings$"),
                CallbackQueryHandler(run_simulation, pattern="^run_simulation$")
            ],
            MOOD_SELECTION: [
                CallbackQueryHandler(update_mood, pattern="^mood_"),
                CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$")
            ],
            SIMULATION_MENU: [
                CallbackQueryHandler(run_simulation, pattern="^run_simulation$"),
                CallbackQueryHandler(run_multi_simulation, pattern="^run_multi_simulation$"),
                CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"),
                CallbackQueryHandler(simulation_menu, pattern="^simulation$")
            ],
            EVENT_HISTORY: [
                CallbackQueryHandler(event_history, pattern="^event_history$"),
                CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$")
            ],
            MOOD_HISTORY: [
                CallbackQueryHandler(mood_history, pattern="^mood_history$"),
                CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$")
            ],
            SETTINGS: [
                CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$")
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    application.add_handler(conv_handler)
    
    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()