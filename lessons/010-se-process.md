---
day: 10
topic_id: se-process
title: "Ingegneria del Software — processo di sviluppo e ciclo di vita"
area: computer-science
course: Ingegneria del Software
grounded_in: "UNIBO/terzoAnno/IngengeriaDelSoftware (progetto Signal)"
adjacent: [se-requirements, pm-agile, xc-swe-tdd]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo."
---

# Ingegneria del Software — processo e ciclo di vita

> **Perché oggi:** è il tuo corso di terzo anno e la base per lavorare da software/system engineer — decidere *come* si costruisce un sistema, non solo scriverlo. L'hai applicato davvero su **Signal** (gruppo 13), dove curavi **analisi dei requisiti** e **architettura**: proprio le prime fasi del processo che stai per ripassare. In colloquio queste domande arrivano quasi sempre ("waterfall o Agile?", "verifica o validazione?"): qui hai le risposte pronte e collegate a un progetto vero.

## Cos'è l'ingegneria del software

**Ingegneria del software (Software Engineering)** = l'applicazione di un approccio **sistematico, disciplinato e quantificabile** allo sviluppo, al funzionamento e alla manutenzione del software. Scomponiamo i tre aggettivi, perché sono il cuore della definizione:

- **sistematico** = segui un metodo ripetibile, non improvvisi;
- **disciplinato** = ti attieni a regole, standard e processi condivisi dal team;
- **quantificabile** = misuri (tempi, costi, difetti, qualità), così puoi controllare e migliorare.

Il punto chiave: **non è "programmare", è ingegnerizzare un sistema** sotto vincoli reali di **costo**, **tempo**, **qualità** e **team** (più persone che lavorano insieme). Programmare è una delle attività dentro l'ingegneria del software, non tutto il lavoro.

**Programma vs prodotto software** — la distinzione che spiega perché serve un'ingegneria:

- Un **programma** lo scrivi **tu**, è **piccolo**, lo usi tu, di solito senza documentazione, senza test formali, senza manutenzione. Funziona "abbastanza" per il tuo scopo.
- Un **prodotto software** è **usato da altri**, quindi va **documentato** (per chi lo usa e per chi lo manterrà), **testato** (deve reggere input e casi che tu non avevi previsto), **mantenuto** nel tempo (bug, nuovi ambienti, nuove richieste) e progettato per essere **affidabile**.

Costruire un prodotto costa **molto di più** che scrivere il programma equivalente: in letteratura si cita un **fattore moltiplicativo** — un prodotto software costa **diverse volte** (in ordine di grandezza, non "un po' di più") ciò che costa il programma nudo, proprio per via di documentazione, test, robustezza e manutenzione. **Signal** è un **prodotto**: web-app di segnalazioni civiche usata da cittadini e amministratori, quindi ha richiesto documento dei requisiti, casi d'uso, architettura, non solo "codice che gira".

## La qualità del software

La qualità non è una cosa sola: è un insieme di **attributi**. Definiamoli uno per uno (in colloquio bastano tre-quattro, ma sappili tutti).

- **Correttezza (correctness):** il software fa **esattamente** quello che la specifica dice. È un giudizio **binario** rispetto ai requisiti: o è conforme, o non lo è.
- **Affidabilità (reliability):** si comporta come atteso **il più delle volte, nel tempo**. È statistica: quanto raramente sbaglia durante l'uso normale.
- **Robustezza (robustness):** si comporta "ragionevolmente" anche in situazioni **non previste** dalla specifica (input strani, errori dell'utente, guasti) — non crolla di brutto.
- **Usabilità (usability):** quanto è **facile** da imparare e da usare per l'utente finale.
- **Efficienza (efficiency):** quanto bene usa le **risorse** (tempo di CPU, memoria, rete) — le prestazioni.
- **Manutenibilità (maintainability):** quanto è **facile modificarlo** dopo il rilascio (correggere bug, aggiungere funzioni).
- **Portabilità (portability):** quanto è facile **spostarlo** su un ambiente diverso (altro sistema operativo, altra piattaforma).
- **Riusabilità (reusability):** quanto i suoi pezzi possono essere **riutilizzati** in altri sistemi o progetti.

**Qualità esterne vs interne** — chi le vede?

- **Esterne** = visibili dall'**utente** che usa il prodotto: es. **correttezza**, **affidabilità**, **usabilità**, **efficienza**.
- **Interne** = visibili solo dagli **sviluppatori** che leggono e toccano il codice: es. **manutenibilità**, **leggibilità** del codice, buona struttura.
- Il legame: le interne **abilitano** le esterne. Codice ben scritto e manutenibile (interna) rende più facile ottenere correttezza e affidabilità (esterne) nel tempo.

**Verifica vs validazione** — due domande diverse, entrambe necessarie:

- **Verifica** (*verification*): «Stiamo costruendo il prodotto **bene**?» → controlli che ciò che hai costruito sia conforme alla **specifica** (rispetta i requisiti scritti). *Build the product right.*
- **Validazione** (*validation*): «Stiamo costruendo il prodotto **giusto**?» → controlli che la specifica stessa sia quella che il cliente **voleva davvero**. *Build the right product.*

Esempio su Signal: **verificare** = controllare che la funzione "Effettua Segnalazione" faccia esattamente ciò che il caso d'uso descrive. **Validare** = accertarsi che quel caso d'uso rispecchi ciò che il committente voleva (che cioè avessimo capito il problema, non solo implementato bene una specifica sbagliata).

## Le attività del processo (a cosa servono)

Il **processo di sviluppo** è la sequenza di **attività** (o **fasi**) che porta dall'idea al software in esercizio. Il **ciclo di vita (software life cycle)** è l'intero arco di vita del prodotto, dall'idea fino alla dismissione. Ecco le fasi classiche, una riga a cosa serve ciascuna:

1. **Studio di fattibilità:** capire *se conviene* farlo — costi, benefici, alternative, rischi macro. Output: si fa / non si fa.
2. **Analisi e specifica dei requisiti:** capire e scrivere *cosa* deve fare il sistema (non come). Output: il **documento dei requisiti** con requisiti e casi d'uso. *In Signal questa fase produceva la **tabella dei requisiti** e i **casi d'uso** — Login, Registrazione, Effettua Segnalazione, ecc. — ed era la tua parte.*
3. **Analisi del rischio:** individuare cosa può andare storto (tecnico, di sicurezza, di progetto) e come contrastarlo. *In Signal produceva l'elenco di **minacce** e dei **controlli/contromisure** per mitigarle.*
4. **Progettazione (design):** decidere *come* realizzarlo — l'**architettura** (componenti e loro relazioni) e il dettaglio dei moduli. *In Signal, l'altra tua parte.*
5. **Realizzazione / codifica (coding):** scrivere il **codice** che implementa il design.
6. **Collaudo (testing) dei moduli:** provare ogni **singolo modulo** in isolamento per trovarne i difetti (unit test).
7. **Integrazione e collaudo del sistema:** unire i moduli e verificare che **insieme** funzionino, incluso il collaudo dell'intero sistema.
8. **Utilizzo e manutenzione:** il software è in esercizio e va tenuto in vita — correzioni e miglioramenti (vedi sezione dedicata).

## Il modello a cascata, in figura

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 640 470" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arWf10" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
   <rect x="40" y="20" width="200" height="42" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="140" y="46">Requisiti</text>
   <rect x="130" y="95" width="200" height="42" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="230" y="121">Progettazione</text>
   <rect x="220" y="170" width="200" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="320" y="196">Codifica</text>
   <rect x="310" y="245" width="200" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="410" y="271">Collaudo moduli</text>
   <rect x="360" y="320" width="220" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="470" y="346">Integrazione e collaudo</text>
   <rect x="380" y="400" width="220" height="42" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="490" y="426">Manutenzione</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arWf10)">
   <path d="M140,62 L200,93"/>
   <path d="M230,137 L290,168"/>
   <path d="M320,212 L380,243"/>
   <path d="M410,287 L450,318"/>
   <path d="M470,362 L500,398"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Waterfall: le fasi scendono in sequenza, una completata prima della successiva. Idealmente si scende soltanto — non si torna su.</figcaption>
</figure>

## I modelli di processo

Un **modello di processo** è uno **schema** che dice **in che ordine e con quale logica** eseguire le attività. Gli stessi lavori (requisiti, design, codice, test) possono essere organizzati in modi molto diversi. Vediamo i principali con pro, contro e **quando** usarli.

### Waterfall (a cascata)

Le fasi si eseguono **in sequenza rigida**: ogni fase viene **completata** (e documentata) **prima** di iniziare la successiva, come acqua che scende una cascata. Si producono **molti documenti** che fanno da "consegna" tra una fase e l'altra.

- **Pro:** è **chiaro** e **tracciabile** (sai sempre a che punto sei), facile da pianificare e da gestire con contratti/scadenze, ottima documentazione.
- **Contro:** è **rigido**. I **requisiti si "congelano" all'inizio** (devono essere tutti chiari e stabili subito — nella realtà quasi mai lo sono). Il **cliente vede il prodotto solo alla fine**, quindi se avevate frainteso te ne accorgi troppo tardi. E ogni **cambiamento costa carissimo**, perché ti costringe a tornare indietro attraverso fasi già "chiuse".

### Modello incrementale / iterativo

Invece di costruire tutto in un colpo e consegnare alla fine, costruisci il sistema **a pezzi successivi**, consegnando valore prima e **incorporando il feedback** man mano. Attenzione alla distinzione (spesso confusa):

- **Incrementale:** **aggiungi pezzi** nuovi ogni volta. Costruisci il sistema per **incrementi**: prima un sottoinsieme funzionante di funzionalità, poi ne aggiungi altre, e così via — come mattoni che si sommano.
- **Iterativo:** **raffini lo stesso pezzo**. Fai una prima versione (anche grezza) e poi la **rivedi e migliori** in **iterazioni** successive, tornando sulle stesse funzionalità per renderle migliori.

Nella pratica i due si combinano: aggiungi funzioni **e** raffini quelle esistenti. **Pro:** consegni valore presto, riduci il rischio (scopri i problemi prima), integri il feedback del cliente. **Contro:** serve più coordinamento e una buona architettura di base per non rifare tutto a ogni giro.

### Prototipazione

Costruisci un **prototipo** = una versione **parziale e provvisoria** del sistema, fatta apposta per **chiarire requisiti incerti** prima di impegnarsi sul prodotto vero. Due tipi:

- **Usa-e-getta (throwaway):** lo fai solo per capire/mostrare qualcosa (es. l'aspetto delle schermate), poi lo **butti** e riparti pulito.
- **Evolutivo:** parti da un prototipo e lo **fai crescere** fino a diventare il prodotto finale.

Serve quando il cliente non sa bene cosa vuole: gli mostri qualcosa di concreto, lui reagisce, e i requisiti si chiariscono.

### Modello a spirale (cenno)

Il processo è una **spirale** di iterazioni, ognuna guidata dal **rischio**: a ogni giro **valuti i rischi prima di procedere** (prototipi, analisi, decisioni), e vai avanti solo dopo averli affrontati. Utile per progetti grossi e incerti dove il rischio è il fattore dominante.

### Agile e Scrum

**Agile** è una **famiglia di metodi** basata sul **Manifesto Agile** (2001), che fissa **quattro valori** (a sinistra ciò che conta di più, senza buttare via ciò a destra):

1. **Individui e interazioni** più che processi e strumenti;
2. **Software funzionante** più che documentazione esaustiva;
3. **Collaborazione col cliente** più che negoziazione dei contratti;
4. **Rispondere al cambiamento** più che seguire un piano rigido.

L'idea di fondo: cicli **brevi**, feedback **continuo**, e **abbracciare il cambiamento** invece di temerlo.

**Scrum** è il framework Agile più diffuso. Definiamone i pezzi:

- **Ruoli:**
  - **Product Owner (PO):** rappresenta il cliente/business; decide **cosa** fare e con quale **priorità** (possiede il product backlog).
  - **Scrum Master:** facilita il processo, rimuove gli ostacoli (impedimenti) e fa rispettare Scrum; **non** è un capo che comanda.
  - **Team (Development Team):** chi realizza il software; è **auto-organizzato** (decide *come* fare il lavoro).
- **Sprint:** un'**iterazione breve a durata fissa** (*time-box*, es. **2 settimane**) al termine della quale c'è un **incremento** di software potenzialmente rilasciabile. La durata non cambia in corsa.
- **Backlog:**
  - **Product backlog:** la lista **ordinata per priorità** di tutto ciò che serve al prodotto (funzionalità, fix), gestita dal PO.
  - **Sprint backlog:** il sottoinsieme di elementi che il team si impegna a fare **in questo sprint**.
- **Cerimonie (eventi):**
  - **Sprint planning:** all'inizio dello sprint, si sceglie *cosa* fare e si riempie lo sprint backlog.
  - **Daily standup (daily scrum):** riunione **giornaliera** breve (in piedi) — cosa ho fatto, cosa farò, quali ostacoli.
  - **Sprint review:** alla fine, si mostra l'incremento al cliente/stakeholder per avere **feedback**.
  - **Retrospective:** alla fine, il team riflette su **come ha lavorato** e cosa migliorare nel prossimo sprint.

**Pro:** flessibile ai cambiamenti, feedback continuo, il cliente vede software funzionante presto e spesso. **Contro:** **meno prevedibile** su scadenze e budget fissi (è difficile promettere "tutto questo entro quella data a quel prezzo"), e **richiede un cliente coinvolto** e disponibile. Approfondimento in `pm-agile`.

## Waterfall vs Agile: quando l'uno, quando l'altro

Non c'è un vincitore assoluto: dipende dal contesto.

- **Waterfall** quando i **requisiti sono stabili** e i vincoli sono rigidi: sistemi **safety-critical** (dove un errore fa danni gravi e serve documentazione e tracciabilità formale), **appalti pubblici** e contratti a prezzo/scope fisso, ambiti fortemente regolati.
- **Agile** quando i **requisiti sono incerti o mutevoli** e serve **feedback frequente**: è il caso della **maggior parte del software prodotto oggi** (prodotti web/mobile, startup, evoluzione continua), dove capisci cosa serve **mentre** costruisci.

Regola mnemonica: **requisiti chiari e fissi → waterfall; requisiti che cambiano → Agile.**

## La manutenzione (spesso dimenticata)

Nei corsi si parla tanto di sviluppo, ma nel ciclo di vita reale la **manutenzione** è la fase **più lunga e più costosa**: il software vive anni dopo il rilascio, e continuare a tenerlo in vita pesa più di averlo scritto. Quattro tipi:

- **Correttiva:** **correggi i bug** scoperti dopo il rilascio.
- **Adattativa:** adegui il software a un **nuovo ambiente** (nuovo sistema operativo, nuova versione di una libreria, nuovo hardware).
- **Perfettiva:** aggiungi **nuove funzioni** o **migliori** quelle esistenti (spesso la fetta più grande, perché nasce dalle richieste degli utenti).
- **Preventiva:** intervieni **prima** che si manifesti un problema, per rendere il software più solido e più facile da mantenere in futuro (es. ristrutturare codice fragile).

## Notable use cases

- **Waterfall** è storicamente il modello dei contesti **safety-critical** (avionica, dispositivi medici, ferroviario) e degli **appalti pubblici**, dove la tracciabilità formale e i requisiti fissati a contratto contano più della flessibilità.
- **Agile / Scrum** è oggi lo standard di fatto nello sviluppo di **software di prodotto** moderno (web, mobile, SaaS), dove i requisiti evolvono e il feedback rapido è un vantaggio competitivo.

(Nessun dettaglio proprietario specifico: sono le categorie tipiche in cui ciascun approccio è la scelta naturale.)

## Fonti

- **Ian Sommerville — "Software Engineering"**: il libro di riferimento del corso e del settore (processo, requisiti, design, qualità).
- **Manifesto Agile** — agilemanifesto.org: i quattro valori e i dodici principi Agile, testo originale.
- **Scrum Guide** — scrumguides.org: la definizione ufficiale di Scrum (ruoli, eventi, artefatti), di Schwaber e Sutherland.

## Concetti adiacenti

- **se-requirements:** l'analisi e la specifica dei requisiti in dettaglio (casi d'uso, requisiti funzionali e non funzionali) — la fase che curavi in Signal.
- **se-principles:** i principi di ingegneria del software (modularità, astrazione, incapsulamento, separazione delle responsabilità) che guidano la fase di progettazione.
- **pm-agile:** Agile e Scrum dal punto di vista della **gestione** di prodotto/progetto (backlog, priorità, ruolo del PO).
- **xc-swe-tdd:** il **testing** e il Test-Driven Development, che riempiono di pratica le fasi di collaudo del processo.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Qual è la differenza tra un **programma** e un **prodotto software**, e perché il secondo costa molto di più?
2. Definisci **tre** attributi di qualità del software (a scelta), e di' cosa significa che un attributo è **esterno** o **interno**.
3. Cosa distingue la **verifica** dalla **validazione**? Sintetizza ciascuna con la sua domanda.
4. Elenca le fasi classiche del processo di sviluppo, dalla fattibilità alla manutenzione.
5. Quali sono i principali **difetti del waterfall**?
6. Che differenza c'è tra approccio **incrementale** e approccio **iterativo**?
7. In Scrum: quali sono i **tre ruoli**, cos'è uno **sprint** e nomina almeno **tre eventi**.
8. Quali sono i **quattro tipi di manutenzione** e cosa fa ciascuno?
9. **Quando** conviene il waterfall e **quando** conviene Agile?
10. Cos'è l'**ingegneria del software** (i tre aggettivi della definizione) e su quali **vincoli** lavora?

<details><summary>Risposte</summary>

1. Un **programma** lo scrivi tu, è piccolo, lo usi tu, senza documentazione/test/manutenzione. Un **prodotto software** è usato da altri, quindi va **documentato**, **testato**, **mantenuto** e reso **affidabile/robusto**. Costa di più — un **fattore moltiplicativo**, diverse volte tanto — proprio per documentazione, test, robustezza e manutenzione. Signal è un prodotto (web-app di segnalazioni civiche usata da cittadini e amministratori).
2. Tre esempi: **correttezza** (fa esattamente ciò che dice la specifica), **usabilità** (facile da usare per l'utente), **manutenibilità** (facile da modificare dopo il rilascio). **Esterno** = visto dall'**utente** (es. correttezza, usabilità, affidabilità, efficienza); **interno** = visto dagli **sviluppatori** (es. manutenibilità, leggibilità del codice).
3. **Verifica** = «stiamo costruendo il prodotto **bene**?» → conformità alla specifica (build the product right). **Validazione** = «stiamo costruendo il prodotto **giusto**?» → la specifica è davvero ciò che il cliente voleva (build the right product).
4. **Studio di fattibilità → analisi e specifica dei requisiti → analisi del rischio → progettazione (design) → realizzazione/codifica → collaudo dei moduli → integrazione e collaudo del sistema → utilizzo e manutenzione.**
5. È **rigido**; i **requisiti si congelano all'inizio** (irrealistico); il **cliente vede il prodotto solo alla fine**; i **cambiamenti costano carissimo** perché obbligano a tornare su fasi già chiuse.
6. **Incrementale** = **aggiungi pezzi** nuovi a ogni giro (nuove funzionalità che si sommano). **Iterativo** = **raffini lo stesso pezzo**, migliorando in iterazioni successive funzionalità già esistenti. Nella pratica si combinano.
7. Ruoli: **Product Owner** (decide cosa e con che priorità), **Scrum Master** (facilita, rimuove ostacoli), **Team** (auto-organizzato, realizza). **Sprint** = iterazione breve a **durata fissa** (time-box, es. 2 settimane) che produce un incremento rilasciabile. Eventi (almeno tre): **sprint planning, daily standup, sprint review, retrospective**.
8. **Correttiva** (correggi bug); **adattativa** (adegui a un nuovo ambiente/OS); **perfettiva** (nuove funzioni o migliorie); **preventiva** (intervieni prima che nasca un problema, per solidità futura).
9. **Waterfall** con **requisiti stabili** e vincoli rigidi (safety-critical, appalti pubblici, ambiti regolati). **Agile** con **requisiti incerti/mutevoli** e bisogno di **feedback frequente** — la maggior parte del software prodotto oggi.
10. **Ingegneria del software** = applicazione di un approccio **sistematico** (metodo ripetibile), **disciplinato** (regole e standard) e **quantificabile** (misurabile) allo sviluppo del software. Lavora sotto i **vincoli** di **costo, tempo, qualità e team**.

</details>
