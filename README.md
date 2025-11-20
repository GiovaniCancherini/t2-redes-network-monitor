# Monitor de Tráfego (T2 - Laboratório de Redes)

Este projeto implementa:

- Um **proxy** com túnel de rede (`traffic_tunnel`) e
- Um **monitor de tráfego em Python**, que escuta a interface virtual `tun0`
- Dois **clientes** que enviam tráfego através desse túnel

Tudo orquestrado com **Docker Compose**.


---

## Estrutura do Projeto

```text
t2-redes-network-monitor/
├── docker-compose.yml
├── run_lab.sh
├── README.md
├── logs/
├── docs/
│   └── T2_20252.pdf
├── src/
│   └── monitor/
│       ├── main.py
│       ├── raw_sniffer.py
│       ├── parsers.py
│       ├── logger.py
│       └── utils.py
│   └── requirements.txt
├── traffic_tunnel/
│   ├── Makefile
│   ├── tunnel.c
│   ├── tunnel.h
│   ├── traffic_tunnel.c
│   ├── server.sh
│   ├── client1.sh
│   └── client2.sh
└── docker/
    ├── Dockerfile.proxy
    └── Dockerfile.client
```

* `src/monitor`     -> código Python do sniffer (raw socket, CSV etc.)
* `traffic_tunnel`  -> código C do túnel e scripts fornecidos
* `docker`          -> Dockerfiles para proxy e clientes
* `logs`            -> saída dos CSVs (camada de rede e transporte)
* `docs`            -> enunciado e materiais da disciplina


---

## Como subir o ambiente

Pré-requisitos:

* Docker Desktop (com WSL2)
* Git Bash ou WSL para rodar scripts `.sh`

Na raiz do projeto:

```bash
./run_lab.sh
```

Isso irá:

* Derrubar containers antigos `t2-redes-*` (se existirem)
* Buildar as imagens do proxy e clientes
* Subir os 3 containers na rede `t2-redes-monitor`


---

## Fluxo dentro dos containers

### 1. Proxy (t2-redes-proxy)

Abrir um terminal no proxy:

```bash
docker exec -it t2-redes-proxy bash
```

#### 1.1 Túnel em modo servidor

```bash
cd /workspace/traffic_tunnel
./traffic_tunnel eth0 -s
```

Deixe esse terminal rodando.

#### 1.2 Configuração de tun0 + NAT

Em outro terminal:

```bash
docker exec -it t2-redes-proxy bash
cd /workspace/traffic_tunnel
./server.sh
```

#### 1.3 Rodar o monitor Python em tun0

Em mais um terminal:

```bash
docker exec -it t2-redes-proxy bash
cd /workspace/monitor
python3 main.py tun0
```

Você verá os contadores (IPv4, TCP, UDP, ICMP, ARP) subindo.

Os logs serão gravados em:

```text
/workspace/monitor/logs/
```

que está mapeado no host em `./logs`.


---

### 2. Clientes

#### Cliente 1

```bash
docker exec -it t2-redes-client1 bash
cd /workspace/traffic_tunnel
./traffic_tunnel eth0 -c client1.sh
```

Depois:

```bash
ping 8.8.8.8
curl http://example.com
# Se instalar dnsutils:
apt update && apt install -y dnsutils
dig www.pucrs.br
```

#### Cliente 2

```bash
docker exec -it t2-redes-client2 bash
cd /workspace/traffic_tunnel
./traffic_tunnel eth0 -c client2.sh
```

Pode repetir testes semelhantes.

Todo esse tráfego passa por:

* `tun0` do cliente -> túnel -> `tun0` do proxy -> NAT -> Internet

E é exatamente nessa `tun0` do proxy que o monitor está escutando.


---

## Logs gerados

* `logs/camada_internet.csv`
  Contém informações de IPv4/ICMP etc.

* `logs/camada_transporte.csv`
  Contém IP origem/destino e porta TCP/UDP.


---

## Extensões possíveis

* Adicionar parser para DNS, HTTP, DHCP, NTP na camada de aplicação
* Melhorar interface do monitor (ex: usar rich para tabelas)
* Adicionar métricas por intervalo de tempo (pps, bps etc.)
* Salvar metadados dos fluxos (5-tuple: src IP, dst IP, src port, dst port, protocolo)


---

## Fluxo:

```
1. git bash here e chmod +x run_lab.sh
2. `./run_lab.sh`  
3. sobe proxy + client1 + client2  
4. inicia túnel no proxy (`traffic_tunnel eth0 -s`)  
5. roda `server.sh`  
6. inicia monitor (`python3 main.py tun0`)  
7. inicia túnel nos clientes (`traffic_tunnel eth0 -c clientX.sh`)  
8. gera tráfego -> monitor captura -> logs caem em `logs/`.
```
