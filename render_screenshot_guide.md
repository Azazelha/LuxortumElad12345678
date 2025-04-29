# Покрокова інструкція з розгортання Luxortum на Render із зображеннями

## Крок 1: Реєстрація на Render
1. Перейдіть на [render.com](https://render.com/) і натисніть "Sign Up"
2. Створіть новий обліковий запис або увійдіть через GitHub/GitLab

## Крок 2: Створення нового веб-сервісу
1. На панелі керування натисніть кнопку "+ New" у верхньому правому куті
![Render Dashboard](https://docs.render.com/img/dashboard-empty.png)

2. Виберіть "Web Service" зі списку
![New Web Service](https://docs.render.com/img/blueprint-service-type.png)

## Крок 3: Підключення репозиторію
1. Виберіть "Deploy from existing code" внизу сторінки
![Deploy Existing Code](https://docs.render.com/img/existing-code-option.png)

2. Натисніть "Upload Files"
3. Перетягніть ZIP-архів з проектом або виберіть його з диска
4. Натисніть "Upload"

## Крок 4: Налаштування сервісу
1. Заповніть основні налаштування:
   - **Name**: `luxortum`
   - **Region**: Frankfurt (EU Central) або найближчий до вас регіон
   - **Branch**: `main` (за замовчуванням)
![Basic Configuration](https://docs.render.com/img/web-service-create.png)

2. Налаштуйте розділ Build:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
![Build Settings](https://docs.render.com/img/web-service-create-build.png)

3. Додайте змінні середовища:
   - Натисніть "Advanced" щоб розгорнути додаткові налаштування
   - У розділі "Environment Variables" додайте:
     - `PORT`: `8080`
     - `PYTHON_VERSION`: `3.11`
     - `OPENAI_API_KEY`: ваш ключ OpenAI API (якщо потрібно)
![Environment Variables](https://docs.render.com/img/env-groups-editor.png)

4. Натисніть "Create Web Service"

## Крок 5: Відстеження розгортання
1. Render автоматично почне процес розгортання
2. Відстежуйте процес у розділі "Events"
![Deployment Events](https://docs.render.com/img/web-service-events.png)

3. У розділі "Logs" можна побачити детальний журнал розгортання
![Deployment Logs](https://docs.render.com/img/web-service-logs.png)

## Крок 6: Тестування розгорнутого додатку
1. Коли розгортання завершиться успішно, ви отримаєте URL у форматі `https://luxortum.onrender.com`
2. Натисніть на URL, щоб перейти на веб-сайт
3. Переконайтеся, що всі функції працюють:
   - Головна сторінка завантажується правильно
   - Працюють демонстрації контекстних підказок і системи настрою світу
   - Доступні всі статичні ресурси (CSS, JS, зображення)

## Поширені проблеми та їх вирішення

### Проблема: Додаток не запускається
**Симптом**: Сторінка показує помилку 503 Service Unavailable
**Рішення**:
1. Перевірте логи у розділі "Logs"
2. Впевніться, що у вашому додатку використовується змінна оточення `PORT`
3. Переконайтеся, що команда запуску правильна: `gunicorn main:app`

### Проблема: Статичні файли не завантажуються
**Симптом**: Сторінка виглядає не оформленою, відсутні стилі або зображення
**Рішення**:
1. Перевірте, чи статичні файли знаходяться у папці `static/`
2. Переконайтеся, що в коді використовуються правильні шляхи до статичних файлів

### Проблема: Помилки імпорту модулів
**Симптом**: У логах помилки на кшталт `ModuleNotFoundError: No module named 'xyz'`
**Рішення**:
1. Додайте відсутні залежності до файлу `requirements.txt`
2. Виконайте повторне розгортання через "Manual Deploy"

## Налаштування постійної роботи (для платних планів)
За замовчуванням на безкоштовному плані Render, веб-сервіс "засинає" після 15 хвилин неактивності.

Для постійної роботи:
1. Перейдіть до налаштувань сервісу
2. У розділі "Suspended" змініть налаштування на "Never Suspend"
![Suspend Settings](https://docs.render.com/img/web-service-suspend.png)

## Налаштування власного домену (для платних планів)
1. Перейдіть до налаштувань сервісу
2. У розділі "Custom Domain" натисніть "Add Custom Domain"
3. Введіть ваш домен і слідуйте інструкціям для налаштування DNS
![Custom Domain](https://docs.render.com/img/custom-domains-add.png)

## Додаткові ресурси
- [Офіційна документація Render](https://docs.render.com/)
- [Приклади Python додатків на Render](https://github.com/render-examples)
- [Render Community Discord](https://render.com/chat)