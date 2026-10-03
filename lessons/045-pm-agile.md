---
day: 45
topic_id: pm-agile
title: "Agile e Scrum"
area: management
course: "Project Management"
grounded_in: null
adjacent: [se-process, pm-lifecycle, xc-pm-role]
completeness_checked: true
quiz_count: 10
---

# Agile e Scrum

> **Perché oggi:** Agile è il modo in cui si gestisce la maggior parte dei progetti software di oggi, e "come funziona Scrum" è una delle domande più ricorrenti in un colloquio tecnico o gestionale. Nel tema `se-process` hai già visto Agile come uno dei modelli di ciclo di vita, accanto a waterfall e incrementale. Qui lo guardiamo dal punto di vista della **gestione del progetto e del prodotto**: cosa dice davvero il Manifesto, come è fatto il framework Scrum nella sua definizione ufficiale aggiornata, come si stima e si misura il lavoro, e in cosa Scrum differisce da Kanban. L'obiettivo è saperlo spiegare con precisione, senza confondere i termini.

## Cos'è Agile: il Manifesto
**Agile** non è un metodo unico ma una **famiglia di approcci** allo sviluppo iterativo, uniti da un insieme di principi fissati nel **Manifesto Agile** (2001). Il Manifesto contiene **quattro valori** e **dodici principi**.

I **quattro valori** sono scritti come confronti (a sinistra ciò che conta di più, senza buttare via ciò a destra):
1. **Individui e interazioni** più che processi e strumenti;
2. **Software funzionante** più che documentazione esaustiva;
3. **Collaborazione col cliente** più che negoziazione dei contratti;
4. **Rispondere al cambiamento** più che seguire un piano.

L'idea di fondo è governare l'incertezza con **cicli brevi** e **feedback frequente**: invece di decidere tutto all'inizio (come nel waterfall) e scoprire gli errori alla fine, si costruisce un pezzo, lo si mostra, si impara e si corregge la rotta. Tra i dodici principi vale la pena ricordarne alcuni: consegnare valore **presto e con continuità**, **accogliere i cambiamenti** anche tardi, consegnare software funzionante **di frequente**, misurare l'avanzamento soprattutto con il **software funzionante**, e riflettere a intervalli regolari su come migliorare.

Agile non è una cosa sola: **Scrum** e **Kanban** sono i due approcci più diffusi, e **Extreme Programming (XP)** aggiunge pratiche tecniche (test automatici, integrazione continua, pair programming). Scrum è di gran lunga il più usato, e il resto della lezione si concentra su di esso.

## Scrum: il framework
**Scrum** è un framework leggero per affrontare problemi complessi consegnando valore in modo iterativo. È definito dalla **Scrum Guide**, scritta dai suoi creatori Ken Schwaber e Jeff Sutherland e aggiornata l'ultima volta nel 2020. Scrum si regge su **tre pilastri** empirici: **trasparenza** (il lavoro è visibile a tutti), **ispezione** (si controlla spesso l'avanzamento) e **adattamento** (si corregge in base a ciò che si è ispezionato). È un approccio **empirico**: si decide in base a ciò che si osserva, non a un piano fissato una volta per tutte.

### I tre ruoli (accountabilities)
Lo **Scrum Team** è piccolo (tipicamente fino a una decina di persone) e ha tre responsabilità:
- **Product Owner (PO):** è responsabile di **massimizzare il valore** del prodotto. Decide **cosa** fare e con quale **priorità**, ed è l'unico proprietario del product backlog. Rappresenta clienti e business verso il team.
- **Scrum Master (SM):** è responsabile dell'**efficacia** dello Scrum Team. Facilita, rimuove gli **impedimenti** (ostacoli), allena il team all'auto-organizzazione e protegge il processo, agendo da servitore del team (**servant leader**) più che da capo che assegna i compiti.
- **Developers (sviluppatori):** chi realizza concretamente l'incremento (non solo programmatori: chiunque contribuisca a costruirlo). Sono **auto-organizzati**, cioè decidono **come** fare il lavoro.

Una nota di terminologia: la Scrum Guide 2020 parla di **Developers**; versioni precedenti usavano "Development Team". È lo stesso gruppo, con un nome aggiornato per sottolineare che il team è uno solo.

### Gli artefatti e i loro impegni
Scrum ha **tre artefatti**, ciascuno legato a un **impegno (commitment)** che lo rende misurabile:
- **Product backlog:** la lista **ordinata per priorità** di tutto ciò che potrebbe servire al prodotto (funzioni, correzioni, miglioramenti), gestita dal PO. Il suo impegno è il **Product Goal**, l'obiettivo di lungo periodo verso cui punta il prodotto.
- **Sprint backlog:** il sottoinsieme di elementi che il team si impegna a realizzare **in questo sprint**, più il piano per farlo. Il suo impegno è lo **Sprint Goal**, l'obiettivo unico dello sprint.
- **Increment (incremento):** la somma del lavoro completato e utilizzabile. Il suo impegno è la **Definition of Done (DoD):** la definizione condivisa di "fatto", cioè i criteri di qualità che un elemento deve soddisfare per dirsi completato (es. testato, documentato, revisionato). Senza DoD, "finito" vuol dire cose diverse per persone diverse.

Il **refinement** (rifinitura del backlog), cioè l'attività continua di chiarire, stimare e spezzare gli elementi del product backlog, **non è un evento** formale di Scrum ma un'attività che il team svolge con continuità.

### Gli eventi e i loro time-box
Tutto avviene dentro lo **Sprint**, l'iterazione a **durata fissa** (al massimo un mese, spesso due settimane) che fa da contenitore a tutti gli altri eventi. La durata non cambia a sprint iniziato, e appena finisce ne comincia subito un altro. Un **time-box** è la durata **massima** riservata a un evento. Per uno sprint di un mese la Scrum Guide indica questi limiti (che si scalano in proporzione per sprint più brevi):
- **Sprint Planning** (pianificazione, massimo 8 ore): si definiscono lo Sprint Goal e lo sprint backlog, rispondendo a "perché questo sprint ha valore", "cosa si può fare" e "come".
- **Daily Scrum** (daily, 15 minuti, ogni giorno): i Developers sincronizzano il lavoro e ripianificano la giornata verso lo Sprint Goal. È loro, breve, quotidiano.
- **Sprint Review** (revisione, massimo 4 ore): a fine sprint si mostra l'incremento agli stakeholder per raccogliere **feedback** e adattare il product backlog.
- **Sprint Retrospective** (retrospettiva, massimo 3 ore): il team riflette su **come ha lavorato** (persone, relazioni, processo, strumenti) e sceglie miglioramenti per lo sprint successivo.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 660 300" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arScr" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
    <rect x="20" y="120" width="120" height="60" rx="9" fill="var(--card2)" stroke="var(--rule)"/><text x="80" y="145">Product</text><text x="80" y="162">backlog</text>
    <rect x="175" y="124" width="120" height="52" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="235" y="146">Sprint</text><text x="235" y="163">planning</text>
    <circle cx="430" cy="150" r="72" fill="none" stroke="var(--accent)" stroke-width="1.7"/>
    <text x="430" y="138" font-weight="700">Sprint</text><text x="430" y="156" font-size="10" fill="var(--muted)">max 1 mese</text><text x="430" y="172" font-size="10" fill="var(--muted)">daily 15 min</text>
    <rect x="560" y="88" width="90" height="46" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="605" y="108" font-size="10.5">Review</text><text x="605" y="123" font-size="9.5" fill="var(--muted)">feedback</text>
    <rect x="560" y="166" width="90" height="46" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="605" y="186" font-size="10.5">Retro</text><text x="605" y="201" font-size="9.5" fill="var(--muted)">processo</text>
    <rect x="360" y="256" width="140" height="34" rx="7" fill="var(--card)" stroke="var(--good)" stroke-width="1.5"/><text x="430" y="277" font-size="10.5">Incremento (Done)</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none" marker-end="url(#arScr)">
    <path d="M140,150 L172,150"/>
    <path d="M295,150 L355,150"/>
    <path d="M500,135 L557,115"/>
    <path d="M500,165 L557,185"/>
    <path d="M430,222 L430,254"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Il ciclo Scrum: dal product backlog si seleziona il lavoro in sprint planning; durante lo sprint (con daily quotidiani) i Developers producono un incremento "Done"; a fine sprint la review raccoglie feedback e la retrospettiva migliora il processo. Poi si ricomincia.</figcaption>
</figure>

## Stima e misura: story point, velocity, burndown
Gli elementi di backlog si stimano spesso in **story point:** un'unità **relativa** di sforzo, che mette insieme complessità, incertezza e quantità di lavoro. Si usa il relativo (questa cosa è il doppio di quella) perché le persone stimano meglio a confronto che in ore assolute. Una tecnica comune è il **planning poker**, in cui ciascuno stima in contemporanea con carte (spesso una scala tipo Fibonacci: 1, 2, 3, 5, 8, 13) e si discute sulle differenze.

La **velocity** è quanti story point il team completa **mediamente** per sprint: serve a prevedere quanti sprint servono per un dato backlog, ma è una misura **interna** del team e non va usata per confrontare team diversi. Il **burndown chart** mostra il lavoro residuo che scende verso zero nello sprint (o nel rilascio): dà un colpo d'occhio sull'avanzamento.

Attenzione, dettaglio da colloquio: **story point, velocity, planning poker e burndown non fanno parte della Scrum Guide**. Sono **pratiche diffuse** nate attorno a Scrum e a XP, utili ma non obbligatorie. Confonderle con la definizione ufficiale di Scrum è l'errore classico.

## Scrum vs Kanban
Sono due modi diversi di applicare Agile:
- **Scrum** lavora a **iterazioni (sprint)** di durata fissa, con ruoli ed eventi definiti; il lavoro si impegna a blocchi (lo sprint backlog).
- **Kanban** lavora a **flusso continuo**, senza sprint: si visualizza il lavoro su una **board** a colonne (es. Da fare / In corso / Fatto) e si limita il **work in progress (WIP)**, cioè il numero massimo di elementi in lavorazione contemporanea, per evitare di cominciare troppe cose e finirne poche. Misura tipica: il **lead time**, il tempo che un elemento impiega ad attraversare la board.

Regola pratica: Scrum quando il lavoro si pianifica bene a blocchi e serve una cadenza; Kanban quando il lavoro arriva in modo continuo e imprevedibile (es. manutenzione, supporto). Molti team li combinano (**Scrumban**).

## Esempi concreti
- **Uno sprint tipico.** Team di cinque Developers, sprint di due settimane. Planning il lunedì mattina: scelgono uno Sprint Goal ("l'utente può reimpostare la password da solo") e tirano dal product backlog le story che ci stanno. Ogni mattina un daily di 15 minuti. Venerdì della seconda settimana: review con gli stakeholder (si mostra il flusso funzionante) e poi retrospettiva (hanno notato che le code review erano lente: decidono di introdurre un turno di revisione fisso).
- **Perché la Definition of Done conta.** Due Developers dicono "ho finito la mia story". Senza DoD, uno intende "il codice compila", l'altro "testato e in staging". Con una DoD condivisa ("codice revisionato, test passati, deploy in ambiente di prova") la parola "finito" significa la stessa cosa per tutti, e l'incremento è davvero utilizzabile.
- **Relativo meglio di assoluto.** Chiedere "quante ore?" porta a stime fragili; chiedere "questa story è più o meno grande di quella che abbiamo già fatto?" porta a story point più stabili, perché il cervello confronta meglio di quanto misuri in assoluto.

## Notable use case
- **Spotify** ha reso celebre un modello organizzativo (squad, tribe, chapter, guild) per scalare il lavoro agile su molti team mantenendo autonomia e allineamento. È un modello ispirato ad Agile ed esterno a Scrum, e la stessa azienda lo ha poi descritto come la fotografia di un momento, da prendere con cautela come ricetta universale.
- **Scrum** nasce nel software ma viene applicato anche fuori (marketing, hardware, ricerca): ovunque il lavoro sia complesso e i requisiti incerti, la cadenza a sprint con revisione e retrospettiva aiuta a correggere la rotta presto.

## Fonti
- **Scrum Guide** (scrumguides.org), Schwaber e Sutherland, edizione 2020: la definizione ufficiale di ruoli, eventi e artefatti.
- **Manifesto Agile** (agilemanifesto.org): i quattro valori e i dodici principi, testo originale.
- **Henrik Kniberg**, *Kanban and Scrum: making the most of both*: confronto pratico tra i due.
- **PMBOK Guide** (PMI), che nelle edizioni recenti integra approcci agili accanto a quelli predittivi.

## Concetti adiacenti
- `se-process`: Agile come modello di ciclo di vita accanto a waterfall e incrementale, dal punto di vista dell'ingegneria del software (tema già visto).
- `pm-lifecycle`: il ciclo di vita del progetto e gli standard di project management (PMBOK, ISO 21502), dove l'agile convive con l'approccio predittivo.
- `xc-pm-role`: il ruolo del Product Owner rispetto al Product Manager e la distinzione tra gestione del prodotto e del progetto.

## Quiz (10 — tutte rispondibili dalla lezione)
1. Quanti **valori** e quanti **principi** contiene il Manifesto Agile? Enuncia i quattro valori.
2. Quali sono i **tre pilastri empirici** di Scrum e cosa significa che Scrum è "empirico"?
3. Elenca i **tre ruoli** dello Scrum Team e la responsabilità principale di ciascuno.
4. Quali sono i **tre artefatti** di Scrum e l'**impegno (commitment)** associato a ciascuno?
5. Cos'è la **Definition of Done** e perché è importante?
6. Lo **Sprint**: cos'è, quanto dura al massimo, e la sua durata può cambiare in corsa?
7. Nomina i **quattro eventi** dentro lo sprint (oltre allo sprint stesso) e il loro scopo. A chi appartiene il Daily Scrum?
8. Il **refinement** del backlog è un evento di Scrum? Spiega.
9. Cosa sono **story point**, **velocity** e **burndown**, e perché è un errore dire che fanno parte della Scrum Guide?
10. Differenza tra **Scrum** e **Kanban**: come scorre il lavoro in ciascuno e cos'è il limite di **WIP**?

<details><summary>Risposte</summary>

1. **Quattro valori** e **dodici principi**. I valori: individui e interazioni più che processi e strumenti; software funzionante più che documentazione esaustiva; collaborazione col cliente più che negoziazione dei contratti; rispondere al cambiamento più che seguire un piano.
2. **Trasparenza, ispezione, adattamento.** "Empirico" significa che si decide in base a ciò che si **osserva** (si ispeziona spesso e si corregge), non a un piano deciso una volta per tutte.
3. **Product Owner** (massimizza il valore, decide cosa e con che priorità, possiede il product backlog); **Scrum Master** (responsabile dell'efficacia del team, facilita e rimuove impedimenti); **Developers** (realizzano l'incremento, auto-organizzati sul come).
4. **Product backlog** con impegno il **Product Goal**; **Sprint backlog** con impegno lo **Sprint Goal**; **Increment** con impegno la **Definition of Done**.
5. È la **definizione condivisa di "fatto"**: i criteri di qualità che un elemento deve soddisfare per dirsi completato (es. testato, revisionato). Conta perché rende l'incremento davvero utilizzabile e dà alla parola "finito" lo stesso significato per tutti.
6. È l'**iterazione a durata fissa**, al massimo **un mese** (spesso due settimane); fa da contenitore agli altri eventi. La durata **non cambia** a sprint iniziato, e appena finisce ne parte subito un altro.
7. **Sprint Planning** (definire Sprint Goal e sprint backlog), **Daily Scrum** (sincronizzarsi ogni giorno, 15 minuti), **Sprint Review** (mostrare l'incremento e raccogliere feedback), **Sprint Retrospective** (migliorare il modo di lavorare). Il **Daily Scrum** appartiene ai **Developers**.
8. **No**, il refinement **non è un evento** di Scrum: è un'**attività continua** di chiarire, stimare e spezzare gli elementi del product backlog.
9. **Story point**: unità **relativa** di sforzo (complessità + incertezza + quantità). **Velocity**: story point medi completati per sprint, misura interna per fare previsioni. **Burndown**: grafico del lavoro residuo che scende verso zero. È un errore attribuirle alla Scrum Guide perché sono **pratiche diffuse** nate attorno a Scrum/XP, non parte della definizione ufficiale.
10. **Scrum** lavora a **iterazioni (sprint)** fisse con ruoli ed eventi; **Kanban** lavora a **flusso continuo** su una board, senza sprint. Il limite di **WIP (work in progress)** è il numero massimo di elementi in lavorazione contemporanea, per non iniziare troppe cose e finirne poche.
</details>

## Esercizi
1. **Imposta uno sprint.** Un team di quattro Developers (sprint di due settimane) deve lavorare su una funzione di "ricerca avanzata". Scrivi: uno **Sprint Goal** in una frase, tre voci plausibili di **sprint backlog**, e una **Definition of Done** con almeno tre criteri.
2. **Costruisci un mini product backlog ordinato.** Dato questo elenco disordinato di elementi, riordinalo per priorità motivando la scelta (metti prima ciò che dà più valore o sblocca il resto): "esportare i risultati in CSV", "login utente", "ricerca per parola chiave", "tema scuro". Assegna a ciascuno una stima in story point sulla scala 1, 2, 3, 5, 8.
3. **Stima la durata con la velocity.** Un backlog vale 80 story point. Il team ha chiuso negli ultimi tre sprint rispettivamente 18, 22 e 20 punti. Stima quanti sprint servono e spiega il limite di questa previsione.
4. **Scrum o Kanban?** Per ciascuno scegli e motiva in una riga: (a) un team che sviluppa nuove funzioni pianificabili a blocchi; (b) un team di supporto che riceve richieste impreviste tutto il giorno.

<details><summary>Soluzioni</summary>

1. **Sprint Goal:** "L'utente trova un risultato pertinente combinando più filtri di ricerca". **Sprint backlog** (esempi): aggiungere il filtro per categoria; combinare più filtri in AND; mostrare il numero di risultati in tempo reale. **Definition of Done:** codice revisionato da un altro Developer; test automatici scritti e passati; funzione provata in ambiente di staging; nessun errore noto aperto.
2. Ordine proposto: **login utente (3)** per primo perché abilita l'uso del prodotto e spesso sblocca il resto; **ricerca per parola chiave (5)** perché è il valore centrale atteso; **esportare i risultati in CSV (3)** perché estende un valore già consegnato; **tema scuro (2)** per ultimo perché è un miglioramento estetico, non sblocca nulla. Le stime sono relative: login e export simili e medi, la ricerca più grande per via della complessità, il tema il più piccolo. (Numeri plausibili, l'importante è la coerenza relativa e la motivazione per valore/dipendenze.)
3. Velocity media = (18 + 22 + 20) / 3 = **20** punti a sprint. Sprint stimati = 80 / 20 = **4 sprint**. Limiti: la velocity è una media con variabilità (qui va da 18 a 22), il backlog può crescere o essere rifinito e ristimato, e imprevisti o cambi di squadra la alterano. È una previsione, non una promessa; va riaggiornata a ogni sprint.
4. (a) **Scrum:** lavoro pianificabile a blocchi, trae vantaggio dalla cadenza a sprint con obiettivo e review. (b) **Kanban:** richieste continue e imprevedibili, meglio un flusso con limite di WIP e misura del lead time invece di impegni a sprint fissi.
</details>
