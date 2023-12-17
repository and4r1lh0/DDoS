# -*- coding: cp1251 -*-
from icmplib import ping

def is_alive(address):
    host = ping(address, count=1000, interval=0, payload_size=65500)
    return host

is_alive(str(input('IP-адрес атакуемого хоста: ')))