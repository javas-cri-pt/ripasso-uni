---
day: 33
topic_id: os-scheduling
title: "Scheduling della CPU"
area: computer-science
course: "Sistemi Operativi"
grounded_in: null
adjacent: [os-processes, os-concurrency, os-deadlock]
completeness_checked: true
quiz_count: 10
---

# Scheduling della CPU

> **Perché oggi:** in `os-processes` hai visto che un sistema operativo tiene in vita molti processi insieme, ma la CPU (o ogni singolo core) può eseguirne davvero **uno solo alla volta**. Chi sceglie quale processo pronto mandare in esecuzione, e per quanto, è lo **scheduler**. È una decisione che prende migliaia di volte al secondo e che determina se il sistema ti sembra reattivo o impallato. Qui vediamo gli algoritmi classici (FCFS, SJF, SRTF, Round Robin, priorità, code multilivello) con i conti fatti per davvero, così da saper dire a voce quale conviene e perché.

## Il problema: cosa decide lo scheduler
Un **processo** (vedi `os-processes`) alterna due fasi: **CPU burst** (quando calcola e ha bisogno della CPU) e **I/O burst** (quando aspetta il disco, la rete, l'utente). Mentre un processo è in attesa di I/O la CPU resterebbe inutilizzata: lo **scheduler della CPU** (detto anche *short-term scheduler*) sceglie, tra i processi nello stato **pronto** (ready), quale assegnare alla CPU per sfruttarla al massimo.

La decisione può avvenire in due regimi:
- **Scheduling non-preemptive (senza prelazione):** una volta che un processo prende la CPU la tiene finché non finisce o si blocca volontariamente su un I/O. Semplice, ma un processo lungo può monopolizzare la CPU.
- **Scheduling preemptive (con prelazione):** il sistema operativo può **togliere** la CPU a un processo in corso (per esempio allo scadere di un tempo prestabilito o all'arrivo di un processo più urgente) e darla a un altro. L'operazione di salvare lo stato del processo uscente e caricare quello entrante si chiama **context switch** (cambio di contesto) ed ha un costo non nullo: è puro overhead, durante il quale non si fa lavoro utile.

## I criteri: cosa vuol dire "buono"
Non esiste lo scheduler migliore in assoluto, esiste quello giusto per l'obiettivo. Le metriche standard:
- **Throughput:** numero di processi completati per unità di tempo. Più alto è meglio.
- **Tempo di completamento (completion time):** l'istante in cui il processo finisce.
- **Tempo di turnaround:** tempo totale che il processo passa nel sistema, dall'**arrivo** al completamento. Formula: `turnaround = completamento − arrivo`.
- **Tempo di attesa (waiting time):** quanto tempo il processo passa nella coda dei pronti **senza** essere eseguito. Formula: `attesa = turnaround − durata del CPU burst`. È la metrica che gli algoritmi cercano tipicamente di minimizzare.
- **Tempo di risposta (response time):** tempo dall'arrivo al **primo** istante in cui il processo ottiene la CPU. Conta nei sistemi interattivi, dove importa che l'utente veda *qualcosa* subito.
- **Starvation (attesa indefinita):** il rischio che un processo non venga **mai** scelto perché ne arrivano sempre altri più prioritari. Un buono scheduler la evita.

Useremo sempre, per confrontare gli algoritmi, l'attesa media e il turnaround medio su uno stesso insieme di processi.

## FCFS (First-Come, First-Served)
Il più semplice: **primo arrivato, primo servito**. I processi vengono eseguiti nell'ordine in cui arrivano, senza prelazione. Si implementa con una semplice **coda FIFO**.

Esempio: tre processi arrivano tutti all'istante `0`, con durate `P1 = 24`, `P2 = 3`, `P3 = 3`, nell'ordine `P1, P2, P3`.

FCFS li esegue nell'ordine di arrivo:
- Attesa: `P1 = 0`, `P2 = 24`, `P3 = 27`. Media `= (0 + 24 + 27) / 3 = 17`.
- Turnaround: `P1 = 24`, `P2 = 27`, `P3 = 30`. Media `= 81 / 3 = 27`.

Il difetto è il **convoy effect (effetto convoglio):** un processo lungo davanti costringe tutti i corti ad aspettare, come un camion lento che blocca una fila di auto. Se riordinassimo gli stessi processi, l'attesa media crollerebbe: è esattamente l'idea del prossimo algoritmo.

## SJF (Shortest Job First) e SRTF
**SJF** esegue sempre, tra i processi pronti, quello con il **CPU burst più breve**. Si può dimostrare che SJF dà l'**attesa media minima possibile** per un dato insieme di processi.

Sullo stesso esempio di prima (`P1 = 24`, `P2 = 3`, `P3 = 3`), SJF sceglie l'ordine `P2, P3, P1`:
- Attesa: `P2 = 0`, `P3 = 3`, `P1 = 6`. Media `= 9 / 3 = 3`.
- Turnaround: `P2 = 3`, `P3 = 6`, `P1 = 30`. Media `= 39 / 3 = 13`.

Da `17` a `3` di attesa media, stessi processi. Due problemi però. Primo: richiede di **conoscere in anticipo** la durata del prossimo burst, cosa impossibile in generale; in pratica la si **stima** con una media esponenziale dei burst passati. Secondo: rischio di **starvation** per i processi lunghi se ne arrivano in continuazione di corti.

**SRTF (Shortest Remaining Time First)** è la **versione preemptive** di SJF: a ogni arrivo di un nuovo processo, se questo ha un tempo rimanente minore di quello in esecuzione, gli viene tolta la CPU. Minimizza l'attesa media ancora più aggressivamente quando gli arrivi sono scaglionati nel tempo, al prezzo di più context switch. Lo vedremo nei conti negli esercizi.

## Round Robin (RR)
È l'algoritmo dei sistemi **time-sharing** (a tempo condiviso), pensato per l'interattività. Si fissa un **quanto di tempo (time quantum)**, una piccola fetta (tipicamente da 10 a 100 ms). I processi stanno in una coda FIFO circolare: ciascuno riceve al massimo un quanto, poi, se non ha finito, viene **prelazionato** e rimesso in **fondo** alla coda; la CPU passa al successivo.

Sull'esempio `P1 = 24`, `P2 = 3`, `P3 = 3` con quanto `q = 4`, ordine `P1, P2, P3`:
- `P1` gira da `0` a `4` (gli restano `20`), poi va in coda.
- `P2` gira da `4` a `7` e finisce.
- `P3` gira da `7` a `10` e finisce.
- da `10` è rimasto solo `P1`, che gira ininterrotto da `10` a `30`.

Risultati: attesa media `= (6 + 4 + 7) / 3 ≈ 5.67`, turnaround medio `≈ 15.67`. Si colloca **tra** FCFS e SJF: RR non minimizza l'attesa, ma garantisce che nessuno aspetti più di `(n−1) × q` prima del primo turno, quindi ottimo **tempo di risposta** e nessuna starvation. La scelta del quanto è delicata: troppo grande e RR degenera in FCFS; troppo piccolo e l'overhead dei context switch divora la CPU. Regola pratica: il quanto deve essere grande rispetto al costo di un context switch, ma tale da far stare dentro la maggior parte dei burst.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 620 220" style="max-width:100%;height:auto;font-family:inherit">
<rect x="0" y="0" width="620" height="220" fill="var(--card2)" rx="8"/>
<g font-size="12" fill="var(--ink)">
<text x="20" y="28" font-weight="700">Diagramma di Gantt: FCFS vs SJF (P1=24, P2=3, P3=3)</text>
<text x="8" y="72" font-size="11" fill="var(--muted)">FCFS</text>
<rect x="40" y="56" width="432" height="30" fill="var(--card)" stroke="var(--rule)"/><text x="256" y="76" text-anchor="middle" font-size="11">P1</text>
<rect x="472" y="56" width="54" height="30" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="499" y="76" text-anchor="middle" font-size="10">P2</text>
<rect x="526" y="56" width="54" height="30" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="553" y="76" text-anchor="middle" font-size="10">P3</text>
<text x="38" y="104" font-size="9" fill="var(--muted)">0</text><text x="468" y="104" font-size="9" fill="var(--muted)">24</text><text x="522" y="104" font-size="9" fill="var(--muted)">27</text><text x="574" y="104" font-size="9" fill="var(--muted)">30</text>
<text x="8" y="146" font-size="11" fill="var(--muted)">SJF</text>
<rect x="40" y="130" width="54" height="30" fill="var(--card)" stroke="var(--good)" stroke-width="1.6"/><text x="67" y="150" text-anchor="middle" font-size="10">P2</text>
<rect x="94" y="130" width="54" height="30" fill="var(--card)" stroke="var(--good)" stroke-width="1.6"/><text x="121" y="150" text-anchor="middle" font-size="10">P3</text>
<rect x="148" y="130" width="432" height="30" fill="var(--card)" stroke="var(--rule)"/><text x="364" y="150" text-anchor="middle" font-size="11">P1</text>
<text x="38" y="178" font-size="9" fill="var(--muted)">0</text><text x="90" y="178" font-size="9" fill="var(--muted)">3</text><text x="144" y="178" font-size="9" fill="var(--muted)">6</text><text x="574" y="178" font-size="9" fill="var(--muted)">30</text>
<text x="20" y="206" font-size="10.5" fill="var(--muted)">Stessi processi, ordine diverso: attesa media FCFS = 17, SJF = 3. I corti davanti al lungo.</text>
</g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Lo stesso insieme di processi schedulato con FCFS (in alto, convoy effect: P2 e P3 aspettano il lungo P1) e con SJF (in basso, i due corti passano prima). Spostare i corti in testa abbatte l'attesa media da 17 a 3.</figcaption>
</figure>

## Scheduling a priorità
A ogni processo si associa una **priorità** (un numero); la CPU va al processo pronto con priorità più alta. SJF è di fatto un caso particolare di questo schema, dove la priorità è l'inverso della durata stimata del burst. Può essere **preemptive** (un processo più prioritario che arriva prelaziona quello in corso) o non-preemptive.

Il difetto noto è la **starvation**: un processo a bassa priorità può restare in coda per sempre se continuano ad arrivarne di più prioritari. La cura classica è l'**aging (invecchiamento):** si **aumenta gradualmente** la priorità dei processi che aspettano da tanto, così prima o poi anche il meno prioritario sale in cima e viene servito.

## Multilevel Feedback Queue (MLFQ)
La **coda a più livelli con retroazione (multilevel feedback queue)** è l'approccio che gli scheduler reali avvicinano di più: invece di una sola coda, ne usa **diverse**, ciascuna con una priorità e una sua politica. L'idea chiave, la "retroazione" (feedback), è che un processo **si sposta tra le code** in base al comportamento osservato:
- Un processo nuovo entra nella coda a **priorità più alta**, con un quanto piccolo.
- Se **consuma tutto il quanto** senza finire (segno che è CPU-bound, cioè fa molto calcolo), viene **retrocesso** in una coda a priorità più bassa, che però gli dà un quanto più lungo.
- Se invece **rilascia la CPU prima** del quanto (segno che è I/O-bound, cioè interattivo), resta in alto.

Così i processi interattivi e corti restano prioritari (buon tempo di risposta) e quelli lunghi ottengono comunque la CPU in blocchi grandi quando quelli corti non la usano, senza doverne conoscere la durata in anticipo. Per evitare starvation dei processi finiti in fondo si usa anche qui l'**aging**, periodicamente riportando tutti in alto.

## Esempi concreti
- **Il tuo editor di testo mentre compili:** la compilazione è un processo CPU-bound lungo; l'editor è I/O-bound, ha burst cortissimi tra una pressione di tasto e l'altra. Con uno scheduler MLFQ l'editor resta nelle code ad alta priorità e ti risponde immediatamente anche se la compilazione sta usando la CPU a tappo, perché ogni volta rilascia subito il quanto.
- **Convoy effect in un server:** un server che serve richieste in puro FCFS (una coda sola, nessuna prelazione) e riceve una richiesta "pesante" (un report enorme) fa aspettare dietro di lei decine di richieste leggere, che in isolamento durerebbero millisecondi. È la ragione per cui i server web usano thread pool con code gestite, non un singolo FCFS cieco.

## Notable use case
- **Linux** oggi usa lo scheduler **EEVDF (Earliest Eligible Virtual Deadline First)**, che dal kernel 6.6 ha sostituito il precedente **CFS (Completely Fair Scheduler)**. L'idea di fondo resta la stessa del CFS: ripartire la CPU in modo **equo** tra i task tenendo traccia di quanto tempo "virtuale" ciascuno ha già consumato, e dare la CPU a chi ne ha avuto meno, con una logica di scadenze per garantire reattività agli interattivi.
- **Windows** usa uno scheduler **preemptive a priorità** con 32 livelli e un meccanismo di **priority boost** (parente dell'aging) che rialza temporaneamente la priorità di un thread quando, per esempio, finisce di attendere un I/O, per migliorare la reattività.

## Fonti
- **Silberschatz, Galvin, Gagne** — *Operating System Concepts* (il capitolo "CPU Scheduling", riferimento per FCFS/SJF/RR/MLFQ)
- **Tanenbaum** — *Modern Operating Systems* (capitolo sullo scheduling, con la distinzione batch/interattivo/real-time)
- **Arpaci-Dusseau** — *Operating Systems: Three Easy Pieces*, ostep.org (ottimo capitolo gratuito su MLFQ)

## Concetti adiacenti
- `os-processes` — processi, thread e stati (ready/running/waiting): il contesto in cui opera lo scheduler
- `os-concurrency` — quando più processi condividono dati, l'ordine con cui lo scheduler li alterna crea race condition da gestire
- `os-deadlock` — l'altra faccia della contesa di risorse: qui si sceglie chi va in CPU, lì cosa succede quando ci si blocca a vicenda

## Quiz (10 — tutte rispondibili dalla lezione)
1. Qual è la differenza tra scheduling **preemptive** e **non-preemptive**, e cos'è un **context switch**?
2. Scrivi le formule di **tempo di turnaround** e **tempo di attesa** a partire da arrivo, completamento e durata del burst.
3. Cos'è il **convoy effect** e con quale algoritmo si manifesta?
4. Perché si dice che **SJF** è ottimo, e quali due problemi pratici ha?
5. Che differenza c'è tra **SJF** e **SRTF**?
6. In **Round Robin**, cosa succede a un processo che non finisce entro il quanto, e cosa comporta scegliere un quanto troppo grande o troppo piccolo?
7. Perché RR ha un ottimo **tempo di risposta** ma non minimizza l'attesa media?
8. Cos'è la **starvation** nello scheduling a priorità, e come la risolve l'**aging**?
9. Nella **multilevel feedback queue**, in base a quale comportamento un processo viene retrocesso o mantenuto in alto?
10. Qual è la differenza tra **tempo di risposta** e **tempo di attesa**?

<details><summary>Risposte</summary>

1. Nel **non-preemptive** un processo tiene la CPU finché non finisce o si blocca su I/O; nel **preemptive** il sistema operativo può togliergliela (es. allo scadere del quanto o all'arrivo di uno più urgente). Il **context switch** è il salvataggio dello stato del processo uscente e il caricamento di quello entrante: overhead puro.
2. `turnaround = completamento − arrivo`; `attesa = turnaround − durata del CPU burst`.
3. È quando un processo lungo davanti costringe tutti i corti dietro di lui ad aspettare, gonfiando l'attesa media. Si manifesta con **FCFS**.
4. È ottimo perché minimizza l'**attesa media** per un dato insieme di processi. Problemi: richiede di **conoscere in anticipo** la durata del prossimo burst (va stimata) e può causare **starvation** dei processi lunghi.
5. **SJF** è non-preemptive (il processo scelto gira fino alla fine del burst); **SRTF** è la sua versione preemptive: all'arrivo di un processo con tempo rimanente minore, prelaziona quello in corso.
6. Viene **prelazionato** e rimesso in **fondo** alla coda, la CPU passa al prossimo. Quanto troppo grande: RR degenera in **FCFS**. Quanto troppo piccolo: troppi context switch, overhead che spreca CPU.
7. Perché garantisce a ciascuno un turno entro `(n−1) × q`, quindi tutti partono presto (ottimo response time); ma spezzettando i processi lunghi e mescolandoli, non raggiunge l'attesa media minima come farebbe SJF.
8. La **starvation** è un processo a bassa priorità che non viene mai scelto perché arrivano sempre processi più prioritari. L'**aging** aumenta gradualmente la priorità di chi aspetta da tanto, così prima o poi sale in cima.
9. Se **consuma tutto il quanto** senza finire (CPU-bound) viene retrocesso a priorità più bassa; se **rilascia la CPU prima** del quanto (I/O-bound, interattivo) resta in alto.
10. Il **tempo di risposta** va dall'arrivo al **primo** istante in cui il processo ottiene la CPU; il **tempo di attesa** è il totale del tempo passato nella coda dei pronti senza essere eseguito (può accumularsi in più intervalli).
</details>

## Esercizi
1. **FCFS e SJF non-preemptive con arrivi scaglionati.** Dati i processi `P1 (arrivo 0, burst 8)`, `P2 (arrivo 1, burst 4)`, `P3 (arrivo 2, burst 9)`, `P4 (arrivo 3, burst 5)`, calcola il **tempo di attesa medio** e il **turnaround medio** con FCFS e con SJF non-preemptive.
2. **SRTF (preemptive).** Sullo stesso insieme dell'esercizio 1, calcola attesa media e turnaround medio con SRTF. Confronta con i risultati precedenti.
3. **Round Robin.** Dati `P1 (burst 5)`, `P2 (burst 3)`, `P3 (burst 8)`, tutti con arrivo `0` e nell'ordine `P1, P2, P3`, con quanto `q = 2`, disegna la sequenza di esecuzione e calcola l'attesa media.

<details><summary>Soluzioni</summary>

1. **FCFS** (ordine di arrivo P1, P2, P3, P4):
   - Completamenti: `P1 = 8`, `P2 = 12`, `P3 = 21`, `P4 = 26`.
   - Turnaround (completamento − arrivo): `P1 = 8`, `P2 = 11`, `P3 = 19`, `P4 = 23`; media `= 61 / 4 = 15.25`.
   - Attesa (turnaround − burst): `P1 = 0`, `P2 = 7`, `P3 = 10`, `P4 = 18`; media `= 35 / 4 = 8.75`.

   **SJF non-preemptive:** a `t = 0` è pronto solo P1, che gira fino a `8`. A `t = 8` sono pronti P2(4), P3(9), P4(5): si sceglie P2, poi P4, poi P3.
   - Completamenti: `P1 = 8`, `P2 = 12`, `P4 = 17`, `P3 = 26`.
   - Turnaround: `P1 = 8`, `P2 = 11`, `P4 = 14`, `P3 = 24`; media `= 57 / 4 = 14.25`.
   - Attesa: `P1 = 0`, `P2 = 7`, `P4 = 9`, `P3 = 15`; media `= 31 / 4 = 7.75`.

2. **SRTF.** P1 parte a `0`; a `t = 1` arriva P2 (rem 4 < rem 7 di P1) e prelaziona; P2 gira fino a `5`; poi tra P1(7), P3(9), P4(5) vince P4, che gira `5→10`; poi P1 `10→17`; poi P3 `17→26`.
   - Completamenti: `P2 = 5`, `P4 = 10`, `P1 = 17`, `P3 = 26`.
   - Turnaround: `P1 = 17`, `P2 = 4`, `P3 = 24`, `P4 = 7`; media `= 52 / 4 = 13`.
   - Attesa: `P1 = 9`, `P2 = 0`, `P3 = 15`, `P4 = 2`; media `= 26 / 4 = 6.5`.
   SRTF batte sia FCFS (8.75) sia SJF non-preemptive (7.75) sull'attesa media, al prezzo di più prelazioni.

3. **Round Robin, q = 2.** Sequenza: `P1(0-2) P2(2-4) P3(4-6) P1(6-8) P2(8-9) P3(9-11) P1(11-12) P3(12-14) P3(14-16)`.
   - Completamenti: `P2 = 9`, `P1 = 12`, `P3 = 16`.
   - Turnaround: `P1 = 12`, `P2 = 9`, `P3 = 16`; media `= 37 / 3 ≈ 12.33`.
   - Attesa (turnaround − burst): `P1 = 7`, `P2 = 6`, `P3 = 8`; media `= 21 / 3 = 7`.
</details>
