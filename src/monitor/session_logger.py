import os
import csv
from datetime import datetime

class SessionLogger:
    def __init__(self):
        # Cria pasta da sessão
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_dir = os.path.join("logs", f"session_{ts}")
        os.makedirs(self.session_dir, exist_ok=True)

        # Caminhos dos arquivos exigidos pelo enunciado
        self.internet_csv   = os.path.join(self.session_dir, "camada_internet.csv")
        self.transp_csv     = os.path.join(self.session_dir, "camada_transporte.csv")
        self.aplic_csv      = os.path.join(self.session_dir, "camada_aplicacao.csv")
        self.monitor_log    = os.path.join(self.session_dir, "monitor.log")
        self.raw_file       = os.path.join(self.session_dir, "raw_packets.bin")

        # Criar cabeçalhos dos 3 arquivos
        self._init_csv_files()

    def _init_csv_files(self):
        with open(self.internet_csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "timestamp",
                "protocolo",
                "src_ip",
                "dst_ip",
                "id_interno",
                "info_extra",
                "tamanho"
            ])

        with open(self.transp_csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "timestamp",
                "protocolo",
                "src_ip",
                "src_port",
                "dst_ip",
                "dst_port",
                "tamanho"
            ])

        with open(self.aplic_csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "timestamp",
                "protocolo",
                "info"
            ])

    def log(self, text):
        print(text)
        with open(self.monitor_log, "a") as f:
            f.write(text + "\n")

    def save_raw(self, raw):
        with open(self.raw_file, "ab") as f:
            f.write(raw + b"\n")

    def write_internet(self, row):
        with open(self.internet_csv, "a", newline="") as f:
            csv.writer(f).writerow(row)

    def write_transport(self, row):
        with open(self.transp_csv, "a", newline="") as f:
            csv.writer(f).writerow(row)

    def write_application(self, row):
        with open(self.aplic_csv, "a", newline="") as f:
            csv.writer(f).writerow(row)
