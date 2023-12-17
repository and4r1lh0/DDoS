# -*- coding: cp1251 -*-
import os
from scapy.all import sniff, IP, ICMP
from collections import defaultdict
import threading
import time
#from socket import gethostbyname, gethostname
import socket

def count_icmp_packets(packet):
    global local_ip
    if IP in packet and ICMP in packet:
        ip_source = packet[IP].src
        if ip_source != local_ip:  # Исключаем IP-адрес хоста из подсчета
            icmp_counter[ip_source] += 1

def print_statistics():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Local IP: ',local_ip)
        print("IP адрес\tПакетов")
        for ip, count in icmp_counter.items():
            print(f"{ip}: \t{count}")
        
        # Сравнение с предыдущими значениями за разные временные интервалы
        current_time = time.time()
        recent_10s = sum(count for timestamp, count in time_counter.items() if current_time - timestamp <= 10)
        recent_1m = sum(count for timestamp, count in time_counter.items() if current_time - timestamp <= 60)
        recent_5m = sum(count for timestamp, count in time_counter.items() if current_time - timestamp <= 300)

        # Проверка на ICMP-флуд и вывод соответствующего сообщения
        if recent_10s > 50 or recent_1m > 100 or recent_5m > 200:
            attacker_ip = max(icmp_counter, key=icmp_counter.get)
            print(f"ICMP flood detected! Attacker ip address {attacker_ip}")

        time.sleep(1)

icmp_counter = defaultdict(int)
time_counter = defaultdict(int)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
local_ip=sock.getsockname()
local_ip=(local_ip[0])
#local_ip = gethostbyname(gethostname())

statistics_thread = threading.Thread(target=print_statistics)
statistics_thread.start()

def update_time_counter():
    while True:
        time.sleep(1)
        current_time = time.time()
        for ip, count in icmp_counter.items():
            time_counter[current_time] += count

update_time_thread = threading.Thread(target=update_time_counter)
update_time_thread.start()

sniff(prn=count_icmp_packets, store=0)
