---
day: 31
topic_id: ml-basics
title: "ML: apprendimento supervisionato vs non supervisionato, train/test"
area: computer-science
course: "Laboratorio IA e Machine Learning"
grounded_in: null
adjacent: [ml-eval, ml-nn, ml-llm]
completeness_checked: true
quiz_count: 10
---

# ML: apprendimento supervisionato vs non supervisionato, train/test

> **Perché oggi:** sotto le reti neurali e gli LLM c'è una grammatica di base del machine learning che conviene avere ben salda: che differenza c'è tra imparare "con le risposte" e "senza", e perché un modello va **sempre** misurato su dati che non ha mai visto. È la prima cosa che ti chiedono a un colloquio tecnico su AI ("spiegami supervisionato vs non supervisionato"), ed è l'errore numero uno dei principianti: valutare un modello sugli stessi dati con cui l'hanno allenato e stupirsi che in produzione non funzioni.

## Cos'è il machine learning (e perché è diverso dal programmare)
Nella programmazione classica tu scrivi le **regole** e il computer le applica ai dati per produrre un risultato. Nel **machine learning (ML, apprendimento automatico)** ribalti la cosa: dai al computer i **dati** e i **risultati attesi**, e lui ricava da solo le regole. Il prodotto di questo processo è un **modello**, cioè una funzione che ha "imparato" una relazione dai dati e che potrai usare su casi nuovi.

Due termini che userò di continuo:
- **Feature (variabile, attributo):** una delle caratteristiche in ingresso che descrivono un esempio. Per una casa: metri quadri, numero di stanze, zona. Per una email: numero di link, presenza di certe parole.
- **Label (etichetta, target):** la risposta corretta associata a un esempio, cioè ciò che vorremmo predire (il prezzo della casa, "spam" / "non spam").

Un **dataset** è una tabella: ogni riga è un **esempio**, le colonne sono le feature, e (se ci sono) una colonna è la label.

## Apprendimento supervisionato
Nell'**apprendimento supervisionato** ogni esempio di allenamento ha la sua **label**: impari "con le risposte accanto". Il modello osserva molte coppie (feature → label) e cerca la funzione che, date le feature, azzecca la label. Si divide in due famiglie a seconda di cosa predici:
- **Classificazione:** la label è una **categoria** (un insieme finito di classi). Esempi: spam / non spam (binaria), riconoscere la cifra scritta a mano 0-9 (multiclasse). L'output è "a quale classe appartiene".
- **Regressione:** la label è un **numero continuo**. Esempi: prevedere il prezzo di una casa, la temperatura di domani, le vendite del mese. L'output è una quantità.

Il modo di capire se è l'uno o l'altro: **la risposta è una categoria o un numero?** "Che specie di fiore è" → classificazione; "quanto costerà" → regressione.

## Apprendimento non supervisionato
Nell'**apprendimento non supervisionato** gli esempi **non hanno label**: hai solo le feature e vuoi scoprire **struttura nascosta** nei dati. Nessuno ti dice qual è la risposta giusta. I due compiti tipici:
- **Clustering (raggruppamento):** dividere gli esempi in **gruppi** (cluster) di elementi simili tra loro e diversi dagli altri. Esempio: segmentare i clienti in profili di acquisto senza averli etichettati prima. L'algoritmo più noto è **k-means**: scegli `k` (quanti gruppi vuoi), parti da `k` centri a caso e ripeti due passi finché si stabilizza, (1) assegna ogni punto al centro più vicino, (2) sposta ogni centro nella media dei punti che gli sono stati assegnati.
- **Riduzione di dimensionalità:** comprimere tante feature in poche, mantenendo l'informazione importante, per visualizzare i dati o toglierne il rumore. La tecnica classica è la **PCA (Principal Component Analysis, analisi delle componenti principali)**, che trova le direzioni lungo cui i dati variano di più.

Esistono anche sfumature intermedie: nel **semi-supervisionato** solo una parte degli esempi è etichettata (etichettare costa), e nell'**apprendimento per rinforzo (reinforcement learning)** un agente impara per tentativi massimizzando una ricompensa. Oggi mi concentro sui due grandi paradigmi, supervisionato e non supervisionato.

## Train, validation e test: perché si dividono i dati
Un modello non deve **memorizzare** gli esempi visti: deve **generalizzare**, cioè funzionare su dati nuovi. Per misurarlo onestamente si divide il dataset in parti, e l'unica regola d'oro è che **il test non deve mai aver toccato l'allenamento**.
- **Training set (addestramento):** la fetta più grande (es. 60-80%), quella con cui il modello impara i suoi parametri.
- **Validation set (convalida):** una fetta usata **durante** lo sviluppo per scegliere tra configurazioni diverse (quale algoritmo, quali **iperparametri**, cioè le manopole che imposti tu prima di allenare, come `k` o la profondità di un albero). Serve a non "barare" guardando il test.
- **Test set (verifica):** una fetta che si tocca **una sola volta, alla fine**, per stimare come il modello si comporterà nel mondo reale. È il tuo esame, e si fa una volta.

Il motivo per cui questa separazione è sacra è il **data leakage (fuga di informazione):** quando informazione del test filtra nell'allenamento, i risultati sembrano ottimi ma sono gonfiati. L'errore tipico: **normalizzare o standardizzare** le feature (es. riscalarle) calcolando media e scala **su tutto il dataset** prima di dividerlo. Così il modello "sbircia" statistiche che includono il test. Il modo corretto: calcolare le trasformazioni **solo sul training** e poi applicarle a validation e test.

## Overfitting e underfitting (l'intuizione)
- **Overfitting (sovradattamento):** il modello impara "a memoria" il training, compreso il rumore, e va **benissimo sul training ma male sui dati nuovi**. È lo studente che ripete a pappagallo gli esercizi visti ma crolla su una variante.
- **Underfitting (sottoadattamento):** il modello è troppo semplice per cogliere la relazione e va **male ovunque**, anche sul training.

Il sintomo dell'overfitting è proprio un **divario** tra prestazione alta sul training e bassa sul test: per questo serve il test separato, per vederlo. Come si misura questo divario, e come si quantificano le prestazioni con metriche come accuracy, precision e recall, è il tema della lezione `ml-eval`.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 680 270" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="170" y="20" font-weight="700">Supervisionato: con label</text>
    <rect x="30" y="34" width="120" height="30" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="90" y="53" font-size="11">feature</text>
    <rect x="30" y="68" width="120" height="30" rx="6" fill="var(--card2)" stroke="var(--accent)" stroke-width="1.6"/><text x="90" y="87" font-size="11">label (risposta)</text>
    <rect x="200" y="50" width="80" height="34" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="240" y="71" font-size="11">modello</text>
    <rect x="320" y="50" width="96" height="34" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="368" y="66" font-size="10.5">predice</text><text x="368" y="79" font-size="10.5" fill="var(--muted)">classe / numero</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none" marker-end="url(#m31)">
    <path d="M150,49 L198,63"/><path d="M150,83 L198,71"/><path d="M280,67 L318,67"/>
  </g>
  <defs><marker id="m31" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <line x1="450" y1="20" x2="450" y2="250" stroke="var(--rule)"/>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="565" y="20" font-weight="700">Non supervisionato: clustering</text>
    <circle cx="505" cy="70" r="5" fill="var(--accent)"/><circle cx="520" cy="85" r="5" fill="var(--accent)"/><circle cx="498" cy="92" r="5" fill="var(--accent)"/>
    <circle cx="620" cy="130" r="5" fill="var(--good)"/><circle cx="635" cy="145" r="5" fill="var(--good)"/><circle cx="615" cy="150" r="5" fill="var(--good)"/>
    <ellipse cx="508" cy="82" rx="30" ry="26" fill="none" stroke="var(--muted)" stroke-dasharray="4 3"/>
    <ellipse cx="623" cy="142" rx="30" ry="26" fill="none" stroke="var(--muted)" stroke-dasharray="4 3"/>
    <text x="508" y="128" font-size="10.5" fill="var(--muted)">gruppo 1</text>
    <text x="623" y="188" font-size="10.5" fill="var(--muted)">gruppo 2</text>
    <text x="565" y="230" font-size="10" fill="var(--muted)">nessuna label: raggruppa per similarità</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">A sinistra l'apprendimento supervisionato: il modello impara dalle coppie feature + label e poi predice una classe (classificazione) o un numero (regressione). A destra il non supervisionato: senza label, l'algoritmo trova gruppi di punti simili (clustering).</figcaption>
</figure>

## Esempi concreti
- **Filtro antispam (classificazione supervisionata):** dataset di email già marcate "spam" / "non spam" (le label); feature come parole presenti, numero di link, mittente. Il modello impara a classificare le nuove.
- **Prezzo di un immobile (regressione supervisionata):** feature metri quadri, stanze, zona; label il prezzo storico di vendita. Il modello predice un numero per una casa nuova.
- **Segmentazione clienti (clustering non supervisionato):** nessuno ha etichettato i clienti; k-means li raggruppa per comportamento d'acquisto e poi il marketing dà un nome ai gruppi scoperti.
- **La trappola del leakage:** un principiante standardizza tutte le feature sull'intero dataset, poi divide e ottiene il 99% in test. In produzione crolla: aveva fatto entrare nel modello statistiche calcolate anche sui dati di test.

## Notable use case
- **Netflix e i sistemi di raccomandazione** combinano segnali supervisionati (hai guardato / valutato) e tecniche non supervisionate per raggruppare contenuti e utenti simili.
- **Rilevamento frodi** nelle carte di credito: spesso impostato come classificazione supervisionata su transazioni storiche etichettate "frode / legittima", con il problema tipico delle classi **sbilanciate** (le frodi sono rarissime), tema che riprende `ml-eval`.
- **scikit-learn**, la libreria Python di riferimento per il ML classico, organizza proprio le sue API attorno a questi concetti: `fit` (allena sul training), `predict` (applica a dati nuovi), `train_test_split` (divide i dati).

## Fonti
- **Google — Machine Learning Crash Course** (developers.google.com/machine-learning/crash-course)
- **scikit-learn — User Guide** (scikit-learn.org/stable/user_guide.html), in particolare `cross_validation` e `preprocessing`
- **James, Witten, Hastie, Tibshirani — An Introduction to Statistical Learning (ISLR)**, capitoli su apprendimento supervisionato/non supervisionato (statlearning.com)

## Concetti adiacenti
- `ml-eval` — come si misura un modello (accuracy, precision/recall) e come si vede l'overfitting con numeri
- `ml-nn` — le reti neurali, un tipo di modello (quasi sempre supervisionato) costruito su questi stessi principi
- `ml-llm` — gli LLM nascono da un pre-addestramento **auto-supervisionato** (il modello impara a prevedere parti di testo mancanti, ricavando da solo le "risposte" dal testo stesso, senza etichette umane) su enormi quantità di testo

## Quiz (10 — tutte rispondibili dalla lezione)
1. In una frase, qual è la differenza tra programmazione classica e machine learning (chi produce le regole)?
2. Cosa sono una **feature** e una **label**, con un esempio?
3. Cosa distingue l'apprendimento **supervisionato** dal **non supervisionato**?
4. Dentro il supervisionato, qual è la differenza tra **classificazione** e **regressione**? Fai un esempio per ciascuna.
5. Cos'è il **clustering** e quali due passi ripete l'algoritmo **k-means**?
6. A cosa serve la **riduzione di dimensionalità** e come si chiama la tecnica classica?
7. A cosa servono **training**, **validation** e **test set**, e qual è la regola d'oro che li lega?
8. Cos'è il **data leakage** e perché standardizzare le feature su tutto il dataset prima di dividerlo lo provoca?
9. Cos'è l'**overfitting** e qual è il suo sintomo misurabile?
10. Cosa significa **underfitting** e in cosa è diverso dall'overfitting?

<details><summary>Risposte</summary>

1. Nella programmazione classica **scrivi tu le regole** e le applichi ai dati; nel ML dai dati e risposte attese e il computer **ricava le regole** da solo (produce un modello).
2. Una **feature** è una caratteristica in ingresso che descrive un esempio (es. i metri quadri di una casa); una **label** è la risposta corretta da predire (es. il prezzo). 
3. Nel **supervisionato** ogni esempio ha una **label** (impari con le risposte); nel **non supervisionato** non ci sono label e cerchi **struttura nascosta** nei dati.
4. **Classificazione:** la label è una **categoria** (es. spam / non spam). **Regressione:** la label è un **numero continuo** (es. il prezzo di una casa).
5. Il **clustering** divide gli esempi in gruppi di elementi simili senza label. **k-means** ripete: (1) assegna ogni punto al centro più vicino; (2) sposta ogni centro nella media dei suoi punti; fino a stabilizzarsi.
6. Serve a **comprimere molte feature in poche** mantenendo l'informazione utile (per visualizzare o togliere rumore). La tecnica classica è la **PCA**.
7. **Training** = il modello impara i parametri; **validation** = scegli algoritmo/iperparametri durante lo sviluppo; **test** = stima finale su dati mai visti, usata una sola volta. Regola d'oro: **il test non deve mai aver toccato l'allenamento**.
8. È la **fuga di informazione** dal test verso l'allenamento: i risultati sembrano ottimi ma sono gonfiati. Standardizzare su tutto il dataset calcola media/scala usando **anche il test**, così il modello "sbircia" statistiche che non dovrebbe conoscere. Corretto: calcolarle solo sul training.
9. L'**overfitting** è imparare a memoria il training (incluso il rumore). Sintomo misurabile: prestazione **alta sul training ma bassa sul test** (il divario tra i due).
10. L'**underfitting** è un modello troppo semplice che va **male ovunque**, anche sul training; l'overfitting invece va bene sul training e male sul test.
</details>

## Esercizi
1. **Supervisionato o non supervisionato?** Classifica ciascuno di questi scenari e, se supervisionato, di' se è classificazione o regressione: (a) prevedere quanti caffè venderà un bar domani; (b) raggruppare 10.000 articoli di news per argomento senza categorie predefinite; (c) riconoscere se una radiografia mostra una frattura (sì/no) partendo da immagini già diagnosticate; (d) comprimere un dataset con 300 colonne in 2 per disegnarlo su un grafico.
2. **Split e valutazione con scikit-learn.** Scrivi lo pseudocodice/codice Python che: divide `X, y` in train e test (80/20), standardizza le feature nel modo corretto (senza leakage), allena un modello e ne stampa l'accuratezza sul test.
3. **k-means a mano fino a convergenza.** Punti su una retta: `2, 4, 10, 12`. `k = 2`, centri iniziali `c1 = 2`, `c2 = 5`. Esegui le iterazioni (assegnamento + aggiornamento dei centri) finché i centri non cambiano più, e scrivi i centri finali.

<details><summary>Soluzioni</summary>

1. (a) **Supervisionato, regressione** (prevedi un numero). (b) **Non supervisionato, clustering** (nessuna categoria data). (c) **Supervisionato, classificazione** binaria (immagini già diagnosticate = label). (d) **Non supervisionato, riduzione di dimensionalità** (es. PCA).
2. Punto chiave: `fit` dello scaler **solo sul training**, poi `transform` su entrambi.
   ```python
   from sklearn.model_selection import train_test_split
   from sklearn.preprocessing import StandardScaler
   from sklearn.linear_model import LogisticRegression
   from sklearn.metrics import accuracy_score

   X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
   sc = StandardScaler().fit(X_tr)          # media/scala SOLO dal training
   X_tr, X_te = sc.transform(X_tr), sc.transform(X_te)
   clf = LogisticRegression().fit(X_tr, y_tr)
   print(accuracy_score(y_te, clf.predict(X_te)))
   ```
3. **Iterazione 1** — assegnamento (centri 2 e 5): `2`→c1 (|2-2|=0 < |2-5|=3), `4`→c2 (|4-2|=2 > |4-5|=1), `10`→c2, `12`→c2. Gruppi c1={2}, c2={4,10,12}. Aggiornamento: `c1 = 2`, `c2 = (4+10+12)/3 ≈ 8,67`. **Iterazione 2** — assegnamento (centri 2 e 8,67): `2`→c1, `4`→c1 (|4-2|=2 < |4-8,67|=4,67), `10`→c2, `12`→c2. Gruppi c1={2,4}, c2={10,12}. Aggiornamento: `c1 = 3`, `c2 = 11`. **Iterazione 3** — gli stessi assegnamenti producono di nuovo c1={2,4}, c2={10,12}: i centri non cambiano, l'algoritmo è **arrivato a convergenza**. Centri finali: **c1 = 3, c2 = 11**.
</details>
