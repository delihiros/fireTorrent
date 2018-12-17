def encode(data, encoding='utf-8'):
    if isinstance(data, str):
        return bytes(str(len(data)), encoding) + b':' + bytes(data, encoding)
    elif isinstance(data, bytes):
        return bytes(str(len(data)), encoding) + b':' + data
    elif isinstance(data, int):
        return b'i' + bytes(str(data), encoding) + b'e'
    elif isinstance(data, dict):
        return b'd' + b''.join([encode(k) + encode(v)
                                for k, v in data.items()]) + b'e'
    elif isinstance(data, list):
        return b'l' + b''.join([encode(v) for v in data]) + b'e'


def decode(data, encoding='utf-8'):
    idx = 0

    def _is_bdigit(b):
        return b in [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9']

    def _decode_str(data):
        nonlocal idx
        length = b''
        while idx < len(data) and _is_bdigit(bytes([data[idx]])):
            length += bytes([data[idx]])
            idx += 1
        idx += 1
        length = int(length.decode(encoding))
        s = data[idx:idx + length]
        idx += length
        return s

    def _decode_int(data):
        nonlocal idx
        idx += 1
        i = b''
        while idx < len(data) and bytes([data[idx]]) != b'e':
            i += bytes([data[idx]])
            idx += 1
        idx += 1
        return i

    def _decode_dict(data):
        nonlocal idx
        d = {}
        idx += 1
        while idx < len(data) and bytes([data[idx]]) != b'e':
            key = _decode(data)
            value = _decode(data)
            d[key] = value
        idx += 1
        return d

    def _decode_list(data):
        nonlocal idx
        l = []
        idx += 1
        while idx < len(data) and bytes([data[idx]]) != b'e':
            l.append(_decode(data))
        idx += 1
        return l

    def _decode(data):
        nonlocal idx

        first = data[idx:idx + 1]

        if _is_bdigit(first):
            return _decode_str(data)
        elif first == b'i':
            return _decode_int(data)
        elif first == b'd':
            return _decode_dict(data)
        elif first == b'l':
            return _decode_list(data)

    return _decode(data)
