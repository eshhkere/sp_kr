import asyncio
import aiofiles
import os

HOST = '127.0.0.1'
PORT = 9001
DIR = "test_files"

async def count_lines_async(filepath):
    try:
        async with aiofiles.open(filepath, 'rb') as f:
            content = await f.read()
            return content.count(b'\n')
    except FileNotFoundError:
        return -1

async def handle_client(reader, writer):
    try:
        data = await reader.read(100)
        if not data: return
        filename = data.decode().strip()
        filepath = os.path.join(DIR, filename)

        count = await count_lines_async(filepath)

        writer.write(str(count).encode())
        await writer.drain()
    except Exception:
        pass
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except:
            pass

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[Async] Запущен на {PORT}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
