---
day: 24
topic_id: sec-auth
title: "Autenticazione e autorizzazione — sessioni, JWT, OAuth2, least-privilege"
area: computer-science
course: Cybersecurity ed Ethical Hacking
grounded_in: "UNIBO/terzoAnno/sicurezza + lavoro reale (auth federata, JWT, token firmati)"
adjacent: [sec-crypto, web-backend, xc-api-rest, sec-cia]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo."
---

# Autenticazione e autorizzazione — sessioni, JWT, OAuth2, least-privilege

> **Perché oggi:** ogni app con utenti deve rispondere a "**chi sei**?" e "**cosa puoi fare**?". Lo fai già: JWT in MaiCare, **auth federata** tra le app in Glacom (il preventivi-bot che si autentica con l'app principale), e i **token firmati HMAC** di Job Pipeline. Sono le domande di sicurezza più frequenti ai colloqui backend.

## Le due parole che vengono confuse
- **Autenticazione (authentication, AuthN):** *chi sei?* Verifichi l'**identità** (password, codice, biometria, un token valido).
- **Autorizzazione (authorization, AuthZ):** *cosa puoi fare?* Decidi i **permessi** una volta nota l'identità (questo utente può leggere ma non cancellare).

Prima autentichi, poi autorizzi. Confonderle è un classico: "sei loggato" non vuol dire "puoi fare tutto".

## Il problema di fondo: HTTP è senza memoria
**HTTP è stateless** (senza stato): ogni richiesta è a sé, il server non "ricorda" la precedente. Se ti sei loggato con la richiesta 1, alla richiesta 2 il server **non sa** che sei tu. Serve un modo per **portare la prova di identità a ogni richiesta**. Due famiglie di soluzioni: **sessioni** e **token**.

## Sessioni (stateful)
Dopo il login, il server crea una **sessione**: salva **da qualche parte** (memoria, DB, Redis) un record "sessione X = utente Y" e manda al browser un **cookie** con l'**ID di sessione**. Il browser rimanda quel cookie a ogni richiesta; il server cerca l'ID nel suo store e ti riconosce.

- **Pro:** semplice, revoca immediata (cancelli la sessione lato server e sei fuori).
- **Contro:** il server deve **tenere lo stato** (lo store delle sessioni); scalare su molti server richiede uno store condiviso.

## Token: JWT (stateless)
Un **token** sposta lo stato **dal server al client**. Il più diffuso è il **JWT (JSON Web Token)**: un pezzo di testo che contiene i dati dell'utente (**claim**, es. `id`, `ruolo`, scadenza) ed è **firmato** dal server. Ha tre parti separate da punto: **header . payload . firma**.

Il punto cruciale è la **firma**: il server firma header+payload con una **chiave segreta** (o una coppia asimmetrica). A ogni richiesta il client manda il token; il server **ricalcola la firma** e la confronta: se combacia, il token è **autentico e non manomesso**, e il server si fida dei claim **senza consultare un database**. È lo stesso principio dei tuoi token di Job Pipeline, firmati **HMAC** (una firma con chiave segreta: chi non ha la chiave non può forgiare un token valido).

Attenzione (domande da colloquio):
- Il payload è **firmato, non cifrato**: chiunque lo può **leggere** (è solo Base64), quindi **niente segreti** dentro.
- **Revoca difficile:** essendo stateless, un JWT valido resta valido fino alla **scadenza** anche se "logout". Per questo si usano **scadenze brevi** + un **refresh token** (a vita più lunga, revocabile) per riottenerne di nuovi.

<svg viewBox="0 0 640 210" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="au" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <rect x="30" y="80" width="110" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="85" y="107">Client</text>
    <rect x="500" y="80" width="110" height="46" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="555" y="107">Server</text>
  </g>
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
    <path d="M140,92 L498,92" stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#au)"/>
    <text x="320" y="84">1. login (credenziali)</text>
    <path d="M498,112 L142,112" stroke="var(--accent)" stroke-width="1.5" fill="none" marker-end="url(#au)"/>
    <text x="320" y="128">2. token firmato (JWT)</text>
    <path d="M140,150 L498,150" stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#au)"/>
    <text x="320" y="144">3. richiesta + token in ogni chiamata</text>
    <text x="320" y="176" fill="var(--muted)" font-size="10.5">4. il server RICALCOLA la firma: combacia → si fida dei claim (nessun DB)</text>
  </g>
</svg>

## OAuth 2.0 e "Login con Google"
**OAuth 2.0** è il protocollo standard di **autorizzazione delegata**: permette a un'app di **agire su risorse tue** ospitate altrove **senza vedere la tua password**. Quando premi "**Login con Google**", non dai la password di Google all'app: Google ti autentica, e rilascia all'app un **access token** con permessi **limitati** (gli **scope**, es. "leggi email, non cancellarle"). L'app usa quel token per le API. Nota: OAuth nasce per l'**autorizzazione**; per l'**autenticazione** ("chi sei") ci si appoggia a **OpenID Connect (OIDC)**, uno strato sopra OAuth che aggiunge un **ID token**.

Il tuo caso: l'**auth federata** tra il preventivi-bot e l'app principale è la stessa idea a livello aziendale — un servizio si fida dell'identità stabilita da un altro, senza gestire credenziali separate.

## Autorizzazione: modelli di permesso
Nota l'identità, decidi cosa può fare:
- **RBAC (Role-Based Access Control):** permessi legati a **ruoli** (admin, editor, viewer); assegni ruoli agli utenti. Semplice, il più diffuso.
- **ABAC (Attribute-Based):** permessi da **attributi/contesto** (reparto, orario, proprietà della risorsa). Più flessibile, più complesso.
- **Least privilege (minimo privilegio):** principio-guida — dai a ogni utente/servizio **solo** i permessi che gli servono, niente di più. Limita il danno se un account viene compromesso. È lo stesso spirito degli **scope** ristretti di OAuth.

## Completeness check (integrato da me)
- **Le password non si salvano in chiaro:** si salva un **hash** con funzione lenta e apposita (**bcrypt/argon2**) + **salt** (un valore casuale per utente che rende inutili le tabelle precalcolate). Se il DB trapela, gli hash non rivelano le password. (Hash e crittografia: giorno adiacente `sec-crypto`.)
- **MFA (autenticazione a più fattori):** combinare **qualcosa che sai** (password) + **qualcosa che hai** (codice sul telefono) + **qualcosa che sei** (biometria). Alza molto la barriera.
- **Dove vivono i token nel browser:** un cookie **HttpOnly** (non leggibile da JavaScript) protegge da furto via **XSS**; va accompagnato da difese **CSRF**. Trade-off di sicurezza reali, non dettagli.

## Fonti
- **OWASP — Authentication Cheat Sheet** (cheatsheetseries.owasp.org)
- **jwt.io** — ispeziona e capisci la struttura di un JWT
- **oauth.net / "OAuth 2 Simplified"**, Aaron Parecki

## Concetti adiacenti
- `sec-crypto` — hash, firma, simmetrico/asimmetrico (la base della firma dei token)
- `web-backend` — sessioni, cookie e auth lato server
- `xc-api-rest` — proteggere le API (token, scope, idempotenza)

## Quiz (10 — tutte rispondibili dalla lezione)
1. Differenza tra **autenticazione** e **autorizzazione**?
2. Cosa vuol dire che **HTTP è stateless** e perché è un problema per il login?
3. Come funziona l'autenticazione a **sessione** (cookie + store) e qual è il suo pro/contro principale?
4. Cos'è un **JWT** e da quali tre parti è composto?
5. Perché la **firma** di un JWT permette al server di fidarsi senza consultare un DB?
6. Perché **non** si mettono segreti nel payload di un JWT?
7. Perché la **revoca** di un JWT è difficile e come si mitiga?
8. Cosa fa **OAuth 2.0** e perché "Login con Google" non dà la password all'app?
9. Differenza tra **RBAC** e principio di **least privilege**?
10. Perché le password si salvano come **hash con salt** e non in chiaro?

<details><summary>Risposte</summary>

1. **Autenticazione** = verificare **chi sei** (identità); **autorizzazione** = decidere **cosa puoi fare** (permessi). Prima l'una, poi l'altra.
2. Ogni richiesta HTTP è **indipendente**: il server non ricorda la precedente, quindi dopo il login serve un modo per **riprovare l'identità** a ogni richiesta.
3. Il server salva "sessione X = utente Y" in uno **store** e manda un **cookie** con l'ID; **pro**: revoca immediata; **contro**: il server deve tenere lo **stato** (store condiviso per scalare).
4. Un **JSON Web Token**: **header . payload . firma**.
5. Perché la firma è calcolata con una **chiave segreta**: il server la **ricalcola** e, se combacia, il token è autentico e non manomesso, così si fida dei claim **senza DB**.
6. Perché il payload è **firmato ma non cifrato**: è leggibile da chiunque (solo Base64).
7. Perché è **stateless**: un token valido resta valido fino a **scadenza** anche dopo "logout"; si mitiga con **scadenze brevi** + **refresh token** revocabile.
8. È **autorizzazione delegata**: l'app ottiene un **access token** con **scope** limitati per agire sulle tue risorse; Google ti autentica e l'app **non vede mai la password**.
9. **RBAC** lega i permessi a **ruoli**; **least privilege** è il principio di dare **solo** i permessi necessari (vale anche dentro RBAC).
10. Perché se il DB trapela un **hash** (lento, con **salt** per utente) non rivela la password né si presta a tabelle precalcolate; il chiaro sarebbe subito compromesso.
</details>
