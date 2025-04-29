"""
Симуляція розгортання проекту Luxortum на Render.com
Перевіряє, чи проект правильно сконфігуровано відповідно до вимог Render
"""
import os
import sys
import json
import yaml
import subprocess
from urllib.parse import urlparse

def validate_render_yaml():
    """Перевіряє файл render.yaml на відповідність вимогам"""
    if not os.path.exists('render.yaml'):
        print("✗ Файл render.yaml не знайдено")
        return False
    
    try:
        with open('render.yaml', 'r') as f:
            config = yaml.safe_load(f)
            
        # Перевіряємо основні поля
        if 'services' not in config:
            print("✗ У файлі render.yaml відсутній розділ 'services'")
            return False
        
        services = config['services']
        if not services or not isinstance(services, list):
            print("✗ Розділ 'services' має бути непорожнім списком")
            return False
        
        web_service = next((s for s in services if s.get('type') == 'web'), None)
        if not web_service:
            print("✗ Не знайдено сервіс з типом 'web'")
            return False
        
        # Перевіряємо необхідні поля для веб-сервісу
        required_fields = ['name', 'env', 'buildCommand', 'startCommand']
        missing_fields = [f for f in required_fields if f not in web_service]
        
        if missing_fields:
            print(f"✗ Відсутні обов'язкові поля: {', '.join(missing_fields)}")
            return False
        
        print("✓ Файл render.yaml коректний і містить всі необхідні поля")
        return True
    except Exception as e:
        print(f"✗ Помилка читання файлу render.yaml: {e}")
        return False

def validate_procfile():
    """Перевіряє Procfile на відповідність вимогам"""
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
        
        print("✓ Файл Procfile коректний")
        return True
    except Exception as e:
        print(f"✗ Помилка читання файлу Procfile: {e}")
        return False

def simulate_build():
    """Симулює процес збірки на Render"""
    print("\n=== Симуляція процесу збірки на Render ===")
    
    # Перевіряємо команду збірки з render.yaml
    try:
        with open('render.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        services = config['services']
        web_service = next((s for s in services if s.get('type') == 'web'), None)
        build_command = web_service.get('buildCommand', '')
        
        if not build_command:
            print("✗ Команда збірки не вказана в render.yaml")
            return False
        
        # Перевіряємо наявність команди та умови для її виконання
        if 'pip install' in build_command:
            print(f"✓ Команда збірки: {build_command}")
            
            # Перевіряємо наявність файлу requirements.txt
            if not os.path.exists('requirements.txt'):
                print("✗ Файл requirements.txt відсутній, але він потрібен для команди збірки")
                return False
            
            print("✓ Файл requirements.txt присутній")
            return True
        else:
            print(f"✗ Команда збірки не містить 'pip install': {build_command}")
            return False
    except Exception as e:
        print(f"✗ Помилка симуляції збірки: {e}")
        return False

def simulate_startup():
    """Симулює процес запуску на Render"""
    print("\n=== Симуляція процесу запуску на Render ===")
    
    # Перевіряємо команду запуску з render.yaml
    try:
        with open('render.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        services = config['services']
        web_service = next((s for s in services if s.get('type') == 'web'), None)
        start_command = web_service.get('startCommand', '')
        
        if not start_command:
            print("✗ Команда запуску не вказана в render.yaml")
            return False
        
        # Перевіряємо наявність gunicorn в команді запуску
        if 'gunicorn' in start_command:
            print(f"✓ Команда запуску використовує gunicorn: {start_command}")
            
            # Перевіряємо вказаний додаток
            parts = start_command.split()
            app_part = next((p for p in parts if ':app' in p), None)
            
            if not app_part:
                print("✗ Не вказано додаток у форматі 'module:app'")
                return False
            
            module_name = app_part.split(':')[0]
            
            if not os.path.exists(f"{module_name}.py"):
                print(f"✗ Файл {module_name}.py не знайдено")
                return False
            
            print(f"✓ Файл {module_name}.py присутній")
            return True
        else:
            print(f"✗ Команда запуску не використовує gunicorn: {start_command}")
            return False
    except Exception as e:
        print(f"✗ Помилка симуляції запуску: {e}")
        return False

def main():
    print("=== Тестування конфігурації для розгортання на Render ===")
    
    # Перевіряємо конфігураційні файли
    render_yaml_valid = validate_render_yaml()
    procfile_valid = validate_procfile()
    
    if not (render_yaml_valid and procfile_valid):
        print("\n❌ Конфігураційні файли містять помилки")
        return 1
    
    # Симулюємо процеси збірки та запуску
    build_valid = simulate_build()
    startup_valid = simulate_startup()
    
    if not (build_valid and startup_valid):
        print("\n❌ Симуляція збірки або запуску виявила проблеми")
        return 1
    
    print("\n✅ Всі перевірки пройдено успішно! Проект готовий до розгортання на Render.")
    print("Для розгортання використовуйте інструкції з файлу deploy_instructions.md")
    
    return 0

if __name__ == '__main__':
    try:
        import yaml
    except ImportError:
        print("Для запуску тесту потрібна бібліотека PyYAML.")
        print("Вона буде додана до пакету для розгортання, але не вимагається на сервері.")
        sys.exit(1)
    
    sys.exit(main())