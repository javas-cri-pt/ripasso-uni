---
day: 44
topic_id: xc-sd-micro
title: "Microservizi vs monolite, API gateway"
area: cross-cutting
course: "System Design"
grounded_in: null
adjacent: [se-arch, xc-api-rest, xc-sd-basics]
completeness_checked: true
quiz_count: 10
---

# Microservizi vs monolite, API gateway

> **Perché oggi:** "monolite o microservizi?" è la domanda architetturale che più spesso rivela se un candidato ragiona per mode o per trade-off. La risposta giusta quasi mai è "microservizi perché sono moderni": è "dipende da quante persone lavorano al codice, da quanto il sistema deve scalare a pezzi e da quanto puoi permetterti la complessità operativa". Oggi definiamo con precisione cosa sono le due architetture, perché i microservizi risolvono certi problemi creandone altri, e cosa fa il componente che li tiene insieme verso l'esterno: l'**API gateway**. Nel tema `se-arch` hai visto gli stili architetturali in generale; qui li mettiamo alla prova della scala.

## Il monolite: tutto in un'unica applicazione
Un'architettura **monolitica** mette tutto il codice applicativo in **un solo programma distribuibile**: interfaccia, logica di business e accesso ai dati vivono nello stesso processo e si distribuiscono come un unico artefatto (un solo `.jar`, una sola immagine, un solo deploy). Non significa "codice disordinato": un monolite può essere benissimo organizzato in moduli puliti.
- **Pro:** semplice da sviluppare all'inizio, da testare (tutto gira in locale), da distribuire (un deploy solo) e da debuggare (una chiamata tra due funzioni è una chiamata in memoria, non in rete). Le **transazioni** che toccano più parti del dominio sono facili perché c'è un solo database.
- **Contro:** cresce male oltre una certa dimensione. Un piccolo cambiamento impone di ricompilare e ridistribuire **tutto**; un bug di memoria in un modulo può far cadere l'intera applicazione; non puoi scalare **solo** la parte sotto stress, devi replicare tutto il monolite; e sopra un certo numero di sviluppatori il repository unico diventa un collo di bottiglia di merge e coordinamento.

Variante matura e sottovalutata: il **monolite modulare (modular monolith)**, un singolo deploy ma con confini interni netti tra moduli. Ti dà ordine senza la complessità di rete dei microservizi, ed è spesso il punto di partenza giusto.

## I microservizi: tante applicazioni piccole e indipendenti
In un'architettura a **microservizi** l'applicazione è spezzata in **tanti servizi piccoli e autonomi**, ognuno responsabile di una **singola capacità di business** (es. "catalogo", "pagamenti", "spedizioni"), ognuno con il **proprio processo**, il **proprio database** e il **proprio ciclo di deploy**. Comunicano tra loro **via rete** attraverso interfacce ben definite.

I due principi che li reggono:
- **Un servizio = un bounded context.** Il **bounded context** è un concetto del Domain-Driven Design: un confine dentro il quale un modello del dominio è coerente e i termini hanno un significato preciso. Tagliare i servizi lungo i bounded context (per **capacità di business**) e non lungo gli strati tecnici è la regola d'oro. Tagliare male è la causa numero uno dei fallimenti.
- **Database per servizio (database per service).** Ogni servizio possiede i **suoi** dati e nessun altro ci accede direttamente: si chiede il dato **all'API** del servizio proprietario. Questo garantisce il vero disaccoppiamento ma è anche la fonte dei problemi più duri (le transazioni distribuite, sotto).

Vantaggi concreti: **deploy indipendenti** (aggiorni il servizio pagamenti senza toccare il catalogo), **scalabilità selettiva** (dai più repliche solo al servizio sotto carico), **isolamento dei guasti** (se cade un servizio secondario il resto regge, se ben progettato), **team autonomi** (ogni team possiede i suoi servizi, scala organizzativamente), e **libertà tecnologica** (un servizio in Python, un altro in Go).

## Il prezzo dei microservizi: la complessità si sposta, non sparisce
Qui sta il cuore di un buon ragionamento da colloquio: i microservizi non eliminano la complessità, la **spostano dal codice all'infrastruttura e alla rete**.
- **La rete è inaffidabile.** Una chiamata che nel monolite era in memoria ora è una chiamata di rete: può essere lenta, fallire, andare in timeout. Servono **retry**, **timeout** e il **circuit breaker** (interruttore): un meccanismo che, dopo troppi errori verso un servizio, smette temporaneamente di chiamarlo e risponde subito con un fallback, evitando che il guasto si propaghi a cascata (**cascading failure**).
- **Le transazioni distribuite sono difficili.** Senza un unico database, un'operazione che attraversa più servizi (es. "prenota volo e hotel insieme") non può usare una transazione ACID classica. Si usa il **saga pattern**: una sequenza di transazioni locali, ciascuna nel suo servizio, con **azioni di compensazione** che annullano i passi precedenti se uno fallisce (consistenza eventuale invece di atomicità).
- **Osservabilità più dura.** Una richiesta attraversa molti servizi: per capire cosa è andato storto serve il **distributed tracing** (seguire una richiesta tra i servizi con un id di correlazione) oltre a log e metriche centralizzati.
- **Il distributed monolith, l'anti-pattern da evitare.** Se spezzi in servizi ma restano così accoppiati da non poter essere deployati da soli (ogni rilascio ne tocca cinque insieme), hai il peggio dei due mondi: la complessità di rete dei microservizi senza l'indipendenza che li giustifica.

Conseguenza pratica, ed è la tesi di Martin Fowler ("Monolith First"): **inizia monolite** (meglio se modulare) e spezza in microservizi **solo quando** un problema concreto lo richiede (il team è troppo grande per un repo solo, una parte deve scalare in modo molto diverso dal resto). Spezzare troppo presto è un errore costoso.

## L'API gateway: la porta d'ingresso unica
Con decine di servizi, non puoi esporre ognuno direttamente ai client (app, browser): dovrebbero conoscere decine di indirizzi, gestire l'autenticazione con ciascuno e soffrire ogni refactoring interno. L'**API gateway** è un singolo punto d'ingresso che sta davanti ai microservizi e instrada ogni richiesta esterna verso il servizio giusto. È l'applicazione del **reverse proxy** al mondo dei microservizi. Responsabilità tipiche, centralizzate così da non ripeterle in ogni servizio:
- **Routing:** `/ordini/*` va al servizio ordini, `/pagamenti/*` al servizio pagamenti.
- **Autenticazione e autorizzazione:** valida il token una volta all'ingresso, così i servizi dietro si fidano. Vedi `xc-api-rest` e `sec-auth`.
- **Rate limiting** e protezione: limita quante richieste un client può fare, taglia il traffico abusivo.
- **Aggregazione:** una richiesta del client può diventare più chiamate interne, raccolte in un'unica risposta, così il client fa un round-trip solo.
- **Cross-cutting concerns:** terminazione TLS, logging, metriche, caching delle risposte, trasformazione di formato.

Una variante importante è il **BFF (Backend for Frontend):** un gateway dedicato per ciascun tipo di client (uno per l'app mobile, uno per il web), così ognuno riceve esattamente i dati nella forma che gli serve, senza appesantire un gateway generico. Da non confondere con due componenti vicini: il **service discovery** (come i servizi trovano gli indirizzi attuali degli altri, che cambiano di continuo in ambienti dinamici) e il **service mesh** (gestisce la comunicazione **tra** servizi interni, con sidecar che fanno retry, mTLS e tracing, mentre il gateway gestisce il traffico **dall'esterno**, detto north-south).

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 700 320" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="150" y="20" font-weight="700">Monolite</text>
    <rect x="60" y="34" width="180" height="150" rx="10" fill="var(--card)" stroke="var(--rule)"/>
    <rect x="80" y="50" width="140" height="28" rx="5" fill="var(--card2)" stroke="var(--rule)"/><text x="150" y="68" font-size="10.5">UI</text>
    <rect x="80" y="84" width="140" height="28" rx="5" fill="var(--card2)" stroke="var(--rule)"/><text x="150" y="102" font-size="10.5">Logica di business</text>
    <rect x="80" y="118" width="140" height="28" rx="5" fill="var(--card2)" stroke="var(--rule)"/><text x="150" y="136" font-size="10.5">Accesso dati</text>
    <ellipse cx="150" cy="168" rx="38" ry="12" fill="var(--card2)" stroke="var(--accent)"/><text x="150" y="172" font-size="10">1 DB</text>
    <text x="150" y="202" font-size="10" fill="var(--muted)">un solo deploy</text>
  </g>
  <line x1="300" y1="20" x2="300" y2="300" stroke="var(--rule)"/>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="510" y="20" font-weight="700">Microservizi dietro un API gateway</text>
    <rect x="440" y="40" width="140" height="30" rx="6" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/><text x="510" y="60" font-size="11">API Gateway</text>
    <text x="510" y="86" font-size="9.5" fill="var(--muted)">routing · auth · rate limit</text>

    <rect x="345" y="110" width="95" height="44" rx="8" fill="var(--card2)" stroke="var(--good)" stroke-width="1.5"/><text x="392" y="132" font-size="10.5">Catalogo</text>
    <rect x="462" y="110" width="95" height="44" rx="8" fill="var(--card2)" stroke="var(--good)" stroke-width="1.5"/><text x="509" y="132" font-size="10.5">Pagamenti</text>
    <rect x="580" y="110" width="95" height="44" rx="8" fill="var(--card2)" stroke="var(--good)" stroke-width="1.5"/><text x="627" y="132" font-size="10.5">Spedizioni</text>

    <ellipse cx="392" cy="188" rx="30" ry="11" fill="var(--card)" stroke="var(--rule)"/><text x="392" y="192" font-size="9">DB</text>
    <ellipse cx="509" cy="188" rx="30" ry="11" fill="var(--card)" stroke="var(--rule)"/><text x="509" y="192" font-size="9">DB</text>
    <ellipse cx="627" cy="188" rx="30" ry="11" fill="var(--card)" stroke="var(--rule)"/><text x="627" y="192" font-size="9">DB</text>
    <text x="510" y="224" font-size="10" fill="var(--muted)">un database per servizio · deploy indipendenti</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none" marker-end="url(#ar2)">
    <path d="M480,70 L400,108"/><path d="M510,70 L509,108"/><path d="M540,70 L620,108"/>
    <path d="M392,154 L392,176"/><path d="M509,154 L509,176"/><path d="M627,154 L627,176"/>
  </g>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
    <text x="350" y="262" font-weight="700">Regola pratica: monolite (meglio modulare) prima; spezzare solo quando un problema concreto lo chiede</text>
    <text x="350" y="286" font-size="10.5" fill="var(--muted)">la complessità si sposta dal codice alla rete: retry, circuit breaker, saga, tracing</text>
  </g>
  <defs>
    <marker id="ar2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="var(--muted)"/></marker>
  </defs>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">A sinistra il monolite: UI, logica e dati in un unico deploy su un solo database. A destra i microservizi: ogni servizio ha il suo database e si distribuisce da solo, con un API gateway come porta d'ingresso unica che fa routing, autenticazione e rate limiting.</figcaption>
</figure>

## Esempi concreti
- **Startup al primo prodotto (pochi sviluppatori, requisiti ancora in movimento):** monolite, quasi sempre. Il dominio non è ancora stabile, quindi non sai nemmeno dove tagliare i confini; spezzare ora significa indovinare male e pagare continui refactoring tra servizi. Un monolite modulare ben organizzato ti dà già moduli puliti pronti a diventare servizi in futuro.
- **E-commerce maturo con picchi stagionali:** qui i microservizi ripagano. Nel Black Friday il servizio **pagamenti** e **catalogo** vanno sotto stress mille volte più del servizio **recensioni**: scali selettivamente solo quelli, risparmiando risorse. E team diversi rilasciano in autonomia più volte al giorno.
- **Un cambiamento che tocca più servizi:** se per aggiungere un campo "note di consegna" devi modificare e ridistribuire ordini, spedizioni e notifiche **insieme**, è un segnale che i confini sono sbagliati (distributed monolith): quella responsabilità andrebbe concentrata in un solo servizio.

## Notable use case
- **Amazon** a metà anni 2000 passò da un grande monolite a centinaia di servizi, introducendo la regola delle "**two-pizza team**" (team abbastanza piccoli da sfamarsi con due pizze), ognuno padrone dei propri servizi: fu una scelta tanto organizzativa quanto tecnica.
- **Netflix** è il caso di scuola dei microservizi su cloud, con centinaia di servizi, un API gateway (Zuul) e strumenti di resilienza (Hystrix per il circuit breaker) nati proprio lì e diventati standard di settore.
- **Uber** partì monolite e migrò a microservizi crescendo, arrivando poi a consolidare i troppi servizi in "domini" più grossi: la prova che anche lo spezzettamento ha un punto di ritorno.
- **Shopify** è il contro-esempio virtuoso: regge un enorme volume restando in larga parte un **monolite modulare** (Ruby on Rails) con confini interni netti, a dimostrazione che "grande scala" non implica automaticamente "microservizi".

## Fonti
- **Sam Newman, _Building Microservices_** — il riferimento pratico su come e quando spezzare
- **Martin Fowler** — gli articoli "Microservices", "MonolithFirst" e "Microservice Premium" su martinfowler.com
- **Chris Richardson, microservices.io** — catalogo dei pattern (API Gateway, Saga, Database per Service, Circuit Breaker)
- **Eric Evans, _Domain-Driven Design_** — l'origine del concetto di bounded context

## Concetti adiacenti
- `se-arch` — gli stili architetturali (layered, MVC, client-server, broker, microservizi) visti dal lato ingegneria del software
- `xc-api-rest` — come si progettano le interfacce che i servizi espongono e che il gateway instrada
- `xc-sd-basics` — load balancer, caching e scalabilità: il reverse proxy e il bilanciamento che stanno sotto l'API gateway

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cosa distingue un'architettura monolitica da una a microservizi in termini di deploy e database?
2. Elenca due vantaggi concreti del monolite e due suoi limiti quando il sistema cresce.
3. Cos'è un monolite modulare e perché è spesso il punto di partenza giusto?
4. Cosa significa "un servizio = un bounded context" e perché tagliare per capacità di business (non per strato tecnico) è la regola d'oro?
5. Cosa impone il principio "database per servizio" e quale problema introduce?
6. Cos'è un circuit breaker e quale guasto previene?
7. Perché nei microservizi non puoi usare una transazione ACID classica tra servizi, e cosa usi al suo posto?
8. Cos'è un "distributed monolith" e perché è il peggio dei due mondi?
9. Elenca quattro responsabilità tipiche di un API gateway.
10. Qual è la differenza tra un API gateway e un service mesh? E cos'è un BFF?

<details><summary>Risposte</summary>

1. Il **monolite** è un unico programma distribuito come un solo artefatto, con un solo database. I **microservizi** sono tanti servizi autonomi, ognuno con il proprio processo, il **proprio database** e il **proprio ciclo di deploy indipendente**, che comunicano via rete.
2. **Vantaggi:** semplice da sviluppare/testare/distribuire/debuggare; transazioni facili (un solo DB). **Limiti:** un piccolo cambiamento impone di ridistribuire tutto e non puoi scalare solo la parte sotto stress; sopra un certo numero di sviluppatori il repo unico diventa un collo di bottiglia.
3. È un **singolo deploy** con confini interni netti tra moduli: dà ordine e separazione senza la complessità di rete dei microservizi, e lascia i moduli pronti a diventare servizi se e quando servirà.
4. Un **bounded context** è il confine entro cui un modello del dominio è coerente. Tagliare i servizi lungo le **capacità di business** mantiene ogni servizio coeso e autonomo; tagliare per strato tecnico crea servizi che devono cambiare tutti insieme a ogni funzionalità (accoppiamento), causa principale dei fallimenti.
5. Impone che ogni servizio possieda i **suoi** dati e che nessun altro vi acceda direttamente: si chiede il dato all'**API** del proprietario. Introduce il problema delle **transazioni distribuite**, non più risolvibili con una singola transazione ACID.
6. Un **circuit breaker** (interruttore) smette temporaneamente di chiamare un servizio dopo troppi errori e risponde subito con un fallback. Previene il **cascading failure**, cioè la propagazione a catena di un guasto da un servizio a quelli che lo chiamano.
7. Perché non c'è un unico database su cui aprire la transazione: i dati sono sparsi tra servizi. Si usa il **saga pattern**, una sequenza di transazioni locali con **azioni di compensazione** che annullano i passi precedenti se uno fallisce (consistenza eventuale).
8. È un sistema spezzato in servizi che però restano così accoppiati da **non poter essere deployati da soli** (ogni rilascio ne tocca diversi insieme): paghi la complessità di rete dei microservizi senza ottenere l'indipendenza che li giustifica.
9. Routing verso il servizio giusto; autenticazione/autorizzazione centralizzata; rate limiting e protezione; aggregazione di più chiamate interne in una risposta (più: TLS, logging, caching).
10. L'**API gateway** gestisce il traffico **dall'esterno** verso i servizi (north-south): routing, auth, rate limiting. Il **service mesh** gestisce la comunicazione **tra** servizi interni (retry, mTLS, tracing via sidecar). Un **BFF (Backend for Frontend)** è un gateway dedicato a un tipo di client (mobile, web), che gli serve i dati nella forma esatta che gli serve.
</details>

## Esercizi
1. **Monolite o microservizi? Decidi e giustifica tre scenari.** Per ognuno scegli l'architettura e scrivi due righe di motivazione: (a) due fondatori che costruiscono l'MVP di una nuova app, dominio ancora incerto; (b) un'azienda con 120 sviluppatori su un prodotto maturo, in cui il modulo di ricerca va scalato 50 volte più del resto; (c) un gestionale interno usato da 30 persone, carico stabile e basso.
2. **Taglia i confini.** Un e-commerce ha queste responsabilità: autenticazione utenti, catalogo prodotti, carrello, pagamenti, spedizioni, recensioni, notifiche email. Proponi una divisione in microservizi (quali servizi, perché proprio quelli) e indica quale operazione richiederà una **saga** perché attraversa più servizi.
3. **Progetta l'API gateway.** Per l'e-commerce dell'esercizio 2, elenca cosa metti **nel gateway** e cosa lasci **dentro i singoli servizi**, spiegando il criterio con cui decidi dove va ciascuna responsabilità (auth, validazione dei dati di dominio, rate limiting, logica di prezzo, TLS).

<details><summary>Soluzioni</summary>

1. (a) **Monolite (modulare).** Il dominio è incerto: spezzare ora significa sbagliare i confini e pagare refactoring continui tra servizi; il team è minuscolo e non ha bisogno di deploy indipendenti. (b) **Microservizi**, almeno per isolare la **ricerca**: 120 sviluppatori beneficiano di deploy e team autonomi, e la ricerca che scala 50x va scalata **da sola** senza replicare tutto il resto. (c) **Monolite.** Carico basso e stabile, pochi utenti, nessuna esigenza di scalabilità selettiva: i microservizi aggiungerebbero solo complessità operativa senza benefici.
2. Divisione sensata, **una per capacità di business**: `auth`, `catalogo`, `carrello`, `pagamenti`, `spedizioni`, `recensioni`, `notifiche`. Ognuno possiede i propri dati (il carrello non legge direttamente dal DB del catalogo, lo chiede via API). L'operazione che richiede una **saga** è il **checkout**: attraversa carrello → pagamenti → spedizioni (riserva stock) → notifiche. Se il pagamento riesce ma la spedizione non trova stock, le azioni di **compensazione** rimborsano il pagamento e liberano il carrello, perché non esiste una transazione ACID unica su database diversi.
3. **Nel gateway** (cross-cutting, uguale per tutti i servizi): terminazione **TLS**, **autenticazione** (valida il token una volta all'ingresso), **rate limiting**, routing, logging/metriche di base. **Dentro i servizi** (logica di dominio, specifica di ognuno): la **validazione dei dati di dominio** (il servizio pagamenti sa quali importi sono validi, il gateway no) e la **logica di prezzo/sconti** (regole di business del catalogo/carrello). Criterio: nel gateway va ciò che è **trasversale e indipendente dal dominio**; nei servizi va ciò che richiede **conoscenza del dominio specifico**. L'**autorizzazione** fine (questo utente può modificare *questo* ordine?) spesso resta nel servizio, mentre quella grossolana (token valido, scope presente) sta nel gateway.
</details>
