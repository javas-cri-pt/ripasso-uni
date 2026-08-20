---
day: 9
topic_id: xc-llm-chunking
title: "Chunking avanzato (parent-document, contextual retrieval, tabelle e codice)"
area: cross-cutting
course: LLM / AI Engineering
grounded_in: null
adjacent: [xc-llm-vectordb, xc-llm-rag]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun termine lasciato senza definizione. Taglio pratico."
---

# Chunking avanzato

> **Perché oggi:** il chunking è la leva col miglior rapporto risultato/sforzo in un RAG. Se spezzi male i documenti, il retrieval è già mediocre a monte, e nessun reranking a valle ti salva: stai riordinando pezzi sbagliati. A Glacom la qualità delle risposte del chatbot dipende in gran parte da qui, e queste strategie avanzate sono spesso quello che separa un RAG "che funzicchia" da uno che risponde bene.

## Ripasso lampo (le basi)

Un **chunk** è un pezzo del documento che vettorizzi (trasformi in numeri) e metti nell'indice per poterlo cercare. Le strategie base sono **fixed-size** (tagli ogni N token con un **overlap**, cioè una sovrapposizione tra un pezzo e il successivo così una frase spezzata a metà non perde il senso) e **recursive** (tagli prima sui separatori grossi come i paragrafi, poi scendi a frasi e spazi). Il trade-off di fondo: chunk **piccolo** = preciso ma con poco contesto attorno; chunk **grande** = tanto contesto ma più rumore e più costo. Tutto questo è in `xc-llm-vectordb`.

Il problema di fondo che l'avanzato risolve è il **dilemma precisione-contesto**: per **cercare** bene servono chunk **piccoli** (un pezzo piccolo e mirato matcha in modo preciso la domanda, senza significati mescolati), ma per **rispondere** bene serve **contesto ampio** (all'LLM serve il paragrafo intorno, non una frase isolata). Le due esigenze tirano in direzioni opposte. Quasi tutte le tecniche di oggi sono modi diversi di avere entrambe le cose insieme.

## 1. Small-to-big / Parent-document retrieval

È la soluzione principe al dilemma. L'idea in una riga: **cerchi in piccolo, rispondi in grande.**

In pratica **indicizzi** (cioè metti nell'indice, pronti per la ricerca) chunk **piccoli** e precisi — poche frasi ciascuno. Ma quando uno di questi chunk piccoli **matcha** la domanda, non passi *quello* all'LLM: risali e **passi all'LLM il chunk "genitore" (parent) più grande**, cioè il paragrafo o la sezione da cui il pezzo piccolo proviene. La ricerca sfrutta la precisione del piccolo; la generazione riceve il contesto ampio del grande. Il legame piccolo → grande lo tieni salvato (tipicamente ogni chunk piccolo porta nei metadati l'ID del suo parent, così risalire è immediato).

Perché funziona: il chunk piccolo è "l'amo" che aggancia il punto esatto rilevante, il parent è "la rete" di contesto che dai al modello per rispondere completo. Ottieni precisione **e** contesto senza dover scegliere.

Tool reali:

- **ParentDocumentRetriever** di **LangChain** — indicizza i figli piccoli, tiene i genitori grandi in uno store a parte, e al momento del recupero ti restituisce automaticamente i parent.
- **AutoMergingRetriever** di **LlamaIndex** — variante intelligente: i chunk sono organizzati ad albero (piccoli sotto, grandi sopra); se **tanti figli dello stesso genitore** vengono recuperati insieme, il retriever li "fonde" (merge) e restituisce direttamente il genitore, invece di darti tre pezzetti separati dello stesso paragrafo.

## 2. Sentence-window retrieval

È una variante dello stesso principio "cerca in piccolo, rispondi in grande", ma portata all'estremo del piccolo. Qui **indicizzi singole frasi**: ogni frase è un chunk a sé, quindi la ricerca è precisissima. Al momento del recupero, però, **espandi** la frase che ha matchato con **N frasi prima e N frasi dopo** — questa è la "finestra" (window) — e passi all'LLM quel blocchetto allargato.

Il risultato: la **precisione** del match sulla singola frase, più il **contesto locale** immediato che le sta intorno. La differenza col parent-document è il tipo di contesto restituito: qui è una **finestra scorrevole** di frasi vicine (tante prima, tante dopo la frase-amo), non un blocco "genitore" predefinito come il paragrafo o la sezione.

Tool: **SentenceWindowNodeParser** di **LlamaIndex** — spezza il testo per frasi e memorizza per ognuna la sua finestra di contesto, che viene reinserita al momento del recupero.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 700 250" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arChkS2B" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
   <rect x="20" y="30" width="150" height="180" rx="10" fill="none" stroke="var(--rule)" stroke-dasharray="4 3"/>
   <text x="95" y="22" font-size="10" fill="var(--muted)">Indice (chunk piccoli)</text>
   <rect x="38" y="44" width="114" height="30" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="95" y="63" font-size="10">chunk piccolo</text>
   <rect x="38" y="82" width="114" height="30" rx="7" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/><text x="95" y="101" font-size="10">chunk che matcha</text>
   <rect x="38" y="120" width="114" height="30" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="95" y="139" font-size="10">chunk piccolo</text>
   <rect x="38" y="158" width="114" height="30" rx="7" fill="var(--card)" stroke="var(--rule)"/><text x="95" y="177" font-size="10">chunk piccolo</text>

   <rect x="300" y="70" width="150" height="90" rx="10" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
   <text x="375" y="105" font-size="11.5">Parent grande</text>
   <text x="375" y="124" font-size="9.5" fill="var(--muted)">paragrafo/sezione</text>
   <text x="375" y="139" font-size="9.5" fill="var(--muted)">da cui viene il chunk</text>

   <rect x="540" y="82" width="140" height="66" rx="10" fill="var(--card)" stroke="var(--rule)"/>
   <text x="610" y="112" font-size="11.5">Prompt all'LLM</text>
   <text x="610" y="130" font-size="9.5" fill="var(--muted)">riceve il parent</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arChkS2B)">
   <path d="M95,20 C95,4 375,4 375,66"/>
   <path d="M154,97 L296,110"/>
   <path d="M452,115 L536,115"/>
  </g>
  <g font-size="9.5" fill="var(--muted)" text-anchor="middle">
   <text x="235" y="88">query matcha</text>
   <text x="235" y="100">un chunk piccolo</text>
   <text x="235" y="9">query cerca in piccolo</text>
   <text x="495" y="103">rispondi</text>
   <text x="495" y="115">in grande</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Small-to-big: la query cerca tra i chunk piccoli (preciso), ma quando uno matcha si risale al parent grande, che è ciò che finisce nel prompt dell'LLM (contesto).</figcaption>
</figure>

## 3. Contextual retrieval (contesto pre-aggiunto)

Problema che risolve: i **chunk orfani**. Quando spezzi un documento, un chunk isolato spesso perde i suoi riferimenti. Prendi un chunk come *"Il valore è salito del 3% rispetto al trimestre precedente."* Quale valore? Di quale azienda? Quale trimestre? Nel documento originale la risposta era due paragrafi sopra, ma nel chunk quel contesto non c'è più. Un chunk così è **orfano**: da solo non si capisce, e per giunta il suo embedding è vago (non ha abbastanza segnale per matchare le domande giuste).

La soluzione, resa nota da **Anthropic**, è la **contextual retrieval**: prima di embeddare, **anteponi a ogni chunk un breve contesto** generato da un **LLM**, che descrive da dove viene il chunk e di cosa parla. Nell'esempio, invece del solo *"Il valore è salito del 3%..."*, embeddi qualcosa tipo:

> *"Questo estratto viene dal report finanziario Q3 2024 dell'azienda e riguarda l'andamento del fatturato: Il valore è salito del 3% rispetto al trimestre precedente."*

Così il chunk **si auto-descrive** e il suo embedding è molto più azzeccato, perché ora contiene i riferimenti che prima erano impliciti. Concretamente: per ogni chunk fai una passata con un LLM passandogli il chunk **più il documento intero** (o un buon riassunto) e gli chiedi "scrivi una o due righe che situino questo pezzo nel documento". Quel contestino va davanti al chunk, e la coppia contesto+chunk è ciò che embeddi.

Costo: è **una passata LLM in più in fase di indicizzazione**, per ogni chunk. Si paga una volta sola (l'indicizzazione è offline), e si **mitiga con il prompt caching**: siccome per tutti i chunk dello stesso documento il documento è identico, lo tieni in cache e non lo ri-processi da zero ogni volta, abbattendo molto il costo.

## 4. Indicizzazione gerarchica e per riassunti

Invece di un indice piatto (tutti i chunk allo stesso livello), costruisci un indice a **più livelli**: in cima i **riassunti** di documento e di sezione, sotto i **chunk di dettaglio**. La ricerca può allora procedere dall'alto verso il basso: prima trova la **sezione giusta** usando i riassunti, poi **scende** dentro quella sezione a cercare il dettaglio preciso. Eviti di confrontare subito la domanda con migliaia di frammenti di dettaglio sparsi, e riduci il rischio di pescare un chunk simile ma preso dal documento sbagliato.

È particolarmente utile su **corpus grandi e ben strutturati** (manuali, normative, documentazione tecnica con capitoli e sezioni), dove la struttura del documento è un'informazione preziosa che l'indice piatto butterebbe via.

Tool e pattern:

- **HierarchicalNodeParser** di **LlamaIndex** — spezza il documento in nodi a più livelli di granularità (documento → sezioni → chunk piccoli), mantenendo il legame padre-figlio. È lo stesso albero su cui poi lavora l'AutoMergingRetriever visto prima.
- Pattern **"summary index"** — associ a ogni documento (o sezione) un **riassunto** e lo usi come primo filtro: la ricerca sceglie prima *quale documento/sezione* è rilevante guardando i riassunti, poi cerca il dettaglio solo lì dentro.

## 5. Late chunking (cenno)

Nelle tecniche viste finora spezzi **prima** ed embeddi **dopo**: ogni chunk viene vettorizzato da solo, senza sapere cosa c'è nel resto del documento. Il **late chunking** ("chunking tardivo") ribalta l'ordine, sfruttando i modelli di embedding a **contesto lungo** (che accettano in ingresso interi documenti, non poche frasi):

1. Prima passi l'**intero documento** dentro il modello di embedding. Così ogni token, mentre viene elaborato, "vede" tutto il resto del documento e ne assorbe il contesto.
2. Poi **derivi** gli embedding dei singoli chunk **dai token già contestualizzati** al passo 1 (raggruppando i token che appartengono a ciascun chunk), invece di ri-embeddare ogni chunk da zero e isolato.

Il vantaggio intuitivo: i chunk mantengono il **contesto globale del documento** già "cotto dentro" il loro vettore. Il pezzo *"Il valore è salito del 3%"* eredita nel suo embedding l'informazione che nel documento si parlava del fatturato Q3, senza bisogno di anteporre testo a mano come nella contextual retrieval. È una tecnica **recente**: tienila a mente come direzione, sapendo che richiede un modello di embedding pensato per il contesto lungo.

## 6. Chunking di tabelle e codice (i casi che rompono tutto)

Le strategie generiche assumono **testo in prosa**, che scorre in frasi e paragrafi. Ma tabelle e codice **non** si spezzano come il testo normale, e trattarli allo stesso modo rompe il retrieval.

- **Tabelle.** Non tagliarle mai a metà riga: mezzo record senza intestazioni di colonna è illeggibile sia per l'LLM sia per l'embedding. Due approcci pratici: (a) tieni la **tabella intera come un unico chunk** (se ci sta nel limite); oppure (b) genera un **riassunto in linguaggio naturale** della tabella (es. *"Tabella dei prezzi per fascia di peso e destinazione, con valori tra X e Y"*), **embeddi il riassunto** (che matcha bene le domande in linguaggio naturale) e tieni la **tabella vera nei metadati** per poterla mostrare all'utente. Per estrarre correttamente le tabelle dai PDF/documenti servono parser dedicati: **Unstructured** e **LlamaParse**, che riconoscono la struttura tabellare invece di appiattirla in testo confuso.
- **Codice.** Non spezzarlo per **numero di righe**: rischi di troncare una funzione a metà, lasciando un chunk che non compila e non ha senso. Spezza per **unità sintattiche** — funzione, classe, metodo — così ogni chunk è **auto-contenuto** (una funzione intera con la sua firma e il suo corpo). LangChain offre splitter **"per linguaggio"** che conoscono la sintassi dei vari linguaggi (Python, JavaScript, ecc.) e tagliano nei punti giusti.
- **Header/titoli nel chunk.** Vale per tutti i tipi di documento: includi sempre i **titoli di sezione** dentro il chunk. Se un chunk parla di una procedura di rimborso, anteponigli la sua gerarchia di titoli (es. `"## Rimborsi > Tempistiche > "`) così il pezzo non perde **a quale argomento appartiene**. È un modo semplice ed economico di evitare i chunk orfani della sezione 3: il titolo dà al chunk il suo "indirizzo" nel documento.

## Come scegliere e MISURARE

Nessuna di queste strategie è "la migliore" in assoluto, e **non esiste una dimensione di chunk giusta a priori**: dipende dal tipo di documenti (prosa lunga? tabelle? codice? testi brevi?) e dal tipo di domande (puntuali su un fatto? di sintesi su un'intera sezione?). Il punto pratico è uno solo: **misura**, non scegliere a sensazione.

Come si misura, concretamente:

1. Metti su un piccolo set di **domande con la risposta attesa** (cioè sai quale chunk/documento *dovrebbe* essere recuperato per rispondere).
2. Fai girare le diverse strategie e confronta i risultati con il **recall@k**.

Il **recall@k** è la **frazione di domande per cui il chunk giusto compare tra i primi k risultati recuperati**. Esempio: 20 domande di test, `k=5`; se per 17 domande il chunk corretto è tra i primi 5 recuperati, il recall@5 è 17/20 = 0,85. È la metrica che ti dice se il retrieval *ha in mano* l'informazione giusta (se non ce l'ha lì, tutto il resto — reranking, generazione — parte già perdente).

In pratica **A/B testi** le strategie sui **tuoi** dati: fixed vs recursive vs parent-document vs sentence-window, tutte contro lo stesso set di domande, e tieni quella col recall@k più alto. È un pomeriggio di lavoro che vale più di mille opinioni.

## Errori comuni

- **Chunk troppo grandi "per sicurezza".** L'istinto è "metto tanto contesto così non manca niente", ma chunk enormi **annacquano il retrieval**: dentro c'è troppa roba diversa, l'embedding diventa vago e matcha peggio. Meglio piccolo per cercare + parent per rispondere (sezione 1).
- **Tagliare tabelle o codice a metà.** Mezza tabella senza intestazioni, mezza funzione che non compila: chunk inutili. Trattali coi metodi dedicati (sezione 6).
- **Niente header/titoli nel chunk → chunk orfani.** Un pezzo che non sa a quale sezione appartiene perde riferimenti e matcha male. Anteponi sempre la gerarchia di titoli.
- **Scegliere la strategia "a sensazione", senza misurare.** Senza recall@k su un set di test stai tirando a indovinare. Misura e A/B testa sui tuoi dati.
- **Overlap eccessivo.** Un po' di sovrapposizione tra chunk aiuta ai bordi, ma troppo overlap significa **duplicazione** (lo stesso testo in più chunk, che affolla i risultati con quasi-doppioni) e **costi** più alti (più token da embeddare e da salvare).

## Fonti

- **Anthropic — "Introducing Contextual Retrieval"** (anthropic.com/news/contextual-retrieval) — la tecnica di anteporre contesto generato da LLM ai chunk prima di embeddarli, e il ruolo del prompt caching per contenere i costi.
- **LlamaIndex Documentation** — node parsers e retriever: `SentenceWindowNodeParser` (sentence-window), `AutoMergingRetriever` (small-to-big ad albero), `HierarchicalNodeParser` (indicizzazione gerarchica).
- **LangChain Documentation** — `ParentDocumentRetriever` (small-to-big) e gli splitter "per linguaggio" per il codice.
- **Unstructured** (unstructured.io) — parsing di documenti reali (PDF, Office) con riconoscimento di tabelle e struttura, utile a monte del chunking.

## Concetti adiacenti

- **xc-llm-vectordb** — i mattoni sotto: embedding, indicizzazione ANN, vector DB e le strategie di chunking di base (fixed, recursive) da cui parte questa lezione.
- **xc-llm-rag** — il sistema completo in cui il chunking vive: come i chunk recuperati diventano contesto per l'LLM che genera la risposta finale.

## Quiz (10 — tutte rispondibili dalla lezione)

1. In cosa consiste il **dilemma precisione-contesto** che le tecniche avanzate di chunking cercano di risolvere?
2. Come risolve il dilemma il **parent-document retrieval** (small-to-big)? Spiega il meccanismo.
3. Cos'è il **sentence-window retrieval** e in cosa differisce dal parent-document nel tipo di contesto che restituisce?
4. Cos'è la **contextual retrieval** e quale problema risolve? Fai l'esempio del chunk orfano.
5. Qual è il **costo** della contextual retrieval e come si **mitiga**?
6. Cos'è l'**indicizzazione gerarchica / per riassunti** e quando è particolarmente utile?
7. Come vanno gestite le **tabelle** nel chunking? Cita almeno un approccio e un tool di parsing.
8. Come si spezza il **codice** e perché **non** per numero di righe?
9. Cos'è il **recall@k**? Fai un esempio numerico e spiega perché conviene misurarlo.
10. Cita **due errori comuni** del chunking e spiega perché sono un problema.

<details><summary>Risposte</summary>

1. Per **cercare** bene servono chunk **piccoli** (matchano in modo preciso la domanda, senza significati mescolati), ma per **rispondere** bene serve **contesto ampio** (all'LLM serve il paragrafo intorno, non una frase isolata). Le due esigenze tirano in direzioni opposte: chunk piccoli danno precisione ma poco contesto, chunk grandi danno contesto ma più rumore. Le tecniche avanzate servono ad avere entrambe le cose.

2. **Indicizzi** chunk **piccoli e precisi** (l'"amo" per la ricerca), ma quando uno matcha la domanda **risali al chunk "genitore" (parent) più grande** — il paragrafo o la sezione da cui viene — e passi *quello* all'LLM. Cerchi in piccolo (precisione), rispondi in grande (contesto). Il legame piccolo→grande è salvato (es. l'ID del parent nei metadati). Tool: ParentDocumentRetriever di LangChain, AutoMergingRetriever di LlamaIndex.

3. **Indicizzi singole frasi** (ricerca precisissima) e, al recupero, **espandi** la frase che ha matchato con **N frasi prima e N frasi dopo** (la "finestra"). Differenza col parent-document: il contesto restituito è una **finestra scorrevole** di frasi vicine centrata sulla frase-amo, non un blocco "genitore" predefinito come il paragrafo o la sezione. Tool: SentenceWindowNodeParser di LlamaIndex.

4. La **contextual retrieval** (resa nota da Anthropic) **antepone a ogni chunk un breve contesto generato da un LLM** prima di embeddarlo, così il chunk si auto-descrive. Risolve il problema dei **chunk orfani**: un chunk isolato come *"Il valore è salito del 3%"* perde i riferimenti (quale valore? quale trimestre?). Anteponendo *"Questo estratto viene dal report Q3 2024 e riguarda il fatturato: ..."* il chunk contiene i riferimenti e il suo embedding matcha molto meglio.

5. Il costo è **una passata LLM in più in indicizzazione** per ogni chunk (per generare il contestino). Si **mitiga con il prompt caching**: il documento intero, che serve per contestualizzare tutti i chunk, si tiene in cache invece di ri-processarlo da zero per ogni chunk, abbattendo il costo. È comunque un costo offline, pagato una volta sola.

6. È un indice a **più livelli**: in cima i **riassunti** di documento e sezione, sotto i **chunk di dettaglio**. La ricerca scende dall'alto: prima trova la **sezione giusta** dai riassunti, poi **scende** al dettaglio dentro quella sezione. È utile soprattutto su **corpus grandi e ben strutturati** (manuali, normative, documentazione con capitoli). Tool: HierarchicalNodeParser di LlamaIndex, pattern "summary index".

7. Non tagliarle a metà riga. Approcci: (a) tieni la **tabella intera come un chunk**; oppure (b) embedda un **riassunto in linguaggio naturale** della tabella e tieni la **tabella vera nei metadati** per mostrarla. Tool di parsing per estrarle bene: **Unstructured** o **LlamaParse**.

8. Si spezza per **unità sintattiche** — funzione, classe, metodo — così ogni chunk è **auto-contenuto**. **Non** per numero di righe perché rischi di troncare una funzione a metà, ottenendo un chunk che non compila e non ha senso. LangChain offre splitter "per linguaggio" che conoscono la sintassi e tagliano nei punti giusti.

9. Il **recall@k** è la **frazione di domande per cui il chunk giusto compare tra i primi k risultati recuperati**. Esempio: 20 domande di test, k=5; se per 17 il chunk corretto è tra i primi 5, recall@5 = 17/20 = 0,85. Conviene misurarlo perché ti dice se il retrieval *ha in mano* l'informazione giusta: se non ce l'ha, reranking e generazione partono già perdenti. Serve a scegliere la strategia coi dati (A/B test) invece che a sensazione.

10. Due qualsiasi tra: **chunk troppo grandi "per sicurezza"** (annacquano il retrieval, embedding vago); **tagliare tabelle/codice a metà** (chunk illeggibili o che non compilano); **niente header/titoli nel chunk** (chunk orfani che non sanno a quale sezione appartengono); **scegliere a sensazione senza misurare** (niente recall@k = tirare a indovinare); **overlap eccessivo** (duplicazione di testo e costi più alti).

</details>
