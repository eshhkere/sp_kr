import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 9000
DIR = "test_files"


def count_lines(filepath):
    try:
        with open(filepath, 'rb') as f:
            return f.read().count(b'\n')
    except FileNotFoundError:
        return -1


def handle_client(conn):
    try:
        filename = conn.recv(1024).decode().strip()
        filepath = os.path.join(DIR, filename)

        count = count_lines(filepath)

        conn.sendall(str(count).encode())
    except:
        pass
    finally:
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1000)
    print(f"[Threaded] Запущен на {PORT}")

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn,))
        t.start()


if __name__ == "__main__":
    start_server()
