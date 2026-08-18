---
day: 3
topic_id: xc-llm-fundamentals
title: "Come funziona un LLM — token, embedding, transformer, attention"
area: cross-cutting
course: LLM / AI Engineering
grounded_in: null
adjacent: [xc-llm-rag, xc-llm-prompting, ml-nn]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun acronimo lasciato senza definizione."
---

# Come funziona un LLM

> **Perché oggi:** i ruoli che punti (AI Engineer / LLM Engineer) e il lavoro a Glacom/MaiCare ruotano intorno agli LLM — il bot preventivi, il triage dei ticket, gli assistenti clinici sono tutti costruiti *sopra* un modello linguistico. Sapere **cosa** succede davvero dentro (non trattarlo come una scatola magica) è ciò che distingue chi *usa* l'API da chi *progetta* il sistema: ti serve per scegliere il modello giusto, capire perché "allucina", dimensionare i costi e sapere quando serve la RAG.

## Cos'è un LLM

**LLM = Large Language Model** ("grande modello linguistico"). È un modello statistico, addestrato su enormi quantità di testo, che ha imparato a fare **una sola cosa**, ripetuta miliardi di volte: **dato un pezzo di testo, predire quale sarà il token (pezzo di parola) successivo più probabile.**

Sembra poco, ma da questa singola capacità — "indovina la prossima parola" — emergono traduzione, riassunto, scrittura di codice, risposta a domande. Il motivo: per predire *davvero bene* la parola successiva su tutto il testo del mondo, il modello è **costretto** a imparare grammatica, fatti, ragionamento, stile. La predizione è il compito; la "comprensione" è l'effetto collaterale necessario.

Un punto chiave subito, perché sfata la magia: l'LLM **non ha un database di risposte** e **non "cerca" nulla**. Ha dei **parametri** (numeri, detti *pesi*) fissati durante l'addestramento, e ogni risposta è **calcolata** al volo facendo passare l'input attraverso quei numeri. È un calcolo, non una ricerca.

La pipeline completa, dall'input alla risposta, è questa:

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 250" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="ar1" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
   <rect x="8" y="90" width="96" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="56" y="108">Testo</text><text x="56" y="123" font-size="10.5" fill="var(--muted)">"Il cielo è"</text>
   <rect x="128" y="90" width="112" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="184" y="108">Tokenizzazione</text><text x="184" y="123" font-size="10.5" fill="var(--muted)">testo → token</text>
   <rect x="264" y="90" width="112" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="320" y="108">Embedding</text><text x="320" y="123" font-size="10.5" fill="var(--muted)">token → vettori</text>
   <rect x="400" y="90" width="120" height="42" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="460" y="108">Transformer</text><text x="460" y="123" font-size="10.5" fill="var(--muted)">N layer</text>
   <rect x="544" y="72" width="120" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="604" y="90">Probabilità</text><text x="604" y="105" font-size="10.5" fill="var(--muted)">su prossimo token</text>
   <rect x="544" y="150" width="120" height="42" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="604" y="168">Token scelto</text><text x="604" y="183" font-size="10.5" fill="var(--muted)">"azzurro"</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#ar1)">
   <path d="M104,111 L126,111"/>
   <path d="M240,111 L262,111"/>
   <path d="M376,111 L398,111"/>
   <path d="M520,105 L542,97"/>
   <path d="M604,114 L604,148"/>
  </g>
  <g stroke="var(--accent)" stroke-width="1.4" fill="none" marker-end="url(#ar1)" stroke-dasharray="4 3">
   <path d="M604,192 L604,222 L184,222 L184,134"/>
  </g>
  <text x="380" y="238" font-size="10.5" fill="var(--accent)" text-anchor="middle">autoregressivo: il token scelto viene riaccodato all'input e il ciclo riparte</text>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">La pipeline: Testo → Tokenizzazione → Embedding → Transformer (N layer) → probabilità sul prossimo token → token scelto → si ripete (freccia tratteggiata: ciclo autoregressivo).</figcaption>
</figure>

---

## 1. Token e tokenizzazione

Il modello **non vede lettere né parole intere**: vede **token**. Un **token** è un *pezzo di parola* — spesso una radice, un suffisso o una parola breve. Il **tokenizer** ("tokenizzatore") è il pezzo di software che, prima di tutto, spezza il testo in questi pezzi e li converte in numeri interi (ogni token ha un ID nel *vocabolario* del modello, cioè la lista di tutti i token che conosce, tipicamente decine di migliaia).

Esempio (indicativo): la parola `tokenizzazione` potrebbe diventare `token` + `izz` + `azione` → 3 token. `Ciao` è 1 token. Anche lo **spazio** e la **punteggiatura** contano come (parte di) token.

**Perché non parole intere?** Tre motivi:
- **Le parole sono troppe.** Ogni lingua ha centinaia di migliaia di parole, più nomi propri, refusi, parole nuove. Un vocabolario di sole parole intere sarebbe gigantesco e comunque incompleto.
- **Parole mai viste.** Con le parole intere, una parola nuova (es. un termine tecnico o un errore di battitura) sarebbe *sconosciuta* e ingestibile. Con i pezzi, il modello la ricompone da sotto-pezzi che conosce.
- **Efficienza.** I pezzi frequenti (come `azione`, `ing`, `pre`) si riusano in migliaia di parole diverse: il vocabolario resta compatto ma copre tutto.

L'algoritmo classico che sceglie *come* spezzare si chiama **BPE = Byte Pair Encoding** ("codifica a coppie di byte"): parte dai singoli caratteri e, guardando tanto testo, **fonde ripetutamente le coppie di simboli più frequenti** in un unico token. Così le sequenze comuni diventano un token solo, quelle rare restano spezzate. Questo tipo di token (più piccolo della parola, più grande della lettera) si chiama **subword** ("sotto-parola").

**Context window (finestra di contesto).** È il numero **massimo di token** che il modello può considerare **tutti insieme** in una singola chiamata — include sia il tuo input (prompt) sia la risposta che sta generando. Tutto ciò che eccede la finestra **non esiste** per il modello: se una conversazione diventa più lunga della finestra, le parti più vecchie vengono tagliate e il modello "le dimentica". Regola pratica per stimare: in inglese ~1 token ≈ 0,75 parole (in italiano un po' meno per token); quindi una finestra da 8.000 token ≈ ~6.000 parole tra domanda e risposta.

---

## 2. Embedding

Un numero-ID di un token (es. il token `cane` = ID 4711) non dice **nulla** sul significato: 4711 non è "più vicino" a 4712 in senso di significato, è solo un indice. Serve un modo per rappresentare il *significato* in forma numerica. È l'**embedding**.

Un **embedding** è un **vettore di numeri** (una lista ordinata di valori, es. 768 o 1536 numeri) associato a un token, che ne rappresenta il significato in uno **spazio geometrico**. Il modello impara questi vettori durante l'addestramento. La proprietà fondamentale, e il motivo per cui funziona:

> **Token/parole con significato simile finiscono con vettori vicini nello spazio; significati diversi → vettori lontani.**

Così `cane`, `gatto`, `cucciolo` stanno in una regione vicina; `banca`, `mutuo`, `interesse` in un'altra. Il numero di valori nel vettore è la **dimensione** dell'embedding (es. 768, 1024, 3072): più dimensioni = più "sfumature" di significato rappresentabili, ma vettori più pesanti da calcolare e memorizzare.

**Come si misura la "vicinanza"?** Con la **similarità coseno (cosine similarity)**: si misura l'**angolo** tra due vettori, non la loro lunghezza. Formalmente è il coseno dell'angolo tra i due vettori:

> **cosine similarity(A, B) = (A · B) / (‖A‖ · ‖B‖)**

dove `A · B` è il **prodotto scalare** (somma dei prodotti componente per componente) e `‖A‖` è la **lunghezza** (norma) del vettore. Il risultato va da **−1 a +1**:
- **+1** = stessa direzione → significati molto simili;
- **0** = perpendicolari → non correlati;
- **−1** = direzioni opposte.

Si guarda l'**angolo** (e non la distanza in linea retta) perché conta la *direzione* del significato, non quanto è "lungo" il vettore. Questa è la stessa matematica che regge la **ricerca semantica** e la RAG (topic `xc-llm-rag`): trovi i testi rilevanti cercando gli embedding con similarità coseno più alta rispetto alla domanda.

---

## 3. Transformer e self-attention

Il **transformer** ("trasformatore") è l'**architettura di rete neurale** che sta dentro ogni LLM moderno, introdotta nel 2017 dal paper *"Attention Is All You Need"*. Il suo cuore è un meccanismo chiamato **self-attention** ("auto-attenzione").

**L'intuizione dell'attention.** Il significato di una parola dipende dalle *altre* parole intorno. Nella frase *"ho versato il vino nel bicchiere finché **non** fu pieno"*, per capire cosa era pieno il modello deve collegare "pieno" al "bicchiere", non al "vino". La **self-attention** fa esattamente questo: per ogni token, **guarda tutti gli altri token della finestra e decide quali sono rilevanti**, dando a ciascuno un **peso** (un'importanza). Poi rappresenta ogni token come una **miscela pesata** delle informazioni dei token rilevanti. È "self" (auto) perché i token di una stessa sequenza si guardano tra loro.

**Come pesa: query, key, value (a parole).** Per ogni token il modello calcola tre vettori:
- **Query (Q)** = "cosa sto cercando?" — la domanda che questo token pone.
- **Key (K)** = "cosa offro / di cosa parlo?" — l'etichetta che ogni token espone.
- **Value (V)** = "quale informazione porto?" — il contenuto vero e proprio.

Il meccanismo confronta la **Query** di un token con le **Key** di tutti gli altri (con un prodotto scalare: Query e Key simili → punteggio alto). Quei punteggi, normalizzati in probabilità, diventano i **pesi di attenzione**; con quei pesi si fa la **media pesata dei Value**. Metafora: in una stanza fai una domanda (Query); ogni persona ha un cartello con l'argomento che conosce (Key); ascolti di più chi ha il cartello più pertinente e prendi la sua informazione (Value).

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 620 170" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="ar2" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--accent)" stroke-width="1.6"/></marker></defs>
  <g font-size="13" fill="var(--ink)" text-anchor="middle">
   <rect x="12"  y="100" width="70" height="34" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="47"  y="122">The</text>
   <rect x="98"  y="100" width="82" height="34" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="139" y="122">animal</text>
   <rect x="196" y="100" width="80" height="34" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="236" y="122">didn't</text>
   <rect x="292" y="100" width="76" height="34" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="330" y="122">cross</text>
   <rect x="384" y="100" width="72" height="34" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="420" y="122">the</text>
   <rect x="472" y="100" width="86" height="34" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="515" y="122">street</text>
   <rect x="230" y="18"  width="76" height="34" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="268" y="40">it</text>
  </g>
  <g stroke="var(--accent)" stroke-width="2" fill="none" marker-end="url(#ar2)">
   <path d="M258,52 C210,72 165,82 141,98"/>
  </g>
  <g stroke="var(--muted)" stroke-width="1" fill="none" marker-end="url(#ar2)" opacity="0.45" stroke-dasharray="3 3">
   <path d="M272,52 C300,72 320,82 332,98"/>
   <path d="M285,50 C360,74 470,82 512,98"/>
  </g>
  <text x="150" y="80" font-size="11" fill="var(--accent)" text-anchor="middle">peso alto</text>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Self-attention: per capire a chi si riferisce "it", il modello attende con peso alto "the animal" (freccia piena) e con peso basso gli altri token (tratteggiate). Così "it" eredita il significato di "animal".</figcaption>
</figure>

**Multi-head attention (attenzione a più teste).** Non si fa una sola attention, ma **molte in parallelo** (le *head*, "teste"), ciascuna con le proprie Query/Key/Value. Ogni testa può specializzarsi su un tipo di relazione diversa: una segue i legami grammaticali (soggetto↔verbo), un'altra i riferimenti (pronome↔nome), un'altra ancora il tema. I risultati delle teste vengono poi ricombinati. È come avere più "punti di vista" simultanei sulla stessa frase.

**Positional encoding (codifica di posizione).** L'attention di per sé è "cieca all'ordine": guarderebbe i token come un insieme, non come una sequenza. Ma *"il cane morde l'uomo"* ≠ *"l'uomo morde il cane"*. Per questo si aggiunge a ogni embedding un'informazione sulla **posizione** del token nella sequenza (*positional encoding*), così il modello sa **chi viene prima e chi dopo**.

**Perché il transformer batte le RNN.** Prima dei transformer si usavano le **RNN = Recurrent Neural Network** ("reti neurali ricorrenti"), che leggono il testo **una parola alla volta in sequenza**, portandosi dietro uno "stato" che riassume il passato. Due limiti gravi:
- **Niente parallelismo:** dovendo processare in ordine, non puoi calcolare la parola 100 finché non hai fatto la 99. Addestramento lento.
- **Dipendenze lunghe:** l'informazione di inizio frase si "diluisce" mano a mano che passa di stato in stato, e su testi lunghi si perde.

Il transformer risolve entrambi: la self-attention **guarda tutti i token contemporaneamente** (→ enorme **parallelismo**, sfrutta le GPU, addestramento veloce) e collega direttamente due token **a qualsiasi distanza** con un solo passaggio (→ **dipendenze lunghe** gestite bene). È questa combinazione — parallelismo + dipendenze lunghe — ad aver reso possibili i modelli enormi di oggi.

**N layer.** Un transformer non ha un solo blocco di attention: ne impila **N** (decine o centinaia). Ogni layer raffina la rappresentazione prodotta dal precedente: i primi layer catturano relazioni locali (grammatica), quelli profondi concetti astratti e ragionamento.

---

## 4. Come nasce la risposta (decoding)

Ecco il punto che smitizza tutto: **l'LLM genera la risposta un token alla volta**, e ogni token è una nuova predizione basata su *tutto ciò che c'è finora* (il tuo prompt + i token già generati). Questo si chiama generazione **autoregressiva** ("auto-regressiva": si regge sul proprio output precedente).

Il ciclo, passo per passo:
1. L'input attuale passa attraverso i transformer (sez. 3).
2. All'ultimo strato il modello produce un punteggio grezzo (detto *logit*) **per ogni token del vocabolario**: "quanto è plausibile ciascun token come prossimo?".
3. Questi punteggi passano nella **softmax**, una funzione che li trasforma in una **distribuzione di probabilità**: tutti valori tra 0 e 1 che **sommano a 1**. Es. `azzurro` 0,62; `sereno` 0,15; `grigio` 0,08; ...
4. Si **sceglie un token** da questa distribuzione (come, sotto).
5. Il token scelto viene **accodato all'input** e si **torna al passo 1**. Si ripete finché non esce un token speciale di "fine" o si raggiunge il limite.

**Come si sceglie il token al passo 4 — le strategie di decoding:**
- **Greedy** ("goloso"): prendi **sempre** il token con probabilità più alta. Deterministico (stesso input → stessa uscita), ma tende a essere ripetitivo e piatto.
- **Sampling** ("campionamento"): **estrai a sorte** il token *rispettando le probabilità* (un token a 0,62 esce ~62% delle volte). Introduce varietà e creatività, ma anche imprevedibilità.

Due manopole controllano quanto il sampling è "audace":

- **Temperature (temperatura).** Un numero (tipicamente 0–2) che **appiattisce o accentua** la distribuzione prima di estrarre. **Bassa (→0):** accentua i picchi, il modello va quasi sempre sul token più probabile → risposte **prevedibili, precise, ripetibili** (di fatto tende al greedy). **Alta (>1):** appiattisce le probabilità, dà chance anche ai token improbabili → risposte **creative, varie, ma più a rischio di errori/incoerenze**. Regola pratica: bassa per compiti fattuali (estrazione dati, classificazione ticket), più alta per brainstorming e scrittura creativa.
- **Top-p (nucleus sampling).** Invece di considerare tutti i token, tieni solo i **più probabili la cui probabilità cumulata raggiunge p** (es. p = 0,9 → il "nucleo" che copre il 90% della probabilità) e scarti la coda lunga di token improbabili. Estrai solo da quel nucleo. Evita che, per sfortuna, esca un token assurdo dalla coda, mantenendo però varietà. (Parente: **top-k**, che tiene i k token più probabili in numero fisso.)

**In pratica a Glacom/MaiCare:** per il triage dei ticket o l'estrazione di dati strutturati vuoi **temperature bassa** (deterministico, ripetibile); per generare bozze di testo o suggerimenti vuoi temperature media con top-p.

---

## 5. Addestramento (a grandi linee)

Come impara un LLM a fare tutto questo? In tre fasi.

**a) Pre-training (pre-addestramento).** La fase principale, la più costosa. Il modello legge **enormi quantità di testo** (libri, siti web, codice) e viene allenato su un unico compito: **predire il token successivo**. Ogni volta che sbaglia la predizione, i suoi **parametri (pesi)** vengono aggiustati un pochino (via un algoritmo di ottimizzazione). Ripetuto su miliardi di frasi, il modello finisce per "assorbire" grammatica, fatti e schemi di ragionamento. **I parametri sono proprio questi numeri** — i pesi delle connessioni della rete — ed è lì che vive tutta la "conoscenza" del modello.

**b) Instruction tuning (messa a punto sulle istruzioni).** Un modello solo pre-addestrato sa completare testo, ma non necessariamente **seguire istruzioni** o rispondere in modo utile. Lo si affina ulteriormente su esempi del tipo *(istruzione → risposta desiderata)*, così impara il formato "assistente che risponde a una richiesta".

**c) RLHF = Reinforcement Learning from Human Feedback** ("apprendimento per rinforzo da feedback umano"). Serve ad allineare il modello a ciò che gli umani considerano **utile, onesto e innocuo**. Come funziona, a grandi linee: si mostrano a delle **persone** più risposte del modello alla stessa domanda e loro le **ordinano dalla migliore alla peggiore**. Con queste preferenze si addestra un **reward model** ("modello di ricompensa") che impara a dare un punteggio alle risposte; poi, con l'**apprendimento per rinforzo** (*reinforcement learning*: il modello riceve una "ricompensa" quando fa bene e aggiusta il comportamento per massimizzarla), si spinge l'LLM a produrre risposte che il reward model valuta alte. È la fase che rende un modello grezzo un **assistente educato e allineato**.

---

## Numeri e ordini di grandezza

**Context window tipiche.** Si va da poche migliaia di token dei modelli più vecchi fino a **centinaia di migliaia / milioni** di token nei modelli recenti (l'ordine di grandezza cresce di anno in anno). Più contesto = puoi dargli documenti lunghi interi, ma costa di più (paghi ~per token) e la finestra resta comunque **finita**.

**Cosa vuol dire "7B / 70B parametri".** Il numero di **parametri** (i pesi, sez. 5) è la misura della "taglia" del modello. **B = Billion = miliardi.** Quindi:
- **7B** = **7 miliardi** di parametri — modello "piccolo", gira anche su hardware modesto, veloce ed economico, buono per compiti semplici o self-hosting (es. sul server con vLLM).
- **70B** = **70 miliardi** — molto più capace su ragionamento e compiti complessi, ma richiede molta più memoria/GPU ed è più lento e costoso.

Regola generale (con eccezioni): **più parametri → più capacità, ma più costo e latenza.** La scelta della taglia è un trade-off ingegneristico, esattamente come dimensionare un server.

---

## Notable use cases (grandi aziende)

Solo fatti pubblici e generali, senza dettagli tecnici proprietari:

- **GPT — OpenAI.** La famiglia di modelli (**GPT = Generative Pre-trained Transformer**) resa celebre da ChatGPT, l'assistente che ha portato gli LLM al grande pubblico. Offerti soprattutto via API/prodotto (closed-weight).
- **Gemini — Google (DeepMind).** Famiglia di modelli di Google, integrata nei suoi prodotti e disponibile via API; noti per essere **multimodali** (testo, immagini, audio).
- **Claude — Anthropic.** Famiglia di assistenti con forte enfasi su **sicurezza e allineamento** (è il modello che stai usando ora), offerta via API e prodotto.
- **Llama — Meta.** Famiglia rilasciata come **open-weight** (i pesi sono scaricabili ed eseguibili in proprio), molto usata da chi vuole **self-hosting** e personalizzazione — rilevante quando servono controllo dei dati e costi (es. modelli eseguiti internamente).

Distinzione utile da ricordare: **closed-weight** (usi il modello solo via API di chi lo possiede) vs **open-weight** (scarichi i pesi e lo esegui/adatti tu). È una scelta chiave per privacy dei dati e costi in progetti reali.

---

## Completeness check (integrato da me)

Tre **limiti strutturali** da tenere sempre a mente (non sono bug, discendono da *come* funziona un LLM):

1. **Allucinazioni (hallucinations).** Il modello genera il token **più probabile**, non il più **vero**: quando non "sa", produce comunque testo plausibile e ben scritto, che può essere **falso** (nomi, cifre, citazioni inventate). Non ha un meccanismo interno che distingue "lo so" da "lo sto inventando".
2. **Knowledge cutoff (data di taglio della conoscenza).** Il modello conosce solo ciò che era nel testo di addestramento **fino a una certa data**. Eventi successivi gli sono **ignoti** — non è "connesso" al mondo di default.
3. **Nessun accesso ai dati privati.** Non conosce i **tuoi** documenti (i ticket di Glacom, le cartelle di MaiCare, i PDF interni): quei dati non erano nell'addestramento.

**L'aggancio → RAG.** Questi tre limiti si affrontano con la **RAG = Retrieval-Augmented Generation** ("generazione aumentata dal recupero", topic `xc-llm-rag`): invece di fidarsi solo della memoria interna, **prima si recuperano** i documenti pertinenti (usando gli embedding e la similarità coseno della sez. 2!) e **poi si mettono nel contesto** del modello, così risponde su dati **aggiornati, privati e verificabili**, riducendo le allucinazioni. Ecco perché embedding e context window, viste qui, sono i mattoni della prossima lezione.

---

## Fonti

- **"Attention Is All You Need"**, Vaswani et al., 2017 — il paper che introduce il transformer: `arxiv.org/abs/1706.03762`
- **"The Illustrated Transformer"**, Jay Alammar — la spiegazione visuale più famosa di attention e transformer: `jalammar.github.io/illustrated-transformer/`
- **Hugging Face — Learn / NLP Course** — corsi gratuiti su token, embedding, transformer e uso pratico dei modelli: `huggingface.co/learn`

---

## Concetti adiacenti

- `xc-llm-rag` — **RAG**: dare al modello documenti aggiornati/privati recuperandoli e mettendoli nel contesto (risolve i 3 limiti visti sopra).
- `xc-llm-prompting` — **Prompting**: come scrivere l'input per guidare l'output, sfruttando context window e temperature.
- `xc-llm-vectordb` — **Vector database**: dove si salvano gli embedding e come si cercano per similarità coseno su larga scala.
- `ml-nn` — **Reti neurali**: le fondamenta (neuroni, pesi, addestramento) su cui poggia l'architettura transformer.

---

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cosa significa **LLM** e qual è l'unico compito base su cui è addestrato?
2. Cos'è un **token** e perché i modelli usano pezzi di parola (subword/**BPE**) invece di parole intere? Cosa vuol dire **BPE**?
3. Cos'è la **context window** e cosa succede a ciò che la eccede?
4. Cos'è un **embedding** e qual è la sua proprietà fondamentale rispetto ai significati?
5. Scrivi la **formula della similarità coseno** e di' tra quali valori sta il risultato e cosa significano gli estremi.
6. Spiega la **self-attention** in una frase e di' cosa rappresentano **query, key e value**.
7. Perché il transformer **batte le RNN**? Cita i due vantaggi. Cosa vuol dire **RNN**?
8. Descrivi il ciclo **autoregressivo** di generazione: cosa fa la **softmax** e cosa distingue **greedy** da **sampling**?
9. Cosa controlla la **temperature**? Cosa succede con temperature bassa vs alta?
10. Cosa vuol dire **RLHF** (per esteso) e a cosa serve? E cosa significa "**7B parametri**"?

<details><summary>Risposte</summary>

1. **LLM = Large Language Model** (grande modello linguistico). L'unico compito base è **predire il token (pezzo di parola) successivo più probabile** dato il testo precedente; da questa singola capacità emergono tutte le altre.
2. Un **token** è un **pezzo di parola** (subword). Si usano i pezzi perché le parole intere sono troppe (vocabolario enorme e incompleto), non gestirebbero parole mai viste, e i pezzi frequenti si riusano (efficienza). **BPE = Byte Pair Encoding**: parte dai caratteri e **fonde ripetutamente le coppie di simboli più frequenti** in un token unico.
3. La **context window** è il numero **massimo di token** che il modello considera **tutti insieme** in una chiamata (input + risposta). Ciò che la eccede **non esiste** per il modello: viene tagliato e "dimenticato".
4. Un **embedding** è un **vettore di numeri** che rappresenta il significato di un token. Proprietà fondamentale: **significati simili → vettori vicini** nello spazio; significati diversi → vettori lontani.
5. **cosine similarity(A, B) = (A · B) / (‖A‖ · ‖B‖)** (prodotto scalare diviso il prodotto delle lunghezze). Il risultato va da **−1 a +1**: **+1** = stessa direzione (molto simili), **0** = non correlati, **−1** = opposti. Misura l'**angolo**, non la distanza.
6. **Self-attention:** per ogni token, il modello **guarda tutti gli altri token e pesa quali sono rilevanti**, rappresentando il token come miscela pesata delle loro informazioni. **Query** = cosa il token cerca; **Key** = di cosa ogni token "parla" (l'etichetta da confrontare con la query); **Value** = l'informazione che il token porta e che viene mescolata secondo i pesi.
7. **RNN = Recurrent Neural Network** (rete neurale ricorrente), legge in sequenza una parola alla volta. Il transformer la batte per (1) **parallelismo** — la self-attention guarda tutti i token insieme, sfruttando le GPU — e (2) **dipendenze lunghe** — collega direttamente token a qualsiasi distanza senza che l'informazione si diluisca.
8. **Autoregressivo:** il modello genera **un token alla volta**; ogni token scelto viene accodato all'input e il ciclo riparte. La **softmax** trasforma i punteggi grezzi (logit) in una **distribuzione di probabilità** (valori tra 0 e 1 che sommano a 1). **Greedy** = prendi sempre il token più probabile (deterministico); **sampling** = estrai a sorte rispettando le probabilità (vario/creativo).
9. La **temperature** appiattisce o accentua la distribuzione prima di estrarre. **Bassa (→0):** accentua i picchi → risposte prevedibili, precise, ripetibili (tende al greedy). **Alta (>1):** appiattisce → risposte creative e varie, ma più a rischio di errori/incoerenze.
10. **RLHF = Reinforcement Learning from Human Feedback** (apprendimento per rinforzo da feedback umano): allinea il modello a risposte utili/oneste/innocue, usando preferenze umane per addestrare un reward model e poi rinforzando le risposte ben valutate. **"7B parametri" = 7 miliardi** (B = Billion) **di parametri/pesi**: un modello relativamente piccolo, veloce ed economico.
</details>
