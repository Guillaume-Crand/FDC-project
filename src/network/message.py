import io
import json
import pickle
import selectors
import struct
import sys

from message_utils import unwrap_json_bytes_into_obj

request_search = {
    "morpheus": "Follow the white rabbit. \U0001f430",
    "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
    "\U0001f436": "\U0001f43e Playing ball! \U0001f3d0",
}


class MessageBase:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(io.BytesIO(json_bytes), encoding=encoding, newline="")
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(self, *, content_bytes, content_type, content_encoding):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def read(self):
        self._read()

        self._recv_buffer, is_received = unwrap_json_bytes_into_obj(self._recv_buffer)
        if is_received:
            return self.process_message_received(is_received)
        return None

    # def process_events(self, mask):
    #     if mask & selectors.EVENT_READ:
    #         return self.read()
    #     if mask & selectors.EVENT_WRITE:
    #         return self.write()

    def close(self):
        print(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(f"Error: selector.unregister() exception for " f"{self.addr}: {e!r}")

        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_message_received(self, obj):
        print(obj)
        # raise NotImplementedError(f"process_message_received")


class MessageServer(MessageBase):
    def __init__(self, selector, sock, addr):
        super().__init__(selector, sock, addr)
        self.request = None
        self.response_created = False

    def _write(self):
        if self._send_buffer:
            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def process_message_received(self, obj):
        # content_len = self.jsonheader["content-length"]
        # if not len(self._recv_buffer) >= content_len:
        #     return
        # data = self._recv_buffer[:content_len]
        # self._recv_buffer = self._recv_buffer[content_len:]
        # if self.jsonheader["content-type"] == "text/json":
        #     encoding = self.jsonheader["content-encoding"]

        #     self.request = self._json_decode(data, encoding)
        #     print(f"Received request {self.request!r} from {self.addr}")
        # else:
        #     # Binary or unknown content-type
        #     self.request = data
        #     print(
        #         f"Received {self.jsonheader['content-type']} "
        #         f"request from {self.addr}"
        #     )
        self.request = obj
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

        return self.request

    def create_response(self):
        # if self.jsonheader["content-type"] == "text/json":
        #     response = self._create_response_json_content()
        # else:
        #     # Binary or unknown content-type
        #     response = self._create_response_binary_content()
        response = self._create_response_json_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message

    def _create_response_json_content(self):
        action = self.request.get("action")
        if action == "search":
            query = self.request.get("value")
            answer = request_search.get(query) or f"No match for '{query}'."
            content = {"result": answer}
        else:
            content = {"result": f"Error: invalid action '{action}'."}
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: " + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response


class MessageClient(MessageBase):
    def __init__(self, selector, sock, addr, request):
        super().__init__(selector, sock, addr)
        self.request = request
        self._request_queued = False

    def _write(self):
        if self._send_buffer:
            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

        if self._request_queued:
            if not self._send_buffer:
                # Set selector to listen for read events, we're done writing.
                self._set_selector_events_mask("r")

    def queue_request(self):
        content = self.request["content"]
        content_type = self.request["type"]
        content_encoding = self.request["encoding"]
        if content_type == "text/json":
            req = {
                "content_bytes": self._json_encode(content, content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        else:
            req = {
                "content_bytes": content,
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        message = self._create_message(**req)
        self._send_buffer += message
        self._request_queued = True

    def process_message_received(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]

        if self.jsonheader["content-type"] != "text/json":
            raise ValueError(
                f"Binary or unknown content-type : {self.jsonheader['content-type']}"
            )

        else:
            encoding = self.jsonheader["content-encoding"]
            message = self._json_decode(data, encoding)

            print(f"Received response {message!r} from {self.addr}")
            content = message
            result = content.get("result")
            print(f"Got result: {result}")
        self.close()

        return message
