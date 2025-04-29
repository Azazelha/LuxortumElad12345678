"""
Симуляція розгортання проекту Luxortum на Heroku
Перевіряє, чи проект правильно сконфігуровано відповідно до вимог Heroku
"""
import os
import sys
import json
import subprocess

def validate_procfile():
    """Перевіряє Procfile на відповідність вимогам Heroku"""
    if not os.path.exists('Procfile'):
        print("✗ Файл Procfile не знайдено")
        return False
    
    try:
        with open('Procfile', 'r') as f:
            content = f.read().strip()
        
        # Перевіряємо формат
        if not content.startswith('web:'):
            print("✗ Procfile має починатися з 'web:'")
            return False
        
        # Перевіряємо, чи містить gunicorn
        if 'gunicorn' not in content:
            print("✗ Procfile має містити команду запуску gunicorn")
            return False
        
        print("✓ Файл Procfile коректний для Heroku")
        return True
    except Exception as e:
        print(f"✗ Помилка читання файлу Procfile: {e}")
        return False

def validate_runtime():
    """Перевіряє runtime.txt на відповідність вимогам Heroku"""
    if not os.path.exists('runtime.txt'):
        print("✗ Файл runtime.txt не знайдено, буде використана версія Python за замовчуванням")
        return True
    
    try:
        with open('runtime.txt', 'r') as f:
            content = f.read().strip()
        
        # Перевіряємо формат
        if not content.startswith('python-'):
            print("✗ runtime.txt має починатися з 'python-'")
            return False
        
        # Перевіряємо підтримувані версії Python
        version = content.split('-')[1]
        if not version.startswith(('3.9', '3.10', '3.11')):
            print(f"✗ Версія Python {version} може не підтримуватися на Heroku")
            return False
        
        print(f"✓ Файл runtime.txt коректний, вказана версія Python: {version}")
        return True
    except Exception as e:
        print(f"✗ Помилка читання файлу runtime.txt: {e}")
        return False

def validate_requirements():
    """Перевіряє requirements.txt на відповідність вимогам Heroku"""
    if not os.path.exists('requirements.txt'):
        print("✗ Файл requirements.txt не знайдено")
        return False
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.readlines()
        
        # Перевіряємо наявність flask і gunicorn
        required_packages = ['flask', 'gunicorn']
        found_packages = []
        
        for line in content:
            for package in required_packages:
                if package in line.lower():
                    found_packages.append(package)
        
        missing_packages = [p for p in required_packages if p not in found_packages]
        
        if missing_packages:
            print(f"✗ У файлі requirements.txt відсутні необхідні пакети: {', '.join(missing_packages)}")
            return False
        
        print("✓ Файл requirements.txt містить всі необхідні пакети")
        return True
    except Exception as e:
        print(f"✗ Помилка читання файлу requirements.txt: {e}")
        return False

def check_port_config():
    """Перевіряє, чи використовується змінна оточення PORT"""
    main_files = ['main.py', 'app.py', 'wsgi.py']
    port_configured = False
    
    for filename in main_files:
        if not os.path.exists(filename):
            continue
        
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            # Шукаємо використання змінної PORT
            if "os.environ.get('PORT'" in content or 'os.environ.get("PORT"' in content:
                print(f"✓ Файл {filename} використовує змінну оточення PORT")
                port_configured = True
                break
        except Exception as e:
            print(f"✗ Помилка читання файлу {filename}: {e}")
    
    if not port_configured:
        print("✗ Не знайдено використання змінної оточення PORT в жодному з основних файлів")
        print("  Heroku динамічно призначає порт через змінну оточення PORT")
        return False
    
    return True

def main():
    print("=== Тестування конфігурації для розгортання на Heroku ===")
    
    # Перевіряємо конфігураційні файли
    procfile_valid = validate_procfile()
    runtime_valid = validate_runtime()
    requirements_valid = validate_requirements()
    port_valid = check_port_config()
    
    all_valid = procfile_valid and runtime_valid and requirements_valid and port_valid
    
    if all_valid:
        print("\n✅ Всі перевірки пройдено успішно! Проект готовий до розгортання на Heroku.")
        print("Для розгортання використовуйте інструкції з файлу deploy_instructions.md")
    else:
        print("\n❌ Деякі перевірки не пройдено. Виправте проблеми перед розгортанням на Heroku.")
    
    return 0 if all_valid else 1

if __name__ == '__main__':
    sys.exit(main())