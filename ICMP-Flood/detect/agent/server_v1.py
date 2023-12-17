import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        print(data.decode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.1.35', 8000))
    server.listen(5)
    print('[INFO] Server listening on port 8000')

    while True:
        client_socket, addr = server.accept()
        print(f'[INFO] Accepted connection from {addr[0]}:{addr[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

start_server()
