---
day: 5
topic_id: xc-llm-agents
title: "Agenti LLM e sistemi multi-agente — tool use, ReAct, orchestrazione"
area: cross-cutting
course: LLM / AI Engineering
grounded_in: null
adjacent: [xc-llm-rag, xc-llm-fundamentals, xc-llm-eval]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo. Nessun acronimo lasciato senza definizione."
---

# Agenti LLM e sistemi multi-agente

> **Perché oggi:** è esattamente ciò che stai progettando. Per **MaiCare** (la tua startup FemTech) hai disegnato un **team di agenti** — nome interno **"Paperclip"** — con ruoli separati e orchestrazione, invece di un unico mega-prompt. Il ruolo che punti (**AI/LLM Engineer**) è, in gran parte, *saper decidere quando e come mettere un LLM dentro un loop con degli strumenti*. Questa lezione mette in fila i concetti che stai già usando, così li sai nominare e difendere a un colloquio.

Prima gli acronimi base: **LLM = Large Language Model**, il modello linguistico di grandi dimensioni (es. Claude, GPT) che, dato del testo in ingresso, produce testo in uscita. **API = Application Programming Interface**, l'interfaccia con cui un programma chiama un altro servizio.

## Da LLM ad agente

Un **LLM "puro"** fa una sola cosa: **testo → testo**. Gli dai un prompt, lui restituisce una risposta. Non naviga il web, non legge un database, non esegue codice: sa solo *predire testo* sulla base di ciò che ha in ingresso (il **contesto**, cioè tutto il testo che gli passi in quel momento). Se gli chiedi "che tempo fa a Torino ora?", inventa o si arrende: non ha modo di *guardare*.

Un **agente** è un LLM messo in un **loop** (ciclo) in cui può:
1. **usare strumenti (tool)** — cioè chiamare funzioni esterne per *agire* sul mondo (cercare sul web, interrogare un DB, chiamare un'API), e
2. **decidere le prossime azioni** da solo, passo dopo passo, per raggiungere un **obiettivo**.

Due definizioni che useremo di continuo:

- **Tool use / function calling** ("uso di strumenti" / "chiamata di funzione"): il meccanismo per cui l'LLM, invece di rispondere in prosa, produce una **chiamata strutturata a una funzione esterna** — es. `cerca_web(query="meteo Torino")`, `query_db(sql=...)`, `chiama_API(...)`. Il tuo programma **esegue** davvero quella funzione, prende il **risultato** e lo **rimette nel contesto** dell'LLM. A quel punto il modello "vede" il risultato reale e continua. Nota il punto chiave: **l'LLM non esegue niente da sé** — decide *quale* funzione chiamare e *con quali argomenti*; a eseguirla è il codice attorno (il "runtime" dell'agente).
- **Agency / autonomia**: il grado in cui l'agente decide **da solo** i passi successivi invece di seguire uno script fisso. Più agency = più libertà (e più potenza), ma anche più imprevedibilità e più costo. Non è un interruttore acceso/spento: è una manopola.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 660 300" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arReact" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12.5" fill="var(--ink)" text-anchor="middle">
   <rect x="250" y="12" width="160" height="40" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="330" y="36">Obiettivo</text>
   <rect x="60" y="110" width="150" height="46" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="135" y="130">Thought</text><text x="135" y="146" font-size="10.5" fill="var(--muted)">(ragiona)</text>
   <rect x="255" y="110" width="150" height="46" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="330" y="130">Action</text><text x="330" y="146" font-size="10.5" fill="var(--muted)">(sceglie tool)</text>
   <rect x="450" y="110" width="170" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="535" y="130">Tool / Ambiente</text><text x="535" y="146" font-size="10.5" fill="var(--muted)">(esegue davvero)</text>
   <rect x="255" y="210" width="150" height="46" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="330" y="230">Observation</text><text x="330" y="246" font-size="10.5" fill="var(--muted)">(risultato)</text>
   <rect x="470" y="248" width="150" height="40" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="545" y="272">Risposta finale</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arReact)">
   <path d="M330,52 L135,108"/>
   <path d="M210,133 L253,133"/>
   <path d="M405,133 L448,133"/>
   <path d="M535,156 L410,225"/>
   <path d="M255,233 L138,158"/>
   <path d="M405,233 L468,255"/>
  </g>
  <g font-size="10.5" fill="var(--muted)" text-anchor="middle"><text x="205" y="200">loop: finché non basta</text></g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Il loop ReAct: dall'obiettivo si entra nel ciclo Thought → Action → Tool/Ambiente → Observation → (di nuovo) Thought, finché l'agente ha abbastanza per la risposta finale.</figcaption>
</figure>

## Il loop ReAct

**ReAct = Reasoning + Acting** ("ragionare + agire"): è il pattern (schema) di agente proposto da Yao et al. (2022) e diventato lo standard di partenza. L'idea è alternare, **a ogni passo**, un pensiero e un'azione, invece di sparare subito una risposta. Il ciclo ha tre momenti che si ripetono:

- **Thought** ("pensiero"): l'LLM scrive **a parole** cosa gli serve fare adesso — es. *"per rispondere mi serve il meteo attuale, uso il tool cerca_web"*. È ragionamento **esplicito** (imparentato con la chain-of-thought, sezione Planning).
- **Action** ("azione"): l'LLM emette la **chiamata a un tool** (function calling): quale strumento e con quali argomenti.
- **Observation** ("osservazione"): il **risultato reale** del tool (il testo restituito, i dati, un eventuale errore) torna nel contesto.

Poi si **ripete**: nuovo Thought che *tiene conto dell'Observation appena arrivata*, nuova Action, nuova Observation… finché l'agente giudica di avere abbastanza per dare la **risposta finale** e chiude il loop.

**Perché batte una risposta secca?** Perché l'agente **si corregge con il feedback dell'ambiente**. Un LLM che risponde in un colpo solo può solo "indovinare bene". Un agente ReAct, se un tool restituisce un errore o un dato inatteso, lo **vede** nell'Observation e cambia mossa al passo dopo (riprova, usa un altro tool, chiede meno dati). Il ragionamento resta **ancorato a fatti reali** presi dagli strumenti, non solo a ciò che il modello "ricorda". Il prezzo è che ogni passo è una chiamata all'LLM: più passi = più costo e più latenza (torna nella sezione rischi).

## I componenti di un agente

### Tool use / function calling

Un **tool** lo definisci con uno **schema** (descrizione strutturata) che dice all'LLM: come si chiama, cosa fa, quali argomenti vuole. In pratica è quasi sempre **JSON = JavaScript Object Notation**, il formato testuale standard per dati strutturati. Esempio di schema di un tool:

```json
{
  "name": "cerca_web",
  "description": "Cerca sul web e restituisce i primi risultati per una query.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Il testo da cercare" }
    },
    "required": ["query"]
  }
}
```

L'LLM legge questa descrizione e, quando serve, produce una chiamata tipo `cerca_web({"query": "meteo Torino oggi"})`. Esempi tipici di tool: **cerca_web** (informazioni fresche), **query_db** (leggere dal database), **chiama_API** (es. meteo, pagamenti), **esegui_codice** (far girare uno snippet in una sandbox), **leggi_file / scrivi_file**. Regola d'oro: la `description` è **prompt a tutti gli effetti** — se è vaga, l'agente sbaglia strumento.

### Memoria

La memoria di un agente è su **due orizzonti**:

- **Memoria a breve termine** = il **contesto della conversazione**: la sequenza di messaggi, Thought, Action e Observation del task in corso, tenuta nella **context window** (la finestra di contesto, cioè la quantità massima di testo — misurata in *token*, i pezzetti in cui il modello spezza il testo — che l'LLM può "vedere" in una volta). È volatile: finito il task o riempita la finestra, va gestita/tagliata.
- **Memoria a lungo termine** = uno **store esterno** da cui l'agente **recupera** informazioni tra sessioni diverse: preferenze dell'utente, fatti appresi, documenti. Tipicamente un **VectorDB (database vettoriale)**: un archivio che salva i testi come **embedding** (vettori di numeri che catturano il significato) e permette di ritrovare i più *simili* a una domanda. È esattamente il meccanismo del **RAG = Retrieval-Augmented Generation** ("generazione aumentata dal recupero", → `xc-llm-rag`): recuperare i pezzi rilevanti e infilarli nel contesto. La memoria a lungo termine di un agente **è** un RAG sulla sua stessa storia.

### Planning

**Planning** ("pianificazione") = **decomporre un obiettivo grande in sotto-task** più piccoli e gestibili, e decidere in che ordine affrontarli. Tre approcci che sentirai nominare:

- **Chain-of-thought (CoT)** ("catena di pensiero"): far ragionare il modello **passo-passo a voce** prima di rispondere ("ragioniamo per gradi…"). Migliora i compiti che richiedono più passaggi logici. È il "Thought" di ReAct.
- **Plan-and-execute** ("pianifica-ed-esegui"): prima l'agente **scrive un piano completo** (lista di passi), poi lo **esegue** un passo alla volta. Più prevedibile e controllabile del decidere tutto al volo.
- **ReAct**: pianificazione **intrecciata all'azione** — decidi il prossimo passo *dopo* aver visto il risultato del precedente. Più reattivo, ma senza un piano d'insieme rischia di "girare in tondo".

### Reflection / self-critique

**Reflection** ("riflessione") o **self-critique** ("auto-critica") = l'agente **valuta e corregge il proprio output** prima di consegnarlo. In pratica: produce una bozza, poi in un passo successivo si chiede *"è corretto? manca qualcosa? il codice compila?"* e, se serve, **rivede**. È come una rilettura critica del proprio compito. Migliora la qualità, ma **costa passi in più** (altre chiamate LLM), quindi va dosata.

## Sistemi multi-agente

Perché usare **più agenti specializzati** invece di uno solo tuttofare? Tre motivi:

- **Separazione delle responsabilità**: ogni agente ha **un** compito chiaro (cercare, scrivere, verificare). Più facile da ragionare, testare e correggere — come dividere un lavoro tra persone con ruoli diversi.
- **Prompt e tool dedicati**: ogni agente ha il **suo** prompt di sistema e **solo i tool che gli servono**. Un unico mega-prompt con venti strumenti confonde il modello; un agente focalizzato sbaglia meno.
- **Robustezza**: se un agente specializzato fallisce, l'errore è **localizzato** e più facile da isolare, invece di corrompere un unico enorme ragionamento.

I **pattern** ricorrenti:

- **Orchestrator-worker** ("coordinatore-lavoratori"): un agente **orchestratore** riceve l'obiettivo, lo spezza in sotto-task e li **assegna** ad agenti **worker** specializzati; poi **ricompone** i loro risultati nella risposta finale. È il pattern del team con un capo-progetto.
- **Pipeline / sequenziale**: gli agenti sono in **catena**, l'**output di uno è l'input del successivo** (es. Estrai → Trasforma → Riassumi). Semplice e prevedibile; adatto quando i passi sono fissi e in ordine noto.
- **Debate / revisione** ("dibattito/revisione"): un agente **produce**, un altro **critica** (o due argomentano tesi opposte). Il confronto fa emergere errori che un singolo agente non vedrebbe. È la reflection (sopra) ma svolta da **agenti separati**.

**I rischi — da conoscere e nominare:**
- **Costo**: più agenti e più passi = **più chiamate LLM** = più soldi e più latenza. Un compito banale può costare 10× senza motivo.
- **Propagazione degli errori**: in una pipeline, un errore all'inizio si **trascina** e amplifica fino in fondo ("garbage in, garbage out").
- **Loop infiniti**: due agenti (o un agente ReAct) possono rimbalzarsi all'infinito senza convergere.

Per questo servono **limiti e guardrail** ("barriere di protezione"): un **max step / max iterazioni** (numero massimo di cicli, oltre il quale si ferma), **timeout** e **budget** di costo, **validazione degli output** (controlli sul formato/contenuto di ciò che un agente passa al successivo) e un **fallback** (piano B) se l'agente non conclude.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 680 300" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arOrch" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12.5" fill="var(--ink)" text-anchor="middle">
   <rect x="40" y="120" width="130" height="56" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="105" y="145">Obiettivo</text><text x="105" y="162" font-size="10.5" fill="var(--muted)">utente</text>
   <rect x="255" y="118" width="160" height="60" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.9"/><text x="335" y="145">Orchestrator</text><text x="335" y="163" font-size="10.5" fill="var(--muted)">assegna e ricompone</text>
   <rect x="510" y="18" width="150" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="585" y="40">Agente Ricerca</text><text x="585" y="55" font-size="10" fill="var(--muted)">tool: cerca_web</text>
   <rect x="510" y="126" width="150" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="585" y="148">Agente Scrittura</text><text x="585" y="163" font-size="10" fill="var(--muted)">tool: —</text>
   <rect x="510" y="234" width="150" height="46" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="585" y="256">Agente Verifica</text><text x="585" y="271" font-size="10" fill="var(--muted)">critica/valida</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arOrch)">
   <path d="M170,148 L253,148"/>
   <path d="M415,140 L508,52"/>
   <path d="M415,148 L508,149"/>
   <path d="M415,156 L508,248"/>
  </g>
  <g stroke="var(--muted)" stroke-width="1.1" stroke-dasharray="4 3" fill="none" marker-end="url(#arOrch)">
   <path d="M508,60 L417,138"/>
   <path d="M508,157 L417,152"/>
   <path d="M508,242 L417,160"/>
  </g>
  <g font-size="10" fill="var(--muted)" text-anchor="middle"><text x="455" y="298">tratteggiato = risultati che tornano</text></g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Pattern orchestrator-worker: l'orchestratore spezza l'obiettivo, lo assegna agli agenti specializzati (Ricerca, Scrittura, Verifica), poi ricompone i risultati (frecce tratteggiate) nella risposta.</figcaption>
</figure>

## Case study (roba tua)

Per **MaiCare** (la mia startup **FemTech** — tecnologia dedicata alla salute femminile) ho progettato un **team di agenti** con nome interno **"Paperclip"**: **ruoli separati** e **orchestrazione**, cioè un modo per far **collaborare più agenti specializzati** su un compito complesso invece di affidarsi a un **unico mega-prompt**. L'idea guida è quella di questa lezione: separare le responsabilità, dare a ciascun agente il suo prompt e i suoi tool, e coordinarli. (Mi fermo qui, onestamente: niente metriche o dettagli tecnici precisi che non posso verificare.)

## Notable use cases / framework reali

Framework e prodotti reali che implementano questi pattern (descrizioni generali, senza dettagli interni inventati):

- **LangGraph** (di LangChain): libreria per costruire agenti come **grafi di stati** — nodi e transizioni espliciti. Utile quando vuoi controllo fine su loop, rami e guardrail.
- **AutoGen** (Microsoft): framework per **conversazioni tra più agenti** che si scambiano messaggi per risolvere un task (adatto ai pattern debate/orchestrator).
- **CrewAI**: framework che modella gli agenti come una **"crew"** (equipaggio) con **ruoli** e **task** assegnati — molto vicino alla metafora del team.
- **OpenAI Assistants / Agents SDK**: strumenti di OpenAI per costruire agenti con tool, memoria e orchestrazione gestiti.
- **Coding agent** (pattern): un agente che **legge il codice, esegue comandi, modifica file e verifica i risultati** in loop — è il caso d'uso oggi più maturo (lo stai usando adesso). Esempi di questa famiglia: Claude Code, ecc.

## Completeness check (integrato da me)

**Quando NON servono gli agenti.** Gli agenti aggiungono **costo** e **imprevedibilità**: non sono gratis. Se il compito si risolve con **una singola chiamata** all'LLM (riassumi questo testo, classifica questo messaggio) o con un **RAG semplice** (recupera i documenti giusti e rispondi), **non mettere un loop di agenti**: aggiungeresti passi, latenza e possibilità di sbagliare senza guadagno. La regola: parti dalla soluzione **più semplice** (prompt secco → RAG → agente singolo → multi-agente) e sali di complessità **solo quando la semplice non basta**. Anthropic lo dice esplicitamente nel suo "Building effective agents": usa la potenza minima necessaria.

**La valutazione (aggancio a `xc-llm-eval`).** Un agente è **difficile da valutare** proprio perché non è deterministico e fa più passi: due esecuzioni sullo stesso input possono differire. Servono strumenti dedicati — **task di test** con esito verificabile, controllo dei **passi intermedi** (ha usato i tool giusti?), non solo dell'output finale, e spesso un **LLM-as-judge** (un LLM che valuta la risposta di un altro). Senza valutazione, "sembra funzionare" non è "funziona": è il tema di `xc-llm-eval`.

## Fonti

- **ReAct: Synergizing Reasoning and Acting in Language Models** — Yao et al., arXiv (arxiv.org/abs/2210.03629): il paper del loop ReAct.
- **LangGraph — documentazione** — langchain-ai.github.io/langgraph
- **Building effective agents** — Anthropic (anthropic.com): quando (e quando no) usare agenti, con i pattern.
- **AutoGen — documentazione** — microsoft.github.io/autogen

## Concetti adiacenti

- `xc-llm-rag` — Retrieval-Augmented Generation: il meccanismo di recupero che alimenta la memoria a lungo termine degli agenti.
- `xc-llm-eval` — Valutazione di LLM e agenti: come misuri che un sistema non deterministico funzioni davvero.
- `xc-llm-fundamentals` — Fondamenti degli LLM: token, context window, prompting, su cui poggia tutto il resto.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cosa distingue un **agente** da un **LLM "puro"**?
2. Cos'è il **function calling / tool use**, e chi *esegue* davvero la funzione: l'LLM o il codice attorno?
3. Cosa significa l'acronimo **ReAct** e quali sono i **tre momenti** del suo ciclo?
4. Perché un agente ReAct **batte** una risposta secca in un colpo solo?
5. Differenza tra **memoria a breve termine** e **a lungo termine** di un agente, e con quale altro tema si collega la memoria a lungo termine?
6. Descrivi il pattern **orchestrator-worker** in una frase.
7. Cita **un rischio** dei sistemi multi-agente e **un guardrail** che lo mitiga.
8. Cos'è la **reflection / self-critique** e qual è il suo costo?
9. **Quando NON** conviene usare un sistema di agenti?
10. Cos'è la **context window** e in cosa si misura?

<details><summary>Risposte</summary>

1. Un **LLM puro** fa solo **testo → testo** (nessuna azione sul mondo). Un **agente** è un LLM messo in un **loop** in cui può **usare tool** (agire) e **decidere da solo le prossime azioni** per raggiungere un obiettivo.
2. È il meccanismo per cui l'LLM produce una **chiamata strutturata a una funzione esterna** (nome + argomenti, in JSON) invece di rispondere in prosa; il **risultato torna nel contesto**. A **eseguirla è il codice attorno** (il runtime dell'agente), non l'LLM: il modello decide solo *quale* funzione e *con quali argomenti*.
3. **ReAct = Reasoning + Acting** (ragionare + agire). Ciclo: **Thought** (ragiona a parole) → **Action** (sceglie e chiama un tool) → **Observation** (il risultato reale torna nel contesto), ripetuto finché basta.
4. Perché **si corregge con il feedback dell'ambiente**: se un tool dà errore o un dato inatteso, l'agente lo **vede** nell'Observation e cambia mossa al passo dopo; il ragionamento resta **ancorato a fatti reali**, non solo a ciò che il modello "ricorda".
5. **Breve termine** = il **contesto della conversazione** in corso (messaggi/Thought/Action/Observation nella context window, volatile). **Lungo termine** = uno **store esterno** (tipicamente un **VectorDB**) da cui l'agente **recupera** info tra sessioni. La memoria a lungo termine si collega al **RAG** (Retrieval-Augmented Generation).
6. Un agente **orchestratore** spezza l'obiettivo in sotto-task, li **assegna** ad agenti **worker** specializzati e poi **ricompone** i loro risultati nella risposta finale.
7. **Rischio** (uno tra): costo/latenza per le molte chiamate LLM; propagazione degli errori lungo la pipeline; loop infiniti. **Guardrail** corrispondente (uno tra): **max step/iterazioni**, timeout/budget, **validazione degli output**, fallback.
8. È l'agente che **valuta e corregge il proprio output** prima di consegnarlo (auto-critica/rilettura). Il **costo** sono **passi/chiamate LLM in più**, quindi va dosata.
9. Quando basta una **singola chiamata** all'LLM (riassumere, classificare) o un **RAG semplice**: lì gli agenti aggiungono solo **costo e imprevedibilità** senza guadagno. Parti dal più semplice e sali di complessità solo se serve.
10. La **context window** (finestra di contesto) è la **quantità massima di testo che l'LLM può vedere in una volta**; si misura in **token** (i pezzetti in cui il modello spezza il testo).
</details>
