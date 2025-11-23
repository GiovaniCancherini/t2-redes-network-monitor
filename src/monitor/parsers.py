import struct

class ParsedPacket:
    def __init__(self, layer, proto, src=None, dst=None,
                 src_port=None, dst_port=None, inner_proto=None,
                 extra=None, size=None):
        self.layer = layer
        self.proto = proto
        self.src = src
        self.dst = dst
        self.src_ip = src
        self.dst_ip = dst
        self.src_port = src_port
        self.dst_port = dst_port
        self.inner_proto = inner_proto
        self.extra = extra
        self.size = size

def parse_ethernet(data):
    if len(data) < 14:
        return None
    dst, src, proto = struct.unpack("!6s6sH", data[:14])
    return proto, data[14:]

def parse_ipv4(data):
    if len(data) < 20:
        return None

    version = data[0] >> 4
    ihl = (data[0] & 0x0F) * 4
    if version != 4:
        return None

    total_len = struct.unpack("!H", data[2:4])[0]
    proto = data[9]
    src = ".".join(map(str, data[12:16]))
    dst = ".".join(map(str, data[16:20]))

    return proto, src, dst, total_len, data[ihl:]

def parse_icmp(data):
    if len(data) < 4:
        return None
    return {"type": data[0], "code": data[1]}

def parse_tcp(data):
    if len(data) < 20:
        return None
    src_port, dst_port = struct.unpack("!HH", data[:4])
    return src_port, dst_port

def parse_udp(data):
    if len(data) < 8:
        return None
    src_port, dst_port = struct.unpack("!HH", data[:4])
    return src_port, dst_port
