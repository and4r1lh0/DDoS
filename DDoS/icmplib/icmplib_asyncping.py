import asyncio
from icmplib import async_ping

async def is_alive(address):
    host = await async_ping('192.168.1.1', count=1000, interval=0,payload_size=65507)
    return host

asyncio.run(is_alive('192.168.1.1'))