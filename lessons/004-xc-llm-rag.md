---
day: 4
topic_id: xc-llm-rag
title: "RAG — tipi e architetture (naive, advanced, hybrid, graph, agentic)"
area: cross-cutting
course: LLM / AI Engineering
grounded_in: null
adjacent: [xc-llm-fundamentals, xc-llm-vectordb, xc-llm-agents, dm-ai]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun acronimo lasciato senza definizione."
---

# RAG — tipi e architetture

> **Perché oggi:** questa è la lezione centrale. A Glacom porti RAG in produzione, e hai già fatto un tuo benchmark che confronta diverse architetture RAG sulle stesse domande. Per il ruolo target di **AI/LLM Engineer** devi sapere spiegare a memoria i cinque tipi di RAG, quando usarli, e — soprattutto — perché "più sofisticato" non vince quasi mai in automatico. Oggi metti in fila tutto: dal RAG più ingenuo a quello agentico, con i tool veri che useresti.

## Cos'è RAG e il problema che risolve

**RAG** = **Retrieval-Augmented Generation** (generazione aumentata dal recupero). È un pattern in cui, prima di far rispondere l'LLM, **recuperi** (retrieval) i pezzi di testo rilevanti da una tua base di conoscenza e li **infili nel prompt** come contesto, così l'LLM risponde basandosi su quelli invece che sulla sola memoria interna.

Il problema che risolve nasce da tre limiti di un LLM "nudo":

- **Knowledge cutoff** (data di taglio della conoscenza): l'LLM sa solo ciò che ha visto durante l'addestramento, fino a una certa data. Tutto ciò che è successo dopo, o che non era pubblico, semplicemente non lo conosce.
- **Documenti privati**: il modello non ha mai visto i contratti, i ticket, i manuali interni della tua azienda. Non stavano nel suo training set.
- **Allucinazione** (hallucination): quando non sa, l'LLM tende comunque a produrre una risposta plausibile ma **inventata**, con tono sicuro. Non ti dice "non lo so"; riempie il vuoto.

La soluzione di RAG è il **grounding** (ancoraggio): fornire all'LLM, dentro al prompt, il testo-sorgente da cui deve ricavare la risposta, così che la generi *ancorata* a documenti reali e verificabili (spesso con citazioni). Se la risposta deve venire da un chunk che gli hai passato, il modello ha molto meno spazio per inventare.

Definizioni compatte:

- **Grounding**: ancorare la risposta del modello a fonti concrete passate nel contesto, così è verificabile e meno inventata.
- **Allucinazione**: output linguisticamente fluente ma factualmente falso, prodotto quando il modello "riempie i buchi".
- **Knowledge cutoff**: la data oltre la quale il modello non ha conoscenza, perché il suo addestramento si è fermato lì.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 220" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arRag1" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
   <rect x="8" y="30" width="120" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="68" y="47">Domanda</text><text x="68" y="62">utente</text>
   <rect x="8" y="140" width="120" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="68" y="157">Embedding</text><text x="68" y="172">della domanda</text>
   <rect x="170" y="140" width="150" height="42" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="245" y="157">Vector DB</text><text x="245" y="172">ricerca top-k</text>
   <rect x="360" y="140" width="130" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="425" y="157">Chunk</text><text x="425" y="172">recuperati</text>
   <rect x="360" y="30" width="130" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="425" y="47">Prompt</text><text x="425" y="62">domanda + chunk</text>
   <rect x="530" y="30" width="110" height="42" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="585" y="54">LLM</text>
   <rect x="530" y="140" width="180" height="42" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="620" y="157">Risposta</text><text x="620" y="172">con citazioni</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arRag1)">
   <path d="M68,72 L68,138"/>
   <path d="M128,161 L168,161"/>
   <path d="M320,161 L358,161"/>
   <path d="M425,138 L425,74"/>
   <path d="M490,51 L528,51"/>
   <path d="M585,72 L585,120 L620,120 L620,138"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Pipeline RAG base: la domanda diventa un vettore, cerca i chunk simili nel Vector DB, quelli entrano nel prompt insieme alla domanda, l'LLM genera la risposta ancorata alle fonti.</figcaption>
</figure>

## I mattoni (che servono a tutti i tipi)

Qualunque tipo di RAG, dal più ingenuo all'agentico, poggia sugli stessi mattoni. Se questi li hai chiari, ogni architettura è solo un modo diverso di combinarli.

- **Chunking** (spezzettamento): un documento intero è troppo grande per essere passato al modello, e comunque diluirebbe il segnale. Lo spezzi in **chunk** — pezzi di testo di poche centinaia di token (es. 200–800 token, spesso con un piccolo *overlap* di sovrapposizione per non tagliare frasi a metà). **Token** = l'unità in cui il modello legge il testo (circa 3/4 di parola in inglese). Trade-off: chunk **piccoli** = recupero preciso ma rischi di perdere il contesto attorno; chunk **grandi** = più contesto ma più rumore e più token spesi. Tool tipici: gli `TextSplitter` di LangChain (es. `RecursiveCharacterTextSplitter`) o i `NodeParser` di LlamaIndex.
- **Embedding** (immersione/vettorializzazione): trasformi ogni chunk in un **vettore** (una lista di numeri, es. 384, 768 o 1536 dimensioni) che rappresenta il suo *significato*. Testi con significato simile finiscono vicini nello spazio vettoriale. Modelli reali: **OpenAI `text-embedding-3`** (small e large), **Cohere** (`embed-v3`), e i modelli open **sentence-transformers** (es. `all-MiniLM-L6-v2`, `bge`, `e5`) che giri in locale gratis.
- **Vector DB / indice** (database vettoriale): memorizza tutti i vettori dei chunk e, data una query vettorizzata, ti restituisce i più simili in fretta. Tool reali: **FAISS** (libreria in-memory di Facebook/Meta, ottima per iniziare), **Pinecone** (servizio gestito cloud), **Weaviate**, **Qdrant**, e **pgvector** (estensione di PostgreSQL: vettori dentro al tuo Postgres). Per cercare veloce non fa un confronto esatto con tutti i vettori (troppo lento su milioni), ma usa la **ANN** = **Approximate Nearest Neighbor** (ricerca dei vicini più prossimi in modo *approssimato*): trova quasi-sempre i più simili ma in tempo enormemente inferiore, tipicamente con indici tipo HNSW (grafi di vicinato).
- **Similarità coseno** (cosine similarity): il modo standard per misurare "quanto due vettori si somigliano". A parole: guarda l'**angolo** tra i due vettori, non la loro lunghezza. Se puntano nella stessa direzione, la similarità è vicina a 1 (molto simili); se sono perpendicolari, vicina a 0 (scorrelati). È così che il Vector DB decide quali chunk sono "vicini" alla domanda.
- **top-k**: il numero **k** di chunk più simili che decidi di recuperare (es. top-5 = i 5 chunk più vicini). Pochi = rischi di perdere il pezzo giusto; troppi = riempi il prompt di rumore e spendi token.

## I tipi di RAG (dal più semplice al più sofisticato)

Li vediamo in ordine crescente di sofisticazione. Per ciascuno: **come funziona**, il **difetto** che risolve rispetto al precedente, e **quando** usarlo.

### 1. Naive RAG

Il RAG "da manuale", la versione base. Flusso: **embed** (vettorizzi la domanda) → **retrieve** (prendi i top-k chunk più simili dal Vector DB) → **stuff** (li impacchetti tutti nel prompt) → **generate** (l'LLM risponde).

- *Come funziona*: una sola ricerca semantica, k fisso, nessun ritocco della query né dei risultati.
- *Difetti*: recupero **impreciso** (la similarità coseno può ingannarsi), spesso finiscono nel contesto **chunk irrilevanti**, e non gestisce **query complesse** o ambigue (una domanda che richiede più informazioni sparse fallisce).
- *Quando usarlo*: prototipo, dominio piccolo e pulito, domande dirette "cosa dice il documento su X". È il punto di partenza corretto: fallo funzionare, poi migliora.

### 2. Advanced RAG

Stesso scheletro, ma aggiungi migliorie **prima** del retrieval (pre-retrieval) e **dopo** (post-retrieval) per alzare la precisione.

- **Query rewriting / expansion** (riscrittura / espansione della query): riformuli la domanda dell'utente in una o più query migliori per la ricerca (es. sciogli i pronomi, aggiungi sinonimi), così peschi meglio.
- **HyDE** = **Hypothetical Document Embeddings** (embedding di documento ipotetico): invece di cercare con la *domanda*, chiedi prima all'LLM di **inventare una risposta plausibile** alla domanda, poi vettorizzi *quella risposta finta* e con essa cerchi nel Vector DB. Idea: una risposta ipotetica assomiglia (nello spazio vettoriale) ai chunk-risposta veri più di quanto vi assomigli la domanda.
- **Reranking** (riordino): dopo aver recuperato, poniamo, i primi 20 chunk con la ricerca veloce, passi ognuno insieme alla domanda a un **cross-encoder**, un modello che legge *coppia (domanda, chunk) insieme* e assegna un punteggio di rilevanza fine. È più lento ma molto più accurato del confronto vettoriale, perciò lo usi solo per riordinare i pochi candidati e tenere i migliori (es. i top-5 dopo il rerank). Tool reali: **Cohere Rerank**, i cross-encoder di **sentence-transformers**, il reranker di **BGE**.
- **Metadata filtering** (filtro sui metadati): ai chunk associ metadati (data, autore, cliente, tipo documento) e filtri la ricerca (es. "solo documenti del 2025 del cliente X"), riducendo il campo prima ancora di misurare la similarità.
- **Chunk migliori**: chunking più intelligente (per struttura del documento, per paragrafo, gerarchico), così ogni chunk è auto-contenuto.
- *Difetto del naive che risolve*: la scarsa precisione del recupero e i chunk irrilevanti.
- *Quando usarlo*: quasi sempre in produzione seria; il **reranking** in particolare è spesso il singolo miglioramento con più ritorno rispetto allo sforzo.

### 3. Hybrid RAG (retrieval ibrido)

Combini due modi diversi di cercare e ne **fondi** i risultati.

- **Ricerca densa** (dense retrieval): quella per **embedding**, cattura il *significato*. Trova chunk che parlano della stessa cosa anche con parole diverse (sinonimi, parafrasi).
- **Ricerca sparsa / lessicale** (sparse / lexical retrieval): cerca per **parole chiave esatte**, tipicamente con **BM25**. **BM25** (Best Matching 25) è l'algoritmo classico dei motori di ricerca testuale: a parole, premia i documenti in cui compaiono i termini della query, dando più peso ai termini **rari** (discriminanti) e correggendo per la lunghezza del documento e per la ripetizione (un termine ripetuto 10 volte non vale 10 volte 1). Non capisce i sinonimi, ma è imbattibile su termini **esatti**: codici prodotto, sigle, nomi propri, numeri di articolo.
- *Perché fondere le due*: la densa prende il **significato**, la lessicale prende i **termini esatti** che la densa spesso "sfuma". Query come "errore E-4021 sul modulo Alba" hanno bisogno di entrambe: il concetto *e* il codice preciso.
- **Fusione con RRF** = **Reciprocal Rank Fusion** (fusione per rango reciproco): come unisci due classifiche diverse (una dalla densa, una dalla lessicale)? Con RRF: ad ogni documento dai un punteggio pari alla somma di `1 / (k + rango)` sulle due liste (k è una costante piccola, es. 60). Vale la **posizione** in classifica, non i punteggi (che sono su scale incomparabili). Un documento che sta in alto in *entrambe* le liste vince; così premi il consenso tra i due metodi senza dover normalizzare punteggi eterogenei. Supportato nativamente da Weaviate, Qdrant, Elasticsearch/OpenSearch e dai retriever ibridi di LangChain/LlamaIndex.
- *Difetto dell'advanced che risolve*: la ricerca puramente semantica che manca i match esatti (codici, sigle, nomi).
- *Quando usarlo*: domini con tanta terminologia tecnica, codici, ID, nomi propri — cioè quasi ogni base di conoscenza aziendale reale.

### 4. Graph RAG

Invece di cercare tra chunk isolati, costruisci un **knowledge graph** (grafo della conoscenza) dai documenti.

- *Come funziona*: con l'LLM estrai dai testi le **entità** (persone, prodotti, aziende, concetti) come **nodi** e le **relazioni** tra loro come **archi** (es. "Alba Trasporti" —*fornisce*→ "Cliente X"). Al momento della domanda **navighi il grafo**: parti dalle entità citate e segui gli archi per raccogliere il contesto connesso, invece di sperare che stia tutto in un chunk.
- *Difetto che risolve*: le domande **multi-hop** (a più salti) e sulle **relazioni**, dove la risposta si costruisce collegando informazioni sparse in documenti diversi. Esempio: "quali clienti sono serviti da fornitori che hanno avuto un ritardo nel 2025?" — un salto solo non basta.
- *Costo*: **più costoso da costruire e mantenere** (devi estrarre entità/relazioni, tenere il grafo aggiornato). Tool/approcci reali: **Microsoft GraphRAG**, LangChain con **Neo4j** (database a grafo), i `KnowledgeGraphIndex` di LlamaIndex.
- *Quando usarlo*: domande relazionali e multi-hop, sintesi globale su tutto il corpus ("temi ricorrenti nei ticket"). Non per semplici lookup: lì è overkill (e nel mio benchmark il graph puro ha proprio perso — vedi sotto).

### 5. Agentic RAG

Il retrieval smette di essere un passo fisso e diventa una **decisione** presa da un **agente**.

- **Agente** (agent): un LLM messo in un ciclo in cui può **ragionare, scegliere azioni (tool) e usare i risultati** per decidere il passo successivo, iterando finché non ha abbastanza per rispondere (collega al topic **xc-llm-agents**).
- *Come funziona*: l'agente decide **dinamicamente** se recuperare (a volte non serve), **cosa** cercare, **quante volte** iterare, se **riformulare** la query dopo un recupero deludente, e **quali fonti/tool** usare (Vector DB, ricerca web, chiamata a un'API, un database SQL). Può fare più giri: cerca, valuta se basta, cerca ancora meglio.
- *Difetto che risolve*: la rigidità di tutti i precedenti — un solo giro, k fisso, una sola strategia. Su domande composte o che richiedono più fonti, un flusso fisso fallisce; l'agente adatta.
- *Costo*: più chiamate all'LLM, più **latenza** e più **imprevedibilità** (può loopare o divagare). Va messo con guardrail e limiti di iterazione.
- *Quando usarlo*: domande eterogenee e complesse, più fonti, quando serve decidere *se* e *come* recuperare invece di farlo sempre uguale. Framework reali: i costrutti agentici di **LangGraph**, gli agenti di **LlamaIndex**.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 260" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arRag2" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
   <rect x="130" y="14" width="140" height="38" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="200" y="38">Naive</text>
   <rect x="230" y="62" width="150" height="38" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="305" y="86">Advanced</text>
   <rect x="330" y="110" width="150" height="38" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="405" y="134">Hybrid</text>
   <rect x="430" y="158" width="150" height="38" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="505" y="182">Graph</text>
   <rect x="530" y="206" width="160" height="38" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="610" y="230">Agentic</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none" marker-end="url(#arRag2)">
   <path d="M270,33 L228,52"/>
   <path d="M380,81 L328,100"/>
   <path d="M480,129 L428,148"/>
   <path d="M580,177 L528,196"/>
  </g>
  <g font-size="11" fill="var(--muted)" text-anchor="start">
   <text x="14" y="40">↑ semplicità</text>
   <text x="14" y="232">↑ qualità potenziale,</text>
   <text x="14" y="246">costo e latenza</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">La scala dei 5 tipi: salendo cresce la qualità potenziale, ma anche costo, latenza e complessità. Più in alto non è automaticamente meglio — dipende dalle domande reali.</figcaption>
</figure>

## Un mio benchmark (case study reale)

Ho confrontato diverse architetture RAG sullo **stesso set di domande**, misurando token spesi per risposta e qualità della risposta.

Un approccio **ibrido con router** ha ridotto i token usati per risposta di circa l'**87%** (da **~1282 a ~165 token**, circa un ottavo) **mantenendo** la qualità: punteggio qualità **4,00 su 5** contro **3,92** del baseline più pesante (il *full-context stuffing*, cioè infilare tutto il contesto nel prompt). Una variante **graph-RAG puro** spingeva i token ancora più in basso (~150) **ma la qualità crollava a 3,17**: falliva sulle domande *aggregate* (quelle senza un'entità nominata, es. "elenca i clienti in trattativa"). Proprio quel fallimento è la ragione del **router + fallback obbligatorio** — il numero conta meno della diagnosi.

Cos'è un **router** qui: è il componente che, ricevuta una domanda, **sceglie la strategia di retrieval** giusta per *quella* query — ad esempio decide se fare ricerca densa, lessicale, ibrida, o addirittura se serve recuperare. Invece di applicare sempre la pipeline più pesante a tutte le domande, il router indirizza ognuna verso il percorso minimo sufficiente. È così che l'ibrido+router taglia i token: non spreca contesto su domande semplici.

**Lezione**: più sofisticato non è automaticamente meglio. L'**ibrido + router** vinceva sull'**efficienza a parità di qualità** (stessa qualità, un ottavo dei token), mentre il **graph-RAG puro** — più complesso — è risultato il peggiore in qualità su questo set. Misura sempre sulle tue domande vere, prima di scegliere l'architettura.

## Notable use cases (grandi aziende)

RAG è il pattern dietro a moltissimi prodotti reali:

- **Assistenti sulla documentazione aziendale**: fai domande in linguaggio naturale al manuale interno, alle policy, alla knowledge base tecnica, e ricevi risposte con citazioni alle pagine.
- **Customer support su knowledge base**: il bot risponde ai clienti pescando dagli articoli di supporto e dalla FAQ, riducendo i ticket che arrivano agli umani.
- **Ricerca legale e medica con citazioni**: interrogare corpus di sentenze, normative o letteratura clinica, con la risposta ancorata alle fonti citate (dove la verificabilità è obbligatoria).
- È il pattern dietro praticamente ogni **"chatta col tuo PDF" / "chatta con la tua knowledge base"**: sotto il cofano c'è chunking + embedding + Vector DB + generazione ancorata.

## Quando NON serve RAG

RAG aggiunge complessità e latenza: non è gratis. Evitalo quando:

- **La conoscenza è già nel modello**: domande di cultura generale o su nozioni pubbliche ben note — l'LLM le sa già, recuperare è inutile.
- **Basta il fine-tuning**: se ti serve *comportamento/stile/formato* costante (non fatti freschi), meglio addestrare il modello su esempi (aggancio a **xc-llm-finetune**). Regola pratica: RAG per la **conoscenza** che cambia, fine-tuning per il **comportamento** stabile.
- **I dati stanno in un DB strutturato**: se la risposta è "quanti ordini a giugno", non spezzetti tabelle in chunk — usi **text-to-SQL** (l'LLM genera la query SQL, il database dà il numero esatto). RAG semantico su dati numerici/tabellari è lo strumento sbagliato.

## Fonti

- Lewis et al., *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*, arXiv 2020 — il paper che introduce RAG.
- *"Retrieval-Augmented Generation for Large Language Models: A Survey"*, arXiv — survey che sistematizza Naive / Advanced / Modular RAG.
- Documentazione **LangChain** — python.langchain.com (retriever, splitter, reranking, hybrid, LangGraph).
- Documentazione **LlamaIndex** — docs.llamaindex.ai (node parser, query engine, knowledge graph index, agenti).

## Concetti adiacenti

- **xc-llm-vectordb**: come funzionano dentro gli indici vettoriali (HNSW, ANN) e i Vector DB che RAG usa per il retrieval.
- **xc-llm-agents**: il ciclo ragiona-agisci-osserva che sta sotto l'Agentic RAG.
- **xc-llm-fundamentals**: token, embedding, prompt e contesto — i concetti base su cui poggia tutto RAG.
- **dm-ai**: fondamenti di data mining / machine learning (spazi vettoriali, similarità) che danno intuizione alla ricerca densa.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cosa significa la sigla RAG e cosa fa in una frase?
2. Cos'è un **chunk** e qual è il trade-off tra chunk piccoli e grandi?
3. Cosa vuol dire **knowledge cutoff** e perché è un problema che RAG risolve?
4. Qual è la differenza tra ricerca **densa** e ricerca **lessicale/sparsa**?
5. Cos'è il **reranking** e con quale tipo di modello si fa?
6. Cosa fa un **router** in un sistema RAG?
7. Che differenza c'è tra **Graph RAG** e **Agentic RAG**?
8. Cos'è **RRF** e a cosa serve nel retrieval ibrido?
9. Nel mio benchmark, di quanto sono scesi i token con l'ibrido+router e la qualità è calata?
10. Cita due situazioni in cui **NON** conviene usare RAG.

<details><summary>Risposte</summary>

1. **RAG = Retrieval-Augmented Generation**. Recupera i pezzi di testo rilevanti da una base di conoscenza e li infila nel prompt come contesto, così l'LLM risponde ancorato a quelli (grounding) invece che alla sola memoria interna.
2. Un **chunk** è un pezzo di documento (poche centinaia di token) in cui spezzi i testi per poterli vettorizzare e recuperare. Trade-off: chunk **piccoli** = recupero più preciso ma rischio di perdere il contesto attorno; chunk **grandi** = più contesto ma più rumore e più token spesi.
3. **Knowledge cutoff** = la data oltre la quale il modello non ha conoscenza, perché l'addestramento si è fermato lì; non conosce eventi successivi né i tuoi documenti privati. RAG lo risolve fornendo quei documenti nel prompt al momento della domanda.
4. **Densa** = ricerca per embedding, cattura il *significato* (trova anche sinonimi e parafrasi). **Lessicale/sparsa** = ricerca per parole chiave esatte (es. BM25), imbattibile su codici, sigle, nomi propri, ma non capisce i sinonimi.
5. **Reranking** = riordinare i chunk recuperati per rilevanza fine, passando ogni coppia (domanda, chunk) a un **cross-encoder**, un modello che legge domanda e chunk *insieme* e dà un punteggio più accurato del confronto vettoriale; si tiene poi i migliori. Tool: Cohere Rerank, cross-encoder sentence-transformers, BGE reranker.
6. Un **router** riceve la domanda e **sceglie la strategia di retrieval** giusta per quella query (densa, lessicale, ibrida, o nessun recupero), indirizzandola verso il percorso minimo sufficiente invece di applicare sempre la pipeline più pesante.
7. **Graph RAG**: costruisci un knowledge graph (entità = nodi, relazioni = archi) dai documenti e recuperi navigando il grafo, utile per domande multi-hop e relazionali. **Agentic RAG**: un agente decide dinamicamente se/cosa/quante volte recuperare, riformula, usa più fonti/tool e itera. In breve: Graph cambia la *struttura dati* del recupero; Agentic cambia il *controllo* (chi decide come recuperare).
8. **RRF = Reciprocal Rank Fusion**. Serve a fondere due classifiche diverse (densa e lessicale) sommando per ogni documento `1/(k+rango)` sulle due liste: usa le posizioni, non i punteggi incomparabili, e premia i documenti in alto in entrambe le liste.
9. I token sono scesi di circa l'**87%** (da ~1282 a ~165 per risposta, circa un ottavo) e la qualità **NON** è calata: **4,00** su 5 contro **3,92** del baseline più pesante. (La variante solo-grafo scendeva anche più in basso ma perdeva qualità, 3,17.)
10. Due tra: (a) la conoscenza è già nel modello (nozioni pubbliche note); (b) serve solo comportamento/stile/formato → meglio fine-tuning; (c) i dati stanno in un DB strutturato → meglio text-to-SQL.

</details>
