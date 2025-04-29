# Інструкції з розгортання проекту Luxortum

## Варіант 1: Розгортання на Render

Render - це сучасна платформа для хостингу, яка чудово підходить для Flask додатків.

### Кроки для розгортання:

1. Зареєструйтесь на [Render](https://render.com/) (безкоштовний рівень доступний)
2. Створіть новий веб-сервіс:
   - Натисніть "New +" і виберіть "Web Service"
   - Завантажте архів проекту `luxortum_deployment_package.tar.gz` або підключіть GitHub репозиторій
   - Виберіть тип "Python"
   - Налаштуйте:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn main:app`
   - Додайте змінні середовища:
     - `PYTHON_VERSION`: 3.11
     - `PORT`: 8080
3. Натисніть "Create Web Service"

## Варіант 2: Розгортання на Heroku

Heroku також добре підтримує Python додатки.

### Кроки для розгортання:

1. Зареєструйтесь на [Heroku](https://www.heroku.com/) (безкоштовний рівень для testing доступний)
2. Встановіть [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Увійдіть в Heroku через термінал: `heroku login`
4. Створіть новий додаток: `heroku create luxortum`
5. Розпакуйте архів `luxortum_deployment_package.tar.gz`
6. Ініціалізуйте Git репозиторій і зробіть коміт:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   ```
7. Відправте код на Heroku:
   ```
   git push heroku master
   ```

## Варіант 3: Розгортання на PythonAnywhere

PythonAnywhere спеціалізується на хостингу Python додатків.

### Кроки для розгортання:

1. Зареєструйтесь на [PythonAnywhere](https://www.pythonanywhere.com/)
2. Створіть новий веб-додаток:
   - Виберіть Flask і Python 3.8+
   - Завантажте архів `luxortum_deployment_package.tar.gz` через "Files"
   - Розпакуйте архів
3. Налаштуйте WSGI файл (автоматично створений):
   - Переконайтесь, що він імпортує `app` з `main`
4. Перезавантажте веб-додаток

## Структура проекту

Архів `luxortum_deployment_package.tar.gz` містить:

- `app.py`: Основний код додатку
- `main.py`: Точка входу для WSGI серверів
- `main_minimal.py` і `super_simple.py`: Спрощені версії для тестування
- `static/`: Статичні файли (CSS, JS, зображення)
- `templates/`: HTML шаблони
- `render.yaml`: Конфігурація для Render
- `Procfile`: Конфігурація для Heroku

## Тестування після розгортання

Після успішного розгортання відвідайте головну сторінку вашого додатку (URL буде надано платформою) щоб переконатись, що все працює правильно.

Ви повинні побачити головну сторінку Luxortum з доступом до демонстрації контекстних підказок і системи настрою світу.