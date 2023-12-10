import ping3

def send_ping(destination, size,n):
    for i in range(1,n):
        response_time = ping3.ping(destination, size=size)


destination = '192.168.1.1'
size = 1472  # указываем размер в байтах MTU

send_ping(destination, size,800000)