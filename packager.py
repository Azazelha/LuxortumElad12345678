"""
Утиліта для пакування проекту Luxortum для розгортання
"""
import os
import sys
import shutil
import subprocess
import time

def create_deployment_package():
    """Створює пакет для розгортання"""
    timestamp = int(time.time())
    package_name = f"luxortum_deployment_{timestamp}"
    
    # Створюємо директорію для пакета
    os.makedirs(package_name, exist_ok=True)
    
    # Копіюємо основні файли
    files_to_copy = [
        'main.py',
        'app.py',
        'wsgi.py',
        'Procfile',
        'render.yaml',
        'runtime.txt',
        'deploy_instructions.md',
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(package_name, file))
            print(f"✓ Скопійовано файл {file}")
        else:
            print(f"✗ Не знайдено файл {file}")
    
    # Копіюємо директорії
    dirs_to_copy = ['static', 'templates']
    
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(
                dir_name, 
                os.path.join(package_name, dir_name),
                dirs_exist_ok=True
            )
            print(f"✓ Скопійовано директорію {dir_name}")
        else:
            print(f"✗ Не знайдено директорію {dir_name}")
    
    # Створюємо requirements.txt з поточних залежностей
    try:
        with open(os.path.join(package_name, 'requirements.txt'), 'w') as f:
            f.write("""flask==2.3.3
gunicorn==23.0.0
openai==1.21.0
requests==2.32.3
werkzeug==2.3.7
""")
        print("✓ Створено файл requirements.txt")
    except Exception as e:
        print(f"✗ Помилка створення requirements.txt: {e}")
    
    # Архівуємо пакет
    try:
        archive_name = f"{package_name}.tar.gz"
        subprocess.run(['tar', '-czvf', archive_name, package_name])
        print(f"✓ Створено архів {archive_name}")
        
        # Видаляємо тимчасову директорію
        shutil.rmtree(package_name)
        print(f"✓ Видалено тимчасову директорію {package_name}")
        
        print(f"\n✅ Пакет для розгортання готовий: {archive_name}")
        print(f"Використовуйте цей архів для розгортання на будь-якій платформі згідно інструкцій в deploy_instructions.md")
    except Exception as e:
        print(f"✗ Помилка архівування: {e}")

if __name__ == '__main__':
    print("=== Пакування проекту Luxortum для розгортання ===")
    create_deployment_package()