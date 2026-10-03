---
day: 34
topic_id: xc-sd-data
title: "Dati a scala: sharding, replicazione, CAP theorem"
area: cross-cutting
course: "System Design"
grounded_in: null
adjacent: [db-tx, xc-ds-consistency, xc-sd-basics]
completeness_checked: true
quiz_count: 10
---

# Dati a scala: sharding, replicazione, CAP theorem

> **Perché oggi:** nel tema `xc-sd-basics` hai visto come si scala lo strato applicativo (load balancer, cache, CDN): aggiungere server davanti è facile perché sono *stateless*, senza stato. Il database invece lo stato lo custodisce, ed è lì che un sistema va in ginocchio per primo. "Come scali il database quando una macchina sola non basta più?" è la domanda che apre metà dei colloqui di system design. Oggi vediamo le due leve fondamentali, **replicazione** (più copie degli stessi dati) e **sharding** (dati spezzati su più macchine), e il teorema che fissa cosa puoi e cosa non puoi avere quando la rete si rompe: il **CAP theorem**.

## Il punto di partenza: scaling verticale vs orizzontale
Hai due modi di dare più potenza a un database.
- **Scaling verticale (scale up):** compri una macchina più grossa (più CPU, più RAM, dischi più veloci). Semplice e senza cambiare codice, ma ha un tetto fisico e un prezzo che cresce più che linearmente, e resta un **single point of failure**, cioè un unico punto la cui caduta ferma tutto.
- **Scaling orizzontale (scale out):** aggiungi più macchine e distribuisci il carico tra loro. Non ha il tetto del verticale, ma introduce il problema vero di oggi: se i dati stanno su più macchine, come li tieni **coerenti** e come decidi **dove** sta ogni dato? Le risposte sono replicazione e sharding.

Le due tecniche sono ortogonali e in produzione si usano insieme: prima si replica per leggere di più e sopravvivere ai guasti, poi si shard quando nemmeno la singola copia regge il volume.

## Replicazione: più copie degli stessi dati
La **replicazione** consiste nel tenere lo **stesso insieme di dati** su più nodi. Serve a tre cose: **leggere di più** (le letture si spalmano su più copie), **alta disponibilità** (se un nodo cade, un altro ha già i dati) e **vicinanza geografica** (una copia vicina all'utente riduce la latenza). Lo schema più comune è **leader-follower** (detto anche **primary-replica** o master-slave):
- Un nodo è il **leader (primary)**: riceve tutte le **scritture**.
- Gli altri sono **follower (replica)**: ricevono dal leader un flusso di modifiche (il **replication log**) e lo riapplicano per restare allineati. Servono le **letture**.

Il nodo chiave qui è il **replication lag**, cioè il ritardo con cui un follower recepisce una scrittura appena fatta sul leader. Da esso dipende la scelta tra due modalità:
- **Replicazione sincrona:** il leader conferma la scrittura al client solo dopo che (almeno) un follower l'ha ricevuta. Garanzia forte, ma se quel follower è lento o giù la scrittura si blocca.
- **Replicazione asincrona:** il leader conferma subito e propaga dopo. Veloce e resiliente, ma se il leader muore prima di aver propagato, quelle scritture si perdono. È la causa classica del problema "ho appena salvato una cosa, ricarico la pagina e non c'è": hai scritto sul leader e letto da un follower ancora indietro.

Esistono varianti oltre al leader singolo: **multi-leader** (più nodi accettano scritture, utile tra data center diversi, ma apre il problema dei **conflitti** quando lo stesso dato è modificato in due posti) e **leaderless** (ogni replica accetta scritture, usato da Dynamo e Cassandra, con la lettura/scrittura a **quorum** che vedremo sotto).

### Read replica: scalare le letture
Una conseguenza pratica immediata: se la tua app legge molto più di quanto scrive (il caso normale di quasi tutti i prodotti), aggiungi **read replica** e mandi lì le `SELECT`, lasciando al leader solo le scritture. Attenzione al **read-after-write**: subito dopo una scrittura, se l'utente deve rivedere il proprio dato, leggilo dal leader (o da una replica garantita aggiornata), non da una replica qualunque.

## Sharding: spezzare i dati su più macchine
La replicazione non risolve un problema: se il dataset è troppo grande per **stare** su una macchina, o le **scritture** sono troppe per un solo leader, copiarlo di più non aiuta. Serve lo **sharding** (detto anche **partizionamento orizzontale**): dividere i dati in sottoinsiemi disgiunti, gli **shard (partizioni)**, e metterli su macchine diverse. Ogni shard tiene solo una fetta delle righe; insieme ricostruiscono l'intero dataset. "Orizzontale" perché tagli per **righe** (utenti 1-1M su uno shard, 1M-2M su un altro), non per **colonne**.

Il cuore della faccenda è la **shard key (chiave di partizione)**: l'attributo in base al quale decidi su quale shard finisce una riga (es. `user_id`). Da come la scegli dipende tutto. Tre strategie:
- **Range-based (per intervalli):** shard A = id da 1 a 1M, shard B = da 1M a 2M. Ottimo per le **query di intervallo** (tutti gli ordini di gennaio stanno vicini), ma rischia gli **hotspot**: se tutti i nuovi id crescenti finiscono nell'ultimo shard, quello si sovraccarica mentre gli altri dormono.
- **Hash-based (per hash):** applichi una **funzione di hash** alla chiave e usi il risultato per scegliere lo shard. Distribuisce in modo **uniforme** ed evita gli hotspot, ma perde la località: una query di intervallo deve interrogare **tutti** gli shard (**scatter-gather**).
- **Directory-based (per lookup):** una tabella di mapping dice esplicitamente dove sta ogni chiave. Massima flessibilità, ma la tabella diventa essa stessa un componente critico da scalare.

### Il problema del resharding e l'hashing consistente
Con l'hash ingenuo `shard = hash(key) % N` (dove `N` è il numero di shard) c'è una trappola: se aggiungi o togli una macchina, `N` cambia e **quasi tutte** le chiavi vengono rimappate, costringendo a spostare quasi l'intero dataset. La soluzione è l'**hashing consistente (consistent hashing)**: chiavi e nodi si dispongono su un **anello** (un cerchio di valori hash) e ogni chiave va al primo nodo che incontra girando in senso orario. Aggiungere o togliere un nodo sposta **solo** le chiavi del suo tratto di anello, non tutte. È la tecnica usata dai sistemi distribuiti (e dalle cache distribuite) proprio per rendere economico il **resharding**.

### Il prezzo dello sharding
Lo sharding non è gratis, ed è onesto dirlo a voce in un colloquio.
- Le **join** tra righe su shard diversi diventano costose o impossibili: spesso si denormalizza o si fa il join in applicazione.
- Le **transazioni** che toccano più shard richiedono protocolli distribuiti (es. **two-phase commit**, 2PC) lenti e fragili. Vedi `db-tx`.
- Le query che non filtrano per shard key diventano **scatter-gather** su tutti gli shard.
Morale: shard solo quando serve davvero, e scegli la shard key in base alla query più frequente.

## Il teorema CAP
Quando i dati stanno su più nodi che comunicano in rete, prima o poi la rete si rompe: pacchetti persi, un nodo isolato, un data center irraggiungibile. Questo evento si chiama **network partition** (partizione di rete): due gruppi di nodi vivi che non riescono a parlarsi. Il **teorema CAP** (formulato da Eric Brewer) dice che un sistema distribuito può garantire al massimo **due** di queste tre proprietà:
- **C — Consistency (coerenza):** ogni lettura vede l'ultima scrittura confermata, come se ci fosse una sola copia dei dati. (Attenzione: è una nozione diversa dalla "C" di ACID.)
- **A — Availability (disponibilità):** ogni richiesta a un nodo vivo riceve una risposta sensata, senza errori né attese infinite.
- **P — Partition tolerance (tolleranza alle partizioni):** il sistema continua a funzionare anche se la rete tra i nodi si spezza.

La lettura corretta del teorema è questa: in un sistema distribuito reale la **P non è opzionale**, perché le partizioni di rete *accadono* e non puoi decidere di non averle. Quindi la scelta vera, **quando** arriva una partizione, è tra **C e A**:
- **Sistema CP:** di fronte alla partizione sacrifica la disponibilità per non dare dati incoerenti. Il nodo che non è sicuro di avere il dato aggiornato **rifiuta** la richiesta (errore o attesa). Esempio tipico: un sistema bancario, dove preferisci un errore a un saldo sbagliato.
- **Sistema AP:** di fronte alla partizione resta disponibile ma può servire un dato **vecchio**, riconciliando dopo. Esempio tipico: il conteggio dei "mi piace" o un carrello, dove un valore leggermente stantio è accettabile.

### Oltre il CAP: PACELC
Il CAP descrive solo cosa succede **durante** una partizione, che è rara. Il modello **PACELC** completa il quadro: **se c'è una Partizione (P), scegli tra A e C; altrimenti (E, "else"), nel funzionamento normale, scegli tra Latency (L) e Consistency (C)**. Cattura il compromesso quotidiano: anche senza guasti, garantire coerenza forte tra le copie costa **latenza** (devi aspettare che le repliche siano d'accordo), mentre accettare coerenza debole è più veloce.

## ACID vs BASE e i modelli di consistenza
Dalla scelta CAP nascono due filosofie di database.
- **ACID** è l'insieme di garanzie dei database relazionali tradizionali: **Atomicity** (una transazione o si completa tutta o niente), **Consistency** (le regole di integrità restano valide), **Isolation** (transazioni concorrenti non si calpestano), **Durability** (una volta confermata, la scrittura sopravvive ai crash). Priorità alla correttezza. Vedi `db-tx`.
- **BASE** è la filosofia di molti database distribuiti NoSQL che privilegiano A e disponibilità: **Basically Available** (risponde quasi sempre), **Soft state** (lo stato può cambiare da solo mentre si propaga), **Eventual consistency** (coerenza eventuale). La **consistenza eventuale** significa che, se smetti di scrivere, dopo un po' **tutte** le repliche convergono allo stesso valore; nel frattempo puoi leggere valori diversi da nodi diversi.

### I quorum: un cursore tra C e A
Nei sistemi leaderless puoi regolare il compromesso con i **quorum**. Con `N` repliche, imponi che una scrittura sia confermata da `W` nodi e una lettura interroghi `R` nodi. Se vale **`R + W > N`**, l'insieme letto e l'insieme scritto si **sovrappongono** per forza su almeno un nodo, quindi la lettura vede sempre l'ultima scrittura (coerenza forte). Abbassando `W` o `R` guadagni disponibilità e velocità ma perdi la garanzia. È il "cursore" con cui tarare caso per caso.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 700 300" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="175" y="20" font-weight="700">Replicazione (leader-follower)</text>
    <rect x="120" y="36" width="110" height="34" rx="7" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/><text x="175" y="57">Leader (scritture)</text>
    <rect x="35" y="110" width="110" height="32" rx="7" fill="var(--card2)" stroke="var(--rule)"/><text x="90" y="130" font-size="11">Follower 1</text>
    <rect x="205" y="110" width="110" height="32" rx="7" fill="var(--card2)" stroke="var(--rule)"/><text x="260" y="130" font-size="11">Follower 2</text>
    <text x="175" y="162" font-size="10" fill="var(--muted)">replica log → letture (read replica)</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none" marker-end="url(#ar)">
    <path d="M150,70 L105,108"/><path d="M200,70 L245,108"/>
  </g>
  <line x1="360" y1="20" x2="360" y2="200" stroke="var(--rule)"/>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="530" y="20" font-weight="700">Sharding (per shard key)</text>
    <rect x="410" y="36" width="240" height="30" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="530" y="56" font-size="11">router: shard = f(shard key)</text>
    <rect x="410" y="100" width="70" height="60" rx="7" fill="var(--card2)" stroke="var(--good)" stroke-width="1.6"/><text x="445" y="126" font-size="11">Shard A</text><text x="445" y="144" font-size="9.5" fill="var(--muted)">id 1–1M</text>
    <rect x="495" y="100" width="70" height="60" rx="7" fill="var(--card2)" stroke="var(--good)" stroke-width="1.6"/><text x="530" y="126" font-size="11">Shard B</text><text x="530" y="144" font-size="9.5" fill="var(--muted)">id 1M–2M</text>
    <rect x="580" y="100" width="70" height="60" rx="7" fill="var(--card2)" stroke="var(--good)" stroke-width="1.6"/><text x="615" y="126" font-size="11">Shard C</text><text x="615" y="144" font-size="9.5" fill="var(--muted)">id 2M–3M</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none" marker-end="url(#ar)">
    <path d="M470,66 L450,98"/><path d="M530,66 L530,98"/><path d="M590,66 L612,98"/>
  </g>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
    <text x="350" y="232" font-weight="700">CAP: durante una partizione scegli C oppure A</text>
    <text x="350" y="256" font-size="11" fill="var(--muted)">CP = rifiuta la richiesta per non dare dati vecchi · AP = risponde con dati forse stantii</text>
    <text x="350" y="278" font-size="11" fill="var(--muted)">P (tolleranza alle partizioni) non è opzionale in un sistema distribuito reale</text>
  </g>
  <defs>
    <marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="var(--muted)"/></marker>
  </defs>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">A sinistra la replicazione: un leader riceve le scritture e le propaga ai follower, che servono le letture. A destra lo sharding: un router manda ogni riga allo shard scelto dalla shard key; gli shard tengono fette disgiunte dei dati. In basso il compromesso CAP di fronte a una partizione di rete.</figcaption>
</figure>

## Esempi concreti
- **App che legge molto, scrive poco (blog, catalogo, dashboard):** una sola istanza del DB come leader più due read replica. Le pagine pubbliche leggono dalle replica, l'area admin che salva scrive sul leader e rilegge dal leader per evitare il read-after-write. Nessuno sharding: il dataset sta comodamente su una macchina.
- **Chat o messaggistica con miliardi di messaggi:** qui il volume di scrittura è enorme e serve sharding. Shard key naturale: l'id della conversazione (`conversation_id`), così tutti i messaggi di una chat stanno sullo stesso shard e li leggi con una query locale, senza scatter-gather. L'hash sulla conversazione distribuisce il carico in modo uniforme.
- **Contatore di visualizzazioni di un video virale:** classico caso AP. Mostrare "1.248.000" invece del valore esatto istantaneo non fa male a nessuno; meglio restare disponibili e riconciliare dopo, che bloccare per avere il numero perfetto.

## Notable use case
- **Instagram** partì con PostgreSQL e crebbe tramite **sharding logico**: migliaia di partizioni logiche distribuite su poche macchine fisiche, così da poter spostare partizioni senza rimappare le chiavi (hanno pubblicato lo schema di id che include il numero di shard nell'id stesso).
- **Amazon Dynamo** è il capostipite dei sistemi **AP/leaderless**: hashing consistente sull'anello, scritture sempre accettate, riconciliazione dei conflitti, consistenza eventuale. Da lì discendono **DynamoDB** e **Cassandra**.
- **Google Spanner** è l'eccezione che punta a **C e disponibilità alta insieme** su scala globale, al prezzo di un'infrastruttura di orologi sincronizzati (TrueTime) per ordinare le transazioni: dimostra che il compromesso si sposta con l'ingegneria, non sparisce.
- **MongoDB** e **MySQL/Postgres** offrono read replica integrate e, per Mongo, sharding nativo con shard key dichiarata: gli strumenti di oggi sono standard, non esotici.

## Fonti
- **Martin Kleppmann, _Designing Data-Intensive Applications_** (DDIA) — i capitoli su Replication, Partitioning e Consistency sono il riferimento su questo tema
- **Eric Brewer** — l'articolo originale sul teorema CAP e il ripensamento "CAP Twelve Years Later"
- **Documentazione ufficiale** di PostgreSQL (replication), MongoDB (sharding) e Amazon DynamoDB
- **Il paper di Amazon Dynamo** (2007) — consistent hashing e consistenza eventuale in pratica

## Concetti adiacenti
- `db-tx` — transazioni e ACID: le garanzie che lo sharding rende difficili tra shard diversi
- `xc-ds-consistency` — consistenza, consenso e fault tolerance viste dal lato dei sistemi distribuiti
- `xc-sd-basics` — scalabilità, load balancing e caching: lo strato stateless che si scala prima del DB

## Quiz (10 — tutte rispondibili dalla lezione)
1. Qual è la differenza tra scaling verticale e orizzontale, e perché il verticale lascia comunque un single point of failure?
2. Nello schema leader-follower, chi riceve le scritture e chi serve le letture? Cos'è il replication lag?
3. Spiega la differenza tra replicazione sincrona e asincrona e un rischio concreto di ciascuna.
4. Cos'è una shard key e perché la sua scelta determina se una query diventa scatter-gather?
5. Confronta sharding range-based e hash-based: pro e contro di ciascuno (hotspot e query di intervallo).
6. Perché `hash(key) % N` è problematico quando aggiungi una macchina, e come lo risolve l'hashing consistente?
7. Enuncia il teorema CAP definendo C, A e P. Perché in un sistema distribuito reale la scelta è di fatto tra C e A?
8. Cosa distingue un sistema CP da uno AP di fronte a una partizione di rete? Fai un esempio d'uso per ciascuno.
9. Cosa aggiunge PACELC rispetto al CAP?
10. Cosa significa "consistenza eventuale" e, nei quorum, perché `R + W > N` garantisce di leggere l'ultima scrittura?

<details><summary>Risposte</summary>

1. Il **verticale (scale up)** potenzia una singola macchina; l'**orizzontale (scale out)** aggiunge più macchine. Il verticale resta un **single point of failure** perché i dati stanno tutti su quell'unica macchina: se cade, cade tutto, e c'è comunque un tetto fisico alla sua potenza.
2. Il **leader (primary)** riceve tutte le **scritture**; i **follower (replica)** le ricevono via replication log e servono le **letture**. Il **replication lag** è il ritardo con cui un follower recepisce una scrittura appena fatta sul leader.
3. **Sincrona:** il leader conferma solo dopo che un follower ha ricevuto il dato → garanzia forte, ma se il follower è lento/giù la scrittura si blocca. **Asincrona:** conferma subito e propaga dopo → veloce e resiliente, ma se il leader muore prima di propagare quelle scritture si perdono.
4. La **shard key** è l'attributo che decide su quale shard finisce una riga. Se la query filtra per shard key, va a un solo shard; se filtra per altro, deve interrogarli tutti (**scatter-gather**).
5. **Range-based:** ottimo per query di intervallo (dati vicini stanno vicini), ma rischia **hotspot** se gli id crescenti si concentrano sull'ultimo shard. **Hash-based:** distribuzione **uniforme** che evita gli hotspot, ma perde la località → le query di intervallo diventano scatter-gather.
6. Con `% N`, cambiare `N` rimappa **quasi tutte** le chiavi, costringendo a spostare quasi tutti i dati. L'**hashing consistente** dispone chiavi e nodi su un **anello**: aggiungere/togliere un nodo sposta solo le chiavi del suo tratto, non tutte.
7. **C** = ogni lettura vede l'ultima scrittura; **A** = ogni richiesta a un nodo vivo riceve risposta; **P** = il sistema regge anche se la rete tra i nodi si spezza. In un sistema distribuito reale le partizioni **accadono**, quindi P è obbligatoria e la scelta effettiva, durante la partizione, è tra C e A.
8. **CP:** sacrifica A, **rifiuta** la richiesta pur di non dare dati incoerenti (es. sistema bancario). **AP:** resta disponibile servendo dati forse **vecchi**, riconciliando dopo (es. conteggio dei like o carrello).
9. **PACELC** aggiunge il caso **senza** partizione: in funzionamento normale (E, "else") c'è comunque un compromesso tra **Latency** e **Consistency**, perché garantire coerenza forte costa latenza.
10. **Consistenza eventuale:** se smetti di scrivere, dopo un po' tutte le repliche convergono allo stesso valore; nel frattempo nodi diversi possono dare valori diversi. Con i **quorum**, `R + W > N` forza l'insieme letto e quello scritto a sovrapporsi su almeno un nodo, quindi la lettura include sempre il nodo con l'ultima scrittura.
</details>

## Esercizi
1. **Progetta lo schema di sharding di una piattaforma di messaggistica.** Hai le entità `utente`, `conversazione`, `messaggio`. La query dominante è "dammi gli ultimi 50 messaggi di una conversazione". Scegli la **shard key**, la **strategia** (range o hash) e spiega perché, poi indica quale operazione resta costosa con la tua scelta.
2. **Decidi CP o AP per tre funzionalità.** Per ciascuna, scegli CP o AP e motiva in una riga: (a) il saldo di un conto corrente; (b) il numero di "mi piace" sotto un post; (c) la disponibilità a magazzino dell'ultimo pezzo di un prodotto in vendita.
3. **Taratura dei quorum.** Hai `N = 5` repliche leaderless. Vuoi coerenza forte. Proponi una coppia `(W, R)` che la garantisca e una coppia che privilegi la **velocità delle letture** rinunciando alla garanzia. Giustifica con la regola.

<details><summary>Soluzioni</summary>

1. **Shard key = `conversation_id`**, strategia **hash-based**. Motivo: mettendo tutti i messaggi di una conversazione sullo stesso shard, la query dominante ("ultimi 50 messaggi di una conversazione") si risolve su **un solo shard** senza scatter-gather; l'hash distribuisce le conversazioni in modo uniforme evitando hotspot. L'ordinamento per data dentro lo shard si ottiene con un indice su `(conversation_id, timestamp)`. Operazione che resta **costosa**: una query trasversale come "tutti i messaggi inviati da un certo utente in tutte le sue conversazioni" tocca più shard (scatter-gather), perché l'utente non è la shard key. Un'alternativa è denormalizzare mantenendo una seconda vista shardata per `user_id`.
2. (a) Saldo conto → **CP**: un valore sbagliato è inaccettabile, meglio un errore temporaneo. (b) Like → **AP**: un conteggio leggermente stantio non fa danno, meglio restare disponibili. (c) Ultimo pezzo a magazzino → **CP**: vendere due volte lo stesso pezzo (oversell) è un danno reale, serve coerenza sulla quantità residua.
3. Con `N = 5`: per **coerenza forte** serve `R + W > N`, cioè `R + W ≥ 6`. Una scelta equilibrata è `W = 3, R = 3` (3 + 3 = 6 > 5): ogni lettura interseca ogni scrittura su almeno un nodo. Per **letture veloci** senza garanzia: `W = 5, R = 1` dà letture rapidissime da un solo nodo ma scritture lente, oppure `W = 1, R = 1` (1 + 1 = 2, non > 5): letture e scritture velocissime ma puoi leggere un valore vecchio, cioè solo consistenza eventuale.
</details>
