"""
Прямий сокетний сервер для миттєвого запуску в Replit
Відкриває порт відразу без додаткових бібліотек
"""

import socket
import threading
import os
import time
import subprocess
import sys

# Порт сервера
PORT = int(os.environ.get('PORT', 5000))

# HTML відповідь
HTML_RESPONSE = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Connection: close

<!DOCTYPE html>
<html>
<head>
    <title>Luxortum</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
            background-color: #1a0a2a;
            color: white;
        }
        h1 {
            color: #ffbb00;
        }
        .loader {
            border: 16px solid #333;
            border-top: 16px solid #8a2be2;
            border-radius: 50%;
            width: 80px;
            height: 80px;
            animation: spin 2s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .info {
            max-width: 600px;
            margin: 0 auto;
            background-color: rgba(74, 42, 138, 0.6);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
    </style>
    <script>
        // Перезавантаження сторінки кожні 5 секунд
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    </script>
</head>
<body>
    <h1>Luxortum - Платформа божественної симуляції</h1>
    <div class="info">
        <h2>Запуск сервера...</h2>
        <div class="loader"></div>
        <p>Порт 5000 відкрито. Система ініціалізується.</p>
        <p><small>Сторінка автоматично оновиться через 5 секунд</small></p>
    </div>
</body>
</html>
"""

def simple_socket_server():
    """Простий сокетний сервер, який одразу відкриває порт"""
    server = None
    try:
        # Створюємо сокет
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', PORT))
        server.listen(5)
        print(f"[+] Сервер запущено на порту {PORT}")
        
        # Безкінечний цикл обробки запитів
        while True:
            client, addr = server.accept()
            print(f"[+] Підключення від {addr}")
            
            # Читаємо дані (ігноруємо)
            client.recv(1024)
            
            # Відправляємо HTML відповідь
            client.send(HTML_RESPONSE.encode())
            client.close()
            
    except Exception as e:
        print(f"[-] Помилка сервера: {e}")
    finally:
        if server:
            server.close()

def launch_main_server():
    """Запуск основного сервера через деякий час"""
    time.sleep(3)  # Зачекаємо, щоб сокетний сервер встиг відкрити порт
    try:
        print("[+] Запуск основного Flask сервера...")
        
        # Запускаємо Flask сервер в окремому процесі
        # Важливо: ми не запускаємо через import, щоб уникнути блокування
        cmd = ["python3", "-c", "import subprocess; subprocess.run(['gunicorn', '--bind', '0.0.0.0:5001', 'fastest:app'])"]
        subprocess.Popen(cmd)
        
    except Exception as e:
        print(f"[-] Помилка запуску основного сервера: {e}")

if __name__ == "__main__":
    print("[+] Запуск прямого сокетного сервера...")
    
    # Запускаємо основний сервер у окремому потоці
    main_server_thread = threading.Thread(target=launch_main_server)
    main_server_thread.daemon = True
    main_server_thread.start()
    
    # Запускаємо сокетний сервер у основному потоці
    simple_socket_server()