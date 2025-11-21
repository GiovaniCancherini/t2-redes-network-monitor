#!/bin/bash
set -e

echo "[+] Detectando interface da máquina real..."

# Detecta interface física automaticamente
IFACE=$(ip -o link show | awk -F': ' \
   '$2!="lo" && $2 !~ /^veth/ && $2 !~ /^docker/ && $2 !~ /^br-/ {print $2; exit}')

echo "[+] Interface detectada: $IFACE"

echo "[+] Removendo rede antiga, se existir..."
docker network rm t2net-macvlan 2>/dev/null || true

echo "[+] Criando rede macvlan..."

docker network create -d macvlan \
  --subnet=172.20.0.0/16 \
  --gateway=172.20.0.1 \
  -o parent=$IFACE \
  t2net-macvlan

echo "[+] Rede criada com sucesso!"
docker network inspect t2net-macvlan
