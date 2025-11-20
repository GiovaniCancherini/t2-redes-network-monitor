import sys
import time
from raw_sniffer import RawSniffer

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <interface>")
        sys.exit(1)

    interface = sys.argv[1]
    sniffer = RawSniffer(interface)

    print(f"[+] Capturando pacotes na interface {interface}...")
    print("[Ctrl+C para sair]\n")

    try:
        while True:
            sniffer.capture_once()
            counters = sniffer.counters

            print(
                f"\rIPv4:{counters['IPv4']}  "
                f"TCP:{counters['TCP']}  "
                f"UDP:{counters['UDP']}  "
                f"ICMP:{counters['ICMP']}  "
                f"ARP:{counters['ARP']}",
                end=""
            )

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nEncerrando captura...")

if __name__ == "__main__":
    main()
