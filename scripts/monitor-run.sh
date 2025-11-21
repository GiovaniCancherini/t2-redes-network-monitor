#!/bin/bash

echo ""
echo "==========================================="
echo "       T2 - MÁQUINA MONITOR / PROXY        "
echo "==========================================="
echo ""

# Diretório raiz do projeto
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TUN_DIR="$ROOT_DIR/traffic_tunnel"
MON_DIR="$ROOT_DIR/src"

echo "[1] Atualizando dependências..."
sudo apt update && sudo apt install -y iproute2 net-tools tcpdump python3 python3-pip make gcc
echo ""

echo "[2] Compilando o túnel..."
cd "$TUN_DIR"
make clean >/dev/null 2>&1
make
echo ""

echo "[3] Subindo o servidor do túnel..."
sudo ./traffic_tunnel eth0 -s &
TUNNEL_PID=$!
sleep 2

echo "[4] Verificando tun0..."
ip a show tun0

echo ""
echo "[5] Executando monitor Python no tun0..."
cd "$MON_DIR"
python3 main.py tun0 &
MON_PID=$!

echo ""
echo "==========================================="
echo "           TESTES A EXECUTAR AGORA         "
echo "==========================================="
echo ""
echo "→ Vá para o CLIENTE 1 e rode: ping 8.8.8.8"
echo "→ Vá para o CLIENTE 1 e rode: curl http://www.pucrs.br"
echo "→ Vá para o CLIENTE 1 e rode: dig www.pucrs.br"
echo ""
echo "→ Faça o mesmo no CLIENTE 2"
echo ""
echo "O MONITOR deve captar pacotes ICMP, TCP, UDP."
echo ""

echo "==========================================="
echo "      Pressione ENTER quando terminar      "
echo "==========================================="
read

echo ""
echo "[6] Encerrando monitor e túnel..."
kill $MON_PID
sudo kill $TUNNEL_PID

echo ""
echo "[7] Logs gerados em:"
echo "$ROOT_DIR/logs"
ls -lh "$ROOT_DIR/logs"

echo ""
echo "==========================================="
echo "              FINALIZADO                   "
echo "==========================================="
