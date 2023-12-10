from icmplib import ping

def is_alive(address):
    host = ping('192.168.1.1', count=1000, interval=0,payload_size=65507)
    return host

is_alive('192.168.1.1')