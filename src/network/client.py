import socket
from queue import Queue
from threading import Thread

MSG_DISCONNECT = "disconect"


class Client(Thread):
    def __init__(self, port=40682) -> None:
        Thread.__init__(self)
        self.socket = socket.socket()
        self.socket.connect(("127.0.0.1", port))

        self.message_queue = Queue()

    def add_messages(self, message: str) -> None:
        self.message_queue.put(message)

    def run(self):
        self.continue_loop = True
        while self.continue_loop:
            self.receive_message()
            self.send_message()

    def receive_message(self) -> None:
        message = self.socket.recv(1024).decode()

        if message == MSG_DISCONNECT:
            self.continue_loop = False
            return

        print(message)

    def send_message(self) -> None:
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.socket.send(message.encode())
            print(f"message sent : {message}")
