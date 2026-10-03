---
day: 27
topic_id: db-er
title: "Modello relazionale e modellazione ER"
area: computer-science
course: "Basi di Dati / Sistemi Informativi"
grounded_in: null
adjacent: [db-norm, db-sql, is-bpmn]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun termine lasciato senza definizione."
---

# Modello relazionale e modellazione ER

> **Perché oggi:** ogni applicazione che tocchi ha un database sotto, e prima di scrivere una riga di SQL qualcuno deve aver deciso *quali tabelle esistono e come si collegano*. Quel disegno è la **modellazione dei dati**: si parte da uno schema concettuale (il diagramma **ER**) e lo si traduce in tabelle (il **modello relazionale**). È una delle domande più ricorrenti ai colloqui backend ("progettami lo schema per X") ed è il fondamento su cui poggiano query, normalizzazione e performance.

## Due livelli: prima il concetto, poi le tabelle
Progettare un database si fa in due passi distinti, ed è importante tenerli separati:

1. **Modello concettuale (ER):** descrivi il *dominio* — di quali cose parli e come sono legate — senza preoccuparti di come verranno salvate. È un disegno, fatto per ragionare con chi conosce il problema (il cliente, il product manager).
2. **Modello logico (relazionale):** traduci quel disegno in **tabelle** con righe e colonne, pronte per essere create in un database SQL.

Il diagramma ER è la mappa; le tabelle sono le strade asfaltate. Si disegna prima la mappa perché correggere un disegno costa niente, correggere uno schema già pieno di dati costa carissimo.

## Il modello ER (Entity-Relationship)
Il **modello ER**, introdotto da **Peter Chen** nel 1976, descrive il dominio con tre mattoni: **entità**, **attributi** e **relazioni**.

### Entità
Un'**entità** è una *classe di cose* del dominio che vuoi tracciare, della quale esistono molte istanze. Non è la singola cosa, ma il "tipo": `Utente`, `Segnalazione`, `Prodotto`. Una singola riga reale (l'utente Mario) è un'**istanza** di quell'entità. Si disegna come un rettangolo.

### Attributi
Un **attributo** è una proprietà che descrive un'entità: `Utente` ha `nome`, `email`, `data_registrazione`. Ogni attributo ha un **dominio**, cioè l'insieme dei valori ammessi (testo, numero intero, data, booleano…). Tra gli attributi se ne sceglie uno — o una combinazione — che fa da **identificatore**: distingue un'istanza da tutte le altre (vedi *chiave* più sotto).

### Relazioni (associazioni)
Una **relazione** è un legame *con significato* tra due (o più) entità: un `Utente` **effettua** una `Segnalazione`. Il verbo conta: descrive *come* le due cose sono collegate nel dominio. Si disegna come un rombo (o, nelle notazioni moderne, come una linea etichettata) che congiunge le due entità.

### Cardinalità
La **cardinalità** di una relazione dice *quante* istanze di un'entità possono essere legate a quante dell'altra. È l'informazione più importante del diagramma. Tre casi:

- **1:1 (uno a uno):** ogni istanza di A è legata ad al più una di B, e viceversa. Esempio: ogni `Utente` ha un solo `Profilo`, e ogni profilo appartiene a un solo utente.
- **1:N (uno a molti):** un'istanza di A può essere legata a molte di B, ma ogni B a una sola A. Esempio: un `Utente` effettua molte `Segnalazioni`, ma ogni segnalazione è di un solo utente. È il caso più comune.
- **N:M (molti a molti):** ogni A può essere legata a molte B e ogni B a molte A. Esempio: un `Ordine` contiene molti `Prodotti` e ogni prodotto compare in molti ordini.

### Chiavi (nel modello ER)
Una **chiave** è l'attributo (o l'insieme minimo di attributi) che identifica **univocamente** ogni istanza di un'entità. In `Utente` può essere `email` o un `id` numerico. È il concetto che, tradotto in tabella, diventa la **chiave primaria**.

### Generalizzazione (ereditarietà)
La **generalizzazione** collega un'entità *generale* (padre) a entità *specializzate* (figlie) che ne sono casi particolari e ne ereditano gli attributi. Esempio: l'entità generale `Utente` si specializza in `Cliente` e `Operatore`; entrambi hanno `nome` ed `email` (ereditati), ma `Operatore` aggiunge `reparto`. È l'equivalente, nei dati, dell'ereditarietà della programmazione a oggetti.

## Dal modello ER al modello relazionale
Il **modello relazionale** (ideato da **Edgar Codd**, 1970) organizza i dati in **tabelle**, dette anche *relazioni*. Vocabolario preciso:

- **Tabella (relazione):** una griglia di dati omogenei, es. la tabella `Utente`.
- **Tupla (riga):** un singolo record, cioè un'istanza dell'entità (un utente specifico).
- **Attributo (colonna):** un campo, con lo stesso significato per tutte le righe.
- **Dominio:** l'insieme dei valori ammessi per quella colonna (es. "intero positivo", "testo di max 255 caratteri").

La traduzione da ER a tabelle segue regole meccaniche:

- **Ogni entità** diventa **una tabella**; i suoi attributi diventano **colonne**.
- **La chiave** dell'entità diventa la **chiave primaria** della tabella.
- **Le relazioni** si traducono con le chiavi, ma *come* dipende dalla cardinalità (sotto).

### Chiave primaria e chiave esterna
- **Chiave primaria (Primary Key, PK):** una colonna (o combinazione) che identifica **univocamente** ogni riga e **non può essere nulla**. Garantisce che non esistano due righe indistinguibili e dà un "indirizzo" sicuro a cui puntare.
- **Chiave esterna (Foreign Key, FK):** una colonna che **punta** alla PK di un'altra tabella, materializzando una relazione. In `Segnalazione`, la colonna `utente_id` è una FK verso `Utente.id`: dice "questa segnalazione appartiene a quell'utente".

### Integrità referenziale
L'**integrità referenziale** è la garanzia, imposta dal database, che **ogni FK punti a una riga che esiste davvero**. Con questo vincolo attivo non puoi inserire una `Segnalazione` con `utente_id = 99` se l'utente 99 non esiste, né cancellare un utente lasciando segnalazioni "orfane" che puntano al vuoto (il DB o te lo impedisce, o cancella/aggiorna a cascata, a seconda della regola scelta). È ciò che tiene i collegamenti sempre coerenti.

### Come si traducono le cardinalità
- **1:N → una FK.** Si mette la FK **sul lato "molti"**. Esempio: `Segnalazione` (molti) riceve la colonna `utente_id` che punta a `Utente` (uno). Nessuna tabella in più.
- **1:1 → una FK** (su una delle due tabelle, di solito quella "debole"), marcata **UNIQUE** per impedire che due righe condividano lo stesso partner.
- **N:M → una terza tabella.** Una relazione molti-a-molti **non si può** rappresentare con una sola FK: serve una **tabella associativa** (detta anche *tabella ponte* o *di giunzione*). Questa tabella contiene **due FK**, una per ciascuna entità, e ogni sua riga rappresenta un singolo accoppiamento. Esempio: `Ordine` N:M `Prodotto` diventa una tabella `Riga_Ordine` con `ordine_id` (FK) e `prodotto_id` (FK) — e lì ci puoi anche appoggiare attributi *della relazione*, come la `quantita`. La sua chiave primaria è tipicamente la **coppia** `(ordine_id, prodotto_id)`.

## Schema

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 660 300" style="max-width:100%;height:auto;font-family:inherit" role="img" aria-label="Diagramma ER: l'entità Utente effettua Segnalazione, relazione uno a molti, tradotta in due tabelle con chiave primaria e chiave esterna">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6" fill="none" stroke="var(--accent)" stroke-width="1.5"/>
    </marker>
  </defs>
  <g font-size="12.5" fill="var(--ink)">
    <!-- livello ER -->
    <text x="20" y="24" font-size="11" fill="var(--muted)">Modello ER (concetto)</text>

    <rect x="20" y="36" width="150" height="50" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="95" y="66" text-anchor="middle" font-weight="700">Utente</text>

    <rect x="470" y="36" width="170" height="50" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="555" y="66" text-anchor="middle" font-weight="700">Segnalazione</text>

    <line x1="170" y1="61" x2="470" y2="61" stroke="var(--accent)" stroke-width="1.6" marker-end="url(#arr)"/>
    <text x="320" y="52" text-anchor="middle" font-size="11.5" fill="var(--muted)">effettua</text>
    <text x="196" y="76" text-anchor="middle" font-size="12" fill="var(--accent)" font-weight="700">1</text>
    <text x="448" y="76" text-anchor="middle" font-size="12" fill="var(--accent)" font-weight="700">N</text>

    <!-- freccia giù "si traduce in" -->
    <line x1="330" y1="100" x2="330" y2="128" stroke="var(--rule)" stroke-width="1.4" stroke-dasharray="4 3"/>
    <text x="345" y="118" font-size="11" fill="var(--muted)">si traduce in tabelle</text>

    <!-- livello relazionale -->
    <text x="20" y="152" font-size="11" fill="var(--muted)">Modello relazionale (tabelle)</text>

    <rect x="20" y="164" width="210" height="118" rx="10" fill="var(--card)" stroke="var(--rule)"/>
    <text x="125" y="186" text-anchor="middle" font-weight="700">Utente</text>
    <line x1="20" y1="196" x2="230" y2="196" stroke="var(--rule)"/>
    <text x="34" y="218"><tspan fill="var(--accent)" font-weight="700">id</tspan>  (PK)</text>
    <text x="34" y="242">nome</text>
    <text x="34" y="266">email  (UNIQUE)</text>

    <rect x="430" y="164" width="210" height="118" rx="10" fill="var(--card)" stroke="var(--rule)"/>
    <text x="535" y="186" text-anchor="middle" font-weight="700">Segnalazione</text>
    <line x1="430" y1="196" x2="640" y2="196" stroke="var(--rule)"/>
    <text x="444" y="218"><tspan fill="var(--accent)" font-weight="700">id</tspan>  (PK)</text>
    <text x="444" y="242"><tspan fill="var(--accent2)" font-weight="700">utente_id</tspan>  (FK)</text>
    <text x="444" y="266">testo</text>
  </g>
  <!-- FK -> PK sul lato "molti" -->
  <path d="M444,238 C330,238 300,218 230,218" fill="none" stroke="var(--accent)" stroke-width="1.6" marker-end="url(#arr)"/>
  <text x="332" y="212" text-anchor="middle" font-size="11" fill="var(--muted)">FK → PK</text>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">La relazione 1:N "effettua" diventa una FK <code>utente_id</code> sul lato molti (Segnalazione), che punta alla PK di Utente.</figcaption>
</figure>

## Esempi concreti
**Un gestionale di ticket (help desk).** Dominio: operatori che lavorano i ticket aperti dai clienti, con etichette per categorizzarli.

- Entità `Cliente` → tabella `cliente` (`id` PK, `nome`, `email` UNIQUE).
- Entità `Operatore` → tabella `operatore` (`id` PK, `nome`, `reparto`).
- Entità `Ticket` → tabella `ticket` (`id` PK, `titolo`, `stato`, `creato_il`, più le FK che seguono).
- Relazione **1:N** `Cliente —apre— Ticket`: FK `cliente_id` nella tabella `ticket`.
- Relazione **1:N** `Operatore —gestisce— Ticket`: FK `operatore_id` nella tabella `ticket` (può essere nulla finché il ticket non è assegnato).
- Relazione **N:M** `Ticket —ha— Etichetta` (un ticket ha più etichette, un'etichetta sta su più ticket): tabella associativa `ticket_etichetta` con FK `ticket_id` e FK `etichetta_id`, PK la coppia dei due.
- Possibile **generalizzazione**: `Utente` padre, specializzato in `Cliente` e `Operatore`, se condividono `nome`/`email`.

Con questo schema una domanda come "quanti ticket aperti per operatore?" è un semplice conteggio con un join sulle FK — ma puoi farla *solo* perché lo schema è stato disegnato bene prima.

## Notable use case
**Il carrello di un e-commerce** è il caso da manuale della relazione N:M fatta bene. Un `Ordine` contiene molti `Prodotti`, un `Prodotto` compare in molti ordini: molti-a-molti puro. La soluzione non è "una colonna con la lista dei prodotti" (impossibile da interrogare e da vincolare), ma una **tabella associativa** `riga_ordine` con `ordine_id`, `prodotto_id` **e** `quantita` + `prezzo_al_momento`. Due cose da notare: (1) gli attributi `quantita` e `prezzo_al_momento` appartengono alla *relazione*, non al prodotto né all'ordine presi da soli — ed è esattamente lì che la tabella ponte li ospita; (2) salvare il **prezzo al momento dell'acquisto** evita che modificare il listino riscriva la storia degli ordini passati. È il momento in cui la teoria ER smette di essere accademica e diventa una decisione di business.

## Fonti
- **Database System Concepts** (Silberschatz, Korth, Sudarshan) — db-book.com (capitoli su ER e modello relazionale, il riferimento classico)
- **Chen, "The Entity-Relationship Model"** (1976) — il paper originale che introduce la notazione ER
- **Vertabelo / dbdiagram.io** — vertabelo.com, dbdiagram.io (tutorial pratici di modellazione ER e strumenti per disegnare schemi)

## Concetti adiacenti
- `db-norm` — Normalizzazione (1NF→3NF/BCNF): come spezzare le tabelle per eliminare ridondanze e anomalie
- `db-sql` — SQL e join: come si interroga lo schema una volta creato (le FK diventano condizioni di join)
- `is-bpmn` — Modellazione dei processi (BPMN): disegnare il *comportamento* del dominio, complemento della modellazione dei *dati*

## Quiz (10 — tutte rispondibili dalla lezione)
1. Qual è la differenza tra **modello concettuale (ER)** e **modello logico (relazionale)**, e perché si disegna prima l'ER?
2. Cosa sono, nel modello ER, un'**entità**, un **attributo** e una **relazione**? Dai un esempio di ciascuno.
3. Cosa indica la **cardinalità** di una relazione? Elenca i tre casi con un esempio.
4. Nel modello relazionale, cosa sono una **tupla**, un **attributo** e il **dominio** di un attributo?
5. Cos'è una **chiave primaria** e quali due proprietà deve avere?
6. Cos'è una **chiave esterna** e come si collega alla chiave primaria?
7. Cosa garantisce l'**integrità referenziale**? Fai un esempio di cosa impedisce.
8. Come si traduce una relazione **1:N** in tabelle, e su quale lato si mette la FK?
9. Perché una relazione **N:M** non si può rappresentare con una sola FK, e qual è la soluzione corretta?
10. Cos'è la **generalizzazione** nel modello ER? Fai un esempio.

<details><summary>Risposte</summary>

1. L'**ER** descrive il *dominio* (quali cose esistono e come sono legate) senza dire come salvarle; il **relazionale** traduce quel disegno in **tabelle** concrete. Si disegna prima l'ER perché correggere un disegno costa nulla, mentre correggere uno schema già pieno di dati costa carissimo.
2. Un'**entità** è una classe di cose del dominio (es. `Utente`); un **attributo** è una sua proprietà (es. `email`); una **relazione** è un legame con significato tra entità (es. un utente *effettua* una segnalazione).
3. Indica **quante** istanze di un'entità possono essere legate a quante dell'altra. Casi: **1:1** (un utente ↔ un profilo), **1:N** (un utente → molte segnalazioni), **N:M** (molti ordini ↔ molti prodotti).
4. Una **tupla** è una riga, cioè un singolo record; un **attributo** è una colonna/campo con significato uguale per tutte le righe; il **dominio** è l'insieme dei valori ammessi per quella colonna (es. intero positivo, testo, data).
5. È una colonna (o combinazione) che identifica **univocamente** ogni riga; deve essere **unica** e **non nulla**.
6. È una colonna che **punta alla chiave primaria di un'altra tabella**, materializzando una relazione; il suo valore deve corrispondere a una PK esistente nella tabella puntata.
7. Garantisce che **ogni FK punti a una riga che esiste davvero**. Impedisce, per esempio, di inserire una segnalazione con `utente_id` di un utente inesistente, o di lasciare righe "orfane" cancellando l'utente puntato.
8. Si mette **una FK sul lato "molti"**, che punta alla PK del lato "uno". Esempio: `Segnalazione` (molti) riceve `utente_id` che punta a `Utente` (uno); non serve nessuna tabella in più.
9. Perché ogni lato può avere molti partner: una sola FK potrebbe memorizzare un solo riferimento, non molti. La soluzione è una **tabella associativa** (ponte) con **due FK**, una per entità; ogni riga è un accoppiamento, e lì si appoggiano eventuali attributi della relazione (es. `quantita`).
10. È il legame tra un'entità **generale** (padre) e entità **specializzate** (figlie) che ne ereditano gli attributi. Esempio: `Utente` si specializza in `Cliente` e `Operatore`, che ereditano `nome`/`email` e aggiungono i propri (es. `reparto` per l'operatore).
</details>
