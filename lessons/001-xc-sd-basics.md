---
day: 1
topic_id: xc-sd-basics
title: "System Design — fondamenti (scalabilità, load balancing, caching, CDN, scaling del DB)"
area: cross-cutting
course: System Design
grounded_in: null   # cross-cutting: non trattato all'uni → costruito da conoscenza + web
adjacent: [cloud-arch, db-index, xc-sd-data, xc-sd-async]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso qui sotto. Nessun acronimo lasciato senza definizione."
---

# System Design — fondamenti

> **Perché oggi:** non l'hai fatto all'uni, ma è **adiacente** (tocca Reti, Sistemi Operativi, Basi di Dati, Cloud) ed è **rilevante per il lavoro** e per i colloqui. L'esempio perfetto di "tangente ma prezioso".

## Il problema che risolve
Un sistema che funziona per 100 utenti spesso si rompe a 100.000: la stessa architettura non regge il carico. **System design** è decidere *come strutturare un sistema perché regga la scala, resti veloce e non cada quando qualcosa si rompe.* Prima un acronimo che useremo: **QPS = Queries Per Second**, richieste al secondo — la misura base del carico.

---

## 1. Scalabilità: verticale vs orizzontale

**Scalare** = aumentare la capacità del sistema. Due modi:

- **Verticale (scale up):** dai alla *stessa* macchina più risorse (CPU, RAM). Semplice (non cambi architettura), ma ha due difetti: c'è un **tetto fisico** (la macchina più grossa che esiste) e resta un **single point of failure** (SPOF) = un unico punto che, se si rompe, butta giù tutto.
- **Orizzontale (scale out):** metti *più* macchine che lavorano in parallelo. Nessun tetto pratico (ne aggiungi altre) e **tolleranza ai guasti** (se una cade, le altre reggono). Il prezzo: devi (a) **distribuire le richieste** tra le macchine (→ load balancer, sezione 2) e (b) gestire lo **stato**.

**Stateless — il concetto chiave.** Un server è *stateless* ("senza stato") se **non tiene in memoria informazioni sull'utente tra una richiesta e l'altra** (es. la sessione di login). Perché conta? Perché con lo scale out una richiesta dell'utente può finire su un server diverso ogni volta: se lo stato fosse nella memoria di *un* server, andrebbe perso. Soluzione: i server restano stateless e lo **stato si mette in uno store condiviso** che tutti raggiungono (una cache tipo Redis, o il database). Così ogni server è **intercambiabile**. Regola pratica dei sistemi moderni: **stateless + scale out**.

---

## 2. Load balancing

Un **load balancer (LB)** è un componente che sta *davanti* a N server e smista ogni richiesta a uno di loro. Fa tre lavori: **spalma il carico**, **toglie dal giro i server morti** (li controlla con degli *health check*, piccole richieste periodiche "sei vivo?"), e permette di **rilasciare nuove versioni senza downtime** (togli un server, aggiorni, rimetti).

**Come sceglie a quale server mandare (gli algoritmi):**
- **Round-robin:** a turno, uno dopo l'altro (server 1, 2, 3, 1, 2, 3…). Semplice; presuppone che i server siano equivalenti.
- **Least-connections:** manda la richiesta al server che in quel momento ha **meno connessioni attive** (cioè il più scarico). Meglio quando le richieste durano tempi molto diversi.
- **IP-hash (sticky sessions):** calcola una funzione (*hash*) sull'IP dell'utente e usa il risultato per scegliere *sempre lo stesso* server per quell'utente. Serve se il server tiene stato locale — ma è una toppa: meglio essere stateless (sez. 1).

**Due livelli di LB (dai livelli di rete che hai visto in Reti):**
- **L4** (livello trasporto, TCP/UDP): smista guardando solo IP e porta. Velocissimo, ma "cieco" al contenuto.
- **L7** (livello applicativo, HTTP): legge la richiesta HTTP, quindi può instradare **per contenuto** (es. `/api/*` a un gruppo di server, `/static/*` a un altro). Più intelligente, un po' più lento.

---

## 3. Caching

**Cache** = una copia dei dati tenuta *vicino e veloce da leggere*, per **non rifare ogni volta un lavoro costoso** (una query pesante, una risposta di un LLM, un calcolo). "Vicino" e "veloce" perché tipicamente la cache sta in RAM (Redis, Memcached), leggere dalla RAM è ordini di grandezza più rapido che interrogare un DB su disco.

**Dove si mette (dal più vicino all'utente al più lontano):** browser → CDN (sez. 4) → **cache applicativa** (Redis/Memcached, condivisa tra i server) → cache interna del DB.

**Il problema vero è l'invalidazione:** quando il dato originale cambia, la copia in cache diventa **vecchia** (*stale*). Chi legge dalla cache rischia un dato non aggiornato. Le tre strategie classiche:
- **TTL (Time To Live):** dai a ogni voce una **scadenza** (es. 60 secondi). Dopo, viene buttata e ricaricata dalla sorgente. Semplice; accetti che il dato possa essere vecchio *al massimo* di quel tempo.
- **Write-through** ("scrivi attraverso"): ogni volta che scrivi un dato, lo scrivi **in cache E nel DB nello stesso momento**. La cache è **sempre fresca**, ma ogni scrittura è un po' più lenta (fa due scritture).
- **Cache-aside** ("cache di lato", la più comune): l'app **legge prima dalla cache**; se il dato c'è (*cache hit*) lo usa; se non c'è (*cache miss*) lo legge dal DB e **riempie la cache** per la prossima volta. Semplice, ma il **primo** accesso è lento (miss) e, se un dato cambia nel DB, la cache può restare vecchia finché non scade il TTL.
- (Cenno: **write-back** = scrivi solo in cache subito e nel DB dopo, in differita. Velocissimo in scrittura, ma se la cache muore prima di scaricare, **perdi dati**. Si usa solo dove la perdita è tollerabile.)

**Hit ratio — la metrica della cache.** È la **frazione di richieste servite dalla cache** invece che dalla sorgente lenta:
> **hit ratio = cache hit / (cache hit + cache miss)**

Esempio: su 100 richieste, 90 trovano il dato in cache (hit) e 10 no (miss) → hit ratio = 90/100 = **0,90 (90%)**. Alto = la cache sta lavorando (meno carico sul DB, meno latenza); basso = la cache serve a poco (dati troppo vari o TTL troppo corto).

---

## 4. CDN (Content Delivery Network)

**CDN** = una **rete di server distribuiti geograficamente** che tengono copie dei contenuti **statici** (immagini, JS, CSS, video) e li servono dal nodo **più vicino** all'utente. Se l'origine è a Francoforte e l'utente a São Paulo, il file arriva dal nodo CDN di São Paulo, non da Francoforte → **meno latenza** (meno strada da fare) e **meno carico sull'origine**. È concettualmente caching, ma su scala **geografica**.

---

## 5. Scaling del database (qui muore quasi sempre il sistema)

Il DB è spesso il **collo di bottiglia**: i server web li scali facilmente, il DB no. Tre rimedi, **in ordine di quando li applichi**:

1. **Indici (index).** Un indice è una **struttura dati aggiuntiva** (di solito un B-tree) che il DB tiene su una colonna per **trovare le righe senza scorrere tutta la tabella**. Senza indice, cercare "utente con email X" su 10 milioni di righe le legge *tutte* (scan completo, lentissimo); con un indice sull'email, ci arriva in pochi passi (come l'indice analitico di un libro). **Primo rimedio, quasi gratis.**
2. **Read-replica (replica di lettura).** Una **copia del database** che riceve in continuazione gli aggiornamenti dal DB principale (*primary*) e serve **solo le letture**. Le app leggono dalle repliche e scrivono sul primary → alleggerisci il primary quando le letture sono molte più delle scritture (il caso tipico). Costo: le repliche sono aggiornate con un **piccolo ritardo** (*replication lag*), quindi una lettura potrebbe non vedere l'ultimissima scrittura.
3. **Sharding (partizionamento).** Quando *un* DB non basta più nemmeno per le scritture, **spezzi i dati su più database** in base a una chiave (*shard key*): es. utenti A-M sul DB 1, N-Z sul DB 2. Ogni shard regge una fetta del carico. Potente ma **complesso** (le query che attraversano più shard diventano difficili) → **ultima spiaggia**, non la prima mossa.

Ecco perché la frase "prima indici e read-replica, poi (se serve) sharding" ha un senso preciso: sono tre rimedi di **costo/complessità crescente**, e li applichi in quest'ordine.

---

## Esempi concreti

**Esempio A — il tuo bot preventivi (Glacom) diventa virale, 500 QPS.** Nell'ordine:
1. App **stateless** dietro **load balancer**, scale out a 3-4 istanze.
2. Le risposte/documenti già generati li **cachi** (cache-aside + TTL): stesso input → stessa risposta, niente ricomputo del LLM.
3. Statici (loghi, template) su **CDN**.
4. Il DB rallenta → **indici** sulle colonne cercate, poi **read-replica** per le letture; **sharding** solo se davvero esplode.

**Esempio B — un feed di notizie letto da tutti (poche scritture, moltissime letture).** Qui il **caching** e le **read-replica** fanno il 90% del lavoro: la stessa home page servita a migliaia di utenti si calcola una volta e si mette in cache (hit ratio altissimo).

**Esempio C — una chat in tempo reale.** Il caching serve meno; contano di più i **WebSocket** (connessione persistente, → topic adiacente `xc-sd-async`) e i server stateless con lo stato della sessione in Redis.

## Case study reale
**Instagram agli inizi:** 3 ingegneri, milioni di utenti. La ricetta era esattamente questa — servizi **stateless** dietro **load balancer**, **caching** aggressivo (Memcached, hit ratio altissimo), **CDN** per le foto, **Postgres con read-replica** e poi sharding. Niente magia: le leve di sopra, applicate nell'ordine giusto.

## Completeness check (integrato da me)
Oltre alle leve: a un colloquio di system design il **metodo** conta quanto le nozioni. Passi: (1) **chiarisci requisiti e stime** (quanti QPS? quanti dati? read-heavy o write-heavy?), (2) disegna lo **schema alto** (client → LB → server → cache → DB), (3) approfondisci i **colli di bottiglia**, (4) discuti i **trade-off**. Non esiste "la" risposta giusta: esistono scelte **motivate** dai trade-off (es. read-replica = scali le letture *ma* accetti replication lag).

## Fonti
- **System Design Primer** — github.com/donnemartin/system-design-primer (riferimento gratuito più usato)
- **Designing Data-Intensive Applications**, Martin Kleppmann (il libro di riferimento su dati/scala)
- **AWS Well-Architected Framework** — aws.amazon.com/architecture/well-architected
- **High Scalability** — highscalability.com (case study reali)

## Concetti adiacenti (dove andare dopo)
- `xc-sd-data` — Dati a scala: sharding, replicazione, **CAP theorem** (collegato a Basi di Dati → transazioni/ACID)
- `xc-sd-async` — Code, messaging, WebSocket (collegato a OS → IPC)
- `cloud-arch` — Architetture cloud e scalabilità
- `db-index` — Indici e ottimizzazione query (approfondimento del punto 5.1)

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cosa significa **QPS**?
2. Scaling **verticale** vs **orizzontale**: definisci entrambi e di' quale tollera il guasto di una macchina, e perché.
3. Cosa vuol dire che un server è **stateless**, e *dove* si mette allora lo stato dell'utente?
4. A cosa serve un **load balancer** e come fa a evitare di mandare richieste a un server morto?
5. Differenza tra load balancer **L4** e **L7**?
6. Algoritmo **round-robin** vs **least-connections**: come scelgono il server?
7. Scrivi la **formula dell'hit ratio** e calcolalo se su 200 richieste 150 sono hit.
8. **Write-through** vs **cache-aside**: come funziona ciascuna e qual è il difetto di ciascuna?
9. Cos'è un **indice** su un database e perché rende le query più veloci?
10. Metti in ordine di **costo/complessità crescente**: sharding, indici, read-replica. Spiega in una riga cosa fa ciascuno.

<details><summary>Risposte</summary>

1. **Queries Per Second**, richieste al secondo: la misura base del carico.
2. **Verticale** = più risorse alla stessa macchina; **orizzontale** = più macchine in parallelo. **L'orizzontale** tollera il guasto: se una macchina cade le altre reggono; la verticale ha un unico punto di guasto (SPOF).
3. Stateless = **non tiene in memoria info sull'utente tra una richiesta e l'altra**. Lo stato si mette in uno **store condiviso** (cache tipo Redis, o il DB), così ogni server è intercambiabile.
4. Smista le richieste tra N server (spalma il carico, deploy senza downtime). Evita i server morti con gli **health check**: controlli periodici "sei vivo?"; se un server non risponde, lo toglie dal giro.
5. **L4** guarda solo IP+porta (livello trasporto): veloce ma cieco al contenuto. **L7** legge l'HTTP (livello applicativo): può instradare per path/header, più intelligente e un po' più lento.
6. **Round-robin**: a turno, uno dopo l'altro. **Least-connections**: al server con **meno connessioni attive** in quel momento (il più scarico).
7. **hit ratio = hit / (hit + miss)**. Con 150 hit su 200 richieste (50 miss): 150/200 = **0,75 (75%)**.
8. **Write-through**: a ogni scrittura scrivi in **cache e DB insieme** → cache sempre fresca, ma scrittura più lenta. **Cache-aside**: leggi dalla cache, se manca (miss) leggi dal DB e riempi la cache → semplice, ma primo accesso lento e dato potenzialmente vecchio fino al TTL.
9. È una **struttura dati aggiuntiva** (B-tree) su una colonna che permette di **trovare le righe senza scorrere tutta la tabella** (come l'indice di un libro): da uno scan completo a pochi passi.
10. In ordine crescente: **indici** (struttura per query veloci, quasi gratis) → **read-replica** (copia del DB che serve le letture, alleggerisce il primary, ha replication lag) → **sharding** (spezzi i dati su più DB per chiave, regge anche le scritture ma è complesso: ultima spiaggia).
</details>
