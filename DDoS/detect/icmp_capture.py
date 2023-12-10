import os
from scapy.all import sniff, ICMP, show_interfaces
show_interfaces()

def detect_icmp_flood(packet):
    if ICMP in packet:
        for p in packet:
            a = p.show(dump=True)
            print (a,end='',flush=False)
            
            #os.system('cls')
            exit(0)

sniff(iface=None, filter='icmp', prn=detect_icmp_flood)