---
day: 11
topic_id: se-requirements
title: "Analisi dei requisiti — raccolta, validazione, casi d'uso e scenari"
area: computer-science
course: Ingegneria del Software
grounded_in: "UNIBO/terzoAnno/IngengeriaDelSoftware (progetto Signal)"
adjacent: [se-analysis, se-process, xc-pm-prd, is-bpmn]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo."
---

# Analisi dei requisiti — raccolta, validazione, casi d'uso e scenari

> **Perché oggi:** nel progetto **Signal** (gruppo 13) questa era **la tua parte**: analisi dei requisiti + architettura. È il punto in cui ti fermi a chiedere "ma il problema qual è, davvero?" prima di scrivere una riga di codice. E "capire il problema giusto" è metà del mestiere sia da **software engineer** sia da **Product**: sbagliare i requisiti è l'errore più costoso di tutti, perché ti porti dietro la cosa sbagliata fino alla fine. Ripassare questo capitolo ti serve due volte — per l'esame e per il colloquio, dove "come raccogli e validi i requisiti" è una domanda che torna sempre.

## Perché i requisiti sono la fase più critica

Un **requisito** è una **proprietà o un servizio che il sistema deve avere o offrire**: qualcosa che, se manca, il sistema non è quello che avevi promesso. La fase in cui li definisci è la prima del progetto ed è anche la più delicata, per un motivo economico preciso.

Un errore introdotto nei requisiti e scoperto **tardi** costa **ordini di grandezza** in più rispetto allo stesso errore corretto subito. La ragione è che l'errore si propaga: se il requisito è sbagliato, ci costruisci sopra l'analisi, poi il design, poi il codice, poi i test. Correggerlo in fase di **analisi** significa cambiare una riga in un documento — costa **poco**. Correggerlo in **produzione**, a sistema già consegnato e in uso, significa disfare e rifare tutto quello che ci hai costruito sopra, con il sistema già nelle mani degli utenti — costa **tantissimo**. Non è un numero preciso: è un principio qualitativo (prima lo scopri, meno costa) che vale in tutti i modelli di sviluppo. Per questo si investe tempo a farli bene: è il posto dove un'ora spesa ne fa risparmiare cento.

## Requisiti funzionali vs non funzionali

I requisiti si dividono in due grandi famiglie, e la differenza è tra il **cosa** e il **come**.

- **Requisiti funzionali** — descrivono **cosa** fa il sistema: le funzioni, i servizi, i comportamenti. Rispondono a "quali cose deve poter fare l'utente / il sistema". Esempio in Signal: *"l'utente può effettuare una segnalazione con posizione"*, oppure *"l'amministratore può revisionare e pubblicare una segnalazione sulla bacheca"*. Sono le azioni concrete.
- **Requisiti non funzionali** — descrivono **come** il sistema deve farlo: le **qualità** e i **vincoli**. Non aggiungono funzioni nuove, ma dicono con quale livello di prestazioni, sicurezza, usabilità, affidabilità e privacy le funzioni devono essere offerte. Esempi di categorie: **prestazioni** (quanto veloce), **sicurezza** (protezione da accessi non autorizzati), **usabilità** (quanto è facile da usare), **affidabilità** (quanto raramente si rompe), **privacy/GDPR** (come tratti i dati personali). In Signal i **requisiti di protezione dei dati** (GDPR — il regolamento europeo sulla protezione dei dati personali) erano proprio requisiti non funzionali.

Attenzione a una trappola classica: i requisiti non funzionali sono spesso i **più trascurati** (perché meno visibili di una schermata da costruire) e allo stesso tempo i **più critici** — un sistema che fa tutto ma è lento, insicuro o non a norma sul trattamento dati è un sistema che non puoi mettere in produzione.

## Le attività: raccolta → analisi → specifica → validazione

L'analisi dei requisiti non è un unico gesto: è una sequenza di quattro attività. Vediamole una per una.

### Raccolta (elicitation)

La **raccolta** (in inglese *elicitation*, "far emergere") è il momento in cui i requisiti **vengono fuori** dalle persone e dai documenti. Le fonti tipiche:

- **interviste agli stakeholder** — gli **stakeholder** (portatori di interesse: committente, utenti, chi userà o pagherà il sistema) si intervistano per farsi raccontare cosa serve;
- **osservazione** — guardare come le persone lavorano oggi, per capire il processo reale (non quello dichiarato);
- **documenti** — leggere materiale esistente (normative, manuali, moduli cartacei);
- **brainstorming** — sessioni in cui si generano idee liberamente.

Le difficoltà sono la parte interessante: **gli utenti non sanno sempre cosa vogliono** (lo capiscono quando lo vedono), esistono **requisiti impliciti** (dati per scontati e mai detti a voce, tipo "ovvio che i dati siano al sicuro"), e ci sono **conflitti tra stakeholder** (l'amministratore vuole controllo, il cittadino vuole velocità: qualcuno deve mediare).

### Analisi del dominio e vocabolario/glossario

Prima di scrivere i requisiti devi **capire il dominio**: il campo in cui il sistema opera (per Signal, le segnalazioni civiche e come funziona una pubblica amministrazione che le gestisce). Il prodotto concreto di questa attività è un **glossario** (o **vocabolario**): un elenco condiviso dei termini con la loro definizione precisa, così che **tutti intendano la stessa cosa con la stessa parola**.

In Signal il glossario fissava cosa significano termini come:

- **segnalazione** — l'anomalia che un cittadino comunica (una buca, un lampione spento, un problema domestico), con la sua posizione;
- **presa in carico** — l'atto con cui un utente "appropriato" si assume il compito di risolvere quel problema;
- **amministratore** — il ruolo che revisiona le segnalazioni, le smista per tipologia e le pubblica sulla bacheca.

Senza glossario, ognuno intende termini diversi e i requisiti diventano ambigui. È un investimento piccolo che previene un sacco di malintesi.

### Specifica

La **specifica** è scrivere i requisiti in modo **strutturato**, non a prosa libera. Lo strumento tipico è la **tabella dei requisiti**: una riga per requisito, con colonne come **ID** (identificatore univoco, es. RF-01), **descrizione**, **priorità** (quanto è importante) e **tipo** (funzionale / non funzionale). In Signal questa tabella c'era davvero ed era il cuore del documento.

Un **buon requisito** ha cinque proprietà, da ricordare a memoria:

- **chiaro** — si capisce senza spiegazioni;
- **non ambiguo** — ha una sola interpretazione possibile;
- **verificabile** — puoi controllare, a sistema fatto, se è soddisfatto o no (quindi niente "veloce", ma "risponde entro X");
- **tracciabile** — lo puoi seguire dal bisogno originario fino al codice e ai test (grazie all'ID);
- **consistente** — non contraddice altri requisiti.

### Validazione

La **validazione** è verificare **coi committenti** che i requisiti scritti siano davvero **quelli giusti**: completi (non manca niente di importante), coerenti (non si contraddicono) e realizzabili (si possono davvero costruire con le risorse date). È un controllo fatto *insieme al cliente*, perché solo lui può dire "sì, è proprio questo che volevo".

Attenzione alla distinzione più insidiosa del capitolo: **validazione ≠ verifica**.

- **Validazione** = "stiamo scrivendo i requisiti **giusti**?" → *il sistema giusto* (giudica il cliente).
- **Verifica** = "stiamo costruendo il sistema **secondo i requisiti**?" → *il sistema costruito bene* (giudica il test rispetto alla specifica).

In una frase: la validazione guarda se hai puntato al bersaglio giusto, la verifica se hai centrato il bersaglio che avevi scelto.

## Casi d'uso (use case)

Un **caso d'uso** (in inglese *use case*) descrive **come un attore usa il sistema per raggiungere un obiettivo**. È il modo standard di raccontare una funzionalità dal punto di vista di chi la usa, invece che dal punto di vista tecnico. Definiamo i due mattoni:

- **Attore** — un **ruolo esterno** che interagisce col sistema. Non è una persona specifica, è un ruolo: in Signal gli attori sono l'**Utente/Cittadino** e l'**Amministratore**. (Un attore può anche essere un altro sistema, ma qui restiamo sulle persone.)
- **Caso d'uso** — una **funzionalità vista dal punto di vista dell'attore**, con un obiettivo che l'attore vuole ottenere. In Signal, per esempio: *Effettua Segnalazione*, *Visualizza Stato Segnalazione*, *Prendi in carico segnalazione*.

Tra i casi d'uso ci sono due relazioni utili da conoscere:

- **include** — un caso d'uso ne usa **sempre** un altro come pezzo obbligatorio. Esempio: "Effettua Segnalazione" *include* "autenticazione" perché per segnalare devi sempre essere loggato.
- **extend** — un caso d'uso aggiunge un **comportamento opzionale**, che scatta solo in certe condizioni. È l'eccezione o la variante, non il caso base.

Il **diagramma dei casi d'uso** è un disegno UML (**UML** = *Unified Modeling Language*, il linguaggio grafico standard per modellare il software) che mostra gli **attori**, i **casi d'uso** e le **linee di associazione** che collegano ogni attore ai casi d'uso che gli competono. È una mappa a colpo d'occhio di "chi può fare cosa".

Il catalogo completo dei casi d'uso di Signal, dai due lati:

- **Lato utente**: **Login**, **Registrazione**, **Visualizza Profilo**, **Effettua Segnalazione**, **Visualizza Stato Segnalazione**, **Prendi in carico segnalazione**, **Richiedi terminazione**, **Ricerca segnalazione**.
- **Lato amministratore**: revisione, smistamento per tipologia e pubblicazione delle segnalazioni sulla bacheca.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 640 360" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
   <rect x="18" y="150" width="96" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="66" y="176">Utente</text>
   <rect x="526" y="150" width="100" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="576" y="176">Amministratore</text>
   <rect x="150" y="18" width="340" height="324" rx="12" fill="none" stroke="var(--rule)" stroke-dasharray="5 4"/><text x="320" y="38" fill="var(--muted)" font-size="11">Sistema Signal</text>
   <ellipse cx="320" cy="66" rx="112" ry="22" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="320" y="70">Effettua Segnalazione</text>
   <ellipse cx="320" cy="118" rx="112" ry="22" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="320" y="122">Visualizza Stato</text>
   <ellipse cx="320" cy="170" rx="112" ry="22" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="320" y="174">Prendi in carico</text>
   <ellipse cx="320" cy="222" rx="112" ry="22" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="320" y="226">Richiedi terminazione</text>
   <ellipse cx="320" cy="274" rx="112" ry="22" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="320" y="278">Ricerca segnalazione</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none">
   <path d="M114,168 L208,70"/>
   <path d="M114,170 L208,120"/>
   <path d="M114,172 L208,170"/>
   <path d="M114,174 L208,222"/>
   <path d="M114,176 L208,274"/>
   <path d="M526,168 L432,170"/>
   <path d="M526,170 L432,222"/>
   <path d="M526,172 L432,274"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Diagramma dei casi d'uso (Signal): a sinistra l'attore Utente, a destra l'Amministratore, al centro i casi d'uso del sistema con le linee di associazione.</figcaption>
</figure>

## Scenari

Un **scenario** è una **sequenza concreta di passi** con cui un caso d'uso viene eseguito una volta specifica. Se il caso d'uso è l'obiettivo astratto ("effettuare una segnalazione"), lo scenario è **una particolare esecuzione** raccontata passo per passo. Uno scenario ha:

- un **flusso principale** (o "flusso di base") — la sequenza quando **tutto va bene**;
- uno o più **flussi alternativi / eccezioni** — cosa succede quando qualcosa **devia** dal caso ideale.

Esempio scritto passo-passo — scenario del caso d'uso **Effettua Segnalazione** (flusso principale):

1. l'utente apre il **form** di segnalazione;
2. inserisce **descrizione**, **categoria** e **posizione**;
3. **invia** la segnalazione;
4. il sistema **salva** la segnalazione in stato **"in revisione"** (in attesa che l'amministratore la revisioni);
5. il sistema **mostra la conferma** all'utente.

**Flusso alternativo** (eccezione): al passo 2 la **posizione manca** → il sistema **chiede di specificarla** e non procede finché non è indicata. Un altro caso d'uso avrebbe altri flussi alternativi (dati non validi, utente non loggato, ecc.).

Tieni ben distinti i due concetti, perché è una domanda tipica: il **caso d'uso** è **astratto** (l'obiettivo, "effettuare una segnalazione", con tutti i suoi possibili svolgimenti); lo **scenario** è **una specifica esecuzione** di quel caso d'uso (una particolare sequenza di passi, principale o alternativa). Un caso d'uso raccoglie molti scenari.

## Security use case e misuse case (dal tuo progetto)

Finora abbiamo guardato gli usi **leciti**. Ma un sistema serio si progetta pensando anche a **come lo si rompe**. Qui entrano due concetti che in Signal facevate davvero, nell'**analisi del rischio**:

- **Misuse case** (caso di abuso) — descrive come un **attore ostile** (un attaccante) potrebbe **usare male o attaccare** il sistema. È un "caso d'uso al contrario": l'obiettivo è dannoso. Esempi per Signal: inserire **segnalazioni false di massa** per intasare la bacheca, oppure tentare di **accedere a dati altrui** (le segnalazioni o il profilo di un altro utente).
- **Security use case** (caso d'uso di sicurezza) — è la **contromisura** che neutralizza un misuse case: il comportamento che il sistema mette in campo per difendersi (es. autenticazione, limiti sul numero di segnalazioni, controlli di autorizzazione sull'accesso ai dati).

Il ragionamento è a coppie: per ogni minaccia (misuse case) definisci il controllo (security use case) che la ferma. In Signal questa analisi del rischio, con minacce e controlli, era parte del documento insieme ai requisiti di protezione dati (GDPR).

Concetto pratico da spendere a un colloquio: un bravo ingegnere non pensa solo a **come funziona**, ma anche a **come si rompe** e a chi ha interesse a romperlo. Mostrare questo tipo di ragionamento (threat modeling in miniatura) fa la differenza.

## User story (il cugino Agile, cenno)

Nel mondo **Agile** (le metodologie di sviluppo iterativo e incrementale) i requisiti si scrivono spesso non come casi d'uso ma come **user story**: frasi brevi, dal punto di vista dell'utente, con un formato fisso:

> **Come [ruolo] voglio [obiettivo] così che [beneficio].**

Esempio in stile Signal: *"Come **cittadino** voglio **segnalare una buca** così che **venga riparata**."* Il "così che" è importante perché costringe a dire **perché** serve, non solo cosa.

Le user story sono **più leggere** dei casi d'uso (una frase invece di un documento con flussi), e si accompagnano ai **criteri di accettazione**: le condizioni concrete che devono essere vere perché la story si consideri "fatta" (è il modo di renderla verificabile). È lo strumento tipico del **PRD** e del backlog di prodotto → aggancio a **xc-pm-prd**.

## Errori comuni

I modi tipici di sbagliare questa fase — riconoscerli è metà del lavoro:

- **requisiti ambigui o non verificabili** — il classico *"il sistema deve essere veloce"*: veloce **quanto**? Senza un criterio misurabile non puoi verificarlo, quindi non è un buon requisito;
- **dimenticare i non funzionali** — concentrarsi solo sulle funzioni e trascurare prestazioni, sicurezza, privacy, che poi ti esplodono in mano;
- **non validare col cliente** — scrivere requisiti bellissimi ma che non sono quelli che il committente voleva (verifica senza validazione);
- **confondere il requisito (cosa) con la soluzione (come)** — scrivere già "usiamo questa tecnologia" invece del bisogno: chiudi le opzioni prima del tempo;
- **nessun glossario** — senza vocabolario condiviso, ognuno intende i termini a modo suo e nascono ambiguità e conflitti.

## Fonti

- **Ian Sommerville, "Software Engineering"** — il manuale di riferimento del corso, con i capitoli dedicati alla *requirements engineering* (raccolta, analisi, specifica, validazione).
- **UML — uml.org** e **Martin Fowler, "UML Distilled"** — il linguaggio grafico standard e una guida sintetica ai diagrammi (tra cui i casi d'uso).
- **Karl Wiegers, "Software Requirements"** — testo di riferimento specifico sull'ingegneria dei requisiti, con tabelle, proprietà dei buoni requisiti e tecniche di validazione.

## Concetti adiacenti

- **se-analysis** — la fase subito dopo: dai requisiti si passa all'analisi e alla modellazione del sistema (le classi, i comportamenti).
- **se-process** — i modelli di processo (a cascata, iterativo, Agile) che dicono *quando* e *quanto spesso* si fa l'analisi dei requisiti.
- **xc-pm-prd** — il PRD (Product Requirements Document) e le user story: come i requisiti si scrivono nel mondo prodotto/Agile.
- **is-bpmn** — la modellazione dei processi di business (BPMN): serve a capire il dominio e i flussi prima di fissare i requisiti.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cos'è un **requisito**? E perché un errore nei requisiti scoperto tardi costa così tanto?
2. Qual è la differenza tra requisito **funzionale** e **non funzionale**? Fai un esempio di ciascuno preso da Signal.
3. Quali sono le **quattro attività** dell'analisi dei requisiti, in ordine?
4. Quali sono le **cinque proprietà** di un buon requisito?
5. Che differenza c'è tra **validazione** e **verifica**?
6. Cos'è un **attore** e cos'è un **caso d'uso**? Fai gli esempi di Signal.
7. Che differenza c'è tra le relazioni **include** ed **extend** tra casi d'uso?
8. Qual è la differenza tra un **caso d'uso** e uno **scenario**? Cosa sono il flusso principale e il flusso alternativo?
9. Cos'è un **misuse case** e cos'è un **security use case**? Fai un esempio da Signal.
10. Qual è il **formato di una user story**? Scrivine una per Signal.

<details><summary>Risposte</summary>

1. Un **requisito** è una **proprietà o un servizio che il sistema deve avere/offrire**. Un errore nei requisiti scoperto tardi costa **ordini di grandezza** in più perché si **propaga**: ci costruisci sopra analisi, design, codice e test; corretto in analisi cambi una riga (costa poco), corretto in produzione devi disfare e rifare tutto ciò che ci hai costruito sopra (costa tantissimo).

2. **Funzionale** = **cosa** fa il sistema (le funzioni): es. Signal *"l'utente può effettuare una segnalazione con posizione"*. **Non funzionale** = **come** deve farlo, cioè qualità e vincoli (prestazioni, sicurezza, usabilità, affidabilità, privacy): es. Signal i **requisiti di protezione dei dati (GDPR)**.

3. **Raccolta (elicitation) → Analisi (del dominio, con glossario) → Specifica → Validazione.**

4. Un buon requisito è **chiaro, non ambiguo, verificabile, tracciabile, consistente**.

5. **Validazione** = stiamo scrivendo i requisiti **giusti**? (il *sistema giusto*, lo giudica il **cliente/committente**). **Verifica** = stiamo costruendo il sistema **secondo i requisiti**? (il *sistema costruito bene*, si giudica rispetto alla specifica). In breve: validazione = bersaglio giusto; verifica = bersaglio centrato.

6. **Attore** = un **ruolo esterno** che interagisce col sistema (in Signal: **Utente/Cittadino** e **Amministratore**). **Caso d'uso** = una **funzionalità dal punto di vista dell'attore** con un obiettivo (in Signal: *Effettua Segnalazione*, *Visualizza Stato Segnalazione*, *Prendi in carico segnalazione*, ecc.).

7. **include** = un caso d'uso ne usa **sempre** un altro (pezzo obbligatorio, es. segnalare *include* essere autenticati). **extend** = aggiunge un **comportamento opzionale**, che scatta solo in certe condizioni (l'eccezione/variante).

8. Il **caso d'uso** è **astratto** (l'obiettivo, con tutti i suoi svolgimenti possibili); lo **scenario** è **una specifica esecuzione** del caso d'uso, raccontata passo per passo. Il **flusso principale** è la sequenza quando tutto va bene; il **flusso alternativo/eccezione** è cosa succede quando qualcosa devia (es. in "Effettua Segnalazione" la posizione manca → il sistema la richiede).

9. **Misuse case** = come un **attore ostile** attacca/usa male il sistema (es. Signal: inserire **segnalazioni false di massa**, o **accedere a dati altrui**). **Security use case** = la **contromisura** che neutralizza quel misuse case (es. autenticazione, limiti sul numero di segnalazioni, controlli di autorizzazione). Si ragiona a coppie minaccia–controllo.

10. Formato: **"Come [ruolo] voglio [obiettivo] così che [beneficio]."** Esempio Signal: *"Come cittadino voglio segnalare una buca così che venga riparata."* Si accompagna ai **criteri di accettazione** che la rendono verificabile.

</details>
