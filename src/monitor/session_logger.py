import os
import csv
from utils import now

class SessionLogger:
    def __init__(self):
        # Diretório base desta sessao
        self.session_dir = os.path.join("logs", f"session_{now().replace(':','-')}")
        os.makedirs(self.session_dir, exist_ok=True)

        # Arquivos exigidos pelo enunciado
        self.internet = os.path.join(self.session_dir, "camada_internet.csv")
        self.transport = os.path.join(self.session_dir, "camada_transporte.csv")
        self.app = os.path.join(self.session_dir, "camada_aplicacao.csv")

        # Arquivos auxiliares
        self.raw_file = os.path.join(self.session_dir, "raw_packets.bin")
        self.log_file = os.path.join(self.session_dir, "monitor.log")

        # Inicializa cabeçalhos
        self._init_headers()

    # ----------------------------------------------------------
    # Cabeçalhos CSV exigidos pelo trabalho
    # ----------------------------------------------------------
    def _init_headers(self):
        with open(self.internet, "w", newline="") as f:
            csv.writer(f).writerow([
                "timestamp",
                "protocolo",
                "src_ip",
                "dst_ip",
                "id_interno",
                "info_extra",
                "tamanho"
            ])

        with open(self.transport, "w", newline="") as f:
            csv.writer(f).writerow([
                "timestamp",
                "protocolo",
                "src_ip",
                "src_port",
                "dst_ip",
                "dst_port",
                "tamanho"
            ])

        with open(self.app, "w", newline="") as f:
            csv.writer(f).writerow([
                "timestamp",
                "protocolo",
                "info"
            ])

    # ----------------------------------------------------------
    # Logging geral (monitor.log)
    # ----------------------------------------------------------
    def log(self, text):
        print(text)
        with open(self.log_file, "a") as f:
            f.write(text + "\n")

    # ----------------------------------------------------------
    # Raw packets
    # ----------------------------------------------------------
    def save_raw(self, raw_bytes):
        with open(self.raw_file, "ab") as f:
            f.write(raw_bytes + b"\n")

    # ----------------------------------------------------------
    # Camada 3 — Internet
    # ----------------------------------------------------------
    def write_internet(self, row):
        with open(self.internet, "a", newline="") as f:
            csv.writer(f).writerow(row)

    # ----------------------------------------------------------
    # Camada 4 — Transporte
    # ----------------------------------------------------------
    def write_transport(self, row):
        with open(self.transport, "a", newline="") as f:
            csv.writer(f).writerow(row)

    # ----------------------------------------------------------
    # Camada 7 — Aplicacao
    # ----------------------------------------------------------
    def write_application(self, row):
        with open(self.app, "a", newline="") as f:
            csv.writer(f).writerow(row)
