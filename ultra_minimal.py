"""
Luxortum - Ультра-мінімальна версія для швидкого запуску
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Luxortum працює!</h1><a href="/hello">Перевірити</a>'

@app.route('/hello')
def hello():
    return 'Привіт, світе Luxortum!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)