---
day: 47
topic_id: os-concurrency
title: "Concorrenza e sincronizzazione: mutex, semafori, monitor"
area: computer-science
course: "Sistemi Operativi"
grounded_in: null
adjacent: [os-deadlock, os-processes, db-conc, xc-ds-consistency]
completeness_checked: true
quiz_count: 10
---

# Concorrenza e sincronizzazione: mutex, semafori, monitor

> **Perché oggi:** in `os-processes` hai visto che un sistema esegue più processi e thread insieme, e in `os-scheduling` che lo scheduler li alterna sulla CPU in un ordine che non controlli. Il guaio nasce quando due di loro toccano **lo stesso dato** nello stesso momento: il risultato dipende da *chi arriva primo*, e cambia a ogni esecuzione. Questi bug, le **race condition**, sono tra i più insidiosi che esistano perché spariscono quando li cerchi. Oggi vediamo perché succede e gli strumenti per impedirlo: mutex, semafori e monitor, fino al classico problema produttore-consumatore.

## La race condition: il problema che vogliamo eliminare
Immagina due thread che incrementano la stessa variabile condivisa `contatore`, che vale `0`. L'operazione `contatore = contatore + 1` sembra atomica ma in realtà la CPU la esegue in tre passi: **leggi** il valore in un registro, **incrementa** il registro, **riscrivi** in memoria. Se lo scheduler intreccia i passi dei due thread:

```
Thread A: legge contatore (0)
Thread B: legge contatore (0)
Thread A: incrementa -> 1, scrive 1
Thread B: incrementa -> 1, scrive 1
```

Il risultato è `1`, non `2`: un incremento è andato perso. Una **race condition (corsa critica)** è esattamente questo: più thread accedono a un dato condiviso e almeno uno lo modifica, e l'esito finale dipende dall'**ordine** di esecuzione, che non è deterministico. Il tratto crudele è la **non riproducibilità**: il bug si manifesta una volta su mille, magari mai in test e sempre in produzione sotto carico.

## Sezione critica e le tre proprietà
La parte di codice che accede alla risorsa condivisa si chiama **sezione critica (critical section)**. La soluzione a ogni problema di concorrenza è garantire che, quando un thread è nella sua sezione critica, nessun altro lo sia sulla stessa risorsa. Una soluzione corretta deve soddisfare tre proprietà:
- **Mutua esclusione (mutual exclusion):** al più un thread per volta nella sezione critica.
- **Progresso (progress):** se nessuno è nella sezione critica e qualcuno vuole entrare, la scelta di chi entra non può essere rimandata all'infinito.
- **Attesa limitata (bounded waiting):** esiste un limite a quante volte altri thread entrano prima che tocchi a chi sta aspettando. Serve a evitare la **starvation** (attesa indefinita) di un thread.

## Il lock mutex
Lo strumento più semplice è il **mutex** (da *mutual exclusion*, mutua esclusione): un **lucchetto** con due operazioni, `lock()` (acquisisci) e `unlock()` (rilascia). Un thread che vuole entrare nella sezione critica fa `lock()`: se il mutex è libero lo prende e prosegue; se è già preso da un altro, si **blocca** finché non viene rilasciato. All'uscita fa `unlock()`.

```
lock(m)
  # ... sezione critica: tocca il dato condiviso ...
unlock(m)
```

Sul contatore di prima, racchiudere l'incremento tra `lock(m)` e `unlock(m)` elimina la race: il secondo thread deve aspettare che il primo abbia finito tutti e tre i passi. Dettaglio importante: `lock` e `unlock` devono essere **atomiche**, altrimenti sposteremmo solo la race dentro al lock stesso; per questo si appoggiano a istruzioni hardware apposite (per esempio **test-and-set** o **compare-and-swap**, che leggono e scrivono una cella in un colpo solo indivisibile). Un mutex è concettualmente un lock **binario** (preso/libero) con una nozione di proprietà: tipicamente solo chi ha fatto `lock` può fare `unlock`.

## Il semaforo
Il **semaforo**, introdotto da Dijkstra, generalizza il mutex. È un contatore intero `S` con due operazioni atomiche:
- **`wait(S)`** (storicamente `P`): decrementa `S`; se `S` diventa negativo, il thread si **blocca** in attesa.
- **`signal(S)`** (storicamente `V`): incrementa `S`; se c'era qualcuno in attesa, ne sveglia uno.

Il valore iniziale di `S` dice **quante risorse** sono disponibili. Due usi:
- **Semaforo binario** (`S` inizializzato a `1`): si comporta come un mutex, garantisce mutua esclusione.
- **Semaforo contatore** (`S` inizializzato a `N`): permette fino a `N` accessi contemporanei. Utile quando hai `N` risorse identiche (es. `N` connessioni in un pool): i primi `N` thread passano, il successivo aspetta che uno liberi.

Il semaforo è potente perché serve anche a **sincronizzare un ordine** tra thread, non solo a proteggere un dato: inizializzandolo a `0`, un thread che fa `wait` resta bloccato finché un altro non fa `signal`, realizzando un vincolo "B non parte prima che A abbia finito".

## Il monitor
Semafori e mutex sono potenti ma **fragili**: basta dimenticare un `unlock`, invertire due `wait`, o sbagliare il valore iniziale, e ottieni deadlock o corruzione, in un punto qualsiasi del codice. Il **monitor** è un costrutto di più alto livello (offerto dal linguaggio, non dal programmatore a mano) che incapsula i dati condivisi insieme alle procedure che li toccano, e **garantisce automaticamente** che una sola chiamata alla volta sia attiva nel monitor. La mutua esclusione è implicita: non c'è nessun lock da ricordarsi.

Per far aspettare un thread dentro un monitor finché una condizione non è vera si usano le **variabili di condizione**, con due operazioni: `wait()` (il thread si sospende e **rilascia** il monitor, così altri possono entrare) e `signal()` (sveglia un thread sospeso su quella condizione). La differenza cruciale con il `signal` del semaforo: il `signal` del monitor su una condizione **senza nessuno in attesa non ha effetto** e si perde, mentre quello del semaforo incrementa comunque il contatore e "si ricorda". In pratica i monitor stanno dietro al `synchronized` di Java e al `lock` di C#.

## Il problema produttore-consumatore
È il banco di prova classico della sincronizzazione: un **produttore** genera elementi e li mette in un **buffer limitato** di `N` posti; un **consumatore** li preleva e li usa. Due vincoli: il produttore non deve scrivere se il buffer è **pieno**, il consumatore non deve leggere se è **vuoto**, e i due non devono toccare il buffer insieme. Soluzione con tre semafori:

```
semaphore vuoti = N     # posti liberi nel buffer
semaphore pieni = 0     # posti occupati
semaphore mutex = 1     # mutua esclusione sul buffer

Produttore:
  loop:
    item = produci()
    wait(vuoti)         # se non ci sono posti liberi, aspetta
    wait(mutex)         # prendi l'accesso esclusivo al buffer
      buffer.inserisci(item)
    signal(mutex)
    signal(pieni)       # c'è un elemento in più da consumare

Consumatore:
  loop:
    wait(pieni)         # se non c'è niente, aspetta
    wait(mutex)
      item = buffer.preleva()
    signal(mutex)
    signal(vuoti)       # c'è un posto in più libero
    consuma(item)
```

`vuoti` e `pieni` contano i posti e realizzano l'attesa quando il buffer è pieno o vuoto; `mutex` protegge l'inserimento e il prelievo. **L'ordine dei due `wait` è obbligatorio**: prima quello sul semaforo contatore (`vuoti` o `pieni`), poi quello sul `mutex`. Se li invertissi, un produttore potrebbe prendere il `mutex` e poi bloccarsi su `wait(vuoti)` perché il buffer è pieno, restando fermo **con il mutex in mano**; a quel punto il consumatore, per liberare un posto, ha bisogno del mutex che non otterrà mai: un **deadlock** (stallo). I `signal` invece possono stare in qualunque ordine.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 620 230" style="max-width:100%;height:auto;font-family:inherit">
<rect x="0" y="0" width="620" height="230" fill="var(--card2)" rx="8"/>
<g font-size="12" fill="var(--ink)">
<text x="20" y="26" font-weight="700">Produttore-consumatore con buffer limitato</text>
<rect x="30" y="70" width="90" height="46" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="75" y="92" text-anchor="middle" font-size="11">Produttore</text><text x="75" y="107" text-anchor="middle" font-size="9" fill="var(--muted)">produci</text>
<rect x="500" y="70" width="90" height="46" rx="8" fill="var(--card)" stroke="var(--good)" stroke-width="1.6"/><text x="545" y="92" text-anchor="middle" font-size="11">Consumatore</text><text x="545" y="107" text-anchor="middle" font-size="9" fill="var(--muted)">consuma</text>
<text x="240" y="60" text-anchor="middle" font-size="10" fill="var(--muted)">buffer (N posti)</text>
<rect x="220" y="68" width="40" height="40" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="240" y="93" text-anchor="middle" font-size="11">x</text>
<rect x="265" y="68" width="40" height="40" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="285" y="93" text-anchor="middle" font-size="11">x</text>
<rect x="310" y="68" width="40" height="40" rx="5" fill="var(--card)" stroke="var(--rule)"/>
<rect x="355" y="68" width="40" height="40" rx="5" fill="var(--card)" stroke="var(--rule)"/>
<path d="M122,93 L216,88" stroke="var(--accent)" stroke-width="1.5" fill="none" marker-end="url(#arConc47)"/>
<path d="M397,88 L498,93" stroke="var(--good)" stroke-width="1.5" fill="none" marker-end="url(#arConc47)"/>
<text x="168" y="83" font-size="9" fill="var(--muted)">inserisci</text>
<text x="430" y="83" font-size="9" fill="var(--muted)">preleva</text>
<text x="20" y="160" font-size="10.5" fill="var(--ink)">vuoti = posti liberi (iniz. N) ; pieni = posti occupati (iniz. 0) ; mutex = 1</text>
<text x="20" y="182" font-size="10.5" fill="var(--muted)">Produttore: wait(vuoti) -> wait(mutex) -> inserisci -> signal(mutex) -> signal(pieni)</text>
<text x="20" y="202" font-size="10.5" fill="var(--muted)">Consumatore: wait(pieni) -> wait(mutex) -> preleva -> signal(mutex) -> signal(vuoti)</text>
<text x="20" y="222" font-size="9.5" fill="var(--accent)">Ordine dei wait obbligatorio: contatore prima del mutex, o si rischia deadlock.</text>
</g>
<defs><marker id="arConc47" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--muted)"/></marker></defs>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Il produttore riempie il buffer, il consumatore lo svuota. I semafori vuoti e pieni contano i posti e bloccano chi arriva quando il buffer è pieno o vuoto; mutex protegge l'accesso. Invertire i due wait porterebbe allo stallo.</figcaption>
</figure>

## Deadlock: cenni
Quando per proteggere più risorse si usano più lock, nasce il rischio di **deadlock (stallo):** due o più thread restano bloccati per sempre perché ciascuno aspetta un lock che un altro tiene. Il caso minimo: il thread A prende il lock `L1` e aspetta `L2`, mentre B ha `L2` e aspetta `L1`. Nessuno molla, nessuno procede. Il rimedio più semplice e usato è imporre un **ordine globale di acquisizione** dei lock (tutti prendono sempre prima `L1` poi `L2`), che spezza la possibilità dello stallo. Le condizioni formali del deadlock e le strategie di prevenzione, evitamento e rilevamento sono il tema di `os-deadlock`.

## Esempi concreti
- **Un contatore di visite su un sito:** più richieste arrivano insieme e ognuna fa `visite++`. Senza un lock (o un'operazione atomica apposita) perdi conteggi esattamente come nell'esempio iniziale. In pratica si usa un lock, un contatore atomico, oppure si delega al database con un `UPDATE ... SET visite = visite + 1`, che garantisce l'atomicità lato DB.
- **Pool di connessioni al database:** l'applicazione tiene `N` connessioni riutilizzabili. Un **semaforo contatore** inizializzato a `N` modella perfettamente la cosa: ogni richiesta fa `wait` per ottenere una connessione, `signal` quando la restituisce; la `N+1`-esima richiesta aspetta che una si liberi, invece di aprirne una nuova e sovraccaricare il database.

## Notable use case
- **Java** offre la concorrenza a più livelli: la parola chiave **`synchronized`** è un monitor incorporato nel linguaggio (ogni oggetto ha un lock implicito), mentre il package `java.util.concurrent` fornisce `ReentrantLock` (mutex esplicito), `Semaphore` (semaforo contatore) e strutture dati già thread-safe come `ConcurrentHashMap`.
- **Il Global Interpreter Lock (GIL) di CPython** è un unico mutex globale che permette a **un solo thread per volta** di eseguire bytecode Python. Semplifica l'interprete e rende atomiche molte operazioni, ma impedisce ai thread Python di sfruttare più core per codice CPU-bound: un esempio celebre di come una scelta di sincronizzazione modelli le prestazioni di un intero linguaggio.

## Fonti
- **Silberschatz, Galvin, Gagne** — *Operating System Concepts* (capitoli "Synchronization Tools" e "Synchronization Examples", con produttore-consumatore)
- **Tanenbaum** — *Modern Operating Systems* (sezione su IPC, semafori e monitor)
- **Arpaci-Dusseau** — *Operating Systems: Three Easy Pieces*, ostep.org (capitoli su locks, condition variables e semafori)

## Concetti adiacenti
- `os-deadlock` — le condizioni dello stallo e come prevenirlo, evitarlo o rilevarlo: il naturale seguito dei lock multipli
- `os-processes` — processi e thread, ciò che condivide memoria e quindi va sincronizzato
- `db-conc` — gli stessi problemi a livello di database: lock, transazioni e livelli di isolamento
- `xc-ds-consistency` — quando i dati sono distribuiti su più nodi, consistenza e consenso generalizzano la sincronizzazione

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cos'è una **race condition** e perché l'incremento `contatore = contatore + 1` non è atomico?
2. Cos'è una **sezione critica** e quali sono le tre proprietà che una soluzione corretta deve garantire?
3. Come funzionano `lock()` e `unlock()` di un **mutex**, e perché devono essere operazioni atomiche?
4. Definisci `wait(S)` e `signal(S)` di un **semaforo**. Cosa rappresenta il valore iniziale di `S`?
5. Che differenza c'è tra **semaforo binario** e **semaforo contatore**, e a cosa serve ciascuno?
6. Cos'è un **monitor** e qual è il suo vantaggio rispetto all'uso manuale dei semafori?
7. Qual è la differenza tra il `signal` di una **variabile di condizione** di un monitor e il `signal` di un semaforo quando non c'è nessuno in attesa?
8. Nel produttore-consumatore, a cosa servono i semafori `vuoti`, `pieni` e `mutex`?
9. Perché nel produttore-consumatore `wait(vuoti)` deve venire **prima** di `wait(mutex)`? Cosa succederebbe invertendoli?
10. Descrivi il caso minimo di **deadlock** con due lock e il rimedio basato sull'ordine di acquisizione.

<details><summary>Risposte</summary>

1. È quando più thread accedono a un dato condiviso e almeno uno lo modifica, e il risultato dipende dall'**ordine** di esecuzione. L'incremento non è atomico perché la CPU lo esegue in tre passi (leggi, incrementa, riscrivi): se due thread si intrecciano, leggono lo stesso valore e un incremento va perso.
2. La **sezione critica** è la parte di codice che accede alla risorsa condivisa. Le tre proprietà: **mutua esclusione** (uno alla volta), **progresso** (chi può entrare non è rimandato all'infinito), **attesa limitata** (c'è un tetto a quante volte altri entrano prima di chi aspetta).
3. `lock()` prende il lucchetto se libero, altrimenti blocca il thread finché non si libera; `unlock()` lo rilascia. Devono essere atomiche altrimenti la race si sposterebbe dentro al lock stesso; si appoggiano a istruzioni hardware come test-and-set o compare-and-swap.
4. `wait(S)` decrementa `S` e blocca il thread se `S` diventa negativo; `signal(S)` incrementa `S` e sveglia un eventuale thread in attesa. Il valore iniziale di `S` indica **quante risorse** sono disponibili.
5. **Binario** (iniz. `1`): fa da mutex, garantisce mutua esclusione. **Contatore** (iniz. `N`): consente fino a `N` accessi simultanei, utile con `N` risorse identiche come un pool di connessioni.
6. È un costrutto di alto livello (fornito dal linguaggio) che incapsula dati condivisi e le procedure che li toccano, garantendo **automaticamente** una sola chiamata attiva alla volta. Vantaggio: la mutua esclusione è implicita, non ci sono lock da ricordarsi di rilasciare, quindi molti meno errori.
7. Il `signal` su una **variabile di condizione** senza nessuno in attesa **non ha effetto** e si perde; il `signal` di un **semaforo** incrementa comunque il contatore, quindi "si ricorda" e sbloccherà un `wait` futuro.
8. `vuoti` conta i posti liberi (blocca il produttore se il buffer è pieno), `pieni` conta i posti occupati (blocca il consumatore se è vuoto), `mutex` garantisce accesso esclusivo durante inserimento e prelievo.
9. Perché invertendoli un produttore potrebbe prendere il `mutex` e poi bloccarsi su `wait(vuoti)` con il buffer pieno, restando fermo **con il mutex in mano**; il consumatore, per liberare un posto, avrebbe bisogno di quel mutex che non otterrà mai: deadlock.
10. A prende `L1` e aspetta `L2`; B prende `L2` e aspetta `L1`: entrambi bloccati per sempre. Rimedio: imporre un **ordine globale** di acquisizione (tutti prendono sempre prima `L1`, poi `L2`), che rende impossibile l'attesa circolare.
</details>

## Esercizi
1. **Trova e correggi la race condition.** Due thread eseguono 1000 volte ciascuno `saldo = saldo + 1` su una variabile condivisa `saldo` inizialmente `0`. Qual è il valore finale atteso, quale può uscire in pratica e perché? Riscrivi la sezione critica con un mutex.
2. **Semaforo come sincronizzatore d'ordine.** Hai due thread: `T1` deve stampare "A" e `T2` deve stampare "B", ma vuoi garantire che "A" sia stampato **sempre prima** di "B". Usando **un solo** semaforo, scrivi lo pseudocodice dei due thread.
3. **Produttore-consumatore.** Scrivi lo pseudocodice completo di produttore e consumatore con un buffer limitato di `N` posti, usando i tre semafori. Indica i valori iniziali e spiega in una riga perché l'ordine dei `wait` è quello.

<details><summary>Soluzioni</summary>

1. Valore atteso: `2000`. In pratica può uscire **un numero minore di 2000** perché `saldo = saldo + 1` non è atomico: con l'intreccio dei passi leggi/incrementa/riscrivi, incrementi si perdono (lost update). In teoria si può scendere parecchio sotto i 2000 (il minimo assoluto è addirittura 2), anche se in pratica di solito il risultato resta poco sotto il valore atteso. Correzione:
   ```
   lock(m)
     saldo = saldo + 1
   unlock(m)
   ```
   Ogni thread, prima di toccare `saldo`, acquisisce il mutex; così i tre passi di un incremento non possono intrecciarsi con quelli dell'altro thread, e il risultato è sempre `2000`.

2. Si usa un semaforo `s` inizializzato a `0`:
   ```
   semaphore s = 0

   T1:              T2:
     stampa("A")      wait(s)      # resta bloccato finché T1 non fa signal
     signal(s)        stampa("B")
   ```
   Qualunque sia l'ordine in cui lo scheduler li avvia, `T2` non può stampare "B" prima che `T1` abbia fatto `signal(s)`, cioè prima di aver stampato "A". Il semaforo inizializzato a `0` realizza il vincolo di precedenza.

3. (è la soluzione vista nel corpo)
   ```
   semaphore vuoti = N     # posti liberi
   semaphore pieni = 0     # posti occupati
   semaphore mutex = 1     # accesso esclusivo al buffer

   Produttore:                 Consumatore:
     loop:                       loop:
       item = produci()            wait(pieni)
       wait(vuoti)                 wait(mutex)
       wait(mutex)                   item = buffer.preleva()
         buffer.inserisci(item)    signal(mutex)
       signal(mutex)               signal(vuoti)
       signal(pieni)               consuma(item)
   ```
   L'ordine `wait(contatore)` poi `wait(mutex)` evita che un thread si blocchi sul semaforo contatore **mentre tiene il mutex**: così non si crea l'attesa circolare che porterebbe allo stallo.
</details>
