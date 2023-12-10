import os
from scapy.all import sniff, IP, ICMP
from collections import defaultdict
import threading
import time
import socket

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def count_icmp_packets(packet):
    current_time = time.time()
    if IP in packet and ICMP in packet:
        ip_source = packet[IP].src
        if ip_source != local_ip:
            icmp_counter[ip_source]['total'] += 1
            icmp_counter[ip_source]['1_min'][current_time] += 1
            icmp_counter[ip_source]['5_min'][current_time] += 1
            icmp_counter[ip_source]['15_min'][current_time] += 1

def print_statistics():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("IP адрес\tПакетов (Всего)\t(1 минута)\t(5 минут)\t(15 минут)")
        for ip, counters in icmp_counter.items():
            total = counters['total']
            packets_1_min = count_packets_in_interval(counters['1_min'], 60)
            packets_5_min = count_packets_in_interval(counters['5_min'], 300)
            packets_15_min = count_packets_in_interval(counters['15_min'], 900)
            
            print(f"{ip}: \t{total}\t\t{packets_1_min}\t\t\t{packets_5_min}\t\t\t{packets_15_min}")
        time.sleep(1)

def count_packets_in_interval(interval_counter, interval_length):
    current_time = time.time()
    start_time = current_time - interval_length
    packets_in_interval = sum(count for timestamp, count in interval_counter.items() if timestamp >= start_time)
    return packets_in_interval

#Cловарь для подсчета ICMP пакетов от каждого IP
icmp_counter = defaultdict(lambda: {'total': 0, '1_min': defaultdict(int), '5_min': defaultdict(int), '15_min': defaultdict(int)})


local_ip = get_local_ip()

#Поток для вывода статистики
statistics_thread = threading.Thread(target=print_statistics)
statistics_thread.start()

sniff(prn=count_icmp_packets, store=0, filter="icmp")