# T2 – Guia de Execução Manual dos Testes  
**Monitor Linux (VM) + Clientes Windows reais — SEM TÚNEL**

Este documento descreve exatamente como executar TODOS os testes necessários do T2 utilizando:

- **Monitor em Linux (VM VirtualBox)**
- **Clientes Windows reais**
- Captura de pacotes com **AF_PACKET**
- **Sem túnel**, conforme exceção permitida pela professora

---

# 📌 1. Preparação do Ambiente

## 1.1 Monitor (VM Linux)

### Requisitos:
- VM configurada em modo **Bridge Adapter**
- Interface ativa: normalmente `enp0s3`
- Projeto clonado em:
```

~/t2-redes-network-monitor

````

### Comandos:

```bash
cd ~/t2-redes-network-monitor/src/monitor
sudo python3 main.py enp0s3
````

Saída esperada:

```
[+] Monitorando interface enp0s3
IPv4:0 IPv6:0 ICMP:0 TCP:0 UDP:0 ARP:0
```

> **IMPORTANTE:** O `sudo` é obrigatório para o socket RAW funcionar.

---

## 1.2 Clientes Windows

Nos PCs Windows, abra **PowerShell**.

Obtenha o IP do monitor:

```bash
ip a
```

Exemplo:

```
192.168.15.49
```

Certifique-se de que TODOS os dispositivos estão na MESMA rede física.

---

# 📌 2. Testes Individuais

Execute cada teste no **Cliente 1** e depois repita no **Cliente 2**.

O monitor deve incrementar corretamente ICMP, TCP, UDP e ARP.

---

## 2.1 Teste ICMP – Ping

No Windows:

```powershell
ping 192.168.15.49
```

No monitor, deve registrar:

```
ARP += 1
ICMP += 4
```

Explicação:

* Primeiro pacote → ARP resolve MAC
* Depois → ICMP Echo Request/Reply

---

## 2.2 Teste DNS – UDP

No Windows:

```powershell
nslookup www.pucrs.br
```

Monitor deve registrar:

```
UDP += 1 ou 2
```

Depende de cache DNS.

---

## 2.3 Teste TCP – HTTP/HTTPS

No Windows:

```powershell
curl https://www.pucrs.br
```

No monitor:

```
TCP += vários pacotes
```

---

## 2.4 Teste de Conectividade entre Clientes

No PC1:

```powershell
ping <IP_DO_PC2>
```

No PC2:

```powershell
ping <IP_DO_PC1>
```

O monitor deve ver ambos os fluxos ICMP.

---

# 📌 3. Testes Concorrentes

Execute simultaneamente em ambos os PCs.

---

## 3.1 Ping simultâneo

PC1:

```powershell
ping 192.168.15.49 -t
```

PC2:

```powershell
ping 192.168.15.49 -t
```

Monitor deve ver ICMP contínuo dos dois.

---

## 3.2 DNS simultâneo

PC1:

```powershell
nslookup www.google.com
```

PC2:

```powershell
nslookup www.pucrs.br
```

Monitor registra múltiplos UDP.

---

## 3.3 TCP simultâneo

PC1:

```powershell
curl https://www.pucrs.br
```

PC2:

```powershell
curl https://www.ifsc.edu.br
```

Monitor verá vários fluxos TCP diferentes.

---

# 📌 4. Testes com Degradação de Rede (CLUMSY)

Instale no Windows:

🔗 [https://github.com/jagt/clumsy/releases](https://github.com/jagt/clumsy/releases)

---

## 4.1 Latência simulada

Configure no Clumsy:

* Lag: 200 ms
* Enable: ON

Execute:

```powershell
ping 192.168.15.49
```

Monitor verá:

* tempos maiores
* possíveis retransmissões

---

## 4.2 Perda de pacotes

Configure:

* Drop: 30%

Execute:

```powershell
ping 192.168.15.49
```

Monitor verá:

* ICMP subindo mais devagar
* variações no fluxo

---

# 📌 5. Finalização

Para encerrar o monitor:

```
CTRL + C
```

Ele exibirá:

```
Logs salvos em logs/session_YYYY-MM-DD_HH-MM-SS
```

Cada sessão contém:

```
camada_internet.csv
camada_transporte.csv
camada_aplicacao.csv
monitor.log
raw_packets.bin
```

Esses são os arquivos obrigatórios pelo enunciado.

---

# 📌 6. Checklist para o Relatório

Marque conforme concluir:

* [ ] Captura de ARP
* [ ] Captura de ICMP
* [ ] Captura de DNS (UDP)
* [ ] Captura de TCP
* [ ] Captura concorrente
* [ ] Teste com latência (Clumsy)
* [ ] Teste com perda (Clumsy)
* [ ] Geração dos CSVs
* [ ] Logs organizados por sessão
* [ ] Descrição da arquitetura
* [ ] Justificativa técnica da ausência do túnel
* [ ] Prints do monitor + testes

---

# 📌 7. Observação sobre o Túnel (Tun0)

Como autorizado pela professora:

> O túnel **não será utilizado**, pois não funciona com clientes Windows e requer ambiente totalmente Linux.

Seu monitor opera diretamente sobre a **interface real da VM**, capturando tráfego da LAN via **AF_PACKET**, o que satisfaz integralmente os requisitos do trabalho.
