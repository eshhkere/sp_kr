import socket
import threading
import requests

def handle(conn):
    try:
        req = conn.recv(1024).decode(errors='ignore')
        page = '1'
        if 'page=' in req:
            page = req.split('page=')[1].split()[0]

        url = f'https://dental-first.ru/catalog/?PAGEN_1={page}'
        r = requests.get(url)
        text = r.text

        lines = text.splitlines()
        lines = lines[:20]

        with open('sync_products.txt', 'a', encoding='utf-8') as f:
            for line in lines:
                line = line.strip()
                if line:
                    f.write(line + '\n')

        conn.sendall(b'HTTP/1.1 200 OK\r\n\r\nOK')
    except:
        pass
    finally:
        conn.close()

sock = socket.socket()
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, _ = sock.accept()
    threading.Thread(target=handle, args=(conn,)).start()
