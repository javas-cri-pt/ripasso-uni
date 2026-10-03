---
day: 35
topic_id: xc-pm-discovery
title: "Product discovery, user research, Jobs-to-be-Done"
area: cross-cutting
course: "Product Management"
grounded_in: null
adjacent: [xc-pm-role, xc-pm-prd, bp-canvas]
completeness_checked: true
quiz_count: 10
---

# Product discovery, user research, Jobs-to-be-Done

> **Perché oggi:** la domanda più costosa in un prodotto arriva prima del codice ed è "stiamo costruendo la cosa giusta?". La **discovery** è la disciplina che risponde proprio a questa domanda prima di scrivere codice: capire il problema, parlare con chi lo vive, decidere cosa vale la pena fare. È il cuore del ruolo di Product Manager e la competenza che distingue chi costruisce prodotti usati da chi costruisce feature che nessuno apre. Oggi vediamo come si fa discovery in modo continuo, come si conduce la ricerca con gli utenti e come si inquadra il bisogno con i **Jobs-to-be-Done**, fino a tradurlo in una **user story** pronta per il team.

## Discovery e delivery: due lavori diversi
Un prodotto si costruisce su due binari paralleli.
- La **discovery** (scoperta) decide **cosa** vale la pena costruire e **perché**: esplora i problemi degli utenti, valida le idee, riduce l'incertezza. Il suo rischio è costruire la cosa sbagliata.
- La **delivery** (consegna) decide **come** costruirlo bene e lo porta in produzione: progettazione, codice, test, rilascio. Il suo rischio è costruire male la cosa.

La tentazione classica è saltare la discovery e passare subito a scrivere requisiti e codice. Il problema è che una feature tecnicamente perfetta ma inutile resta uno spreco. La discovery serve proprio a comprare informazione a basso costo (una conversazione, un prototipo di carta) prima di spendere settimane di sviluppo.

**Discovery continua (continuous discovery):** l'approccio moderno, reso popolare da Teresa Torres, dice che la scoperta è un'**abitudine settimanale e permanente**: il team di prodotto parla con gli utenti ogni settimana, in piccolo, per tutta la vita del prodotto. Si contrappone così alla discovery "a progetto", fatta una volta all'inizio e poi mai più.

## La ricerca con gli utenti (user research)
La **user research** è l'insieme dei metodi per capire bisogni, comportamenti e difficoltà degli utenti con prove, non con opinioni. Si classifica lungo due assi.

Primo asse, lo **scopo**:
- **Ricerca generativa (o esplorativa):** serve a **scoprire** problemi e bisogni quando ancora non sai cosa costruire. Risponde a "quali problemi hanno le persone?". Tipica a inizio discovery.
- **Ricerca valutativa:** serve a **giudicare** una soluzione che hai già in mente o già costruito. Risponde a "questa soluzione funziona per loro?". Tipico esempio: lo usability test.

Secondo asse, il **tipo di dato**:
- **Qualitativa:** poche persone, molta profondità. Risponde al **perché** (interviste, osservazione). Ti dà le motivazioni, non le proporzioni.
- **Quantitativa:** tanti dati, poca profondità. Risponde al **quanto** (survey con molte risposte, analytics di uso). Ti dà le proporzioni, non le motivazioni.

I metodi che useresti più spesso:
- **Intervista con l'utente:** conversazione uno a uno. La regola d'oro è chiedere di **comportamenti concreti e passati** ("raccontami l'ultima volta che hai dovuto fare X"), non opinioni o ipotesi sul futuro ("useresti una app che...?"). Le persone sanno raccontare cosa hanno fatto, ma sono pessime a prevedere cosa faranno. Vanno evitate le **domande guida (leading)** che suggeriscono la risposta.
- **Usability test:** metti davanti all'utente un prototipo o il prodotto e gli chiedi di **svolgere un compito** mentre pensa ad alta voce. Serve a trovare dove si blocca. Bastano pochissimi partecipanti per far emergere la maggior parte dei problemi gravi di usabilità.
- **Survey (questionario):** domande strutturate a molte persone. Forte sui numeri, debole sulle motivazioni; va bene per misurare, male per scoprire.
- **Analytics comportamentale:** i dati di come le persone **usano davvero** il prodotto (quali schermate, dove abbandonano). Dicono cosa succede, non perché: si combinano con il qualitativo.

Attenzione a due trappole ricorrenti: il **survivorship bias** (parli solo con chi è rimasto, non con chi se n'è andato) e il divario tra ciò che le persone **dicono** e ciò che **fanno**. Per questo la discovery pesa di più i comportamenti osservati delle dichiarazioni.

## Jobs-to-be-Done (JTBD)
Il framework **Jobs-to-be-Done (JTBD)**, associato a Clayton Christensen, ribalta il punto di vista: le persone non "comprano prodotti", **assumono (hire) un prodotto per svolgere un lavoro (job)** che devono portare a termine in una certa situazione. La frase che riassume tutto: la gente non vuole un trapano, vuole il **buco nel muro** (anzi, l'oggetto appeso al muro).

Un **job** ha tre componenti:
- una dimensione **funzionale** (il compito pratico: "trasferire denaro a un amico");
- una dimensione **emotiva** (come voglio sentirmi: "senza ansia di aver sbagliato");
- una dimensione **sociale** (come voglio essere visto dagli altri).

Il valore pratico del JTBD è che sposta la definizione del **concorrente**: se il job è "mangiare qualcosa di veloce in pausa pranzo", il concorrente del tuo panino non è solo l'altro bar, ma anche il distributore automatico e il saltare il pranzo. Definire il job allarga lo sguardo oltre i competitor ovvi.

Si scrive con una **job story**, nel formato:
> Quando *[situazione]*, voglio *[motivazione]*, così che *[risultato atteso]*.

Esempio: "Quando arrivo in stazione di corsa e il treno parte tra due minuti, voglio comprare il biglietto in pochi secondi senza fare la fila, così che non perda il treno". Nota che non c'è nessuna soluzione dentro: solo situazione, motivazione e risultato. La soluzione la cerchi dopo.

## Dall'opportunità alla soluzione
Uno strumento per tenere in ordine la discovery è l'**Opportunity Solution Tree (OST)** di Teresa Torres: un albero che collega l'obiettivo di business alle opportunità (i bisogni e i problemi scoperti negli utenti), le opportunità alle soluzioni possibili, e le soluzioni agli esperimenti per validarle. Serve a non innamorarsi della prima idea e a rendere visibile **perché** stai lavorando su una certa cosa.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 640 330" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
    <rect x="235" y="14" width="170" height="40" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/>
    <text x="320" y="33">Outcome di business</text><text x="320" y="47" font-size="10" fill="var(--muted)">es. +20% rinnovi</text>
    <rect x="70" y="100" width="180" height="38" rx="8" fill="var(--card2)" stroke="var(--rule)"/><text x="160" y="124">Opportunità A (bisogno)</text>
    <rect x="390" y="100" width="180" height="38" rx="8" fill="var(--card2)" stroke="var(--rule)"/><text x="480" y="124">Opportunità B (bisogno)</text>
    <rect x="20" y="186" width="120" height="36" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="80" y="208" font-size="10.5">Soluzione 1</text>
    <rect x="160" y="186" width="120" height="36" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="220" y="208" font-size="10.5">Soluzione 2</text>
    <rect x="410" y="186" width="140" height="36" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="480" y="208" font-size="10.5">Soluzione 3</text>
    <rect x="40" y="268" width="240" height="34" rx="7" fill="var(--card)" stroke="var(--good)" stroke-width="1.5"/><text x="160" y="289" font-size="10.5">Esperimenti / test</text>
    <rect x="370" y="268" width="220" height="34" rx="7" fill="var(--card)" stroke="var(--good)" stroke-width="1.5"/><text x="480" y="289" font-size="10.5">Esperimenti / test</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none">
    <path d="M300,54 L160,98"/><path d="M340,54 L480,98"/>
    <path d="M140,138 L80,184"/><path d="M180,138 L220,184"/><path d="M480,138 L480,184"/>
    <path d="M80,222 L140,266"/><path d="M220,222 L180,266"/><path d="M480,222 L480,266"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Opportunity Solution Tree: l'outcome di business in cima, sotto le opportunità scoperte negli utenti, poi le soluzioni candidate e infine gli esperimenti che le validano. Si esplorano più opportunità e più soluzioni prima di impegnarsi.</figcaption>
</figure>

## Dalla scoperta alla consegna: la user story
Quando una soluzione è validata, la si passa al team in piccoli pezzi di valore chiamati **user story**: una descrizione breve di una funzionalità vista dal punto di vista di chi la userà. Il formato canonico è:
> Come *[tipo di utente]*, voglio *[azione]*, così che *[beneficio]*.

Una user story non è un documento tecnico: dice il **chi**, il **cosa** e il **perché**, e lascia il **come** al team. Perché sia pronta da sviluppare le si attaccano i **criteri di accettazione (acceptance criteria):** le condizioni verificabili che dicono quando la story è "fatta". Si scrivono spesso nello schema **Dato / Quando / Allora** (given / when / then): dato un contesto, quando accade un'azione, allora ci si aspetta un certo risultato.

Differenza utile da tenere a mente: la **job story** (JTBD) descrive il bisogno **indipendente dalla soluzione** (situazione, motivazione, risultato), mentre la **user story** descrive già una **funzionalità** da costruire. Si va dal job alla user story quando si è deciso cosa fare.

## Esempi concreti
- **Intervista fatta male vs fatta bene.** Male: "Ti piacerebbe una funzione per esportare i dati in PDF?" (domanda guida, ipotetica, suggerisce la soluzione). Bene: "Raccontami l'ultima volta che hai dovuto condividere questi dati con qualcuno fuori dal team: cosa hai fatto, passo per passo?". La seconda fa emergere il job reale (condividere) e magari scopri che il PDF non c'entra, serviva un link.
- **JTBD che cambia il concorrente.** Un servizio di consegna pasti definisce il job come "cena pronta senza pensarci dopo una giornata piena". Qui i concorrenti includono anche il supermercato sotto casa e i surgelati nel freezer, oltre alle altre app di delivery. Questo cambia il modo di posizionare il prodotto.
- **Da job story a user story.** Job story: "Quando torno a casa tardi e ho fame, voglio ordinare qualcosa che arrivi presto, così che non debba cucinare". User story che ne deriva: "Come utente affamato la sera, voglio filtrare i ristoranti per tempo di consegna sotto i 30 minuti, così che scelga solo quelli abbastanza veloci". Criterio di accettazione: "Dato l'elenco ristoranti, quando attivo il filtro 30 minuti, allora vedo solo quelli con stima di consegna minore o uguale a 30 minuti".

## Notable use case
- **Amazon** pratica il **working backwards**: prima di costruire, scrive il **comunicato stampa** e le **FAQ** del prodotto come se fosse già lanciato, dal punto di vista del cliente. Se il beneficio non è convincente sulla carta, il prodotto non parte: è discovery scritta prima della delivery.
- Il framework **JTBD** nasce osservando casi concreti di consumo: lo studio classico di Christensen su perché le persone "assumono" un frullato al mattino (il job era rendere meno noioso il tragitto in auto) mostra come lo stesso prodotto serva job diversi in momenti diversi.
- Molti team di prodotto maturi adottano la **continuous discovery** con interviste settimanali ricorrenti, così che le decisioni poggino su un flusso costante di contatto con gli utenti invece che su una ricerca fatta una volta.

## Fonti
- **Teresa Torres**, *Continuous Discovery Habits*: discovery continua e Opportunity Solution Tree (sito: producttalk.org).
- **Clayton Christensen**, *Competing Against Luck*: la teoria dei Jobs-to-be-Done.
- **Marty Cagan**, *Inspired* (Silicon Valley Product Group): discovery vs delivery e rischi di prodotto.
- **Steve Portigal**, *Interviewing Users*: come condurre interviste senza domande guida.
- **Nielsen Norman Group** (nngroup.com): metodi di usability testing e user research.

## Concetti adiacenti
- `xc-pm-role`: cos'è il Product Management, la differenza tra Product Manager e Project Manager, discovery vs delivery nel ruolo.
- `xc-pm-prd`: come si scrive un PRD e si definisce il problema, dove le user story trovano casa.
- `bp-canvas`: il Business Model Canvas e la value proposition, che collocano il job dell'utente dentro il modello di business (tema già visto).

## Quiz (10 — tutte rispondibili dalla lezione)
1. Qual è la differenza tra **discovery** e **delivery**, e qual è il rischio tipico di ciascuna?
2. Cosa significa **continuous discovery** e in cosa si oppone alla discovery "a progetto"?
3. Spiega i due assi con cui si classifica la user research (scopo e tipo di dato) e cosa distingue ciascun estremo.
4. Perché in un'intervista conviene chiedere comportamenti **passati e concreti** invece di opinioni sul futuro? Cos'è una domanda **guida (leading)**?
5. Cosa afferma il framework **Jobs-to-be-Done** e quali sono le tre dimensioni di un job?
6. Come il JTBD cambia la definizione di **concorrente**? Fai l'esempio.
7. Scrivi il formato di una **job story** e spiega perché non deve contenere la soluzione.
8. Cos'è un **Opportunity Solution Tree** e quali livelli collega?
9. Qual è il formato canonico di una **user story** e cosa sono i **criteri di accettazione** (schema Dato/Quando/Allora)?
10. Che differenza c'è tra **job story** e **user story**?

<details><summary>Risposte</summary>

1. La **discovery** decide *cosa* costruire e *perché* (rischio: costruire la cosa sbagliata); la **delivery** decide *come* costruirlo bene e lo porta in produzione (rischio: costruire male la cosa giusta).
2. È l'abitudine di fare scoperta in **continuo**, con contatto settimanale con gli utenti per tutta la vita del prodotto, invece di concentrarla in una fase iniziale che poi finisce.
3. Asse **scopo**: ricerca **generativa** (scoprire problemi quando non sai cosa fare) vs **valutativa** (giudicare una soluzione che hai già). Asse **dato**: **qualitativa** (poche persone, molta profondità, il *perché*) vs **quantitativa** (molti dati, poca profondità, il *quanto*).
4. Perché le persone sanno raccontare bene cosa **hanno fatto** ma prevedono male cosa faranno; le opinioni ipotetiche sono inaffidabili. Una **domanda guida** suggerisce già la risposta (es. "Ti piacerebbe una funzione X?") e distorce ciò che l'utente dice.
5. Afferma che le persone **assumono un prodotto per svolgere un lavoro (job)** in una data situazione, non comprano il prodotto in sé. Le tre dimensioni: **funzionale**, **emotiva**, **sociale**.
6. Il concorrente diventa **qualunque cosa svolga lo stesso job**, non solo i prodotti simili. Esempio: per "mangiare veloce in pausa pranzo" il concorrente del panino è anche il distributore automatico o saltare il pranzo.
7. Formato: *Quando [situazione], voglio [motivazione], così che [risultato atteso]*. Non contiene la soluzione perché deve descrivere il **bisogno** in modo neutro, lasciando libere più soluzioni possibili.
8. È un albero che collega l'**outcome di business** alle **opportunità** (bisogni scoperti), queste alle **soluzioni** candidate, e le soluzioni agli **esperimenti** che le validano. Serve a esplorare più strade e a rendere visibile il perché.
9. Formato: *Come [tipo di utente], voglio [azione], così che [beneficio]*. I **criteri di accettazione** sono le condizioni verificabili che dicono quando la story è "fatta", spesso nello schema **Dato** (contesto) / **Quando** (azione) / **Allora** (risultato atteso).
10. La **job story** descrive il bisogno **indipendente dalla soluzione** (situazione, motivazione, risultato); la **user story** descrive già una **funzionalità** da costruire (chi, cosa, perché). Si passa dall'una all'altra quando si è deciso cosa fare.
</details>

## Esercizi
1. **Scrivi una job story.** Immagina un professionista che deve tenere traccia delle spese di lavoro per il rimborso. Scrivi una job story nel formato corretto, senza nominare nessuna soluzione, e indica quale dimensione del job (funzionale/emotiva/sociale) stai toccando.
2. **Trasforma la job story in una user story con criteri di accettazione.** Partendo dalla job story del punto 1, scrivi una user story nel formato canonico e almeno due criteri di accettazione nello schema Dato/Quando/Allora.
3. **Correggi le domande di intervista.** Riscrivi queste due domande guida in domande aperte sul comportamento passato: (a) "Non trovi scomodo inserire le spese a mano?" (b) "Useresti una funzione che fotografa lo scontrino?".
4. **Imposta un mini-piano di discovery.** Per lo stesso contesto (tracciare le spese di lavoro) scegli **un** metodo di ricerca generativa e **uno** di ricerca valutativa, e scrivi in una riga cosa vuoi scoprire con ciascuno.

<details><summary>Soluzioni</summary>

1. Esempio: *Quando torno da una trasferta con molti scontrini in tasca, voglio registrare ogni spesa nel momento in cui la faccio, così che a fine mese non debba ricostruire tutto a memoria e rischiare di perdere un rimborso.* Dimensione prevalente: **funzionale** (registrare la spesa), con una componente **emotiva** (non avere l'ansia di dimenticare). Nessuna soluzione nominata (niente app, foto, excel).
2. User story: *Come professionista in trasferta, voglio aggiungere una spesa in pochi secondi dal telefono, così che la registri sul momento senza rimandarla.* Criteri di accettazione:
   - a) *Dato* che sono nella schermata spese, *quando* inserisco importo e categoria e salvo, *allora* la spesa compare in cima all'elenco con data odierna.
   - b) *Dato* un importo non valido (vuoto o negativo), *quando* premo salva, *allora* vedo un messaggio di errore e la spesa non viene salvata.
3. (a) "Raccontami come hai registrato l'ultima spesa di lavoro: cosa hai fatto, passo per passo?" (b) "L'ultima volta che hai avuto uno scontrino da conservare per il rimborso, cosa ne hai fatto?". Entrambe chiedono un comportamento passato e concreto, senza suggerire la soluzione.
4. **Generativa:** interviste uno a uno con cinque professionisti, per scoprire *come fanno oggi* a tenere le spese e dove perdono tempo o soldi. **Valutativa:** un usability test su un prototipo di inserimento spesa, per vedere *se e dove si bloccano* nel completare il compito "aggiungi una spesa".
</details>
