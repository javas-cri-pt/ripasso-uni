---
day: 30
topic_id: db-index
title: "Indici e ottimizzazione delle query"
area: computer-science
course: "Basi di Dati / Sistemi Informativi"
grounded_in: null
adjacent: [db-er, prog-ds, xc-sysdesign]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun termine lasciato senza definizione."
---

# Indici e ottimizzazione delle query

> **Perché oggi:** quando un'applicazione diventa lenta, nove volte su dieci la colpa è una query che scansiona l'intera tabella invece di saltare dritta alle righe giuste. L'**indice** è il singolo fattore che più spesso trasforma una query da lenta a istantanea, e capirlo significa applicare al database quello che già sai di **Big-O** e **strutture dati**: un indice è nient'altro che un albero di ricerca (o una tabella hash) costruito sui tuoi dati. È anche uno dei temi più ricorrenti ai colloqui backend e di system design ("questa query è lenta, come la sistemi?"), perché separa chi usa il database da chi lo capisce.

## Il problema: trovare una riga in mezzo a milioni
Immagina una tabella `Utente` con 5 milioni di righe e la query `SELECT * FROM Utente WHERE email = 'mario@x.it'`. Il database deve restituirti quella riga. Ha due modi.

- **Full table scan (scansione completa):** il database legge **tutte** le righe, una per una, e per ciascuna controlla se `email` corrisponde. Su 5 milioni di righe sono 5 milioni di confronti: costo **O(n)**, lineare nel numero di righe. Finché la tabella è piccola va bene; quando cresce, i tempi crescono con lei.
- **Index seek (ricerca tramite indice):** se esiste un **indice** sulla colonna `email`, il database non guarda la tabella: interroga l'indice, che è una struttura dati pensata per trovare in fretta, salta direttamente al punto giusto e recupera la riga. Costo tipico **O(log n)**: su 5 milioni di righe sono una ventina di passi invece di 5 milioni.

La differenza tra O(n) e O(log n) è esattamente la differenza tra cercare un nome sfogliando l'elenco telefonico pagina per pagina e usarlo come è fatto per essere usato: ordinato, aprendolo a metà e dimezzando ogni volta.

## Cos'è un indice
Un **indice** è una **struttura dati aggiuntiva**, mantenuta dal database accanto alla tabella, che permette di trovare le righe che soddisfano una condizione **senza scansionare l'intera tabella**. Contiene i valori di una (o più) colonne, tenuti in un ordine o in una forma che rende la ricerca veloce, e per ogni valore un **puntatore** alla riga corrispondente nella tabella.

Il paragone giusto è l'indice analitico in fondo a un libro: non rileggi tutto il libro per trovare dove si parla di "normalizzazione", vai all'indice (ordinato alfabeticamente), trovi la voce e il numero di pagina, e salti lì. L'indice del database fa la stessa cosa: è una copia ordinata e ricercabile di una colonna, più il "numero di pagina" (il puntatore) verso la riga vera.

Un indice **non cambia i dati**: è una struttura di supporto. Puoi crearlo e cancellarlo in qualsiasi momento senza perdere nulla, cambi solo *la velocità* con cui certe query vengono eseguite.

## Le strutture dati sotto gli indici
Un indice è veloce perché sotto c'è una struttura dati adatta. Le due famiglie principali sono il B-tree e l'hash index.

### B-tree e B+tree
Il **B-tree** (albero bilanciato) e la sua variante **B+tree** sono la struttura usata dalla **stragrande maggioranza degli indici** nei database relazionali. È un albero di ricerca tenuto sempre **bilanciato**: tutte le foglie stanno alla stessa profondità, quindi ogni ricerca costa lo stesso numero di passi, pari all'altezza dell'albero, cioè **O(log n)**.

Caratteristiche che contano:

- **Ricerca per uguaglianza** (`email = 'x'`): si scende dalla radice alle foglie, **O(log n)**.
- **Range query** (`eta BETWEEN 18 AND 30`, `prezzo > 100`, `nome LIKE 'Mar%'`): qui sta il punto di forza. Nel **B+tree** tutte le chiavi stanno nelle **foglie**, collegate tra loro in una lista ordinata. Trovato il primo valore del range, basta **scorrere le foglie in sequenza** fino alla fine del range. Un hash index, che vedremo, non può farlo.
- **ORDER BY**: siccome l'indice tiene già i valori **ordinati**, il database può restituire i risultati ordinati leggendo l'indice, senza doverli ordinare a parte.

Il motivo per cui i DB scelgono i B+tree e non, per dire, un albero binario, è pratico: ogni **nodo** del B+tree contiene **molte chiavi** (tipicamente centinaia) e corrisponde a un blocco di disco. Con tanti figli per nodo l'albero è **molto basso** (bastano **3-4 livelli** per indicizzare milioni di righe), quindi servono pochissime **letture da disco** — l'operazione costosa — per arrivare al dato.

### Hash index
Un **hash index** usa una **tabella hash**: applica una **funzione hash** al valore della colonna e la usa come indirizzo dove trovare il puntatore alla riga. La ricerca per uguaglianza è **O(1)** in media (tempo costante): più veloce del B-tree.

Il grosso limite: **funziona solo per l'uguaglianza** (`=`). Siccome la funzione hash sparpaglia i valori senza mantenere alcun ordine, un hash index **non sa fare range query** (`>`, `<`, `BETWEEN`), né ordinamenti, né ricerche per prefisso. Per questo è utile in casi specifici (lookup esatti), mentre il B+tree resta la scelta di default perché copre uguaglianza *e* range *e* ordinamento.

## Indice clusterizzato vs non clusterizzato
La distinzione riguarda **dove stanno fisicamente i dati** rispetto all'indice.

- **Indice clusterizzato (clustered):** l'indice **determina l'ordine fisico** delle righe sul disco. Le righe della tabella sono salvate **ordinate secondo la chiave dell'indice** — di fatto, i dati *sono* dentro le foglie dell'indice. Conseguenza: ne può esistere **uno solo per tabella** (i dati possono essere ordinati in un solo modo). Una ricerca con l'indice clusterizzato arriva direttamente alla riga, senza un salto in più.
- **Indice non clusterizzato (non-clustered / secondary):** è una struttura **separata** dalla tabella; le sue foglie contengono il valore indicizzato e un **puntatore** alla riga vera (che sta altrove, nel suo ordine). Puoi averne **molti** su una tabella. La ricerca trova nell'indice il puntatore, poi fa un secondo accesso per leggere la riga completa.

Esempio concreto: in **InnoDB** (il motore di MySQL) la **chiave primaria è l'indice clusterizzato**, quindi le righe sono fisicamente ordinate per PK; ogni altro indice è non clusterizzato e, nelle sue foglie, memorizza la PK per poi risalire alla riga.

## Indice composito e regola del prefisso più a sinistra
Un **indice composito** è un indice costruito su **più colonne insieme**, es. un indice su `(cognome, nome)`. L'ordine delle colonne non è un dettaglio: l'indice è ordinato **prima per la prima colonna, poi per la seconda** a parità della prima — come la rubrica, ordinata prima per cognome e poi, a parità di cognome, per nome.

Da qui la **regola del prefisso più a sinistra (leftmost prefix):** un indice composito su `(A, B, C)` può servire le query che filtrano su un **prefisso iniziale e contiguo** delle colonne — cioè su `A`, su `A, B`, o su `A, B, C` — ma **non** una query che filtra **solo su `B`** o **solo su `C`**. Motivo: senza fissare `A` i valori di `B` sono sparsi per tutto l'indice (come cercare tutti i "Mario" nella rubrica senza sapere il cognome: devi scorrerla tutta). Quindi l'ordine delle colonne nell'indice composito va scelto in base a **come filtri davvero** nelle tue query.

## Quali colonne indicizzare
La regola pratica: indicizza le colonne che compaiono dove il database deve **cercare, collegare o ordinare**.

- **WHERE:** le colonne usate nei filtri (`WHERE stato = 'aperto'`), così la selezione usa un index seek invece di uno scan.
- **JOIN:** le colonne usate per collegare tabelle — tipicamente le **chiavi esterne**. Un join tra due tabelle grandi senza indice sulla colonna di join è una delle cause più comuni di lentezza.
- **ORDER BY (e GROUP BY):** le colonne di ordinamento, perché l'indice fornisce già i valori ordinati ed evita un ordinamento a parte.

## Il costo degli indici: perché non si indicizza tutto
Se gli indici rendono le letture veloci, perché non metterne uno su ogni colonna? Perché hanno un **costo**, che si paga sulle **scritture** e sullo **spazio**.

- **Scritture più lente:** ogni `INSERT`, `UPDATE` o `DELETE` deve aggiornare **non solo la tabella ma anche tutti gli indici** che toccano le colonne modificate. Dieci indici significa che ogni inserimento fa dieci aggiornamenti in più. Su una tabella con scritture frequenti, troppi indici rallentano tutto.
- **Spazio su disco:** ogni indice è una struttura dati in più da memorizzare; su tabelle grandi gli indici possono occupare tanto quanto i dati, o di più.

Quindi indicizzare è un **compromesso lettura/scrittura**: si aggiungono indici dove servono query veloci, e si evitano su colonne mai filtrate o su tabelle dominate dalle scritture. Indicizzare tutto è un antipattern.

### Selettività e cardinalità
Un indice conviene quando è **selettivo**, cioè quando il valore cercato restringe a **poche righe**. La **cardinalità** è il numero di valori **distinti** in una colonna: `email` ha cardinalità altissima (quasi tutti i valori diversi → molto selettiva, indice ottimo); una colonna booleana `attivo` (solo `true`/`false`) ha cardinalità 2 → poco selettiva, un indice serve a poco perché ogni valore copre comunque metà tabella, e il database spesso preferisce lo scan.

### EXPLAIN e query plan
Il **query plan** (piano di esecuzione) è la strategia che il database decide per eseguire una query: quale indice usare (o se fare uno scan), in che ordine unire le tabelle, come ordinare. Lo decide un componente chiamato **query optimizer** stimando i costi. Il comando **`EXPLAIN`** (lo stesso nome in PostgreSQL e MySQL) mostra questo piano **senza eseguire** la query: è lo strumento con cui verifichi se la tua query sta davvero usando l'indice (in PostgreSQL `Index Scan`) o se sta facendo una scansione completa (in PostgreSQL `Seq Scan`, in MySQL `type: ALL`). È la prima mossa quando una query è lenta.

### Covering index
Un **covering index** è un indice che contiene **tutte le colonne di cui la query ha bisogno**, sia per filtrare sia per restituire il risultato. In quel caso il database risponde **leggendo solo l'indice**, senza mai toccare la tabella (salta il secondo accesso alla riga). Esempio: query `SELECT nome FROM Utente WHERE email = 'x'` con un indice su `(email, nome)` — l'indice ha sia la colonna del filtro sia quella richiesta, quindi "copre" la query.

## Schema

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 660 320" style="max-width:100%;height:auto;font-family:inherit" role="img" aria-label="Schema di un B+tree: un nodo radice con chiavi di separazione punta a nodi foglia ordinati e collegati tra loro, ognuno con puntatori alle righe della tabella">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6" fill="none" stroke="var(--accent)" stroke-width="1.5"/>
    </marker>
  </defs>
  <g font-size="12.5" fill="var(--ink)">
    <text x="20" y="22" font-size="11" fill="var(--muted)">B+tree su email — ricerca in O(log n), foglie ordinate per le range query</text>
    <!-- radice -->
    <rect x="250" y="40" width="160" height="40" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <line x1="303" y1="40" x2="303" y2="80" stroke="var(--rule)"/>
    <line x1="356" y1="40" x2="356" y2="80" stroke="var(--rule)"/>
    <text x="276" y="65" text-anchor="middle" font-weight="700">A–E</text>
    <text x="330" y="65" text-anchor="middle" font-weight="700">F–L</text>
    <text x="383" y="65" text-anchor="middle" font-weight="700">M–Z</text>
    <text x="420" y="64" text-anchor="start" font-size="11" fill="var(--muted)">radice (nodo interno)</text>
    <!-- collegamenti radice -> foglie -->
    <line x1="276" y1="80" x2="100" y2="150" stroke="var(--accent)" stroke-width="1.4" marker-end="url(#arr)"/>
    <line x1="330" y1="80" x2="330" y2="150" stroke="var(--accent)" stroke-width="1.4" marker-end="url(#arr)"/>
    <line x1="383" y1="80" x2="560" y2="150" stroke="var(--accent)" stroke-width="1.4" marker-end="url(#arr)"/>
    <!-- foglie -->
    <rect x="30" y="156" width="150" height="44" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="105" y="183" text-anchor="middle">Ada · Bea · Dino</text>
    <rect x="255" y="156" width="150" height="44" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="330" y="183" text-anchor="middle">Gina · Leo</text>
    <rect x="480" y="156" width="150" height="44" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="555" y="183" text-anchor="middle">Mara · Nino · Zoe</text>
    <text x="105" y="222" text-anchor="middle" font-size="11" fill="var(--muted)">foglie ordinate</text>
    <!-- lista collegata tra foglie -->
    <line x1="180" y1="178" x2="255" y2="178" stroke="var(--accent2)" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#arr)"/>
    <line x1="405" y1="178" x2="480" y2="178" stroke="var(--accent2)" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#arr)"/>
    <text x="330" y="314" text-anchor="middle" font-size="11" fill="var(--accent2)">foglie collegate in sequenza → range query scorrendole</text>
    <!-- puntatori alle righe -->
    <rect x="255" y="256" width="150" height="40" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="330" y="281" text-anchor="middle" font-size="11.5">righe della tabella</text>
    <line x1="330" y1="200" x2="330" y2="256" stroke="var(--accent)" stroke-width="1.4" marker-end="url(#arr)"/>
    <text x="398" y="236" font-size="11" fill="var(--muted)">puntatore alla riga</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Un B+tree: dalla radice si scende alle foglie in O(log n); le foglie sono ordinate e collegate tra loro (per le range query) e puntano alle righe reali.</figcaption>
</figure>

## Esempi concreti
**Cercare un utente per email su 5 milioni di righe.** Query: `SELECT * FROM Utente WHERE email = 'mario@x.it'`.

- **Senza indice:** full table scan. Il database legge tutte e 5 milioni le righe e confronta `email` una per una. O(n): tempo che cresce linearmente, nell'ordine dei secondi su tabelle grandi, e peggiora man mano che gli utenti aumentano.
- **Con indice su `email`:** index seek su un B+tree. In termini di confronti sono circa 22 passi (log₂ di 5 milioni ≈ 22), ma questi avvengono dentro **soli 3-4 nodi** — cioè 3-4 **letture da disco** — perché ogni nodo contiene centinaia di chiavi; poi un salto alla riga. O(log n): millisecondi, e resta veloce anche se gli utenti decuplicano.

Lo stesso ragionamento su un **JOIN**: `SELECT * FROM Ordine o JOIN Utente u ON o.utente_id = u.id`. Se `utente_id` (la FK) non è indicizzato, per ogni ordine il database rischia di scansionare `Utente`; con l'indice ogni collegamento è un seek. Ecco perché le colonne di join vanno quasi sempre indicizzate.

Un caso di **range query**: `SELECT * FROM Ordine WHERE creato_il BETWEEN '2026-01-01' AND '2026-01-31'`. Con un B+tree su `creato_il` il database trova la prima data del range e **scorre le foglie ordinate** fino alla fine del mese. Un hash index qui sarebbe inutile.

## Notable use case
**PostgreSQL** crea indici **B-tree di default**: quando scrivi `CREATE INDEX ... ON Utente (email)` senza specificare altro, ottieni un B-tree, perché copre il caso più ampio (uguaglianza, range, ordinamento, prefissi). Gli hash index esistono ma si usano solo in casi mirati di sola uguaglianza. Inoltre PostgreSQL **non** indicizza automaticamente le chiavi esterne: sei tu a doverle indicizzare, ed è una svista frequente che rende lenti i join.

**MySQL/InnoDB** ha un comportamento diverso e istruttivo: la **chiave primaria è un indice clusterizzato**, cioè le righe della tabella sono fisicamente ordinate e memorizzate secondo la PK (i dati vivono dentro le foglie dell'indice primario). Ogni indice secondario memorizza nelle foglie il valore indicizzato più il **valore della PK**, e per leggere la riga completa risale tramite la PK all'indice clusterizzato. Questo spiega due cose: perché conviene una PK **piccola** (viene ripetuta in ogni indice secondario) e perché le ricerche per PK sono le più veloci possibili.

## Fonti
- **Database System Concepts** (Silberschatz, Korth, Sudarshan) — db-book.com (capitoli su indicizzazione e B+tree, il riferimento classico)
- **Use The Index, Luke!** — use-the-index-luke.com (guida pratica agli indici e ai query plan, orientata agli sviluppatori)
- **Documentazione PostgreSQL — Indexes** e **MySQL Reference Manual — Optimization and Indexes** (postgresql.org/docs, dev.mysql.com)

## Concetti adiacenti
- `db-er` — Modello ER e relazionale: le chiavi primarie ed esterne che poi diventano i candidati naturali all'indicizzazione (le FK per i join)
- `prog-ds` — Strutture dati: alberi bilanciati, tabelle hash e Big-O, cioè le fondamenta teoriche di ciò che un indice fa sotto il cofano
- `xc-sysdesign` — System design: dove la scelta degli indici diventa una decisione di scalabilità e performance sotto carico

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cos'è un **indice** e a cosa serve? Perché è una struttura "aggiuntiva"?
2. Qual è la differenza tra **full table scan** e **index seek**, e che complessità (Big-O) hanno tipicamente?
3. Perché i database usano un **B+tree** come struttura di default per gli indici? Cita almeno due vantaggi rispetto a un hash index.
4. Cos'è un **hash index**, che complessità ha per l'uguaglianza e qual è il suo limite principale?
5. Qual è la differenza tra indice **clusterizzato** e **non clusterizzato**? Quanti indici clusterizzati può avere una tabella e perché?
6. Cos'è un **indice composito** e cosa dice la **regola del prefisso più a sinistra**? Fai un esempio di query che l'indice su `(A, B)` *non* può servire bene.
7. Su quali tipi di colonna conviene mettere un indice (rispetto a WHERE, JOIN, ORDER BY)?
8. Qual è il **costo** degli indici e perché non si indicizza ogni colonna?
9. Cosa sono **selettività** e **cardinalità**? Perché un indice su una colonna booleana è spesso poco utile?
10. A cosa serve **`EXPLAIN`** / il **query plan**, e cos'è un **covering index**?

<details><summary>Risposte</summary>

1. È una **struttura dati aggiuntiva** mantenuta accanto alla tabella che permette di trovare le righe che soddisfano una condizione **senza scansionare tutta la tabella**; contiene i valori di una colonna in forma ricercabile più un puntatore alla riga. È "aggiuntiva" perché non cambia i dati: puoi crearla o cancellarla a piacere, cambi solo la velocità delle query.
2. Il **full table scan** legge **tutte** le righe una per una e le confronta: costo **O(n)**. L'**index seek** interroga l'indice e salta direttamente alle righe giuste: costo tipico **O(log n)** (con un B-tree). Su tabelle grandi è la differenza tra secondi e millisecondi.
3. Perché il B+tree copre **sia l'uguaglianza sia le range query sia l'ordinamento**, ed è bilanciato (O(log n) garantito). Vantaggi rispetto all'hash index: (1) gestisce le **range query** (`>`, `<`, `BETWEEN`) scorrendo le foglie ordinate e collegate; (2) restituisce i valori **già ordinati** (utile per ORDER BY); l'hash index non può fare nessuna delle due.
4. Un **hash index** usa una tabella hash: applica una funzione hash al valore e la usa come indirizzo del puntatore alla riga. Per l'uguaglianza è **O(1)** in media. Limite: **funziona solo per l'uguaglianza** (`=`), non per range né ordinamenti, perché l'hash non mantiene l'ordine dei valori.
5. L'indice **clusterizzato** determina l'**ordine fisico** delle righe su disco (i dati stanno dentro le foglie dell'indice); quello **non clusterizzato** è una struttura separata con un **puntatore** alla riga che sta altrove. Di clusterizzato ce n'è **uno solo per tabella**, perché i dati possono essere ordinati fisicamente in un solo modo.
6. Un **indice composito** è costruito su **più colonne insieme** (es. `(cognome, nome)`), ordinato prima per la prima colonna e poi per la seconda. La **regola del prefisso più a sinistra** dice che l'indice serve solo le query che filtrano su un **prefisso iniziale e contiguo** delle colonne. Un indice su `(A, B)` **non** può servire bene una query che filtra **solo su `B`**, perché senza fissare `A` i valori di `B` sono sparsi per tutto l'indice.
7. Sulle colonne usate per **cercare, collegare o ordinare**: colonne nei filtri **WHERE**, colonne usate nei **JOIN** (tipicamente le chiavi esterne) e colonne usate in **ORDER BY**/GROUP BY (perché l'indice le fornisce già ordinate).
8. Il costo si paga sulle **scritture** e sullo **spazio**: ogni `INSERT`/`UPDATE`/`DELETE` deve aggiornare tabella **e tutti gli indici** coinvolti (scritture più lente), e ogni indice occupa spazio su disco. Perciò è un compromesso lettura/scrittura e non si indicizza ogni colonna: su colonne mai filtrate o tabelle dominate dalle scritture gli indici fanno più danno che bene.
9. La **cardinalità** è il numero di valori **distinti** in una colonna; la **selettività** è quanto un valore cercato restringe il risultato a poche righe. Un indice su una colonna **booleana** (cardinalità 2) è poco utile perché ogni valore copre comunque metà tabella: poco selettivo, e il database spesso preferisce lo scan.
10. **`EXPLAIN`** mostra il **query plan** (la strategia scelta dall'optimizer: quale indice usare o se fare uno scan, ordine dei join, ordinamenti) **senza eseguire** la query, per verificare se sta davvero usando l'indice. Un **covering index** è un indice che contiene **tutte** le colonne di cui la query ha bisogno (filtro + risultato), così il database risponde leggendo solo l'indice senza accedere alla tabella.
</details>
