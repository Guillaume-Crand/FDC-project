import selectors
import socket
import traceback

import const
from message import MessageClient, MessageServer


class NetworkBase:
    def __init__(self) -> None:
        self.sel = selectors.DefaultSelector()
        self.addr = (const.host, const.port)
        self.timeout = const.timeout
        self._start_connection()

    def __del__(self):
        self.sel.close()

    def process_received_messages(self):
        events = self.sel.select(timeout=self.timeout)
        for key, mask in events:
            self.process_message(key, mask)

        # Check for a socket being monitored to continue.
        return self.sel.get_map()

    def _start_connection(self):
        raise NotImplementedError(f"_start_connection")

    def send_message(self):
        raise NotImplementedError(f"send_message")

    def process_message(self):
        raise NotImplementedError(f"process_message")


class NetworkServer(NetworkBase):
    def __init__(self) -> None:
        super().__init__()

    def _start_connection(self):
        print(f"Starting connection Server to {self.addr}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((const.host, const.port))
        self.sock.listen()
        print(f"Listening on {(const.host, const.port)}")
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)

    def process_message(self, key, mask):
        if key.data is None:
            self.accept_wrapper(key.fileobj)
        else:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print(
                    f"Main: Error: Exception for {message.addr}:\n"
                    f"{traceback.format_exc()}"
                )
                message.close()

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        message = MessageServer(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)


class NetworkClient(NetworkBase):
    def __init__(self) -> None:
        super().__init__()

    def _start_connection(self):
        print(f"Starting connection Client to {self.addr}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex(self.addr)
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE

    def send_message(self, request):
        message = MessageClient(self.sel, self.sock, self.addr, request)
        self.sel.register(self.sock, self.events, data=message)

    def process_message(self, key, mask):
        message = key.data
        try:
            message.process_events(mask)
        except Exception:
            print(
                f"Main: Error: Exception for {message.addr}:\n"
                f"{traceback.format_exc()}"
            )
            message.close()
