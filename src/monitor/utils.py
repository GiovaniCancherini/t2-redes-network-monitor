import sys
from datetime import datetime

def now():
    return datetime.now().isoformat()

def timestamped_filename(prefix, ext):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{ts}.{ext}"

def print_status(counters):
    status = (
        f"IPv4:{counters['ipv4']}  "
        f"ICMP:{counters['icmp']}  "
        f"TCP:{counters['tcp']}  "
        f"UDP:{counters['udp']}  "
        f"ARP:{counters['arp']}"
    )
    sys.stdout.write("\r" + status)
    sys.stdout.flush()
