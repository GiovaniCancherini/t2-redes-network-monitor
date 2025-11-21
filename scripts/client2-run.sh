#!/bin/bash

echo ""
echo "==========================================="
echo "            T2 - CLIENTE 2                "
echo "==========================================="
echo ""

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TUN_DIR="$ROOT_DIR/traffic_tunnel"

echo "[1] Atualizando dependências..."
sudo apt update && sudo apt install -y iproute2 net-tools tcpdump make gcc curl dnsutils
echo ""

echo "[2] Compilando túnel..."
cd "$TUN_DIR"
make clean >/dev/null 2>&1
make

echo ""
echo "[3] Subindo túnel CLIENTE 2..."
sudo ./traffic_tunnel eth0 -c client2.sh &
TUN_PID=$!

sleep 2

echo "[4] Verificando tun0..."
ip a show tun0

echo ""
echo "==========================================="
echo "           TESTES PARA EXECUTAR           "
echo "==========================================="
echo ""
echo "✔ ping 8.8.8.8"
echo "✔ curl http://www.pucrs.br"
echo "✔ dig www.pucrs.br"
echo ""
echo "Monitor (proxy) deve captar os pacotes."
echo ""
echo "Pressione ENTER quando terminar os testes."
read

echo ""
echo "[5] Encerrando túnel..."
sudo kill $TUN_PID

echo ""
echo "==========================================="
echo "               CLIENTE 2 OK                "
echo "==========================================="
