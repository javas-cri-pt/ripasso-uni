---
day: 13
topic_id: os-processes
title: "Sistemi Operativi — processi, thread e concorrenza"
area: computer-science
course: Sistemi Operativi
grounded_in: "UNIBO/secondoAnno/Sistemi operativi"
adjacent: [os-scheduling, os-concurrency, xc-sysdesign]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun acronimo lasciato senza definizione."
---

# Sistemi Operativi — processi, thread e concorrenza

> **Perché oggi:** il **sistema operativo (SO)** è ciò su cui gira *ogni* tua app — dal backend Node al database. Capire **processi**, **thread** e **concorrenza** ti serve per tre cose molto concrete: scrivere un backend che regge più richieste insieme, evitare bug subdoli (le **race condition**, che in produzione fanno perdere soldi veri), e rispondere ai colloqui di sistemi senza andare nel panico. È materia "vecchia" ma è il cuore pratico di tutto il resto.

## Cos'è un sistema operativo (in 4 righe)

Un **sistema operativo (SO)** è il software che **gestisce le risorse della macchina** — CPU, memoria, dischi, dispositivi — e fa da **intermediario tra l'hardware e i tuoi programmi**. Tre termini che useremo:

- **Kernel** = il "nocciolo" del SO, la parte sempre in memoria che ha il controllo diretto dell'hardware (decide chi usa la CPU, chi accede alla memoria, ecc.).
- **System call (chiamata di sistema)** = il modo in cui un programma **chiede un servizio al kernel** (aprire un file, creare un processo, mandare dati in rete). Il tuo codice non tocca l'hardware da solo: passa sempre dal kernel via system call.
- **Modalità utente vs modalità kernel** = due "livelli di privilegio" della CPU. Il tuo programma gira in **modalità utente** (limitata, non può toccare l'hardware direttamente); quando fa una system call, la CPU passa in **modalità kernel** (privilegiata) per eseguire l'operazione sensibile, poi torna indietro. È una barriera di sicurezza: un'app che va in crash non porta giù la macchina.

## Processo

Un **processo** è un **programma in esecuzione**. Attenzione alla distinzione: il *programma* è un file inerte su disco; il *processo* è quel programma **caricato in memoria e in corso di esecuzione**, con le sue risorse. Ogni processo ha un suo **spazio di memoria isolato**, cioè un'area di memoria che gli altri processi **non possono leggere né scrivere** (isolamento = sicurezza + robustezza). Quello spazio è diviso in quattro parti:

- **Codice (text)** = le istruzioni del programma.
- **Dati** = le variabili globali/statiche.
- **Heap** = la memoria allocata dinamicamente a runtime (es. `malloc` in C, `new` altrove); cresce quando chiedi memoria.
- **Stack** = la pila delle chiamate a funzione: parametri, variabili locali, indirizzi di ritorno. Cresce e si restringe man mano che entri ed esci dalle funzioni.

**PCB (Process Control Block).** Per gestire un processo, il SO tiene una struttura dati che lo descrive: il **PCB (Process Control Block)**, letteralmente "blocco di controllo del processo". Dentro ci sono: il **PID (Process IDentifier)** cioè il numero identificativo del processo, lo **stato** corrente, il **program counter** (a quale istruzione è arrivato), il contenuto dei **registri** della CPU, informazioni sulla memoria e sui file aperti. Il PCB è ciò che permette al SO di **sospendere e riprendere** un processo senza perdere nulla.

**Stati del processo.** Nel suo ciclo di vita un processo attraversa questi stati:

- **new** = appena creato, il SO lo sta preparando.
- **ready** ("pronto") = ha tutto per girare e **aspetta solo la CPU**. Sta in una coda insieme agli altri pronti.
- **running** ("in esecuzione") = sta usando la CPU **ora**. Su un singolo core, un solo processo è running alla volta.
- **waiting / blocked** ("in attesa / bloccato") = **non può proseguire** perché aspetta un evento esterno, tipicamente un'operazione di **I/O (Input/Output)**, cioè lettura/scrittura da disco o rete. Non spreca CPU mentre aspetta.
- **terminated** ("terminato") = ha finito (o è stato ucciso); il SO recupera le sue risorse.

Cosa fa cambiare stato: da **ready → running** ci pensa lo **scheduler** (la parte del SO che sceglie *chi* far girare — approfondimento in `os-scheduling`); da **running → ready** succede quando scade il suo turno di CPU (**preemption**, "prelazione": il SO lo mette in pausa per dare spazio a un altro); da **running → waiting** quando il processo fa I/O o chiede una risorsa non disponibile; da **waiting → ready** quando l'evento atteso arriva (il dato dal disco è pronto) — nota che **non** torna diretto a running, si rimette in coda.

**Context switch (cambio di contesto).** Quando la CPU passa dal processo A al processo B, il SO deve **salvare lo stato di A** (registri, program counter → nel PCB di A) e **caricare lo stato di B** (dal PCB di B). Questa operazione si chiama **context switch** e **ha un costo**: durante lo switch la CPU non fa lavoro utile, e in più si "sporcano" le cache. È lavoro puro di gestione (overhead). Tienilo a mente: fare *troppi* switch (troppi processi/thread che si contendono pochi core) fa **perdere prestazioni**.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 640 320" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arOs13" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12.5" fill="var(--ink)" text-anchor="middle">
   <rect x="250" y="14" width="140" height="40" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="320" y="39">new</text>
   <rect x="40" y="130" width="150" height="44" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="115" y="157">ready (pronto)</text>
   <rect x="450" y="130" width="150" height="44" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="525" y="157">running (in CPU)</text>
   <rect x="245" y="256" width="150" height="44" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="320" y="283">waiting (bloccato)</text>
   <rect x="450" y="256" width="150" height="44" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="525" y="283">terminated</text>
  </g>
  <g font-size="11" fill="var(--muted)" text-anchor="middle">
   <text x="230" y="86">ammesso</text>
   <text x="300" y="145">dispatch (scheduler)</text>
   <text x="345" y="205">scade il turno</text>
   <text x="460" y="212">I/O / attesa</text>
   <text x="175" y="240">evento pronto</text>
   <text x="600" y="215">exit</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arOs13)">
   <path d="M270,54 C200,80 150,100 120,128"/>
   <path d="M192,145 L448,145"/>
   <path d="M448,163 L192,163"/>
   <path d="M500,174 C470,215 430,240 396,262"/>
   <path d="M245,266 C170,240 140,210 118,176"/>
   <path d="M525,174 L525,254"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Diagramma degli stati del processo: ready ⇄ running (lo scheduler assegna la CPU, la prelazione la toglie), running → waiting su I/O, waiting → ready quando l'evento è pronto (si rimette in coda, non torna diretto a running), running → terminated all'uscita.</figcaption>
</figure>

## Thread

Un **thread** (letteralmente "filo") è un **singolo flusso di esecuzione dentro un processo**. Un processo può avere un solo thread (il caso classico) oppure **più thread** che avanzano ciascuno per conto suo *ma dentro lo stesso processo*.

La differenza chiave sta in **cosa si condivide**. Più thread dello stesso processo **condividono**:

- il **codice**,
- i **dati** (variabili globali),
- lo **heap** (la memoria allocata dinamicamente),
- i file aperti.

Ma **ogni thread ha il suo stack** (le sue chiamate a funzione, le sue variabili locali) e i suoi registri/program counter. In una riga: **memoria condivisa, esecuzione separata**.

**Processo vs thread — la tabella mentale:**

| | Processo | Thread |
|---|---|---|
| **Memoria** | spazio **isolato** (nessuno vede quello degli altri) | **condivisa** con gli altri thread del processo (tranne lo stack) |
| **Comunicazione** | complessa: serve **IPC (Inter-Process Communication)**, cioè meccanismi appositi (pipe, socket, memoria condivisa) | semplice: basta leggere/scrivere le stesse variabili |
| **Costo di creazione** | alto (nuovo spazio di memoria) | basso (riusa quello del processo) |
| **Costo di context switch** | alto | più basso (meno roba da cambiare) |
| **Robustezza** | un crash **non** tocca gli altri processi | un thread che corrompe la memoria condivisa **può** rompere tutto il processo |

**Multithreading** = usare più thread nello stesso processo. A cosa serve:

1. **Parallelismo**: su una CPU **multi-core** thread diversi possono girare *davvero contemporaneamente* su core diversi → il lavoro finisce prima.
2. **Non bloccare su I/O**: mentre un thread è **waiting** su un'operazione lenta (leggere dal disco, aspettare una risposta di rete), un altro thread dello stesso processo può continuare a lavorare. È il motivo pratico numero uno nei backend: mentre servi una richiesta che aspetta il database, ne servi altre.

**Cenno — thread a livello utente vs kernel.** I thread **a livello kernel** sono conosciuti e schedulati dal SO (il kernel sa che esistono e li mette lui sui core). I thread **a livello utente** sono gestiti da una libreria dentro il processo, senza che il kernel li veda: sono leggerissimi da creare, ma se **uno** si blocca su una system call rischia di **bloccare tutti** perché il kernel vede un solo thread. I sistemi reali spesso combinano i due (modelli "molti-a-molti"). Ti basta sapere che esiste la distinzione.

## Concorrenza e il problema della sincronizzazione

**Concorrenza** = più flussi di esecuzione (thread o processi) che **avanzano "insieme"**. "Insieme" può voler dire *interleaved* — si alternano a piccoli pezzi sullo stesso core, dando l'illusione della simultaneità — oppure *paralleli* — davvero contemporanei su core diversi. In entrambi i casi il problema è lo stesso.

**Il problema.** Finché ogni thread lavora sui *suoi* dati, tutto bene. I guai iniziano quando **due o più thread toccano lo stesso dato condiviso**. L'ordine con cui i loro passi si intrecciano è **imprevedibile** (lo decide lo scheduler, momento per momento), e alcuni intrecci producono un risultato **sbagliato**. Questo si chiama **race condition** (letteralmente "condizione di corsa"): il risultato **dipende dall'ordine di esecuzione**, che tu non controlli.

**Esempio concreto — due thread incrementano lo stesso saldo.** Immagina una variabile condivisa `saldo = 100`. Due thread eseguono `saldo = saldo + 50`. Ti aspetti `200`. Ma quell'istruzione **non è atomica**: la CPU la esegue in **tre passi separati** — *leggi* il valore dalla memoria, *modifica* (aggiungi 50), *scrivi* il risultato indietro (in inglese: **read-modify-write**). Ora guarda un intreccio sfortunato:

```
saldo = 100

Thread A: legge saldo → 100
Thread B: legge saldo → 100      (A non ha ancora scritto!)
Thread A: calcola 100 + 50 = 150
Thread B: calcola 100 + 50 = 150
Thread A: scrive saldo = 150
Thread B: scrive saldo = 150      (sovrascrive A)

saldo finale = 150   ← SBAGLIATO, doveva essere 200
```

Un incremento è **sparito**. Perché? Perché B ha letto il valore **prima** che A finisse di scriverlo: la sequenza leggi-modifica-scrivi dei due si è **intrecciata**. Questo è il tipico bug che **non si vede quasi mai in test** (di solito i passi non si intrecciano male) e poi **esplode in produzione** sotto carico. È esattamente il genere di bug su cui ti interrogano ai colloqui.

Due definizioni per parlarne con precisione:

- **Sezione critica (critical section)** = il **pezzo di codice che accede al dato condiviso** (nell'esempio: le tre operazioni su `saldo`). È la zona "pericolosa".
- **Mutua esclusione (mutual exclusion)** = la garanzia che **un solo thread alla volta** possa trovarsi nella sezione critica. Se la ottieni, la race condition sparisce: B è costretto ad aspettare che A abbia finito *tutta* la sequenza leggi-modifica-scrivi prima di iniziare la sua.

## Gli strumenti di sincronizzazione

Ottenere la mutua esclusione è il lavoro degli **strumenti di sincronizzazione**. Dal più basso al più alto livello:

- **Lock / mutex.** Un **mutex** (da *MUTual EXclusion*) è una "serratura": prima di entrare nella sezione critica fai `lock()` (acquisisci la serratura), quando esci fai `unlock()` (la rilasci). Se un secondo thread prova a fare `lock()` mentre è già presa, **si ferma e aspetta** finché non viene rilasciata. Così solo uno è dentro alla volta. Regola d'oro: **prendi il lock prima, rilascialo sempre dopo** (anche in caso di errore), altrimenti gli altri restano fuori per sempre.

- **Semaforo (semaphore).** Un **contatore** gestito dal SO che regola **quanti thread possono passare**. Ha due operazioni: `wait` (o `P`) **decrementa** il contatore, e se va sotto zero il thread si blocca; `signal` (o `V`) **incrementa** e sveglia un thread in attesa. Due sapori: **binario** (contatore 0/1 → si comporta come un mutex, uno alla volta) e **contatore** (valore N → permette fino a N thread insieme, utile per limitare l'accesso a una risorsa con N "posti", es. un pool di 10 connessioni al database). Differenza pratica col mutex: il mutex ha di solito un "proprietario" (chi lo prende lo rilascia), il semaforo no ed è più generale (serve anche a **coordinare** thread, non solo a proteggere dati).

- **Monitor.** Un costrutto di **livello più alto** che **incapsula insieme** i dati condivisi **e** la mutua esclusione: tutti i metodi del monitor sono automaticamente in mutua esclusione, quindi non devi ricordarti tu di prendere/rilasciare il lock a mano. L'esempio che conosci: in **Java** la parola chiave **`synchronized`** su un metodo/blocco fa proprio questo — garantisce che un solo thread alla volta esegua quel codice sull'oggetto. Il monitor è "più difficile sbagliarlo" perché la serratura è integrata nel costrutto.

**Cenno — deadlock (stallo).** Attento all'effetto collaterale dei lock: due thread possono bloccarsi **a vicenda per sempre**. Classico: A tiene il lock 1 e vuole il lock 2; B tiene il lock 2 e vuole il lock 1. Nessuno dei due molla, nessuno dei due avanza → **deadlock**. È un problema serio con condizioni e soluzioni proprie: lo approfondisci in `os-deadlock`.

## Concorrenza vs parallelismo

Sono spesso confusi, ma **non** sono la stessa cosa — e alle interviste lo chiedono apposta.

- **Concorrenza** = **gestire più cose che avanzano** nello stesso periodo di tempo. Riguarda la **struttura** del programma. Puoi avere concorrenza **anche su un solo core**: i thread si **alternano** a piccoli pezzi (interleaving) e sembrano procedere insieme, ma in ogni istante ne gira uno solo.
- **Parallelismo** = **eseguire davvero più cose nello stesso istante**. Riguarda l'**esecuzione** e richiede **hardware con più core** (o più macchine): al tempo T, due istruzioni girano *contemporaneamente*.

Slogan da ricordare (Rob Pike): *"la concorrenza è occuparsi di molte cose insieme, il parallelismo è farle insieme"*. Un programma può essere concorrente ma non parallelo (un core, thread che si alternano), parallelo grazie alla concorrenza (più core), o nessuno dei due. La race condition è un problema della **concorrenza**: esiste anche su un solo core, perché basta che i passi di due thread si **intreccino** male.

## Perché conta nel tuo lavoro (il ponte)

Qui tutto diventa pratico. Un **web server** deve servire **tante richieste insieme**, e lo fa scegliendo un modello di concorrenza:

- **thread/processi per richiesta** (es. server Java, PHP-FPM): ogni richiesta ha il suo thread; semplice da ragionare, ma migliaia di thread costano in memoria e context switch;
- **modello asincrono / event loop** (es. Node.js, Nginx): **un solo thread** che non si blocca mai su I/O — quando un'operazione lenta parte, il thread passa a un'altra richiesta e verrà richiamato quando l'I/O è pronto. Regge tantissime connessioni con poca memoria.

Le **race condition** sono **bug reali in produzione**: due richieste che aggiornano lo stesso record, due processi che scrivono lo stesso contatore. Compaiono solo sotto carico, sono difficili da riprodurre, e possono corrompere dati (o soldi).

Ed ecco il collegamento più importante per i colloqui di system design: è **il motivo per cui i server web si tengono stateless**. **Stateless** = il server **non conserva stato dell'utente in memoria tra una richiesta e l'altra**. Perché? Perché con più server (o più thread/processi) lo stato in memoria locale sarebbe (a) **perso** se quel server cade o se la richiesta successiva finisce su un altro, e (b) una fonte di **race condition** difficili. La soluzione: **lo stato va in uno store condiviso** (un database, o una cache come Redis) che gestisce lui la concorrenza. Così ogni server è intercambiabile e scali semplicemente aggiungendone altri (aggancio a `xc-sysdesign`).

Infine, la programmazione **async/await** che usi ogni giorno **nasce da qui**: è un modo di scrivere codice concorrente *senza bloccare* il thread mentre aspetti l'I/O, leggibile come se fosse sequenziale. Sotto sotto è l'event loop di cui sopra.

## Notable use cases

- **Node.js** — **single-thread + event loop**. Il tuo codice JavaScript gira su **un solo thread**, quindi **non hai race condition** sulle variabili JS (due pezzi di codice non girano mai davvero insieme). Il prezzo: non devi **bloccare** quel thread (un calcolo lungo e sincrono congela tutto il server); usi **callback / promise / async-await** per l'I/O. Le operazioni pesanti vere le delega a un pool di thread interno.
- **Database e transazioni** — i DB usano **lock** per proteggere i dati quando più transazioni li toccano insieme, garantendo che il risultato sia come se fossero eseguite una alla volta (è la "I" di **ACID**, *Isolation*). È mutua esclusione applicata ai dati persistenti.
- **Browser multi-processo** — i browser moderni mettono **ogni scheda in un processo separato**: se una pagina va in crash o è compromessa, l'**isolamento tra processi** impedisce che porti giù le altre schede o il browser. Esattamente il vantaggio del processo (memoria isolata) di cui abbiamo parlato.

## Fonti

- **A. Silberschatz, P. Galvin, G. Gagne — *Operating System Concepts*** (il "dinosauro", per la copertina): il testo di riferimento classico su processi, thread e sincronizzazione.
- **A. Tanenbaum — *Modern Operating Systems***: altro riferimento storico, molto chiaro sui concetti di base.
- **OSTEP — *Operating Systems: Three Easy Pieces*** (Arpaci-Dusseau), **gratuito online su ostep.org**: la parte "Concurrency" spiega thread, lock e race condition in modo asciutto e pratico.

## Concetti adiacenti

- **os-scheduling** — *come* il SO sceglie quale processo/thread mandare in CPU tra i "ready" (algoritmi: round-robin, priorità, ecc.).
- **os-concurrency** — approfondimento sui pattern e i problemi classici di sincronizzazione (produttore-consumatore, lettori-scrittori).
- **os-deadlock** — quando i thread si bloccano a vicenda per sempre: condizioni necessarie, prevenzione, rilevamento.
- **xc-sysdesign** — come le regole di concorrenza (stateless, store condiviso, scale-out) diventano scelte di architettura per sistemi che reggono la scala.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Qual è la differenza tra un **programma** e un **processo**?
2. Cosa **condividono** i thread dello stesso processo, e cosa invece ha **ciascun thread per sé**?
3. Elenca gli **stati del processo** e di' cosa fa passare un processo da **running** a **waiting**.
4. Cos'è un **context switch** e perché ha un **costo**?
5. Cos'è una **race condition** e *perché* nasce nell'esempio dei due thread che incrementano lo stesso saldo?
6. Definisci **sezione critica** e **mutua esclusione**.
7. Che differenza c'è tra un **mutex** e un **semaforo** (binario vs contatore)?
8. Cos'è un **monitor** e quale costrutto Java lo realizza?
9. **Concorrenza** e **parallelismo**: che differenza c'è? Può esserci concorrenza su un solo core?
10. Perché i server web si tengono **stateless** e dove va messo lo stato?

<details><summary>Risposte</summary>

1. Il **programma** è un file inerte su disco (le istruzioni); il **processo** è quel programma **caricato in memoria e in esecuzione**, con il suo spazio di memoria isolato (codice, dati, heap, stack) e le sue risorse. Programma = statico; processo = programma "vivo".

2. **Condividono**: codice, dati (variabili globali), **heap** e file aperti. **Per sé** ogni thread ha il proprio **stack** (variabili locali, chiamate a funzione) e i propri registri/program counter. In breve: memoria condivisa, esecuzione separata.

3. Stati: **new, ready, running, waiting/blocked, terminated**. Da **running → waiting** si passa quando il processo deve **aspettare un evento esterno**, tipicamente un'operazione di **I/O** (lettura/scrittura da disco o rete) o una risorsa non disponibile: non può proseguire, quindi lascia la CPU e non la spreca mentre aspetta.

4. Un **context switch** è il passaggio della CPU da un processo/thread a un altro: il SO **salva lo stato** del primo (registri, program counter nel PCB) e **carica lo stato** del secondo. Ha un **costo** perché durante lo switch la CPU non fa lavoro utile ed è puro overhead di gestione (in più si "sporcano" le cache); troppi switch fanno perdere prestazioni.

5. Una **race condition** è una situazione in cui il **risultato dipende dall'ordine imprevedibile** con cui si intrecciano le esecuzioni di più thread sullo **stesso dato condiviso**. Nell'esempio del saldo nasce perché `saldo = saldo + 50` **non è atomica**: è una sequenza **leggi-modifica-scrivi** in tre passi. Se il thread B **legge** il saldo *prima* che A abbia **scritto** il suo risultato, entrambi partono da 100, calcolano 150 e scrivono 150: un incremento va perso (risultato 150 invece di 200).

6. **Sezione critica** = il pezzo di codice che **accede al dato condiviso** (la zona pericolosa). **Mutua esclusione** = la garanzia che **un solo thread alla volta** stia nella sezione critica; ottenendola, la race condition sparisce.

7. Un **mutex** è una serratura per la mutua esclusione: `lock` prima della sezione critica, `unlock` dopo; di solito ha un "proprietario" (chi lo prende lo rilascia), uno alla volta. Un **semaforo** è un **contatore** gestito dal SO (`wait`/`P` decrementa e può bloccare, `signal`/`V` incrementa e sveglia): **binario** (0/1, si comporta come un mutex, uno alla volta) o **contatore** (valore N, permette fino a **N** thread insieme, es. un pool di N connessioni). Il semaforo è più generale e serve anche a **coordinare** thread, non solo a proteggere un dato.

8. Un **monitor** è un costrutto di alto livello che **incapsula insieme dati condivisi e mutua esclusione**: i suoi metodi sono automaticamente in mutua esclusione, così non gestisci il lock a mano. In **Java** lo realizza la parola chiave **`synchronized`** (un solo thread alla volta esegue il blocco/metodo sull'oggetto).

9. **Concorrenza** = gestire più flussi che **avanzano** nello stesso periodo (struttura del programma); **parallelismo** = eseguirli **davvero nello stesso istante** (richiede più core/macchine). **Sì**, c'è concorrenza anche su un solo core: i thread si **alternano** a piccoli pezzi (interleaving) e in ogni istante ne gira uno solo, ma "avanzano insieme". Ecco perché la race condition esiste anche su un solo core.

10. Perché con **più server** (o più thread/processi) lo stato tenuto in **memoria locale** verrebbe **perso** se quel server cade o se la richiesta successiva finisce su un altro server, e sarebbe fonte di **race condition**. Tenendo i server **stateless** (senza stato dell'utente in memoria tra le richieste) ogni server è **intercambiabile** e si scala aggiungendone altri. Lo **stato va in uno store condiviso** — un database o una cache tipo Redis — che gestisce lui la concorrenza.

</details>
