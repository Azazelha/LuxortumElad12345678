import requests
import time
import os

def save_webpage(url, output_file):
    try:
        response = requests.get(url, timeout=5)
        with open(output_file, 'wb') as f:
            f.write(response.content)
        return f"Successfully saved {url} to {output_file}"
    except Exception as e:
        return f"Error saving {url}: {str(e)}"

# Зберігаємо HTML файли для візуального ознайомлення
print(save_webpage("http://localhost:5000/", "homepage.html"))
print(save_webpage("http://localhost:5000/tooltip-demo", "tooltip_demo.html"))
print(save_webpage("http://localhost:5000/world-mood", "world_mood.html"))
print(save_webpage("http://localhost:5000/api/tooltips", "tooltips_api.json"))
print(save_webpage("http://localhost:5000/api/world-mood", "world_mood_api.json"))

print("\nПеревіряємо стан сервера:")
os.system("ps aux | grep python | grep -v grep")