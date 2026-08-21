---
day: 18
topic_id: prog-algo
title: "Algoritmi e complessità — Big-O, sorting, ricerca"
area: computer-science
course: Programmazione & Algoritmi
grounded_in: "UNIBO/primoAnno/Fondamenti di Informatica 2"
adjacent: [prog-ds, xc-dsa-review]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo."
---

# Algoritmi e complessità — Big-O

> **Perché oggi:** è *LA* domanda dei colloqui tecnici — "qual è la complessità?" — e conta davvero. Un algoritmo **O(n²)** su un milione di elementi non finisce mai; uno **O(n log n)** sì. Sapere valutare la complessità ti serve a scrivere codice che **regge la scala**, non solo che "funziona" sul tuo laptop con dieci righe di test. È la differenza tra un sistema che vive e uno che muore appena arrivano gli utenti veri.

## Perché misurare la complessità

Quando dici che un algoritmo è "veloce", cosa intendi? La tentazione è misurare i **secondi**. Ma i secondi non ci interessano, e per un motivo preciso: **dipendono dalla macchina**. Lo stesso codice è più rapido su un server nuovo, più lento su un telefono vecchio, cambia col linguaggio e col compilatore. Se misuri i secondi, misuri l'hardware, non l'algoritmo.

Quello che ci interessa è invece **come cresce il costo al crescere dell'input**. Chiamiamo **n** la **dimensione dell'input** (quanti elementi ha la lista, quanti caratteri la stringa, quante righe la tabella). La domanda vera è: *se raddoppio n, cosa succede al costo? Raddoppia? Si quadruplica? Resta uguale?* Questo andamento è una proprietà dell'algoritmo, non della macchina — ed è ciò che vogliamo catturare.

Due grandezze da distinguere:

- **Complessità temporale** = conta il **numero di operazioni** che l'algoritmo esegue, in funzione di n. È il "quanto lavora".
- **Complessità spaziale** = conta la **memoria extra** che l'algoritmo usa, sempre in funzione di n. È il "quanto occupa".

L'idea chiave è guardare l'**andamento asintotico**: cosa succede **per n grande**. Per n grande, i dettagli fini spariscono e conta solo la forma della crescita. Per questo, quando misuriamo la complessità, **ignoriamo le costanti e i termini minori** (fra un attimo vediamo perché): non ci serve il numero esatto di operazioni, ci serve la **classe di crescita**.

## La notazione Big-O

La **notazione O grande** (in inglese *Big-O*) è il modo standard per esprimere questa classe di crescita. Scrivere che un algoritmo è **O(f(n))** significa: *"il costo cresce **al più** come f(n), per n grande"*. La O grande descrive quindi un **limite superiore** alla crescita — un tetto. Se un algoritmo è O(n²), stai promettendo che, per n grande, il suo costo non cresce più in fretta di n².

Due regole rendono la O grande semplice da usare, e vanno capite, non memorizzate:

- **Si ignorano le costanti moltiplicative.** O(2n) si scrive **O(n)**; O(n/2) è anch'esso **O(n)**. Perché? Perché il fattore costante (2, ½, 100…) dipende da dettagli di implementazione e di macchina, esattamente ciò che vogliamo togliere di mezzo. Raddoppiare la velocità della macchina dimezza la costante ma **non cambia la forma della crescita**. Ci interessa la forma.
- **Si ignorano i termini di ordine inferiore.** O(n² + n) si scrive **O(n²)**; O(n² + 3n + 7) è ancora **O(n²)**. Perché? Perché **per n grande domina il termine più forte**. Con n = 1.000.000, n² è mille miliardi mentre n è solo un milione: il termine n è polvere rispetto a n². Tenere solo il termine dominante non è pigrizia, è cogliere ciò che conta davvero alla scala.

Messe insieme: la O grande tiene **solo il termine dominante, senza la sua costante**. Un algoritmo con costo "5n² + 100n + 3000" è, in una parola, **O(n²)**.

**Cenni onesti (per completezza).** La O grande ha due parenti che a volte sentirai nominare:

- **Ω (Omega grande)** = il **limite inferiore**: "il costo cresce **almeno** così".
- **Θ (Theta grande)** = il limite **esatto**: vale quando limite superiore e inferiore coincidono ("cresce **esattamente** così").

Nel lavoro e nei colloqui, però, si usa quasi sempre **O**: è quella che risponde alla domanda pratica "quanto male può andare?".

**Caso peggiore, medio, migliore.** Lo stesso algoritmo può costare diversamente a seconda dell'input. Cercare un elemento in una lista: se è il primo, lo trovi subito (**caso migliore**); se è l'ultimo o assente, scorri tutto (**caso peggiore**); in media stai nel mezzo (**caso medio**). Quando si dà "la complessità" senza specificare, di norma si intende il **caso peggiore** — perché è la garanzia: sapere che *non andrà mai peggio di così* è ciò che ti serve per dormire la notte.

## Le classi di complessità (dalla migliore alla peggiore)

Ecco le classi che incontri ogni giorno, ordinate dalla più efficiente alla più disastrosa. Per ognuna: cosa significa, e un esempio concreto.

- **O(1) — costante.** Il tempo è **fisso, indipendente da n**. Che la struttura abbia 10 o 10 milioni di elementi, il costo è lo stesso. *Esempio:* accedere a un elemento di un **array** dato il suo **indice** (`array[7]`), oppure leggere un valore da una **hash map** data la chiave. Non scorri niente: vai dritto al punto.
- **O(log n) — logaritmica.** Ad ogni passo **dimezzi** il problema. Cresce lentissimamente: se n raddoppia, il costo aumenta solo di **un** passo. *Esempio:* la **ricerca binaria** su un array **ordinato** (la vediamo tra poco). Con un milione di elementi bastano circa 20 passi.
- **O(n) — lineare.** Scorri **tutti** gli elementi **una volta**. Raddoppia n, raddoppia il costo. *Esempio:* cercare un valore in una **lista non ordinata** — nel caso peggiore devi guardarli tutti.
- **O(n log n).** È la classe dei **buoni algoritmi di ordinamento** (merge sort, quick sort nel caso medio). Un pelo più della lineare, ma incomparabilmente meglio della quadratica. È il "meglio che si può fare" per ordinare confrontando elementi.
- **O(n²) — quadratica.** Tipicamente un **doppio ciclo annidato**: per ogni elemento, riguardi (quasi) tutti gli altri. Raddoppia n, il costo si **quadruplica**. *Esempio:* confrontare **ogni coppia** di elementi; gli ordinamenti ingenui come **bubble sort** e **insertion sort** (nel caso peggiore).
- **O(2ⁿ) — esponenziale** e **O(n!) — fattoriale.** Queste **esplodono**: aggiungere **un solo** elemento *raddoppia* (2ⁿ) o moltiplica di molto (n!) il costo. Diventano impraticabili già per n piccoli (poche decine di elementi bastano a renderle impossibili). *Esempio:* la **forza bruta** che prova **tutte** le combinazioni o tutte le permutazioni possibili.

Regola mentale: quando in un colloquio dici la complessità, di' la classe (O(n), O(n log n)…), non un numero.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 460 320" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
   <line x1="55" y1="20" x2="55" y2="280" stroke="var(--rule)" stroke-width="1.5"/>
   <line x1="55" y1="280" x2="430" y2="280" stroke="var(--rule)" stroke-width="1.5"/>
   <text x="40" y="150" transform="rotate(-90 40 150)" fill="var(--muted)">operazioni</text>
   <text x="245" y="305" fill="var(--muted)">n (dimensione input)</text>
  </g>
  <g fill="none" stroke-width="2">
   <path d="M55,278 L430,275" stroke="var(--muted)"/>
   <path d="M55,278 C150,250 300,238 430,232" stroke="var(--muted)"/>
   <path d="M55,278 L430,150" stroke="var(--muted)"/>
   <path d="M55,278 C200,200 340,150 430,110" stroke="var(--accent)"/>
   <path d="M55,278 C230,255 320,160 400,35" stroke="var(--accent)"/>
   <path d="M55,278 C130,265 175,220 205,30" stroke="var(--accent)"/>
  </g>
  <g font-size="10.5" fill="var(--ink)" text-anchor="start">
   <text x="205" y="24">O(2ⁿ)</text>
   <text x="392" y="28" text-anchor="end">O(n²)</text>
   <text x="433" y="108">O(n log n)</text>
   <text x="433" y="150">O(n)</text>
   <text x="433" y="230">O(log n)</text>
   <text x="433" y="277">O(1)</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Curve di crescita a confronto: O(1) resta piatta, O(log n) quasi piatta, O(n) sale dritta, O(n log n) poco sopra; O(n²) e soprattutto O(2ⁿ) schizzano in alto e divergono. Più a destra vai (n grande), più la scelta della classe conta.</figcaption>
</figure>

## Esempi che tornano ai colloqui

### Ricerca lineare O(n) vs ricerca binaria O(log n)

**Ricerca lineare:** parti dall'inizio e controlli un elemento alla volta finché non trovi quello giusto (o finisci la lista). Nel caso peggiore li guardi **tutti**: **O(n)**. Funziona su qualsiasi lista, anche disordinata.

**Ricerca binaria:** richiede che l'array sia **ordinato**, ma in cambio è enormemente più veloce. Guardi l'elemento **in mezzo**: se è quello cerchi, hai finito; se il tuo obiettivo è più piccolo, **butti via tutta la metà destra**; se è più grande, butti la metà sinistra. Ad ogni confronto **dimezzi** ciò che resta da guardare. Quanti dimezzamenti servono per arrivare a un solo elemento? Circa **log₂ n**: ecco perché è **O(log n)**. Concretamente: su un milione di elementi, la lineare ne guarda fino a un milione, la binaria circa **20**. La condizione da non dimenticare mai: **i dati devono essere ordinati**, altrimenti "butta via la metà" non ha senso.

### Sorting: perché merge sort è O(n log n) e bubble sort O(n²)

**Bubble sort** confronta coppie di elementi adiacenti e li scambia se sono nell'ordine sbagliato, ripassando la lista più volte finché è ordinata. Sono **due cicli annidati** (per ogni elemento, riscorri gli altri): **O(n²)**. Semplice da scrivere, ma alla scala è un disastro.

**Merge sort** usa la strategia **divide et impera** ("dividi e conquista"): spezza il problema in sotto-problemi, li risolve, e ricombina.

1. **Dividi** l'array a metà, poi ogni metà a metà, e così via finché ogni pezzo ha un solo elemento. Quanti livelli di divisione servono per arrivare da n a 1? Circa **log n** (dimezzi ogni volta — stessa logica della ricerca binaria).
2. **Unisci (merge)** i pezzi ordinati due a due, risalendo. Ad ogni livello, mettere insieme tutti i pezzi ordinati costa **O(n)** (in totale tocchi ogni elemento una volta per livello).

Quindi: **log n livelli**, ciascuno da **O(n)** → **O(n log n)**. Ecco perché merge sort regge dove bubble sort crolla: su un milione di elementi, la differenza tra ~n log n (una ventina di milioni di operazioni) e n² (mille miliardi) è la differenza tra "un attimo" e "mai".

### Hash map: da O(n) a O(1) (a costo di memoria)

Hai una lista di utenti e devi controllare spesso "esiste l'utente X?". Con una lista, ogni controllo è una ricerca lineare **O(n)**. Metti gli stessi dati in una **hash map** (una struttura che associa **chiavi** a valori e le colloca in base a un calcolo sulla chiave) e ogni controllo diventa **O(1)**: vai dritto alla posizione della chiave, senza scorrere. Il rovescio della medaglia: la hash map **occupa più memoria** della semplice lista. È il classico **trade-off tempo/spazio**: spendi memoria per comprare velocità. Spessissimo, alla scala, è l'affare giusto — ed è una delle risposte più apprezzate ai colloqui ("come lo rendi più veloce?" → "uso una hash map per la lookup, passo da O(n) a O(1)").

## Il ponte col lavoro

Perché tutto questo conta davvero, fuori dall'aula:

- **Regge la scala o muore.** La differenza **O(n²) vs O(n log n)** è la differenza tra un sistema che tiene quando gli utenti crescono e uno che rallenta fino a fermarsi. Con pochi dati non te ne accorgi; il codice O(n²) passa i test e va in produzione — poi arriva il carico vero e il sistema muore. La complessità è ciò che ti fa vedere il problema **prima**.
- **La struttura dati cambia la classe.** Scegliere **hash map invece di lista** trasforma una ricerca da O(n) a O(1). La scelta della struttura dati **è** una scelta di complessità: non è un dettaglio, è *la* leva (aggancio a `prog-ds`).
- **Le query lente sui database.** È la stessa idea. Una query senza **indice** fa uno **scan** dell'intera tabella, **O(n)** sulle righe. Aggiungere un **indice** (una struttura ordinata pensata apposta) trasforma la ricerca in circa **O(log n)** — la ricerca binaria applicata al database. Ecco perché "aggiungi un indice" è la prima risposta a "la query è lenta" (aggancio a system design).

## Errori comuni

- **Ottimizzare la costante invece della classe.** Rendere il tuo O(n²) "scritto meglio" (meno operazioni per giro) non lo salva: un O(n) anche "scritto peggio" alla scala lo **stracci** comunque. Prima cambia la **classe**, poi semmai limi la costante.
- **Ignorare la complessità spaziale.** Un algoritmo velocissimo che divora tutta la RAM può essere inutilizzabile. Il tempo non è l'unica risorsa: guarda **anche** la memoria.
- **Dimenticare che la ricerca binaria vuole dati ordinati.** Applicarla a un array non ordinato dà risultati sbagliati. E attenzione: se devi **prima ordinare** (O(n log n)) solo per fare una ricerca, forse la lineare O(n) conveniva.
- **Ottimizzare prematuramente dove n è sempre piccolo.** Se n è sempre 5, l'O(n²) va benissimo e il codice più semplice vince. La complessità conta **alla scala**: non incartare codice per un problema che non hai.

## Fonti

- **T. Cormen, C. Leiserson, R. Rivest, C. Stein — *Introduction to Algorithms* (CLRS)**: *il* riferimento accademico su algoritmi e analisi di complessità. Denso ma completo.
- **Aditya Bhargava — *Grokking Algorithms***: divulgativo e molto visuale, perfetto per costruire l'intuizione (Big-O, ricerca binaria, sorting spiegati con disegni).
- **Big-O Cheat Sheet — bigocheatsheet.com**: tabella di riferimento con le complessità (temporali e spaziali) delle strutture dati e degli algoritmi di sorting più comuni.

## Concetti adiacenti

- **prog-ds** — le **strutture dati** (array, lista, hash map, albero): è la scelta della struttura a determinare la complessità delle operazioni.
- **xc-dsa-review** — ripasso trasversale *data structures & algorithms* in ottica colloquio: pattern ricorrenti e come raccontarli.
- **db-index** — gli **indici** dei database: come trasformano uno scan O(n) in una ricerca ~O(log n).
- **xc-sysdesign** — dove la complessità diventa architettura: scegliere algoritmi e strutture che reggono la scala di un sistema reale.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cosa **misura** la complessità di un algoritmo, e perché **non** misuriamo i secondi?
2. Cosa significa la **notazione O grande** (Big-O), e perché si **ignorano le costanti** e i **termini di ordine inferiore**?
3. Cosa significano **O(1)** e **O(log n)**? Fai un esempio per ciascuna.
4. Cosa significano **O(n)**, **O(n log n)** e **O(n²)**? Un esempio a testa.
5. Descrivi la **ricerca binaria**: perché è O(log n) e cosa **richiede** per funzionare?
6. Perché **merge sort** è **O(n log n)** mentre **bubble sort** è **O(n²)**?
7. Come fa una **hash map** a portare una ricerca da O(n) a **O(1)**, e a quale **costo**?
8. Cos'è il **trade-off tempo/spazio**? Fai un esempio.
9. Differenza tra **complessità temporale** e **complessità spaziale**? E cosa si intende di solito per "la complessità" (quale caso)?
10. Cita un **errore comune** nel ragionare sulla complessità e spiega perché è un errore.

<details><summary>Risposte</summary>

1. La complessità misura **come cresce il costo (numero di operazioni o memoria) al crescere della dimensione dell'input n**, cioè l'**andamento asintotico** per n grande. Non misuriamo i **secondi** perché **dipendono dalla macchina** (hardware, linguaggio, compilatore): misurerebbero l'hardware, non l'algoritmo. L'andamento della crescita è invece una proprietà dell'algoritmo stesso.

2. La **O grande** descrive un **limite superiore** alla crescita: O(f(n)) significa "il costo cresce **al più** come f(n), per n grande". Si **ignorano le costanti** (O(2n) = O(n)) perché il fattore costante dipende dall'implementazione/macchina e non cambia la **forma** della crescita; si **ignorano i termini di ordine inferiore** (O(n² + n) = O(n²)) perché **per n grande domina il termine più forte** (con n grande, n² schiaccia n). Resta solo il **termine dominante senza costante**.

3. **O(1) — costante**: tempo **fisso, indipendente da n** (10 o 10 milioni di elementi, stesso costo). Esempio: accedere a `array[7]` per indice, o leggere da una **hash map** data la chiave. **O(log n) — logaritmica**: ad ogni passo **dimezzi** il problema, cresce lentissimamente. Esempio: la **ricerca binaria** su un array ordinato (~20 passi per un milione di elementi).

4. **O(n) — lineare**: scorri **tutti** gli elementi una volta (esempio: cercare in una lista non ordinata). **O(n log n)**: i buoni algoritmi di **ordinamento** (merge sort, quick sort medio). **O(n²) — quadratica**: tipicamente un **doppio ciclo annidato**, raddoppia n e il costo si quadruplica (esempio: confrontare ogni coppia; bubble/insertion sort).

5. La **ricerca binaria** guarda l'elemento **in mezzo** all'array: se è quello cerchi hai finito, altrimenti **scarti la metà** che non può contenerlo e ripeti sulla metà restante. Ad ogni confronto **dimezza** ciò che resta, quindi servono circa **log₂ n** passi → **O(log n)**. **Richiede** che l'array sia **ordinato**, altrimenti "scartare una metà" non ha senso.

6. **Bubble sort** usa **due cicli annidati** (per ogni elemento riscorre gli altri) → **O(n²)**. **Merge sort** usa **divide et impera**: **divide** l'array a metà ripetutamente (circa **log n** livelli) e a ogni livello **unisce (merge)** i pezzi ordinati con costo **O(n)**; log n livelli × O(n) per livello = **O(n log n)**.

7. Una **hash map** associa **chiavi** a valori collocandoli in base a un calcolo sulla chiave, così per cercare la chiave vai **dritto alla posizione** senza scorrere: **O(1)** invece di O(n) della lista. Il **costo** è più **memoria** occupata rispetto a una semplice lista.

8. Il **trade-off tempo/spazio** è scambiare **più memoria** per **più velocità** (o viceversa). Esempio: usare una **hash map** al posto di una lista fa passare la ricerca da O(n) a O(1), ma occupa più memoria — spendi spazio per comprare tempo.

9. **Complessità temporale** = numero di **operazioni** in funzione di n (quanto lavora); **complessità spaziale** = **memoria extra** usata in funzione di n (quanto occupa). Per "la complessità", senza altra specifica, si intende di solito il **caso peggiore**, perché è la **garanzia** che non andrà mai peggio di così.

10. Esempi validi (uno basta): **(a)** ottimizzare la **costante** invece della **classe** — un O(n) batte comunque un O(n²) alla scala, anche se "scritto peggio", quindi conta prima cambiare classe; **(b)** ignorare la **complessità spaziale** — un algoritmo velocissimo che esaurisce la RAM è inutilizzabile; **(c)** dimenticare che la **ricerca binaria richiede dati ordinati**; **(d)** ottimizzare prematuramente dove **n è sempre piccolo**, complicando il codice senza motivo.

</details>
