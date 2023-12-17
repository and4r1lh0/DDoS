import socket
import threading
import time
import psutil

clients = []  # Define the clients list
interval = 1  # Define the polling interval


def handle_client(client_socket):
    """Обработчик для подключения клиента."""

    # Получаем идентификатор компьютера
    client_id = client_socket.recv(1024).decode()

    # Получаем текущую нагрузку на процессор
    processor_load = psutil.cpu_percent()

    # Отправляем информацию клиенту
    client_socket.send(f"{client_id} {processor_load}".encode())

    # Заносим информацию о клиенте в список
    clients.append((client_id, processor_load))


def main():
    """Основная функция сервера."""

    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Связываем сокет с локальным портом
    server_socket.bind(("localhost", 8000))

    # Слушаем подключения
    server_socket.listen(5)

    while True:
        # Принимаем подключение
        client_socket, _ = server_socket.accept()

        # Создаем поток для обработки подключения
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

        # Опрашиваем клиентов
        for client_id, processor_load in clients:
            print(f"{client_id} {processor_load}")

        # Ждем интервал
        time.sleep(interval)


if __name__ == "__main__":
    main()
