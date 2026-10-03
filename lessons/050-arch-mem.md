---
day: 50
topic_id: arch-mem
title: "Gerarchia di memoria, cache e località"
area: computer-science
course: "Architetture dei Calcolatori"
grounded_in: null
adjacent: [os-memory, arch-isa, arch-pipeline]
completeness_checked: true
quiz_count: 10
---

# Gerarchia di memoria, cache e località

> **Perché oggi:** la CPU, nel suo ciclo fetch-decode-execute (il tema di `arch-isa`), preleva a ogni passo dati e istruzioni dalla memoria. Ma c'è un divario imbarazzante: una CPU moderna fa un'operazione in meno di un nanosecondo, mentre leggere dalla RAM ne richiede un centinaio. Se la CPU aspettasse la RAM a ogni accesso, i tuoi miliardi di transistor resterebbero fermi per il 99% del tempo. La soluzione è la **gerarchia di memoria**: tanti livelli di memoria, dai piccoli e velocissimi ai grandi e lenti. Funziona grazie a un fenomeno quasi magico dei programmi, la **località**. Oggi vediamo come, con i conti dell'hit rate e del tempo medio di accesso.

## Il divario e l'idea della gerarchia
Esiste un compromesso fisico inaggirabile: una memoria **veloce** è **piccola e costosa**, una memoria **capiente** è **lenta e a buon mercato**. Non puoi avere tutto. La **gerarchia di memoria** aggira il problema impilando più livelli e sfruttando il fatto che un programma, in un dato momento, usa solo una piccola fetta dei suoi dati. Dall'alto (veloce, piccolo) verso il basso (lento, grande):
- **Registri:** dentro la CPU, accesso immediato, una manciata di parole.
- **Cache (L1, L2, L3):** memoria statica velocissima vicino ai core; da decine di KB (L1) a decine di MB (L3).
- **RAM (memoria principale):** memoria dinamica, da GB, latenza di ~100 ns.
- **Disco (SSD/HDD) e memoria virtuale:** enorme e lentissimo, latenza da microsecondi (SSD) a millisecondi (HDD).

Ogni livello fa da **cache** (deposito veloce) per quello sotto: tiene una copia dei dati usati più di recente, così la CPU li trova vicino senza scendere ai livelli lenti.

## La località: perché la gerarchia funziona
La gerarchia sarebbe inutile se i programmi accedessero alla memoria a caso. Per fortuna non lo fanno, obbediscono al **principio di località**, in due forme:
- **Località temporale:** se accedi a un dato, è molto probabile che lo riuserai **presto**. Pensa alla variabile contatore di un ciclo: la tocchi a ogni iterazione.
- **Località spaziale:** se accedi a un dato, è molto probabile che userai presto quelli **vicini** in memoria. Pensa a scorrere un array: dopo `a[0]` quasi sicuramente leggi `a[1]`, `a[2]`.

La cache sfrutta entrambe: quando porta su un dato, porta tutto il **blocco** (o linea) che lo contiene, cioè un gruppo di byte contigui (tipicamente 64), scommettendo sulla località spaziale; e tiene i blocchi usati di recente, scommettendo sulla località temporale.

## Hit, miss e come si misura la cache
Quando la CPU chiede un dato:
- **Cache hit:** il dato è già in cache, si legge velocissimo.
- **Cache miss:** il dato non c'è, bisogna scendere al livello sotto (più lento) a prenderlo, pagando la **miss penalty** (penalità di miss), e portarne su il blocco.

Le metriche fondamentali:
- **Hit rate (tasso di successo):** frazione di accessi che sono hit. Se su `1000` accessi `950` sono hit, l'hit rate è `950 / 1000 = 0.95`, cioè il **95%**.
- **Miss rate:** `1 − hit rate`. Nell'esempio, `0.05` cioè il **5%**.
- **Tempo medio di accesso alla memoria (AMAT, Average Memory Access Time):** la formula chiave.

```
AMAT = tempo di hit + (miss rate × miss penalty)
```

Esempio: tempo di hit `= 1` ciclo, miss rate `= 5%`, miss penalty `= 100` cicli. Allora `AMAT = 1 + 0.05 × 100 = 6` cicli. Nota quanto pesano le miss: con solo il 5% di miss, l'accesso medio è **sei volte** il tempo di un hit. Ridurre il miss rate è il lavoro di tutta la progettazione della cache.

Con più livelli la formula si annida. Con L1 e L2: `AMAT = hit L1 + miss rate L1 × (hit L2 + miss rate L2 × penalità memoria)`. Esempio: `hit L1 = 1`, `miss rate L1 = 10%`, `hit L2 = 10`, `miss rate L2 = 20%`, penalità memoria `= 100`. Allora `AMAT = 1 + 0.10 × (10 + 0.20 × 100) = 1 + 0.10 × 30 = 4` cicli. Il secondo livello assorbe gran parte delle miss del primo, abbassando il tempo medio.

## Dove va un blocco: le politiche di mapping
Quando un blocco di memoria viene portato in cache, in quale cella (slot) finisce? L'indirizzo richiesto viene spezzato in tre campi: **tag**, **indice** e **offset**. L'**offset** individua il byte dentro il blocco, l'**indice** individua lo slot della cache, il **tag** è la parte alta dell'indirizzo che si salva accanto al dato per **verificare** che lo slot contenga davvero il blocco cercato (e non un altro che mappa sullo stesso slot). Tre schemi:
- **Diretta (direct-mapped):** ogni blocco di memoria può andare in **un solo** slot, determinato da `indice = numero del blocco mod numero di slot`. Semplicissima e veloce da controllare (guardi un solo slot), ma soffre di **conflitti**: due blocchi che mappano sullo stesso slot si cacciano a vicenda anche se la cache è mezza vuota.
- **Completamente associativa (fully associative):** un blocco può andare in **qualunque** slot. Nessun conflitto strutturale, ma per cercarlo devi confrontare il tag con **tutti** gli slot: costoso in hardware.
- **Associativa a insiemi (set-associative):** il compromesso usato davvero. La cache è divisa in **insiemi** (set) da `k` slot ciascuno ("cache a `k` vie"); l'indice sceglie l'insieme, e dentro l'insieme il blocco può andare in una qualsiasi delle `k` vie. Riduce i conflitti della diretta senza il costo della fully associative.

**Esempio di scomposizione dell'indirizzo** (cache diretta): indirizzi da `32` bit, cache da `16 KB`, blocco da `32 byte`.
- Offset: il blocco ha `32 = 2^5` byte, quindi `5` bit di offset.
- Indice: la cache ha `16 KB / 32 B = 512 = 2^9` slot, quindi `9` bit di indice.
- Tag: i bit restanti, `32 − 9 − 5 = 18` bit.

Quando due blocchi con lo stesso indice ma tag diverso si contendono lo stesso slot in una cache associativa, serve una **politica di rimpiazzo** per decidere chi sfrattare: la più usata è **LRU (Least Recently Used)**, che butta fuori il blocco non usato da più tempo (scommettendo, di nuovo, sulla località temporale).

## Scrivere in cache: write-through e write-back
Le letture sono metà del problema; le scritture pongono la domanda di **coerenza**: se la CPU scrive un dato che è in cache, quando aggiorno la copia in RAM? Due politiche:
- **Write-through (scrittura passante):** ogni scrittura va **sia** in cache **sia** subito in memoria. La RAM è sempre aggiornata e coerente, ma ogni scrittura paga la lentezza della memoria. Si abbina spesso a un **write buffer** (buffer di scrittura) che accoda le scritture così la CPU non aspetta.
- **Write-back (scrittura differita):** la scrittura va **solo** in cache; il blocco viene marcato come **dirty (sporco)**. La RAM viene aggiornata **solo** quando quel blocco viene sfrattato. Molto più veloce se scrivi ripetutamente sugli stessi dati (sfrutta la località temporale), ma la RAM è temporaneamente **incoerente** con la cache, il che complica la vita nei sistemi multiprocessore (serve un protocollo di coerenza tra le cache dei vari core).

In sintesi: write-through è semplice e coerente ma lenta in scrittura; write-back è veloce ma richiede di gestire i blocchi sporchi e la coerenza.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 560 300" style="max-width:100%;height:auto;font-family:inherit">
<rect x="0" y="0" width="560" height="300" fill="var(--card2)" rx="8"/>
<g font-size="12" fill="var(--ink)">
<text x="20" y="26" font-weight="700">La gerarchia di memoria</text>
<rect x="230" y="44" width="100" height="30" rx="4" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="280" y="64" text-anchor="middle" font-size="11">Registri</text>
<rect x="200" y="82" width="160" height="30" rx="4" fill="var(--card)" stroke="var(--rule)"/><text x="280" y="102" text-anchor="middle" font-size="11">Cache L1 / L2 / L3</text>
<rect x="160" y="120" width="240" height="32" rx="4" fill="var(--card)" stroke="var(--rule)"/><text x="280" y="141" text-anchor="middle" font-size="11">RAM (memoria principale)</text>
<rect x="110" y="160" width="340" height="34" rx="4" fill="var(--card)" stroke="var(--rule)"/><text x="280" y="182" text-anchor="middle" font-size="11">Disco (SSD / HDD) e memoria virtuale</text>
<text x="470" y="64" font-size="9" fill="var(--muted)">più veloce</text>
<text x="470" y="80" font-size="9" fill="var(--muted)">più piccola</text>
<text x="470" y="178" font-size="9" fill="var(--muted)">più lenta</text>
<text x="470" y="194" font-size="9" fill="var(--muted)">più grande</text>
<path d="M80,52 L80,186" stroke="var(--muted)" stroke-width="1.2" marker-end="url(#arMem50)"/>
<text x="40" y="120" font-size="9" fill="var(--muted)" transform="rotate(-90 40 120)">latenza crescente</text>
<text x="20" y="226" font-size="10.5" fill="var(--ink)">AMAT = tempo di hit + (miss rate x miss penalty)</text>
<text x="20" y="248" font-size="10" fill="var(--muted)">Es: 1 + 0.05 x 100 = 6 cicli. Ogni livello fa da cache per quello sotto.</text>
<text x="20" y="276" font-size="10" fill="var(--good)">La località temporale e spaziale è ciò che rende alto l'hit rate.</text>
</g>
<defs><marker id="arMem50" markerWidth="8" markerHeight="8" refX="4" refY="7" orient="auto"><path d="M1,1 L7,1 L4,7 Z" fill="var(--muted)"/></marker></defs>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">La gerarchia: salendo si guadagna velocità e si perde capacità. Ogni livello tiene una copia dei dati più usati del livello sotto; la località fa sì che la CPU trovi quasi sempre ciò che cerca nei livelli alti, tenendo basso l'AMAT.</figcaption>
</figure>

## Memoria virtuale: cenni
La gerarchia non si ferma alla RAM. La **memoria virtuale** estende lo stesso principio verso il disco: dà a ogni processo l'illusione di avere a disposizione uno spazio di indirizzi grande e contiguo tutto suo, anche più grande della RAM fisica. Lo spazio virtuale è diviso in **pagine** di dimensione fissa, mappate su **frame** della RAM tramite una **tabella delle pagine**; le pagine non attive risiedono su disco e vengono caricate su richiesta (un **page fault** quando una pagina serve ma non è in RAM, l'equivalente "lento" di una cache miss). La RAM, in questo quadro, è la cache del disco. Il meccanismo completo del paging è il tema di `os-memory`.

## Esempi concreti
- **Scorrere una matrice per righe o per colonne:** in un linguaggio che memorizza le matrici per righe (row-major, come il C), scorrere `matrice[i][j]` variando prima `j` segue l'ordine fisico in memoria: ogni blocco di cache portato su viene usato per intero (ottima località spaziale, pochi miss). Scorrerla variando prima `i` salta da un blocco all'altro a ogni accesso: hit rate basso, programma molto più lento pur facendo gli stessi calcoli. È un esempio da manuale di come la località, non l'algoritmo, decida la velocità.
- **Il buffer pool di un database:** un database come PostgreSQL tiene in RAM un **buffer pool**, una cache delle pagine del disco usate di recente, gestita con una politica vicina a LRU. È esattamente la gerarchia di memoria applicata un livello più in basso: la RAM fa da cache veloce per il disco lento, sfruttando la località degli accessi alle stesse pagine.

## Notable use case
- **I processori moderni** hanno tipicamente tre livelli di cache: **L1** separata per istruzioni e dati (split cache), piccolissima (decine di KB) e per core; **L2** per core (centinaia di KB); **L3** condivisa tra tutti i core (decine di MB). Più ci si allontana dal core, più grande e lenta è la cache, replicando la gerarchia in miniatura dentro il chip.
- **Le CPU usano la cache set-associative** (tipicamente da 4 a 16 vie per L1/L2): è il punto di equilibrio tra il basso costo della diretta e l'assenza di conflitti della fully associative, scelto perché in pratica riduce drasticamente i miss da conflitto con un hardware di confronto ancora gestibile.

## Fonti
- **Hennessy, Patterson** — *Computer Architecture: A Quantitative Approach* (e la versione didattica *Computer Organization and Design*): il riferimento su cache, AMAT e gerarchia
- **Bryant, O'Hallaron** — *Computer Systems: A Programmer's Perspective* (ottimo sul legame tra località del codice e prestazioni della cache)
- **Silberschatz** — *Operating System Concepts* (per il collegamento con la memoria virtuale e il paging)

## Concetti adiacenti
- `os-memory` — memoria virtuale e paging: la gerarchia estesa verso il disco, gestita dal sistema operativo
- `arch-isa` — la CPU e il ciclo fetch-decode-execute che a ogni passo chiede dati alla memoria
- `arch-pipeline` — la pipeline che rende la CPU veloce ha ancora più fame di dati pronti: le cache miss sono tra le sue nemiche principali

## Quiz (10 — tutte rispondibili dalla lezione)
1. Qual è il compromesso fisico che rende necessaria la **gerarchia di memoria**?
2. Definisci **località temporale** e **località spaziale** con un esempio ciascuna.
3. Perché la cache, in un miss, porta su un intero **blocco** e non solo il byte richiesto?
4. Differenza tra **cache hit** e **cache miss**, e cos'è la **miss penalty**?
5. Scrivi la formula dell'**AMAT** e calcolalo con tempo di hit `1`, miss rate `5%`, miss penalty `100`.
6. In quali tre campi viene scomposto un indirizzo per l'accesso alla cache, e a cosa serve ciascuno?
7. Confronta mapping **diretto**, **fully associative** e **set-associative**: vantaggi e svantaggi.
8. Cosa fa la politica di rimpiazzo **LRU** e su quale principio di località si basa?
9. Differenza tra **write-through** e **write-back**, con pro e contro di ciascuna. Cosa significa che un blocco è **dirty**?
10. In cosa la **memoria virtuale** è analoga alla cache, e cos'è un **page fault**?

<details><summary>Risposte</summary>

1. Una memoria veloce è piccola e costosa, una capiente è lenta ed economica: non si può avere grande, veloce ed economica insieme. La gerarchia aggira il compromesso impilando livelli e sfruttando la località.
2. **Temporale:** un dato appena usato sarà probabilmente riusato presto (es. la variabile contatore di un ciclo). **Spaziale:** usato un dato, si useranno presto quelli vicini in memoria (es. scorrere un array `a[0]`, `a[1]`, `a[2]`).
3. Per sfruttare la **località spaziale**: avendo appena acceduto a un dato, è probabile che si useranno presto quelli contigui, quindi conviene portarli su tutti insieme nel blocco.
4. **Hit:** il dato è già in cache, lettura velocissima. **Miss:** il dato non c'è, va preso dal livello sotto, più lento. La **miss penalty** è il tempo extra pagato per andare a recuperare il blocco dal livello inferiore.
5. `AMAT = tempo di hit + miss rate × miss penalty = 1 + 0.05 × 100 = 6` cicli.
6. **Offset** (individua il byte dentro il blocco), **indice** (individua lo slot/insieme della cache), **tag** (parte alta dell'indirizzo, salvata accanto al dato per verificare che lo slot contenga davvero il blocco cercato).
7. **Diretta:** un blocco va in un solo slot; controllo velocissimo ma molti conflitti. **Fully associative:** un blocco va ovunque; nessun conflitto strutturale ma ricerca costosa (confronta tutti i tag). **Set-associative:** compromesso, la cache è divisa in insiemi da `k` vie, l'indice sceglie l'insieme e dentro va in una via libera; pochi conflitti con hardware gestibile.
8. **LRU** sfratta il blocco **non usato da più tempo**; si basa sulla **località temporale** (ciò che non si usa da tanto probabilmente non servirà a breve).
9. **Write-through:** scrive sia in cache sia subito in memoria; RAM sempre coerente ma scritture lente. **Write-back:** scrive solo in cache, marca il blocco **dirty** (sporco, cioè modificato e non ancora riversato in RAM), e aggiorna la RAM solo allo sfratto del blocco; veloce ma la RAM è temporaneamente incoerente.
10. La **RAM fa da cache del disco**: le pagine attive stanno in RAM, le altre su disco, come i blocchi caldi stanno in cache. Un **page fault** è la richiesta di una pagina non presente in RAM, che va caricata da disco: l'equivalente lento di una cache miss.
</details>

## Esercizi
1. **Calcolo di hit rate e AMAT.** Un programma fa `2000` accessi in memoria, di cui `1900` sono hit in cache. Il tempo di hit è `2 ns` e la miss penalty è `80 ns`. Calcola hit rate, miss rate e AMAT.
2. **Scomposizione dell'indirizzo.** Una cache **diretta** da `8 KB` con blocchi da `64 byte` opera su indirizzi da `32 bit`. Calcola quanti bit occupano offset, indice e tag, e quanti slot ha la cache.
3. **Scelta della politica di scrittura.** Un carico di lavoro incrementa ripetutamente gli stessi pochi contatori in memoria, migliaia di volte ciascuno. Quale politica di scrittura (write-through o write-back) conviene e perché? Quale svantaggio introduce in un sistema multi-core?

<details><summary>Soluzioni</summary>

1. Hit rate `= 1900 / 2000 = 0.95` (95%); miss rate `= 1 − 0.95 = 0.05` (5%). `AMAT = 2 + 0.05 × 80 = 2 + 4 = 6 ns`.

2. Offset: blocco `64 = 2^6` byte, quindi `6` bit. Numero di slot: `8 KB / 64 B = 8192 / 64 = 128 = 2^7`, quindi indice `7` bit. Tag: `32 − 7 − 6 = 19` bit. La cache ha `128` slot.

3. Conviene **write-back**: scrivendo migliaia di volte sugli stessi contatori, con write-through ogni incremento pagherebbe la lentezza della RAM, mentre con write-back le scritture restano in cache (il blocco resta dirty) e la RAM viene aggiornata una sola volta, allo sfratto. Sfrutta a pieno la località temporale. Svantaggio multi-core: la RAM è temporaneamente incoerente con la cache, e se un altro core legge quegli indirizzi serve un **protocollo di coerenza** tra le cache per non leggere un valore vecchio.
</details>
