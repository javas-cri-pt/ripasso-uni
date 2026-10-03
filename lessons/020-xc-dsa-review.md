---
day: 20
topic_id: xc-dsa-review
title: "Strutture dati da colloquio — array, hash map, alberi, grafi"
area: cross-cutting
course: Data Structures & Algorithms (ripasso da colloquio)
grounded_in: "UNIBO/primoAnno/Fondamenti di Informatica 2"
adjacent: [prog-ds, prog-algo, db-index]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo (complessità inclusa)."
---

# Strutture dati da colloquio — array, hash map, alberi, grafi

> **Perché oggi:** ieri hai ripassato il Big-O (giorno 18); oggi lo applichi. Ai colloqui tecnici la domanda quasi sempre non è "che algoritmo?" ma "**che struttura dati** scelgo perché l'operazione che mi serve sia veloce?". Sapere il costo di *lookup / insert / delete* di ciascuna è metà del lavoro.

## L'idea di fondo
Una **struttura dati** è un modo di **organizzare i dati in memoria** per rendere veloci le operazioni che ti servono. Non esiste la struttura "migliore": esiste quella giusta **per l'operazione dominante** del tuo problema (cercare? inserire in mezzo? tenere ordinato? prendere il minimo?). Il trucco da colloquio è dire il **perché** in termini di complessità (`O(...)`, "quante operazioni al crescere di n").

<svg viewBox="0 0 660 250" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="80" y="24" font-weight="700">Array</text>
    <g>
      <rect x="20" y="34" width="34" height="30" fill="var(--card)" stroke="var(--rule)"/><text x="37" y="54">a</text>
      <rect x="54" y="34" width="34" height="30" fill="var(--card)" stroke="var(--rule)"/><text x="71" y="54">b</text>
      <rect x="88" y="34" width="34" height="30" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="105" y="54">c</text>
      <rect x="122" y="34" width="34" height="30" fill="var(--card)" stroke="var(--rule)"/><text x="139" y="54">d</text>
    </g>
    <text x="88" y="80" font-size="10.5" fill="var(--muted)">indice → O(1); cercare un valore → O(n)</text>

    <text x="330" y="24" font-weight="700">Hash map</text>
    <rect x="250" y="34" width="70" height="30" fill="var(--card)" stroke="var(--rule)"/><text x="285" y="54" font-size="11">"nome"</text>
    <text x="330" y="53">→</text>
    <rect x="345" y="34" width="60" height="30" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="375" y="54">valore</text>
    <text x="330" y="80" font-size="10.5" fill="var(--muted)">chiave → valore, ~O(1) medio</text>

    <text x="560" y="24" font-weight="700">Albero (BST)</text>
    <circle cx="560" cy="42" r="13" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="560" y="46">8</text>
    <circle cx="525" cy="78" r="13" fill="var(--card)" stroke="var(--rule)"/><text x="525" y="82">3</text>
    <circle cx="595" cy="78" r="13" fill="var(--card)" stroke="var(--rule)"/><text x="595" y="82">12</text>
    <g stroke="var(--muted)" stroke-width="1.3"><path d="M551,52 L534,68"/><path d="M569,52 L586,68"/></g>
    <text x="560" y="104" font-size="10.5" fill="var(--muted)">ricerca ordinata → O(log n) se bilanciato</text>
  </g>
  <line x1="20" y1="128" x2="640" y2="128" stroke="var(--rule)"/>
  <g font-size="11.5" fill="var(--ink)">
    <text x="20" y="150" font-weight="700">Costo tipico (medio)</text>
    <text x="20" y="172">Array / lista dinamica:  accesso per indice O(1) · ricerca O(n) · push in fondo ~O(1)</text>
    <text x="20" y="192">Hash map (dizionario):  lookup / insert / delete ~O(1) medio, O(n) nel caso pessimo</text>
    <text x="20" y="212">Albero di ricerca bilanciato:  ricerca / insert / delete O(log n), e resta ORDINATO</text>
    <text x="20" y="232">Lista collegata:  inserire/togliere in un punto noto O(1) · ma cercare O(n)</text>
  </g>
</svg>

## Le strutture che devi padroneggiare

**Array (e lista dinamica, es. `list` di Python):** elementi **contigui** in memoria, accesso per **indice** in `O(1)`. Aggiungere in fondo è ammortizzato `O(1)`; inserire/togliere **in mezzo** è `O(n)` (devi spostare gli altri). Cercare un valore (non l'indice) è `O(n)`. Default quasi sempre ragionevole.

**Lista collegata (linked list):** nodi sparsi, ognuno punta al successivo. Inserire/rimuovere **dato un puntatore al punto** è `O(1)` (non sposti nulla), ma **accedere all'i-esimo** o cercare è `O(n)`. Utile quando fai tante inserzioni/rimozioni ai bordi (base di code e stack).

**Stack e coda:**
- **Stack** = **LIFO** (Last In, First Out): l'ultimo che entra è il primo che esce (una pila di piatti). Operazioni `push`/`pop` in `O(1)`. Usato per undo, ricorsione, parsing.
- **Coda (queue)** = **FIFO** (First In, First Out): il primo che entra è il primo che esce (la fila alle poste). Usata per buffer, scheduling, BFS.

**Hash map (dizionario / mappa):** coppie **chiave → valore**. Una funzione **hash** trasforma la chiave in una posizione in un array, quindi lookup/insert/delete sono **~`O(1)` in media**. Caso pessimo `O(n)` se troppe chiavi finiscono nella stessa posizione (**collisione**), gestito con liste o rehashing. È la struttura che risolve più problemi da colloquio: "hai già visto questo elemento?", contare occorrenze, deduplicare, indicizzare per id.

**Set (insieme):** come una hash map senza valori: appartenenza (`x è dentro?`) in `~O(1)`. Perfetto per "elementi unici" o "visti/non visti".

**Albero binario di ricerca (BST):** ogni nodo ha figli sinistro (più piccoli) e destro (più grandi). Ricerca/inserimento in `O(log n)` **se l'albero è bilanciato** (alto ~log n). Se si sbilancia degenera in una lista → `O(n)`: per questo esistono alberi **auto-bilancianti** (AVL, red-black) e, su disco, il **B-tree** che è alla base degli **indici dei database** (giorno 19). Vantaggio sulla hash map: i dati restano **ordinati** (puoi fare range, min/max, "il successivo").

**Grafo:** nodi + archi (relazioni). Modella reti, dipendenze, il grafo clienti-progetti-task di Taska. Si esplora con **BFS** (Breadth-First Search, a ondate, usa una coda: trova il cammino più corto in archi) o **DFS** (Depth-First Search, in profondità, usa uno stack/ricorsione: buono per esplorare tutto, rilevare cicli).

## Come si sceglie (il ragionamento da dire a voce)
1. Qual è l'**operazione dominante**? (lookup per chiave? mantenere ordine? prendere sempre il minimo? inserire ai bordi?)
2. Prendi la struttura che rende **quella** operazione più economica.
3. Dichiara il **costo** in Big-O e il **caso pessimo**.

Esempi rapidi: "conta le parole ripetute" → **hash map** (chiave=parola, valore=conteggio), `O(n)`. "Dammi sempre il task a priorità più alta" → **heap / coda a priorità**, estrazione del minimo in `O(log n)`. "Tieni una classifica sempre ordinata" → **albero bilanciato**. "Hai già visto questo id?" → **set**.

## Esempio concreto (roba tua)
Il retrieval **ibrido con router** di Taska (giorno 4) è una scelta di struttura: la **traversata di grafo** sfrutta una struttura a **grafo** (entità collegate), mentre le domande aggregate vanno a una **query strutturata** sul DB (indici = **B-tree**). Diverse strutture per diverse operazioni, scelte in base a *quale* domanda arriva: è lo stesso ragionamento del punto sopra, a livello di sistema.

## Completeness check (integrato da me)
- **Heap / coda a priorità:** albero speciale che tiene sempre in cima il minimo (o massimo); `push`/`pop-min` in `O(log n)`. È la struttura dietro Dijkstra e gli scheduler.
- **Ammortizzato ≠ medio:** "ammortizzato `O(1)`" (es. `append` su array dinamico) vuol dire che *ogni tanto* un'operazione costa `O(n)` (raddoppio dell'array) ma **spalmata** su molte operazioni il costo medio resta costante. Concetto diverso dal "caso medio" probabilistico della hash map.

## Fonti
- **NeetCode** — neetcode.io (pattern di problemi da colloquio per struttura)
- **VisuAlgo** — visualgo.net (animazioni di strutture e algoritmi)
- **Big-O Cheat Sheet** — bigocheatsheet.com

## Concetti adiacenti
- `prog-algo` — Big-O, sorting, ricerca (il giorno 18, la base di oggi)
- `prog-ds` — strutture dati nel corso di Fondamenti
- `db-index` — gli indici dei DB sono B-tree: stessa idea, su disco

## Quiz (10 — tutte rispondibili dalla lezione)
1. Perché l'accesso per **indice** in un array è `O(1)` ma cercare un **valore** è `O(n)`?
2. Qual è il costo medio di lookup/insert in una **hash map** e qual è il suo caso pessimo (e perché)?
3. Differenza tra **stack** e **coda** (sigle e comportamento)?
4. Qual è il vantaggio di un **albero di ricerca bilanciato** rispetto a una hash map?
5. Cosa succede a un BST se si **sbilancia**, e come si evita?
6. Quando conviene una **lista collegata** rispetto a un array?
7. A cosa serve un **set** e con che costo?
8. Differenza tra **BFS** e **DFS** e quale struttura usa ciascuno?
9. Cos'è una **coda a priorità (heap)** e con che costo estrai il minimo?
10. Cosa vuol dire "costo **ammortizzato** `O(1)`" e in cosa differisce dal caso medio?

<details><summary>Risposte</summary>

1. Gli elementi sono **contigui**: l'indirizzo dell'i-esimo si calcola con un'aritmetica costante; ma per trovare un **valore** senza conoscerne la posizione devi scorrere fino a `n` elementi.
2. **~`O(1)` medio**; caso pessimo **`O(n)`** quando molte chiavi collidono nella stessa posizione (hanno lo stesso hash) e si degrada a scorrere una lista.
3. **Stack = LIFO** (ultimo entrato, primo uscito); **coda = FIFO** (primo entrato, primo uscito). Entrambi con operazioni `O(1)`.
4. I dati restano **ordinati**: puoi fare range, min/max e "il successivo" in `O(log n)`, cosa che la hash map (non ordinata) non permette.
5. Degenera in una **lista** → operazioni `O(n)`; si evita con alberi **auto-bilancianti** (AVL, red-black) che mantengono l'altezza ~`log n`.
6. Quando fai molte **inserzioni/rimozioni ai bordi** (o dato un puntatore al punto) e non ti serve l'accesso per indice: quelle sono `O(1)` invece di `O(n)`.
7. A dire se un elemento è **presente** (unicità/"già visto?"), con costo **~`O(1)`**.
8. **BFS** esplora a ondate (usa una **coda**, trova il cammino più corto in numero di archi); **DFS** va in profondità (usa **stack**/ricorsione, buono per visitare tutto e trovare cicli).
9. Un albero che tiene in cima il minimo (o massimo); estrarre il minimo costa **`O(log n)`**.
10. Vuol dire che, **spalmato** su molte operazioni, il costo medio è costante anche se **qualche** operazione singola costa `O(n)` (es. il raddoppio dell'array); è deterministico sulla sequenza, non probabilistico come il caso medio della hash map.
</details>
