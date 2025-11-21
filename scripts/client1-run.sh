#!/bin/bash

echo ""
echo "==========================================="
echo "            T2 - CLIENTE 1                "
echo "==========================================="
sleep 1

echo "[1] Atualizando dependências..."
sudo apt update && sudo apt install -y iproute2 net-tools tcpdump make gcc curl dnsutils
echo ""

WORKDIR="$(pwd)"
TUN_DIR="$WORKDIR/traffic_tunnel"

echo "[2] Compilando túnel..."
cd "$TUN_DIR"
make clean >/dev/null 2>&1
make

echo ""
echo "[3] Subindo túnel CLIENTE 1..."
sudo ./traffic_tunnel eth0 -c client1.sh &
TUN_PID=$!

sleep 2

echo "[4] Verificando tun0..."
ip a show tun0

echo ""
echo "==========================================="
echo "           TESTES PARA EXECUTAR           "
echo "==========================================="
echo ""
echo "✔ Teste 1: ping através do túnel"
echo "   ping 8.8.8.8"
echo ""
echo "✔ Teste 2: acesso HTTP"
echo "   curl http://www.pucrs.br"
echo ""
echo "✔ Teste 3: DNS"
echo "   dig www.pucrs.br"
echo ""
echo "Monitor (proxy) deve mostrar tráfego."
echo ""
echo "Pressione ENTER quando terminar os testes."
read

echo ""
echo "[5] Encerrando túnel..."
sudo kill $TUN_PID

echo ""
echo "==========================================="
echo "               CLIENTE 1 OK                "
echo "==========================================="
