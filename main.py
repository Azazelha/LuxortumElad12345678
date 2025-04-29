"""
Luxortum - Платформа божественної симуляції
Оптимізований проект для демонстрації ключових функцій
"""

import sys
print("Python version:", sys.version)
print("Python path:", sys.path)

try:
    import flask
    print("Flask version:", flask.__version__)
except ImportError as e:
    print("Error importing Flask:", e)

try:
    from app import app
    app.debug = True
    print("App imported successfully")
except Exception as e:
    print("Error importing app:", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)