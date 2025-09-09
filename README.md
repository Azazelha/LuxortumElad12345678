# Автоматичний деплой через Vercel

Цей проект автоматично деплоїться на [Vercel](https://vercel.com/) після кожного коміту в GitHub. Нижче інструкція, як налаштувати все з нуля.

---

## 1. Встановлення залежностей

Перед стартом:
```bash
npm install
```

---

## 2. Підключення GitHub до Vercel

1. Перейди на [https://vercel.com/import/git](https://vercel.com/import/git)
2. Авторизуйся через GitHub
3. Обери свій репозиторій
4. Натисни **"Import"**

Vercel автоматично розпізнає фреймворк (React, Next.js, тощо) та підставить правильні налаштування.

---

## 3. Структура та маршрутизація

Усі сторінки мають бути всередині папки `pages/`.

**Приклад:**
```
pages/
  index.js        # головна сторінка
  about.js        # сторінка /about
```

---

## 4. Автодеплой

Після підключення до GitHub:

- Кожен `git push` викликає автоматичний деплой
- Доступна продакшн-версія: `https://your-project-name.vercel.app`

---

## 5. Конфігурація Vercel (опційно)

Файл `vercel.json` для маршрутизації:

```json
{
  "version": 2,
  "builds": [
    { "src": "next.config.js", "use": "@vercel/next" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/" }
  ]
}
```

---

## 6. Тестування деплоя

- Перейди за лінком, який Vercel згенерує після пушу
- Перевір, що відображаються усі сторінки
- У разі помилки 404 — переконайся, що є `pages/index.js` і всі сторінки експортують функції:

```js
export default function Home() {
  return <div>Hello World</div>
}
```

---

## 7. Приклади використання анімації (Framer Motion)

```bash
npm install framer-motion
```

```js
import { motion } from 'framer-motion'

export default function StageDisplay({ phase, stageIndex }) {
  return (
    <motion.div
      key={stageIndex}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
    >
      <h2>{phase.name}</h2>
      <p>{phase.stages[stageIndex]}</p>
    </motion.div>
  );
}
```

---

## 8. Контакт

З питаннями або помилками звертайся в Issues або pull request.