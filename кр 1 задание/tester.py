import asyncio
import aiohttp
import time
import os
import psutil

async def run_test(port, count):
    url = f'http://127.0.0.1:{port}/'
    process = psutil.Process()
    mem_start = process.memory_info().rss / 1024 / 1024

    async with aiohttp.ClientSession() as session:
        tasks = []
        start = time.time()
        for i in range(1, count + 1):
            tasks.append(session.get(f"{url}?page={i}"))
        await asyncio.gather(*tasks)
        end = time.time()

    mem_end = process.memory_info().rss / 1024 / 1024
    return end - start, mem_end - mem_start

async def main():
    count = 10

    t1, m1 = await run_test(8000, count)
    s1 = os.path.getsize('sync_products.txt') if os.path.exists('sync_products.txt') else 0
    print(f"sync: time={t1:.2f}s mem={m1:.2f}MB file={s1} bytes")

    t2, m2 = await run_test(8080, count)
    s2 = os.path.getsize('async_products.txt') if os.path.exists('async_products.txt') else 0
    print(f"async: time={t2:.2f}s mem={m2:.2f}MB file={s2} bytes")

if __name__ == '__main__':
    asyncio.run(main())
