# Ripasso Uni

A daily **spaced-review** web app for exam prep. Each weekday (Sun–Fri) unlocks a lesson; you take
notes per lesson, browse history, and your progress is saved in the browser.

Two content tracks: **AI / ML** (LLM fundamentals, RAG types, agents, embeddings & retrieval, chatbot
architecture) and **Product Management**.

**Live → https://javas-cri-pt.github.io/ripasso-uni/**

Static build: `curriculum.yml` + `lessons/` → `build-app.py` renders `index.html`. Theme toggle,
mobile drawer, inline SVG system-design diagrams. No backend, no accounts — everything runs client-side.

## Il loop (come non restare a secco)

Le lezioni si sbloccano una al giorno (dom–ven): il **buffer** deve stare **davanti** al giorno
corrente, altrimenti l'app smette di dare cose nuove. Non c'è uno scheduler automatico (il grounding
pesca dalle cartelle uni locali), quindi il loop è manuale:

1. `python3 build-app.py` stampa in fondo il **margine di buffer**, es.
   `maxDay 24 · oggi ~giorno 20, buffer fino a 24 (margine 4)`. Se il margine scende **sotto 3**,
   stampa `⚠ RIGENERA`.
2. Quando serve, genera un nuovo blocco di ~6 lezioni (una settimana) seguendo lo SPEC e la
   **politica di MIX** in testa a `curriculum.yml`: un po' di tutto (AI/ML + SWE + business +
   ripassi generali UNIBO + DSA), colloquio-first, ogni acronimo definito, ~10 quiz, schemi SVG
   theme-aware. Usa i `topic_id` dal backbone in `curriculum.yml`.
3. Rebuild e push. `start_date` nel meta del curriculum è la data di riferimento per la stima del margine.
