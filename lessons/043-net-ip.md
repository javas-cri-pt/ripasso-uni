---
day: 43
topic_id: net-ip
title: "IP, routing e subnetting"
area: computer-science
course: "Reti di Calcolatori"
grounded_in: null
adjacent: [net-stack, net-transport, net-app]
completeness_checked: true
quiz_count: 10
---

# IP, routing e subnetting

> **Perché oggi:** in `net-stack` hai visto la pila ISO/OSI e TCP/IP e hai imparato che il **livello 3 (rete)** ha un compito solo: portare un pacchetto da una macchina qualsiasi del pianeta a un'altra. Oggi scopriamo *come* ci riesce. L'indirizzo IP è il "codice di avviamento postale" di Internet, la **subnet mask** dice dove finisce il quartiere e inizia il resto del mondo, e il **routing** è il navigatore che sceglie la strada. Il subnetting (dividere una rete in sottoreti) è il calcolo che compare in ogni esame di reti e in ogni colloquio di sistemistica: lo impariamo facendo i conti a mano, bit per bit.

## L'indirizzo IPv4

Un **indirizzo IP** (*Internet Protocol address*) identifica in modo univoco un'interfaccia di rete. Nella versione **IPv4** (*Internet Protocol version 4*) è lungo **32 bit**, cioè 4 byte. Lo si scrive in **notazione dotted-decimal**: i quattro byte separati da punti, ciascuno rappresentato dal suo valore decimale da 0 a 255 (un byte sono 8 bit, e `2^8 = 256` valori). Esempio:

```
192 . 168 . 1 . 10
11000000 . 10101000 . 00000001 . 00001010   (gli stessi 32 bit in binario)
```

Siccome i bit totali sono 32, lo spazio IPv4 conta `2^32 ≈ 4,3 miliardi` di indirizzi: tantissimi nel 1981, pochissimi oggi, ed è il motivo per cui esistono NAT e IPv6 (ne parliamo in fondo).

Ogni indirizzo è diviso in **due parti**:

- **Network ID** (parte di rete): identifica la rete a cui la macchina appartiene. Tutte le macchine della stessa rete locale condividono lo stesso network ID.
- **Host ID** (parte di host): identifica la singola macchina **dentro** quella rete.

Il confine tra le due parti **non è fisso**: lo decide la subnet mask. È proprio questo che rende possibile il subnetting.

## La subnet mask e la notazione CIDR

La **subnet mask** (maschera di sottorete) è un altro numero da 32 bit, fatto di una sequenza di **`1` consecutivi** seguita da una sequenza di **`0`**. I bit a `1` segnano le posizioni che appartengono al **network ID**; i bit a `0` segnano le posizioni dell'**host ID**. Esempio classico:

```
Maschera:  255 . 255 . 255 . 0
           11111111.11111111.11111111.00000000
           |---- 24 bit di rete ----|-8 host-|
```

Qui i primi 24 bit sono di rete e gli ultimi 8 di host. Invece di scrivere la maschera per esteso, si usa la **notazione CIDR** (*Classless Inter-Domain Routing*): si aggiunge all'indirizzo uno **slash** seguito dal numero di bit a `1` della maschera, chiamato **prefisso** (*prefix length*). Quindi `255.255.255.0` si scrive **`/24`**, e la rete dell'esempio è `192.168.1.0/24`.

Tabella di conversione delle maschere più comuni:

| CIDR | Subnet mask | Bit di host | Host indirizzabili |
|------|-------------|-------------|--------------------|
| /24  | 255.255.255.0   | 8 | 2^8 − 2 = **254** |
| /25  | 255.255.255.128 | 7 | 2^7 − 2 = **126** |
| /26  | 255.255.255.192 | 6 | 2^6 − 2 = **62**  |
| /27  | 255.255.255.224 | 5 | 2^5 − 2 = **30**  |
| /28  | 255.255.255.240 | 4 | 2^4 − 2 = **14**  |
| /30  | 255.255.255.252 | 2 | 2^2 − 2 = **2**   |

## Classi di indirizzi (il sistema storico)

Prima del CIDR, il confine rete/host era deciso dalle **classi**, cioè dai primi bit dell'indirizzo:

- **Classe A:** primo bit `0`, primo byte `1–126`, maschera `/8`. Pochissime reti enormi (16 milioni di host ciascuna).
- **Classe B:** primi bit `10`, primo byte `128–191`, maschera `/16`. Reti medie (65 534 host).
- **Classe C:** primi bit `110`, primo byte `192–223`, maschera `/24`. Moltissime reti piccole (254 host).
- **Classe D** (`224–239`): riservata al **multicast**. **Classe E** (`240–255`): sperimentale.

Il sistema a classi sprecava enormi quantità di indirizzi (chi aveva bisogno di 2000 host doveva prendersi un'intera classe B da 65 000), perciò dal 1993 è stato sostituito dal **CIDR**, che permette un prefisso di **qualsiasi** lunghezza (`/8`, `/19`, `/26`…) e quindi reti su misura. Le classi restano importanti per capire i testi e per gli **indirizzi privati** (RFC 1918), riservati alle reti interne e non instradabili su Internet pubblica: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.

## Come si calcola: network address, broadcast, host

Dentro ogni rete due indirizzi sono **riservati** e non si possono assegnare a una macchina:

- **Network address** (indirizzo di rete): tutti i bit di host a **`0`**. È il "nome" della rete.
- **Broadcast address** (indirizzo di broadcast): tutti i bit di host a **`1`**. Un pacchetto spedito qui arriva a **tutte** le macchine della rete.

Per questo gli host utilizzabili sono `2^(bit di host) − 2` (si sottraggono network e broadcast). Vediamo il **procedimento** con un esempio completo.

**Dato:** l'indirizzo `192.168.1.0/24`. Vogliamo network, broadcast, range di host e numero di host.

1. **Bit di host** = 32 − 24 = **8**.
2. **Network address**: metti a zero gli 8 bit di host → `192.168.1.0`.
3. **Broadcast**: metti a uno gli 8 bit di host → ultimo byte `11111111` = 255 → `192.168.1.255`.
4. **Range host utilizzabili**: da `192.168.1.1` a `192.168.1.254`.
5. **Numero host**: `2^8 − 2 = 254`.

Il trucco pratico che fa risparmiare tempo è il **block size** (ampiezza del blocco): è l'incremento con cui si susseguono le reti su un certo byte, e vale `256 − (valore della maschera su quel byte)`. Per `/24` la maschera sull'ultimo byte è 0, ma lavoriamo sul byte: per i prefissi "lunghi" (dal /25 in su) il block size si calcola sul byte dove cade il confine. Lo vediamo subito nel subnetting.

## Subnetting: dividere una rete in sottoreti

Fare **subnetting** significa "rubare" alcuni bit all'host ID per crearne di nuovi destinati a distinguere **sottoreti** (*subnet*). Ogni bit rubato raddoppia il numero di sottoreti e dimezza gli host per sottorete. La regola:

- con **`s` bit** presi in prestito ottieni **`2^s` sottoreti**;
- a ciascuna restano `2^(bit di host − s) − 2` host utilizzabili.

**Esempio A — indirizzo generico in una rete /26.** Dato l'host `192.168.10.70/26`, trova a quale sottorete appartiene.

1. **Bit di host** = 32 − 26 = 6. La maschera `/26` sull'ultimo byte è `11000000` = **192**.
2. **Block size** = 256 − 192 = **64**. Le sottoreti sull'ultimo byte partono quindi da 0, 64, 128, 192.
3. **In quale blocco cade 70?** Tra 64 e 127. Quindi:
   - **Network address** = `192.168.10.64`
   - **Broadcast** = 64 + 64 − 1 = 127 → `192.168.10.127`
   - **Range host** = `192.168.10.65` … `192.168.10.126`
   - **Host utilizzabili** = `2^6 − 2 = 62`

**Esempio B — dividere una /24 in 4 sottoreti.** Devi spezzare `192.168.1.0/24` in **4** reti uguali.

1. Servono `2^s ≥ 4` → **s = 2** bit presi in prestito. Nuovo prefisso = 24 + 2 = **/26**.
2. **Block size** = 256 − 192 = **64**.
3. Le 4 sottoreti, elencate col loro network, broadcast e range:

| # | Network | Range host utilizzabili | Broadcast |
|---|---------|-------------------------|-----------|
| 1 | 192.168.1.0/26   | .1 – .62     | 192.168.1.63  |
| 2 | 192.168.1.64/26  | .65 – .126   | 192.168.1.127 |
| 3 | 192.168.1.128/26 | .129 – .190  | 192.168.1.191 |
| 4 | 192.168.1.192/26 | .193 – .254  | 192.168.1.255 |

Ogni sottorete ospita 62 host: 4 × 62 = 248 host totali, un po' meno dei 254 originari (è il prezzo di avere 4 coppie network/broadcast invece di una sola). Questa è la tecnica per dare a quattro reparti di un'azienda ciascuno la sua rete isolata partendo da un unico blocco.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 680 280" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="340" y="22" font-weight="700">192.168.10.70 /26 — 32 bit divisi da una maschera /26</text>
  </g>
  <!-- 4 byte boxes -->
  <g font-size="11" text-anchor="middle">
    <rect x="30" y="44" width="150" height="34" rx="5" fill="var(--card2)" stroke="var(--rule)"/><text x="105" y="66" fill="var(--ink)">192</text>
    <rect x="186" y="44" width="150" height="34" rx="5" fill="var(--card2)" stroke="var(--rule)"/><text x="261" y="66" fill="var(--ink)">168</text>
    <rect x="342" y="44" width="150" height="34" rx="5" fill="var(--card2)" stroke="var(--rule)"/><text x="417" y="66" fill="var(--ink)">10</text>
    <rect x="498" y="44" width="150" height="34" rx="5" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="573" y="66" fill="var(--ink)">70 = 01000110</text>
  </g>
  <!-- network vs host bracket -->
  <line x1="30" y1="92" x2="570" y2="92" stroke="var(--rule)"/>
  <text x="300" y="108" font-size="10.5" fill="var(--muted)" text-anchor="middle">← primi 26 bit: NETWORK (uguali in tutta la sottorete) →</text>
  <line x1="570" y1="92" x2="648" y2="92" stroke="var(--accent)"/>
  <text x="609" y="108" font-size="10.5" fill="var(--accent)" text-anchor="middle">6 bit HOST</text>
  <!-- last byte bit detail -->
  <g font-size="11" text-anchor="middle">
    <text x="340" y="140" fill="var(--ink)" font-weight="700">Ultimo byte: 01000110</text>
    <rect x="250" y="152" width="115" height="30" rx="4" fill="var(--card)" stroke="var(--rule)"/><text x="307" y="172" fill="var(--ink)" font-size="10.5">01 = rete</text>
    <rect x="367" y="152" width="175" height="30" rx="4" fill="var(--card)" stroke="var(--accent)" stroke-width="1.5"/><text x="454" y="172" fill="var(--ink)" font-size="10.5">000110 = host</text>
  </g>
  <!-- results -->
  <g font-size="11.5" fill="var(--ink)" text-anchor="start">
    <rect x="120" y="200" width="440" height="66" rx="8" fill="var(--card2)" stroke="var(--rule)"/>
    <text x="140" y="222">Block size = 256 − 192 = 64 → blocchi: 0, 64, 128, 192</text>
    <text x="140" y="242" fill="var(--good)">Network 192.168.10.64 · Broadcast 192.168.10.127</text>
    <text x="140" y="260" fill="var(--muted)">Host .65 – .126 (62 utilizzabili)</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">La maschera /26 taglia i 32 bit a due bit dalla fine del quarto byte: i 26 bit a sinistra sono rete, i 6 a destra host. L'ultimo byte 70 = 01000110 ha i due bit alti (01) nella parte di rete, che insieme al block size di 64 colloca l'host nel blocco che parte da .64.</figcaption>
</figure>

## Gateway e routing di base

Una macchina che vuole spedire un pacchetto fa prima un test semplice, usando la **subnet mask**: calcola il network address del **proprio** indirizzo e quello del **destinatario**. Se coincidono, il destinatario è nella **stessa rete locale** e il pacchetto gli viene consegnato direttamente (tramite indirizzo fisico, livello 2). Se **non** coincidono, il destinatario è "fuori dal quartiere" e il pacchetto va mandato al **default gateway**.

Il **default gateway** (gateway predefinito) è il **router** della rete locale: la porta d'uscita verso tutto ciò che non è locale. Un **router** è un dispositivo di livello 3 che ha più interfacce su reti diverse e inoltra i pacchetti da una all'altra, avvicinandoli alla destinazione.

Come sceglie il router dove mandare un pacchetto? Consulta la sua **tabella di routing** (*routing table*), un elenco di righe del tipo **"rete di destinazione → prossimo salto (next hop)"**. Il router confronta l'IP di destinazione con le reti in tabella e sceglie quella che combacia col **prefisso più lungo** (*longest prefix match*): la rotta più specifica vince. Se nessuna rotta specifica combacia, usa la **default route** `0.0.0.0/0`, cioè "per tutto il resto, manda da questa parte".

Le tabelle si riempiono in due modi:

- **Routing statico:** le rotte sono scritte a mano dall'amministratore. Semplice, ma non si adatta ai guasti.
- **Routing dinamico:** i router si scambiano informazioni con **protocolli di routing** e aggiornano le tabelle da soli. I due grandi criteri sono:
  - **Distance vector** (vettore distanza, es. **RIP** — *Routing Information Protocol*): ogni router conosce solo la "distanza" (numero di salti, *hop count*) verso ogni rete e la comunica ai vicini.
  - **Link state** (stato dei collegamenti, es. **OSPF** — *Open Shortest Path First*): ogni router conosce la topologia completa e calcola i cammini più brevi (con l'algoritmo di Dijkstra). Tra reti di operatori diversi (i *sistemi autonomi*) si usa **BGP** (*Border Gateway Protocol*), il protocollo che tiene insieme Internet.

## Cenni a NAT e IPv6

Lo spazio IPv4 è esaurito. Due risposte convivono:

- **NAT** (*Network Address Translation*, traduzione degli indirizzi di rete): un solo IP pubblico viene condiviso da molte macchine con IP **privati**. Il router di casa riscrive, in uscita, l'indirizzo privato sorgente (es. `192.168.1.10`) con il proprio IP pubblico e tiene una tabella per sapere a chi restituire le risposte. È il motivo per cui decine di dispositivi di casa tua navigano con un solo indirizzo pubblico. Il dettaglio di come NAT usa le **porte** (PAT) si lega al livello di trasporto di `net-transport`.
- **IPv6** (*Internet Protocol version 6*): la soluzione strutturale. Usa indirizzi da **128 bit** (contro i 32 di IPv4), cioè `2^128` indirizzi, un numero così grande da rendere il NAT non più necessario. Si scrivono in **esadecimale** a gruppi di 16 bit separati da due punti, es. `2001:0db8:85a3::8a2e:0370:7334` (i gruppi di soli zeri si comprimono con `::`).

## Esempi concreti

- **La tua rete di casa.** Il router assegna indirizzi in `192.168.1.0/24` (privata, RFC 1918); il PC prende `192.168.1.10`, il gateway è `192.168.1.1`, il broadcast `192.168.1.255`. Quando apri un sito, l'IP di destinazione è pubblico, quindi fuori rete: il pacchetto va al gateway, che fa **NAT** e lo instrada verso Internet.
- **Segmentare un ufficio.** Un'azienda con un blocco `10.0.0.0/24` vuole separare amministrazione, produzione e ospiti per sicurezza. Fa subnetting in tre `/26` (`10.0.0.0/26`, `10.0.0.64/26`, `10.0.0.128/26`), 62 host ciascuna: i reparti non si vedono tra loro se non passando dal router, dove si applicano regole di filtraggio.
- **Collegamento punto-punto tra due router.** Per il link che unisce due soli router si usa una **/30** (`255.255.255.252`): 4 indirizzi totali, 2 utilizzabili, esattamente uno per router. Zero spreco.

## Notable use case

- **Reti private RFC 1918** sono usate praticamente da ogni rete aziendale e domestica del mondo dietro NAT; senza di esse i 4,3 miliardi di IPv4 sarebbero finiti decenni fa.
- **Google, Facebook e i grandi operatori** scambiano le loro rotte via **BGP**: un errore di configurazione BGP ha causato blackout globali reali (interi servizi irraggiungibili per ore) perché il mondo "perde la strada" verso quelle reti.
- **Cloud provider** (AWS, Azure, GCP) ti fanno definire una **VPC** (*Virtual Private Cloud*) scegliendo un blocco CIDR (es. `10.0.0.0/16`) e poi fare subnetting in sottoreti per zona di disponibilità: il subnetting di oggi è esattamente ciò che fai configurando l'infrastruttura cloud.
- **IPv6** è ormai maggioritario nel traffico mobile di molti operatori, che instradano nativamente su 128 bit evitando il doppio NAT.

## Fonti

- **Kurose, Ross** — *Computer Networking: A Top-Down Approach* (capitolo Network Layer: IP, addressing, routing)
- **Tanenbaum, Wetherall** — *Computer Networks* (il riferimento classico sullo strato di rete)
- **RFC 1918** — Address Allocation for Private Internets; **RFC 4632** — CIDR
- **subnetting-practice** — subnettingpractice.com e il subnet calculator di jodies.de (ip.jodies.de) per verificare i calcoli

## Concetti adiacenti

- `net-stack` — dove si colloca IP (livello 3) nella pila ISO/OSI e TCP/IP, la cornice della lezione di oggi
- `net-transport` — cosa viaggia *dentro* i pacchetti IP: TCP e UDP, le porte su cui si appoggia anche il NAT
- `net-app` — HTTP, DNS e TLS, i protocolli applicativi che usano gli indirizzi e le rotte di oggi

## Quiz (10 — tutte rispondibili dalla lezione)

1. Quanti bit ha un indirizzo IPv4, come si scrive in dotted-decimal e quanti indirizzi totali esistono?
2. Cosa distinguono il **network ID** e l'**host ID**, e chi stabilisce il confine tra i due?
3. Come è fatta una **subnet mask** e cosa significa la notazione **CIDR** `/24`?
4. Perché il sistema a **classi** è stato sostituito dal CIDR, e quali sono i tre blocchi di indirizzi **privati**?
5. Cosa sono il **network address** e il **broadcast address**, e perché gli host utilizzabili sono `2^(bit di host) − 2`?
6. Dato `/26`, quanto vale la maschera sull'ultimo byte e quanto il **block size**?
7. Per dividere una rete in `N` sottoreti, quanti **bit** devi prendere in prestito e cosa succede al numero di host per sottorete?
8. Come fa una macchina a decidere se consegnare un pacchetto **direttamente** o mandarlo al **default gateway**?
9. Cos'è il **longest prefix match** e a cosa serve la **default route** `0.0.0.0/0`?
10. Spiega in una frase cosa fanno **NAT** e **IPv6** rispetto all'esaurimento degli indirizzi IPv4.

<details><summary>Risposte</summary>

1. **32 bit** (4 byte). In **dotted-decimal** si scrivono i 4 byte separati da punti, ciascuno da 0 a 255 (es. `192.168.1.10`). Totale: `2^32 ≈ 4,3 miliardi` di indirizzi.
2. Il **network ID** identifica la rete (uguale per tutte le macchine della stessa rete), l'**host ID** la singola macchina dentro quella rete. Il confine è stabilito dalla **subnet mask**.
3. È una sequenza di `1` consecutivi seguita da `0`: i bit a `1` sono la parte di rete, quelli a `0` la parte di host. **CIDR `/24`** significa 24 bit a `1` (maschera `255.255.255.0`), cioè 24 bit di rete e 8 di host.
4. Perché le classi sprecavano indirizzi (confine rete/host fisso a /8, /16, /24): il CIDR consente un prefisso di **qualsiasi** lunghezza, quindi reti su misura. I privati sono `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
5. **Network address** = tutti i bit di host a `0` (nome della rete); **broadcast** = tutti i bit di host a `1` (raggiunge tutte le macchine). Sono riservati, quindi dagli indirizzi disponibili se ne sottraggono 2: `2^(bit di host) − 2`.
6. Maschera sull'ultimo byte = `11000000` = **192**; **block size** = 256 − 192 = **64**.
7. Devi prendere `s` bit tali che `2^s ≥ N`. Ogni bit rubato all'host **raddoppia** le sottoreti e **dimezza** gli host per sottorete (restano `2^(bit di host − s) − 2`).
8. Calcola il network address **proprio** e quello del **destinatario** usando la subnet mask: se coincidono, consegna **diretta** (stessa rete locale); se differiscono, manda al **default gateway** (il router).
9. Il **longest prefix match** è la regola per cui, tra più rotte che combaciano, vince quella col **prefisso più lungo** (la più specifica). La **default route `0.0.0.0/0`** è la rotta "per tutto il resto", usata quando nessuna rotta specifica combacia.
10. **NAT** fa condividere un solo IP pubblico a molte macchine con IP privati, riscrivendo l'indirizzo in uscita; **IPv6** risolve il problema alla radice passando a indirizzi da **128 bit** (`2^128` indirizzi).
</details>

## Esercizi

1. **Calcolo completo su un host.** Dato `172.16.20.200/27`, calcola: subnet mask in dotted-decimal, block size, network address, broadcast address, range di host utilizzabili e numero di host.
2. **Dividere una rete in N sottoreti.** Devi suddividere `192.168.5.0/24` in **8** sottoreti uguali. Trova il nuovo prefisso, la maschera, il block size, e scrivi network e broadcast delle prime **tre** sottoreti.
3. **Stessa rete o gateway?** Un PC ha IP `10.1.1.130` con maschera `/25` (`255.255.255.128`). Deve inviare un pacchetto a `10.1.1.60` e un altro a `10.1.1.200`. Per ciascuno, stabilisci se la consegna è diretta o se passa dal default gateway, mostrando il calcolo.
4. **Dimensiona il prefisso.** Un reparto ha bisogno di ospitare almeno **50** host in un'unica sottorete. Qual è il prefisso CIDR più "stretto" (meno spreco) che basta? Giustifica con il numero di host.

<details><summary>Soluzioni</summary>

1. `/27` → bit di host = 32 − 27 = 5; maschera = `11111111.11111111.11111111.11100000` = **255.255.255.224**. Block size = 256 − 224 = **32** → blocchi sull'ultimo byte: 0, 32, 64, …, 192, 224. 200 cade tra **192 e 223**. Quindi:
   - **Network** = `172.16.20.192`
   - **Broadcast** = 192 + 32 − 1 = 223 → `172.16.20.223`
   - **Range host** = `172.16.20.193` … `172.16.20.222`
   - **Host utilizzabili** = `2^5 − 2 = 30`
2. Servono `2^s ≥ 8` → **s = 3** bit. Nuovo prefisso = 24 + 3 = **/27**; maschera **255.255.255.224**; block size = 256 − 224 = **32**. Prime tre sottoreti:
   - Sottorete 1: network `192.168.5.0/27`, broadcast `192.168.5.31` (host .1–.30)
   - Sottorete 2: network `192.168.5.32/27`, broadcast `192.168.5.63` (host .33–.62)
   - Sottorete 3: network `192.168.5.64/27`, broadcast `192.168.5.95` (host .65–.94)
   (Le successive proseguono a passi di 32: .96, .128, .160, .192, .224.)
3. Con `/25` il block size sull'ultimo byte è 256 − 128 = **128**, quindi i blocchi sono `0–127` e `128–255`. Il PC `10.1.1.130` sta nel blocco **128–255**, cioè rete `10.1.1.128/25`.
   - Verso `10.1.1.60`: 60 sta nel blocco **0–127**, rete `10.1.1.0/25` → **rete diversa** → passa dal **default gateway**.
   - Verso `10.1.1.200`: 200 sta nel blocco **128–255**, rete `10.1.1.128/25` → **stessa rete** del PC → **consegna diretta**.
4. Servono ≥ 50 host, quindi `2^(bit di host) − 2 ≥ 50`. Con 6 bit: `2^6 − 2 = 62 ≥ 50` (basta). Con 5 bit: `2^5 − 2 = 30 < 50` (insufficiente). Quindi servono **6 bit di host**, prefisso = 32 − 6 = **/26** (maschera `255.255.255.192`). È il più stretto che basta: ospita 62 host, lo spreco minimo rispetto a un /25 (126 host) troppo largo.
</details>
