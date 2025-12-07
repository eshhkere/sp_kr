import asyncio
import time
import psutil
import subprocess
import random
import os

TEST_REQUESTS = 200


async def tcp_client(port, filename):
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', port)
        writer.write(filename.encode())
        await writer.drain()
        data = await reader.read(100)
        writer.close()
        await writer.wait_closed()
        return data
    except:
        return None


def get_memory_usage(pid):
    try:
        process = psutil.Process(pid)
        return process.memory_info().rss / 1024 / 1024
    except:
        return 0


async def run_benchmark(server_script, port, name):
    print(f"\n--- Тестирование {name} ---")

    process = subprocess.Popen(["python", server_script])
    pid = process.pid

    await asyncio.sleep(2)

    mem_idle = get_memory_usage(pid)
    print(f"Память в простое: {mem_idle:.2f} MB")

    tasks = []
    for i in range(TEST_REQUESTS):
        fname = f"file_{random.randint(0, 99)}.txt"
        tasks.append(tcp_client(port, fname))

    start_time = time.time()

    mem_peak = mem_idle

    async def monitor_mem():
        nonlocal mem_peak
        for _ in range(10):
            current = get_memory_usage(pid)
            if current > mem_peak: mem_peak = current
            await asyncio.sleep(0.05)

    monitor_task = asyncio.create_task(monitor_mem())
    await asyncio.gather(*tasks)

    end_time = time.time()
    await monitor_task

    process.terminate()

    total_time = end_time - start_time
    mem_consumed = mem_peak - mem_idle

    mem_per_req = mem_consumed / TEST_REQUESTS
    mem_for_1000 = mem_idle + (mem_per_req * 1000)

    print(f"Время выполнения ({TEST_REQUESTS} requests): {total_time:.4f} сек")
    print(f"Потребление памяти : {mem_consumed:.4f} MB")
    print(f"Память на 1 запрос: {mem_per_req:.6f} MB")
    print(f"ПРОГНОЗ: Для 1000 одновременных запросов нужно минимум: {mem_for_1000:.2f} MB")


async def main():
    await run_benchmark("threaded_server.py", 9000, "Threaded Server (Многопоточный)")
    await run_benchmark("async_server.py", 9001, "Async Server (Асинхронный)")


if __name__ == "__main__":
    asyncio.run(main())
