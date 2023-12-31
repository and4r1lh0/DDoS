﻿import socket
import threading
import time

interval = 1  # Define the polling interval
    
def handle_client(client_socket):
    client_id = client_socket.recv(1024).decode()
    client_socket.send(client_id.encode())
    print(client_id)
   

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.1.35", 8000))
    server_socket.listen(5)
    print('[INFO] Server listening on port 8000')

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

        time.sleep(interval)

if __name__ == "__main__":
    main()