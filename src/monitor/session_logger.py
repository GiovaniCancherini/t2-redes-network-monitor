import os
import csv
from utils import now

class SessionLogger:
    def __init__(self):
        self.session_dir = os.path.join("logs", f"session_{now().replace(':','-')}")
        os.makedirs(self.session_dir, exist_ok=True)

        self.internet = os.path.join(self.session_dir, "camada_internet.csv")
        self.transport = os.path.join(self.session_dir, "camada_transporte.csv")
        self.app = os.path.join(self.session_dir, "camada_aplicacao.csv")
        self.raw_file = os.path.join(self.session_dir, "raw_packets.bin")
        self.log_file = os.path.join(self.session_dir, "monitor.log")

        self._init_headers()

    def _init_headers(self):
        with open(self.internet, "w") as f:
            csv.writer(f).writerow(
                ["timestamp","protocolo","src_ip","dst_ip","id_interno","info_extra","tamanho"]
            )

        with open(self.transport, "w") as f:
            csv.writer(f).writerow(
                ["timestamp","protocolo","src_ip","src_port","dst_ip","dst_port","tamanho"]
            )

        with open(self.app, "w") as f:
            csv.writer(f).writerow(
                ["timestamp","protocolo","info"]
            )
