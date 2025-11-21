#!/bin/bash
set -e

# Resolve caminho absoluto do dir raiz do projeto
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[+] Subindo ambiente T2 (build + containers)..."
docker compose -f "$ROOT_DIR/docker-compose.yml" down -v || true
docker compose -f "$ROOT_DIR/docker-compose.yml" up -d --build

echo
echo "[+] Containers em execução:"
docker ps --filter "name=t2-redes-"

cat <<EOF

========================================
COMANDOS ÚTEIS
========================================

# Entrar no proxy (servidor do túnel + monitor)
docker exec -it t2-redes-proxy bash

# Entrar nos clientes
docker exec -it t2-redes-client1 bash
docker exec -it t2-redes-client2 bash

----------------------------------------
PASSO A PASSO DENTRO DO PROXY (t2-redes-proxy)
----------------------------------------

1) Ativar o túnel em modo servidor:

    cd /workspace/traffic_tunnel
    ./traffic_tunnel eth0 -s

   (deixe esse comando rodando em primeiro terminal)

2) Em OUTRO terminal do proxy, configurar tun0 e NAT:

    docker exec -it t2-redes-proxy bash
    cd /workspace/traffic_tunnel
    ./server.sh

3) Em OUTRO terminal ainda do proxy, rodar o monitor:

    docker exec -it t2-redes-proxy bash
    cd /workspace/monitor
    python3 main.py tun0

----------------------------------------
PASSO A PASSO DENTRO DOS CLIENTES
----------------------------------------

CLIENTE 1:

    docker exec -it t2-redes-client1 bash
    cd /workspace/traffic_tunnel
    ./traffic_tunnel eth0 -c client1.sh

    # Depois que tun0 estiver ativo:
    ping 8.8.8.8
    curl http://example.com
    dig www.pucrs.br   # se instalar dnsutils

CLIENTE 2:

    docker exec -it t2-redes-client2 bash
    cd /workspace/traffic_tunnel
    ./traffic_tunnel eth0 -c client2.sh

    # Testes semelhantes:
    ping 8.8.8.8
    curl http://example.com

----------------------------------------
LOGS DO MONITOR
----------------------------------------

No host (Windows), os CSVs ficam em:

    ./logs/camada_internet.csv
    ./logs/camada_transporte.csv

EOF
