import socket
from parsers import (
    ParsedPacket, parse_ethernet, parse_ipv4,
    parse_icmp, parse_tcp, parse_udp
)

ETH_P_ALL = 0x0003

class RawSniffer:
    def __init__(self, interface):
        self.iface = interface
        self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))
        self.sock.bind((interface, 0))

        self.counters = {
            "ipv4": 0,
            "tcp": 0,
            "udp": 0,
            "icmp": 0,
            "arp": 0
        }

    def capture_once(self):
        raw, addr = self.sock.recvfrom(65535)

        eth_proto, payload = parse_ethernet(raw)

        # ARP
        if eth_proto == 0x0806:
            self.counters["arp"] += 1
            return raw, ParsedPacket(layer=3, proto="ARP", size=len(raw)), self.counters

        # IPv4
        if eth_proto == 0x0800:
            self.counters["ipv4"] += 1
            ip = parse_ipv4(payload)
            if not ip:
                return raw, None, self.counters

            proto, src, dst, total_len, ip_payload = ip
            pkt = None

            if proto == 1:
                self.counters["icmp"] += 1
                icmp = parse_icmp(ip_payload)
                pkt = ParsedPacket(3, "IPv4", src, dst, inner_proto="ICMP",
                                   extra=str(icmp), size=total_len)

            elif proto == 6:
                self.counters["tcp"] += 1
                sp, dp = parse_tcp(ip_payload)
                pkt = ParsedPacket(4, "TCP", src, dst, sp, dp, size=total_len)

            elif proto == 17:
                self.counters["udp"] += 1
                sp, dp = parse_udp(ip_payload)
                pkt = ParsedPacket(4, "UDP", src, dst, sp, dp, size=total_len)

            else:
                pkt = ParsedPacket(3, "IPv4", src, dst, inner_proto=proto, size=total_len)

            return raw, pkt, self.counters

        return raw, None, self.counters
