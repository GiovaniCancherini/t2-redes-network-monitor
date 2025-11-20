import struct

def parse_ethernet(data):
    if len(data) < 14:
        return None
    
    # MAC Destino	6 bytes
    # MAC Origem	6 bytes
    # EtherType	    2 bytes
    # TOTAL         14 bytes
    dst, src, proto = struct.unpack("!6s6sH", data[:14])
    # !     -> network byte order (big endian)
    # 6s    -> 6 bytes (string/bytes)   = MAC destino
    # 6s    -> 6 bytes (string/bytes)   = MAC origem
    # H     -> unsigned short (2 bytes) = EtherType
    return {
        "proto": proto,
        "payload": data[14:]
    }

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

    return {
        "proto": proto,
        "src": src,
        "dst": dst,
        "length": total_len,
        "payload": data[ihl:]
    }

def parse_icmp(data):
    if len(data) < 4:
        return None
    icmp_type = data[0]
    icmp_code = data[1]
    return {"type": icmp_type, "code": icmp_code}

def parse_tcp(data):
    if len(data) < 20:
        return None
    src_port, dst_port = struct.unpack("!HH", data[:4])
    return {"src_port": src_port, "dst_port": dst_port}

def parse_udp(data):
    if len(data) < 8:
        return None
    src_port, dst_port = struct.unpack("!HH", data[:4])
    return {"src_port": src_port, "dst_port": dst_port}
