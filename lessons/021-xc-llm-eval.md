---
day: 21
topic_id: xc-llm-eval
title: "Valutare sistemi LLM — evals, LLM-as-judge, hallucination, guardrail"
area: cross-cutting
course: LLM / AI Engineering
grounded_in: "Lavoro reale (Glacom: framework di valutazione ad agenti) + ml-eval"
adjacent: [ml-eval, xc-llm-agents, xc-llm-chatbot-arch, qe-spc]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo."
---

# Valutare sistemi LLM — evals, LLM-as-judge, hallucination, guardrail

> **Perché oggi:** costruire un chatbot è metà del lavoro; l'altra metà è **sapere se funziona davvero** e accorgersi quando **peggiora**. È esattamente ciò che fai a Glacom con il tuo framework di valutazione ad agenti. Per i ruoli AI questa è la competenza che distingue chi "fa girare un modello" da chi **spedisce sistemi affidabili**.

## Perché valutare gli LLM è diverso
Un LLM è **non deterministico** (stesso input, risposte diverse) e non ha una singola "risposta giusta": per una domanda aperta ci sono molte risposte buone e infinite sbagliate. Quindi non basta un `assert output == atteso` come nei test normali. Servono le **eval** (*evaluation*): un modo **sistematico e ripetibile** di misurare la qualità delle risposte, così puoi confrontare due versioni del sistema e capire se una modifica migliora o rompe.

Due termini da fissare subito:
- **Hallucination (allucinazione):** quando il modello produce un'affermazione **plausibile ma falsa** (un dato, una citazione, un'API inesistente) con tono sicuro. È il fallimento numero uno da tenere sotto controllo.
- **Guardrail:** un **controllo esplicito** attorno al modello che blocca o corregge output indesiderati (fuori tema, tossici, che rivelano dati sensibili, in formato sbagliato). Non è il modello: è la rete di sicurezza intorno.

## I tre modi di valutare (dal più rigido al più flessibile)
1. **Metriche deterministiche / reference-based:** confronti l'output con una risposta di riferimento. Utile quando esiste un "giusto": *exact match*, contiene la keyword, JSON valido secondo lo schema, la citazione punta a un documento che esiste. Oggettive ma rigide (non catturano "buona ma detta diversamente").
2. **Human evaluation:** persone leggono e danno un voto/preferenza. È il *gold standard* per qualità e sfumature, ma **lenta e costosa**: non la puoi far girare a ogni commit.
3. **LLM-as-judge:** usi **un altro LLM** come **giudice** che legge la risposta (e un criterio) e assegna un verdetto o un punteggio. È il compromesso: **scalabile come il codice, sfumato come un umano**. È la tecnica su cui si regge gran parte delle eval moderne, e la base del framework di valutazione che hai costruito a Glacom.

## LLM-as-judge, in pratica
Dai al giudice: la **domanda**, la **risposta da valutare**, spesso il **contesto/ground truth**, e un **criterio chiaro** ("è corretta rispetto al contesto? risponde davvero?"). Il giudice restituisce un **verdetto strutturato** (es. `RESOLVED` / `UNRESOLVED`, o un punteggio 1-5). Modi d'uso:
- **Reference-free:** giudica la risposta in sé (coerente? sul tema?).
- **Reference-based / groundedness:** verifica che la risposta sia **supportata dal contesto** recuperato (anti-allucinazione): "ogni affermazione è nei documenti dati?".
- **Pairwise:** dà due risposte (versione A vs B) e sceglie la migliore — ottimo per confrontare due versioni del sistema.

**Attenzione ai bias del giudice** (domande da colloquio): tende a preferire risposte **più lunghe**, quelle in **prima posizione** (position bias), o quelle prodotte dallo **stesso modello**. Si mitiga con criteri espliciti, invertendo l'ordine, e — come fai tu — richiedendo **conferme multiple**.

## Il tuo caso (framework di valutazione a Glacom)
Il tuo framework fa una cosa precisa: **agenti LLM impersonano utenti reali**, parlano col bot dal vivo, e un giudice emette un verdetto **RESOLVED / UNRESOLVED**. La parte non banale è come **abbassi i falsi positivi** (dire "risolto" quando non lo è): una **conferma unanime asimmetrica**, cioè un verdetto "risolto" conta **solo se sopravvive a 3 ri-controlli su 3**; basta un "no" per bocciarlo. Gira **su richiesta** e come **audit programmato**, e i suoi verdetti tornano indietro come **segnale di regressione**. È esattamente il ponte tra "l'ho costruito" e "so che funziona nelle mani dell'utente".

<svg viewBox="0 0 660 210" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="ev" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <rect x="14" y="70" width="110" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="69" y="90">Agente-utente</text><text x="69" y="106" font-size="10.5" fill="var(--muted)">impersona</text>
    <rect x="164" y="70" width="96" height="46" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="212" y="97">Bot (SUT)</text>
    <rect x="300" y="70" width="110" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="355" y="90">Giudice LLM</text><text x="355" y="106" font-size="10.5" fill="var(--muted)">criterio</text>
    <rect x="450" y="34" width="120" height="40" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="510" y="58" font-size="11.5">3 ri-controlli</text>
    <rect x="450" y="112" width="120" height="40" rx="9" fill="var(--card)" stroke="var(--good)" stroke-width="1.7"/><text x="510" y="130" font-size="11">RESOLVED</text><text x="510" y="145" font-size="10" fill="var(--muted)">solo se 3/3</text>
    <rect x="596" y="70" width="52" height="46" rx="9" fill="var(--card2)" stroke="var(--rule)"/><text x="622" y="90" font-size="10.5">segnale</text><text x="622" y="104" font-size="10.5">regress.</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#ev)">
    <path d="M124,93 L162,93"/><path d="M260,93 L298,93"/>
    <path d="M410,86 L448,62"/><path d="M510,74 L510,110"/>
    <path d="M570,132 C588,132 592,110 596,100"/>
  </g>
  <path d="M596,86 C300,-6 60,-6 60,66" fill="none" stroke="var(--muted)" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#ev)"/>
  <text x="330" y="12" text-anchor="middle" font-size="10.5" fill="var(--muted)">il segnale rientra: correggi e ri-testa</text>
</svg>

## Notable use cases (come si fa nel settore)
- **OpenAI Evals / framework di eval:** suite di test versionate che girano a ogni cambio di modello o prompt, esattamente come una test-suite software.
- **RAG groundedness (es. RAGAS, TruLens):** metriche automatiche che misurano se la risposta è **fedele** al contesto recuperato e se il contesto era **pertinente** — allineate al tuo lavoro anti-allucinazione.
- **LMArena (ex Chatbot Arena):** valutazione **pairwise** su larga scala con voti umani per classificare i modelli: la versione "human eval" del pairwise.

## Completeness check (integrato da me)
- **Il ponte con Quality Engineering (giorno uni):** le eval sono il cugino AI del **controllo statistico di processo** (`qe-spc`): definisci una metrica, la misuri nel tempo, e scatti quando esce dai limiti. Un **eval set** che gira a ogni deploy è una **regression suite**.
- **Offline vs online:** *offline* = su un set fisso di casi prima del rilascio; *online* = in produzione su traffico reale (feedback impliciti come pollice su/giù, tasso di escalation a umano). Servono entrambi.
- **Il set di valutazione è un asset:** curare 50-200 casi veri e difficili vale più di mille sintetici. Nota di onestà da colloquio: un giudice della **stessa famiglia** del modello valutato e un set piccolo rendono i numeri un **benchmark di decisione**, non una verità assoluta.

## Fonti
- **Hugging Face — LLM Evaluation Guidebook** (github.com/huggingface/evaluation-guidebook)
- **RAGAS** — docs.ragas.io (metriche per RAG: faithfulness, answer/context relevance)
- **Chatbot Arena / LMArena** — lmarena.ai (valutazione pairwise con voti umani)

## Concetti adiacenti
- `ml-eval` — precision/recall, overfitting (la valutazione nel ML classico)
- `xc-llm-chatbot-arch` — dove i guardrail e l'osservabilità vivono nel sistema
- `qe-spc` — control chart: misurare un processo nel tempo e scattare sui limiti

## Quiz (10 — tutte rispondibili dalla lezione)
1. Perché non basta un test `output == atteso` per valutare un LLM?
2. Cos'è un'**allucinazione**?
3. Cos'è un **guardrail** e in cosa è diverso dal modello?
4. Quali sono i **tre modi** di valutare, dal più rigido al più flessibile?
5. Cos'è **LLM-as-judge** e perché è un buon compromesso?
6. Cosa verifica una valutazione di **groundedness** (reference-based)?
7. Cita due **bias** del giudice-LLM e un modo per mitigarli.
8. Nel tuo framework di valutazione, cos'è la **conferma unanime asimmetrica** e a cosa serve?
9. Differenza tra valutazione **offline** e **online**?
10. Perché un **eval set** curato di casi veri è un asset, e quale caveat va detto sui numeri?

<details><summary>Risposte</summary>

1. Perché l'LLM è **non deterministico** e per una domanda aperta esistono **molte** risposte buone: non c'è un'unica stringa attesa da confrontare.
2. Un'affermazione **plausibile ma falsa** (dato/citazione/API inesistente) prodotta con tono sicuro.
3. Un **controllo esplicito** attorno al modello che blocca/corregge output indesiderati (fuori tema, tossici, formato sbagliato); non è il modello, è la rete di sicurezza intorno.
4. **Metriche deterministiche/reference-based** → **human evaluation** → **LLM-as-judge**.
5. Usare **un altro LLM come giudice** con un criterio: **scalabile come il codice** ma capace di sfumature **come un umano**.
6. Che la risposta sia **supportata dal contesto** recuperato (ogni affermazione è nei documenti dati) → misura anti-allucinazione.
7. Preferenza per risposte **più lunghe**, **position bias** (prima posizione), preferenza per lo **stesso modello**; si mitiga con criteri espliciti, invertendo l'ordine, richiedendo conferme multiple.
8. Un verdetto "risolto" conta **solo se sopravvive a 3 ri-controlli su 3** (basta un "no" per bocciare): serve ad **abbassare i falsi positivi**.
9. **Offline** = su un set fisso prima del rilascio; **online** = in produzione su traffico reale (feedback impliciti). Servono entrambi.
10. Perché pochi **casi veri e difficili** catturano i fallimenti reali meglio di mille sintetici; caveat: giudice della stessa famiglia + set piccolo = **benchmark di decisione**, non verità assoluta.
</details>
