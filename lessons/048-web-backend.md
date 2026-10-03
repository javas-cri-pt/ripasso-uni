---
day: 48
topic_id: web-backend
title: "Server-side: sessioni, autenticazione, Node/Express"
area: computer-science
course: "Tecnologie Web & Progettazione Applicazioni Web"
grounded_in: null
adjacent: [sec-auth, web-http, sec-crypto]
completeness_checked: true
quiz_count: 10
---

# Server-side: sessioni, autenticazione, Node/Express

> **Perché oggi:** in `web-http` hai visto il protocollo HTTP e il modello client-server. Oggi passi dall'altra parte, al **server-side**: il codice che gira sul server, riceve le richieste, parla col database e decide cosa rispondere. E affronti il problema numero uno di ogni applicazione web: HTTP **non ha memoria** da una richiesta all'altra, eppure l'app deve "ricordarsi" chi sei dopo che hai fatto login. Come? Con sessioni e token. Vediamo il meccanismo, con esempi in **Node.js/Express**, e come si custodisce una password senza mai salvarla in chiaro (tema che riprenderai in `sec-auth` e `sec-crypto`).

## Il problema di fondo: HTTP è stateless
HTTP è un protocollo **stateless** (senza stato): ogni richiesta è indipendente e il server, di per sé, non sa che la richiesta di adesso arriva dallo stesso utente di un minuto fa. È una scelta che rende i server scalabili (una richiesta può andare a qualsiasi macchina), ma crea un problema: dopo che hai fatto login, come fa l'app a riconoscerti nella richiesta successiva senza chiederti di nuovo la password?

La soluzione è far **riportare al client**, a ogni richiesta, una prova di identità. Due famiglie di soluzioni: le **sessioni** (stato sul server) e i **token** (stato dal client). Entrambe poggiano su un veicolo comune, il **cookie**.

## Cookie: il veicolo dello stato
Un **cookie** è una piccola coppia chiave-valore che il server invia al browser con l'header di risposta `Set-Cookie`; il browser la conserva e la **rispedisce automaticamente** a ogni richiesta successiva verso quel sito, nell'header `Cookie`. È il meccanismo che permette al server di ritrovare un filo tra richieste altrimenti scollegate.

I cookie hanno attributi di sicurezza fondamentali:
- **`HttpOnly`:** il cookie non è leggibile dal JavaScript della pagina. Difende dal furto del cookie via **XSS** (Cross-Site Scripting, l'iniezione di script malevolo in una pagina).
- **`Secure`:** il cookie viaggia solo su HTTPS (connessione cifrata), mai in chiaro.
- **`SameSite`:** limita l'invio del cookie quando la richiesta parte da un altro sito. Difende dal **CSRF** (Cross-Site Request Forgery, far compiere al tuo browser azioni non volute su un sito dove sei loggato).

## Sessioni: lo stato vive sul server
Con l'approccio a **sessione**, dopo il login il server crea una **sessione**: un record lato server che contiene i dati dell'utente (chi è, i suoi permessi), identificato da un **session ID** (identificativo di sessione) lungo e casuale. Al client va, dentro un cookie, **solo il session ID**, non i dati. A ogni richiesta il browser rispedisce il cookie, il server legge il session ID, recupera la sessione dalla sua memoria e sa chi sei.

- **Dove vivono le sessioni:** in memoria per esperimenti, ma in produzione in uno **store condiviso** (es. Redis, un database in memoria), così tutti i server dietro il bilanciatore vedono la stessa sessione.
- **Vantaggio:** il server ha il controllo pieno. Per fare **logout** o revocare l'accesso basta **cancellare la sessione** dallo store: il cookie resta nel browser ma non vale più nulla.
- **Svantaggio:** il server deve conservare e cercare lo stato a ogni richiesta (è **stateful**); su larga scala richiede uno store veloce e condiviso.

## Token (JWT): lo stato viaggia col client
Con l'approccio a **token**, dopo il login il server non conserva nulla: emette un **token** firmato e lo consegna al client, che lo rispedisce a ogni richiesta (di solito nell'header `Authorization: Bearer <token>`). Il formato più diffuso è il **JWT (JSON Web Token)**.

Un JWT è composto da tre parti separate da punti, ciascuna codificata in Base64URL (`header.payload.firma`):
- **Header:** dice il tipo e l'algoritmo di firma.
- **Payload:** i **claim**, cioè le affermazioni sull'utente (id, ruolo) e metadati come `exp`, la scadenza. **Attenzione:** il payload è solo **codificato**, non cifrato: chiunque può leggerlo. Non ci si mettono segreti.
- **Firma (signature):** calcolata dal server con una chiave segreta su header+payload. Serve a garantire l'**integrità**: se qualcuno modifica anche un carattere del payload, la firma non torna più e il token viene rifiutato.

Il server, ricevuto un JWT, ne **verifica la firma** con la propria chiave: se è valida e non è scaduto, si fida dei claim **senza interrogare il database**. Qui sta il pregio e il difetto:
- **Vantaggio:** è **stateless**, il server non conserva sessioni; comodo per API distribuite e microservizi.
- **Svantaggio:** la **revoca** è difficile. Un JWT valido resta valido fino alla scadenza anche se vuoi cacciare l'utente, perché il server non tiene una lista. Si mitiga con scadenze **brevi** per il token d'accesso più un **refresh token** a vita più lunga (e revocabile) per ottenerne di nuovi.

Regola pratica: sessioni per le app web classiche (semplici da revocare), JWT per API tra servizi o verso client mobili.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 260" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
    <text x="180" y="18" font-weight="700" font-size="12.5">Sessione (stato sul server)</text>
    <text x="540" y="18" font-weight="700" font-size="12.5">JWT (stato dal client)</text>

    <rect x="36" y="40" width="110" height="34" rx="7" fill="var(--card2)" stroke="var(--rule)"/><text x="91" y="61">Browser</text>
    <rect x="224" y="40" width="110" height="34" rx="7" fill="var(--card2)" stroke="var(--accent)" stroke-width="1.6"/><text x="279" y="61">Server</text>
    <rect x="224" y="150" width="110" height="34" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="279" y="171" font-size="10">Store sessioni</text>

    <text x="180" y="92" font-size="9.5" fill="var(--muted)">Cookie: sid=abc…</text>
    <text x="279" y="120" font-size="9.5" fill="var(--muted)">cerca sid</text>
    <text x="180" y="210" font-size="9" fill="var(--muted)">logout = cancella la sessione</text>

    <rect x="396" y="40" width="110" height="34" rx="7" fill="var(--card2)" stroke="var(--rule)"/><text x="451" y="61">Browser</text>
    <rect x="584" y="40" width="110" height="34" rx="7" fill="var(--card2)" stroke="var(--accent)" stroke-width="1.6"/><text x="639" y="61">Server</text>

    <text x="540" y="92" font-size="9.5" fill="var(--muted)">Authorization: Bearer</text>
    <text x="540" y="106" font-size="9.5" fill="var(--muted)">header.payload.firma</text>
    <rect x="470" y="150" width="140" height="48" rx="7" fill="var(--card)" stroke="var(--good)" stroke-width="1.5"/>
    <text x="540" y="170" font-size="10">verifica firma</text><text x="540" y="186" font-size="9" fill="var(--muted)">niente DB</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none">
    <path d="M146,52 L222,52"/><path d="M279,74 L279,148"/>
    <path d="M506,52 L582,52"/><path d="M639,74 L560,148"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">A sinistra la sessione: il cookie porta solo un session ID, i dati stanno nello store lato server (facile revocare). A destra il JWT: il token autoconsistente viaggia col client, il server ne verifica la firma senza interrogare il database (stateless, ma difficile da revocare).</figcaption>
</figure>

## Come si custodisce una password: hashing + salt
La regola assoluta: **le password non si salvano mai in chiaro**, e nemmeno cifrate (una cifratura si può decifrare). Si salva l'**hash** della password. Un **hash** è il risultato di una funzione a senso unico: dalla password produce una stringa di lunghezza fissa, ma dall'hash **non si può tornare** alla password (vedi `sec-crypto`). Al login si calcola l'hash di ciò che l'utente digita e lo si confronta con quello salvato.

Ma gli hash generici (come SHA-256) sono **troppo veloci**: un attaccante che ruba il database può provarne miliardi al secondo. Due accorgimenti indispensabili:
- **Salt (sale):** una stringa casuale **diversa per ogni utente**, aggiunta alla password prima dell'hash e salvata accanto. Così due utenti con la stessa password hanno hash diversi, e si annullano le **rainbow table** (tabelle precalcolate di hash comuni).
- **Funzione lenta e tarabile:** si usano algoritmi progettati **apposta per essere lenti** e regolabili nel costo, come **bcrypt**, **scrypt** o **Argon2**. Il "fattore di costo" si alza man mano che l'hardware migliora, tenendo l'attacco a forza bruta impraticabile. (bcrypt genera e include il salt da solo.)

## Mettere tutto insieme in Node/Express
**Node.js** è un runtime che esegue JavaScript lato server; **Express** è il framework minimale più diffuso per costruire server web e API in Node. I concetti chiave di Express:
- **Route (rotta):** l'associazione tra un metodo HTTP + un percorso e una funzione che lo gestisce (es. `app.post('/login', ...)`).
- **Middleware:** funzioni che si inseriscono **nella catena** tra la richiesta e la risposta; ognuna può leggere/modificare richiesta e risposta e poi passare alla successiva con `next()`. È il meccanismo con cui si fa parsing del body, logging, e soprattutto **autenticazione**: un middleware che blocca le richieste senza credenziali valide.

Registrazione con hashing (bcrypt):

```js
import bcrypt from 'bcrypt';
app.post('/register', async (req, res) => {
  const { email, password } = req.body;
  const hash = await bcrypt.hash(password, 12); // 12 = fattore di costo
  await db.users.insert({ email, passwordHash: hash });
  res.status(201).json({ ok: true });
});
```

Login con verifica:

```js
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await db.users.findByEmail(email);
  // confronto costante gestito da bcrypt; mai dire se è l'email o la password a sbagliare
  if (!user || !(await bcrypt.compare(password, user.passwordHash)))
    return res.status(401).json({ error: 'Credenziali non valide' });
  req.session.userId = user.id;      // approccio a sessione
  res.json({ ok: true });
});
```

Middleware che protegge le rotte riservate:

```js
function requireAuth(req, res, next) {
  if (!req.session.userId) return res.status(401).json({ error: 'Non autenticato' });
  next(); // autenticato: prosegui
}
app.get('/profilo', requireAuth, (req, res) => res.json({ id: req.session.userId }));
```

Un chiarimento che in colloquio fa la differenza: **autenticazione** ("chi sei?", verificare l'identità) e **autorizzazione** ("cosa puoi fare?", verificare i permessi) sono cose diverse. Il middleware qui sopra autentica; per autorizzare controlleresti anche il **ruolo** dell'utente (tema di `sec-auth`).

## Esempi concreti
- **Carrello che sopravvive al refresh:** aggiungi prodotti, ricarichi la pagina, il carrello è ancora lì. Dietro c'è un cookie che porta il session ID; i prodotti stanno nella sessione lato server.
- **API mobile con JWT:** un'app per smartphone fa login e riceve un JWT con scadenza 15 minuti più un refresh token. A ogni chiamata manda `Authorization: Bearer ...`; il server verifica la firma e risponde senza toccare il database degli utenti. Quando il token scade, l'app usa il refresh token per ottenerne uno nuovo.
- **"Esci da tutti i dispositivi":** con le sessioni è immediato, basta cancellare dallo store tutte le sessioni di quell'utente. Con i soli JWT non si potrebbe, ed è il motivo per cui esistono i refresh token revocabili.

## Notable use case
- Il formato **JWT** è standardizzato nella **RFC 7519** della IETF ed è il mattone di protocolli come **OAuth 2.0** e **OpenID Connect**, usati per il "login con Google/Apple".
- **bcrypt** nasce nel 1999 ed è ancora raccomandato: la sua lentezza regolabile lo ha reso resistente all'aumento della potenza di calcolo per oltre vent'anni; **Argon2** ha vinto nel 2015 la Password Hashing Competition come alternativa moderna.
- **Redis** è lo store di sessioni de facto per le web app a traffico elevato: tiene i session ID in memoria, con lookup in tempo costante.

## Fonti
- **MDN — HTTP cookies** — developer.mozilla.org (Set-Cookie, HttpOnly, Secure, SameSite)
- **Express docs** — expressjs.com (routing, middleware)
- **OWASP — Session Management & Password Storage Cheat Sheets** — cheatsheetseries.owasp.org
- **RFC 7519 — JSON Web Token** — datatracker.ietf.org/doc/html/rfc7519

## Concetti adiacenti
- `web-http` — HTTP e client-server: la base su cui poggia tutto il server-side
- `sec-auth` — autenticazione e autorizzazione a fondo (JWT, OAuth, least-privilege)
- `sec-crypto` — hash, salt e firme: la crittografia dietro password e token

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cosa significa che HTTP è **stateless** e quale problema crea dopo il login?
2. Cos'è un **cookie** e come arriva e torna tra browser e server (quali header)?
3. A cosa servono gli attributi **`HttpOnly`** e **`SameSite`** di un cookie, e da quali attacchi difendono?
4. Nell'approccio a **sessione**, cosa viene salvato sul server e cosa viaggia nel cookie? Perché il logout è semplice?
5. Da quali tre parti è composto un **JWT** e cosa garantisce la **firma**?
6. Perché nel payload di un JWT **non** si devono mettere segreti?
7. Qual è il principale svantaggio dei JWT rispetto alle sessioni, e come lo si mitiga?
8. Perché le password non vanno salvate in chiaro né semplicemente cifrate, ma **hashate**?
9. Cos'è il **salt** e quale attacco rende inefficace? Perché si preferisce bcrypt/Argon2 a SHA-256 per le password?
10. Cos'è un **middleware** in Express e come lo si usa per proteggere una rotta? Qual è la differenza tra autenticazione e autorizzazione?

<details><summary>Risposte</summary>

1. Stateless significa che ogni richiesta HTTP è **indipendente**: il server non sa, di per sé, che arrivano dallo stesso utente. Dopo il login questo crea il problema di **riconoscere** l'utente nelle richieste successive senza richiedere di nuovo le credenziali.
2. Un **cookie** è una coppia chiave-valore che il server manda col header `Set-Cookie`; il browser la conserva e la **rispedisce automaticamente** a ogni richiesta verso quel sito nell'header `Cookie`.
3. **`HttpOnly`** rende il cookie illeggibile dal JavaScript della pagina (difende dal furto via **XSS**); **`SameSite`** limita l'invio del cookie quando la richiesta parte da un altro sito (difende dal **CSRF**).
4. Sul server si salva la **sessione** (i dati dell'utente); nel cookie viaggia **solo il session ID**. Il logout è semplice perché basta **cancellare la sessione** dallo store: il cookie residuo non vale più.
5. **Header . Payload . Firma** (ciascuno in Base64URL). La **firma** garantisce l'**integrità**: se il payload viene modificato, la firma non torna e il token è rifiutato.
6. Perché il payload è solo **codificato** (Base64URL), non cifrato: chiunque abbia il token può leggerlo.
7. La **revoca**: un JWT valido resta tale fino alla scadenza anche se vuoi bloccare l'utente, perché il server non tiene lo stato. Si mitiga con token d'accesso a **scadenza breve** più un **refresh token** revocabile.
8. Perché in chiaro un furto del DB le espone tutte; cifrate si potrebbero **decifrare** con la chiave. L'**hash** è a senso unico: dall'hash non si risale alla password, e al login si confronta l'hash del valore digitato.
9. Il **salt** è una stringa casuale diversa per utente aggiunta prima dell'hash: annulla le **rainbow table** e rende diversi gli hash di password uguali. Si preferiscono **bcrypt/Argon2** perché sono **lenti e tarabili**, mentre SHA-256 è troppo veloce e permette miliardi di tentativi al secondo.
10. Un **middleware** è una funzione nella catena richiesta→risposta che può bloccare o far proseguire (`next()`). Per proteggere una rotta si mette un middleware che verifica le credenziali prima dell'handler. **Autenticazione** = verificare *chi sei*; **autorizzazione** = verificare *cosa puoi fare* (i permessi/ruoli).
</details>

## Esercizi
1. **Login con hash della password.** Scrivi in Node/Express gli handler di `/register` (salva l'hash della password) e `/login` (verifica la password e apre la sessione). Spiega perché non salvi la password in chiaro.
2. **Middleware di protezione.** Scrivi un middleware `requireAuth` che lasci passare solo le richieste con una sessione valida, e applicalo a una rotta `/dashboard`.
3. **Sessione o JWT?** Per ciascuno di questi casi scegli l'approccio e motiva: (a) un gestionale web interno dove serve poter fare logout immediato; (b) un'API consumata da un'app mobile e da altri microservizi.

<details><summary>Soluzioni</summary>

1. 
   ```js
   import bcrypt from 'bcrypt';

   app.post('/register', async (req, res) => {
     const { email, password } = req.body;
     const passwordHash = await bcrypt.hash(password, 12);
     await db.users.insert({ email, passwordHash });
     res.status(201).json({ ok: true });
   });

   app.post('/login', async (req, res) => {
     const { email, password } = req.body;
     const user = await db.users.findByEmail(email);
     if (!user || !(await bcrypt.compare(password, user.passwordHash)))
       return res.status(401).json({ error: 'Credenziali non valide' });
     req.session.userId = user.id;
     res.json({ ok: true });
   });
   ```
   Non si salva la password in chiaro perché un furto del database la esporrebbe direttamente (e gli utenti riusano le password altrove). Si salva l'**hash** con bcrypt (lento, con salt incluso): irreversibile e costoso da attaccare. Il messaggio d'errore è **generico** per non rivelare se a sbagliare è l'email o la password.

2. 
   ```js
   function requireAuth(req, res, next) {
     if (!req.session?.userId)
       return res.status(401).json({ error: 'Non autenticato' });
     next();
   }
   app.get('/dashboard', requireAuth, (req, res) => {
     res.json({ msg: `Benvenuta, utente ${req.session.userId}` });
   });
   ```
   Il middleware intercetta la richiesta prima dell'handler: se manca una sessione valida risponde `401`, altrimenti chiama `next()` e la richiesta prosegue.

3. (a) **Sessione**: il gestionale interno trae vantaggio dal poter **revocare** l'accesso all'istante cancellando la sessione dallo store; il traffico limitato rende il costo dello stato lato server trascurabile. (b) **JWT**: un'API per app mobile e microservizi beneficia dell'approccio **stateless** (ogni servizio verifica la firma senza un sessione-store condiviso); la revoca si gestisce con scadenze brevi e refresh token revocabili.
</details>
