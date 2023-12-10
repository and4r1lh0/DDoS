import argparse
import socket
import struct
import sys
import time
import logging

def create_icmp_packet():
    # Заголовок ICMP Echo Request (тип 8, код 0, контрольная сумма 0, идентификатор, номер последовательности)
    icmp_header = struct.pack("!BBHHH", 8, 0, 0, 1, 1)

    # Данные (просто набор байт для примера)
    data = b'ABCDEFGHIJKLMNOPQRSTUVWX'

    # Контрольная сумма для заголовка и данных
    checksum = calculate_checksum(icmp_header + data)

    # Перезаписываем контрольную сумму в заголовке
    icmp_header = struct.pack("!BBHHH", 8, 0, socket.htons(checksum), 1, 1)

    # Возвращаем готовый ICMP пакет
    return icmp_header + data

def calculate_checksum(data):
    checksum = 0
    count_to = (len(data) // 2) * 2

    for count in range(0, count_to, 2):
        this_val = data[count + 1] * 256 + data[count]
        checksum += this_val
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

def send_icmp_request(target_ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except socket.error as e:
        logging.error(f"Error creating socket: {e}")
        sys.exit(1)

    packet = create_icmp_packet()

    try:
        sock.sendto(packet, (target_ip, 0))
    except socket.error as e:
        logging.error(f"Error sending ICMP packet: {e}")
        sys.exit(1)

    logging.info(f"ICMP request sent to {target_ip}")

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='ICMP Echo Request Generator')
    #parser.add_argument('target_ip', type=str, help='Target IP address')

    #args = parser.parse_args()
    target_ip='192.168.1.1'
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    while True:
        send_icmp_request(target_ip)
