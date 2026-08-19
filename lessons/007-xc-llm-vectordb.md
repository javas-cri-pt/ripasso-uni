---
day: 7
topic_id: xc-llm-vectordb
title: "Vettorializzazione, embedding, indicizzazione e retrieval (pratico)"
area: cross-cutting
course: LLM / AI Engineering
grounded_in: null
adjacent: [xc-llm-rag, xc-llm-fundamentals, prog-ds]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun termine lasciato senza definizione. Taglio pratico."
---

# Vettorializzazione, embedding, indicizzazione e retrieval

> **Perché oggi:** questo è il motore che gira sotto ogni RAG e ogni chatbot che costruisci a Glacom. Quando dici "metto i documenti in un vector DB e li cerco", stanno succedendo quattro cose concrete. Oggi non guardi la teoria: guardi i mattoni pratici e i tool veri con cui li costruisci, così sai cosa scegliere e perché.

## Il percorso di un documento (dalla parola al risultato)

Ogni sistema che "cerca per significato" si divide in due fasi, ed è utilissimo tenerle separate in testa.

**Indicizzazione (offline, la fai una volta).** Prendi i tuoi documenti, li prepari e li carichi in una struttura pronta per essere cercata. È un lavoro batch: lo fai quando arrivano documenti nuovi o cambiano, non ad ogni domanda. Se hai 10.000 PDF, li indicizzi una volta e poi vivi di rendita.

**Retrieval (a runtime, ad ogni domanda).** Arriva la domanda dell'utente, la trasformi anche lei in vettore, cerchi nell'indice i pezzi più simili e li restituisci. Questo accade in tempo reale, deve essere veloce (millisecondi), e succede migliaia di volte.

I quattro verbi che incontrerai, in ordine:

1. **Vettorializzare** — trasformare un testo in numeri che ne catturano il significato.
2. **Indicizzare** — organizzare quei numeri in una struttura che si cerca in fretta.
3. **Cercare** — dato il vettore di una domanda, trovare i vettori più vicini.
4. **Riordinare** — rimettere in ordine i candidati per qualità prima di usarli.

I primi due appartengono alla fase offline, gli ultimi due al runtime.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 160" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arVdbIdx" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
   <rect x="8" y="58" width="96" height="44" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="56" y="78">Documenti</text><text x="56" y="92" font-size="9.5" fill="var(--muted)">PDF, web, DB</text>
   <rect x="120" y="58" width="96" height="44" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="168" y="78">Loader</text><text x="168" y="92" font-size="9.5" fill="var(--muted)">estrai testo</text>
   <rect x="232" y="58" width="96" height="44" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="280" y="78">Chunking</text><text x="280" y="92" font-size="9.5" fill="var(--muted)">spezza</text>
   <rect x="344" y="58" width="108" height="44" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="398" y="76">Embedding</text><text x="398" y="90" font-size="9.5" fill="var(--muted)">model</text>
   <rect x="468" y="58" width="96" height="44" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="516" y="78">Vettori</text><text x="516" y="92" font-size="9.5" fill="var(--muted)">liste di numeri</text>
   <rect x="580" y="58" width="130" height="44" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="645" y="76">Indice /</text><text x="645" y="90">Vector DB</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arVdbIdx)">
   <path d="M104,80 L118,80"/><path d="M216,80 L230,80"/><path d="M328,80 L342,80"/><path d="M452,80 L466,80"/><path d="M564,80 L578,80"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Fase di indicizzazione: si fa offline, una volta. I documenti diventano testo, poi pezzi, poi vettori, poi entrano nell'indice.</figcaption>
</figure>

## 1. Vettorializzazione ed embedding (in pratica)

**Vettorializzazione** significa trasformare un testo in un **vettore**, cioè una lista di numeri (es. `[0.021, -0.44, 0.17, ...]`) che ne cattura il significato. Due frasi che vogliono dire cose simili producono vettori vicini nello spazio; due frasi lontane come significato producono vettori lontani. È così che una macchina "misura" la somiglianza di senso senza capire le parole come noi.

Il pezzo che fa questa trasformazione si chiama **embedding model** (modello di embedding). Praticamente è una scatola: gli dai in ingresso del testo, ti restituisce un vettore di **N dimensioni** (N è quanti numeri ha la lista). Valori tipici che vedrai: **384**, **768**, **1536** dimensioni. Più dimensioni non vuol dire sempre meglio: significano vettori più "ricchi" ma anche più pesanti da salvare e confrontare.

Modelli reali, con le caratteristiche pratiche che ti interessano davvero (quante dimensioni, se gira in locale o via API, il compromesso costo/qualità):

- **OpenAI `text-embedding-3-small` / `text-embedding-3-large`** — via API (paghi a chiamata, i dati escono verso OpenAI). Lo `small` è economico e buono per la maggior parte dei casi; il `large` costa di più ed è più accurato. Zero da gestire, ma serve connessione e budget.
- **Cohere `embed-v3`** — anch'esso via API, forte sul multilingua e pensato per la ricerca; ha varianti ottimizzate per query e per documenti.
- **Open-source con `sentence-transformers`** (libreria Python) — girano **in locale**, sul tuo hardware, senza mandare dati fuori:
  - **`all-MiniLM-L6-v2`** — piccolo (384 dimensioni), veloce, ottimo per partire e per prototipi; leggero anche su CPU.
  - **`bge`** (famiglia BAAI, es. `bge-base`, `bge-large`) — qualità alta, molto usato in produzione open-source.
  - **`e5`** (famiglia intfloat, es. `e5-base`) — forte sul retrieval, richiede prefissi tipo `query:` e `passage:` per distinguere domande da documenti.

La scelta locale vs API è pratica: **API** = zero gestione ma costo per chiamata e dati che escono (attenzione a dati sensibili dei clienti); **locale** = controllo totale, dati che restano da te, ma devi avere l'hardware e gestirlo.

**Regola d'oro:** usa **lo stesso modello di embedding per indicizzare e per cercare**. I vettori dei documenti e il vettore della domanda devono vivere nello **stesso spazio** (stesse dimensioni, stesso "modo di misurare"), altrimenti confronti mele con pere e il retrieval restituisce spazzatura. Se un giorno cambi modello, devi **re-indicizzare tutto** da capo.

Un cenno intuitivo alla similarità, senza formule: il modo più comune di misurare quanto due vettori sono vicini è la **similarità coseno**, che guarda l'**angolo** tra i due vettori, non la loro lunghezza. Due testi "puntano nella stessa direzione" (angolo piccolo) quando parlano della stessa cosa, a prescindere da quanto sono lunghi. È per questo che una frase corta e un paragrafo lungo sullo stesso argomento possono risultare molto simili.

## 2. Chunking (come spezzi i documenti)

Non si vettorializza un intero PDF in un colpo solo. Primo, i modelli di embedding hanno un limite di quanto testo accettano per volta. Secondo, e più importante: un vettore solo per 40 pagine "spalma" troppi significati diversi in un unico punto, e quando cerchi non recuperi il paragrafo giusto ma "tutto il documento", che è inutile. Per questo si fa il **chunking**: spezzi il documento in pezzi (**chunk**) più piccoli, e vettorizzi ogni pezzo.

Strategie pratiche:

- **Fixed-size (a dimensione fissa)** — tagli ogni N token (unità di testo, all'incirca pezzi di parola) con un **overlap** (sovrapposizione): gli ultimi token di un chunk vengono ripetuti all'inizio del successivo, così una frase spezzata a metà non perde il senso al confine. Semplice e robusto.
- **Recursive (ricorsivo, per separatori)** — provi a tagliare prima sui separatori "grossi" (paragrafi: `\n\n`), poi se il pezzo è ancora troppo lungo scendi a quelli più fini (frasi, poi spazi). Così i tagli cadono in punti naturali. È l'approccio del **`RecursiveCharacterTextSplitter`** di **LangChain**, il default sensato per il testo generico.
- **Semantic (semantico)** — tagli dove **cambia argomento**: misuri quando due frasi vicine diventano poco simili tra loro e lì metti il confine. Chunk più coerenti, ma più costoso da calcolare.
- **Per struttura** — sfrutti la forma del documento: tagli per **heading** e sezioni, rispetti i blocchi Markdown, tieni le **tabelle** intere invece di spezzarle a metà. Ottimo per manuali e documentazione ben strutturata.

Il **trade-off della dimensione del chunk** è il concetto chiave:

- **Chunk piccolo** → molto **preciso** (recuperi esattamente il pezzo rilevante) ma con **poco contesto** attorno: a volte al modello manca l'informazione che stava una riga sopra.
- **Chunk grande** → tanto **contesto** ma più **rumore** (dentro c'è anche roba irrilevante che confonde la ricerca) e più **costo** (più token da vettorizzare e da mandare poi all'LLM).

**Consiglio pratico di partenza:** chunk intorno a **300–500 token**, con **overlap del 10–15%**. Non è una legge fisica: è un punto di partenza ragionevole da cui misurare e aggiustare sui tuoi documenti.

## 3. Indicizzazione (come si cerca veloce su milioni di vettori)

Un **indice** è la struttura dati che permette di trovare in fretta i vettori più simili a quello che cerchi. Senza indice dovresti confrontare la domanda con **ogni singolo vettore** uno per uno: su qualche migliaio va, ma su milioni diventa lentissimo ad ogni query.

La soluzione pratica si chiama **ANN = Approximate Nearest Neighbor** (ricerca dei vicini più prossimi *approssimati*). L'idea: invece di garantire il risultato *esatto* controllando tutto, l'indice usa scorciatoie intelligenti per trovare *quasi sempre* i vicini giusti, molto più in fretta. Rinunci a una briciola di precisione teorica in cambio di enorme velocità — e in un RAG questa è quasi sempre la scelta giusta.

Tipi di indice che incontrerai:

- **Flat** — nessuna scorciatoia: confronta la query con tutti i vettori, uno a uno. È **esatto** (trova davvero i più vicini) ma diventa lento con la scala. Ottimo fino a qualche decina di migliaia di vettori, o quando la precisione perfetta conta più della velocità.
- **HNSW (Hierarchical Navigable Small World)** — costruisce un **grafo di vicinato**: ogni vettore è collegato ai suoi simili, e la ricerca "salta" da nodo a nodo avvicinandosi rapidamente alla zona giusta. È il **default moderno**: veloce e molto accurato, funziona bene fino a milioni di vettori. Quando non sai cosa scegliere, è questo.
- **IVF (Inverted File)** — divide lo spazio in **celle/cluster**: prima trovi le poche celle più promettenti, poi cerchi solo dentro quelle invece che in tutto il dataset. Efficiente in memoria su dataset molto grandi, ma va "addestrato" sui dati e va tarato quante celle esplorare.

**Cosa scegliere secondo la scala, in pratica:** poche decine di migliaia di vettori → **Flat** va benissimo, semplice ed esatto. Da lì fino a milioni → **HNSW** è la scelta di default. Dataset enormi con vincoli di memoria → **IVF** (spesso combinato con compressione dei vettori).

Le **metriche di distanza** (il modo con cui l'indice misura "quanto sono vicini" due vettori), a parole:

- **Cosine (coseno)** — guarda l'**angolo**, ignora la lunghezza. È la scelta più comune per il testo, perché ci interessa la direzione del significato, non "quanto è lungo" il vettore.
- **Dot product (prodotto scalare)** — tiene conto anche della lunghezza dei vettori. Alcuni modelli producono vettori già **normalizzati** (tutti della stessa lunghezza): in quel caso dot product e coseno danno lo stesso ordine, e il dot product è un filo più veloce.
- **Euclidea (L2)** — la distanza "in linea d'aria" nello spazio. Usata quando conta la posizione assoluta e non solo la direzione; per il testo è meno comune del coseno.

Regola pratica: usa la metrica **consigliata dal modello di embedding che hai scelto** (la trovi nella sua scheda). Molti modelli testuali sono pensati per il coseno.

## 4. I Vector DB (quale, in pratica)

Un **vector DB** (database vettoriale) è il posto dove salvi i vettori, l'indice sopra di essi, e le informazioni collegate — e che ti offre le API per cercare. Ecco il panorama pratico, da "per iniziare" a "produzione":

- **FAISS** (Facebook AI Similarity Search) — è una **libreria**, non un server: gira **in-memory** dentro il tuo processo Python. Velocissima, perfetta per **prototipi** e per imparare. Da sola non gestisce persistenza comoda, metadati ricchi o accesso multiutente: la usi quando vuoi partire subito.
- **Chroma** — leggero, gira in **locale**, pensato per lo **sviluppo**: lo installi con un `pip` e in due righe hai una collezione. Ottimo per il dev e i piccoli progetti.
- **Qdrant** e **Weaviate** — **server open-source** pensati per la **produzione**: gestiscono milioni di vettori, offrono **filtri sui metadati** e ricerca **ibrida** (densa + lessicale). Li fai girare tu (o in cloud gestito) quando il progetto diventa serio.
- **pgvector** — un'estensione di **PostgreSQL**: se hai **già un Postgres**, tieni i vettori dentro il tuo database esistente, accanto ai dati relazionali, con una sola infrastruttura da gestire. Molto pragmatico quando non vuoi introdurre un nuovo sistema.
- **Pinecone** — servizio **gestito nel cloud**: zero-ops, non gestisci server né scalabilità, paghi il servizio. Comodo quando vuoi concentrarti sull'app e non sull'infrastruttura.

Un punto pratico che fa tutta la differenza: oltre al vettore, un vector DB salva il **payload / metadati**, cioè le informazioni collegate al chunk. Tipicamente: il **testo originale** del chunk (ti serve per mostrarlo all'LLM e all'utente), la **fonte** (nome file, URL, pagina), la **data**, l'**autore**, il **cliente**. Questi dati servono a due cose fondamentali: le **citazioni** (dire "questa risposta viene dal documento X, pagina Y") e i **filtri** (cercare solo tra i documenti di un certo cliente o periodo). Un vettore senza metadati è un numero muto: ritrova il pezzo ma non sai da dove viene né puoi restringere la ricerca.

## 5. Retrieval (a runtime, ad ogni domanda)

Ora la fase live. Arriva la domanda e questo è il percorso, passo per passo.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 170" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arVdbQry" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
   <rect x="8" y="62" width="92" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="54" y="82">Domanda</text><text x="54" y="96" font-size="9.5" fill="var(--muted)">utente</text>
   <rect x="116" y="62" width="104" height="46" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="168" y="80">Embedding</text><text x="168" y="94" font-size="9.5" fill="var(--muted)">stesso modello</text>
   <rect x="236" y="62" width="104" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="288" y="80">Ricerca ANN</text><text x="288" y="94" font-size="9.5" fill="var(--muted)">nell'indice</text>
   <rect x="356" y="62" width="104" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="408" y="80">Filtro</text><text x="408" y="94" font-size="9.5" fill="var(--muted)">metadati</text>
   <rect x="476" y="62" width="92" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="522" y="80">Top-k</text><text x="522" y="94" font-size="9.5" fill="var(--muted)">candidati</text>
   <rect x="584" y="62" width="126" height="46" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="647" y="80">Reranking</text><text x="647" y="94" font-size="9.5" fill="var(--muted)">chunk finali</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arVdbQry)">
   <path d="M100,85 L114,85"/><path d="M220,85 L234,85"/><path d="M340,85 L354,85"/><path d="M460,85 L474,85"/><path d="M568,85 L582,85"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Fase di retrieval: accade ad ogni domanda, in tempo reale. La domanda diventa vettore con lo stesso modello dell'indicizzazione, poi si cerca, si filtra, si prende il top-k e si riordina.</figcaption>
</figure>

I termini nuovi, definiti:

- **Top-k** — quanti chunk recuperi dalla ricerca. `k=5` significa "dammi i 5 più simili". È una manopola: k basso = poco materiale ma pulito; k alto = più materiale ma più rumore (e più token da pagare all'LLM dopo).
- **Metadata filtering (filtro sui metadati)** — restringere la ricerca in base agli attributi salvati nel payload **prima** (o insieme) alla misura di similarità. Esempio concreto: "cerca solo tra i documenti del cliente Rossi, degli ultimi 12 mesi". Così non recuperi un chunk simile ma appartenente al cliente sbagliato — cosa che oltre a essere inutile può essere un problema di riservatezza. È esattamente il motivo per cui i metadati (sezione 4) sono così importanti.
- **Reranking (riordino)** — dopo aver preso i primi candidati con la ricerca ANN (veloce ma "grossolana"), passi quei pochi candidati a un modello **cross-encoder**, che rilegge insieme la **coppia domanda + chunk** e assegna un punteggio di rilevanza preciso, poi riordina. La differenza con l'embedding: l'embedding calcola il vettore della domanda e del chunk **separatamente** e poi li confronta (veloce, adatto a milioni di documenti); il cross-encoder guarda i due testi **insieme** in un colpo solo (molto più accurato ma lento, quindi lo usi solo su una manciata di candidati, non su tutto l'indice). Schema tipico: recuperi 50 candidati con la ricerca ANN, li reranki, tieni i migliori 5.

  Tool reali di reranking: **Cohere Rerank** (via API, molto usato), i **cross-encoder di sentence-transformers** (es. `cross-encoder/ms-marco-MiniLM-L-6-v2`, girano in locale), il **BGE reranker** (`bge-reranker-base`/`large`, open-source).

- **Hybrid search (ricerca ibrida)** — combinare la ricerca **densa** (per vettori/significato, quella di oggi) con quella **lessicale** basata su **BM25** (che pesa le parole esatte, come un motore di ricerca classico: ottima quando cerchi un codice prodotto, un nome proprio, un termine tecnico raro che l'embedding "annacqua"). Le due si completano; il dettaglio lo vedi in `xc-llm-rag`.

## Errori pratici comuni (checklist)

- **Modello di embedding diverso tra indicizzazione e query.** Vettori in spazi diversi = risultati senza senso. Fissa un modello e usalo per entrambe; se lo cambi, **re-indicizza tutto**.
- **Chunk troppo grandi o troppo piccoli.** Grandi = rumore e costo; piccoli = manca contesto. Parti da ~300–500 token con overlap 10–15% e aggiusta misurando.
- **Nessun metadato salvato.** Senza payload non hai **citazioni** ("da dove viene questa risposta?") né **filtri** (per cliente/data). Salva sempre almeno testo originale e fonte.
- **Top-k troppo alto.** Recuperi troppa roba: aumentano il **rumore** (chunk irrilevanti che confondono l'LLM) e il **costo** (più token). Tieni k basso e, se serve più recall, alza k ma aggiungi il **reranking**.
- **Dimenticare di re-indicizzare quando i documenti cambiano.** Se aggiorni o aggiungi documenti e non li re-indicizzi, il sistema risponde su dati vecchi. Prevedi un processo che re-indicizza ciò che cambia.

## Notable use cases (grandi aziende)

- **Ricerca semantica interna** — cercare nella documentazione aziendale "per significato" invece che per parola esatta: trovi il documento giusto anche se hai usato sinonimi diversi.
- **"Chatta col tuo PDF"** — carichi un documento (o un manuale) e fai domande in linguaggio naturale ottenendo risposte con citazioni al punto esatto.
- **Knowledge base di supporto** — l'assistente clienti (umano o bot) recupera al volo la procedura o l'articolo giusto per rispondere a un ticket.
- **Ricerca prodotti** — negli e-commerce, trovare prodotti per descrizione e intento ("scarpe da corsa leggere per asfalto") e non solo per parola chiave.

## Fonti

- **Pinecone Learn** — pinecone.io/learn (concetti di embedding, indicizzazione ANN, vector DB, spiegati in modo pratico).
- **Qdrant Documentation** — qdrant.tech/documentation (indici, metriche di distanza, filtri sui metadati, ricerca ibrida).
- **LangChain Docs** — text splitters e retrievers (chunking pratico, `RecursiveCharacterTextSplitter`, pipeline di retrieval).
- **Sentence-Transformers** — sbert.net (embedding open-source in locale e cross-encoder per il reranking).

## Concetti adiacenti

- **xc-llm-rag** — il sistema completo che usa questo retrieval per dare contesto all'LLM e generare risposte fondate; ci trovi anche l'hybrid search per esteso.
- **xc-llm-chatbot-arch** — come tutto questo si incastra dentro l'architettura di un chatbot (memoria, orchestrazione, tool).
- **xc-llm-fundamentals** — cosa sono token, modelli e context window, i mattoni sotto embedding e generazione.
- **prog-ds** — strutture dati e complessità: perché un indice ANN batte la ricerca uno-a-uno, e il ragionamento sui trade-off velocità/precisione.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cos'è la **vettorializzazione** e chi la esegue?
2. Perché devi usare **lo stesso modello di embedding** per indicizzare e per cercare?
3. Cita **due strategie di chunking** e spiega in una riga come funzionano.
4. Cos'è la **ANN** e perché serve invece di confrontare tutti i vettori uno a uno?
5. Che differenza c'è tra un indice **HNSW** e un indice **Flat**, e quando usi l'uno o l'altro?
6. Cosa aggiunge il **metadata filtering** al retrieval? Fai un esempio.
7. Cos'è il **reranking** e con che tipo di modello si fa? In cosa è diverso dall'embedding?
8. Descrivi un **errore pratico comune** tra quelli in checklist e perché è un problema.
9. Cosa salva un vector DB **oltre al vettore**, e a cosa serve?
10. Cosa misura la **similarità coseno**, a parole?

<details><summary>Risposte</summary>

1. È la trasformazione di un testo in un **vettore** (lista di numeri) che ne cattura il significato: testi simili → vettori vicini. La esegue l'**embedding model** (gli dai testo, ti restituisce un vettore di N dimensioni, es. 384/768/1536).

2. Perché i vettori dei documenti e quello della domanda devono vivere nello **stesso spazio** (stesse dimensioni, stesso modo di misurare). Con modelli diversi confronteresti mele con pere e il retrieval restituirebbe risultati senza senso. Se cambi modello devi re-indicizzare tutto.

3. Due qualsiasi tra: **fixed-size** (tagli ogni N token con overlap tra un pezzo e il successivo); **recursive** (tagli prima sui separatori grossi come i paragrafi, poi su frasi/spazi, es. `RecursiveCharacterTextSplitter` di LangChain); **semantic** (tagli dove cambia argomento); **per struttura** (tagli per heading/Markdown, tieni le tabelle intere).

4. **ANN = Approximate Nearest Neighbor**, la ricerca dei vicini più prossimi *approssimati*. Serve perché confrontare la query con ogni singolo vettore uno a uno è troppo lento su milioni di vettori; l'ANN usa scorciatoie per trovare *quasi sempre* i più simili molto più in fretta, rinunciando a una briciola di precisione teorica.

5. **Flat** confronta la query con tutti i vettori uno a uno: è **esatto** ma lento con la scala (bene fino a qualche decina di migliaia). **HNSW** costruisce un **grafo di vicinato** e "salta" verso la zona giusta: veloce e molto accurato fino a milioni di vettori, è il default moderno. Flat quando i vettori sono pochi o vuoi precisione perfetta; HNSW da lì in su.

6. Restringe la ricerca in base agli **attributi nei metadati** (payload) prima/insieme alla similarità, così eviti chunk simili ma dal contesto sbagliato. Esempio: "cerca solo tra i documenti del cliente Rossi, degli ultimi 12 mesi". Migliora la pertinenza e protegge la riservatezza.

7. Il **reranking** riordina i candidati recuperati dalla ricerca ANN usando un modello **cross-encoder**, che rilegge insieme la **coppia domanda + chunk** e dà un punteggio di rilevanza preciso. È diverso dall'embedding perché quest'ultimo calcola i vettori di domanda e chunk **separatamente** (veloce, adatto a milioni di documenti), mentre il cross-encoder guarda i due testi **insieme** (più accurato ma lento, quindi solo su pochi candidati). Tool: Cohere Rerank, cross-encoder di sentence-transformers, BGE reranker.

8. Uno qualsiasi tra: modello di embedding diverso tra index e query (vettori in spazi diversi → risultati insensati); chunk troppo grandi (rumore+costo) o troppo piccoli (manca contesto); nessun metadato (niente citazioni né filtri); top-k troppo alto (rumore + costo in token); non re-indicizzare quando i documenti cambiano (rispondi su dati vecchi).

9. Il **payload / metadati**: testo originale del chunk, fonte (file/URL/pagina), data, autore, cliente. Servono per le **citazioni** (dire da dove viene la risposta) e per i **filtri** (restringere la ricerca per attributi).

10. Misura l'**angolo** tra due vettori, **non** la loro lunghezza: due testi che "puntano nella stessa direzione" parlano della stessa cosa, a prescindere da quanto sono lunghi.

</details>
