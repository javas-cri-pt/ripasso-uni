---
day: 28
topic_id: net-transport
title: "Livello di trasporto: TCP vs UDP e controllo della congestione"
area: computer-science
course: "Reti di Calcolatori"
grounded_in: null
adjacent: [net-stack, net-app, xc-sysdesign]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun acronimo lasciato senza definizione."
---

# Livello di trasporto: TCP vs UDP

> **Perché oggi:** nella pila che hai già visto (`net-stack`) il livello di trasporto è quello strato in mezzo che prende i dati della tua applicazione e li porta "dal processo giusto al processo giusto". Oggi ci entri dentro. È il livello che decide se una connessione è **affidabile** o **veloce**, ed è la radice delle cose concrete che tocchi ogni giorno: la **latenza** di una chiamata API, i **timeout** che la fanno fallire, il motivo per cui una videochiamata preferisce "saltare un pezzo" piuttosto che bloccarsi. Ai colloqui di reti e di **system design** è terreno fisso: "TCP o UDP, e perché?", "cos'è il three-way handshake?", "cosa succede quando la rete si intasa?".

## A cosa serve il livello di trasporto

Il livello di **rete** (dove vive **IP**, *Internet Protocol*) sa portare un pacchetto **da un computer a un altro**: conosce gli indirizzi, lo fa saltare di router in router. Ma un computer fa girare **tanti programmi insieme** — il browser, il client di posta, un'app di chat, un server web. IP ti porta alla **macchina** giusta; non sa a **quale programma**, dentro quella macchina, consegnare i dati.

È qui che entra il livello di **trasporto**: il suo compito è la comunicazione **processo-a-processo**, cioè portare i dati dal **processo** (il programma in esecuzione) giusto sul mittente al **processo** giusto sul destinatario. Per farlo introduce due idee: le **porte** e il **multiplexing**.

**Porta** (*port*): un numero (da 0 a 65535) che **identifica un'applicazione su un host**. La coppia **indirizzo IP + porta** individua univocamente un estremo di comunicazione e si chiama **socket**. L'analogia è un palazzo: l'**indirizzo IP** è l'indirizzo del palazzo, la **porta** è il numero dell'interno. Alcune porte sono convenzionali e note (*well-known ports*): la **80** è HTTP, la **443** è HTTPS, la **53** è il DNS, la **22** è SSH. Un server "resta in ascolto" su una porta; un client, quando apre una connessione, ne usa una temporanea (*ephemeral*) scelta dal sistema operativo.

**Multiplexing** e **demultiplexing**: *multiplexing* ("multiplazione") è la capacità di far convivere **più flussi di dati diversi sulla stessa rete**. In uscita, il livello di trasporto prende i dati di tanti processi e li incanala tutti giù verso IP, marcando ciascuno con la sua porta (multiplexing). In arrivo, fa il contrario: guarda la porta di destinazione di ogni pezzo in arrivo e lo **smista al processo giusto** (*demultiplexing*). È grazie a questo che puoi guardare un video, scaricare un file e chattare **nello stesso momento** sulla stessa connessione Internet senza che i dati si confondano: ogni flusso ha la sua coppia di porte che lo tiene separato dagli altri.

Su questo livello convivono due protocolli con filosofie opposte: **TCP** e **UDP**. Stessa rete sotto, stesso scopo (processo-a-processo), ma due modi radicalmente diversi di intendere il trasporto.

## TCP: la connessione affidabile

**TCP (Transmission Control Protocol)** è **orientato alla connessione** e **affidabile**. La sua unità di dati si chiama **segmento**.

**Orientato alla connessione** (*connection-oriented*) significa che prima di scambiare qualunque dato utile i due estremi **stabiliscono un canale** tra loro, concordando dei parametri iniziali (lo vediamo tra poco col three-way handshake). Non è un "filo fisico" dedicato: è uno **stato condiviso** che i due host tengono in memoria per riconoscere che stanno parlando l'uno con l'altro.

**Affidabile** (*reliable*) significa che TCP **garantisce** che i dati arrivino **tutti, integri e nell'ordine giusto**, anche se sotto c'è IP che è *best-effort* ("fa del suo meglio ma non promette niente": può perdere pacchetti, duplicarli, consegnarli fuori ordine). TCP ricostruisce l'affidabilità con tre meccanismi che lavorano insieme:

- **Numeri di sequenza** (*sequence numbers*): TCP non manda "un messaggio", manda un **flusso di byte**, e **numera** ogni byte. Ogni segmento porta nell'header il numero di sequenza del primo byte che contiene. Così il ricevente sa esattamente dove va inserito ogni pezzo — e può **rimettere in ordine** segmenti arrivati scombinati e **scartare i duplicati**.
- **ACK** (*acknowledgment*, "conferma di ricezione"): il ricevente **conferma** ciò che ha ricevuto, rimandando indietro un numero che dice "ho ricevuto fino a qui, ora aspetto il byte numero X". È la ricevuta di ritorno.
- **Ritrasmissione** (*retransmission*): il mittente fa partire un **timer** quando spedisce un segmento. Se l'ACK corrispondente **non arriva in tempo** (timeout) — oppure se arrivano segnali che un pezzo si è perso — il mittente **rispedisce** quel segmento. Nessun dato va perso davvero: al massimo viene rimandato.

Oltre all'affidabilità, TCP fa due tipi di controllo sul ritmo dell'invio: il **controllo di flusso** e il **controllo di congestione**. Sono due cose diverse e vale la pena non confonderle.

### Il three-way handshake

Il canale TCP si apre con il **three-way handshake** ("stretta di mano a tre vie"): tre messaggi che sincronizzano i due estremi **prima** che passi un solo byte di dati utili. Usa due flag (bit di controllo nell'header): **SYN** (*synchronize*, "sincronizza") e **ACK** (conferma).

1. **SYN** — il **client** manda un segmento col flag **SYN** attivo: "voglio aprire una connessione, e il mio numero di sequenza iniziale è *x*".
2. **SYN-ACK** — il **server** risponde con **SYN + ACK** insieme: "accetto (SYN mio, numero di sequenza *y*) e confermo il tuo (ACK di *x*)".
3. **ACK** — il **client** conferma a sua volta con **ACK**: "ricevuto il tuo, connessione aperta".

Dopo questi tre messaggi la connessione è stabilita e i dati possono fluire. Punto da ricordare per i colloqui: è un intero **giro di andata e ritorno** (*round-trip*) speso **prima** di mandare il primo byte utile — e questo **costa tempo (latenza)**. Se ci aggiungi l'handshake di **TLS** (la cifratura, vedi `net-stack`), capisci perché aprire connessioni da zero ogni volta è costoso e perché si cerca di **riusarle**.

### Lo schema del three-way handshake

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 600 320" style="max-width:100%;height:auto;font-family:inherit" role="img" aria-label="Three-way handshake TCP: SYN dal client, SYN-ACK dal server, ACK dal client">
  <defs>
    <marker id="arHsR" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" fill="none" stroke="var(--accent)" stroke-width="1.6"/></marker>
    <marker id="arHsL" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" fill="none" stroke="var(--accent)" stroke-width="1.6"/></marker>
  </defs>
  <g font-size="13" fill="var(--ink)" text-anchor="middle">
    <!-- colonne -->
    <rect x="70" y="20" width="130" height="40" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="135" y="45" font-weight="600">Client</text>
    <rect x="400" y="20" width="130" height="40" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="465" y="45" font-weight="600">Server</text>
  </g>
  <!-- linee di vita -->
  <g stroke="var(--muted)" stroke-width="1.2" stroke-dasharray="4 4">
    <path d="M135,60 L135,300"/>
    <path d="M465,60 L465,300"/>
  </g>
  <!-- frecce -->
  <g stroke="var(--accent)" stroke-width="1.8" fill="none">
    <path d="M135,110 L458,140" marker-end="url(#arHsR)"/>
    <path d="M465,180 L142,210" marker-end="url(#arHsL)"/>
    <path d="M135,250 L458,280" marker-end="url(#arHsR)"/>
  </g>
  <g font-size="12.5" fill="var(--ink)" text-anchor="middle" font-weight="600">
    <text x="300" y="118">1 · SYN</text>
    <text x="300" y="188">2 · SYN-ACK</text>
    <text x="300" y="258">3 · ACK</text>
  </g>
  <g font-size="10.5" fill="var(--muted)" text-anchor="middle">
    <text x="300" y="133">"apro la connessione, seq = x"</text>
    <text x="300" y="203">"accetto (seq = y) e confermo x"</text>
    <text x="300" y="273">"confermo y — connessione aperta"</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Il three-way handshake di TCP. Tre messaggi (SYN → SYN-ACK → ACK) sincronizzano client e server prima che passi un solo byte di dati utili: un round-trip completo speso in apertura.</figcaption>
</figure>

### Controllo di flusso: non sommergere il ricevente

Il **controllo di flusso** (*flow control*) risolve un problema a due: cosa succede se il **mittente spedisce più in fretta di quanto il ricevente riesca a leggere**? Il ricevente ha un buffer (una memoria di parcheggio) di dimensione limitata: se si riempie, i dati in eccesso andrebbero persi.

TCP lo evita con la **finestra** (*window*). Il ricevente comunica di continuo, dentro gli ACK, **quanto spazio libero gli resta nel buffer**: è la *finestra di ricezione* (*receive window*). Il mittente non può avere "in volo" (spediti ma non ancora confermati) più byte di quanti ne entrano in quella finestra. Se il ricevente rallenta, annuncia una finestra più piccola e il mittente frena; se si libera, la finestra cresce e il mittente accelera. È un sistema a **finestra scorrevole** (*sliding window*): man mano che arrivano gli ACK, la finestra "scorre" in avanti e permette di spedire nuovi byte. In una frase: il controllo di flusso protegge il **ricevente**.

### Controllo di congestione: non intasare la rete

Il **controllo di congestione** (*congestion control*) risolve un problema diverso: non il ricevente, ma la **rete in mezzo**. I router hanno code di capacità finita; se tutti spingono troppi dati insieme, le code si riempiono, i pacchetti vengono scartati e la rete va in **congestione** (l'equivalente di un ingorgo stradale). Il paradosso è che più tutti insistono, peggio va per tutti.

TCP affronta la cosa con un principio: **la perdita di pacchetti è il segnale che la rete è intasata**, quindi quando perdo pacchetti devo **rallentare**. Il mittente tiene una seconda finestra, la *finestra di congestione* (*congestion window*), che stima quanto la rete può sopportare in quel momento. La quantità di dati che può davvero spedire è il **minimo** tra la finestra di ricezione (controllo di flusso) e la finestra di congestione (controllo di congestione). Due algoritmi classici, a parole:

- **Slow start** ("partenza lenta"): all'inizio il mittente non sa quanto regge la rete, quindi **parte piano** e **raddoppia** il ritmo a ogni round-trip andato a buon fine. Sembra prudente ma cresce in fretta (è una crescita esponenziale): sonda rapidamente il limite della rete.
- **AIMD** (*Additive Increase, Multiplicative Decrease*, "aumento additivo, diminuzione moltiplicativa"): una volta raggiunta una velocità ragionevole, TCP **cresce piano** (aggiunge un po' a ogni round-trip: aumento *additivo*) ma, appena rileva una perdita, **taglia di netto** (dimezza: diminuzione *moltiplicativa*). "Sali con cautela, scendi di colpo." Questo comportamento "a dente di sega" è ciò che rende TCP **equo** (*fair*): tante connessioni che condividono lo stesso collo di bottiglia tendono a spartirsi la banda in modo bilanciato.

La differenza da tenere a mente: **controllo di flusso = riguardo per il ricevente; controllo di congestione = riguardo per la rete.** Sono due freni distinti che agiscono insieme.

## UDP: senza connessione, leggero

**UDP (User Datagram Protocol)** è l'opposto di TCP: **senza connessione** (*connectionless*) e **non affidabile**. La sua unità di dati si chiama **datagramma** (*datagram*).

Niente **handshake**: non c'è alcun canale da stabilire, il primo pacchetto parte subito. Niente **numeri di sequenza**: UDP non riordina nulla. Niente **ACK** né **ritrasmissioni**: UDP **non conferma** la ricezione e **non rispedisce** ciò che si perde. Niente controllo di flusso né di congestione: spara i datagrammi al ritmo che vuole l'applicazione. In pratica UDP aggiunge a IP quasi solo una cosa: le **porte** (quindi il multiplexing/demultiplexing processo-a-processo) e un controllo di integrità minimale (*checksum*). Tutto il resto — se serve — lo deve gestire l'applicazione.

Il prezzo è l'inaffidabilità; il guadagno è che UDP è **velocissimo e leggerissimo**: zero tempo perso ad aprire connessioni (nessun round-trip iniziale), zero peso di contabilità, zero ritardi dovuti a ritrasmissioni. Per certi usi, "arrivare subito" conta più di "arrivare tutto".

## Quando usare l'uno, quando l'altro

Il criterio è una domanda sola: **è più importante che arrivi tutto, o che arrivi in fretta?**

- **TCP** quando l'**integrità conta più della velocità**: il **web** (HTTP/HTTPS), il trasferimento di **file**, la posta elettronica, qualsiasi API dove un dato mancante corrompe il risultato. Se scarichi un PDF e si perde un pezzo, il file è rotto: meglio aspettare la ritrasmissione.
- **UDP** quando la **tempestività conta più della perfezione** e perdere qualche pezzo è tollerabile:
  - **Streaming** video/audio: meglio saltare un fotogramma che bloccare tutto per ritrasmetterne uno ormai vecchio.
  - **Gaming** online: conta l'**ultima** posizione del giocatore, non recuperare quelle vecchie — ritrasmettere un dato scaduto è inutile.
  - **DNS**: una domanda-risposta minuscola (nome → IP). Aprire una connessione TCP a tre vie per due pacchetti sarebbe uno spreco.
  - **VoIP** (*Voice over IP*, la telefonia su Internet) e **videochiamate**: la conversazione deve restare in tempo reale; un pacchetto in ritardo è peggio di un pacchetto perso.

Regola pratica da colloquio: "**TCP = affidabile ma con overhead; UDP = leggero ma fai da te sull'affidabilità**". E la frontiera moderna (vedi *Notable use case*) mostra che si può anche **costruire l'affidabilità sopra UDP**, prendendo il meglio dei due mondi.

## Esempi concreti

- **Una chiamata API REST** dalla tua app a un backend: va su **HTTP**, quindi su **TCP**. Dietro le quinte: three-way handshake (un round-trip), poi handshake TLS, poi la richiesta. Se l'app apre una nuova connessione a ogni chiamata, paga quegli handshake **ogni volta** — per questo si usano **keep-alive** e connessioni persistenti, per ammortizzare il costo su molte richieste.
- **Un timeout che scatta.** Poiché TCP ritrasmette e sotto c'è IP best-effort, una richiesta può restare appesa ad aspettare un ACK che non arriva. Nel codice imposti un **timeout** (dopo quanti secondi rinunciare): sapere che esiste il meccanismo di ritrasmissione ti spiega *perché* una connessione può "pendere" invece di fallire subito.
- **Una videochiamata che "pixela" ma non si blocca.** È **UDP** al lavoro: quando la rete perde pacchetti, l'app preferisce mostrare un fotogramma degradato piuttosto che fermarsi ad aspettare. Con TCP l'intera chiamata si congelerebbe in attesa della ritrasmissione.
- **Il tuo browser che carica dieci risorse insieme** (immagini, CSS, script): è il **multiplexing** del livello di trasporto — flussi distinti, ciascuno con la sua coppia di porte, che convivono sulla stessa connessione Internet senza mischiarsi.

## Notable use case

**QUIC e HTTP/3 su UDP.** Per decenni la regola è stata "web = TCP, UDP = roba che può perdersi". Oggi quella regola si è capovolta nel punto più visibile del web. **QUIC** (nato in Google, poi standardizzato) è un protocollo di trasporto costruito **sopra UDP** — non sopra TCP. Perché proprio UDP, il protocollo "inaffidabile"? Perché UDP è una base **minimale e leggera**: QUIC parte da lì e **ricostruisce da sé** l'affidabilità (numeri di sequenza, ritrasmissioni, controllo di congestione), ma **senza i vincoli di TCP**. I vantaggi chiave:

- **Meno round-trip in apertura.** QUIC **integra la cifratura** (TLS) dentro l'handshake di trasporto, invece di farli in sequenza (prima TCP, poi TLS). Risultato: la connessione sicura si stabilisce in **meno giri di andata e ritorno**, quindi meno latenza all'avvio.
- **Niente *head-of-line blocking* tra flussi.** In TCP, se si perde un segmento, **tutti** i flussi multiplati su quella connessione si fermano ad aspettarlo (il "blocco in testa alla coda"). QUIC tiene i flussi **indipendenti**: la perdita su un flusso non blocca gli altri.

**HTTP/3** è semplicemente la versione di HTTP che gira sopra QUIC. È già diffusissimo (lo usano Google, Cloudflare, Meta). La morale che chiude il cerchio con `net-stack`: l'affidabilità **non deve** per forza stare dentro TCP — si può metterla a un livello più alto, dove costa meno, lasciando sotto un trasporto leggero come UDP. "UDP inaffidabile" non significa "UDP inutile per cose serie": significa che su UDP puoi **costruirti l'affidabilità che vuoi**.

## Fonti

- **Kurose & Ross, "Computer Networking: A Top-Down Approach"** — il capitolo sul livello di trasporto è il riferimento: TCP, UDP, controllo di flusso e congestione spiegati nell'ordine in cui li incontri nella pratica.
- **Tanenbaum, "Computer Networks"** — la trattazione classica e approfondita dei protocolli di trasporto e dei meccanismi di affidabilità.
- **RFC 9000 (QUIC)** e **MDN Web Docs** (developer.mozilla.org) — per HTTP/3 e QUIC, il riferimento aggiornato su come il web moderno usa UDP.

## Concetti adiacenti

- **net-stack** — la pila a livelli completa (ISO/OSI e TCP/IP), l'incapsulamento e il viaggio di una richiesta web: il quadro in cui questo livello si incastra.
- **net-app** — il livello applicativo che gira **sopra** il trasporto: HTTP in dettaglio (metodi, versioni 1.1/2/3), DNS come sistema gerarchico, cookie e sessioni.
- **xc-sysdesign** — dove latenza, round-trip, connessioni persistenti e scelta del protocollo diventano decisioni di architettura nei colloqui di system design.

## Quiz (10 — tutte rispondibili dalla lezione)

1. A cosa serve il livello di **trasporto** e perché IP da solo non basta?
2. Cos'è una **porta** e cosa aggiunge rispetto all'indirizzo IP? Cosa sono **multiplexing** e **demultiplexing**?
3. Cosa significa che TCP è **orientato alla connessione** e **affidabile**? Con quali tre meccanismi ricostruisce l'affidabilità?
4. Spiega il **three-way handshake**, passo per passo, e di' perché "costa" in termini di latenza.
5. Cos'è il **controllo di flusso** e come funziona la **finestra**? Chi protegge?
6. Cos'è il **controllo di congestione** e in che modo differisce dal controllo di flusso?
7. Spiega a parole **slow start** e **AIMD**.
8. Quali caratteristiche ha **UDP**? Cosa gli manca rispetto a TCP e cosa ci guadagna in cambio?
9. Elenca casi d'uso tipici di **TCP** e di **UDP**, con il criterio che li distingue.
10. Cos'è **QUIC/HTTP3** e perché è notevole che il web moderno si appoggi a **UDP**?

<details><summary>Risposte</summary>

1. Il livello di **trasporto** porta i dati **dal processo giusto al processo giusto** (comunicazione **processo-a-processo**). IP sa consegnare i pacchetti alla **macchina** giusta tramite l'indirizzo IP, ma su un computer girano **tanti programmi insieme**: IP non sa a quale consegnare. Il trasporto colma questo vuoto con le **porte** e il multiplexing.

2. Una **porta** è un numero (0–65535) che **identifica un'applicazione su un host**; la coppia IP + porta è un **socket**. Rispetto all'indirizzo IP (che individua la macchina), la porta individua il **programma** dentro la macchina (es. 80 = HTTP, 443 = HTTPS, 53 = DNS). Il **multiplexing** è incanalare in uscita i dati di più processi sulla stessa rete marcandoli con la loro porta; il **demultiplexing** è, in arrivo, smistare ogni pezzo al processo giusto guardando la porta di destinazione. È ciò che fa convivere più flussi senza mescolarli.

3. **Orientato alla connessione**: prima di scambiare dati i due estremi **stabiliscono un canale** (stato condiviso) con l'handshake. **Affidabile**: garantisce che i dati arrivino **tutti, integri e in ordine**, anche sopra un IP best-effort. I tre meccanismi: **numeri di sequenza** (ogni byte è numerato, così si riordina e si scartano i duplicati), **ACK** (il ricevente conferma fin dove ha ricevuto), **ritrasmissione** (se l'ACK non arriva entro un timeout, il mittente rispedisce il segmento).

4. (1) **SYN** — il client chiede di aprire la connessione e annuncia il suo numero di sequenza iniziale; (2) **SYN-ACK** — il server accetta (SYN suo) e conferma quello del client (ACK); (3) **ACK** — il client conferma a sua volta e la connessione è aperta. "Costa" perché è un intero **round-trip** (andata e ritorno) speso **prima** di inviare il primo byte utile — latenza pura, a cui spesso si aggiunge l'handshake TLS.

5. Il **controllo di flusso** evita che il mittente spedisca **più in fretta di quanto il ricevente riesca a leggere**. Funziona con la **finestra** (*window*): il ricevente annuncia negli ACK quanto spazio libero ha nel buffer (finestra di ricezione) e il mittente non può tenere "in volo" più byte di quelli; è una **finestra scorrevole** che avanza man mano che arrivano gli ACK. Protegge il **ricevente**.

6. Il **controllo di congestione** evita di **intasare la rete** in mezzo (le code dei router), non il ricevente. TCP interpreta la **perdita di pacchetti come segnale di congestione** e rallenta, regolando una *finestra di congestione*; la quantità spedibile è il **minimo** tra finestra di ricezione e di congestione. Differenza chiave: il controllo di **flusso** protegge il **ricevente**, quello di **congestione** protegge la **rete**.

7. **Slow start** ("partenza lenta"): all'inizio il mittente non sa quanto regge la rete, quindi **parte piano** e **raddoppia** il ritmo a ogni round-trip riuscito (crescita rapida, esponenziale) per sondare il limite. **AIMD** (*Additive Increase, Multiplicative Decrease*): a regime **cresce piano** (aggiunge poco a ogni round-trip) ma, appena c'è una perdita, **taglia di colpo** (dimezza). "Sali con cautela, scendi di netto" — ed è ciò che rende TCP equo tra più connessioni.

8. **UDP (User Datagram Protocol)** è **senza connessione** e **non affidabile**: niente handshake, niente numeri di sequenza, niente ACK, niente ritrasmissioni, niente controllo di flusso/congestione. Gli manca tutto l'apparato di affidabilità di TCP; in cambio è **velocissimo e leggero** (nessun round-trip iniziale, nessun overhead, nessun ritardo da ritrasmissione). L'unità dati è il **datagramma**.

9. **TCP** quando l'**integrità conta più della velocità**: web (HTTP/HTTPS), trasferimento file, email, API dove un dato mancante rompe tutto. **UDP** quando la **tempestività conta più della perfezione** e perdere qualche pezzo è tollerabile: streaming, gaming online, DNS, VoIP e videochiamate. Il criterio: *deve arrivare tutto, o deve arrivare in fretta?*

10. **QUIC** è un protocollo di trasporto costruito **sopra UDP** che **ricostruisce da sé** l'affidabilità (sequenze, ritrasmissioni, congestione) senza i vincoli di TCP, e **HTTP/3** è la versione di HTTP che ci gira sopra. È notevole perché ribalta il vecchio "web = TCP": partendo da UDP, QUIC **riduce i round-trip** in apertura (integra la cifratura TLS nell'handshake) ed elimina il *head-of-line blocking* tra flussi. Morale: l'affidabilità si può mettere a un livello più alto, sopra un trasporto leggero come UDP.

</details>
