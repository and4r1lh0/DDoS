# import asyncio
# from icmplib import async_ping

# async def is_alive(address):
#     host = await async_ping('192.168.1.1', count=1000, interval=0,payload_size=65507)
#     return host

# asyncio.run(is_alive('192.168.1.1'))





# from icmplib import ping

# def is_alive(address):
#     host = ping('192.168.1.1', count=1000, interval=0,payload_size=65507)
#     return host

# is_alive('192.168.1.1')

import ping3

def send_ping(destination, size,n):
    for i in range(1,n):
        response_time = ping3.ping(destination, size=size)


destination = '192.168.1.70'
size = 1472  # указываем размер в байтах MTU

send_ping(destination, size,800000)


# def main():
#     ip_destination = '192.168.1.10'
#     ip_source = '192.168.1.35'
#     sent_buff_size = 65500
#     num_threads = 187

#     threads = []
#     for i in range(num_threads):
#         thread = threading.Thread(target=send_ping, args=(ip_destination,sent_buff_size,8000))
#         threads.append(thread)
#         thread.start()
#     print('Running')
#     for thread in threads:
#         thread.join()

# if __name__ == '__main__':
#     main()