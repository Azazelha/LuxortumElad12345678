-- Схема бази даних для Luxortum
-- Таблиця для зберігання стану настрою світу
CREATE TABLE IF NOT EXISTS world_mood (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_data TEXT NOT NULL,  -- Серіалізований JSON з даними стану світу
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000)  -- Unix timestamp в мілісекундах
);

-- Можливе розширення для зберігання історії зміни настроїв
CREATE TABLE IF NOT EXISTS mood_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT NOT NULL,  -- Код настрою (peaceful, joyful, anxious, тощо)
    intensity REAL NOT NULL,  -- Значення від 0 до 1
    timestamp INTEGER NOT NULL,  -- Unix timestamp в мілісекундах
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000)
);

-- Таблиця для зберігання подій
CREATE TABLE IF NOT EXISTS world_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    impact TEXT NOT NULL,  -- positive, neutral, negative
    timestamp INTEGER NOT NULL,  -- Unix timestamp в мілісекундах
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000)
);