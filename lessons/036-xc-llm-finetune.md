---
day: 36
topic_id: xc-llm-finetune
title: "Fine-tuning vs RAG vs prompting: quando usare cosa"
area: cross-cutting
course: "LLM / AI Engineering"
grounded_in: null
adjacent: [xc-llm-rag, xc-llm-prompting, xc-llm-eval, ml-llm]
completeness_checked: true
quiz_count: 10
---

# Fine-tuning vs RAG vs prompting: quando usare cosa

> **Perché oggi:** è la domanda più pratica (e più sbagliata) nei progetti con gli LLM. "Mi serve il fine-tuning" è la risposta che danno tutti e che quasi sempre è quella sbagliata: nella maggior parte dei casi basta scrivere meglio il prompt o dare al modello i documenti giusti. Saper scegliere tra le tre leve, e spiegare **perché** anche in termini di costo, è una competenza da colloquio per ruoli di AI engineering e da decisione tecnica reale. Taglio della lezione: quando scegliere cosa, con quali strumenti veri e con quale conto della serva sui costi; la matematica dell'addestramento resta sullo sfondo.

## Le tre leve, in una riga ciascuna
Immagina il modello come un neolaureato bravissimo ma generico. Puoi migliorarne le risposte in tre modi:
- **Prompting:** gli **spieghi meglio il compito** nell'istruzione, senza cambiare nulla del modello. Include il **few-shot**, cioè mettere nel prompt alcuni **esempi** di input→output desiderato, e tecniche come chiedere di ragionare per passi. È il tema di `xc-llm-prompting`.
- **RAG (Retrieval-Augmented Generation, generazione aumentata dal recupero):** prima di rispondere, un sistema **recupera documenti pertinenti** da una **knowledge base** (una raccolta di tuoi documenti indicizzati, tipicamente in un **database vettoriale**, cioè un archivio che memorizza i testi come vettori numerici e li ritrova per similarità di significato) e li **incolla nel prompt** come contesto, così il modello risponde su fatti che non aveva in testa. È il tema di `xc-llm-rag`.
- **Fine-tuning (messa a punto):** **ri-addestri il modello** su un tuo insieme di esempi, modificandone i pesi, così **interiorizza** un comportamento, uno stile o un formato. È l'unica delle tre che cambia il modello.

## Cosa cambia davvero ciascuna leva
La chiave per scegliere è capire **su cosa** agisce ognuna. Un modo utile: distinguere tra dare **conoscenza** (fatti) e dare **comportamento** (come si comporta, in che forma risponde).
- **Prompting e RAG danno conoscenza e contesto al momento della richiesta.** Il RAG in particolare è il modo giusto per **fatti freschi, privati o che cambiano** (documentazione aziendale, listini, normative aggiornate): aggiorni la knowledge base e le risposte si aggiornano, senza ritoccare il modello.
- **Il fine-tuning cambia il comportamento, non aggiunge fatti affidabili.** È fortissimo per **formato, stile, tono, aderenza a un gergo o a un compito ripetitivo** (rispondere sempre in un certo JSON, imitare un tono di brand, classificare in categorie fisse). È la scelta sbagliata per infilare fatti aggiornati: il modello può comunque **allucinare** (inventare con tono sicuro), e ogni volta che i fatti cambiano dovresti ri-addestrarlo.

Un rischio specifico del fine-tuning è il **catastrophic forgetting (dimenticanza catastrofica):** addestrando troppo su un compito ristretto, il modello può **peggiorare** sulle capacità generali che aveva prima. Per questo oggi quasi nessuno ri-addestra tutti i pesi.

## Fine-tuning moderno: LoRA, QLoRA, PEFT (perché non spaventa più)
Ri-addestrare da zero tutti i miliardi di parametri è costoso e rischioso. La pratica attuale è il **PEFT (Parameter-Efficient Fine-Tuning, messa a punto efficiente nei parametri):** invece di toccare tutti i pesi, ne addestri una piccolissima frazione. La tecnica più diffusa è il **LoRA (Low-Rank Adaptation):** congeli il modello originale e aggiungi piccole matrici addestrabili "a lato"; alleni solo quelle, che pesano una minima parte del totale. Il **QLoRA** è LoRA applicato a un modello **quantizzato** (con i pesi rappresentati a precisione ridotta per occupare meno memoria), così il fine-tuning sta anche su una singola GPU modesta. Risultato pratico: il fine-tuning è diventato accessibile, ma resta un progetto vero, con **dati da curare** e **valutazione** da fare.

## Come scegliere (l'albero decisionale da dire a voce)
1. **Parti sempre dal prompting.** È gratis da provare, immediato, zero infrastruttura. Spesso un buon prompt con qualche esempio few-shot risolve.
2. **Il problema è che al modello mancano fatti (freschi, privati, specifici)?** → **RAG.** Gli dai i documenti giusti al momento della domanda.
3. **Il problema è il comportamento (formato/stile/tono/compito ristretto sempre uguale), e il prompting non basta o il prompt diventa enorme?** → **Fine-tuning.**
4. **Servono sia fatti sia comportamento?** → si **combinano**: fine-tuning per lo stile/formato + RAG per i fatti. Non sono alternative esclusive.

La regola mnemonica: **RAG per quello che il modello deve sapere, fine-tuning per come deve comportarsi, prompting per dirglielo.**

## Costi e trade-off (il conto della serva)
- **Prompting:** costo di sviluppo quasi nullo, nessuna infrastruttura. Però prompt lunghi (molti esempi, molto contesto) costano a ogni chiamata, perché paghi per **token** (le unità in cui il testo è spezzato) e riempiono la **context window** (la quantità massima di testo che il modello può leggere in una volta).
- **RAG:** costo medio e continuativo: serve un **database vettoriale** e una pipeline di indicizzazione, e ogni risposta spende token extra per i documenti recuperati. In cambio i fatti restano **aggiornabili** senza ri-addestrare.
- **Fine-tuning:** costo **iniziale** alto (raccogliere e pulire gli esempi, lanciare l'addestramento, valutare), ma può **ridurre** il costo per chiamata, perché il comportamento è nel modello e il prompt diventa più corto. Svantaggio: è **statico**, se cambia ciò che vuoi devi ri-addestrare, e richiede abbastanza esempi di qualità (da qualche decina di esempi curati in su, a seconda del compito).

## Strumenti reali
- **Prompting:** niente di speciale, l'API del modello; librerie per gestire i prompt e l'output strutturato.
- **RAG:** un **database vettoriale** (es. FAISS in locale, o servizi gestiti), framework di orchestrazione come **LangChain** o **LlamaIndex**. Approfondimento in `xc-llm-rag` e `xc-llm-vectordb`.
- **Fine-tuning:** l'**API di fine-tuning** dei fornitori di modelli chiusi, che vuole i dati in formato **JSONL** (un esempio per riga, in JSON); per i modelli aperti la libreria **PEFT** di Hugging Face, e strumenti che semplificano il tutto come **Unsloth** o **Axolotl**.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 620 300" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="m36" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
    <rect x="235" y="14" width="150" height="34" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="310" y="35">Prova prima il prompting</text>
    <rect x="215" y="86" width="190" height="34" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="310" y="107" font-size="10.5">Manca conoscenza o comportamento?</text>
    <rect x="30" y="170" width="170" height="46" rx="8" fill="var(--card2)" stroke="var(--rule)"/><text x="115" y="190">Fatti freschi/privati</text><text x="115" y="207" font-size="10.5" fill="var(--muted)">→ RAG</text>
    <rect x="225" y="170" width="170" height="46" rx="8" fill="var(--card2)" stroke="var(--rule)"/><text x="310" y="190">Formato/stile/tono</text><text x="310" y="207" font-size="10.5" fill="var(--muted)">→ Fine-tuning</text>
    <rect x="420" y="170" width="170" height="46" rx="8" fill="var(--card2)" stroke="var(--rule)"/><text x="505" y="190">Entrambi</text><text x="505" y="207" font-size="10.5" fill="var(--muted)">→ RAG + fine-tuning</text>
    <text x="310" y="262" font-size="10.5" fill="var(--muted)">RAG = cosa deve sapere · fine-tuning = come deve comportarsi · prompting = glielo dici</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none" marker-end="url(#m36)">
    <path d="M310,48 L310,84"/>
    <path d="M250,120 L130,168"/><path d="M310,120 L310,168"/><path d="M370,120 L490,168"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">L'albero decisionale: si parte sempre dal prompting; se manca conoscenza fattuale si va su RAG, se manca un comportamento (formato, stile) sul fine-tuning, e per entrambi si combinano. Non sono alternative esclusive.</figcaption>
</figure>

## Esempi concreti
- **Assistente sulla documentazione interna:** le risposte devono citare manuali che cambiano. → **RAG**, così aggiorno i documenti senza ri-addestrare. Il fine-tuning qui sarebbe la scelta sbagliata (fatti statici, rischio allucinazione).
- **Classificatore che deve sempre restituire un JSON con campi fissi:** comportamento ripetitivo e formato rigido. Se il prompting con esempi non è abbastanza stabile o il prompt diventa enorme → **fine-tuning** su molti esempi input→JSON.
- **Chatbot con un tono di brand preciso che risponde su listini aggiornati:** serve sia lo stile sia i fatti freschi. → **fine-tuning per il tono + RAG per i listini**, combinati.
- **Prototipo veloce:** qualunque idea, prima la provo in **prompting**. Se regge, decido se vale la pena investire in RAG o fine-tuning.

## Notable use case
- **OpenAI e Anthropic** documentano il fine-tuning come passo da fare **dopo** aver spremuto prompting e, dove serve, il recupero di contesto.
- **GitHub Copilot e assistenti al codice** combinano un modello forte con il **recupero del contesto** del repository (una forma di RAG) più che ri-addestrare per ogni codebase.
- **Modelli aperti verticalizzati** (es. su ambito legale o medico) nascono spesso da **fine-tuning PEFT/LoRA** di un modello base, perché cambiare il comportamento su un gergo specifico è esattamente il punto di forza del fine-tuning.

## Fonti
- **OpenAI — Fine-tuning guide** e **Prompt engineering guide** (platform.openai.com/docs)
- **Hugging Face — PEFT documentation** (huggingface.co/docs/peft)
- **Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models"** (2021) e **Dettmers et al., "QLoRA"** (2023)
- **Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** (2020)

## Concetti adiacenti
- `xc-llm-rag` — architetture di RAG (naive, advanced, hybrid): la leva "conoscenza"
- `xc-llm-prompting` — zero/few-shot, chain-of-thought, output strutturato: la prima leva da provare
- `xc-llm-eval` — come misuri se la scelta (prompting/RAG/fine-tuning) ha davvero migliorato il sistema
- `ml-llm` — i fondamenti di LLM, embedding e RAG da cui parte tutto

## Quiz (10 — tutte rispondibili dalla lezione)
1. In una riga ciascuna, cosa fanno **prompting**, **RAG** e **fine-tuning**? Quale delle tre modifica il modello?
2. Cos'è il **few-shot** nel prompting?
3. Cosa significa l'acronimo **RAG** e in che modo porta i fatti al modello?
4. Perché il **RAG** è la scelta giusta per fatti **freschi/privati/che cambiano**, e il fine-tuning no?
5. Per cosa è forte il **fine-tuning** (su cosa agisce)?
6. Cos'è il **catastrophic forgetting**?
7. Cosa sono **PEFT** e **LoRA**, e cosa aggiunge il **QLoRA**?
8. Qual è l'ordine consigliato per scegliere la leva (l'albero decisionale)?
9. Confronta i **costi**: prompting vs RAG vs fine-tuning (iniziale e per chiamata).
10. Cita gli strumenti tipici per il fine-tuning e in che **formato** vuole i dati l'API di fine-tuning dei modelli chiusi.

<details><summary>Risposte</summary>

1. **Prompting:** spieghi meglio il compito nell'istruzione. **RAG:** recuperi documenti pertinenti e li incolli nel prompt come contesto. **Fine-tuning:** ri-addestri il modello sui tuoi esempi. Solo il **fine-tuning** modifica il modello.
2. Mettere nel prompt **alcuni esempi** di input→output desiderato, per mostrare al modello il compito.
3. **Retrieval-Augmented Generation:** prima di rispondere recupera documenti pertinenti (spesso da un database vettoriale) e li **aggiunge al prompt** come contesto.
4. Perché col RAG **aggiorni la knowledge base** e le risposte si aggiornano senza toccare il modello; il fine-tuning interiorizza fatti **statici**, può allucinare e andrebbe ri-addestrato a ogni cambiamento.
5. Per il **comportamento**: formato, stile, tono, aderenza a un gergo o a un compito ripetitivo. Non per aggiungere fatti affidabili.
6. Quando, addestrando troppo su un compito ristretto, il modello **peggiora sulle capacità generali** che aveva prima.
7. **PEFT** = messa a punto efficiente nei parametri (addestri solo una piccola frazione dei pesi). **LoRA** = congeli il modello e addestri piccole matrici aggiunte a lato. **QLoRA** = LoRA su un modello **quantizzato** (pesi a precisione ridotta), così sta su una GPU modesta.
8. (1) Parti dal **prompting**; (2) se mancano **fatti** → **RAG**; (3) se manca un **comportamento**/formato e il prompting non basta → **fine-tuning**; (4) se servono entrambi, **combini** RAG + fine-tuning.
9. **Prompting:** sviluppo quasi nullo, nessuna infrastruttura, ma prompt lunghi costano a ogni chiamata (token). **RAG:** costo medio e continuativo (database vettoriale + token extra), fatti aggiornabili. **Fine-tuning:** costo **iniziale** alto, ma può **abbassare** il costo per chiamata (prompt più corto); è statico e serve ri-addestrare se cambia.
10. Per modelli chiusi l'**API di fine-tuning** dei fornitori, che vuole i dati in **JSONL**; per modelli aperti la libreria **PEFT** di Hugging Face e strumenti come **Unsloth** o **Axolotl**.
</details>

## Esercizi
1. **Scegli la leva (e giustifica col costo).** Per ciascun caso indica prompting / RAG / fine-tuning (o combinazione) e una riga di motivazione: (a) un bot che risponde su policy aziendali aggiornate ogni mese; (b) estrarre sempre da un testo un JSON con 5 campi fissi, su grande volume; (c) riassumere un articolo incollato dall'utente; (d) un assistente col tono di un brand che risponde su un catalogo prodotti che cambia spesso.
2. **Scrivi un esempio di training in JSONL.** Per un fine-tuning che deve classificare una recensione in `positiva`/`negativa`/`neutra`, scrivi **una** riga JSONL valida nel formato a messaggi (ruoli system/user/assistant).
3. **Stima dei costi (con assunzioni date).** Supponi un prezzo di input di **$0,50 per 1M di token** e che ogni risposta usi un prompt di **4.000 token**. Con **prompting** servono inoltre 6 esempi few-shot da 500 token l'uno in ogni prompt; con **fine-tuning** quegli esempi non servono. Calcola il costo di input per **100.000 chiamate** nei due casi e la differenza.

<details><summary>Soluzioni</summary>

1. (a) **RAG**: le policy cambiano, basta aggiornare i documenti, niente ri-addestramento. (b) **Fine-tuning** (eventualmente dopo aver provato il prompting): formato rigido e ripetitivo su grande volume, interiorizzarlo accorcia il prompt e stabilizza l'output. (c) **Prompting**: il testo arriva già nella richiesta, nessun fatto esterno né comportamento speciale. (d) **RAG + fine-tuning**: fine-tuning per il tono di brand, RAG per il catalogo che cambia.
2. Una riga JSONL (un oggetto JSON completo su una sola riga):
   ```json
   {"messages":[{"role":"system","content":"Classifica la recensione in positiva, negativa o neutra."},{"role":"user","content":"Consegna lenta ma prodotto ottimo."},{"role":"assistant","content":"neutra"}]}
   ```
3. Token per chiamata:
   - **Prompting:** 4.000 + 6×500 = **7.000** token. Per 100.000 chiamate: 700.000.000 token = 700 M. Costo: 700 × $0,50 = **$350**.
   - **Fine-tuning:** 4.000 token. Per 100.000 chiamate: 400.000.000 = 400 M. Costo: 400 × $0,50 = **$200**.
   - **Differenza:** $350 − $200 = **$150** risparmiati sull'input (da pesare contro il costo iniziale di addestramento del fine-tuning, non incluso qui).
</details>
