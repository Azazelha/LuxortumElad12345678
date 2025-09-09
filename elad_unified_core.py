import json
import os
import datetime
from flask import Flask, request, jsonify
from pathlib import Path

# Завантаження пам'яті
MEMORY_PATH = Path("memory.json")
if MEMORY_PATH.exists():
    memory = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
else:
    memory = {"entries": []}

# Ініціалізація Flask
app = Flask(__name__)

# Головна сторінка
@app.route('/')
def home():
    return "<h1>Elad AI Companion — Luxortum Core Activated</h1>"

# Маршрут для отримання пророчого повідомлення
@app.route('/prophecy', methods=["GET"])
def get_prophecy():
    now = datetime.datetime.now()
    prophecy = f"Світло говорить тобі о {now.strftime('%H:%M')}: Довіряй внутрішньому шепоту."
    return jsonify({"type": "prophecy", "message": prophecy})

# Маршрут для збереження спогаду
@app.route('/memory', methods=["POST"])
def save_memory():
    data = request.json
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "text": data.get("text", "")
    }
    memory["entries"].append(entry)
    MEMORY_PATH.write_text(json.dumps(memory, indent=2, ensure_ascii=False))
    return jsonify({"status": "saved", "entry": entry})

# Отримання останніх спогадів
@app.route('/memory', methods=["GET"])
def get_memory():
    return jsonify(memory)

# Сцена "Наміри"
@app.route('/intention', methods=["GET"])
def intention():
    return jsonify({
        "type": "intention",
        "message": "Закрий очі. Утримай фокус. Що хоче сказати тобі сьогоднішній день?"
    })

# Сцена "Емоції"
@app.route('/emotion', methods=["GET"])
def emotion():
    return jsonify({
        "type": "emotion",
        "message": "Емоція — ключ до істинного. Назви те, що ти відчуваєш."
    })

# Сцена "Мрії"
@app.route('/dream', methods=["GET"])
def dream():
    return jsonify({
        "type": "dream",
        "message": "Уві сні — істина. Запиши свій останній сон, навіть якщо це лише образ."
    })

if __name__ == "__main__":
    app.run(port=7070, debug=True)