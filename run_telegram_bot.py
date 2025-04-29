#!/usr/bin/env python3
"""
Скрипт для запуску Telegram-бота Luxortum
"""

import os
import logging
from telegram_bot import main

if __name__ == "__main__":
    # Налаштування логування
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger("luxortum_bot")
    
    # Перевіряємо наявність токена
    if not os.environ.get("TELEGRAM_TOKEN"):
        logger.error("ПОМИЛКА: Не знайдено змінну оточення TELEGRAM_TOKEN")
        print("Для роботи бота необхідно встановити змінну оточення TELEGRAM_TOKEN.")
        print("Приклад: export TELEGRAM_TOKEN=your_token_here")
        exit(1)
    
    logger.info("Запуск Telegram-бота Luxortum...")
    main()