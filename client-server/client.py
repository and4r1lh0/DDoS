﻿import socket
import psutil
import os

def main():
    while(1):
        client_id = os.getenv("COMPUTERNAME")
        processor_load = psutil.cpu_percent()
        message = f"{client_id} {processor_load}"

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("localhost", 8000))
            client_socket.send(message.encode())
            data = client_socket.recv(1024).decode()
            print(data)
        except ConnectionRefusedError:
            print(f"РЎРµСЂРІРµСЂ РЅРµ РґРѕСЃС‚СѓРїРµРЅ.")


if __name__ == "__main__":
    main()
