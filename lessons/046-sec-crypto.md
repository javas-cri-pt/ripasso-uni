---
day: 46
topic_id: sec-crypto
title: "Crittografia: simmetrica, asimmetrica, hash, TLS"
area: computer-science
course: "Cybersecurity ed Ethical Hacking"
grounded_in: null
adjacent: [net-app, sec-auth, web-backend]
completeness_checked: true
quiz_count: 10
---

# Crittografia: simmetrica, asimmetrica, hash, TLS

> **Perché oggi:** ogni volta che vedi il lucchetto nel browser, che fai login su un sito, che la tua app salva una password, c'è sotto della crittografia. È il mattone trasversale della sicurezza e torna in `sec-auth` (come riconosci chi sei) e in `web-backend` (come custodisci le password). Oggi mettiamo ordine nei quattro strumenti fondamentali: cifratura **simmetrica**, cifratura **asimmetrica**, funzioni **hash**, e come si combinano in **TLS**, il protocollo che rende sicuro il web. Taglio pratico: cosa fa ciascuno, quando si usa, e perché.

## I tre obiettivi: riservatezza, integrità, autenticità
La crittografia serve tre scopi distinti, che conviene tenere separati in testa:
- **Riservatezza (confidentiality):** nascondere il contenuto a chi non deve leggerlo. Se ne occupa la **cifratura**.
- **Integrità (integrity):** garantire che il messaggio non sia stato **alterato**. Se ne occupano gli **hash** e i MAC.
- **Autenticità (authenticity):** garantire **chi** è il mittente e che non possa negarlo (**non ripudio**). Se ne occupa la **firma digitale**.

Un errore comune da colloquio è confondere cifrare (nascondere) con hashare (sigillare): fanno cose diverse, per obiettivi diversi.

## Cifratura simmetrica: una sola chiave condivisa
Nella **cifratura simmetrica** la **stessa chiave** serve sia a cifrare sia a decifrare. Il testo in chiaro (**plaintext**) più la chiave producono il testo cifrato (**ciphertext**); con la stessa chiave si torna indietro. Lo standard moderno è **AES (Advanced Encryption Standard)**, un cifrario a blocchi con chiavi da 128, 192 o 256 bit, velocissimo perché supportato in hardware dalle CPU.

- **Pregio:** è **molto veloce**, adatto a cifrare grandi quantità di dati (file, dischi, flussi di rete).
- **Problema:** la **distribuzione della chiave**. Mittente e destinatario devono condividere la stessa chiave segreta, ma come la si scambia in sicurezza su un canale non sicuro? Se la mandi "in chiaro", chi intercetta può decifrare tutto. Questo è il problema che la crittografia asimmetrica risolve.
- Con `N` persone che vogliono comunicare a coppie servirebbero `N·(N-1)/2` chiavi diverse: non scala.

## Cifratura asimmetrica: coppia di chiavi pubblica e privata
Nella **cifratura asimmetrica** (a chiave pubblica) ogni soggetto ha una **coppia di chiavi** matematicamente legate: una **chiave pubblica**, che può distribuire a tutti, e una **chiave privata**, che tiene segreta. Ciò che una chiave della coppia cifra, **solo l'altra** può decifrare. L'algoritmo storico è **RSA** (dalle iniziali di Rivest, Shamir, Adleman), basato sulla difficoltà di fattorizzare numeri enormi; oggi si usano anche le curve ellittiche (**ECC**), più efficienti a parità di sicurezza. Due usi speculari:

- **Per la riservatezza:** chi vuole scriverti cifra con la **tua chiave pubblica**; solo tu, con la **chiave privata**, puoi decifrare. Chiunque può "chiudere il lucchetto", solo tu hai la chiave per aprirlo.
- **Per l'autenticità (firma digitale):** tu cifri (firmi) con la **tua chiave privata**; chiunque, con la **tua chiave pubblica**, può verificare che la firma è tua. Solo tu potevi produrla: questo dà **autenticità** e **non ripudio**.

Il prezzo: è **molto più lenta** della simmetrica, quindi non si usa per cifrare grandi moli di dati. La si usa per scambiare in sicurezza una chiave simmetrica, e per firmare.

## Il meglio dei due mondi: cifratura ibrida
Simmetrica = veloce ma con il problema della chiave; asimmetrica = risolve la chiave ma lenta. La soluzione pratica, usata ovunque, è la **cifratura ibrida**:
1. Si genera una chiave simmetrica **usa e getta** per quella sessione (**chiave di sessione**).
2. La si scambia in sicurezza usando la **crittografia asimmetrica** (o uno scambio di chiavi come Diffie-Hellman).
3. Da lì in poi tutti i dati viaggiano con la **simmetrica** veloce.

Così si paga la lentezza dell'asimmetrica una sola volta, all'inizio, e si gode della velocità della simmetrica per tutto il resto. È esattamente lo schema di TLS.

## Funzioni hash: l'impronta digitale dei dati
Una **funzione hash crittografica** prende un input di qualsiasi dimensione e produce una stringa di lunghezza **fissa** (il **digest**, o impronta). Proprietà che la rendono crittografica:
- **A senso unico (one-way):** dal digest **non si può** risalire all'input.
- **Deterministica:** lo stesso input dà sempre lo stesso digest.
- **Effetto valanga:** cambiare anche un solo bit dell'input stravolge completamente il digest.
- **Resistente alle collisioni:** è praticamente impossibile trovare due input diversi con lo stesso digest.

Serve a garantire **integrità**: se il digest di un file ricevuto coincide con quello atteso, il file non è stato alterato. Lo standard sicuro è la famiglia **SHA-2** (es. **SHA-256**) e **SHA-3**; **MD5** e **SHA-1** sono **rotti** (si sanno produrre collisioni) e non vanno più usati.

Un chiarimento fondamentale: l'hash **non è cifratura**. Non ha chiave e non è reversibile: non si "decifra" un hash. Per questo le password si **hashano** (vedi `web-backend`): non devono mai poter tornare in chiaro. E lì, ricordi, servono **salt** (stringa casuale per utente) e funzioni **lente** come bcrypt/Argon2, perché gli hash generici sono troppo veloci da attaccare a forza bruta.

Quando all'integrità serve anche una chiave segreta condivisa, si usa un **MAC** (Message Authentication Code), tipicamente **HMAC**: è un hash che include una chiave, così solo chi la possiede può generare o verificare il codice.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 250" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
    <text x="180" y="18" font-weight="700" font-size="12.5">Simmetrica: una chiave</text>
    <text x="540" y="18" font-weight="700" font-size="12.5">Asimmetrica: coppia di chiavi</text>

    <rect x="40" y="44" width="92" height="34" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="86" y="65">plaintext</text>
    <rect x="228" y="44" width="92" height="34" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="274" y="65">ciphertext</text>
    <rect x="134" y="104" width="92" height="30" rx="7" fill="var(--card2)" stroke="var(--accent)" stroke-width="1.6"/><text x="180" y="124" font-size="10">stessa chiave</text>
    <text x="180" y="160" font-size="9.5" fill="var(--muted)">cifra e decifra uguale</text>
    <text x="180" y="176" font-size="9.5" fill="var(--muted)">AES · veloce</text>

    <rect x="400" y="44" width="92" height="34" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="446" y="65">plaintext</text>
    <rect x="588" y="44" width="92" height="34" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="634" y="65">ciphertext</text>
    <rect x="470" y="104" width="86" height="30" rx="7" fill="var(--card2)" stroke="var(--good)" stroke-width="1.6"/><text x="513" y="124" font-size="10">pubblica</text>
    <rect x="566" y="104" width="86" height="30" rx="7" fill="var(--card2)" stroke="var(--accent)" stroke-width="1.6"/><text x="609" y="124" font-size="10">privata</text>
    <text x="540" y="160" font-size="9.5" fill="var(--muted)">cifra con una, decifra con l'altra</text>
    <text x="540" y="176" font-size="9.5" fill="var(--muted)">RSA/ECC · lenta</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none">
    <path d="M132,61 L226,61"/><path d="M180,104 L180,78"/>
    <path d="M492,61 L586,61"/><path d="M513,104 L480,80"/><path d="M609,104 L640,80"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">A sinistra la cifratura simmetrica: una sola chiave segreta per cifrare e decifrare (veloce, ma va condivisa). A destra l'asimmetrica: ciò che la chiave pubblica cifra solo la privata decifra (risolve lo scambio della chiave, ma è lenta). TLS usa entrambe: scambia la chiave con l'asimmetrica, poi cifra i dati con la simmetrica.</figcaption>
</figure>

## TLS: come si mettono insieme tutte le tessere
**TLS (Transport Layer Security)**, il successore di **SSL**, è il protocollo che cifra le connessioni di rete: è la **S** di **HTTPS** (HTTP over TLS, il lucchetto del browser). TLS raggiunge tutti e tre gli obiettivi combinando gli strumenti visti. Quando apri un sito sicuro, avviene l'**handshake** (stretta di mano):

1. **Autenticazione del server tramite certificato.** Il server presenta un **certificato digitale**: un documento che lega la sua identità (il dominio) alla sua **chiave pubblica**, **firmato** da una **Certificate Authority (CA)**, un'autorità di cui il browser si fida. Il browser verifica la firma della CA: così è sicuro di parlare col vero sito e non con un impostore (difesa dal **man-in-the-middle**, l'attaccante che si interpone). Qui lavorano firma digitale (asimmetrica) e hash.
2. **Scambio della chiave di sessione.** Client e server concordano una **chiave simmetrica** usa e getta per questa sessione, proteggendola con la crittografia **asimmetrica** / uno scambio Diffie-Hellman. I TLS moderni usano scambi che garantiscono la **forward secrecy**: anche se un domani la chiave privata del server fosse compromessa, le sessioni passate restano illeggibili.
3. **Comunicazione cifrata.** Da qui in poi tutti i dati viaggiano cifrati con la **simmetrica** veloce (AES), con un controllo di **integrità** su ogni messaggio. È la cifratura **ibrida** in azione.

In sintesi: TLS usa l'**asimmetrica** per autenticare il server e scambiare la chiave, e la **simmetrica** per cifrare la conversazione; gli **hash** garantiscono l'integrità e reggono i certificati. Tutti e quattro gli strumenti della lezione, in un solo protocollo.

## Esempi concreti
- **Login su un sito "https://":** prima che digiti la password, l'handshake TLS ha già verificato il certificato del sito e stabilito una chiave simmetrica; la password viaggia cifrata. Il server poi la **hasha** con bcrypt per confrontarla con quella salvata (riservatezza in transito con TLS, custodia a riposo con l'hash).
- **Verificare un download:** scarichi un file e il sito pubblica il suo **SHA-256**. Ne calcoli l'hash in locale: se coincide, il file non è stato corrotto né manomesso. È integrità, senza bisogno di cifratura.
- **Messaggistica cifrata end-to-end:** le app di messaggistica generano per ogni chat chiavi asimmetriche; il contenuto è cifrato così che nemmeno il server possa leggerlo, e si usa una chiave simmetrica per il flusso dei messaggi. Stessa logica ibrida.

## Notable use case
- **Let's Encrypt** è una Certificate Authority gratuita e automatizzata che ha reso HTTPS lo standard di fatto del web: oggi la grande maggioranza del traffico è cifrata.
- **AES** fu scelto nel 2001 dal **NIST** (ente di standardizzazione USA) con un concorso pubblico, vinto dall'algoritmo "Rijndael"; è usato ovunque, dai dischi cifrati al Wi-Fi (WPA).
- **Signal** ha reso popolare la cifratura end-to-end con il suo protocollo, adottato poi da altre grandi app di messaggistica.
- La crittografia **post-quantum** è la frontiera: il NIST ha standardizzato nel 2024 i primi algoritmi resistenti a futuri computer quantistici, che minaccerebbero RSA ed ECC.

## Fonti
- **RFC 8446 — TLS 1.3** — datatracker.ietf.org/doc/html/rfc8446
- **OWASP — Cryptographic Storage & Transport Layer Protection Cheat Sheets** — cheatsheetseries.owasp.org
- **NIST FIPS 197 (AES)** e **FIPS 180-4 (SHA-2)** — csrc.nist.gov
- **Let's Encrypt — How It Works** — letsencrypt.org/how-it-works

## Concetti adiacenti
- `net-app` — HTTP, DNS, TLS al livello applicativo: dove la crittografia di oggi entra in rete
- `sec-auth` — autenticazione e autorizzazione: usano firme, hash e token
- `web-backend` — sessioni e hashing delle password: la crittografia nel codice server

## Quiz (10 — tutte rispondibili dalla lezione)
1. Distingui i tre obiettivi **riservatezza**, **integrità** e **autenticità** e quale strumento serve ciascuno.
2. Nella cifratura **simmetrica**, quante chiavi ci sono e qual è il suo principale problema pratico?
3. Nella cifratura **asimmetrica**, cosa può fare la chiave pubblica e cosa la privata? Chi tiene segreta quale?
4. Come si ottiene una **firma digitale** con le chiavi asimmetriche, e cosa garantisce?
5. Cos'è la **cifratura ibrida** e perché è conveniente?
6. Elenca le proprietà di una **funzione hash crittografica** (almeno tre) e di' a cosa serve principalmente.
7. Perché un hash **non è** una cifratura e perché le password si **hashano** anziché cifrarle?
8. Perché per le password non basta SHA-256 e servono salt e funzioni come bcrypt/Argon2?
9. Durante l'**handshake TLS**, come fa il browser a essere sicuro di parlare col sito giusto (ruolo di certificato e CA)?
10. In TLS, quali parti usano la crittografia **asimmetrica** e quali la **simmetrica**, e perché questa divisione?

<details><summary>Risposte</summary>

1. **Riservatezza** = nascondere il contenuto (cifratura); **integrità** = garantire che non sia alterato (hash/MAC); **autenticità** = garantire chi è il mittente e il non ripudio (firma digitale).
2. **Una sola** chiave, condivisa per cifrare e decifrare. Il problema principale è la **distribuzione/scambio della chiave** su un canale non sicuro.
3. Ciò che la **pubblica** cifra, solo la **privata** decifra (e viceversa). La chiave **privata** si tiene segreta; la **pubblica** si distribuisce a tutti.
4. Si firma cifrando con la **propria chiave privata**; chiunque verifica con la **chiave pubblica** corrispondente. Garantisce **autenticità** e **non ripudio** (solo il titolare della privata poteva produrla).
5. Si scambia una **chiave simmetrica di sessione** proteggendola con l'**asimmetrica**, poi si cifrano i dati con la **simmetrica** veloce. Conviene perché si paga la lentezza dell'asimmetrica una sola volta e si ottiene velocità per tutto il resto.
6. **A senso unico**, **deterministica**, **effetto valanga**, **resistente alle collisioni** (lunghezza fissa del digest). Serve principalmente a garantire l'**integrità**.
7. Perché l'hash **non ha chiave e non è reversibile**: non si può "decifrare". Le password si hashano proprio perché non devono mai poter tornare in chiaro, nemmeno per chi gestisce il sistema.
8. Perché SHA-256 è **troppo veloce**: un attaccante con il DB rubato prova miliardi di combinazioni al secondo. Il **salt** (casuale per utente) annulla le rainbow table; bcrypt/Argon2 sono **lenti e tarabili**, rendendo la forza bruta impraticabile.
9. Il server presenta un **certificato** che lega il suo dominio alla sua chiave pubblica, **firmato da una CA** di cui il browser si fida; verificando la firma della CA, il browser è certo di parlare col vero sito (difesa dal man-in-the-middle).
10. L'**asimmetrica** autentica il server (certificato/firma) e protegge lo **scambio della chiave** di sessione; la **simmetrica** cifra tutta la conversazione successiva. La divisione sfrutta l'asimmetrica per risolvere lo scambio della chiave e la simmetrica per la velocità sui dati.
</details>

## Esercizi
1. **Simmetrica o asimmetrica?** Per ciascun caso scegli e motiva: (a) cifrare un disco esterno da 500 GB; (b) permettere a chiunque di inviarti un messaggio che solo tu possa leggere; (c) firmare un documento in modo che tutti verifichino che è tuo; (d) scambiare in sicurezza una chiave con uno sconosciuto su Internet.
2. **Hashare una password correttamente.** Scrivi lo pseudocodice (o Node) di registrazione e verifica di una password fatti a regola d'arte, e spiega il ruolo di salt e fattore di costo.
3. **Ricostruisci l'handshake TLS.** Metti in ordine i passi dell'handshake e indica per ciascuno quale strumento crittografico entra in gioco (asimmetrica, simmetrica, hash/firma).

<details><summary>Soluzioni</summary>

1. (a) **Simmetrica (AES):** grande volume di dati, serve velocità e c'è un solo soggetto (tu) che conosce la chiave. (b) **Asimmetrica:** gli altri cifrano con la **tua chiave pubblica**, solo la tua privata decifra. (c) **Asimmetrica (firma):** firmi con la **tua chiave privata**, tutti verificano con la pubblica (autenticità + non ripudio). (d) **Asimmetrica / scambio di chiavi:** è proprio il problema che l'asimmetrica (o Diffie-Hellman) risolve, per poi passare alla simmetrica.

2. 
   ```js
   import bcrypt from 'bcrypt';
   // registrazione
   const passwordHash = await bcrypt.hash(password, 12); // 12 = fattore di costo; salt incluso
   await db.users.insert({ email, passwordHash });
   // verifica al login
   const ok = await bcrypt.compare(passwordDigitata, user.passwordHash);
   ```
   Il **salt** (casuale, diverso per utente, qui generato e incluso da bcrypt) fa sì che password uguali abbiano hash diversi e annulla le rainbow table. Il **fattore di costo** rende l'hash volutamente lento: lo si alza nel tempo per restare al passo con l'hardware e tenere impraticabile la forza bruta. La password in chiaro non viene mai salvata.

3. Ordine: (1) il server invia il **certificato** firmato dalla CA → il browser ne verifica la **firma** (asimmetrica + hash) per autenticare il server; (2) client e server **concordano la chiave di sessione** proteggendola con l'**asimmetrica**/Diffie-Hellman; (3) la conversazione prosegue cifrata con la **simmetrica** (AES), con controllo di **integrità** (hash/MAC) su ogni messaggio. È la cifratura ibrida: asimmetrica per autenticare e scambiare la chiave, simmetrica per i dati.
</details>
