---
day: 6
topic_id: xc-pm-prioritization
title: "Product Management — prioritizzazione (RICE, MoSCoW, Kano, value/effort)"
area: cross-cutting
course: Product Management
grounded_in: null
adjacent: [xc-pm-metrics, xc-pm-discovery, pm-agile]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun acronimo lasciato senza definizione."
---

# Product Management — prioritizzazione

> **Perché oggi:** il ruolo di **Technical/Product PM** (Product Manager) è tra i tuoi target, e prioritizzare è letteralmente il lavoro quotidiano di un PM: ogni giorno decidi cosa costruire prima con risorse che non bastano mai. L'hai già fatto scegliendo cosa costruire per progetti come MaiCare/Samec, e questi framework ti danno un linguaggio condiviso e difendibile per farlo davanti a un team e a uno stakeholder (portatore di interesse: chi ha voce in capitolo — capo, cliente, investitore).

## PM in una riga (e perché la priorità è il suo mestiere)

Il **Product Manager (PM)** decide **cosa** costruire e **perché**, non **come**. Il "come" — architettura, tecnologie, implementazione — è dell'**engineering** (i team di sviluppo). Il PM sta all'incrocio fra tre mondi: gli **utenti** (di cosa hanno bisogno), il **business** (cosa porta valore all'azienda) e la **tecnologia** (cosa è fattibile). Non comanda nessuno di questi gruppi per gerarchia: guida per influenza, dati e una direzione chiara.

Attenzione a non confondere due ruoli con nomi simili:

- **Product Manager** — è responsabile del **prodotto**: capire il problema giusto, definire la strategia, decidere cosa entra e cosa no, misurare il valore consegnato a utente e business. Ragiona sul "quale problema risolviamo e vale la pena".
- **Project Manager** — è responsabile del **progetto** come esecuzione: **tempi, budget, scope** (l'insieme di lavoro concordato), coordinamento, rischi, scadenze. Ragiona sul "consegniamo in tempo, nei costi, con la qualità pattuita". Il suo mondo è quello del ciclo di vita di progetto (collegamento: **pm-lifecycle**).

Due parole chiave che tornano sempre:

- **Discovery** (scoperta) — la fase in cui capisci **il problema giusto** da risolvere: parli con gli utenti, formuli e testi ipotesi, decidi cosa vale la pena costruire. È il "stiamo costruendo la cosa giusta?".
- **Delivery** (consegna) — la fase in cui **costruisci bene** la cosa scelta: sviluppo, test, rilascio. È il "la stiamo costruendo bene?".

Il nocciolo del mestiere: **le risorse (persone, tempo, soldi) sono sempre meno delle idee.** Hai sempre più feature candidate di quante puoi realizzarne. Quindi devi scegliere, e devi farlo in modo **trasparente** (chiunque capisce perché) e **difendibile** (regge alla domanda "perché questa e non quella?"). I framework qui sotto servono esattamente a questo: trasformare un'opinione in un ragionamento che gli altri possono vedere e discutere.

## Il cuore: i framework di prioritizzazione

Nessun framework decide al posto tuo: ti costringe a rendere espliciti i criteri e a confrontare le opzioni sulla stessa scala. Vediamoli uno per uno, con come si calcola e un mini-esempio.

### RICE

**RICE** è un metodo di scoring (assegnazione di un punteggio) che nasce in Intercom. Sta per **Reach, Impact, Confidence, Effort** (Portata, Impatto, Confidenza, Sforzo). La formula:

> **RICE = (Reach × Impact × Confidence) / Effort**

Ogni fattore:

- **Reach (Portata)** — quante persone o eventi vengono impattati in un **periodo definito** (es. utenti al mese). Numero concreto, es. 2.000 utenti/mese.
- **Impact (Impatto)** — quanto la feature muove l'obiettivo **per singola persona**. Si usa una scala qualitativa convertita in numero, tipicamente: 3 = massiccio, 2 = alto, 1 = medio, 0.5 = basso, 0.25 = minimo.
- **Confidence (Confidenza)** — quanto sei **sicuro** delle tue stime di Reach e Impact, espressa in percentuale: 100% = alta (hai dati), 80% = media, 50% = bassa (è più un'intuizione). Serve a penalizzare le scommesse fondate su poco.
- **Effort (Sforzo)** — quanto costa realizzarla, di solito in **persona-mese** (il lavoro di una persona per un mese) o persona-settimane. È al denominatore: più costa, più abbassa il punteggio.

Il punteggio finale è un numero astratto ("impatto per unità di sforzo, pesato dalla confidenza") che serve **solo a confrontare** feature fra loro.

**Esempio numerico — due feature candidate:**

- **Feature A — "Login con Google"**: Reach = 2.000 utenti/mese, Impact = 1 (medio), Confidence = 80% (0.8), Effort = 2 persona-mese.
  RICE = (2.000 × 1 × 0.8) / 2 = **1.600 / 2 = 800**
- **Feature B — "Notifiche push"**: Reach = 8.000 utenti/mese, Impact = 0.5 (basso), Confidence = 100% (1.0), Effort = 4 persona-mese.
  RICE = (8.000 × 0.5 × 1.0) / 4 = **4.000 / 4 = 1.000**

**Vince la Feature B (1.000 > 800):** anche se ha impatto per utente più basso, la portata più ampia e la piena confidenza, divise per lo sforzo, la mettono davanti. Questo è il punto di RICE: rende il confronto un numero, non una discussione a colpi di opinioni.

### MoSCoW

**MoSCoW** serve a mettere d'accordo un team sullo **scope di un rilascio** (cosa entra in questa versione). Le maiuscole sono le categorie (le "o" minuscole sono solo per rendere pronunciabile la parola):

- **Must have (Deve esserci)** — indispensabile: senza, il rilascio non ha senso o non funziona. Se manca anche solo un "Must", il rilascio è fallito.
- **Should have (Dovrebbe esserci)** — importante ma non vitale: fa male non averlo, ma esiste un modo per cavarsela temporaneamente.
- **Could have (Potrebbe esserci)** — desiderabile: piacevole averlo, si include solo se avanzano tempo e risorse. È il primo a saltare quando stringono i tempi.
- **Won't have (this time) (Non ci sarà, per stavolta)** — esplicitamente **escluso da questo rilascio**. Non è "no per sempre": è "non ora". Metterlo per iscritto evita malintesi con gli stakeholder.

Utilità: è veloce, chiaro e ottimo per allineare le aspettative su cosa aspettarsi da una release.

### Value vs Effort (matrice 2×2)

Un metodo visivo: disegni due assi — **Valore** (verticale) e **Sforzo** (orizzontale) — e collochi ogni idea in uno dei quattro quadranti.

- **Quick wins (Vittorie rapide)** — **alto valore, basso sforzo**. Il quadrante d'oro: fai subito questi.
- **Big bets (Grandi scommesse)** — **alto valore, alto sforzo**. Valgono, ma richiedono impegno e pianificazione: si affrontano dopo aver validato con qualcosa di più leggero.
- **Fill-ins (Riempitivi)** — **basso valore, basso sforzo**. Cose da fare nei ritagli, quando c'è tempo libero.
- **Time sinks / Money pit (Perdite di tempo / Pozzi di soldi)** — **basso valore, alto sforzo**. Da **evitare**: costano molto e rendono poco.

**Regola pratica: parti dai quick wins.** Danno il massimo ritorno con il minimo investimento, e ti fanno guadagnare credibilità e dati per giustificare le big bets.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 420 360" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
   <line x1="60" y1="20" x2="60" y2="320" stroke="var(--rule)" stroke-width="1.5"/>
   <line x1="60" y1="320" x2="400" y2="320" stroke="var(--rule)" stroke-width="1.5"/>
   <line x1="230" y1="20" x2="230" y2="320" stroke="var(--rule)" stroke-width="1" stroke-dasharray="4 4"/>
   <line x1="60" y1="170" x2="400" y2="170" stroke="var(--rule)" stroke-width="1" stroke-dasharray="4 4"/>
   <text x="145" y="100" fill="var(--accent)">Quick wins</text>
   <text x="315" y="100">Big bets</text>
   <text x="145" y="250">Fill-ins</text>
   <text x="315" y="250" fill="var(--muted)">Time sinks</text>
   <text x="30" y="170" transform="rotate(-90 30 170)" fill="var(--muted)">Valore →</text>
   <text x="230" y="345" fill="var(--muted)">Sforzo →</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Matrice valore/sforzo: parti dai quick wins.</figcaption>
</figure>

### Kano model

Il **Kano model** (dal nome del ricercatore giapponese Noriaki Kano) non ordina le feature per punteggio: le **classifica per tipo di soddisfazione** che generano nell'utente. Tre categorie chiave:

- **Must-be (Basilari / date per scontate)** — l'utente le dà per scontate. Averle non entusiasma nessuno; **non** averle fa arrabbiare. Esempio: il freno in un'auto, il login che funziona. Sono il minimo per stare sul mercato.
- **Performance (Prestazionali / lineari)** — **più ce n'è, meglio è**. La soddisfazione cresce in proporzione: più velocità, più spazio, meno attese. Esempio: la durata della batteria di un telefono.
- **Delighters / Exciters (Deliziatori / Entusiasmanti)** — sorprese che l'utente non si aspetta e che lo **deliziano**. La loro assenza non disturba (nessuno le chiedeva), ma la loro presenza crea un "wow". Esempio: una funzione geniale che i concorrenti non hanno.

Dinamica temporale importante: **col tempo i delighter diventano must-be.** La fotocamera sullo smartphone era un delighter, oggi è un must-be; se manca, il telefono è "rotto". Morale per un PM: non puoi vivere di soli delighter, e ciò che oggi stupisce domani sarà preteso.

### WSJF (cenno)

**WSJF** sta per **Weighted Shortest Job First** (letteralmente "prima il lavoro più breve, pesato"). Viene da **SAFe** (Scaled Agile Framework, un framework per applicare l'Agile a organizzazioni grandi). La formula:

> **WSJF = Cost of Delay / Job Size**

- **Cost of Delay (Costo del ritardo)** — quanto valore **perdi ogni unità di tempo** in cui NON hai quella feature (valore per l'utente/business, urgenza temporale, riduzione del rischio).
- **Job Size (Dimensione del lavoro)** — quanto è grande il lavoro (una stima di sforzo/durata).

Fai per primo chi ha **WSJF più alto**: cioè chi dà **più valore per unità di tempo**. La logica è: se due cose valgono uguale ma una costa metà, fai prima quella che libera valore più in fretta.

## Le metriche che guidano la priorità

Prioritizzi meglio se sai **quale numero vuoi muovere**. Qui entrano le metriche (approfondite in **xc-pm-metrics**).

- **North Star Metric (Metrica Stella Polare)** — **l'unica metrica** che meglio cattura il **valore consegnato all'utente** e attorno a cui tutto il team si allinea. Esempi noti: per Airbnb "notti prenotate", per Spotify "tempo di ascolto". Serve da bussola: una feature che non muove (direttamente o a monte) la North Star probabilmente non è prioritaria.
- **AARRR** — un framework a imbuto per capire il percorso dell'utente, soprannominato **"pirate funnel"** ("imbuto dei pirati", perché "AARRR" suona come il verso dei pirati). Le cinque tappe:
  - **Acquisition (Acquisizione)** — come le persone ti trovano e arrivano al prodotto.
  - **Activation (Attivazione)** — la prima esperienza di valore: l'utente capisce a cosa serve e prova quel primo "momento aha".
  - **Retention (Retention / Ritenzione)** — le persone **tornano** e continuano a usare il prodotto nel tempo, invece di sparire dopo la prima volta. È spesso la metrica più predittiva della salute di un prodotto.
  - **Referral (Passaparola)** — gli utenti soddisfatti **portano altri utenti** (inviti, consigli).
  - **Revenue (Ricavi)** — l'utente genera fatturato (paga, si abbona, converte).

L'idea di fondo: identifica lo **stadio dell'imbuto che perde di più** e prioritizza le feature che lo sistemano. Se acquisisci tanti utenti ma la retention è pessima, non serve spingere ancora l'acquisition — stai riempiendo un secchio bucato.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 420 320" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <polygon points="40,30 380,30 336,86 84,86" fill="var(--card)" stroke="var(--rule)" stroke-width="1.5"/>
    <polygon points="84,90 336,90 308,146 112,146" fill="var(--card)" stroke="var(--rule)" stroke-width="1.5"/>
    <polygon points="112,150 308,150 280,206 140,206" fill="var(--card)" stroke="var(--accent)" stroke-width="1.5"/>
    <polygon points="140,210 280,210 252,266 168,266" fill="var(--card)" stroke="var(--rule)" stroke-width="1.5"/>
    <polygon points="168,270 252,270 224,314 196,314" fill="var(--card)" stroke="var(--rule)" stroke-width="1.5"/>
    <text x="210" y="62">Acquisition</text>
    <text x="210" y="122">Activation</text>
    <text x="210" y="182" fill="var(--accent)">Retention</text>
    <text x="210" y="242">Referral</text>
    <text x="210" y="296" font-size="11">Revenue</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Il funnel AARRR (pirate funnel): 5 stadi dall'arrivo al ricavo.</figcaption>
</figure>

## Tool reali

Dove si fa davvero questo lavoro, per nome:

- **Backlog e issue** (elenco di lavoro da fare, ticket): **Jira**, **Linear**. Ci tieni le feature/task e spesso ci calcoli campi custom (es. un punteggio RICE).
- **Prioritizzazione e roadmap** (piano nel tempo): **Productboard**, **Aha!**. Nati apposta per raccogliere feedback, assegnare punteggi e costruire la roadmap.
- **PRD** (Product Requirements Document, il documento che descrive cosa e perché di una feature): **Notion**, **Confluence**.
- **Metriche e funnel** (analisi comportamento utenti): **Amplitude**, **Mixpanel**. Ci misuri activation, retention e l'imbuto AARRR.
- **Scoring RICE fatto a mano**: un semplice foglio **Google Sheets** o **Excel** con le colonne Reach, Impact, Confidence, Effort e la formula. Spessissimo la prima versione di un scoring vive proprio qui.

## Esempio concreto (roba tua)

Per **MaiCare** ho dovuto scegliere cosa costruire prima con risorse limitate: un caso classico da **matrice value/effort** e da **RICE**, dove i "quick win" (alto valore, basso sforzo) vanno per primi per validare in fretta e capire se stavo risolvendo il problema giusto prima di investire nelle scommesse più grandi. Il valore dei framework non è stato il numero in sé, ma avere un criterio esplicito da mostrare e discutere invece di decidere "a sensazione".

## Notable use cases (grandi aziende)

- **RICE nasce in Intercom** (azienda di customer messaging): l'hanno creato per prioritizzare la propria roadmap e poi pubblicato sul loro blog, diventando uno standard di settore. È un fatto pubblico e noto.
- **MoSCoW** è uno standard diffuso nei progetti **Agile** (metodologie di sviluppo iterativo e incrementale) e in particolare nel metodo DSDM da cui proviene; si usa per negoziare lo scope di un rilascio.
- **Kano model** è largamente usato in **product management e UX** (User Experience, l'esperienza d'uso) per capire quali feature soddisfano davvero gli utenti e distinguere il basilare dal deliziante.

(Non aggiungo dettagli proprietari o numeri interni che non sono pubblici.)

## Fonti

- **Intercom — "RICE: Simple prioritization for product managers"** (intercom.com) — l'articolo originale che ha introdotto RICE.
- **Reforge** (reforge.com) — corsi e materiali avanzati di product/growth, tra cui prioritizzazione e metriche.
- **"Inspired" di Marty Cagan** (SVPG) — il libro di riferimento su come funzionano i grandi team di prodotto (discovery, ruolo del PM).
- **Lenny's Newsletter** (lennysnewsletter.com) — casi pratici e framework di product management molto usati nel settore.

## Concetti adiacenti

- **xc-pm-metrics** — le metriche che misurano il valore (North Star, AARRR, retention, funnel): sono l'input che alimenta la prioritizzazione.
- **xc-pm-discovery** — capire il problema giusto prima di costruire: la fase che genera le idee poi da prioritizzare.
- **xc-pm-experiment** — validare le ipotesi con esperimenti (es. A/B test) per aumentare la Confidence delle stime.
- **pm-agile** — sviluppo iterativo e incrementale, backlog e rilasci: il contesto in cui MoSCoW e WSJF vivono naturalmente.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Qual è la differenza tra Product Manager e Project Manager?
2. Scrivi la formula di RICE e spiega cosa significano i quattro fattori.
3. Nell'esempio del corpo, calcola il RICE della Feature A ("Login con Google") e della Feature B ("Notifiche push"): quale vince?
4. Quali sono le quattro categorie di MoSCoW e cosa significa ciascuna?
5. Nella matrice value/effort, come si chiamano i quattro quadranti e da quale conviene partire?
6. Quali sono le tre categorie del Kano model? Cosa succede ai delighter col tempo?
7. Cos'è la North Star Metric?
8. Cosa significa l'acronimo AARRR e cosa vuol dire "retention"?
9. Scrivi la formula del WSJF e spiega cosa privilegia.
10. Qual è la differenza tra discovery e delivery?

<details><summary>Risposte</summary>

1. **Product Manager** è responsabile del prodotto: decide **cosa** costruire e **perché** (problema giusto, strategia, valore per utente e business). **Project Manager** è responsabile dell'esecuzione del progetto: **tempi, budget, scope**, coordinamento e scadenze. In breve: il primo sceglie la direzione, il secondo consegna nei vincoli.

2. **RICE = (Reach × Impact × Confidence) / Effort.** **Reach** = quante persone/eventi impattati in un periodo definito; **Impact** = quanto muove l'obiettivo per persona (scala es. 0.25–3); **Confidence** = quanto sei sicuro delle stime, in % ; **Effort** = costo in persona-mese/settimane (al denominatore).

3. **Feature A:** (2.000 × 1 × 0.8) / 2 = 1.600 / 2 = **800**. **Feature B:** (8.000 × 0.5 × 1.0) / 4 = 4.000 / 4 = **1.000**. **Vince la Feature B** (1.000 > 800).

4. **Must have** = indispensabile (senza, il rilascio fallisce); **Should have** = importante ma non vitale (c'è un ripiego temporaneo); **Could have** = desiderabile, solo se avanzano tempo/risorse; **Won't have (this time)** = esplicitamente escluso da questo rilascio (non per sempre, solo non ora).

5. I quattro quadranti: **Quick wins** (alto valore/basso sforzo), **Big bets** (alto valore/alto sforzo), **Fill-ins** (basso valore/basso sforzo), **Time sinks / Money pit** (basso valore/alto sforzo). Si parte dai **quick wins**.

6. **Must-be** (date per scontate: la loro assenza fa arrabbiare, la presenza non entusiasma), **Performance** (più ce n'è meglio è, soddisfazione proporzionale), **Delighters/Exciters** (sorprese che deliziano; la loro assenza non disturba). Col tempo **i delighter diventano must-be** (es. la fotocamera sullo smartphone).

7. La **North Star Metric** è l'**unica metrica** che meglio cattura il **valore consegnato all'utente**, attorno a cui il team si allinea; funge da bussola per decidere cosa è prioritario.

8. **AARRR** = **Acquisition, Activation, Retention, Referral, Revenue** (il "pirate funnel"). **Retention** = le persone **tornano** e continuano a usare il prodotto nel tempo, invece di abbandonarlo dopo la prima volta.

9. **WSJF = Cost of Delay / Job Size** (Weighted Shortest Job First, da SAFe). Privilegia chi dà **più valore per unità di tempo**: si fa per primo chi ha WSJF più alto.

10. **Discovery** = capire il **problema giusto** da risolvere (parlare con gli utenti, testare ipotesi): "stiamo costruendo la cosa giusta?". **Delivery** = **costruire bene** la cosa scelta (sviluppo, test, rilascio): "la stiamo costruendo bene?".

</details>
