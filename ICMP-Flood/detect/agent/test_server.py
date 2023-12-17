# -*- coding: cp1251 -*-
import socket
import threading
import time

HOST = '0.0.0.0'  # Bind to all interfaces
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

client_connections = []

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            print(f"Received message from client: {data.decode('utf-8')}")

            for connection in client_connections:
                if connection != client_socket:
                    connection.send(data)

        except ConnectionResetError:
            print(f"Client disconnected: {client_socket}")
            client_connections.remove(client_socket)
            break

while True:
    client_socket, client_address = server.accept()
    print(f"Connected with client: {client_address}")

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

    client_connections.append(client_socket)