"""
Спрощена версія Luxortum для прямого запуску
"""
from flask import Flask, render_template_string, send_from_directory, jsonify, request, redirect
import os
import time

app = Flask(__name__)

# Простий маршрут
@app.route('/')
def index():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        template = f.read()
    return render_template_string(template)

@app.route('/hello')
def hello():
    return 'Привіт, Luxortum працює!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)