import csv
import os

os.makedirs("logs", exist_ok=True)

def log_internet(ts, proto, src, dst, extra, size):
    with open("logs/camada_internet.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([ts, proto, src, dst, extra, size])

def log_transport(ts, proto, src, sport, dst, dport):
    with open("logs/camada_transporte.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([ts, proto, src, sport, dst, dport])
