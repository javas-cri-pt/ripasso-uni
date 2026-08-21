---
day: 17
topic_id: bp-financials
title: "Financial modeling — costi, break-even, unit economics, runway"
area: management
course: Business Planning / Imprenditorialità
grounded_in: "POLITO/secondo anno/Imprenditorialità e business planning"
adjacent: [acc-corpfin, bp-canvas, xc-pm-metrics]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Numeri solo quelli negli esempi del corpo."
---

# Financial modeling — costi, break-even, unit economics, runway

> **Perché oggi:** saper **leggere e costruire i numeri** di un business è ciò che ti distingue come Ingegnere Gestionale che punta a ruoli Product/business — non basta l'idea, devi mostrare che sta in piedi. Questi conti sono il linguaggio di un **business plan**, sono ciò che ti chiedono in un **colloquio da Product/business** ("qual è il tuo break-even? il tuo LTV/CAC?"), e li hai già affrontati costruendo il modello di MaiCare. Oggi li mettiamo in fila, con le formule e gli esempi numerici.

## Costi: fissi vs variabili, capex vs opex

Prima distinzione, per **volume**:

- **Costi fissi:** non cambiano al variare della quantità prodotta o venduta. Li paghi comunque, che tu venda 10 unità o 10.000. Esempi: **affitto** del locale, **stipendi** del team, il canone del software gestionale.
- **Costi variabili:** crescono col volume. Ogni unità in più ne aggiunge un pezzo. Esempi: **materie prime**, il **costo per unità** di produzione, le commissioni di pagamento su ogni transazione.

Seconda distinzione, per **natura della spesa** (è la coppia che confonde tutti):

- **CAPEX (Capital Expenditure = spesa in conto capitale):** spese in **beni durevoli** che restano nel tempo — attrezzature, macchinari, l'acquisto o lo sviluppo di un **asset** (per esempio costruire una piattaforma software da capitalizzare). È un **investimento**: spendi oggi qualcosa che ti servirà per anni.
- **OPEX (Operating Expenditure = spesa operativa):** spese **correnti** per far girare l'attività giorno per giorno — **affitti, cloud, stipendi, marketing**, licenze mensili. È il costo di **operare**, ricorrente.

**Perché la distinzione conta.** In contabilità un CAPEX non si "consuma" tutto subito: si mette a bilancio come asset e si spalma negli anni tramite l'**ammortamento** (la quota annuale con cui si scarica il costo di un bene durevole). Un OPEX invece va tutto a costo nell'esercizio in cui lo sostieni. E soprattutto conta per la **cassa**: un grosso CAPEX iniziale (compri i macchinari) ti svuota la cassa oggi anche se a conto economico pesa poco all'anno — ed è proprio la cassa che uccide le startup (vedi *runway* più sotto). Regola pratica per un modello: i **fissi/variabili** ti servono per il break-even; i **CAPEX/OPEX** ti servono per capire *quando* escono davvero i soldi.

## Break-even (punto di pareggio)

Il **break-even** (punto di pareggio) è il **volume di vendite** a cui i **ricavi coprono esattamente i costi**: profitto = 0. Sotto, sei in perdita; sopra, guadagni. È la prima domanda che chiunque ti fa: "quante ne devi vendere per non perdere soldi?".

Prima serve un concetto: il **margine di contribuzione** = **Prezzo unitario − Costo variabile unitario**. È **quanto ogni singola unità venduta "contribuisce"** a coprire i costi fissi (e, una volta coperti, a fare profitto). Si chiama così perché ogni unità porta quel margine "al fondo comune" che deve prima ripagare i fissi.

La formula del punto di pareggio, in unità:

**Break-even (unità) = Costi Fissi / (Prezzo unitario − Costo variabile unitario)**

cioè **Costi Fissi / Margine di contribuzione**. La logica: se ogni unità contribuisce con un margine, ti servono tante unità quante bastano a coprire i fissi con quel margine.

**Esempio numerico.** Costi fissi = **10.000 €**. Prezzo di vendita = **50 €**/unità. Costo variabile = **30 €**/unità.

- Margine di contribuzione = 50 − 30 = **20 €** per unità.
- Break-even = 10.000 / 20 = **500 unità**.

Vuol dire: vendendo **500 unità** incassi 500 × 50 = 25.000 € e spendi 10.000 (fissi) + 500 × 30 = 15.000 (variabili) = 25.000 €. Sei in pari. La **501ª unità** inizia a darti profitto (20 € ciascuna, il margine di contribuzione). Se il mercato non ti fa arrivare a 500 unità realistiche, il modello non regge: o alzi il prezzo, o abbassi il costo variabile, o tagli i fissi.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 460 320" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
   <line x1="60" y1="20" x2="60" y2="280" stroke="var(--rule)" stroke-width="1.5"/>
   <line x1="60" y1="280" x2="430" y2="280" stroke="var(--rule)" stroke-width="1.5"/>
   <text x="45" y="150" transform="rotate(-90 45 150)" fill="var(--muted)">€ (ricavi / costi)</text>
   <text x="245" y="307" fill="var(--muted)">Quantità (unità)</text>
  </g>
  <!-- zona perdita (sotto il break-even) e zona profitto (sopra) -->
  <path d="M60,280 L324,94 L324,206 L60,206 Z" fill="var(--rule)" opacity="0.18"/>
  <path d="M324,94 L430,20 L430,50 L324,94 Z" fill="var(--accent)" opacity="0.16"/>
  <!-- linea costi fissi (tratteggiata) -->
  <line x1="60" y1="206" x2="430" y2="206" stroke="var(--muted)" stroke-width="1.2" stroke-dasharray="4 3"/>
  <!-- retta costi totali: da costi fissi (60,206) sale -->
  <line x1="60" y1="206" x2="430" y2="50" stroke="var(--ink)" stroke-width="2"/>
  <!-- retta ricavi: da origine (60,280) sale più ripida -->
  <line x1="60" y1="280" x2="430" y2="20" stroke="var(--accent)" stroke-width="2.2"/>
  <!-- punto di pareggio -->
  <line x1="324" y1="94" x2="324" y2="280" stroke="var(--muted)" stroke-width="1" stroke-dasharray="3 3"/>
  <circle cx="324" cy="94" r="4.5" fill="var(--accent)"/>
  <g font-size="11" fill="var(--ink)">
   <text x="290" y="200" text-anchor="end" fill="var(--muted)">Costi fissi (10.000 €)</text>
   <text x="434" y="46" text-anchor="start">Ricavi</text>
   <text x="434" y="66" text-anchor="start" fill="var(--muted)">Costi totali</text>
   <text x="324" y="84" text-anchor="middle" fill="var(--accent)">Pareggio</text>
   <text x="324" y="293" text-anchor="middle" fill="var(--muted)">500</text>
   <text x="150" y="255" text-anchor="middle" fill="var(--muted)">PERDITA</text>
   <text x="385" y="110" text-anchor="middle" fill="var(--accent)">PROFITTO</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Grafico del break-even: la retta dei ricavi parte da 0 e sale più ripida; quella dei costi totali parte dai costi fissi (10.000 €) e sale più piano. Si incrociano nel punto di pareggio (500 unità): a sinistra perdita, a destra profitto.</figcaption>
</figure>

## Unit economics: CAC e LTV

Qui sta il cuore di un business **scalabile**. Le **unit economics** sono i conti fatti su **una singola unità** — di solito **un cliente**. Domanda: *quando prendo un cliente, ci guadagno o ci perdo?* Se ogni cliente ti fa perdere soldi, crescere ti fa perdere di più: la crescita non ti salva, ti affonda più in fretta.

Due numeri chiave:

- **CAC (Customer Acquisition Cost = costo di acquisizione cliente):** quanto spendi **in media per acquisire un cliente**. Si calcola come **(spesa in marketing + vendite) / numero di clienti acquisiti** in un periodo. Se in un mese spendi 3.000 € in marketing e vendite e porti a casa 100 clienti, il CAC è 30 €.
- **LTV (Lifetime Value = valore del ciclo di vita):** il **valore totale** che un cliente ti porta lungo **tutta la durata** della relazione. Formula semplice: **ricavo per periodo × margine × durata della relazione**. Il margine serve perché conta quanto *ti resta*, non quanto incassi lordo.

Due regole per leggere questi numeri:

1. **Regola d'oro: LTV/CAC ≥ 3.** Un cliente deve valere **almeno 3 volte** quello che hai speso per acquisirlo. Sotto 1 stai perdendo su ogni cliente; tra 1 e 3 sopravvivi ma stretto; ≥ 3 è considerato **sano** (c'è margine per coprire i costi fissi, gli errori e la crescita). Molto sopra 3 può addirittura significare che stai **investendo troppo poco** in acquisizione e lasci mercato sul tavolo.
2. **Payback period:** in **quanti mesi recuperi il CAC** con quello che il cliente ti paga. Se il CAC è 30 € e il cliente ti lascia ~7 €/mese di margine, il payback è circa 4–5 mesi. Più è corto, meno cassa devi anticipare per crescere.

**Esempio numerico.** CAC = **30 €**. Un cliente paga **10 €/mese** per **24 mesi**, con **margine 70%** (0,7).

- LTV = 10 × 24 × 0,7 = **168 €**.
- LTV/CAC = 168 / 30 ≈ **5,6**.

5,6 è **sano** (ben sopra 3): ogni euro speso per acquisire un cliente ne rende circa 5,6 di valore. Questo è il tipo di numero che fa dire a un investitore "il motore di crescita funziona, mettici più benzina (budget)".

## Burn rate e runway

- **Burn rate:** quanto **denaro bruci al mese**, cioè quanto la cassa scende ogni mese quando sei in perdita. In pratica **spese − ricavi** mensili (finché le spese superano i ricavi). Se spendi 15.000 €/mese e incassi 5.000 €/mese, il burn è **10.000 €/mese**.
- **Runway** (letteralmente "la pista di decollo"): per **quanti mesi** ti bastano i soldi che hai in cassa, al ritmo di burn attuale.

**Runway (mesi) = Cassa disponibile / Burn rate mensile**

**Esempio numerico.** Cassa = **120.000 €**. Burn = **10.000 €/mese**. Runway = 120.000 / 10.000 = **12 mesi**. Cioè: senza nuove entrate o nuovi soldi raccolti, tra 12 mesi la cassa è a zero.

**Perché è LA metrica che tiene sveglia una startup.** Puoi avere un prodotto amato e un LTV/CAC bellissimo, ma se finisci la cassa **chiudi**, punto. Il runway ti dice **quanto tempo hai** per raggiungere il break-even o per chiudere un round di finanziamento. Regola pratica del fundraising: **inizia a raccogliere quando ti restano ~6 mesi di runway**, perché raccogliere richiede mesi e non vuoi trattare con l'acqua alla gola (chi tratta col coltello alla gola ottiene condizioni pessime). Ridurre il burn (tagliare costi) **allunga il runway** e ti dà ossigeno.

## Le proiezioni (il modello)

Un **modello finanziario** è, concretamente, un **foglio di calcolo** con **proiezioni a 12–36 mesi**: mese per mese stimi i **ricavi** (unità × prezzo), i **costi** (fissi + variabili), e la **cassa** che ne risulta. È lì che vedi *quando* diventi break-even e *se e quando* finisci i soldi.

Due modi opposti di costruirlo:

- **Top-down:** parti dal **mercato totale** e stimi una **quota**. "Il mercato vale 1 miliardo, se ne prendo lo 0,5% faccio 5 milioni." Veloce ma **fragile**: quella quota è un desiderio, non una leva che controlli.
- **Bottom-up:** parti dalle tue **leve reali**. "Con 2 venditori chiudo ~20 clienti/mese, ognuno paga 50 €/mese → ecco i ricavi." Più **credibile**, perché ogni numero è agganciato a qualcosa che puoi davvero muovere (quanti clienti/mese, a che prezzo, con che tasso di abbandono). In un colloquio o davanti a un investitore, un modello **bottom-up** vince quasi sempre.

E gli **scenari:** non un solo numero, ma tre versioni — **pessimistico / base / ottimistico** — cambiando le ipotesi chiave (tasso di crescita, prezzo, churn). Mostra che conosci i rischi e che il business regge anche se le cose vanno peggio del previsto.

## Il ponte con la tua realtà

Questi non sono esercizi da manuale: sono **esattamente** le domande che un investitore o un capo ti fanno. "Qual è il tuo **break-even**?" "Com'è il tuo **LTV/CAC**?" "Quanto **runway** ti resta e quando raccogli?" Saper rispondere con numeri costruiti bene è ciò che ti fa sembrare qualcuno che **guida** il business, non che lo insegue.

Per una startup come MaiCare questi numeri sono **il linguaggio del fundraising**: il modello finanziario è il documento su cui l'investitore decide. Costruirlo **bottom-up**, con ipotesi difendibili e scenari, vale più di cento slide entusiaste. (Qui resto sul metodo: le cifre reali del tuo caso le metti tu, verificate — non me le invento.)

## Errori comuni

- **Confondere cassa e profitto.** Puoi essere in **utile** a conto economico e comunque **finire i soldi**: se fatturi ma incassi a 90 giorni mentre paghi fornitori e stipendi subito, la cassa va sotto zero prima che l'utile arrivi. È il classico "profittevole ma fallito". La cassa è la realtà, il profitto è un'opinione contabile.
- **Proiezioni "hockey-stick".** La curva piatta che di colpo schizza in alto come una mazza da hockey, senza una leva che spieghi lo scatto. Nessuno ci crede.
- **Ignorare il CAC.** Crescere tanto ma **in perdita su ogni cliente** (LTV/CAC < 1): più cresci, più bruci. La crescita non aggiusta un'unit economics rotta.
- **Dimenticare i costi variabili nel margine.** Calcolare il margine solo su prezzo meno costo "di produzione" saltando commissioni, spedizione, supporto: il margine reale è più basso e il break-even più lontano.
- **Modello top-down "campato per aria".** Lo 0,5% di un mercato enorme, senza dire *come* lo conquisti. Impressiona nessuno; costruisci bottom-up.

## Fonti

- **"Financial Intelligence for Entrepreneurs"** (Karen Berman, Joe Knight) — leggere e usare i numeri senza essere commercialisti: cassa vs profitto, margini, break-even.
- **a16z** e **First Round Review** — contenuti di riferimento su **unit economics**, **LTV/CAC**, burn e metriche delle startup (dai fondi/community che le hanno rese standard).
- **Strategyzer** — collega il **business model** ai numeri (dai creatori del Business Model Canvas).
- Un manuale di **corporate finance** (es. Brealey–Myers) per NPV, attualizzazione e **costo del capitale** — l'aggancio quantitativo più avanzato → vedi `acc-corpfin`.

## Concetti adiacenti

- `acc-corpfin` — Corporate finance: NPV, attualizzazione dei flussi e costo del capitale (il livello "avanzato" sotto queste proiezioni).
- `bp-canvas` — Business Model Canvas: descrive *com'è* il modello; qui verifichi che i **ricavi coprano i costi**.
- `bp-market` — Market analysis (TAM/SAM/SOM): dimensiona il mercato che alimenta il modello top-down.
- `xc-pm-metrics` — Metriche di prodotto (retention, churn, conversione): le leve operative che generano LTV e ricavi nel modello.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Qual è la differenza tra **costi fissi** e **costi variabili**? Fai un esempio di ciascuno.
2. Cosa significano **CAPEX** e **OPEX** (scrivi anche cosa vogliono dire le sigle) e qual è la differenza?
3. Cos'è il **break-even** (punto di pareggio) a parole?
4. Scrivi la **formula del break-even in unità** e spiega ogni termine.
5. Cos'è il **margine di contribuzione** e come si calcola?
6. Con costi fissi 10.000 €, prezzo 50 € e costo variabile 30 €, quanto vale il break-even in unità? Mostra il calcolo.
7. Cosa sono **CAC** e **LTV** (scrivi anche le sigle per esteso)? Qual è la **regola d'oro** sul loro rapporto?
8. Con CAC = 30 €, cliente che paga 10 €/mese per 24 mesi al 70% di margine: calcola **LTV** e **LTV/CAC** e di' se è sano.
9. Cos'è il **runway** e come si calcola? Con 120.000 € in cassa e burn di 10.000 €/mese, quanto vale?
10. Differenza tra proiezione **top-down** e **bottom-up**; e perché puoi essere in **profitto** ma restare **senza soldi** (cassa vs profitto)?

<details><summary>Risposte</summary>

1. I **costi fissi** non cambiano col volume prodotto/venduto: li paghi comunque (es. **affitto**, **stipendi**). I **costi variabili** crescono col volume, ogni unità in più ne aggiunge un pezzo (es. **materie prime**, costo per unità).
2. **CAPEX = Capital Expenditure** (spesa in conto capitale): spese in **beni durevoli/asset** che restano nel tempo (attrezzature, sviluppo di una piattaforma) — investimenti. **OPEX = Operating Expenditure** (spesa operativa): spese **correnti** per far girare l'attività (affitti, cloud, stipendi, marketing). Il CAPEX è un investimento che dura e si ammortizza negli anni; l'OPEX è un costo ricorrente dell'operare.
3. È il **volume di vendite a cui i ricavi coprono esattamente i costi**, cioè profitto = 0. Sotto sei in perdita, sopra guadagni.
4. **Break-even (unità) = Costi Fissi / (Prezzo unitario − Costo variabile unitario)**. *Costi fissi* = quelli che paghi comunque; *Prezzo unitario* = a quanto vendi una unità; *Costo variabile unitario* = quanto ti costa produrre una unità. Il denominatore è il margine di contribuzione: quante unità servono per coprire i fissi con quel margine.
5. Il **margine di contribuzione = Prezzo unitario − Costo variabile unitario**: quanto **ogni unità venduta contribuisce** a coprire i costi fissi (e poi a fare profitto).
6. Margine di contribuzione = 50 − 30 = **20 €**. Break-even = 10.000 / 20 = **500 unità**.
7. **CAC = Customer Acquisition Cost** (costo di acquisizione cliente): spesa marketing+vendite / numero clienti acquisiti. **LTV = Lifetime Value** (valore del ciclo di vita): valore totale che un cliente porta nella sua vita = ricavo per periodo × margine × durata. **Regola d'oro: LTV/CAC ≥ 3** (un cliente vale almeno 3 volte quello che spendi per acquisirlo).
8. LTV = 10 × 24 × 0,7 = **168 €**. LTV/CAC = 168 / 30 ≈ **5,6**. È **sano** perché ben sopra 3.
9. Il **runway** è per **quanti mesi** ti basta la cassa al ritmo di burn attuale. **Runway (mesi) = Cassa disponibile / Burn rate mensile** = 120.000 / 10.000 = **12 mesi**.
10. **Top-down:** parti dal mercato totale e stimi una quota (veloce ma fragile). **Bottom-up:** parti dalle leve reali (clienti/mese × prezzo), più credibile. Puoi essere in **profitto** e restare **senza soldi** perché **cassa ≠ profitto**: se incassi in ritardo (es. a 90 giorni) mentre paghi subito costi e stipendi, la cassa va a zero prima che l'utile si materializzi.
</details>
