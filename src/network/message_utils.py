import io
import json
import struct
import sys

ENCODING = "utf-8"


# Encoding to bytes
def encode_byte(obj, encoding=ENCODING):
    return json.dumps(obj, ensure_ascii=False).encode(encoding)


def decode_byte(obj_bytes, encoding=ENCODING):
    tiow = io.TextIOWrapper(io.BytesIO(obj_bytes), encoding=encoding, newline="")
    obj = json.load(tiow)
    tiow.close()
    return obj


# wrapping into json
def wrap_obj_into_json_bytes(content_obj, content_type="text/json", encoding=ENCODING):
    content_bytes = encode_byte(content_obj, encoding)
    jsonheader = {
        "byteorder": sys.byteorder,
        "content-type": content_type,
        "content-encoding": encoding,
        "content-length": len(content_bytes),
    }
    jsonheader_bytes = encode_byte(jsonheader, encoding)
    message_hdr = struct.pack(">H", len(jsonheader_bytes))
    return message_hdr + jsonheader_bytes + content_bytes


def unwrap_json_bytes_into_obj(_recv_buffer):
    hdrlen = 2
    if len(_recv_buffer) >= hdrlen:
        _jsonheader_len = struct.unpack(">H", _recv_buffer[:hdrlen])[0]
        if (len(_recv_buffer) - hdrlen) >= _jsonheader_len:
            jsonheader = decode_byte(
                _recv_buffer[hdrlen : _jsonheader_len + hdrlen], "utf-8"
            )
            content_len = jsonheader["content-length"]
            if (len(_recv_buffer) - hdrlen - _jsonheader_len) >= content_len:
                # OK
                for reqhdr in (
                    "byteorder",
                    "content-length",
                    "content-type",
                    "content-encoding",
                ):
                    if reqhdr not in jsonheader:
                        raise ValueError(f"Missing required header '{reqhdr}'.")
                if jsonheader["content-type"] != "text/json":
                    raise ValueError(f"Wrong content type {jsonheader['content-type']}")
                if jsonheader["content-encoding"] != ENCODING:
                    raise ValueError(f"Wrong encoding {jsonheader['content-encoding']}")

                data = _recv_buffer[
                    _jsonheader_len + hdrlen : _jsonheader_len + hdrlen + content_len
                ]

                return _recv_buffer[
                    hdrlen + _jsonheader_len + content_len :
                ], decode_byte(data, ENCODING)
                # self._set_selector_events_mask("w")
    return _recv_buffer, False
