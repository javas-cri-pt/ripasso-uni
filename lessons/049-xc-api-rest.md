---
day: 49
topic_id: xc-api-rest
title: "API: REST, GraphQL, versioning, idempotenza, auth"
area: cross-cutting
course: "API Design"
grounded_in: null
adjacent: [web-http, sec-auth, xc-sd-micro]
completeness_checked: true
quiz_count: 10
---

# API: REST, GraphQL, versioning, idempotenza, auth

> **Perché oggi:** un'**API** è il contratto con cui due software si parlano, ed è la superficie che un backend espone al mondo. In un colloquio "progettami l'API per X" è un classico, e si valuta non tanto se conosci la sintassi ma se sai scegliere i verbi giusti, rendere le operazioni sicure da ripetere (**idempotenza**), far evolvere il contratto senza rompere chi lo usa (**versioning**) e proteggerlo (**auth**). Nel tema `xc-sd-micro` hai visto che i servizi comunicano via API instradate da un gateway: oggi guardiamo *dentro* quelle API. Nel tema `web-http` c'è il protocollo HTTP sotto; qui lo usiamo per progettare bene.

## Cos'è un'API e cosa vuol dire REST
Un'**API (Application Programming Interface)** è un insieme di regole e punti di accesso (**endpoint**) con cui un programma offre le sue funzionalità ad altri programmi. Quando viaggia su HTTP ed espone dati sul web, lo stile dominante è **REST**.

**REST (REpresentational State Transfer)** è uno stile architetturale, non un protocollo: un insieme di principi per progettare API su HTTP. I capisaldi:
- **Tutto è una risorsa, identificata da una URL.** Una **risorsa** è un'entità del dominio (un utente, un ordine) indirizzata da un URL con **sostantivi al plurale**, non verbi: `/ordini`, `/ordini/42`. Si scrive `/ordini/42`, mai `/getOrdine?id=42`.
- **I verbi sono i metodi HTTP**, non parte dell'URL. L'azione la esprime il **metodo** della richiesta (sotto).
- **Stateless (senza stato):** ogni richiesta porta con sé tutto il necessario per essere capita (incluse le credenziali); il server non conserva lo stato della conversazione tra una richiesta e l'altra. Questo rende l'API facile da scalare in orizzontale (qualunque server può gestire qualunque richiesta).
- **Rappresentazioni:** la stessa risorsa può essere restituita in formati diversi (oggi quasi sempre **JSON**), negoziati via header.

### I metodi HTTP e le due proprietà che contano
A ogni operazione corrisponde un **metodo HTTP**:
- **GET** — leggi una risorsa. Non la modifica.
- **POST** — crea una nuova risorsa (o avvia un'azione).
- **PUT** — sostituisce **per intero** una risorsa esistente (o la crea a un id noto).
- **PATCH** — modifica **parziale** di una risorsa (solo alcuni campi).
- **DELETE** — rimuove una risorsa.

Due proprietà classificano questi metodi, e sono il concetto più frainteso delle API.
- **Safe (sicuro):** un metodo è *safe* se **non modifica** lo stato del server. GET è safe: puoi chiamarlo mille volte senza effetti.
- **Idempotente:** un metodo è **idempotente** se eseguirlo **più volte** produce lo **stesso effetto** che eseguirlo una volta sola. Attenzione: non significa "stessa risposta", ma "stesso effetto sullo stato del server".

| Metodo | Safe | Idempotente | Perché |
|---|---|---|---|
| GET | sì | sì | non cambia nulla |
| PUT | no | **sì** | metti la risorsa in uno stato preciso: rifarlo la lascia lì |
| DELETE | no | **sì** | cancellare una cosa già cancellata lascia lo stato "assente" |
| PATCH | no | dipende | idempotente se imposta valori assoluti, non se incrementa |
| **POST** | no | **no** | ogni chiamata **crea una nuova** risorsa |

### Perché l'idempotenza è vitale (e come si rende POST sicuro)
La rete è inaffidabile: un client manda una richiesta, non riceve risposta (timeout), e **non sa** se è arrivata. Se riprova, con un metodo idempotente non fa danni; con POST invece rischia di creare **due** ordini, **addebitare due volte** un pagamento. Per questo i POST critici si rendono sicuri con una **idempotency key**: il client genera un identificativo univoco (es. un UUID) e lo manda in un header (`Idempotency-Key`); il server registra quella chiave e, se arriva una seconda richiesta con la **stessa** chiave, **non** riesegue di nuovo l'operazione ma restituisce il risultato della prima. È esattamente il meccanismo che usano i sistemi di pagamento. Dirlo a un colloquio su un endpoint di pagamento fa la differenza.

### Gli status code: il linguaggio delle risposte
REST usa i **codici di stato HTTP** per dire com'è andata, raggruppati per centinaia:
- **2xx — successo:** `200 OK`, `201 Created` (dopo un POST che ha creato qualcosa), `204 No Content` (successo senza corpo, tipico del DELETE).
- **3xx — redirezione.**
- **4xx — errore del client:** `400 Bad Request` (dati malformati), `401 Unauthorized` (non autenticato, "chi sei?"), `403 Forbidden` (autenticato ma non autorizzato, "non puoi"), `404 Not Found`, `409 Conflict`, `429 Too Many Requests` (rate limit superato).
- **5xx — errore del server:** `500 Internal Server Error`, `503 Service Unavailable`.
Usare lo status giusto è parte del contratto: un client deve poter distinguere "ho sbagliato io" (4xx, non ritentare uguale) da "problema tuo" (5xx, forse ritentabile).

## GraphQL: un'alternativa quando le forme dei dati variano
**GraphQL** è un linguaggio di query per API, nato in Facebook, con un approccio diverso: invece di tante URL (una per risorsa), c'è **un solo endpoint** a cui il client manda una **query** che descrive **esattamente** i campi che vuole; il server risponde con quella forma e nient'altro. Risolve due problemi tipici di REST:
- **Over-fetching:** con REST `/utenti/42` ti dà *tutto* l'utente anche se ti serve solo il nome. GraphQL chiede solo `{ nome }`.
- **Under-fetching (e l'N+1):** con REST per avere un utente e i suoi ordini servono più chiamate (`/utenti/42`, poi `/utenti/42/ordini`); GraphQL le unisce in **una** query annidata.

Le operazioni GraphQL sono tre: **query** (leggere, come GET), **mutation** (modificare, come POST/PUT/DELETE) e **subscription** (ricevere aggiornamenti in tempo reale). Il prezzo: **caching più difficile** (con REST sfrutti la cache HTTP per URL, con GraphQL no perché è un solo endpoint in POST), rischio di query troppo pesanti da limitare, e maggiore complessità lato server. Regola pratica: **REST** resta l'impostazione predefinita, semplice e cacheable; **GraphQL** conviene quando i client sono molti e diversi e ognuno vuole una fetta diversa degli stessi dati (tipico delle app mobile che vogliono minimizzare il traffico).

## Versioning: far evolvere l'API senza rompere i client
Un'API pubblica è un **contratto**: una volta che altri la usano, non puoi cambiarla a piacere. Una modifica che rompe i client esistenti si chiama **breaking change** (rinominare o togliere un campo, cambiare un tipo, rendere obbligatorio un parametro prima opzionale). Aggiungere un campo nuovo, invece, di solito **non** rompe nessuno. Per introdurre breaking change si **versiona**:
- **Nell'URL (URI versioning):** `/v1/ordini`, `/v2/ordini`. È il metodo più diffuso ed esplicito: chiaro e facile da instradare, al prezzo di URL "meno puri".
- **Nell'header:** il client indica la versione in un header (es. `Accept: application/vnd.api+json;version=2`). URL più pulite ma meno visibile e più difficile da testare al volo nel browser.
Buona pratica: mantieni la vecchia versione attiva per un periodo di **deprecazione** annunciato, così i client migrano senza rotture improvvise.

## Auth: autenticare e autorizzare le chiamate
Siccome REST è stateless, **ogni richiesta** deve portare la prova di identità. I meccanismi principali (approfonditi in `sec-auth`):
- **API key:** una stringa segreta che identifica l'applicazione chiamante, passata in un header. Semplice, adatta a servizio-a-servizio, ma identifica l'app, non il singolo utente, ed è tutta da proteggere.
- **JWT (JSON Web Token):** un token **firmato** dal server che contiene i dati dell'utente (**claim**: id, ruolo, scadenza). Il client lo manda nell'header `Authorization: Bearer <token>`; il server ne verifica la firma **senza** consultare un database (stateless). Vedi `sec-auth` per i dettagli.
- **OAuth 2.0:** non è un modo di fare login, è un **framework di delega dell'autorizzazione**: permette a un'app di accedere a risorse per conto di un utente **senza** conoscerne la password (è il "Accedi con Google"). L'utente autorizza, il provider rilascia un **access token** con **scope** (permessi) limitati, e l'app usa quel token. Distinzione chiave da ripetere a voce: **autenticazione** = "chi sei?" (→ `401` se manca); **autorizzazione** = "cosa puoi fare?" (→ `403` se non basta).

## Altre buone pratiche di un'API ben fatta
- **Paginazione:** non restituire mai liste potenzialmente enormi tutte insieme. O **offset-based** (`?page=2&size=20`, semplice ma instabile se i dati cambiano) o **cursor-based** (`?after=<cursore>`, stabile e più efficiente su grandi dataset).
- **Filtri e ordinamento** via query string: `?stato=pagato&sort=-data`.
- **Rate limiting:** limita le richieste per client e rispondi `429` quando si sfora, proteggendo il servizio da abusi e sovraccarico (spesso nell'API gateway, vedi `xc-sd-micro`).
- **Errori con un corpo utile:** oltre allo status, un JSON che spiega *cosa* è andato storto, in un formato coerente su tutta l'API.
- **HATEOAS** (Hypermedia As The Engine Of Application State): il livello più "puro" di REST, in cui le risposte includono i **link** alle azioni possibili successive. Elegante ma poco usato nella pratica; vale conoscerne il nome.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 700 300" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="175" y="20" font-weight="700">REST: una URL per risorsa</text>
    <rect x="40" y="38" width="270" height="26" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="175" y="55" font-size="10.5">GET /ordini/42 → tutto l'ordine</text>
    <rect x="40" y="70" width="270" height="26" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="175" y="87" font-size="10.5">GET /ordini/42/righe → altra chiamata</text>
    <text x="175" y="116" font-size="10" fill="var(--muted)">semplice, cacheable · rischio over/under-fetching</text>
  </g>
  <line x1="350" y1="20" x2="350" y2="150" stroke="var(--rule)"/>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="525" y="20" font-weight="700">GraphQL: un endpoint, query su misura</text>
    <rect x="390" y="38" width="270" height="58" rx="5" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/>
    <text x="525" y="56" font-size="10">POST /graphql</text>
    <text x="525" y="72" font-size="9.5" fill="var(--muted)">{ ordine(id:42){ totale righe{nome} } }</text>
    <text x="525" y="88" font-size="9.5" fill="var(--muted)">↳ esattamente i campi chiesti, in 1 chiamata</text>
    <text x="525" y="116" font-size="10" fill="var(--muted)">flessibile · caching più difficile</text>
  </g>
  <line x1="40" y1="162" x2="660" y2="162" stroke="var(--rule)"/>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
    <text x="350" y="184" font-weight="700">Idempotenza: ripetere una richiesta non deve duplicare l'effetto</text>
  </g>
  <g font-size="10.5" fill="var(--ink)">
    <rect x="60" y="200" width="250" height="80" rx="8" fill="var(--card2)" stroke="var(--good)" stroke-width="1.5"/>
    <text x="185" y="220" text-anchor="middle" font-weight="600">PUT /ordini/42 (idempotente)</text>
    <text x="185" y="240" text-anchor="middle" fill="var(--muted)">1ª volta: imposta lo stato</text>
    <text x="185" y="258" text-anchor="middle" fill="var(--muted)">2ª volta (retry): stesso stato, nessun danno</text>
    <rect x="390" y="200" width="250" height="80" rx="8" fill="var(--card2)" stroke="var(--rule)"/>
    <text x="515" y="220" text-anchor="middle" font-weight="600">POST /ordini (NON idempotente)</text>
    <text x="515" y="240" text-anchor="middle" fill="var(--muted)">retry senza chiave → crea 2 ordini</text>
    <text x="515" y="258" text-anchor="middle" fill="var(--accent)">fix: Idempotency-Key uguale → 1 solo ordine</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Sopra, REST (una URL per risorsa, cacheable) a confronto con GraphQL (un endpoint, il client chiede i campi esatti). Sotto, l'idempotenza: PUT ripetuto lascia lo stesso stato, mentre un POST ripetuto duplica l'effetto se non si usa una Idempotency-Key.</figcaption>
</figure>

## Esempi concreti
- **Creare un ordine in modo sicuro:** il client fa `POST /ordini` con header `Idempotency-Key: <uuid>`. Se la risposta si perde e il client ritenta con la **stessa** chiave, il server riconosce di aver già creato quell'ordine e restituisce lo stesso `201 Created` con lo stesso id, senza crearne un secondo.
- **Aggiornare un profilo:** per sostituire l'intero profilo usi `PUT /utenti/42` (idempotente, lo stato finale è sempre quello che mandi); per cambiare solo l'email usi `PATCH /utenti/42` con `{ "email": "..." }`, più economico perché non devi rimandare tutto l'oggetto.
- **App mobile che vuole risparmiare traffico:** una schermata profilo mostra nome, foto e numero di ordini. Con REST sarebbero più chiamate o un payload gonfio; con una query GraphQL chiedi quei tre campi e basta, in un round-trip.

## Notable use case
- **Stripe** è il riferimento di settore per le API REST ben progettate: idempotency key su tutte le richieste di creazione, versioning esplicito (ogni account è ancorato a una versione dell'API), errori con corpo strutturato. È l'esempio da studiare per imparare il mestiere.
- **GitHub** offre **sia** REST **sia** GraphQL in parallelo: la REST per la semplicità e la cacheabilità, la GraphQL per lasciare ai client la libertà di chiedere esattamente i dati che servono, riducendo le chiamate.
- **GraphQL in Facebook/Meta** nacque proprio per le app mobile: su reti lente, minimizzare il numero di round-trip e la dimensione dei payload era un vantaggio decisivo.
- **"Accedi con Google/Apple"** è **OAuth 2.0** in azione: deleghi a un provider la verifica dell'identità e l'app riceve un token con scope limitati, senza mai vedere la tua password.

## Fonti
- **Roy Fielding** — la tesi di dottorato (2000) che ha definito REST
- **Documentazione di Stripe e di GitHub** — due esempi reali di API eccellenti da cui copiare le convenzioni
- **MDN Web Docs** — HTTP methods e status code (developer.mozilla.org)
- **graphql.org** e **oauth.net** — le specifiche ufficiali di GraphQL e OAuth 2.0

## Concetti adiacenti
- `web-http` — il protocollo HTTP (metodi, header, status) su cui poggia ogni API REST
- `sec-auth` — sessioni, JWT e OAuth2 spiegati dal lato sicurezza
- `xc-sd-micro` — i microservizi che espongono queste API e l'API gateway che le instrada, autentica e limita

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cosa significa che REST è "resource-oriented"? Come si scrive l'URL per leggere l'ordine 42, e come **non** va scritto?
2. Qual è la differenza tra un metodo "safe" e uno "idempotente"? Fai un esempio per ciascuna proprietà.
3. Perché PUT e DELETE sono idempotenti mentre POST non lo è?
4. Cos'è una idempotency key e quale problema concreto risolve su un endpoint di pagamento?
5. Quando usi `201`, `204`, `401`, `403` e `429`? Spiega la differenza tra 401 e 403.
6. Quali due problemi di REST risolve GraphQL, e qual è il prezzo principale che paghi scegliendolo?
7. Cos'è un "breaking change"? Dai un esempio e uno di modifica che invece non rompe i client.
8. Confronta il versioning nell'URL e nell'header: un pro e un contro di ciascuno.
9. Cos'è OAuth 2.0 e perché "non è un modo di fare login" ma di delegare l'autorizzazione?
10. Differenza tra paginazione offset-based e cursor-based: perché la seconda è più stabile se i dati cambiano?

<details><summary>Risposte</summary>

1. Significa che ogni entità è una **risorsa** indirizzata da una URL con **sostantivi** (plurali), mentre l'azione la esprime il **metodo HTTP**. Si scrive `GET /ordini/42`; **non** si scrive `/getOrdine?id=42` (verbo nell'URL).
2. **Safe** = non modifica lo stato del server (es. GET). **Idempotente** = ripeterlo più volte produce lo stesso **effetto** di farlo una volta (es. PUT, DELETE). Un metodo può essere idempotente senza essere safe (modifica, ma ripeterlo non cambia il risultato).
3. **PUT** mette la risorsa in uno **stato preciso**: rifarlo la lascia nello stesso stato. **DELETE** la rende "assente": ricancellarla la lascia assente. **POST** invece **crea una nuova** risorsa a ogni chiamata, quindi ripeterlo ne crea più d'una.
4. È un identificativo univoco (es. UUID) che il client manda in un header: il server registra la chiave e, se arriva una seconda richiesta con la **stessa** chiave, non riesegue l'operazione ma restituisce il risultato della prima. Su un pagamento evita il **doppio addebito** quando il client ritenta dopo un timeout.
5. `201 Created` dopo un POST che ha creato una risorsa; `204 No Content` per un successo senza corpo (tipico DELETE); `401 Unauthorized` = non autenticato ("chi sei?"); `403 Forbidden` = autenticato ma senza permesso ("non puoi"); `429 Too Many Requests` = rate limit superato.
6. Risolve l'**over-fetching** (REST restituisce tutta la risorsa anche se ne vuoi un campo) e l'**under-fetching** (REST richiede più chiamate per dati collegati). Prezzo principale: il **caching più difficile**, perché è un solo endpoint in POST e non sfrutti la cache HTTP per URL.
7. Un **breaking change** è una modifica che rompe i client esistenti: es. rinominare o togliere un campo, cambiare un tipo, rendere obbligatorio un parametro prima opzionale. **Non** rompe (di solito) **aggiungere** un campo nuovo a una risposta.
8. **URL** (`/v1/ordini`): esplicito, facile da instradare e testare nel browser; contro: URL "meno pure". **Header**: URL pulite; contro: meno visibile e più difficile da testare al volo.
9. **OAuth 2.0** è un framework di **delega dell'autorizzazione**: permette a un'app di accedere a risorse per conto di un utente **senza conoscerne la password**. L'utente autorizza, il provider rilascia un access token con **scope** limitati. Non verifica l'identità per fare login, delega l'accesso a risorse (è il "Accedi con Google").
10. **Offset-based** (`page/size`) salta un numero fisso di righe: se intanto vengono inseriti/cancellati elementi, gli indici slittano e rischi di saltare o ripetere righe. **Cursor-based** usa un **cursore** che punta a un elemento preciso (`after=<cursore>`): resta ancorato a quel punto anche se il dataset cambia, quindi è stabile ed efficiente su grandi volumi.
</details>

## Esercizi
1. **Progetta gli endpoint REST di una risorsa, curando i metodi e l'idempotenza.** Per la risorsa `prenotazione` (di una sala riunioni) definisci gli endpoint per: elencare, leggere una, crearne una, sostituirla interamente, modificarne solo l'orario, cancellarla. Per ciascuno indica **metodo + URL**, lo **status code** di successo e se è **idempotente**. Poi di' quale endpoint proteggeresti con una idempotency key e perché.
2. **Scegli REST o GraphQL per due casi e motiva.** (a) Un'API pubblica per sviluppatori terzi che vogliono integrare il tuo catalogo, con forte esigenza di caching. (b) L'API interna di un'app mobile con cinque schermate molto diverse, ognuna che mostra un sottoinsieme diverso degli stessi dati utente/ordini.
3. **Classifica status code ed errori.** Per ciascuna situazione indica lo **status code** HTTP corretto: (a) il client manda un JSON malformato; (b) il client non ha incluso alcun token; (c) il client ha un token valido ma non è admin e chiede un'azione da admin; (d) il client ha superato il limite di 100 richieste al minuto; (e) il server ha un'eccezione non gestita.

<details><summary>Soluzioni</summary>

1. Schema degli endpoint:
   - Elencare: `GET /prenotazioni` → `200 OK` — **idempotente** (e safe).
   - Leggere una: `GET /prenotazioni/{id}` → `200 OK` — **idempotente** (e safe).
   - Creare: `POST /prenotazioni` → `201 Created` — **non** idempotente (ogni POST crea una nuova prenotazione).
   - Sostituire interamente: `PUT /prenotazioni/{id}` → `200 OK` — **idempotente** (lo stato finale è quello inviato).
   - Modificare solo l'orario: `PATCH /prenotazioni/{id}` con `{ "orario": "..." }` → `200 OK` — **idempotente** perché imposta un valore assoluto (lo sarebbe meno se incrementasse).
   - Cancellare: `DELETE /prenotazioni/{id}` → `204 No Content` — **idempotente** (ricancellare lascia lo stato "assente").
   Proteggerei con **idempotency key** il `POST /prenotazioni`: è l'unico non idempotente, e un retry dopo un timeout rischia di creare due prenotazioni della stessa sala nello stesso slot (doppia prenotazione). Con la chiave, il retry restituisce la prenotazione già creata.
2. (a) **REST**: un'API pubblica con forte esigenza di **caching** beneficia della cache HTTP per URL, della semplicità e della prevedibilità; è anche più facile da documentare e consumare per terzi. (b) **GraphQL**: cinque schermate che vogliono sottoinsiemi diversi degli stessi dati sono il caso d'uso ideale, ogni schermata chiede esattamente i campi che le servono in un round-trip, evitando over/under-fetching e riducendo il traffico mobile.
3. (a) `400 Bad Request` (dati malformati). (b) `401 Unauthorized` (non autenticato). (c) `403 Forbidden` (autenticato ma non autorizzato). (d) `429 Too Many Requests` (rate limit). (e) `500 Internal Server Error` (errore del server).
</details>
