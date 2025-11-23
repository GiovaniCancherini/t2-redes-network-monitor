from raw_sniffer import RawSniffer
from session_logger import SessionLogger
from utils import now
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <interface>")
        sys.exit(1)

    interface = sys.argv[1]
    sniffer = RawSniffer(interface)
    logger = SessionLogger()

    logger.log(f"[+] Monitorando interface {interface}")
    logger.log(f"[+] Pasta de sessão: {logger.session_dir}")

    try:
        while True:
            raw, pkt, counters = sniffer.capture_once()

            if raw:
                logger.save_raw(raw)

            if not pkt:
                continue

            ts = now()

            if pkt.layer == 3 and pkt.proto == "IPv4":
                logger.write_internet([ts, "IPv4", pkt.src, pkt.dst,
                                    pkt.inner_proto, pkt.extra, pkt.size])

            if pkt.layer == 4 and pkt.proto == "TCP":
                logger.write_transport([ts, "TCP", pkt.src_ip, pkt.src_port,
                                     pkt.dst_ip, pkt.dst_port, pkt.size])

            if pkt.layer == 4 and pkt.proto == "UDP":
                logger.write_transport([ts, "UDP", pkt.src_ip, pkt.src_port,
                                     pkt.dst_ip, pkt.dst_port, pkt.size])

            if pkt.proto == "ARP":
                logger.write_internet([ts, "ARP", pkt.src, pkt.dst, "", "", pkt.size])

            logger.log(f"IPv4:{counters['ipv4']} ICMP:{counters['icmp']} TCP:{counters['tcp']} UDP:{counters['udp']} ARP:{counters['arp']}")

    except KeyboardInterrupt:
        logger.log("[!] Encerrado pelo usuário.")

if __name__ == "__main__":
    main()
