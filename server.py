import socket
import threading
import os

clients = set()
client_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[NEW CONN] {addr} connected.")
    
    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode("utf-8")
            if msg:
                if msg.lower() == "q":
                    print(f"[ADDR {addr}] disconnected")
                    connected = False
                    break

                print(f"[ADDR {addr}] {msg}")
                with client_lock:
                    for c in clients:
                        c.sendall(f"[{addr}] {msg}".encode("utf-8"))
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