# -*- coding: cp1251 -*-
import os
from scapy.all import sniff, IP, ICMP
from collections import defaultdict
import threading
import time
import socket
import json

def send_data(data):
    host = "192.168.1.35"
    port = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            json_data = json.dumps(data)
            sock.sendall(json_data.encode("utf-8"))
            sock.settimeout(1)  # Set a timeout for receiving data
            response = sock.recv(1024)
            # Handle the response if needed
        except Exception as e:
            print(f"Error in send_data: {e}")

def count_icmp_packets(packet, local_ip, icmp_counter, flooding):
    if IP in packet and ICMP in packet:
        ip_source = packet[IP].src
        if ip_source != local_ip:
            icmp_counter[ip_source] += 1
            if flooding and icmp_counter[ip_source] > 200:
                print(f"Flood ended for {ip_source}")
                flooding[0] = False  # Set the flooding flag to False

def print_statistics(local_ip, icmp_counter, time_counter, flooding):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Local IP: ', local_ip)
        print("IP адрес\tПакетов")
        for ip, count in icmp_counter.items():
            print(f"{ip}: \t{count}")

        current_time = time.time()
        recent_10s = sum(count for timestamp, count in time_counter.items() if current_time - timestamp <= 10)
        recent_1m = sum(count for timestamp, count in time_counter.items() if current_time - timestamp <= 60)
        recent_5m = sum(count for timestamp, count in time_counter.items() if current_time - timestamp <= 300)

        if (recent_10s > 50 or recent_1m > 100 or recent_5m > 200) and not flooding[0]:
            attacker_ip = max(icmp_counter, key=icmp_counter.get)
            print(f"ICMP flood detected! Attacker ip address {attacker_ip}")
            data = {
                "client_id": os.getenv("COMPUTERNAME"),
                "local_ip": local_ip,
                "attacker_ip": attacker_ip,
            }
            send_data(data)
            flooding[0] = True  # Set the flooding flag to True

        time.sleep(1)

icmp_counter = defaultdict(int)
time_counter = defaultdict(int)
flooding = [False]  # Flag to indicate whether flooding is ongoing
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
local_ip = sock.getsockname()[0]
# Uncomment the line below to get local IP using gethostbyname
# local_ip = socket.gethostbyname(socket.gethostname())

statistics_thread = threading.Thread(target=print_statistics, args=(local_ip, icmp_counter, time_counter, flooding))
statistics_thread.start()

def update_time_counter(icmp_counter, time_counter):
    while True:
        time.sleep(1)
        current_time = time.time()
        for ip, count in icmp_counter.items():
            time_counter[current_time] += count

update_time_thread = threading.Thread(target=update_time_counter, args=(icmp_counter, time_counter))
update_time_thread.start()

sniff(prn=lambda pkt: count_icmp_packets(pkt, local_ip, icmp_counter, flooding), store=0)