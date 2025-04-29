"""
Тестовий файл для перевірки функцій генерації подій через OpenAI
"""
import json
import os
from openai import OpenAI

# Ініціалізуємо клієнт OpenAI
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
print("OpenAI клієнт ініціалізовано")

def generate_event_description_with_ai(event_name, event_impact, base_description):
    """
    Генерує більш детальний опис події за допомогою OpenAI.
    """
    prompt = f"Напиши короткий, містичний опис для події у світі божественної симуляції. Подія: '{event_name}'. Її вплив: '{event_impact}'. Базовий опис: '{base_description}'. Опис має бути в українській мові, до 50 слів."

    try:
        # Виконуємо запит до OpenAI API
        chat_completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o", # Використовуємо найновішу модель
            max_tokens=100 # Обмежуємо довжину відповіді
        )
        # Отримуємо згенерований текст
        ai_description = chat_completion.choices[0].message.content.strip()
        return ai_description

    except Exception as e:
        print(f"Помилка під час генерації опису події за допомогою OpenAI: {str(e)}")
        return base_description

# Тестуємо різні типи подій
test_events = [
    {"name": "Божественне втручання", "impact": "positive", "base_description": "Світ отримав благословення. Відчувається приплив позитивної енергії."},
    {"name": "Прояв хаосу", "impact": "negative", "base_description": "Силами хаосу посіяно розбрат. Зростає напруженість."},
    {"name": "Гармонійне вирівнювання", "impact": "neutral", "base_description": "Енергії світу збалансовано. Відновлюється рівновага."}
]

# Головна функція для запуску тесту
def main():
    print("Початок тестування генерації описів подій через OpenAI...")
    
    results = []
    
    for event in test_events:
        print(f"Генерація опису для події: {event['name']}...")
        
        description = generate_event_description_with_ai(
            event['name'],
            event['impact'],
            event['base_description']
        )
        
        print(f"Згенерований опис: {description}")
        
        results.append({
            "event": event['name'],
            "impact": event['impact'],
            "original_description": event['base_description'],
            "ai_description": description
        })
    
    # Зберігаємо результати для перевірки
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("Тестування завершено. Результати збережено в test_results.json")

if __name__ == "__main__":
    main()