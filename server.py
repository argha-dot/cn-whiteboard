import socket
import threading
import pickle
import os

clients = set()
client_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[NEW CONN] {addr} connected.")
    
    try:
        connected = True

        while connected:
            msg = pickle.loads(conn.recv(4096 * 8))

            if msg:
                if type(msg) == str:
                    # print(f"[ADDR {addr}] {msg}")
                    if msg == 'q':
                        print(f"[ADDR {addr}] {msg}")
                        conn.sendall(pickle.dumps(msg))
                else:
                    with client_lock:
                        for c in clients:
                            c.sendall(pickle.dumps(msg))

    finally:
        with client_lock:
            clients.remove(conn)

        conn.close()


def start(socket):
    while True:
        conn, addr = socket.accept()

        with client_lock:
            clients.add(conn)

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 9999

    try:
        s = socket.socket()
        s.bind((HOST, PORT))
        s.listen()
        print(f"SERVER IS LISTENING on {HOST}")

        start(s)

    except socket.error as err:
        print(err)



if __name__ == "__main__":
    main()