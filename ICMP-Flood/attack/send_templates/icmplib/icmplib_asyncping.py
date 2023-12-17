import asyncio
from icmplib import async_ping

async def is_alive(address):
    host = await async_ping(address, count=1000, interval=0, payload_size=65500)
    return host

asyncio.run(is_alive(str(input('IP-адрес атакуемого хоста: '))))