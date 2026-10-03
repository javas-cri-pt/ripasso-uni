---
day: 41
topic_id: ml-eval
title: "Valutazione dei modelli ML: accuracy, precision/recall, overfitting"
area: computer-science
course: "Laboratorio IA e Machine Learning"
grounded_in: null
adjacent: [ml-basics, qe-spc, xc-llm-eval, xc-pm-experiment]
completeness_checked: true
quiz_count: 10
---

# Valutazione dei modelli ML: accuracy, precision/recall, overfitting

> **Perché oggi:** allenare un modello è la parte facile; sapere **se è buono davvero** è ciò che distingue chi fa ML sul serio. "Il mio modello ha il 99% di accuratezza" è una frase che, da sola, non vuol dire niente, e in certi casi nasconde un modello inutile. Qui vediamo le metriche che contano (precision, recall, F1), la matrice che le genera, e come riconoscere l'overfitting con i numeri in mano. È il repertorio di risposte a un colloquio su ML. Questa lezione è sul **ML classico**: la valutazione dei sistemi basati su LLM, che ha problemi diversi, la trovi in `xc-llm-eval` (concetto adiacente, qui la cito solo di sfuggita).

## Perché l'accuracy da sola inganna
L'**accuracy (accuratezza)** è la frazione di predizioni corrette sul totale: semplice e intuitiva. Il problema è con le **classi sbilanciate**, cioè quando una classe è molto più rara dell'altra. Esempio classico: su 1000 transazioni solo 5 sono frodi. Un modello pigro che dice sempre "legittima" prende 995 su 1000, cioè **99,5% di accuracy**, pur non avendo trovato **nessuna** frode. È il cosiddetto **accuracy paradox**: un numero altissimo che descrive un modello del tutto inutile per il compito che conta. Per questo servono metriche che guardino la classe rara.

## La confusion matrix (matrice di confusione)
La **confusion matrix** è una tabella che incrocia **ciò che il modello ha predetto** con **la verità**. Per una classificazione binaria (classe "positiva" = quella che ci interessa, es. "frode", "malato", "spam") ha quattro celle:
- **TP (True Positive, vero positivo):** era positivo e l'hai predetto positivo. Giusto.
- **FP (False Positive, falso positivo):** era negativo ma l'hai predetto positivo. **Falso allarme.**
- **FN (False Negative, falso negativo):** era positivo ma l'hai predetto negativo. **Te lo sei perso.**
- **TN (True Negative, vero negativo):** era negativo e l'hai predetto negativo. Giusto.

Da queste quattro celle derivano tutte le metriche. In formula, l'accuracy è `(TP + TN) / (TP + FP + FN + TN)`.

## Precision, recall e F1
Le due metriche che "aggiustano" l'accuracy guardano solo la classe positiva, da due angolazioni diverse:
- **Precision (precisione):** `TP / (TP + FP)`. Tra tutti quelli che ho **dichiarato positivi**, quanti lo erano davvero? Risponde a "quando suono l'allarme, quanto sono affidabile?". Alta precision = pochi falsi allarmi.
- **Recall (richiamo, sensibilità):** `TP / (TP + FN)`. Tra tutti quelli che **erano positivi**, quanti ne ho trovati? Risponde a "quanti me ne sono perso?". Alta recall = pochi casi mancati.

C'è un **compromesso** tra le due. Se il modello dà un **punteggio** di probabilità e tu fissi una **soglia (threshold)** per decidere "positivo", abbassare la soglia ti fa dichiarare positivi più casi (recall sale, precision scende); alzarla fa il contrario. Quale privilegiare dipende dal costo degli errori:
- **Recall prima di tutto** quando un FN è grave: diagnosi di una malattia (meglio un falso allarme che un malato mancato), rilevamento frodi.
- **Precision prima di tutto** quando un FP è costoso o fastidioso: filtro antispam (non voglio buttare una email vera), suggerire un contenuto a pagamento.

L'**F1-score** riassume le due in un solo numero: è la **media armonica** di precision e recall, `F1 = 2 · (precision · recall) / (precision + recall)`. La media armonica, a differenza di quella normale, è bassa se **anche solo una** delle due è bassa: così premia i modelli **bilanciati** e punisce chi massimizza una metrica trascurando l'altra.

## Overfitting, underfitting e il compromesso bias-varianza
Un modello va misurato su dati mai visti (vedi la separazione train/test in `ml-basics`). Confrontando l'errore sui due insiemi si diagnostica il problema:
- **Underfitting (sottoadattamento):** errore **alto sia sul training sia sul test**. Il modello è troppo semplice per cogliere la relazione. Si dice che ha **bias alto**: fa assunzioni troppo rigide.
- **Overfitting (sovradattamento):** errore **basso sul training ma alto sul test**. Il modello ha imparato a memoria, rumore compreso. Si dice che ha **varianza alta**: cambia tanto al variare dei dati di allenamento.

Questo è il **compromesso bias-varianza (bias-variance tradeoff)**: rendere un modello più complesso abbassa il bias ma alza la varianza, e viceversa. Il punto ideale sta nel mezzo, dove l'errore sul test è minimo. Le armi contro l'overfitting: **più dati**, **modelli più semplici**, **regolarizzazione** (una penalità che scoraggia parametri troppo grandi) e la **cross-validation** qui sotto.

## Cross-validation (convalida incrociata)
Con un solo split train/test il risultato dipende dalla fortuna di **quale** fetta è finita nel test. La **k-fold cross-validation** rende la stima più robusta:
1. Dividi i dati in `k` parti uguali (i **fold**), tipicamente `k = 5` o `10`.
2. Alleni `k` volte: ogni volta tieni **un fold come test** e gli altri `k-1` come training.
3. Fai la **media** dei `k` punteggi (e ne guardi la variabilità).

Così ogni esempio finisce nel test esattamente una volta, e ottieni una stima più affidabile, utile soprattutto quando i dati sono pochi. Per le classi sbilanciate si usa la **stratified k-fold**, che mantiene in ogni fold la stessa proporzione tra le classi.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 560 250" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="280" y="20" font-weight="700">Confusion matrix (classe positiva = ciò che cerchi)</text>
    <text x="155" y="52" font-size="11" fill="var(--muted)">Predetto positivo</text>
    <text x="310" y="52" font-size="11" fill="var(--muted)">Predetto negativo</text>
    <text x="74" y="97" font-size="10.5" fill="var(--muted)" text-anchor="end">Reale pos.</text>
    <text x="74" y="163" font-size="10.5" fill="var(--muted)" text-anchor="end">Reale neg.</text>
    <rect x="80" y="62" width="150" height="62" rx="6" fill="var(--card2)" stroke="var(--good)" stroke-width="1.7"/><text x="155" y="88">TP</text><text x="155" y="106" font-size="10" fill="var(--muted)">vero positivo</text>
    <rect x="235" y="62" width="150" height="62" rx="6" fill="var(--card)" stroke="var(--accent)" stroke-width="1.5"/><text x="310" y="88">FN</text><text x="310" y="106" font-size="10" fill="var(--muted)">te lo sei perso</text>
    <rect x="80" y="128" width="150" height="62" rx="6" fill="var(--card)" stroke="var(--accent)" stroke-width="1.5"/><text x="155" y="154">FP</text><text x="155" y="172" font-size="10" fill="var(--muted)">falso allarme</text>
    <rect x="235" y="128" width="150" height="62" rx="6" fill="var(--card2)" stroke="var(--good)" stroke-width="1.7"/><text x="310" y="154">TN</text><text x="310" y="172" font-size="10" fill="var(--muted)">vero negativo</text>
    <text x="470" y="92" font-size="11" text-anchor="start">precision</text><text x="470" y="108" font-size="10" fill="var(--muted)" text-anchor="start">TP/(TP+FP)</text>
    <text x="470" y="150" font-size="11" text-anchor="start">recall</text><text x="470" y="166" font-size="10" fill="var(--muted)" text-anchor="start">TP/(TP+FN)</text>
    <text x="280" y="220" font-size="10.5" fill="var(--muted)">F1 = 2·precision·recall / (precision + recall)</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">La confusion matrix: le due diagonali verdi (TP, TN) sono le predizioni giuste. La precision legge la colonna "predetto positivo" (TP su TP+FP), la recall la riga dei positivi reali (TP su TP+FN). F1 le combina in media armonica.</figcaption>
</figure>

## Esempi concreti
- **Il modello "99% ma inutile":** 1000 transazioni, 5 frodi. Predico sempre "legittima" → accuracy 99,5%, ma **recall sulle frodi = 0** (TP=0). Guardando precision/recall sulla classe rara il bluff crolla subito.
- **Leggere una confusion matrix:** supponi TP=40, FP=10, FN=20, TN=430. Accuracy `(40+430)/500 = 0,94`. Precision `40/(40+10) = 0,80`. Recall `40/(40+20) ≈ 0,67`. F1 `≈ 0,73`. Nota che l'accuracy alta nasconde una recall mediocre: 20 positivi persi.
- **Scegliere la soglia:** in un sistema di diagnosi abbassi la soglia per non perderti malati (recall alta) accettando più falsi allarmi (precision più bassa), perché un FN costa molto più di un FP.

## Notable use case
- **scikit-learn** fornisce tutto pronto: `confusion_matrix`, `classification_report` (stampa precision/recall/F1 per classe), `cross_val_score`, `StratifiedKFold`. È lo standard de facto per valutare il ML classico.
- **Competizioni Kaggle**: molte scelgono F1 o metriche ad hoc proprio perché l'accuracy su dataset sbilanciati non discrimina i modelli.
- **Il ponte con la qualità di processo (`qe-spc`):** misurare una metrica nel tempo e scattare quando esce dai limiti è la stessa idea delle **carte di controllo** del controllo statistico di processo; in produzione si monitora così la metrica di un modello per accorgersi quando degrada.

## Fonti
- **scikit-learn — Metrics and scoring** (scikit-learn.org/stable/modules/model_evaluation.html)
- **Google — Machine Learning Crash Course**, sezioni *Classification* (accuracy, precision, recall)
- **James, Witten, Hastie, Tibshirani — An Introduction to Statistical Learning (ISLR)**, capitolo sulla valutazione e la cross-validation

## Concetti adiacenti
- `ml-basics` — supervisionato/non supervisionato e la separazione train/validation/test su cui poggiano queste metriche
- `qe-spc` — carte di controllo: monitorare una metrica nel tempo e scattare sui limiti
- `xc-llm-eval` — la valutazione dei sistemi LLM (LLM-as-judge, hallucination): problema diverso, stessa mentalità
- `xc-pm-experiment` — A/B testing: misurare se una modifica migliora davvero, con rigore statistico

## Quiz (10 — tutte rispondibili dalla lezione)
1. Perché l'**accuracy** da sola può ingannare? Descrivi l'**accuracy paradox** con l'esempio delle frodi.
2. Cosa sono **TP, FP, FN, TN** in una confusion matrix?
3. Scrivi la formula della **precision** e di' a quale domanda risponde.
4. Scrivi la formula della **recall** e di' a quale domanda risponde.
5. In quale situazione privilegi la **recall** e in quale la **precision**? Un esempio per ciascuna.
6. Cos'è l'**F1-score** e perché si usa la **media armonica** invece della media semplice?
7. Come distingui **overfitting** da **underfitting** guardando l'errore su training e test?
8. Cos'è il **compromesso bias-varianza**? Collega bias e varianza a underfitting e overfitting.
9. Come funziona la **k-fold cross-validation** e perché è più robusta di un singolo split?
10. Cos'è la **stratified k-fold** e quando serve?

<details><summary>Risposte</summary>

1. Perché con **classi sbilanciate** un modello che predice sempre la classe maggioritaria ottiene un'accuracy altissima pur essendo inutile. Esempio: 5 frodi su 1000, predico sempre "legittima" → 99,5% di accuracy ma zero frodi trovate.
2. **TP**: positivo predetto positivo (giusto). **FP**: negativo predetto positivo (falso allarme). **FN**: positivo predetto negativo (perso). **TN**: negativo predetto negativo (giusto).
3. **Precision = TP / (TP + FP)**. Tra quelli dichiarati positivi, quanti lo erano davvero (affidabilità dell'allarme, pochi falsi allarmi).
4. **Recall = TP / (TP + FN)**. Tra i positivi reali, quanti ne ho trovati (quanti me ne sono perso).
5. **Recall** quando un FN è grave: diagnosi medica, rilevamento frodi (meglio un falso allarme che un caso perso). **Precision** quando un FP è costoso: filtro antispam (non buttare email vere).
6. L'**F1** è la **media armonica** di precision e recall: `2·P·R/(P+R)`. La media armonica è **bassa se anche solo una** delle due è bassa, quindi premia i modelli bilanciati e penalizza chi trascura una delle due metriche.
7. **Underfitting**: errore alto **sia su training sia su test**. **Overfitting**: errore basso sul training ma **alto sul test** (divario tra i due).
8. È il fatto che aumentare la complessità **abbassa il bias ma alza la varianza** (e viceversa). **Bias alto → underfitting** (modello troppo rigido); **varianza alta → overfitting** (modello troppo sensibile ai dati di training).
9. Dividi i dati in `k` fold; alleni `k` volte tenendo ogni volta un fold diverso come test e gli altri come training; fai la **media** dei punteggi. È più robusta perché non dipende da quale singola fetta è finita nel test e ogni esempio è testato una volta.
10. È una k-fold che mantiene in **ogni fold la stessa proporzione tra le classi**; serve con **classi sbilanciate**, per evitare fold senza esempi della classe rara.
</details>

## Esercizi
1. **Metriche da una confusion matrix.** Un classificatore binario dà: TP=45, FP=5, FN=15, TN=135. Calcola **accuracy, precision, recall e F1** (due decimali). Commenta in una riga.
2. **Funzione delle metriche.** Scrivi una funzione `precision_recall_f1(tp, fp, fn)` che restituisce i tre valori, gestendo il caso in cui un denominatore sia zero (restituisci 0.0).
3. **Diagnosi.** Per ciascun modello, di' se è over-, under- o ben adattato: (a) accuracy training 0,99, test 0,71; (b) training 0,62, test 0,60; (c) training 0,93, test 0,90. Cosa proveresti per (a)?
4. **Indici k-fold.** Hai 10 esempi con indici 0..9 e vuoi una 5-fold (fold contigui, non mescolati). Scrivi, per ogni iterazione, quali indici sono **test** e quali **training**.

<details><summary>Soluzioni</summary>

1. Totale = 45+5+15+135 = 200. **Accuracy** = (45+135)/200 = **0,90**. **Precision** = 45/(45+5) = **0,90**. **Recall** = 45/(45+15) = **0,75**. **F1** = 2·0,90·0,75/(0,90+0,75) = 1,35/1,65 ≈ **0,82**. Commento: buona precision, ma la recall 0,75 dice che perde 1 positivo su 4.
2. 
   ```python
   def precision_recall_f1(tp, fp, fn):
       precision = tp / (tp + fp) if (tp + fp) else 0.0
       recall    = tp / (tp + fn) if (tp + fn) else 0.0
       f1 = 2*precision*recall/(precision+recall) if (precision+recall) else 0.0
       return precision, recall, f1
   ```
3. (a) **Overfitting** (0,99 vs 0,71, grande divario): proverei più dati, un modello più semplice o la regolarizzazione. (b) **Underfitting** (entrambi bassi): modello troppo semplice, servono feature/modello più espressivi. (c) **Ben adattato** (alto e vicino tra train e test).
4. 5 fold da 2 elementi ciascuno:
   - Iter 1 — test [0,1], train [2,3,4,5,6,7,8,9]
   - Iter 2 — test [2,3], train [0,1,4,5,6,7,8,9]
   - Iter 3 — test [4,5], train [0,1,2,3,6,7,8,9]
   - Iter 4 — test [6,7], train [0,1,2,3,4,5,8,9]
   - Iter 5 — test [8,9], train [0,1,2,3,4,5,6,7]
</details>
