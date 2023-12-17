# -*- coding: cp1251 -*-
import socket
import threading
import time
import psutil

clients = []  
interval = 1

def handle_client(client_socket):

    client_id = client_socket.recv(1024).decode() # ID ПК
    processor_load = psutil.cpu_percent() # нагрузка на CPU
    client_socket.send(f"{client_id} {processor_load}".encode())
    clients.append((client_id, processor_load))


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8000))
    server_socket.listen(5)

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
        for client_id, processor_load in clients:
            print(f"{client_id} {processor_load}")
        time.sleep(interval)

if __name__ == "__main__":
    main()