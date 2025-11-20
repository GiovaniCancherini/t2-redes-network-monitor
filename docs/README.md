# Network Monitor (Raw Socket)

Monitor de tráfego em tempo real utilizando raw sockets em Python, conforme especificação do Trabalho Final (T2) da disciplina de Laboratório de Redes.

Este projeto implementa um analisador de pacotes nível Ethernet, IP, TCP/UDP e ICMP, gerando contadores em tempo real e logs CSV por camada (sem utilizar bibliotecas de alto nível como Scapy).

---

# 🧩 **1. Objetivo do Projeto**

O monitor deve:

* Capturar pacotes diretamente de uma interface de rede (ex.: `eth0`, `tun0`) via **raw sockets**;
* Identificar protocolos das camadas **2, 3 e 4** da pilha TCP/IP;
* Registrar pacotes em arquivos CSV organizados por camada:

  * `camada_internet.csv`
  * `camada_transporte.csv`
  * `camada_aplicacao.csv` *(opcional na versão mínima)*
* Mostrar, no terminal, contadores em tempo real por protocolo;
* **Não** usar Scapy ou bibliotecas equivalentes (somente socket + struct).

---

# 🧱 **2. Arquitetura da Solução**

O projeto está organizado de forma modular para facilitar manutenção, leitura e evolução para versões mais completas.

```
monitor/
├── main.py               # Loop principal, leitura da interface, dashboard de contadores
├── raw_sniffer.py        # Classe RawSniffer: captura e encaminha pacotes para parsers
├── parsers.py            # Funções simples para parsear Ethernet, IPv4, TCP, UDP, ICMP
├── logger.py             # Escrita dos logs CSV em ./logs/
├── utils.py              # Funções utilitárias (timestamp etc.)
└── logs/                 # Criado automaticamente para armazenar os CSVs
```

### 🏗️ **Fluxo de execução interno**

1. `main.py` cria um objeto `RawSniffer` e inicia o loop.
2. `RawSniffer` abre um socket RAW:

   ```python
   socket(AF_PACKET, SOCK_RAW, ntohs(0x0003))
   ```
3. Cada quadro Ethernet recebido passa por:

   * `parse_ethernet()`
   * `parse_ipv4()`, se EtherType for 0x0800
   * `parse_tcp()`, `parse_udp()`, `parse_icmp()`
4. Logs são salvos via `logger.py`
5. Contadores são atualizados e exibidos no terminal
6. Execução continua até `Ctrl+C`

---

# 📦 **3. Descrição dos Arquivos**

### **`main.py`**

* Entrada principal do programa
* Lê interface via linha de comando
* Inicia loop de captura
* Exibe contadores em tempo real

### **`raw_sniffer.py`**

* Classe responsável pelo socket RAW
* Captura quadros Ethernet
* Encaminha payload para os parsers
* Altera contadores por protocolo
* Escreve logs via logger

### **`parsers.py`**

Contém parsers mínimos e didáticos:

* `parse_ethernet()`
* `parse_ipv4()`
* `parse_tcp()`
* `parse_udp()`
* `parse_icmp()`

Todos usam `struct.unpack` para interpretar cabeçalhos manualmente.

### **`logger.py`**

* Cria diretório `logs/` automaticamente
* Escreve CSVs:

  * `camada_internet.csv`
  * `camada_transporte.csv`

### **`utils.py`**

* Apenas função `now()` para timestamp

---

# 🛠️ **4. Requisitos**

### Necessário para execução:

* Linux, WSL2 ou container labredes
* Python 3.8+
* Permissão raw socket
  → via `--privileged` nos containers
  → ou `sudo` em máquina real

---

# 🧪 **5. Como Executar no Ambiente “labredes”**

Este é o ambiente oficial recomendado pelo professor.
Você já tem a imagem:

```
docker pull ghcr.io/sjohann81/labredes:latest
```

## **Passo 1 — Criar rede Docker**

```bash
docker network create lab
```

## **Passo 2 — Subir quantos nós quiser (proxy + clientes)**

Exemplo com 3 nós:

```bash
docker run -it --privileged --network lab -v $(pwd):/home ghcr.io/sjohann81/labredes bash
docker run -it --privileged --network lab -v $(pwd):/home ghcr.io/sjohann81/labredes bash
docker run -it --privileged --network lab -v $(pwd):/home ghcr.io$sjohann81/labredes bash
```

Cada terminal será um “host”.

## **Passo 3 — No host que executará o monitor**

Entre no diretório montado:

```bash
cd /home/monitor
```

Execute o sniffer com a interface da rede Docker (geralmente `eth0`):

```bash
python3 main.py eth0
```

Você verá:

```
IPv4: 10  TCP: 4  UDP: 3  ICMP: 1  ARP: 2
```

Cada contador vai subindo conforme a rede recebe tráfego.

---

# 📡 **6. Gerando Tráfego para Teste**

### Em outro container:

```bash
ping 172.18.0.2
curl http://172.18.0.3
```

### Ou consultando DNS:

```bash
apt update && apt install -y dnsutils
dig www.pucrs.br
```

### Trabalhando DHCP (caso implemente depois):

```bash
dhclient -v eth0
```

Os logs serão salvos automaticamente em:

```
logs/
  camada_internet.csv
  camada_transporte.csv
```

---

# 🧠 **7. Possíveis Melhorias**

Esta versão é intencionalmente minimalista. Melhorias naturais:

### 🔵 Camada Aplicação

Parser de:

* DNS (nome das queries)
* DHCP (yk, opções e lease)
* HTTP (método, status)
* NTP (timestamps)

### 🔵 Dashboard Rich

Uma interface melhor estruturada com:

* Tabela por protocolo
* Taxas (pps)
* Gráficos ASCII

### 🔵 Log Rotativo

* Arquivos por hora
* Pastas por dia
* Sistema de arquivamento automático

### 🔵 Execução em múltiplos workers

Processamento paralelo de pacotes.

---

# 🎯 **8. Conclusão**

Esta versão mínima:

✔ segue 100% das regras do T2 (sem Scapy, só socket + struct)
✔ roda perfeitamente no ambiente labredes
✔ possui arquitetura clara e pronta para expansão
✔ permite capturar pacotes reais entre containers
✔ produz CSVs para relatório
✔ é simples o bastante para você entender camada por camada

---
