#!/bin/bash

echo "====================================="
echo "      T2 - MONITOR (SEM TÚNEL)"
echo "====================================="

echo "[1] Atualizando pacotes..."
apt update -y >/dev/null 2>&1

echo "[2] Rodando sniffer RAW na interface eth0..."
echo "    (AF_PACKET ativado)"

python3 /workspace/src/monitor/main.py eth0
