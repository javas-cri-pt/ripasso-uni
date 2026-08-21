---
day: 14
topic_id: net-stack
title: "Reti — il modello a livelli e lo stack TCP/IP"
area: computer-science
course: Reti di Calcolatori
grounded_in: "UNIBO/terzoAnno/RDC"
adjacent: [net-transport, net-app, xc-sysdesign]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun acronimo lasciato senza definizione."
---

# Reti — il modello a livelli e lo stack TCP/IP

> **Perché oggi:** ogni chiamata API, ogni pagina web, ogni chatbot che fai a Glacom viaggia su questa pila. Non è teoria da libro: capire lo stack è ciò che ti fa **debuggare** la latenza che si mangia i secondi, i **timeout** che fanno fallire una richiesta, gli **errori TLS** che bloccano una connessione o un **DNS** che non risolve. Ed è la spina dorsale delle domande da colloquio di reti e di **system design** — su tutte la classica "cosa succede quando digiti un indirizzo nel browser e premi invio?".

## Perché "a livelli"

Far comunicare due computer in rete è un problema enorme: bisogna trasformare dei dati in segnali elettrici o onde radio, farli attraversare cavi e router, ritrovare la strada giusta, rimettere in ordine i pezzi arrivati, e infine capire cosa significano per l'applicazione. Tutto insieme è ingestibile.

La soluzione è l'**incapsulamento a livelli** (in inglese *layering*): dividere la comunicazione in **strati sovrapposti**, ognuno con **un compito preciso**. Ogni livello si appoggia al servizio del livello sotto e offre un servizio al livello sopra, e — idea chiave — **parla logicamente col suo pari** dall'altra parte della connessione: il livello di trasporto del tuo computer "dialoga" col livello di trasporto del server, come se gli altri livelli non esistessero.

Il vantaggio è la **modularità**: puoi **cambiare un livello senza toccare gli altri**. Passi dal Wi-Fi al cavo Ethernet (cambia il livello più basso) e il tuo browser non se ne accorge nemmeno; nasce un nuovo protocollo applicativo e non devi reinventare come i dati attraversano Internet. Ogni strato è una scatola con un'interfaccia chiara, e questo rende Internet estensibile e riparabile a pezzi.

**Incapsulamento** (*encapsulation*): mentre i dati **scendono** la pila, ogni livello **aggiunge la sua "busta"** attorno ai dati che riceve dal livello sopra. Questa busta si chiama **header** (intestazione): un pacchetto di informazioni di servizio (indirizzi, numeri di porta, numeri di sequenza…) che serve **solo a quel livello** per fare il suo lavoro. Dall'altra parte, mentre i dati **risalgono** la pila, ogni livello **apre la sua busta**, legge il suo header, lo toglie e passa il contenuto al livello sopra. È come spedire una lettera: la metti in una busta (applicazione), la busta va in un sacco postale (trasporto), il sacco su un camion con una destinazione (rete): ogni contenitore ha l'etichetta che serve a chi lo maneggia in quel momento.

## ISO/OSI vs TCP/IP

Esistono due modi di descrivere questa pila, e li devi conoscere entrambi perché ai colloqui li citano.

Il modello **ISO/OSI** (dove **ISO** = *International Organization for Standardization*, l'ente di standardizzazione, e **OSI** = *Open Systems Interconnection*, "interconnessione di sistemi aperti") è il **riferimento teorico**: descrive la comunicazione in **7 livelli**, dal basso verso l'alto — **fisico** (i bit come segnali su un mezzo), **data link** (collegamento tra due nodi adiacenti), **rete** (instradamento tra reti diverse), **trasporto** (comunicazione affidabile tra due processi), **sessione** (gestione di una "sessione" di dialogo), **presentazione** (formato/codifica/cifratura dei dati), **applicazione** (i protocolli usati dalle app). È pulito e didattico, ma **nessuno lo implementa alla lettera**.

Il modello **TCP/IP** è quello **realmente usato da Internet**. **TCP/IP = Transmission Control Protocol / Internet Protocol**, i due protocolli-cardine da cui prende il nome. Ha **4-5 livelli** (a seconda di come si conta): **accesso alla rete** (*network access*, che accorpa il fisico e il data link di OSI), **internet** (l'instradamento tra reti, dove vive IP), **trasporto** (dove vivono TCP e UDP) e **applicazione** (che accorpa sessione, presentazione e applicazione di OSI).

La corrispondenza, a grandi linee: il **trasporto** e il livello **rete/internet** coincidono quasi uno a uno tra i due modelli; sopra, i tre livelli alti di OSI (sessione, presentazione, applicazione) sono tutti schiacciati nell'unico livello **applicazione** di TCP/IP; sotto, i due livelli bassi di OSI (fisico, data link) diventano l'unico livello **accesso alla rete**. In pratica: **OSI è la mappa concettuale, TCP/IP è il territorio.**

## La pila TCP/IP in un colpo d'occhio

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 600 360" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arNetStack" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="13" fill="var(--ink)" text-anchor="middle">
   <rect x="90" y="20" width="360" height="58" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
   <text x="270" y="44" font-weight="600">Applicazione</text>
   <text x="270" y="63" font-size="10.5" fill="var(--muted)">HTTP · DNS · TLS — unità dati: messaggi</text>

   <rect x="90" y="98" width="360" height="58" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
   <text x="270" y="122" font-weight="600">Trasporto</text>
   <text x="270" y="141" font-size="10.5" fill="var(--muted)">TCP · UDP — unità dati: segmenti</text>

   <rect x="90" y="176" width="360" height="58" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
   <text x="270" y="200" font-weight="600">Internet (Rete)</text>
   <text x="270" y="219" font-size="10.5" fill="var(--muted)">IP — unità dati: pacchetti</text>

   <rect x="90" y="254" width="360" height="58" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
   <text x="270" y="278" font-weight="600">Accesso alla rete</text>
   <text x="270" y="297" font-size="10.5" fill="var(--muted)">Ethernet · Wi-Fi — unità dati: frame</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.5" fill="none">
   <path d="M478,40 L478,300" marker-end="url(#arNetStack)"/>
  </g>
  <g font-size="10.5" fill="var(--muted)" text-anchor="middle">
   <text x="510" y="150" transform="rotate(90 510 170)">i dati scendono: ogni livello aggiunge il suo header</text>
   <text x="42" y="150" transform="rotate(-90 42 170)">i dati risalgono: ogni livello toglie il suo header</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">La pila TCP/IP. In uscita i dati scendono e ogni livello aggiunge la sua "busta" (header): messaggi → segmenti → pacchetti → frame. In arrivo risalgono e ogni livello toglie la sua busta. Il nome dell'unità dati cambia a ogni livello.</figcaption>
</figure>

## Livello di rete/Internet: IP

**IP (Internet Protocol)** è il protocollo che tiene insieme Internet: si occupa di **indirizzamento** e **instradamento** dei dati tra reti diverse. La sua unità dati è il **pacchetto** (*packet*).

- **Indirizzamento.** Ogni interfaccia di rete ha un **indirizzo IP**, un numero che la identifica univocamente sulla rete — l'equivalente di un indirizzo di casa a cui recapitare i pacchetti. Esistono due versioni: **IPv4** (*Internet Protocol version 4*), con indirizzi a 32 bit scritti come quattro numeri puntati (es. `93.184.216.34`), ormai **quasi esauriti** perché sono "solo" circa 4 miliardi; e **IPv6** (*version 6*), con indirizzi a 128 bit (es. `2606:2800:220:1:...`), uno spazio praticamente illimitato, pensato proprio per superare l'esaurimento di IPv4.
- **Instradamento (routing).** Portare un pacchetto dal mittente al destinatario significa fargli attraversare, di rete in rete, una catena di apparati. Un **router** è il dispositivo che sta al confine tra reti diverse e, per ogni pacchetto, **decide su quale strada inoltrarlo** verso la destinazione, leggendone l'indirizzo IP di arrivo. È lo "smistatore" del traffico: il pacchetto salta da un router al successivo (*hop* dopo *hop*) finché arriva.
- **Best-effort.** IP è un servizio **best-effort** ("al meglio possibile"): fa del suo meglio per consegnare i pacchetti, ma **non garantisce nulla**. Un pacchetto può **perdersi**, arrivare **duplicato**, o arrivare **fuori ordine** rispetto a come è partito. IP non se ne preoccupa: se serve affidabilità, la mette sopra il livello di trasporto (lo vediamo tra poco). Questa scelta — un livello di rete semplice e "stupido", l'intelligenza ai bordi — è ciò che rende Internet scalabile.

(Il **subnetting**, cioè dividere un grande spazio di indirizzi in sottoreti più piccole, è il modo in cui si organizzano gli indirizzi IP dentro un'organizzazione. Qui basta sapere che esiste: nella pratica lo incontri quando configuri reti o cloud, ma i calcoli con le maschere di sottorete non ci servono adesso.)

## Livello di trasporto: TCP vs UDP

Il livello di trasporto sta **sopra** IP e ne compensa i limiti. Il suo compito: portare i dati **dal processo giusto sul mittente al processo giusto sul destinatario**. Per questo introduce il concetto di **porta**.

**Porta** (*port*): un numero che **identifica l'applicazione (il processo) su un host**. L'indirizzo IP ti porta al computer giusto; la **porta** ti dice, dentro quel computer, **a quale programma** consegnare i dati. Convenzioni note: la **80** è HTTP, la **443** è HTTPS, la **53** è il DNS. Coppia (indirizzo IP + porta) = *socket*, l'estremo di una comunicazione.

Su questo livello convivono due protocolli con filosofie opposte.

**TCP (Transmission Control Protocol)** è **orientato alla connessione** e **affidabile**. "Orientato alla connessione" significa che prima di scambiare dati si stabilisce un canale tra i due estremi; "affidabile" significa che **garantisce** che i dati arrivino **tutti, integri e nell'ordine giusto**. Come? Numera i pezzi, si fa confermare ciò che arriva (**ACK**, *acknowledgment*, "conferma di ricezione"), **ritrasmette** i pezzi persi e **rimette in ordine** quelli arrivati scombinati. In più fa **controllo di flusso** (non manda più dati di quanti il ricevente riesca a gestire) e **controllo di congestione** (rallenta se la rete è intasata, per non peggiorare la situazione). La sua unità dati è il **segmento**.

Il canale TCP si apre con il **three-way handshake** ("stretta di mano a tre vie"), tre messaggi che sincronizzano i due estremi:

1. **SYN** — il client manda un segmento con il flag **SYN** (*synchronize*): "voglio aprire una connessione, ecco il mio numero di sequenza iniziale".
2. **SYN-ACK** — il server risponde con **SYN + ACK**: "ok, accetto (SYN mio), e confermo il tuo (ACK)".
3. **ACK** — il client conferma a sua volta con **ACK**: "ricevuto, connessione aperta".

Dopo questi tre messaggi la connessione è stabilita e i dati possono fluire. Nota bene: è un **giro di andata e ritorno** (*round-trip*) speso **prima** ancora di mandare il primo byte di dati utili — e questo costa tempo, come vedremo nella sezione sulla latenza.

**UDP (User Datagram Protocol)** è l'opposto: **senza connessione** e **non affidabile**. Niente handshake, niente numeri di sequenza, niente ritrasmissioni, niente conferme: spara i suoi pacchetti (chiamati **datagrammi**) e **non si preoccupa** se arrivano, se arrivano in ordine o se si perdono. In cambio è **veloce e leggero**: zero tempo perso a stabilire connessioni, zero peso di controllo.

**Quando l'uno, quando l'altro:**

- **TCP** quando ti serve che **tutto arrivi giusto**: pagine **web** (HTTP/HTTPS), trasferimento di **file**, email. Meglio un attimo più lento ma corretto.
- **UDP** quando la **velocità conta più della perfezione** e perdere qualche pezzo è tollerabile: **streaming** video/audio (meglio saltare un fotogramma che bloccare tutto per ritrasmetterlo), **gaming** online (conta l'ultima posizione, non recuperare quella vecchia), **DNS** (una domanda-risposta minuscola, non vale la pena aprire una connessione TCP), e le **videochiamate**.

## Livello applicativo: HTTP, DNS, TLS

È il livello che le tue applicazioni usano direttamente. Tre protocolli su tutti.

**HTTP (HyperText Transfer Protocol)** è il **protocollo del web**. Funziona a **richiesta/risposta** (*request/response*): il **client** (il browser) manda una **richiesta** (es. "dammi la pagina `/prodotti`") e il **server** risponde con una **risposta** (il contenuto, più un **codice di stato** — 200 "ok", 404 "non trovato", 500 "errore del server"). HTTP è **stateless** ("senza stato"): ogni richiesta è **indipendente** dalle altre, il server **non ricorda** di per sé le richieste precedenti. Per ricordare chi sei tra una richiesta e l'altra (login, carrello) servono meccanismi sopra HTTP, come i **cookie** o i **token**.

**DNS (Domain Name System)** è la **"rubrica di Internet"**: **traduce un nome in un indirizzo IP**. Tu digiti `www.glacom.ai`, ma i router sanno instradare solo verso **numeri** (indirizzi IP): il DNS fa la **risoluzione** nome → IP, cioè ti dice a quale indirizzo numerico corrisponde quel nome. Come cercare un contatto nella rubrica del telefono: conosci il nome, ti serve il numero. Senza DNS dovresti ricordare a memoria gli indirizzi IP di ogni sito.

**TLS (Transport Layer Security)** è il protocollo che **cifra la connessione**. È la **"s" di HTTPS** (*HTTP Secure*): HTTPS non è altro che HTTP fatto viaggiare **dentro** un canale TLS. TLS fa tre cose: **cifratura** (chi intercetta il traffico vede solo dati illeggibili), **integrità** (garantisce che i dati non siano stati alterati per strada) e **autenticazione** (tramite i **certificati**, ti assicura che il server sia davvero chi dice di essere, non un impostore). Anche TLS, come TCP, stabilisce il canale con un suo **handshake** (scambio di chiavi e certificato) prima che i dati veri possano passare. *(TLS è l'evoluzione del vecchio **SSL**, Secure Sockets Layer, oggi deprecato: per questo a volte si dice ancora "certificato SSL".)*

Come si incastrano: quando visiti un sito sicuro, **DNS** trova l'indirizzo, **TCP** apre il canale, **TLS** lo cifra, e dentro quel canale cifrato viaggiano le richieste **HTTP**.

## Cosa succede quando apri un sito (il viaggio di una richiesta)

Questo è **l'esempio d'oro** da saper raccontare a un colloquio. Digiti `https://www.glacom.ai` e premi invio. Ecco il viaggio, passo per passo:

1. **DNS — trovare l'indirizzo.** Il browser non sa dove sia `www.glacom.ai`. Fa una query **DNS** che **risolve il nome nell'indirizzo IP** del server (es. `93.184.216.34`). Ora sa a quale numero bussare.
2. **TCP — aprire la connessione.** Il browser apre una connessione **TCP** verso quell'IP sulla **porta 443** (HTTPS), con il **three-way handshake** (SYN → SYN-ACK → ACK). Un round-trip speso qui.
3. **TLS — cifrare il canale.** Sopra la connessione TCP appena aperta parte l'**handshake TLS**: si scambiano il **certificato** (il browser verifica che il server sia autentico) e le chiavi per **cifrare**. Da qui in poi il canale è sicuro.
4. **HTTP — mandare la richiesta.** Dentro il canale cifrato il browser manda la **richiesta HTTP**: "GET `/`", cioè "dammi la home page".
5. **Giù e su per la pila (incapsulamento).** La richiesta **scende la pila** sul tuo computer: il messaggio HTTP diventa un **segmento** TCP (header con le porte), poi un **pacchetto** IP (header con gli indirizzi), poi un **frame** a livello di accesso alla rete. I pacchetti IP **viaggiano** attraverso i router di Internet (best-effort, hop dopo hop) fino al server. Lì **risalgono la pila**: ogni livello toglie il suo header finché il server ritrova la richiesta HTTP originale.
6. **La risposta torna indietro.** Il server elabora la richiesta e manda la **risposta HTTP** (la pagina, con codice **200**), che rifà lo stesso viaggio a ritroso: scende la pila del server, attraversa la rete, risale la pila del tuo computer, e il browser finalmente **mostra la pagina**.

Il filo da tenere in mente: **DNS → TCP → TLS → HTTP**, con l'incapsulamento che avvolge e svolge i dati a ogni salto di livello.

## Il ponte col lavoro

Perché tutto questo conta quando scrivi codice a Glacom, e non solo al colloquio:

- **Latenza e round-trip.** Hai visto che aprire una connessione costa **giri di andata e ritorno** (*round-trip*): uno per il TCP handshake, altri per il TLS handshake. Se ogni chiamata API riaprisse la connessione da zero, sprecheresti quei round-trip **ogni volta**. Per questo si **riusano le connessioni**: il **keep-alive** (tenere aperta la connessione TCP per più richieste), **HTTP/2** (che multiplexa più richieste su un'unica connessione) e le connessioni persistenti. Meno handshake = meno latenza = app più reattiva.
- **Timeout e retry.** Poiché IP è **best-effort** e la rete può perdere pacchetti o rispondere lenta, ogni chiamata di rete può **non tornare in tempo**. Nel codice imposti un **timeout** (dopo quanti secondi rinunciare) e una politica di **retry** (riprovare, magari con attesa crescente). Capire lo stack ti dice **cosa** può andare storto: un timeout in fase di connessione è diverso da uno in fase di risposta.
- **Debug di errori reali.** Un **errore TLS** ("certificato scaduto/non valido") è un problema del passo 3 del viaggio, non del tuo codice applicativo. Un **DNS che non risolve** ("host not found") è il passo 1: il nome non si traduce in IP, e non hai nemmeno provato a connetterti. Sapere a quale livello sta il problema **dimezza il tempo di debug**.
- **Le fondamenta di WebSocket e CDN.** I **WebSocket** sono una **connessione persistente** bidirezionale (aperta una volta sopra TCP, resta viva per scambiare messaggi nei due sensi in tempo reale, senza rifare la richiesta ogni volta) — utili per chat e notifiche live. Le **CDN (Content Delivery Network)** sono reti di server distribuiti geograficamente: ti servono i contenuti dal nodo **più vicino a te**, accorciando il percorso di rete e quindi la **latenza**. Entrambe sono ottimizzazioni che hanno senso solo se hai in testa lo stack.

Tutto questo si collega a `xc-sysdesign`: quando progetti un sistema, le decisioni su connessioni, latenza, CDN e protocolli sono esattamente il livello di ragionamento che ti chiedono in un colloquio di **system design**.

## Notable use cases

- **HTTPS ovunque (TLS di default).** Oggi il web è quasi tutto in HTTPS: i browser marcano come "non sicuro" un sito in HTTP puro, e certificati gratuiti (es. **Let's Encrypt**) hanno reso TLS lo standard di fatto per qualunque sito, non solo per le banche.
- **DNS gestito.** Poche aziende gestiscono i propri server DNS a mano: si usano servizi **DNS gestiti** (come **Cloudflare** o **Amazon Route 53**) che offrono risoluzione veloce, affidabile e distribuita nel mondo.
- **QUIC e HTTP/3 su UDP.** La frontiera recente: **QUIC** è un protocollo di trasporto costruito **sopra UDP** (non TCP) che integra al suo interno la cifratura e riduce i round-trip iniziali, e **HTTP/3** è la versione di HTTP che ci gira sopra. Curiosità che chiude il cerchio: proprio perché a lungo si è detto "UDP = inaffidabile, TCP = web", vedere il web moderno spostarsi **su UDP** per **ridurre la latenza** mostra che l'affidabilità si può ricostruire a un livello più alto, dove costa meno.

## Fonti

- **Kurose & Ross, "Computer Networking: A Top-Down Approach"** — il libro di riferimento, quello che parte "dall'alto" (dalle applicazioni) e scende: perfetto per capire lo stack nell'ordine in cui lo incontri nella pratica.
- **Tanenbaum, "Computer Networks"** — il classico complementare, con la trattazione approfondita dei livelli più bassi e dei fondamenti.
- **MDN Web Docs** (developer.mozilla.org) — il riferimento pratico e sempre aggiornato per **HTTP**: metodi, codici di stato, header, HTTPS.

## Concetti adiacenti

- **net-transport** — approfondimento sul livello di trasporto: TCP nel dettaglio (finestre, controllo di flusso e congestione, chiusura della connessione) e confronto pieno con UDP.
- **net-app** — il livello applicativo in profondità: HTTP (metodi, header, versioni 1.1/2/3), DNS come sistema gerarchico, cookie e sessioni.
- **net-ip** — il livello di rete nel dettaglio: struttura degli indirizzi IPv4/IPv6, subnetting, tabelle di instradamento e come lavorano davvero i router.
- **xc-sysdesign** — dove questi mattoni (latenza, connessioni persistenti, CDN, protocolli) diventano decisioni di architettura nei colloqui di system design.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Perché la comunicazione di rete è organizzata **a livelli**? Qual è il vantaggio principale?
2. Cos'è l'**incapsulamento** e cosa succede ai dati mentre scendono e risalgono la pila?
3. Che differenza c'è tra il modello **ISO/OSI** e il modello **TCP/IP**? Cosa significano le sigle?
4. Cosa fa il protocollo **IP** e cosa significa che è **best-effort**?
5. Elenca le differenze principali tra **TCP** e **UDP**, con un esempio d'uso per ciascuno.
6. Spiega il **three-way handshake** di TCP, passo per passo.
7. A cosa serve il **DNS**?
8. Cosa fa **TLS** e con cosa è collegato in "HTTPS"?
9. Cos'è una **porta** e a cosa serve, dato che c'è già l'indirizzo IP?
10. Racconta il **viaggio di una richiesta web** quando apri un sito HTTPS, nell'ordine corretto.

<details><summary>Risposte</summary>

1. Perché far comunicare due computer è un problema troppo grande per essere affrontato tutto insieme: dividendolo in **livelli**, ognuno ha **un compito preciso** e parla logicamente col suo pari dall'altra parte. Il vantaggio principale è la **modularità**: puoi **cambiare un livello senza toccare gli altri** (es. passare da Wi-Fi a Ethernet senza che il browser se ne accorga).

2. L'**incapsulamento** è il meccanismo per cui, mentre i dati **scendono** la pila, ogni livello **aggiunge la sua "busta"** (l'**header**, l'intestazione con le info di servizio che servono a quel livello) attorno ai dati del livello sopra. Mentre i dati **risalgono** la pila dall'altra parte, ogni livello **toglie** il suo header e passa il contenuto al livello superiore.

3. **ISO/OSI** (ISO = *International Organization for Standardization*, OSI = *Open Systems Interconnection*) è il **riferimento teorico** a **7 livelli** (fisico, data link, rete, trasporto, sessione, presentazione, applicazione). **TCP/IP** (*Transmission Control Protocol / Internet Protocol*) è il modello **realmente usato da Internet**, a **4-5 livelli** (accesso alla rete, internet, trasporto, applicazione). In OSI i tre livelli alti diventano l'unico "applicazione" di TCP/IP, e i due bassi diventano "accesso alla rete".

4. **IP (Internet Protocol)** si occupa di **indirizzamento** (ogni host ha un **indirizzo IP**) e **instradamento** (i **router** decidono su quale strada inoltrare i **pacchetti** verso la destinazione) tra reti diverse. **Best-effort** significa che IP **fa del suo meglio ma non garantisce nulla**: un pacchetto può perdersi, duplicarsi o arrivare fuori ordine. L'affidabilità, se serve, la aggiunge il livello di trasporto sopra.

5. **TCP** è orientato alla connessione e **affidabile**: garantisce che i dati arrivino tutti, integri e in ordine (numera, conferma con ACK, ritrasmette i persi, riordina), con controllo di flusso e congestione; ma è più "pesante". **UDP** è senza connessione e **non affidabile**: niente handshake né ritrasmissioni, quindi veloce e leggero. Esempi: **TCP** per web e trasferimento file; **UDP** per streaming, gaming, DNS e videochiamate.

6. Il **three-way handshake** apre una connessione TCP con tre messaggi: (1) **SYN** — il client chiede di aprire la connessione (*synchronize*); (2) **SYN-ACK** — il server accetta (SYN suo) e conferma (**ACK**, *acknowledgment*, conferma di ricezione) quello del client; (3) **ACK** — il client conferma a sua volta. Dopo i tre messaggi la connessione è stabilita. È un round-trip speso **prima** di inviare dati utili.

7. Il **DNS (Domain Name System)** è la "**rubrica di Internet**": **traduce un nome** (es. `www.glacom.ai`) **nel corrispondente indirizzo IP** numerico. Serve perché i router instradano solo verso indirizzi IP, mentre gli umani ricordano i nomi.

8. **TLS (Transport Layer Security)** **cifra la connessione**: garantisce **cifratura** (traffico illeggibile a chi intercetta), **integrità** (dati non alterati) e **autenticazione** del server (tramite **certificati**). È la "**s**" di **HTTPS**: HTTPS è HTTP fatto viaggiare dentro un canale TLS. (Evoluzione del vecchio SSL.)

9. Una **porta** è un numero che **identifica l'applicazione (il processo) su un host**. Serve perché l'indirizzo IP ti porta al **computer** giusto, ma dentro quel computer girano tanti programmi: la porta dice **a quale** consegnare i dati (es. 80 = HTTP, 443 = HTTPS, 53 = DNS).

10. Aprendo `https://...`: (1) **DNS** risolve il nome nell'**indirizzo IP** del server; (2) **TCP** apre la connessione con il **three-way handshake** (sulla porta 443); (3) **TLS** cifra il canale con il suo handshake (scambio di certificato e chiavi); (4) **HTTP** manda la **richiesta** (es. GET `/`); (5) i dati **scendono la pila** (incapsulamento: messaggio → segmento → pacchetto → frame), viaggiano come **pacchetti IP** tra i router e **risalgono** la pila dall'altra parte; (6) il server manda la **risposta HTTP**, che rifà il viaggio a ritroso e il browser mostra la pagina.

</details>
