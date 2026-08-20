---
day: 12
topic_id: se-principles
title: "Principi di progettazione (rigidità/fragilità/immobilità, SOLID) e Design Pattern"
area: computer-science
course: Ingegneria del Software
grounded_in: "UNIBO/terzoAnno/IngengeriaDelSoftware (progetto Signal)"
adjacent: [se-patterns, se-arch, xc-swe-clean, prog-oop]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun acronimo lasciato senza definizione."
---

# Principi di progettazione e Design Pattern

> **Perché oggi:** far "funzionare il codice" non basta. Ciò che distingue un software engineer da chi mette insieme righe finché non gira è **progettare bene**: decidere come è fatto il sistema perché regga alle modifiche. Su Signal la tua parte era proprio l'**architettura**, cioè queste decisioni. E non è teoria da lasciare all'università: rigidità, fragilità, SOLID e i design pattern tornano a **ogni colloquio tecnico**, spesso con la domanda "come lo progetteresti?".

## Cosa vuol dire progettare (design)

Dopo aver raccolto i **requisiti** (cosa deve fare il sistema), arriva la **progettazione** (design): decidere **come** è fatto dentro. Il risultato principale è l'**architettura**, cioè quali **moduli** e **componenti** compongono il sistema e come **collaborano** tra loro. Un "modulo" è una parte del software con un confine chiaro (una classe, un package, un componente): la scatola con cui costruisci.

Il nemico numero uno del design è la **complessità**: un sistema grande, se lo pensi tutto insieme, non lo governi. Per domarla hai due armi che vanno sempre insieme:

- **Modularità** — dividi il sistema in **parti** più piccole e trattabili, invece di un unico blocco monolitico. Ogni parte la puoi capire, testare e modificare da sola.
- Il modo in cui dividi conta, e si misura con due proprietà:

**Coesione (cohesion)** — quanto le cose *dentro* un modulo sono legate a un unico scopo. **Alta coesione** significa che il modulo **fa una cosa sola, ben definita**: tutto ciò che c'è dentro serve a quello scopo. Un modulo `RicercaSegnalazioni` che si occupa *solo* di cercare segnalazioni è coeso; un modulo che cerca segnalazioni **e** manda email **e** gestisce il login è poco coeso (fa troppe cose scollegate).

**Accoppiamento (coupling)** — quanto un modulo **dipende** dagli altri. **Basso accoppiamento** significa che i moduli si conoscono poco: ognuno può cambiare dentro senza costringere gli altri a cambiare. Se per modificare la ricerca devi mettere mano anche a cinque altri moduli, l'accoppiamento è alto.

**La regola d'oro della progettazione è: alta coesione + basso accoppiamento.** Moduli che fanno una cosa sola (coesi) e dipendono poco l'uno dall'altro (disaccoppiati). Tutto il resto della lezione — sintomi, SOLID, pattern — è al servizio di questa regola.

## I tre sintomi del cattivo design (Robert Martin)

Come fai a sapere se un design è "marcio"? **Robert C. Martin** (detto "Uncle Bob", l'autore che ha reso popolari questi concetti e SOLID) elenca tre sintomi principali. Sono i segnali che il codice si sta degradando (cap. 7 del corso):

- **Rigidità (rigidity)** — il software è **difficile da modificare**: ogni cambiamento, anche piccolo, ne tira dietro tanti altri a catena. Vuoi toccare una cosa e ti accorgi di dover rimettere mano a dieci punti collegati. Cambiare costa tantissimo, quindi si evita di farlo.
- **Fragilità (fragility)** — quando modifichi un punto, **si rompe qualcosa in un altro punto lontano e non correlato**. Sistemi la ricerca e si guasta la notifica, che non c'entrava niente. Il software si spacca facilmente e in modi imprevedibili.
- **Immobilità (immobility)** — non riesci a **riusare** un pezzo in un altro progetto perché è troppo **intrecciato** col resto: per portarti via il modulo che ti serve dovresti trascinarti dietro mezzo sistema, e allora rinunci e riscrivi da capo.

Ci sono altri "odori" (code smells) minori che il corso cita di sfianco: la **viscosità** (fare la cosa giusta è più scomodo che fare la scorciatoia sporca, quindi il team peggiora il design), la **complessità inutile** (astrazioni e strutture messe "in caso servano" che non servono), la **ripetizione** (lo stesso codice copiato in più punti, che poi vanno corretti tutti a mano) e l'**opacità** (codice scritto in modo poco chiaro, difficile da leggere e capire).

## I principi SOLID (la cura)

**SOLID** è un **acronimo** che raccoglie **cinque principi di progettazione orientata agli oggetti** (object-oriented, cioè basata su classi e oggetti), formulati e resi popolari da **Robert C. Martin**. Ogni lettera è un principio. Servono esattamente a **combattere i tre sintomi** appena visti: applicandoli, il design resta flessibile invece di diventare rigido, fragile e immobile.

- **S — Single Responsibility Principle (SRP), Principio di responsabilità singola.** Una classe deve avere **una sola responsabilità**, cioè **un solo motivo per cambiare**. Se una classe si occupa di due cose diverse (per esempio calcolare qualcosa *e* salvarlo su file), due motivi diversi la fanno cambiare, e le due cose si intralciano. È l'alta coesione applicata alla singola classe.
- **O — Open/Closed Principle (OCP), Principio aperto/chiuso.** Un modulo deve essere **aperto all'estensione** ma **chiuso alla modifica**: devi poter **aggiungere** nuovi comportamenti **senza toccare** il codice già scritto e funzionante. Esempio Signal: se domani vuoi una **nuova categoria di segnalazione** (oltre a quelle esistenti), un buon design ti fa aggiungerla senza riscrivere il cuore del sistema che gestisce le segnalazioni — estendi, non modifichi.
- **L — Liskov Substitution Principle (LSP), Principio di sostituzione di Liskov.** Un **sottotipo** (una sottoclasse) deve poter **sostituire** il suo tipo base **senza rompere** il programma. Ovunque il codice si aspetta la classe base, deve poter ricevere una qualsiasi sua sottoclasse e continuare a funzionare correttamente. Se una sottoclasse si comporta in modo che "tradisce" le aspettative della base, viola LSP.
- **I — Interface Segregation Principle (ISP), Principio di segregazione delle interfacce.** Un'**interfaccia** (l'insieme di metodi che una classe promette di offrire) va tenuta **piccola e specifica**. Meglio **tante interfacce piccole e mirate** che un'unica interfaccia enorme: quest'ultima costringe chi la implementa a scrivere anche metodi che non gli servono, solo per rispettare il contratto.
- **D — Dependency Inversion Principle (DIP), Principio di inversione delle dipendenze.** Dipendi da **astrazioni** (interfacce), **non** da **implementazioni concrete**. Il modulo di alto livello non deve conoscere i dettagli del modulo di basso livello: entrambi si appoggiano a un'interfaccia condivisa. Così puoi sostituire l'implementazione concreta (per esempio scambiare come vengono inviate le notifiche) senza toccare chi la usa.

Il filo che li lega: **SOLID è la cura dei tre sintomi.** SRP e ISP alzano la **coesione**; DIP e OCP abbassano l'**accoppiamento** e rendono il codice estensibile; LSP tiene sane le gerarchie di ereditarietà. Insieme, un sistema SOLID è più facile da modificare (contro la **rigidità**), meno soggetto a rotture a distanza (contro la **fragilità**) e con pezzi più riusabili (contro l'**immobilità**).

## Design pattern (GoF)

Un **design pattern** ("schema di progettazione") è una **soluzione riutilizzabile a un problema ricorrente** di progettazione orientata agli oggetti. L'idea di fondo: certi problemi si ripresentano in mille progetti diversi, e per ognuno esiste uno schema collaudato per risolverlo bene. Invece di reinventare la ruota, riconosci il problema e applichi il pattern.

Attenzione: un pattern **non è codice pronto** da copiare-incollare. È uno **schema**, una descrizione di come organizzare classi e oggetti, che poi adatti al tuo caso e implementi nel tuo linguaggio.

Il catalogo di riferimento è quello dei **GoF — Gang of Four** ("banda dei quattro"), soprannome dei **quattro autori** del libro *"Design Patterns"* (1994): **Erich Gamma, Richard Helm, Ralph Johnson e John Vlissides**. Hanno raccolto e catalogato 23 pattern in **tre famiglie**, secondo il tipo di problema che risolvono:

- **Creazionali (creational)** — riguardano **come si creano gli oggetti**, nascondendo o controllando il processo di creazione.
  - **Singleton** — garantisce che di una certa classe esista **una sola istanza** in tutto il programma, con un punto di accesso globale. Utile per cose di cui deve esistere una copia unica, per esempio la **configurazione** dell'applicazione.
  - **Factory Method** ("metodo fabbrica") — invece di creare un oggetto con `new` direttamente, **deleghi la creazione a un metodo** (spesso ridefinito nelle sottoclassi), che decide *quale* tipo concreto creare. Esempio Signal: un metodo-fabbrica che, dato il tipo richiesto, crea l'oggetto giusto per quel tipo di segnalazione, senza che chi lo chiama debba sapere quale classe concreta viene istanziata.
- **Strutturali (structural)** — riguardano **come si compongono classi e oggetti** in strutture più grandi.
  - **Adapter** ("adattatore") — fa **combaciare due interfacce incompatibili**: avvolge una classe con un'interfaccia diversa da quella che offre, così che una parte del sistema possa usarla anche se "parla una lingua diversa". Come un adattatore per la presa elettrica.
  - **Facade** ("facciata") — mette **un'unica interfaccia semplice davanti a un sottosistema complesso**: nascondi tante classi e passaggi dietro un solo punto d'ingresso pulito, così chi lo usa non deve conoscere il groviglio interno.
- **Comportamentali (behavioral)** — riguardano **come le classi interagiscono** e si dividono le responsabilità a runtime.
  - **Observer** ("osservatore") — quando un oggetto **cambia stato**, **notifica automaticamente** tutti gli oggetti che si erano registrati come suoi "osservatori", senza che lui debba conoscerli uno per uno. Esempio Signal: quando una **segnalazione cambia stato** (es. viene presa in carico), notifica automaticamente chi la sta seguendo — l'utente che l'ha inviata e l'amministratore.
  - **Strategy** ("strategia") — incapsula **algoritmi intercambiabili** in classi separate e ti permette di **scegliere a runtime** quale usare, senza cambiare il codice che lo invoca. Vuoi ordinare i risultati in modi diversi? Ogni criterio è una "strategia" che puoi sostituire al volo.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 660 250" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arObsSig" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
   <rect x="240" y="18" width="180" height="52" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
   <text x="330" y="40">Segnalazione</text>
   <text x="330" y="57" font-size="10.5" fill="var(--muted)">(Soggetto / Subject)</text>

   <rect x="60" y="160" width="180" height="52" rx="9" fill="var(--card)" stroke="var(--rule)"/>
   <text x="150" y="183">Utente</text>
   <text x="150" y="200" font-size="10.5" fill="var(--muted)">(Observer)</text>

   <rect x="420" y="160" width="180" height="52" rx="9" fill="var(--card)" stroke="var(--rule)"/>
   <text x="510" y="183">Amministratore</text>
   <text x="510" y="200" font-size="10.5" fill="var(--muted)">(Observer)</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arObsSig)">
   <path d="M300,70 L165,158"/>
   <path d="M360,70 L495,158"/>
  </g>
  <g font-size="10" fill="var(--muted)" text-anchor="middle">
   <text x="205" y="120">notifica cambio stato</text>
   <text x="470" y="120">notifica cambio stato</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Pattern Observer su Signal: la Segnalazione (il Soggetto) tiene una lista di osservatori (Utente, Amministratore) e, quando cambia stato, li notifica tutti automaticamente — senza dover conoscere in anticipo chi sono.</figcaption>
</figure>

## Dal problema all'architettura (cenno al flusso del corso)

Come si arriva da un requisito a un'architettura fatta di moduli e pattern? Il percorso del corso, in sintesi:

1. Dai **casi d'uso** (le funzionalità richieste, es. *Effettua Segnalazione*, *Prendi in carico*, *Ricerca* su Signal) ricavi le **classi e i moduli** che servono: è il **modello statico**, la fotografia delle scatole del sistema e delle loro relazioni.
2. Descrivi le **interazioni** tra quelle classi — chi chiama chi, in che ordine, per realizzare ciascun caso d'uso: è il **modello dinamico**, il "film" di come collaborano nel tempo.
3. Su questa struttura **applichi i principi**: alta coesione e basso accoppiamento, e i cinque principi SOLID, per tenerla sana.
4. **Riconosci dove un pattern risolve un problema** ricorrente (es. Observer per le notifiche di cambio stato) e lo applichi — dove serve davvero, non a forza.

Il passaggio requisiti → classi/interazioni è approfondito in `se-analysis`; le viste e gli stili architetturali del sistema in `se-arch`.

## Errori comuni

- **Over-engineering (troppa ingegnerizzazione).** Infilare design pattern ovunque "perché fa figo" o "perché si è visto a lezione". I pattern **risolvono problemi**: se il problema non c'è, il pattern aggiunge solo complessità inutile (uno dei code smell visti sopra). Prima il problema, poi — semmai — il pattern.
- **Accoppiamento forte.** Moduli che si conoscono troppo e dipendono l'uno dall'altro nei dettagli: cambi uno e crolla tutto (rigidità e fragilità). Punta al basso accoppiamento, dipendi da astrazioni (DIP).
- **Classi-Dio (God class).** Un'unica classe enorme che fa tutto — cerca, notifica, salva, valida. Viola l'**SRP** (ha mille motivi per cambiare) ed è per definizione poco coesa. Spezzala in classi con una responsabilità ciascuna.
- **Ottimizzare prima di aver capito il design.** Mettersi a limare le prestazioni di un pezzo quando la struttura non è ancora chiara: ottimizzi cose che magari butterai, e complichi il codice. Prima un design pulito e corretto, poi — se e dove serve, misurando — l'ottimizzazione.

## Fonti

- **"Design Patterns: Elements of Reusable Object-Oriented Software"** (1994) — Erich **Gamma**, Richard **Helm**, Ralph **Johnson**, John **Vlissides** (i **Gang of Four**): il catalogo originale dei 23 pattern nelle tre famiglie (creazionali, strutturali, comportamentali).
- **Robert C. Martin** — *"Clean Architecture"* e *"Agile Software Development: Principles, Patterns, and Practices"*: la formulazione dei principi **SOLID** e dei sintomi del cattivo design (rigidità, fragilità, immobilità).
- **refactoring.guru** — catalogo dei design pattern illustrato, con spiegazioni ed esempi visivi per ciascun pattern.

## Concetti adiacenti

- **se-patterns** — approfondimento sui singoli design pattern GoF, uno per uno con struttura e casi d'uso.
- **se-arch** — le viste architetturali e gli stili (a livelli, a componenti) in cui i principi di questa lezione prendono forma nel sistema.
- **xc-swe-clean** — clean code e clean architecture nella pratica quotidiana da software engineer: naming, funzioni piccole, confini tra strati.
- **prog-oop** — le basi della programmazione a oggetti (classi, ereditarietà, interfacce, polimorfismo) su cui poggiano SOLID e i pattern.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cosa sono **coesione** e **accoppiamento**, e qual è la **regola d'oro** della progettazione?
2. Cos'è la **modularità** e a cosa serve nel domare la complessità?
3. Elenca e spiega i **tre sintomi** del cattivo design secondo Robert Martin.
4. Cosa vuol dire l'acronimo **SOLID** e chi lo ha formulato?
5. Spiega la **S** e la **O** di SOLID (nome per esteso e significato), con un esempio per la O.
6. Spiega la **D** di SOLID (nome per esteso e significato).
7. Cos'è un **design pattern** e chi sono i **GoF**? A cosa si riferisce l'acronimo?
8. Quali sono le **tre famiglie** di design pattern e cosa distingue ciascuna? Fai un esempio per famiglia.
9. Cosa fa il pattern **Observer**? Spiegalo con l'esempio di Signal.
10. Cos'è l'**over-engineering** e perché è un errore?

<details><summary>Risposte</summary>

1. La **coesione** misura quanto le cose *dentro* un modulo sono legate a un unico scopo: alta coesione = il modulo fa **una cosa sola, ben definita**. L'**accoppiamento** misura quanto un modulo **dipende** dagli altri: basso accoppiamento = i moduli si conoscono poco e possono cambiare senza costringere gli altri a cambiare. La **regola d'oro** è **alta coesione + basso accoppiamento**.

2. La **modularità** è dividere il sistema in **parti** più piccole e trattabili invece di un unico blocco monolitico, così ogni parte si può capire, testare e modificare da sola. Serve a domare la **complessità**, che altrimenti rende il sistema ingovernabile.

3. **Rigidità**: il software è difficile da modificare perché ogni cambiamento ne tira dietro altri a catena. **Fragilità**: modificare un punto **rompe** cose in punti lontani e non correlati. **Immobilità**: non riesci a **riusare** un pezzo in un altro progetto perché è troppo intrecciato col resto.

4. **SOLID** è un acronimo che raccoglie **cinque principi di progettazione orientata agli oggetti** (una lettera per principio), formulati e resi popolari da **Robert C. Martin** ("Uncle Bob"). Servono a combattere i tre sintomi del cattivo design.

5. **S — Single Responsibility Principle (SRP)**, principio di responsabilità singola: una classe deve avere **una sola responsabilità**, cioè un solo motivo per cambiare. **O — Open/Closed Principle (OCP)**, principio aperto/chiuso: aperto all'**estensione**, chiuso alla **modifica** — aggiungi comportamenti senza toccare il codice esistente. Esempio: una nuova **categoria di segnalazione** su Signal si aggiunge senza riscrivere il cuore del sistema.

6. **D — Dependency Inversion Principle (DIP)**, principio di inversione delle dipendenze: dipendi da **astrazioni** (interfacce), non da **implementazioni concrete**. Il modulo di alto livello non conosce i dettagli di quello di basso livello: entrambi si appoggiano a un'interfaccia condivisa, così puoi sostituire l'implementazione concreta senza toccare chi la usa.

7. Un **design pattern** è una **soluzione riutilizzabile a un problema ricorrente** di progettazione a oggetti: non codice pronto, ma uno **schema** da adattare. I **GoF (Gang of Four)** sono i **quattro autori** del libro *"Design Patterns"* (1994): Gamma, Helm, Johnson, Vlissides. L'acronimo GoF significa "banda dei quattro".

8. **Creazionali**: come si **creano** gli oggetti (es. Singleton, Factory Method). **Strutturali**: come si **compongono** classi e oggetti (es. Adapter, Facade). **Comportamentali**: come le classi **interagiscono** a runtime (es. Observer, Strategy).

9. L'**Observer** fa sì che quando un oggetto **cambia stato** notifichi **automaticamente** tutti gli oggetti registrati come suoi "osservatori", senza doverli conoscere uno per uno. Su Signal: quando una **segnalazione cambia stato** (es. viene presa in carico), notifica automaticamente chi la segue — l'utente che l'ha inviata e l'amministratore.

10. L'**over-engineering** è infilare design pattern (o astrazioni) ovunque "perché fa figo", anche dove non servono. È un errore perché i pattern **risolvono problemi**: se il problema non c'è, il pattern aggiunge solo **complessità inutile**. Prima il problema, poi eventualmente il pattern.

</details>
