"""
Luxortum - спрощена версія для демонстрації
"""
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Luxortum</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #121212;
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }
            
            h1 {
                color: #8e2de2;
                font-size: 3rem;
                margin-bottom: 0.5rem;
                text-shadow: 0 0 10px rgba(142, 45, 226, 0.5);
            }
            
            p {
                font-size: 1.5rem;
                margin-bottom: 2rem;
            }
            
            .animated-text {
                animation: glow 3s infinite;
            }
            
            @keyframes glow {
                0% { text-shadow: 0 0 10px rgba(142, 45, 226, 0.5); }
                50% { text-shadow: 0 0 20px rgba(142, 45, 226, 0.8), 0 0 30px rgba(74, 0, 224, 0.6); }
                100% { text-shadow: 0 0 10px rgba(142, 45, 226, 0.5); }
            }
        </style>
    </head>
    <body>
        <h1 class="animated-text">Luxortum</h1>
        <p>Платформа божественної симуляції</p>
        <p>Сервер запущено успішно!</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)