from raw_sniffer import RawSniffer
from logger import SessionLogger
from datetime import datetime
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <interface>")
        sys.exit(1)

    interface = sys.argv[1]
    logger = SessionLogger()
    sniffer = RawSniffer(interface)

    logger.log(f"[+] Monitorando interface {interface}...")
    logger.log(f"[+] Sessão criada em: {logger.session_dir}")
    
    try:
        while True:
            raw, parsed, counters = sniffer.capture_once(return_all=True)

            logger.save_raw(raw)

            ts = datetime.now().isoformat()

            # INTERNET (camada 3)
            if parsed.layer == 3:
                logger.write_internet([
                    ts, parsed.proto, parsed.src, parsed.dst,
                    parsed.inner_proto, parsed.extra, parsed.size
                ])

            # TRANSPORTE (camada 4)
            if parsed.layer == 4:
                logger.write_transport([
                    ts, parsed.proto, parsed.src_ip, parsed.src_port,
                    parsed.dst_ip, parsed.dst_port, parsed.size
                ])

            # APLICACAO (camada 7)
            if parsed.layer == 7:
                logger.write_application([
                    ts, parsed.proto, parsed.info
                ])

            logger.log(
                f"IPv4:{counters['ipv4']} IPv6:{counters['ipv6']} "
                f"ICMP:{counters['icmp']} TCP:{counters['tcp']} UDP:{counters['udp']}"
            )

    except KeyboardInterrupt:
        logger.log("[!] Encerrado pelo usuário.")
        logger.log(f"Logs salvos em: {logger.session_dir}")

if __name__ == "__main__":
    main()
