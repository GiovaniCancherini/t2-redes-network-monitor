# **RELATÓRIO T2 – Monitoramento de Rede via Socket RAW e Túnel Virtual**

## **Aluno:** Giovani da Silva Cancherini

## **Disciplina:** Laboratório de Redes de Computadores

## **PUCRS – Escola Politécnica**

## **Semestre:** 2025/2

---

# # **1. INTRODUÇÃO**

Este trabalho tem como objetivo implementar um sistema de **monitoramento de tráfego de rede** utilizando:

* Túnel virtual criado via **dispositivo TUN/TAP**
* Criação e envio de pacotes em nível de rede usando **raw sockets**
* Sniffer desenvolvido manualmente utilizando **AF_PACKET**
* Ambientes simulados com **3 máquinas distintas** (Monitor, Cliente 1, Cliente 2)

O enunciado prevê a criação de um ambiente onde um **Proxy/Monitor** captura pacotes enviados entre dois clientes, através de um túnel virtual e uma arquitetura semelhante a um enlace físico dedicado.

Foram realizados testes iniciais em ambiente **Windows + Docker**, mas dificuldades estruturais (ausência de AF_PACKET, tun/tap em WSL2, etc.) levaram à adoção de **máquinas Linux nativas**, como recomendado pela própria documentação da professora.

---

# # **2. FUNDAMENTAÇÃO TEÓRICA**

## ## 2.1 Túnel Virtual TUN/TAP

TUN/TAP é um driver do kernel que cria interfaces virtuais:

* **TUN** → opera na camada 3 (IP)
* **TAP** → opera na camada 2 (Ethernet)

O trabalho utiliza **TUN**, permitindo receber e enviar pacotes IP “crus” diretamente entre processos.

O dispositivo é alocado via:

```c
int tun_fd = open("/dev/net/tun", O_RDWR);
ioctl(tun_fd, TUNSETIFF, &ifr);
```

---

## ## 2.2 Raw Sockets

Raw sockets permitem ao programa:

* Ler pacotes exatamente como chegam na interface
* Sem intervenção do kernel
* Interpretar manualmente cabeçalhos Ethernet, IP, TCP, UDP e ICMP

No Linux, o sniffer utiliza:

```python
socket.socket(AF_PACKET, SOCK_RAW, socket.ntohs(ETH_P_ALL))
```

Mas **AF_PACKET não existe no Windows**, resultando em erro:

```
PermissionError: [Errno 1] Operation not permitted
```

Justificando a migração para ambiente Linux nativo.

---

## ## 2.3 Estrutura do sistema proposto no T2

O ambiente final contém 3 máquinas:

```
CLIENTE 1 → tun0 → Proxy/Monitor → tun0 → CLIENTE 2
```

Cada cliente envia tráfego real (ping, curl, dig).
O Monitor intercepta pacotes do TUN e alimenta o sniffer Python.

---

# # **3. ARQUITETURA IMPLEMENTADA**

A solução completa foi estruturada da seguinte forma:

```
t2-redes-network-monitor/
├── docs/                     # Material de apoio
├── docker/                   # Primeira tentativa (Docker) – não utilizada na versão final
├── logs/                     # Logs do monitor
├── scripts/                  # Scripts para Monitor / Cliente1 / Cliente2
│   ├── monitor-run.sh
│   ├── client1-run.sh
│   ├── client2-run.sh
├── src/
│   ├── monitor/
│   │   ├── raw_sniffer.py    # Sniffer AF_PACKET
│   │   ├── logger.py
│   │   ├── parsers.py
│   │   ├── utils.py
│   ├── traffic_tunnel/       # Código C do túnel virtual
│       ├── traffic_tunnel.c
│       ├── tunnel.c
│       ├── tunnel.h
│       ├── client1.sh
│       ├── client2.sh
│       ├── server.sh
│       └── Makefile
├── README.md
└── run_lab.sh                # Tentativa inicial (Docker) – descontinuado
```

---

# # **4. DESCRIÇÃO DO TÚNEL (C)**

O túnel é implementado pelos arquivos fornecidos pela professora:

* `tunnel.c`
* `traffic_tunnel.c`
* `tunnel.h`

## ## 4.1 Funcionamento

### No Proxy (servidor):

```bash
./traffic_tunnel enp0s3 -s
```

A lógica:

1. Aloca `tun0`
2. Abre socket raw na interface física
3. Realiza forwarding manual entre:

   * pacotes vindos do túnel → interface física
   * pacotes vindos da interface → túnel

### No Cliente:

```bash
./traffic_tunnel enp0s3 -c client1.sh
```

Cada cliente:

* Executa script client1.sh ou client2.sh
* Adiciona rotas de saída via túnel
* Encaminha TODO o tráfego IP pelo túnel

---

# # **5. SNIFFER EM PYTHON**

Implementado em:

```
src/monitor/raw_sniffer.py
```

Utiliza AF_PACKET:

```python
self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))
```

E captura pacotes com:

```python
raw, addr = self.sock.recvfrom(65535)
```

Os pacotes são parseados manualmente:

* Cabeçalho Ethernet
* Cabeçalho IPv4
* Cabeçalho TCP / UDP / ICMP

Gerando contadores:

```
IPv4: X
TCP: Y
UDP: Z
ICMP: W
ARP: K
```

---

# # **6. TENTATIVA INICIAL EM AMBIENTE WINDOWS (Docker)**

### Objetivo inicial:

Criar ambiente com Docker Compose contendo:

* monitor
* client1
* client2
* sniffer

### Principais problemas enfrentados:

1. **AF_PACKET não existe no Windows**
   → Raw sockets não funcionam

2. **/dev/net/tun não existe em contêineres Docker no Windows**
   → Túnel não pode ser criado

3. Captura com tcpdump via contêiner:
   → Somente pacotes internos do container, não do host

4. Arquitetura da professora exige:

   * Kernel real Linux
   * Túnel real
   * Interfaces de rede reais

### Conclusão:

 **Não é possível executar o T2 completamente no Windows via Docker.**

---

# # **7. SOLUÇÃO FINAL: AMBIENTE COM 3 MÁQUINAS LINUX**

Recomendado pela professora e agora adotado.

## ## 7.1 Setup realizado

Criação de 3 máquinas no VirtualBox:

* **Ubuntu-T2-Monitor**
* **Ubuntu-T2-Client1**
* **Ubuntu-T2-Client2**

### Configuração da rede no VirtualBox:

Adapter 1:

```
Bridged Adapter
Promiscuous Mode: Allow All
```

Adapter 2:

```
NAT (para apt update)
```

---

# # **8. PROCEDIMENTO DE EXECUÇÃO**

## ## 8.1 No Monitor

```bash
cd scripts/
sudo ./monitor-run.sh
```

### O script faz:

1. Atualização de pacotes
2. Compilação do túnel
3. Criação do tun0
4. Inicialização do servidor do túnel
5. Início do sniffer Python
6. Exibição de testes obrigatórios

**Local para print:**
📷 *Print 1 — monitor-run.sh em execução com tun0 UP*

---

## ## 8.2 No Cliente 1

```bash
cd scripts/
sudo ./client1-run.sh
```

### Testes obrigatórios:

```bash
ping 8.8.8.8
curl http://www.pucrs.br
dig www.pucrs.br
```

**Local para print:**
📷 *Print 2 — rotas do client1*
📷 *Print 3 — tun0 ativo*
📷 *Print 4 — saída do ping/curl/dig*

---

## ## 8.3 No Cliente 2

Idêntico ao Cliente 1:

```bash
sudo ./client2-run.sh
```

**Local para print:**
📷 *Print 5 — execução de testes no client2*

---

# # **9. RESULTADOS ESPERADOS**

No monitor, conforme os clientes enviam tráfego, o sniffer deve mostrar:

```
IPv4: 120
ICMP: 4
TCP: 80
UDP: 10
ARP: 3
```

**Local para print:**
📷 *Print 6 — saída do monitor com pacotes capturados*

---

# # **10. PRINCIPAIS PROBLEMAS E SOLUÇÕES**

| Problema                       | Causa                           | Solução                     |
| ------------------------------ | ------------------------------- | --------------------------- |
| `SIOCGIFINDEX: No such device` | Interface física não era `eth0` | Usar `enp0s3`               |
| `AF_PACKET PermissionError`    | Monitor não rodava como root    | Usar `sudo`                 |
| `tun0 DOWN`                    | túnel falhou                    | limpar tun0 e reinicializar |
| Docker não capturava AF_PACKET | Windows não suporta             | Migrar para Linux nativo    |

---

# # **11. CONCLUSÃO**

Após diversos testes e tentativas, concluiu-se que:

### ❌ A execução em Windows + Docker é inviável

porque:

* não há AF_PACKET
* não há /dev/net/tun
* não há suporte a forward de pacotes de kernel real
* não há roteamento real entre contêineres

### ✔ A solução final foi migrar para ambiente Linux real

como recomendado pelo enunciado.

Com 3 VMs Linux ou máquinas do laboratório, o túnel funciona corretamente, o monitor captura todos os pacotes e o trabalho pode ser demonstrado integralmente.

---

# # **12. REFERÊNCIAS**

* PDF do T2: *T2_20252.pdf*
* Kernel TUN/TAP documentation
* Python AF_PACKET documentation
* RFC 791 (IPv4), RFC 768 (UDP), RFC 793 (TCP), RFC 792 (ICMP)
