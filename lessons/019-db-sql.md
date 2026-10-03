---
day: 19
topic_id: db-sql
title: "Basi di dati — modello relazionale, chiavi, SQL e join"
area: computer-science
course: Basi di Dati / Sistemi Informativi
grounded_in: "UNIBO/secondoAnno/Sistemi Informativi"
adjacent: [db-er, db-norm, db-tx, db-index, xc-sd-data]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun termine lasciato senza definizione."
---

# Basi di dati — modello relazionale, chiavi, SQL e join

> **Perché oggi:** il database è dove vivono i dati veri di quasi ogni applicazione. Saper modellare tabelle e scrivere una query con i **join** è chiesto praticamente a ogni colloquio tecnico, e lo usi già: **Taska** gira su SQLite, e all'uni hai fatto design di DB con SQL e trigger (Sistemi Informativi).

## Il modello relazionale (in una riga e poi per esteso)
Un **database relazionale** organizza i dati in **tabelle** (dette anche *relazioni*). Ogni tabella è una griglia: le **righe** (*tuple*) sono i singoli record, le **colonne** (*attributi*) sono i campi, ognuno con un **tipo** (intero, testo, data…). Idea chiave, dovuta a **Edgar Codd** (1970): non descrivi *come* trovare i dati, descrivi *che forma hanno* e li interroghi con un linguaggio dichiarativo (SQL). Il motore decide come eseguirla.

Esempio concreto (un mini-gestionale, la forma di Taska):

- tabella **Clienti**: `id`, `nome`, `citta`
- tabella **Ordini**: `id`, `cliente_id`, `importo`, `data`

## Le chiavi (il cuore del modello)
- **Chiave primaria (Primary Key, PK):** una colonna (o combinazione) che identifica **univocamente** ogni riga e non può essere vuota. In Clienti la PK è `id`. Serve a non avere due righe indistinguibili e a puntare a una riga in modo sicuro.
- **Chiave esterna (Foreign Key, FK):** una colonna che **punta** alla PK di un'altra tabella, creando un **collegamento**. In Ordini, `cliente_id` è una FK verso `Clienti.id`: dice "questo ordine appartiene a quel cliente". Il DB può imporre l'**integrità referenziale**: non puoi inserire un ordine con `cliente_id` che non esiste tra i clienti.
- **Chiave candidata / UNIQUE:** un'altra colonna che potrebbe fare da identificatore (es. l'email di un cliente): la marchi `UNIQUE` per vietare duplicati.

Perché le chiavi contano: sono ciò che ti permette di **spezzare** i dati in tabelle senza ripetizioni e poi **ricucirli** con i join. Mettere nome e città del cliente dentro ogni ordine (denormalizzato) sembra comodo ma duplica: se il cliente cambia città devi aggiornare mille righe. Con la FK il dato del cliente sta in **un** posto solo.

<svg viewBox="0 0 640 250" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="fk" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" fill="none" stroke="var(--accent)" stroke-width="1.5"/></marker></defs>
  <g font-size="12.5" fill="var(--ink)">
    <rect x="20" y="30" width="200" height="150" rx="10" fill="var(--card)" stroke="var(--rule)"/>
    <text x="120" y="52" text-anchor="middle" font-weight="700">Clienti</text>
    <line x1="20" y1="62" x2="220" y2="62" stroke="var(--rule)"/>
    <text x="34" y="84"><tspan fill="var(--accent)" font-weight="700">id</tspan>  (PK)</text>
    <text x="34" y="108">nome</text>
    <text x="34" y="132">citta</text>
    <text x="34" y="162" fill="var(--muted)" font-size="11">1 riga = 1 cliente</text>

    <rect x="420" y="30" width="200" height="170" rx="10" fill="var(--card)" stroke="var(--rule)"/>
    <text x="520" y="52" text-anchor="middle" font-weight="700">Ordini</text>
    <line x1="420" y1="62" x2="620" y2="62" stroke="var(--rule)"/>
    <text x="434" y="84"><tspan fill="var(--accent)" font-weight="700">id</tspan>  (PK)</text>
    <text x="434" y="108"><tspan fill="var(--accent2)" font-weight="700">cliente_id</tspan>  (FK)</text>
    <text x="434" y="132">importo</text>
    <text x="434" y="156">data</text>
    <text x="434" y="184" fill="var(--muted)" font-size="11">molti ordini per cliente</text>
  </g>
  <path d="M434,104 C320,104 300,84 224,84" fill="none" stroke="var(--accent)" stroke-width="1.6" marker-end="url(#fk)"/>
  <text x="322" y="80" text-anchor="middle" font-size="11.5" fill="var(--muted)">FK → PK (1 a molti)</text>
</svg>

## SQL: interrogare i dati
**SQL (Structured Query Language)** è il linguaggio standard per definire e interrogare i dati. È **dichiarativo**: dici *cosa* vuoi, non *come* ottenerlo. La query base è il `SELECT`:

```sql
SELECT nome, citta        -- quali colonne
FROM Clienti              -- da quale tabella
WHERE citta = 'Torino'    -- filtro sulle righe
ORDER BY nome;            -- ordinamento
```

I mattoni che tornano sempre:
- **`WHERE`** filtra le **righe** con una condizione (prima di raggruppare).
- **`ORDER BY`** ordina il risultato; **`LIMIT`** ne prende solo le prime N.
- **funzioni di aggregazione** — `COUNT` (conta), `SUM` (somma), `AVG` (media), `MIN`/`MAX` — collassano molte righe in **un** valore.
- **`GROUP BY`** aggrega **per gruppo**: "per ogni cliente, la somma degli ordini". Dopo il raggruppamento, **`HAVING`** filtra sui gruppi (mentre `WHERE` filtra sulle righe *prima* di aggregare — differenza classica da colloquio).

```sql
SELECT cliente_id, SUM(importo) AS totale
FROM Ordini
GROUP BY cliente_id
HAVING SUM(importo) > 1000;   -- solo i clienti che spendono >1000
```

## I JOIN (ricucire le tabelle)
Un **JOIN** combina righe di due tabelle **accostandole dove le chiavi coincidono** (tipicamente FK = PK). È l'operazione che paga il fatto di aver spezzato i dati.

```sql
SELECT c.nome, o.importo, o.data
FROM Clienti c
JOIN Ordini o ON o.cliente_id = c.id;   -- accosta cliente e suoi ordini
```

I tipi che devi conoscere:
- **INNER JOIN** (il `JOIN` semplice): tiene **solo** le righe che hanno corrispondenza in **entrambe** le tabelle. Clienti senza ordini spariscono dal risultato.
- **LEFT (OUTER) JOIN:** tiene **tutte** le righe della tabella di sinistra, e attacca i dati di destra dove ci sono; dove mancano, mette `NULL`. Serve per domande come "tutti i clienti, anche quelli **senza** ordini".
- **RIGHT JOIN:** simmetrico (tutte quelle di destra). Meno usato: spesso si riscrive come LEFT girando le tabelle.
- **`NULL`** = "valore assente/sconosciuto". Non è zero né stringa vuota: i confronti con `NULL` danno *sconosciuto*, per questo si testa con `IS NULL` / `IS NOT NULL`, non con `=`.

## Esempio concreto (roba tua)
In **Taska** (il tuo gestionale su SQLite) i dati hanno proprio questa forma relazionale: clienti, progetti, task e note in **tabelle collegate da chiavi**, e le viste dell'app sono **query con join** che ricuciono le entità legate tra loro. Nel progetto di **Sistemi Informativi** avevi anche scritto **trigger** — pezzi di SQL che il DB esegue **automaticamente** a un evento (es. dopo un `INSERT`) per tenere i dati coerenti.

## Completeness check (integrato da me)
Tre cose che il corso mette accanto a questo e vale la pena nominare:
- **Normalizzazione (1NF→3NF/BCNF):** l'insieme di regole per spezzare le tabelle così da **non ripetere** dati e non avere anomalie di aggiornamento. In pratica 3NF = "ogni colonna dipende dalla chiave, tutta la chiave, e nient'altro che la chiave".
- **Transazioni e ACID** (lezione adiacente): un gruppo di operazioni o va **tutto o niente**.
- **Indici:** una struttura extra (di solito un B-tree) che rende una ricerca su una colonna quasi istantanea invece di scorrere tutta la tabella — al prezzo di scritture un filo più lente e di spazio. È lo stesso trade-off dell'indice di un libro.

## Fonti
- **Use The Index, Luke** — use-the-index-luke.com (indici e performance SQL, pratico)
- **PostgreSQL Tutorial** — postgresqltutorial.com (SQL con esempi)
- **SQLBolt** — sqlbolt.com (esercizi SQL interattivi da colloquio)

## Concetti adiacenti
- `db-norm` — Normalizzazione (togliere le ridondanze in modo sistematico)
- `db-tx` — Transazioni e ACID (atomicità e coerenza)
- `db-index` — Indici e ottimizzazione query (perché una query è lenta)
- `xc-sd-data` — Dati a scala: sharding e replicazione (quando un DB solo non basta)

## Quiz (10 — tutte rispondibili dalla lezione)
1. Nel modello relazionale, cosa sono una **riga** e una **colonna** di una tabella?
2. Cos'è una **chiave primaria** e quali due proprietà deve avere?
3. Cos'è una **chiave esterna** e cosa garantisce l'**integrità referenziale**?
4. Perché spezzare i dati in più tabelle con le FK è meglio che ripetere il dato del cliente in ogni ordine?
5. Qual è la differenza tra `WHERE` e `HAVING`?
6. A cosa serve `GROUP BY` e con quali funzioni si usa di solito?
7. Differenza tra **INNER JOIN** e **LEFT JOIN**?
8. Perché per cercare i valori assenti si usa `IS NULL` e non `= NULL`?
9. Cos'è un **indice** e qual è il suo trade-off?
10. In una frase, cosa vuol dire che SQL è un linguaggio **dichiarativo**?

<details><summary>Risposte</summary>

1. Una **riga** (tupla) è un singolo record; una **colonna** (attributo) è un campo con un tipo, condiviso da tutte le righe.
2. Identifica **univocamente** ogni riga; deve essere **unica** e **non nulla** (non vuota).
3. È una colonna che **punta alla PK di un'altra tabella**; l'integrità referenziale garantisce che non puoi inserire una FK che punta a una riga inesistente.
4. Perché il dato del cliente sta in **un solo posto**: se cambia (es. la città), aggiorni una riga sola invece di mille, e non rischi copie incoerenti.
5. `WHERE` filtra le **righe prima** dell'aggregazione; `HAVING` filtra i **gruppi dopo** il `GROUP BY`.
6. Ad **aggregare per gruppo** (una riga di risultato per gruppo); si usa con `COUNT/SUM/AVG/MIN/MAX`.
7. **INNER** tiene solo le righe con corrispondenza in entrambe le tabelle; **LEFT** tiene **tutte** quelle di sinistra, mettendo `NULL` dove manca la corrispondenza a destra.
8. Perché un confronto con `NULL` dà *sconosciuto*, non vero/falso: `= NULL` non seleziona nulla. `IS NULL` è il test apposito per l'assenza di valore.
9. Una struttura extra (tipicamente B-tree) che rende quasi istantanea la ricerca su una colonna; trade-off: **scritture più lente e spazio in più**.
10. Dici **cosa** vuoi (che dati, con che filtri), non **come** ottenerli: il motore decide il piano di esecuzione.
</details>
