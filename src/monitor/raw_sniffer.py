import socket
from parsers import parse_ethernet, parse_ipv4, parse_icmp, parse_tcp, parse_udp
from logger import log_internet, log_transport
from utils import now

ETH_P_ALL = 0x0003  # captura tudo

class RawSniffer:
    def __init__(self, interface):
        self.iface = interface
        # AF_PACKET para criar a partir da camada de enlace (acessar endereços MAC, dhcp, arp, etc)
        self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))
        self.sock.bind((interface, 0))
        self.counters = {
            "IPv4": 0,
            "TCP": 0,
            "UDP": 0,
            "ICMP": 0,
            "ARP": 0
        }

    def capture_once(self):
        raw, addr = self.sock.recvfrom(65535) # maior tamanho possivel de um pacote Ethernet -> 65535 bytes = 1 pacote IP maximo

        eth = parse_ethernet(raw)
        if not eth:
            return

        if eth["proto"] == 0x0806:
            self.counters["ARP"] += 1
            return

        if eth["proto"] == 0x0800:
            self.counters["IPv4"] += 1
            ip = parse_ipv4(eth["payload"])
            if not ip:
                return

            log_internet(now(), "IPv4", ip["src"], ip["dst"], "", ip["length"])

            if ip["proto"] == 1:
                self.counters["ICMP"] += 1
                parse_icmp(ip["payload"])
                return

            if ip["proto"] == 6:
                self.counters["TCP"] += 1
                tcp = parse_tcp(ip["payload"])
                log_transport(now(), "TCP", ip["src"], tcp["src_port"], ip["dst"], tcp["dst_port"])
                return

            if ip["proto"] == 17:
                self.counters["UDP"] += 1
                udp = parse_udp(ip["payload"])
                log_transport(now(), "UDP", ip["src"], udp["src_port"], ip["dst"], udp["dst_port"])
                return
