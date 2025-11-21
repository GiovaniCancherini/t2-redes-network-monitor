#!/bin/bash
set -e

# Resolve caminho absoluto do dir raiz do projeto
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[+] Subindo ambiente T2 (modo SEM TÚNEL)..."
docker compose -f "$ROOT_DIR/docker-compose-nodetunel.yml" down -v || true
docker compose -f "$ROOT_DIR/docker-compose-nodetunel.yml" up -d --build

echo
echo "[+] Containers ativos:"
docker ps --filter name=t2-

cat <<EOF


========================================
COMO EXECUTAR (SEM TÚNEL)
========================================

# Monitor:
docker exec -it t2-monitor-nodetunel bash

# Cliente 1:
docker exec -it t2-client1-nodetunel bash

# Cliente 2:
docker exec -it t2-client2-nodetunel bash

----------------------------------------
TESTES OBRIGATÓRIOS
----------------------------------------

Cliente 1:
  ping 8.8.8.8
  curl http://www.pucrs.br
  dig www.pucrs.br

Cliente 2:
  ping 1.1.1.1
  curl http://example.com

Monitor:
  Sniffer mostrará ICMP, TCP, UDP, ARP em tempo real.

----------------------------------------
LOGS:
----------------------------------------
Gerados em: ./logs/

EOF
