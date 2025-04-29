"""
Локальне тестування перед розгортанням
Перевіряє, чи всі необхідні файли і залежності присутні
"""
import os
import sys
import importlib
import subprocess

def check_file(filename):
    """Перевіряє наявність файлу і виводить результат"""
    exists = os.path.exists(filename)
    print(f"Файл {filename}: {'✓ існує' if exists else '✗ відсутній'}")
    return exists

def check_module(module_name):
    """Перевіряє, чи можна імпортувати модуль"""
    try:
        importlib.import_module(module_name)
        print(f"Модуль {module_name}: ✓ доступний")
        return True
    except ImportError:
        print(f"Модуль {module_name}: ✗ не знайдено")
        return False

def check_port(port):
    """Перевіряє, чи порт вільний"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    if result == 0:
        print(f"Порт {port}: ✗ зайнятий")
        free = False
    else:
        print(f"Порт {port}: ✓ вільний")
        free = True
    sock.close()
    return free

def main():
    print("=== Перевірка файлів ===")
    files = [
        'main.py', 
        'app.py', 
        'wsgi.py', 
        'Procfile', 
        'render.yaml'
    ]
    
    all_files_exist = all(check_file(f) for f in files)
    
    print("\n=== Перевірка статичних файлів ===")
    static_dir = os.path.join(os.getcwd(), 'static')
    if os.path.isdir(static_dir):
        print(f"Директорія static: ✓ існує")
        # Перевіряємо кілька критичних файлів
        static_files = [
            os.path.join('static', 'index.html'),
            os.path.join('static', 'js', 'tooltip.js'),
            os.path.join('static', 'js', 'world-mood.js'),
            os.path.join('static', 'css', 'style.css')
        ]
        all_static_files_exist = all(check_file(f) for f in static_files)
    else:
        print(f"Директорія static: ✗ відсутня")
        all_static_files_exist = False
    
    print("\n=== Перевірка залежностей ===")
    required_modules = ['flask', 'gunicorn']
    optional_modules = ['openai', 'requests']
    
    all_required_modules = all(check_module(m) for m in required_modules)
    for m in optional_modules:
        check_module(m)
    
    print("\n=== Перевірка мережі ===")
    ports_to_check = [5000, 8080]
    all_ports_free = all(check_port(p) for p in ports_to_check)
    
    # Загальний результат
    print("\n=== Підсумок ===")
    if all_files_exist and all_static_files_exist and all_required_modules and all_ports_free:
        print("✅ Всі перевірки пройдено успішно! Проект готовий до розгортання.")
    else:
        print("❌ Деякі перевірки не пройдено. Виправте проблеми перед розгортанням.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())