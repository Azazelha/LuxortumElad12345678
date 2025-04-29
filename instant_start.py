"""
Luxortum Instant Server
Призначено для миттєвого запуску у Replit
Негайно відкриває порт, а потім запускає повноцінний сервер
"""

import os
import socket
import threading
import time
import subprocess
import sys
import logging

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("luxortum_instant")

# Порт, на якому слухатиме сервер
PORT = int(os.environ.get('PORT', 5000))

# HTML-відповідь, яку будемо надсилати при підключенні
HTML_RESPONSE = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Connection: close

<!DOCTYPE html>
<html>
<head>
    <title>Luxortum</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        .loader { 
            border: 16px solid #f3f3f3; 
            border-top: 16px solid #8a2be2; 
            border-radius: 50%;
            width: 80px;
            height: 80px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    <script>
        // Автоматичне перезавантаження сторінки через 5 секунд
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    </script>
</head>
<body>
    <h1>Luxortum Server</h1>
    <p>Сервер запускається...</p>
    <div class="loader"></div>
    <p><small>Сторінка автоматично перезавантажиться за 5 секунд</small></p>
</body>
</html>
"""

def socket_server():
    """Запуск простого socket-сервера для миттєвого відкриття порту"""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', PORT))
        server_socket.listen(5)
        
        logger.info(f"Попередній сервер запущено на порту {PORT}")
        
        # Обслуговуємо до 100 запитів або до 60 секунд
        start_time = time.time()
        requests_handled = 0
        
        while requests_handled < 100 and time.time() - start_time < 60:
            try:
                # Приймаємо з'єднання з таймаутом 1 секунда
                server_socket.settimeout(1)
                client_socket, addr = server_socket.accept()
                
                # Читаємо запит (необов'язково, але для повноти)
                client_socket.recv(1024)
                
                # Відправляємо відповідь
                client_socket.sendall(HTML_RESPONSE.encode('utf-8'))
                client_socket.close()
                
                requests_handled += 1
            except socket.timeout:
                pass
            except Exception as e:
                logger.error(f"Помилка обробки запиту: {e}")
                pass
                
            # Перевіряємо, чи запущено основний сервер
            if os.path.exists('.server_ready'):
                logger.info("Основний сервер готовий, закриваємо попередній сервер")
                break
        
        logger.info(f"Попередній сервер обробив {requests_handled} запитів")
        server_socket.close()
    except Exception as e:
        logger.error(f"Помилка запуску попереднього сервера: {e}")

def start_main_server():
    """Запуск основного Flask-сервера через gunicorn"""
    try:
        logger.info("Запуск основного сервера...")
        time.sleep(2)  # Маленька затримка для запобігання конфліктів портів
        
        # Команда для запуску основного сервера
        cmd = ["gunicorn", "--bind", f"0.0.0.0:{PORT}", "fastest:app"]
        
        # Запускаємо процес
        process = subprocess.Popen(cmd)
        
        # Створюємо файл-прапорець для сигналізації про готовність
        with open('.server_ready', 'w') as f:
            f.write('1')
        
        # Чекаємо завершення процесу
        process.wait()
    except Exception as e:
        logger.error(f"Помилка запуску основного сервера: {e}")
    finally:
        # Видаляємо файл-прапорець, якщо він існує
        if os.path.exists('.server_ready'):
            os.remove('.server_ready')

if __name__ == "__main__":
    # Видаляємо файл-прапорець, якщо він існує з попереднього запуску
    if os.path.exists('.server_ready'):
        os.remove('.server_ready')
    
    logger.info("Запуск процесу миттєвого запуску...")
    
    # Запускаємо socket-сервер у окремому потоці
    socket_thread = threading.Thread(target=socket_server)
    socket_thread.daemon = True
    socket_thread.start()
    
    # Запускаємо основний сервер
    main_server_thread = threading.Thread(target=start_main_server)
    main_server_thread.daemon = True
    main_server_thread.start()
    
    # Чекаємо завершення обох потоків
    try:
        while socket_thread.is_alive() or main_server_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Отримано сигнал переривання, завершення роботи...")
        sys.exit(0)