---
day: 26
topic_id: prog-ds
title: "Strutture dati: array, liste, hash map, alberi, grafi"
area: computer-science
course: "Programmazione & OOP"
grounded_in: null
adjacent: [prog-algo, xc-dsa-review, db-index]
completeness_checked: true
quiz_count: 10
---

# Strutture dati

> **Perché oggi:** al giorno 18 (`prog-algo`) hai imparato a misurare il costo di un algoritmo con il Big-O. Oggi scopri che quel costo spesso **non dipende dall'algoritmo ma dalla struttura dati** che gli metti sotto: cercare un valore costa `O(n)` in un array e `~O(1)` in una hash map, *lo stesso* identico "cercare". Scegliere la struttura giusta è la domanda da colloquio più ricorrente ("quale struttura usi, e perché?"). Qui le vediamo una per una con la complessità di accesso, ricerca e inserimento.

## Cos'è una struttura dati e come se ne misura il costo
Una **struttura dati** è un modo di organizzare i dati in memoria insieme alle operazioni che ci puoi fare sopra (inserire, cercare, rimuovere, scorrere). Per ciascuna operazione si indica il costo in **Big-O**, cioè come cresce il numero di passi al crescere di `n` (quanti elementi contiene). Le tre operazioni che confronteremo sempre sono: **accesso** (leggere l'elemento in una certa posizione), **ricerca** (trovare un elemento di cui conosci solo il valore) e **inserimento** (aggiungere un elemento). La struttura "migliore" non esiste: esiste quella che rende economica l'**operazione dominante** del tuo problema.

## Array
Un **array** tiene gli elementi in celle di memoria **contigue** (una dopo l'altra). Siccome conosce l'indirizzo di partenza e la dimensione di ogni cella, l'indirizzo dell'elemento `i` si calcola con un'aritmetica costante: **accesso per indice `O(1)`**. Il prezzo di questa contiguità è la rigidità:
- **Ricerca di un valore** (non conosci la posizione): devi scorrere, `O(n)`. Eccezione importante: se l'array è **ordinato** puoi usare la **ricerca binaria** e scendere a `O(log n)`.
- **Inserimento/rimozione in testa o in mezzo:** `O(n)`, perché devi spostare tutti gli elementi successivi di una posizione.
- **Aggiunta in fondo (array dinamico**, es. `list` di Python, `ArrayList` di Java): **ammortizzato `O(1)`**. "Ammortizzato" significa che ogni tanto l'array è pieno e va **raddoppiato** copiando tutto (`O(n)`), ma spalmando quel costo su tutte le aggiunte precedenti la media resta costante.

## Lista concatenata (linked list)
Una **lista concatenata** non è contigua: ogni elemento è un **nodo** sparso in memoria che contiene il valore e un **puntatore** al nodo successivo. Questo ribalta i costi rispetto all'array:
- **Inserimento in testa `O(1)`:** crei un nodo e lo fai puntare al vecchio primo elemento, senza spostare nulla.
- **Accesso all'`i`-esimo elemento `O(n)`:** non c'è aritmetica di indirizzi, devi seguire i puntatori uno a uno dall'inizio.
- **Lista semplice (singly linked)** ha solo il puntatore al successivo; **lista doppia (doubly linked)** ha anche quello al predecessore. Dettaglio da colloquio: **cancellare un nodo di cui hai già il puntatore** è `O(1)` solo nella lista **doppia**; nella lista semplice ti serve anche il **predecessore** (per ricucire i puntatori), e trovarlo costa `O(n)`.
- **Inserimento in fondo `O(1)`** solo se tieni un **puntatore alla coda** (tail), altrimenti devi scorrere fino alla fine, `O(n)`.

Conviene quando fai molte inserzioni/rimozioni ai bordi e non ti serve l'accesso per indice. È la base con cui si costruiscono stack e code.

## Stack e coda (queue)
Sono strutture definite non da *come* sono fatte ma da *quale ordine* impongono. Entrambe hanno le operazioni fondamentali in `O(1)`.
- **Stack = LIFO** (Last In, First Out): l'ultimo che entra è il primo che esce, come una pila di piatti. Operazioni `push` (metti sopra) e `pop` (togli da sopra). Usato per: undo, la pila delle chiamate di funzione (ricorsione), il pulsante "indietro" del browser, parsing di parentesi.
- **Coda = FIFO** (First In, First Out): il primo che entra è il primo che esce, come la fila alle poste. Operazioni `enqueue` (in fondo) e `dequeue` (dalla testa). Attenzione all'implementazione: una coda fatta con un array "ingenuo" ha `dequeue` `O(n)` (devi spostare tutti in avanti); con un **buffer circolare** o una **deque** (coda a due estremità) torna `O(1)`. Usata per: buffer, scheduling, e la visita BFS dei grafi.

## Hash map (dizionario / mappa)
Una **hash map** memorizza coppie **chiave → valore** e promette lookup, insert e delete in **`~O(1)` medio**. Il trucco è la **funzione di hash**: trasforma la chiave (anche una stringa) in un numero, che modulo il numero di celle (`m`, i **bucket**) dà la posizione dove mettere/cercare il valore. Niente scorrimento: vai diretto alla cella.

Il problema sono le **collisioni**: due chiavi diverse possono finire nello stesso bucket. Due strategie classiche per gestirle:
- **Concatenamento (chaining):** ogni bucket contiene una piccola lista delle coppie finite lì; in caso di collisione la si scorre.
- **Indirizzamento aperto (open addressing):** se il bucket è occupato si cerca il successivo libero secondo una regola.

La qualità dipende dal **fattore di carico** `α = n/m` (elementi diviso bucket): più è alto, più collisioni e più ci si avvicina al **caso pessimo `O(n)`** (tutte le chiavi nello stesso bucket → è di fatto una lista). Per questo, quando `α` supera una soglia (Java usa `0.75`), scatta il **rehashing**: si crea una tabella più grande e si reinseriscono tutte le chiavi. È la struttura che risolve più problemi: "ho già visto questo elemento?", contare occorrenze, deduplicare, indicizzare per id. Un **set** (insieme) è la stessa cosa senza i valori: serve solo a dire se un elemento è **presente**, sempre `~O(1)`.

## Alberi: albero binario di ricerca (BST)
Un **albero** è una gerarchia di nodi: una radice, e ogni nodo con dei figli. In un **albero binario di ricerca (BST)** ogni nodo ha al più due figli e vale l'invariante: **tutto ciò che sta a sinistra è minore del nodo, tutto ciò che sta a destra è maggiore**. Cercare un valore diventa come la ricerca binaria: a ogni nodo scarti metà albero.

Il costo di ricerca/inserimento/rimozione è **`O(h)`**, dove `h` è l'**altezza** dell'albero. Se l'albero è **bilanciato** (sinistra e destra sempre di altezza simile) allora `h ≈ log n` e sei a **`O(log n)`**. Ma se inserisci valori già ordinati, l'albero si **sbilancia** e degenera in una lista: `h = n` e torni a `O(n)`. Per evitarlo esistono alberi **auto-bilancianti** (AVL, red-black) che riaggiustano la forma a ogni inserimento. Due vantaggi del BST sulla hash map: i dati restano **ordinati** (una **visita in-order** li restituisce in ordine crescente) e puoi fare query di **intervallo** e **min/max/successivo**, cose che una hash map (non ordinata) non permette.

## Heap (coda di priorità)
Un **heap** è un albero binario con una regola più debole del BST: ogni genitore è **≤ dei figli** (min-heap) oppure **≥** (max-heap). **Non è ordinato**: garantisce solo chi sta in cima, cioè il minimo (o massimo). In pratica si memorizza in un **array**, non con i puntatori: i figli del nodo `i` stanno in posizione `2i+1` e `2i+2`, il che lo rende compatto e veloce. Costi:
- **Peek** (guarda il minimo in cima): `O(1)`.
- **Insert** ed **extract-min** (estrai e togli il minimo): `O(log n)`.
- **Build-heap** (costruirlo da `n` elementi): `O(n)`.

È l'implementazione della **coda a priorità**: "dammi sempre l'elemento più importante". Sta dietro l'algoritmo di Dijkstra e agli scheduler a priorità.

## Grafi
Un **grafo** è un insieme di **nodi (vertici, `V`)** collegati da **archi (`E`)**: modella reti, dipendenze, relazioni ("chi segue chi", "quale task dipende da quale"). Due modi di rappresentarlo, con un netto trade-off:
- **Matrice di adiacenza:** una tabella `V × V` dove la cella `[i][j]` dice se c'è un arco. **Spazio `O(V²)`**, controllare se due nodi sono connessi è **`O(1)`**, ma elencare i vicini di un nodo costa **`O(V)`**. Conviene sui grafi **densi** (molti archi).
- **Liste di adiacenza:** per ogni nodo, la lista dei suoi vicini. **Spazio `O(V+E)`**, elencare i vicini è `O(grado del nodo)`, controllare un singolo arco è `O(grado)`. Conviene sui grafi **sparsi** (pochi archi), che è il caso più comune.

Si esplorano in due modi, entrambi **`O(V+E)`** con liste di adiacenza (e `O(V²)` con la matrice):
- **BFS (Breadth-First Search):** esplora "a ondate", livello per livello, usando una **coda (FIFO)**. Su un grafo **non pesato** trova il **cammino più corto** in numero di archi.
- **DFS (Depth-First Search):** va in profondità finché può, poi torna indietro, usando uno **stack** (o la ricorsione). Utile per visitare tutto, trovare componenti connesse e rilevare **cicli**.

## Quando usare cosa (il ragionamento da dire a voce)
1. Qual è l'**operazione dominante**? Lookup per chiave? Mantenere l'ordine? Prendere sempre il minimo? Inserire ai bordi? Cammino più corto?
2. Scegli la struttura che rende *quella* operazione più economica.
3. Dichiara il **costo** in Big-O e il **caso pessimo**.

In breve: lookup per chiave → **hash map**; "già visto?" / unicità → **set**; ordine + range + min/max → **albero bilanciato**; "sempre il più prioritario" → **heap**; inserimenti ai bordi → **lista**; accesso per indice / ordinato con ricerca binaria → **array**; relazioni e percorsi → **grafo**.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 680 250" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="150" y="22" font-weight="700">Hash map: chiave → bucket</text>
    <rect x="20" y="40" width="110" height="26" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="75" y="57" font-size="11">"anna"</text>
    <rect x="20" y="74" width="110" height="26" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="75" y="91" font-size="11">"luca"</text>
    <rect x="20" y="108" width="110" height="26" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="75" y="125" font-size="11">"sara"</text>
    <text x="165" y="60" font-size="10.5" fill="var(--muted)">hash()</text>
    <text x="165" y="94" font-size="10.5" fill="var(--muted)">hash()</text>
    <text x="165" y="128" font-size="10.5" fill="var(--muted)">hash()</text>
    <rect x="210" y="34" width="46" height="28" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="233" y="52" font-size="11">0</text>
    <rect x="210" y="66" width="46" height="28" rx="5" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="233" y="84" font-size="11">1</text>
    <rect x="210" y="98" width="46" height="28" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="233" y="116" font-size="11">2</text>
    <rect x="210" y="130" width="46" height="28" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="233" y="148" font-size="11">3</text>
    <text x="233" y="178" font-size="10" fill="var(--muted)">4 bucket</text>
    <rect x="300" y="66" width="120" height="28" rx="5" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="360" y="84" font-size="10.5">"luca" + "sara"</text>
    <text x="360" y="112" font-size="10" fill="var(--muted)">collisione → lista nel bucket</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none"><path d="M130,53 L208,48"/><path d="M130,87 L208,80"/><path d="M130,121 L208,80"/><path d="M256,80 L298,80"/></g>
  <line x1="460" y1="30" x2="460" y2="200" stroke="var(--rule)"/>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="575" y="22" font-weight="700">Albero binario di ricerca</text>
    <circle cx="575" cy="52" r="15" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="575" y="57">8</text>
    <circle cx="525" cy="100" r="15" fill="var(--card)" stroke="var(--rule)"/><text x="525" y="105">3</text>
    <circle cx="625" cy="100" r="15" fill="var(--card)" stroke="var(--rule)"/><text x="625" y="105">12</text>
    <circle cx="595" cy="148" r="15" fill="var(--card)" stroke="var(--rule)"/><text x="595" y="153">10</text>
    <g stroke="var(--muted)" stroke-width="1.3"><path d="M564,63 L536,89"/><path d="M586,63 L614,89"/><path d="M616,112 L604,137"/></g>
    <text x="575" y="186" font-size="10.5" fill="var(--muted)">sinistra &lt; nodo &lt; destra · ricerca O(log n) se bilanciato</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">A sinistra una hash map: la funzione hash manda ogni chiave in un bucket (lookup ~O(1)); "luca" e "sara" collidono nello stesso bucket e lì si tiene una lista. A destra un BST: l'invariante sinistra &lt; nodo &lt; destra permette la ricerca in O(log n) quando l'albero è bilanciato.</figcaption>
</figure>

## Esempi concreti
- **Hash map per deduplicare:** hai una lista di email con duplicati e vuoi gli elementi unici. Scorri una volta (`O(n)`) inserendo ogni email in un **set**: inserire un doppione non cambia nulla, e alla fine il set contiene solo gli unici. Con un array dovresti, per ogni elemento, controllare se è già presente (`O(n)` ciascuno), per un totale `O(n²)`.
- **Albero (B-tree) per gli indici di un database:** un indice serve a non scorrere tutta la tabella a ogni `WHERE`. È organizzato come un **B-tree** (in pratica un **B+tree**), una generalizzazione dell'albero di ricerca pensata per il disco: altezza bassissima, ricerca in `O(log n)`, e tiene le chiavi **ordinate** così da supportare anche le query di intervallo (`BETWEEN`, `ORDER BY`). È lo stesso principio del BST visto sopra, adattato alla memoria su disco (vedi `db-index`).

## Notable use case
- **Python `dict`** è una hash table con **indirizzamento aperto**; i costi tipici di lookup/insert sono `~O(1)` medio (fonte: la pagina TimeComplexity del wiki di Python).
- **Java `HashMap`** gestisce le collisioni con il **concatenamento** e, quando un bucket supera 8 elementi, **trasforma la lista in un albero** per limitare il caso pessimo; fa rehashing oltre il fattore di carico `0.75`.
- **InnoDB** (motore di MySQL) memorizza ogni tabella come un **B+tree clusterizzato** sulla chiave primaria: i dati *sono* l'indice.
- **Git** conserva la storia come un **DAG** (grafo diretto aciclico) di commit: ogni commit punta ai genitori.
- **Dijkstra** (cammini minimi) usa una **coda a priorità** (heap) per prendere ogni volta il nodo più vicino non ancora processato.
- **Il pulsante "indietro" del browser** è uno **stack** (LIFO): l'ultima pagina visitata è la prima a cui torni.

## Fonti
- **CLRS** — Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms* (il riferimento su strutture dati e complessità)
- **VisuAlgo** — visualgo.net (animazioni di hash table, BST, heap, grafi)
- **Big-O Cheat Sheet** — bigocheatsheet.com (tabella riassuntiva dei costi)
- **Python Time Complexity** — wiki.python.org/moin/TimeComplexity

## Concetti adiacenti
- `prog-algo` — Big-O, ordinamento e ricerca (il giorno 18, la base per misurare i costi di oggi)
- `xc-dsa-review` — le stesse strutture viste con taglio da colloquio (giorno 20)
- `db-index` — gli indici dei database sono B-tree: stessa idea di oggi, applicata al disco

## Quiz (10 — tutte rispondibili dalla lezione)
1. Perché l'accesso per indice in un array è `O(1)`, e in quale caso la ricerca di un valore in un array scende da `O(n)` a `O(log n)`?
2. Cosa vuol dire che l'aggiunta in fondo a un array dinamico è "ammortizzata `O(1)`", e cosa succede "ogni tanto"?
3. In una lista concatenata, perché cancellare un nodo di cui hai già il puntatore è `O(1)` solo se la lista è **doppia**?
4. Cos'è la **funzione di hash** e come porta la hash map a un lookup `~O(1)`?
5. Cos'è il **fattore di carico** `α` di una hash map, e cosa scatta quando supera la soglia (es. `0.75` in Java)?
6. Cita due strategie per gestire le **collisioni** in una hash map e spiega in breve la differenza.
7. In un BST, da cosa dipende il costo delle operazioni, e cosa restituisce una **visita in-order**?
8. Un heap è una struttura **ordinata**? Qual è la sua regola, e con che costo fai `peek` ed `extract-min`?
9. Confronta **matrice** e **liste di adiacenza** per un grafo: spazio e costo di controllare un arco / elencare i vicini. Quale conviene su un grafo sparso?
10. Differenza tra **BFS** e **DFS** (quale struttura ausiliaria usa ciascuna) e su che tipo di grafo la BFS garantisce il cammino più corto?

<details><summary>Risposte</summary>

1. Perché gli elementi sono in memoria **contigua**: l'indirizzo dell'`i`-esimo si calcola con un'aritmetica costante. La ricerca di un valore scende a `O(log n)` quando l'array è **ordinato** e usi la **ricerca binaria**.
2. Vuol dire che, **spalmato** su tutte le aggiunte, il costo medio di ogni `append` è costante; "ogni tanto" l'array è pieno e va **raddoppiato** copiando tutti gli elementi in uno nuovo (`O(n)`), ma quel costo diluito sulle operazioni precedenti resta `O(1)` medio.
3. Perché per rimuovere il nodo devi **ricucire** i puntatori saltandolo: ti serve il **predecessore**. La lista doppia tiene il puntatore al predecessore (quindi `O(1)`); nella lista semplice il predecessore va cercato dall'inizio, `O(n)`.
4. È una funzione che trasforma la chiave in un numero, usato (modulo il numero di bucket) come **posizione diretta** nell'array interno: così non si scorre, si va subito alla cella giusta, da cui il lookup `~O(1)` medio.
5. `α = n/m`, numero di elementi diviso numero di bucket: misura quanto è "piena". Quando supera la soglia scatta il **rehashing**: si alloca una tabella più grande e si **reinseriscono** tutte le chiavi, per tenere basse le collisioni.
6. **Concatenamento (chaining):** ogni bucket tiene una lista delle coppie finite lì. **Indirizzamento aperto (open addressing):** se il bucket è occupato si cerca la cella libera successiva. Nel primo le collisioni stanno "fuori" in liste, nel secondo si risolvono "dentro" l'array stesso.
7. Dal costo `O(h)`, con `h` l'**altezza**: `O(log n)` se l'albero è bilanciato, fino a `O(n)` se degenera in lista. Una **visita in-order** restituisce le chiavi in **ordine crescente**.
8. No, un heap **non è ordinato**: garantisce solo la regola **genitore ≤ figli** (min-heap) o **≥** (max-heap), quindi solo chi sta in cima. `peek` del minimo è `O(1)`, `extract-min` è `O(log n)`.
9. **Matrice:** spazio `O(V²)`, controllo di un arco `O(1)`, elencare i vicini `O(V)`. **Liste di adiacenza:** spazio `O(V+E)`, elencare i vicini `O(grado)`, controllo di un arco `O(grado)`. Su un grafo **sparso** conviene la lista di adiacenza.
10. **BFS** usa una **coda (FIFO)** ed esplora a ondate; **DFS** usa uno **stack**/ricorsione e va in profondità. La BFS garantisce il cammino più corto (in numero di archi) solo su grafi **non pesati**.
</details>
