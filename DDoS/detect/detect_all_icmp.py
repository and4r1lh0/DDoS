import os
from scapy.all import sniff, IP, ICMP
from collections import defaultdict
import threading
import time

def count_icmp_packets(packet):
    if IP in packet and ICMP in packet:
        ip_source = packet[IP].src
        icmp_counter[ip_source] += 1

def print_statistics():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("IP адрес\t Пакетов")
        for ip, count in icmp_counter.items():
            print(f"{ip}: \t{count}")
        time.sleep(1)

icmp_counter = defaultdict(int)

statistics_thread = threading.Thread(target=print_statistics)
statistics_thread.start()

sniff(prn=count_icmp_packets, store=0, filter="icmp")