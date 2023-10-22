import socket
from queue import Queue
from threading import Thread

MSG_DISCONNECT = "disconect"


class Server(Thread):
    def __init__(
        self, port: int = 40678, max_connection: int = 3, timeout: float = 0.2
    ) -> None:
        Thread.__init__(self)
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", port))
        self.socket.settimeout(timeout)
        self.max_connection = max_connection

        self.message_queue = Queue()
        self.clients = []

    def __del__(self) -> None:
        print("del server")
        for client in self.clients:
            client.send(MSG_DISCONNECT.encode())
            client.close()
        self.socket.close()

    def add_messages(self, message: str) -> None:
        self.message_queue.put(message)
        print(self.message_queue.qsize())
        print(not self.message_queue.empty())

    def run(self):
        self.continue_loop = True
        self.socket.listen(self.max_connection)
        while self.continue_loop:
            self.accept_client()
            self.receive_message()
            self.send_message()

    def accept_client(self) -> None:
        try:
            client, addr = self.socket.accept()
            self.clients.append(client)
            print("Got connection from", addr)
            client.send(b"Thank you for connecting")
        except socket.timeout:
            pass

    def receive_message(self) -> None:
        for client in self.clients:
            message = client.recv(1024).decode()

            if "disconect" == message:
                self.clients.remove(client)
                continue

            print(f"received message {message}")

    def send_message(self) -> None:
        while not self.message_queue.empty():
            message = self.message_queue.get()
            print(f"Send message: {message}")
            for client in self.clients:
                client.send(message.encode())
