import socket
import sys
import pickle


class Client_Network:
    def __init__(self) -> None:
        self.client = socket.socket()
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 9999
        self.addr = (self.host, self.port)
        # self.board

    def connect(self):
        self.client.connect(self.addr)

    def disconnect(self):
        self.client.close()

    def send(self, data, pick: bool = False):
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
        except socket.error as err:
            print(err)
