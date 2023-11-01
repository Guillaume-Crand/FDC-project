import selectors
import socket
import traceback

import const
from message import MessageClient, MessageServer


class NetworkServer:
    def __init__(self) -> None:
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((const.host, const.port))
        self.sock.listen()
        print(f"Listening on {(const.host, const.port)}")
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)

    def __del__(self):
        self.sel.close()

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        message = MessageServer(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)

    def treat_network_event(self):
        events = self.sel.select(timeout=1)
        for key, mask in events:
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


class NetworkClient:
    def __init__(self) -> None:
        self.sel = selectors.DefaultSelector()

        action, value = "search", "morpheus"
        request = self.create_request(action, value)
        self.start_connection(const.host, const.port, request)

    def __del__(self):
        self.sel.close()

    def create_request(self, action, value):
        if action == "search":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action + value, encoding="utf-8"),
            )

    def start_connection(self, host, port, request):
        addr = (host, port)
        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = MessageClient(self.sel, sock, addr, request)
        # message = libclient.Message(sel, sock, addr, request)
        self.sel.register(sock, events, data=message)

    def treat_network_event(self):
        events = self.sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print(
                    f"Main: Error: Exception for {message.addr}:\n"
                    f"{traceback.format_exc()}"
                )
                message.close()

        # Check for a socket being monitored to continue.
        return self.sel.get_map()
