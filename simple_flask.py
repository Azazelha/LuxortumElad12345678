from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Luxortum - Платформа божественної симуляції</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #121212;
                color: #f0f0f0;
                line-height: 1.6;
            }
            
            .container {
                width: 80%;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            header {
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: #fff;
                border-bottom: 4px solid #4a00e0;
            }
            
            h1 {
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 0 0 10px rgba(74, 0, 224, 0.5);
                animation: glow 3s infinite;
            }
            
            p {
                font-size: 1.2em;
                max-width: 800px;
                margin: 0 auto;
            }
            
            .main-content {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 30px;
                margin-top: 40px;
            }
            
            .feature-card {
                flex: 1 1 300px;
                background: rgba(26, 26, 46, 0.8);
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .feature-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: linear-gradient(90deg, #4a00e0, #8e2de2);
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
            }
            
            .feature-card h2 {
                font-size: 1.8em;
                margin-top: 0;
                margin-bottom: 15px;
                color: #8e2de2;
            }
            
            .feature-card p {
                font-size: 1.1em;
                margin-bottom: 20px;
            }
            
            .btn {
                display: inline-block;
                background: linear-gradient(90deg, #4a00e0, #8e2de2);
                color: white;
                padding: 10px 20px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(142, 45, 226, 0.4);
            }
            
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(142, 45, 226, 0.6);
            }
            
            footer {
                text-align: center;
                padding: 30px 0;
                margin-top: 60px;
                color: #888;
                border-top: 1px solid #333;
            }

            /* Анімація для підсвічування тексту */
            @keyframes glow {
                0% {
                    text-shadow: 0 0 10px rgba(74, 0, 224, 0.5);
                }
                50% {
                    text-shadow: 0 0 20px rgba(142, 45, 226, 0.8), 0 0 30px rgba(74, 0, 224, 0.6);
                }
                100% {
                    text-shadow: 0 0 10px rgba(74, 0, 224, 0.5);
                }
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Luxortum</h1>
            <p>Платформа божественної симуляції</p>
        </header>
        
        <div class="container">
            <div class="main-content">
                <div class="feature-card">
                    <h2>Контекстні Підказки</h2>
                    <p>Інтерактивна система підказок з 5 різними типами персонажів, кожен з яких має унікальний стиль спілкування та анімації.</p>
                    <a href="/tooltip-demo" class="btn">Демонстрація</a>
                </div>
                
                <div class="feature-card">
                    <h2>Настрій Світу</h2>
                    <p>Динамічна система відстеження настрою віртуального світу з візуалізацією інтенсивності емоцій та їх впливу на цифрову реальність.</p>
                    <a href="/world-mood" class="btn">Демонстрація</a>
                </div>

                <div class="feature-card">
                    <h2>Аватар Творця</h2>
                    <p>Унікальна можливість керувати аватаром у віртуальному світі та взаємодіяти з його жителями як божественна сутність.</p>
                    <a href="#" class="btn" onclick="alert('Ця функція буде доступна незабаром!')">Скоро</a>
                </div>
            </div>
        </div>
        
        <footer>
            <p>&copy; 2025 Luxortum. Всі права захищені.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/hello')
def hello():
    return 'Привіт, Luxortum працює!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)