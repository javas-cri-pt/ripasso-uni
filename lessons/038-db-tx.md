---
day: 38
topic_id: db-tx
title: "Transazioni e ACID"
area: computer-science
course: "Basi di Dati / Sistemi Informativi"
grounded_in: null
adjacent: [db-sql, db-conc, xc-distsys]
completeness_checked: true
quiz_count: 10
---

# Transazioni e ACID

> **Perché oggi:** al giorno in cui hai studiato `db-sql` hai imparato a scrivere `INSERT`, `UPDATE` e `DELETE`. Ma un singolo bonifico bancario è *due* `UPDATE` (togli 100 da un conto, aggiungi 100 all'altro): se il sistema va in crash **in mezzo**, i soldi spariscono. La transazione è il meccanismo che impedisce questo disastro, raggruppando più operazioni in un'unica unità che o riesce **tutta** o non lascia **alcuna** traccia. Le quattro garanzie che il database offre su questa unità si riassumono nell'acronimo **ACID**: è la domanda da colloquio più classica sui database ("spiegami ACID"), e oggi la smontiamo proprietà per proprietà, vedendo *come* il DBMS la fa rispettare.

## Cos'è una transazione

Una **transazione** è una sequenza di operazioni sul database (letture e scritture) che il sistema tratta come **una sola unità logica di lavoro**: un blocco indivisibile. Il **DBMS** (*Database Management System*, il software che gestisce il database, es. PostgreSQL, MySQL, Oracle) garantisce che l'intera sequenza venga eseguita come se fosse un'unica operazione atomica.

L'esempio canonico è il **bonifico**: trasferire 100 euro dal conto A al conto B significa eseguire

```sql
UPDATE conti SET saldo = saldo - 100 WHERE id = 'A';
UPDATE conti SET saldo = saldo + 100 WHERE id = 'B';
```

Queste due istruzioni **non** devono mai essere viste separatamente dal resto del mondo: o avvengono entrambe, o nessuna delle due. Se dopo il primo `UPDATE` il server si spegne, il conto A avrebbe 100 euro in meno senza che B li abbia ricevuti: denaro distrutto. La transazione serve esattamente a rendere impossibile questo stato intermedio.

In SQL una transazione si delimita con tre comandi:

- **`BEGIN`** (o `START TRANSACTION`): apre la transazione; da qui in poi le modifiche sono "provvisorie".
- **`COMMIT`**: chiude la transazione **confermando** tutte le modifiche, che diventano permanenti e visibili agli altri.
- **`ROLLBACK`**: chiude la transazione **annullando** tutto, riportando il database esattamente com'era prima del `BEGIN`.

```sql
BEGIN;
  UPDATE conti SET saldo = saldo - 100 WHERE id = 'A';
  UPDATE conti SET saldo = saldo + 100 WHERE id = 'B';
COMMIT;   -- se qui qualcosa è andato storto, si usa ROLLBACK;
```

## Le quattro proprietà ACID, una a una

**ACID** è l'acronimo delle quattro garanzie che il DBMS offre su ogni transazione: **A**tomicity, **C**onsistency, **I**solation, **D**urability (atomicità, consistenza, isolamento, durabilità). Vediamole singolarmente, perché a colloquio non basta citarle: va spiegato *cosa* garantisce ciascuna e *come*.

### A — Atomicità (Atomicity)

L'**atomicità** garantisce il principio **"tutto o niente"**: una transazione è indivisibile (dal greco *átomos*, non divisibile). O vengono applicate **tutte** le sue operazioni, o **nessuna**. Non esistono esecuzioni parziali.

Nel bonifico: se il secondo `UPDATE` fallisce (magari il conto B non esiste), il DBMS deve **disfare** anche il primo, riportando il saldo di A al valore originale. Questo "disfare" si chiama **rollback** (letteralmente "riavvolgere"). L'atomicità è ciò che impedisce lo stato intermedio in cui i soldi sono spariti.

### C — Consistenza (Consistency)

La **consistenza** garantisce che una transazione porti il database da uno **stato valido** a un altro **stato valido**, rispettando tutti i **vincoli di integrità** definiti sullo schema: chiavi primarie uniche, chiavi esterne che puntano a righe esistenti, vincoli `CHECK` (es. `saldo >= 0`), ecc. Se una transazione tentasse di violare un vincolo (per esempio portare un saldo sotto zero quando c'è un `CHECK (saldo >= 0)`), il DBMS la **rifiuta** e fa rollback.

Attenzione a un punto sottile che i colloquiatori amano: la consistenza *applicativa* (il fatto che "la somma dei saldi resti invariata in un bonifico") è responsabilità di chi **scrive** la transazione, cioè del programmatore. Il DBMS garantisce solo che i vincoli **dichiarati** nello schema non vengano violati; se scrivi un bonifico che toglie 100 ad A ma ne aggiunge 90 a B, nessun vincolo si lamenta, ma la logica è sbagliata. ACID protegge i vincoli formali, non la correttezza del tuo ragionamento.

### I — Isolamento (Isolation)

L'**isolamento** garantisce che transazioni **concorrenti** (eseguite in parallelo) non si disturbino a vicenda: ciascuna deve vedere il database **come se fosse l'unica** in esecuzione. Il risultato finale di più transazioni concorrenti deve essere equivalente a una qualche loro esecuzione **sequenziale** (una dopo l'altra): questa proprietà ideale si chiama **serializzabilità** (*serializability*).

Senza isolamento emergono le classiche **anomalie di concorrenza**:

- **Dirty read** (lettura sporca): una transazione legge dati che un'altra ha scritto ma **non ancora confermato** con `COMMIT`; se quell'altra poi fa rollback, hai letto un valore che non è mai esistito davvero.
- **Non-repeatable read** (lettura non ripetibile): leggi la stessa riga due volte nella stessa transazione e ottieni valori diversi, perché nel frattempo un'altra transazione l'ha modificata e confermata.
- **Phantom read** (lettura fantasma): esegui due volte la stessa query con una condizione (es. `WHERE saldo > 1000`) e la seconda volta compaiono righe nuove ("fantasmi") inserite da un'altra transazione.

Siccome l'isolamento perfetto (serializzabilità totale) costa caro in prestazioni, lo standard SQL definisce dei **livelli di isolamento** (*isolation levels*) che permettono di scegliere quanto rigore si vuole, barattando sicurezza con velocità: **READ UNCOMMITTED**, **READ COMMITTED**, **REPEATABLE READ**, **SERIALIZABLE**. Più si sale, meno anomalie sono permesse ma più lock servono. Qui ci fermiamo ai **cenni**: il meccanismo con cui vengono realizzati (lock, timestamp, MVCC) e la tabella completa livello-per-anomalia li approfondiamo in `db-conc`, la lezione dedicata al controllo di concorrenza.

### D — Durabilità (Durability)

La **durabilità** garantisce che, una volta che una transazione ha ricevuto conferma del `COMMIT`, le sue modifiche **sopravvivono a qualsiasi guasto** successivo: crash del processo, caduta di corrente, riavvio della macchina. I dati confermati non si perdono più.

Come si ottiene se la RAM è volatile? Grazie al **log** scritto su memoria persistente (disco/SSD), che vediamo nella sezione seguente. Il principio è: prima di dire "commit riuscito" al client, il DBMS si assicura che la registrazione della modifica sia **già** finita su supporto non volatile.

## Come il DBMS realizza atomicità e durabilità: il log

Il cuore del meccanismo è il **log delle transazioni** (*transaction log* o *write-ahead log*, **WAL**): un file su disco in cui il DBMS annota **ogni** modifica *prima* di applicarla ai dati veri. Questa regola si chiama **Write-Ahead Logging** (registrazione anticipata): "scrivi prima nel log, poi tocca i dati".

Ogni voce del log registra, per ogni scrittura, il valore **prima** (*before image*, serve per disfare) e il valore **dopo** (*after image*, serve per rifare), più marcatori come `BEGIN`, `COMMIT`, `ABORT`. Da qui nascono le due operazioni di ripristino:

- **UNDO** (disfare): per una transazione **non** committata al momento del crash, il DBMS usa le *before image* per riportare indietro le modifiche già scritte. Realizza l'**atomicità** e il **rollback**.
- **REDO** (rifare): per una transazione **già** committata ma le cui modifiche erano ancora solo in memoria quando è arrivato il crash, il DBMS usa le *after image* per riapplicarle. Realizza la **durabilità**.

Perché funzioni la durabilità, al `COMMIT` il DBMS forza la scrittura fisica del record di commit nel log (operazione di *flush* / `fsync`): solo dopo che quel record è **fisicamente** sul disco, il commit è considerato riuscito e lo si comunica al client. Così, anche se la corrente salta un istante dopo, al riavvio la **fase di recovery** rilegge il log, fa REDO delle transazioni committate e UNDO di quelle rimaste a metà, riportando il database in uno stato coerente.

## Gli stati di una transazione

Durante la sua vita una transazione attraversa una sequenza ben precisa di **stati**:

1. **Active** (attiva): la transazione è in esecuzione, sta facendo letture e scritture. È lo stato iniziale subito dopo il `BEGIN`.
2. **Partially committed** (parzialmente committata): è stata eseguita l'ultima istruzione, ma le modifiche potrebbero essere ancora solo in memoria e il record di commit non è ancora stato forzato sul disco.
3. **Committed** (committata): il record di commit è stato scritto in modo durevole nel log; le modifiche sono ora permanenti. Stato finale di successo.
4. **Failed** (fallita): si è verificato un errore (violazione di vincolo, crash, deadlock) che impedisce di proseguire.
5. **Aborted** (abortita): dopo il fallimento, il DBMS ha eseguito il **rollback** (UNDO) riportando il database allo stato precedente al `BEGIN`. Stato finale di insuccesso. Da qui la transazione può essere **riavviata** da capo oppure semplicemente scartata.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 680 300" style="max-width:100%;height:auto;font-family:inherit">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--muted)"/>
    </marker>
  </defs>
  <g font-size="12.5" fill="var(--ink)" text-anchor="middle">
    <rect x="30" y="120" width="110" height="46" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="85" y="148">Active</text>
    <rect x="210" y="120" width="130" height="46" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="275" y="142" font-size="11.5">Partially</text><text x="275" y="157" font-size="11.5">committed</text>
    <rect x="420" y="40" width="120" height="46" rx="8" fill="var(--card)" stroke="var(--good)" stroke-width="1.7"/><text x="480" y="68">Committed</text>
    <rect x="210" y="220" width="130" height="46" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="275" y="248">Failed</text>
    <rect x="420" y="220" width="120" height="46" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="480" y="248">Aborted</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arr)">
    <path d="M140,143 L206,143"/>
    <path d="M340,130 L418,80"/>
    <path d="M110,166 C120,210 160,243 206,243"/>
    <path d="M340,150 C370,180 350,210 342,218"/>
    <path d="M340,243 L418,243"/>
  </g>
  <g font-size="10.5" fill="var(--muted)" text-anchor="middle">
    <text x="175" y="135">esegue</text>
    <text x="395" y="98">COMMIT (log su disco)</text>
    <text x="150" y="235">errore</text>
    <text x="378" y="198">errore</text>
    <text x="380" y="235">ROLLBACK / UNDO</text>
  </g>
  <text x="480" y="288" font-size="10.5" fill="var(--muted)" text-anchor="middle">da Aborted: riavvio da capo oppure scarto</text>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Diagramma degli stati di una transazione. Il percorso di successo porta da Active a Committed passando per la scrittura durevole del log; qualsiasi errore devia su Failed e poi, dopo l'UNDO, su Aborted, da cui la transazione può essere riavviata.</figcaption>
</figure>

## Esempi concreti

- **Bonifico con vincolo di saldo.** Supponi `conti(id, saldo)` con `CHECK (saldo >= 0)`, e `A = 50`, `B = 200`. La transazione `BEGIN; saldo_A = saldo_A - 100; saldo_B = saldo_B + 100; COMMIT;` tenta di portare A a `-50`: il vincolo `CHECK` scatta, il DBMS solleva un errore, la transazione passa a *failed* e poi *aborted* con UNDO. Risultato: `A` resta 50, `B` resta 200. Qui la **consistenza** (vincolo) ha innescato l'**atomicità** (rollback della prima riga già scritta).
- **Prenotazione dell'ultimo posto.** Due utenti cercano di prenotare l'unico posto rimasto a un concerto. Senza isolamento, entrambe le transazioni leggono `posti_liberi = 1`, entrambe decrementano, e si vendono **due** biglietti per un posto (anomalia). Con un livello di isolamento adeguato (e i lock che vedremo in `db-conc`), la seconda transazione aspetta la prima e, trovando `posti_liberi = 0`, fallisce correttamente.
- **Crash a metà commit.** Una transazione di e-commerce scrive l'ordine e scala il magazzino, poi riceve conferma di `COMMIT`. Un millisecondo dopo salta la corrente mentre le pagine erano ancora in RAM. Al riavvio, la **fase di recovery** trova nel log il record di commit e fa **REDO**: l'ordine e lo scarico di magazzino riappaiono. La **durabilità** ha retto perché il log era già su disco prima della conferma.

## Notable use case

- **PostgreSQL** usa un **WAL** (Write-Ahead Log): ogni modifica è registrata nel log prima di toccare le pagine dati, e il parametro di configurazione decide quanto aggressivamente forzare il flush al commit. Lo stesso WAL alimenta anche la replica verso i server secondari.
- **MySQL/InnoDB** implementa la durabilità con il **redo log** e l'atomicità/rollback con l'**undo log**, esattamente le due facce (REDO/UNDO) viste sopra. Di default offre il livello **REPEATABLE READ** tramite **MVCC** (*Multi-Version Concurrency Control*, gestione di più versioni delle righe), argomento di `db-conc`.
- **Oracle** e **SQL Server** adottano lo stesso schema log-based con recovery automatica al riavvio; il recovery è un servizio su cui si fonda ogni banca e sistema gestionale serio.
- **Sistemi distribuiti.** Quando una transazione deve toccare più database/nodi, l'atomicità "tutto o niente" si estende con protocolli come il **two-phase commit** (commit a due fasi): un coordinatore chiede a tutti i partecipanti "siete pronti?" e solo se tutti dicono sì invia il commit definitivo. È il ponte verso `xc-distsys`, dove le garanzie ACID incontrano i limiti del teorema CAP.

## Fonti

- **Silberschatz, Korth, Sudarshan** — *Database System Concepts* (capitoli su Transactions, Recovery System, Concurrency Control: il riferimento accademico)
- **Atzeni, Ceri, Paraboschi, Torlone** — *Basi di dati* (il testo italiano classico, parte sulla gestione delle transazioni)
- **PostgreSQL Documentation** — postgresql.org/docs (sezioni "Transactions", "Write-Ahead Logging", "Transaction Isolation")
- **Garcia-Molina, Ullman, Widom** — *Database Systems: The Complete Book*

## Concetti adiacenti

- `db-sql` — il linguaggio con cui scrivi le istruzioni che raggruppi dentro `BEGIN … COMMIT`
- `db-conc` — come l'isolamento viene davvero realizzato: lock, isolation levels in dettaglio, MVCC, deadlock
- `xc-distsys` — quando la transazione attraversa più nodi: two-phase commit, consenso e teorema CAP

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cos'è una transazione e perché il bonifico è l'esempio tipico del perché serve?
2. Cosa fanno esattamente `COMMIT` e `ROLLBACK`?
3. Spiega l'**atomicità**: cosa garantisce e con quale operazione il DBMS la realizza in caso di errore?
4. La **consistenza** ACID garantisce che la tua logica applicativa (es. "la somma dei saldi resta uguale") sia corretta? Cosa garantisce esattamente?
5. Cosa garantisce l'**isolamento** e cos'è la **serializzabilità**?
6. Spiega la differenza tra **dirty read**, **non-repeatable read** e **phantom read**.
7. Cosa garantisce la **durabilità** e perché la RAM volatile non è un problema?
8. Cos'è il **Write-Ahead Logging** e a cosa servono la *before image* e la *after image* nel log?
9. Qual è la differenza tra le operazioni di **UNDO** e **REDO** durante la recovery, e quale proprietà ACID realizza ciascuna?
10. Elenca gli **stati** di una transazione dal `BEGIN` fino a un esito di successo e a uno di insuccesso.

<details><summary>Risposte</summary>

1. È una **sequenza di operazioni** trattata come **un'unica unità logica indivisibile**. Il bonifico è due `UPDATE` (togli da A, aggiungi a B): se il sistema va in crash in mezzo, i soldi spariscono; la transazione garantisce che o avvengono entrambe le scritture o nessuna.
2. **`COMMIT`** conferma tutte le modifiche rendendole permanenti e visibili agli altri; **`ROLLBACK`** le annulla tutte, riportando il database esattamente com'era prima del `BEGIN`.
3. L'atomicità garantisce il **"tutto o niente"**: tutte le operazioni o nessuna. In caso di errore il DBMS esegue il **rollback (UNDO)** disfacendo le modifiche già applicate.
4. **No.** Garantisce solo il rispetto dei **vincoli di integrità dichiarati** nello schema (chiavi, foreign key, `CHECK`). La correttezza della logica applicativa (es. togliere 100 e aggiungere davvero 100) è responsabilità di chi scrive la transazione.
5. Garantisce che transazioni **concorrenti** non si disturbino: ciascuna vede il DB come se fosse l'unica. La **serializzabilità** è la proprietà per cui il risultato di esecuzioni concorrenti equivale a una qualche esecuzione **sequenziale** (una dopo l'altra) delle stesse transazioni.
6. **Dirty read:** leggi dati scritti da un'altra transazione **non ancora committata** (che potrebbe fare rollback). **Non-repeatable read:** rileggi la **stessa riga** e trovi un valore diverso perché un'altra l'ha modificata e committata nel frattempo. **Phantom read:** rieseguendo la stessa query con una condizione compaiono **righe nuove** inserite da un'altra transazione.
7. Garantisce che le modifiche di una transazione **committata sopravvivano a qualsiasi guasto** (crash, blackout). La RAM volatile non è un problema perché, prima di confermare il commit, il DBMS forza la scrittura del log su **memoria persistente** (disco/SSD).
8. Il **WAL** è la regola "scrivi prima nel log, poi tocca i dati": ogni modifica è registrata nel log prima di essere applicata. La **before image** (valore precedente) serve per l'**UNDO**, la **after image** (valore successivo) serve per il **REDO**.
9. **UNDO** disfà le transazioni **non committate** al momento del crash (usa la before image) → realizza l'**atomicità**. **REDO** riapplica le transazioni **già committate** le cui modifiche erano solo in RAM (usa la after image) → realizza la **durabilità**.
10. **Active** → **Partially committed** → **Committed** (successo). In caso di errore: **Active/Partially committed** → **Failed** → **Aborted** (dopo l'UNDO), da cui si può riavviare o scartare.
</details>

## Esercizi

1. **Scrivi una transazione SQL robusta.** Hai le tabelle `conti(id, saldo)` e `movimenti(id, conto, importo, data)`. Scrivi una transazione che trasferisce 250 euro dal conto `'A'` al conto `'B'` e registra due righe in `movimenti`, usando `BEGIN`/`COMMIT` e prevedendo il `ROLLBACK` nel caso il saldo di A diventi negativo. Spiega quale proprietà ACID interviene se qualcosa fallisce.
2. **Diagnostica l'anomalia.** Per ciascuno dei tre scenari, dì **quale proprietà ACID** viene violata (o quale anomalia di isolamento si verifica) e **come il DBMS la previene**:
   a. Durante un bonifico il server si spegne dopo aver scalato A ma prima di accreditare B; al riavvio il denaro è sparito.
   b. La transazione T1 modifica il saldo di un conto senza committare; T2 lo legge e prende una decisione; poi T1 fa rollback.
   c. Il DBMS conferma un `COMMIT` al client, ma dopo un blackout al riavvio quell'ordine non c'è più.
3. **Ordina gli stati.** Data la sequenza di eventi: `BEGIN`; prima scrittura riuscita; seconda scrittura viola un `CHECK`; il sistema reagisce. Elenca nell'ordine gli stati attraversati dalla transazione e indica quale operazione di log viene eseguita.
4. **Ragiona sul log.** Spiega perché, se il DBMS scrivesse *prima* i dati e *poi* il log (cioè violando il Write-Ahead Logging), un crash nel mezzo renderebbe impossibile garantire l'atomicità.

<details><summary>Soluzioni</summary>

1. 
   ```sql
   BEGIN;
     UPDATE conti SET saldo = saldo - 250 WHERE id = 'A';
     UPDATE conti SET saldo = saldo + 250 WHERE id = 'B';
     INSERT INTO movimenti (conto, importo, data) VALUES ('A', -250, CURRENT_DATE);
     INSERT INTO movimenti (conto, importo, data) VALUES ('B', +250, CURRENT_DATE);
   COMMIT;
   ```
   Se sulla colonna `saldo` esiste un `CHECK (saldo >= 0)` e A non ha fondi sufficienti, il primo `UPDATE` solleva un errore: si esegue `ROLLBACK;` (automatico o esplicito) e **nessuna** delle quattro istruzioni resta applicata. Interviene l'**atomicità** (tutto o niente), innescata dalla **consistenza** (il vincolo violato). Senza transazione, avresti potuto scalare A e registrarne il movimento senza mai accreditare B.
2. 
   a. Violata l'**atomicità** (e, a valle, la consistenza: la somma dei saldi non torna). Il DBMS la previene con l'**UNDO** dal log: al riavvio la transazione non committata viene disfatta e A torna al saldo originale. 
   b. È una **dirty read**, violazione dell'**isolamento**: T2 ha letto un valore non committato che poi è stato annullato. Il DBMS la previene con un livello di isolamento almeno **READ COMMITTED** (che impedisce di leggere dati non committati), realizzato tramite lock o MVCC (dettagli in `db-conc`). 
   c. Violata la **durabilità**. Il DBMS la previene scrivendo in modo **forzato** il record di commit nel **log su disco** *prima* di confermare al client; al riavvio il **REDO** riapplica le modifiche della transazione committata.
3. **Active** (dopo `BEGIN`, prima scrittura riuscita) → la seconda scrittura viola il `CHECK` → **Failed** → il DBMS esegue l'**UNDO** (rollback) usando le *before image* del log → **Aborted**. Non si raggiunge mai *Committed*.
4. Perché l'atomicità in caso di crash si basa sul poter **disfare** (UNDO) le scritture incomplete usando le *before image* conservate nel log. Se i dati fossero già stati modificati su disco **senza** che il log contenesse la before image corrispondente, dopo il crash il DBMS non avrebbe alcun modo di sapere quale fosse il valore originale da ripristinare: la modifica parziale resterebbe impressa e il "tutto o niente" sarebbe impossibile. Il Write-Ahead Logging (log *prima*, dati *poi*) garantisce che per ogni modifica su disco esista sempre già la sua registrazione di UNDO.
</details>
