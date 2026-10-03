---
day: 16
topic_id: se-vcs
title: "Controllo di versione — Git (branch, merge, pull request)"
area: computer-science
course: Ingegneria del Software
grounded_in: "UNIBO/terzoAnno/IngengeriaDelSoftware (cap. 11)"
adjacent: [xc-swe-review, sa-devops, xc-do-cicd]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo."
---

# Controllo di versione — Git

> **Perché oggi:** Git è lo strumento che usi **tutti i giorni** da software engineer. Senza, non collabori a un progetto reale: è dato per scontato in ogni team e chiesto a ogni colloquio ("mi spieghi come funziona un branch? cos'è una pull request?"). Non è teoria da lasciare all'università: è il gesto quotidiano con cui salvi, condividi e integri il tuo lavoro. Anche questo ripasso-uni è versionato con Git — ogni lezione che leggi è un commit nella storia del progetto.

## Cos'è un sistema di controllo di versione (VCS)

Un **VCS = Version Control System** (sistema di controllo di versione) è uno strumento che tiene la **storia** di tutte le modifiche a un progetto. In pratica ti dà quattro superpoteri:

- **Tornare indietro**: se una modifica ha rotto tutto, recuperi una versione precedente che funzionava, senza aver salvato a mano copie tipo `progetto_finale_v2_DEFINITIVO`.
- **Vedere chi ha cambiato cosa e quando**: ogni modifica è registrata con autore, data e una descrizione. Puoi risalire a quando è stata introdotta una riga e perché.
- **Collaborare senza pestarsi i piedi**: più persone lavorano sullo stesso progetto in parallelo, e il VCS sa **unire** i loro contributi.
- **Sperimentare in sicurezza**: provi un'idea in una linea separata; se non funziona, la butti senza aver toccato il lavoro buono.

Ci sono due grandi famiglie di VCS, e la differenza è **dove vive la storia**:

- **Centralizzato** (es. **SVN**, Subversion): esiste **un unico server** che custodisce tutta la storia. Gli sviluppatori hanno solo l'ultima versione dei file sul proprio PC; per salvare una modifica o vedere la storia devono parlare col server. Se il server è irraggiungibile (sei offline, è in manutenzione) non committi e non consulti la storia; se si perde senza backup, perdi tutto.
- **Distribuito** (es. **Git**): **ogni sviluppatore ha una copia completa** del repository, storia inclusa. Committi, guardi la storia, crei branch **in locale**, senza rete. Ti sincronizzi col resto del team solo quando vuoi.

**Perché il distribuito ha vinto:** è più veloce (quasi tutto avviene in locale, senza attese di rete), lavori anche **offline**, ogni copia è di fatto un **backup** completo, ed è pensato per creare e unire **branch** con leggerezza — il che abilita il modo di collaborare moderno (branch + pull request) che vedi più sotto. Git, creato nel 2005 per lo sviluppo del kernel Linux, è oggi lo standard di fatto.

## I concetti di Git (il modello mentale)

Prima dei comandi, i termini. Se questi sei ti sono chiari, Git smette di sembrare magia:

- **Repository (repo)** — il **progetto insieme a tutta la sua storia**. Non è solo la cartella coi file di adesso: è la cartella *più* l'archivio di ogni versione passata (che Git tiene in una sottocartella nascosta `.git`).
- **Commit** — uno **snapshot** (una fotografia) del progetto in un dato istante, salvato con un **messaggio** che descrive la modifica e un **identificatore** univoco (un **hash**, cioè un codice tipo `a1b2c3d`). Un commit dice: "a questo punto della storia, i file erano fatti così, e l'ho fatto per questo motivo". È l'unità base della storia.
- **Le tre aree** dove può stare una modifica:
  - **Working directory** (directory di lavoro) — **i tuoi file** sul disco, quelli che stai modificando adesso nell'editor.
  - **Staging area / index** (area di staging o indice) — una zona di **preparazione**: cosa hai deciso di includere nel **prossimo commit**. Metti in staging le modifiche pronte, lasciando fuori quelle a metà. È il "carrello" prima di finalizzare la spesa.
  - **Repository** — la **storia committata**, cioè gli snapshot già salvati in modo permanente.
- **Branch** (ramo) — una **linea di sviluppo parallela**. Tecnicamente è solo un **puntatore mobile** a un commit: mentre committi, il branch avanza e punta all'ultimo commit. Ti serve per lavorare a una cosa (una feature, un bugfix) **isolata** dal resto. Il branch principale si chiama per convenzione **`main`** (in progetti più vecchi, `master`).
- **HEAD** — un puntatore speciale che indica **dove sei ora**: il commit/branch su cui stai lavorando in questo momento. Quando cambi branch, sposti HEAD.
- **Remote** — una **copia del repo su un server**, condivisa dal team (es. su GitHub). Il remote di default si chiama per convenzione **`origin`**. Il tuo repo locale e il remote si scambiano commit quando fai `push` e `pull`.

## Le tre aree e i comandi che spostano i file

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 200" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arGit16" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
   <rect x="8" y="70" width="150" height="50" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="83" y="90">Working dir</text><text x="83" y="106" font-size="9.5" fill="var(--muted)">i tuoi file</text>
   <rect x="192" y="70" width="150" height="50" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="267" y="90">Staging</text><text x="267" y="106" font-size="9.5" fill="var(--muted)">prossimo commit</text>
   <rect x="376" y="70" width="150" height="50" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="451" y="90">Repository</text><text x="451" y="106" font-size="9.5" fill="var(--muted)">storia (locale)</text>
   <rect x="560" y="70" width="150" height="50" rx="9" fill="var(--card)" stroke="var(--rule)"/><text x="635" y="90">Remote</text><text x="635" y="106" font-size="9.5" fill="var(--muted)">origin (server)</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arGit16)">
   <path d="M158,88 L190,88"/>
   <path d="M342,88 L374,88"/>
   <path d="M526,88 L558,88"/>
   <path d="M558,132 C450,168 266,168 160,132"/>
  </g>
  <g font-size="9.5" fill="var(--accent)" text-anchor="middle">
   <text x="174" y="80">git add</text>
   <text x="358" y="80">git commit</text>
   <text x="542" y="80">git push</text>
  </g>
  <text x="360" y="162" font-size="9.5" fill="var(--muted)" text-anchor="middle">git pull (dal remote fino ai tuoi file)</text>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Le tre aree di Git più il remote, e i comandi che spostano le modifiche da una all'altra. Da sinistra: <code>git add</code> mette in staging, <code>git commit</code> salva lo snapshot nella storia locale, <code>git push</code> lo manda al server. <code>git pull</code> fa il percorso inverso: porta nel tuo repo (e nei tuoi file) i commit nuovi dal remote.</figcaption>
</figure>

## Il workflow di tutti i giorni (con i comandi)

Questi sono i comandi che digiti davvero ogni giorno. Impara questi e sei operativa.

- **`git clone <url>`** — copia un repo esistente (dal remote) sul tuo PC. È il primo comando quando entri in un progetto: `git clone https://github.com/team/progetto.git`. Ti scarica i file **e** tutta la storia, e imposta già `origin` come remote.
- **`git status`** — ti dice **cosa è cambiato**: quali file hai modificato, cosa è in staging e cosa no, su quale branch sei. È il comando che lanci di continuo per orientarti.
- **`git add <file>`** — mette una modifica **in staging** (la prepara per il prossimo commit). `git add .` mette in staging **tutto** ciò che è cambiato nella cartella corrente.
- **`git commit -m "messaggio"`** — salva uno **snapshot** delle modifiche in staging, con un **messaggio** che spiega cosa e perché: `git commit -m "Aggiungi validazione email nel form di contatto"`. Da qui in poi quella versione è nella storia e la puoi recuperare.
- **`git push`** — manda i tuoi commit locali al **remote** (`origin`), così il team li vede. `git pull` — scarica dal remote i commit fatti dagli altri e li integra nel tuo lavoro. La regola: **`pull` spesso (per restare allineata), `push` quando hai qualcosa di sensato da condividere.**
- **`git log`** — mostra la **storia** dei commit (hash, autore, data, messaggio). `git log --oneline` la mostra compatta, un commit per riga.

**Branch** — il gesto quotidiano per lavorare a qualcosa senza toccare `main`:

- **`git branch`** — elenca i branch esistenti e ti dice su quale sei.
- **`git checkout -b <nome>`** oppure **`git switch -c <nome>`** — **crea** un nuovo branch **e** ci passa sopra in un colpo solo (`switch` è il comando più recente e leggibile; `checkout` è quello storico che fa la stessa cosa). Esempio: `git switch -c feature/login`.
- Lavori sul branch (modifichi, `add`, `commit` quante volte serve), poi lo **unisci** a `main` con un **merge** — di solito passando da una **pull request** (vedi sotto).

Un giro completo tipico: `git switch -c feature/x` → modifichi → `git add .` → `git commit -m "..."` → `git push` → apri la pull request → dopo la review, si mergia in `main`.

## Branch, merge e conflitti

**Perché si lavora su branch:** per **isolare** una modifica (una feature, un fix) senza rompere `main`. `main` deve restare sempre in uno stato funzionante — è la versione "buona", spesso quella che va in produzione. Tu ti crei un branch, ci fai tutti i tuoi commit sperimentali, e finché non è pronto il resto del team non ne risente. Se l'idea non funziona, cancelli il branch e `main` non se n'è nemmeno accorto.

<svg viewBox="0 0 680 170" style="max-width:100%;height:auto;font-family:inherit">
  <g stroke="var(--rule)" stroke-width="2" fill="none">
    <path d="M40,120 L640,120"/>
    <path d="M180,120 C240,120 250,55 300,55 L440,55 C500,55 500,110 520,120"/>
  </g>
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
    <circle cx="60" cy="120" r="11" fill="var(--card)" stroke="var(--rule)" stroke-width="1.6"/>
    <circle cx="180" cy="120" r="11" fill="var(--card)" stroke="var(--rule)" stroke-width="1.6"/>
    <circle cx="300" cy="55" r="11" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
    <circle cx="420" cy="55" r="11" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
    <circle cx="520" cy="120" r="12" fill="var(--card)" stroke="var(--good)" stroke-width="2"/>
    <circle cx="620" cy="120" r="11" fill="var(--card)" stroke="var(--rule)" stroke-width="1.6"/>
    <text x="60" y="150" fill="var(--muted)">main</text>
    <text x="360" y="34" fill="var(--accent)">feature/login</text>
    <text x="520" y="150" fill="var(--good)">merge</text>
    <text x="180" y="150" fill="var(--muted)" font-size="10">branch parte qui</text>
  </g>
</svg>

<figcaption style="font-size:12px;color:var(--muted);margin-top:4px;text-align:center">Un branch <code>feature/login</code> parte da un commit di <code>main</code>, accumula i suoi commit in isolamento, e il <b>merge</b> li reintegra in <code>main</code> con un commit di fusione. Se i due lati hanno toccato le stesse righe, Git segnala un <b>conflitto</b> da risolvere a mano.</figcaption>

**Merge (fusione):** unire i commit di un branch in un altro. Tipicamente: hai finito `feature/login`, la vuoi in `main`. Il merge prende il lavoro del tuo branch e lo integra. Nella maggioranza dei casi Git lo fa **da solo**, perché i due branch hanno toccato file o righe diverse.

**Merge conflict (conflitto di merge):** succede quando **due branch hanno modificato le stesse righe dello stesso file** in modi diversi. Git non può indovinare quale versione tenere, quindi **si ferma e chiede a te** di decidere. Nel file comparirà una zona marcata così:

```
<<<<<<< HEAD
codice della tua versione (il branch corrente)
=======
codice dell'altra versione (il branch che stai unendo)
>>>>>>> feature/login
```

**Come si risolve:** apri il file, **scegli tu** cosa tenere (una delle due versioni, o una combinazione), **cancelli i marcatori** `<<<<<<<`, `=======`, `>>>>>>>`, poi fai `git add <file>` per segnare il conflitto come risolto e infine `git commit` per concludere il merge. Un conflitto **non è un errore né una rottura**: è Git che ti chiede una decisione umana che solo tu puoi prendere.

**Merge vs rebase (cenno):** ci sono due modi di integrare i commit di un branch.
- **Merge** crea un commit di unione e **conserva** la storia com'è andata (i due rami restano visibili).
- **Rebase** invece **"riscrive" la storia**: prende i tuoi commit e li **rimette in cima** ai commit più recenti dell'altro branch, come se avessi lavorato partendo da lì. Il risultato è una storia **più lineare e pulita**.
- La regola d'oro: **non fare rebase su branch condivisi** (quelli su cui lavorano anche altri). Riscrivere la storia di un branch che altri hanno già scaricato manda in confusione le loro copie. Rebase va bene sul tuo branch privato; su ciò che è pubblico si usa il merge.

## Pull request e collaborazione

La **pull request (PR)** — chiamata **merge request** su GitLab — è il meccanismo con cui **proponi** di unire il tuo branch in `main`. Non mergi tu direttamente: apri una PR e dici al team "ho fatto questa feature sul branch `feature/login`, la vorrei in `main`, date un'occhiata".

A quel punto scatta la **code review**: i colleghi **leggono le tue modifiche**, commentano riga per riga, chiedono cambiamenti, approvano. Tu rispondi, magari fai altri commit sul branch per sistemare, e la PR si aggiorna. Solo **dopo l'approvazione** la PR viene **mergiata** in `main`. È il cuore della collaborazione moderna: nessuno butta codice in `main` senza che almeno un altro paio d'occhi lo abbia visto (approfondimento in `xc-swe-review`).

Due meccanismi che rendono la PR una vera "porta di controllo":
- **Branch protection** (protezione del branch): si configura il repo perché su `main` **non si possa pushare direttamente** — l'unico modo per entrare è una PR approvata. Così `main` resta sempre pulito.
- **CI sui PR** (Continuous Integration): a ogni PR parte in automatico una pipeline che **compila il codice e lancia i test**. Se qualcosa non passa, la PR si segna come fallita e non si mergia finché non è verde. Così il codice rotto viene fermato prima di arrivare in `main` (approfondimento in `xc-do-cicd`).

## File e pratiche utili

- **`.gitignore`** — un file di testo in cui elenchi i **pattern di file che Git NON deve versionare**. Serve a tenere fuori dalla storia ciò che non è codice sorgente: le **dipendenze** scaricabili (es. `node_modules/`), i **segreti** (file `.env` con password e chiavi), gli **artefatti di build** (cartelle `dist/`, `build/`), i file temporanei dell'editor e del sistema. Regola pratica: nel repo va **solo ciò che serve a ricostruire il progetto**, non ciò che si può rigenerare o che è segreto.
- **Buoni messaggi di commit** — chiari, che dicono **cosa** cambia e **perché**, scritti al **presente/imperativo** ("Aggiungi validazione email", non "aggiunte varie" o "ho sistemato"). Un buon messaggio è quello che, riletto tra sei mesi da un collega, spiega la modifica senza dover aprire il codice.
- **Commit piccoli e frequenti** — ogni commit dovrebbe fare **una cosa sola e coerente**. Meglio dieci commit piccoli e a tema che un commitone che mischia tutto: sono più facili da leggere in review, da capire nella storia e da annullare singolarmente se serve.
- **MAI committare segreti** — password, API key, token, chiavi private **non vanno mai** in un commit. La storia di Git è **permanente**: una volta committato e pushato, il segreto resta negli snapshot passati anche se lo cancelli dopo, e chiunque cloni il repo lo trova. Segreti fuori dal repo (variabili d'ambiente, file `.env` messo in `.gitignore`).

## Errori comuni

- **Committare segreti o file enormi.** Password e chiavi finiscono per sempre nella storia (vedi sopra); file binari giganti (video, dataset, dipendenze) gonfiano il repo e rallentano ogni clone. Prevenzione: `.gitignore` fatto bene, fin dal primo commit.
- **Messaggi di commit inutili** — "fix", "update", "asdf", "varie". Non dicono niente: fra un mese nessuno (nemmeno tu) capisce cosa è successo. Il messaggio è documentazione gratis, non sprecarla.
- **Commit giganti che mescolano dieci cose** — un unico commit che tocca la feature, sistema un bug, rinomina venti file e cambia lo stile. Illeggibile in review e impossibile da annullare in parte. Spezza in commit a tema.
- **Lavorare direttamente su `main`.** Salti il branch e committi le tue prove sul ramo buono: rischi di romperlo per tutti e ti perdi review e CI. Sempre un **feature branch**.
- **Non fare `pull` prima di `push`.** Se gli altri hanno pushato mentre lavoravi e tu non ti sei allineata, il tuo `push` viene rifiutato e ti ritrovi a gestire conflitti nel momento peggiore. Abitudine: `git pull` prima di iniziare e prima di pushare.

## Notable use cases

- **Host del repository.** Il repo remoto vive su piattaforme dedicate: **GitHub**, **GitLab**, **Bitbucket**. Offrono lo storage del repo più gli strumenti di collaborazione: pull/merge request, code review, gestione dei permessi, issue, e le pipeline di CI/CD integrate.
- **Il flusso standard di ogni team software.** Praticamente ovunque si lavora così: **feature branch** (un branch per ogni pezzo di lavoro) → **pull request** con **code review** → **CI** che compila e testa in automatico → **merge in `main`** solo se review approvata e CI verde, con `main` protetto da branch protection. È il modello che troverai (con piccole varianti) in qualunque azienda, ed è quello che i colloqui danno per scontato tu sappia descrivere.

## Fonti

- **Pro Git** (git-scm.com/book) — il libro di riferimento su Git, **gratuito** e online, di Scott Chacon e Ben Straub. Se un giorno un dubbio su Git va chiarito bene, si parte da qui.
- **Documentazione di GitHub** (docs.github.com) — guide pratiche su pull request, branch protection, GitHub Actions (la CI di GitHub) e il flusso di collaborazione.
- **Atlassian Git tutorials** (atlassian.com/git) — tutorial molto chiari e visivi su branch, merge, rebase e workflow, dai creatori di Bitbucket.

## Concetti adiacenti

- **xc-swe-review** — la code review nella pratica: cosa si guarda in una pull request, come si dà e si riceve feedback, perché è il punto in cui la qualità entra nel codice.
- **sa-devops** — la cultura DevOps in cui Git è il fondamento: dal commit al rilascio, automazione e collaborazione tra sviluppo e operations.
- **xc-do-cicd** — le pipeline di CI/CD che girano sui commit e sui PR: build, test e deploy automatici innescati da Git.
- **se-process** — i processi e i modelli di sviluppo (agile, iterativo) dentro cui il workflow a branch e pull request prende senso a livello di team.

## Quiz (10 — tutte rispondibili dalla lezione)

1. Cos'è un **VCS** e quali superpoteri ti dà?
2. Qual è la differenza tra VCS **centralizzato** e **distribuito**, e perché il distribuito ha vinto?
3. Cos'è un **commit**? Da cosa è composto?
4. Quali sono le **tre aree** di Git e **quale comando** sposta una modifica dall'una all'altra (fino al remote)?
5. Cos'è un **branch** e perché si lavora su un branch invece che direttamente su `main`?
6. Cos'è un **merge conflict**, quando si verifica e come si **risolve**?
7. Qual è la differenza tra **merge** e **rebase**, e qual è la regola d'oro sul rebase?
8. Cos'è una **pull request** e cosa succede tra l'aprirla e il mergiarla?
9. A cosa serve il file **`.gitignore`** e cosa ci si mette dentro?
10. Cita e spiega **un errore comune** con Git e come evitarlo.

<details><summary>Risposte</summary>

1. Un **VCS (Version Control System)** è uno strumento che tiene la **storia** di tutte le modifiche a un progetto. I superpoteri: **tornare indietro** a una versione precedente, vedere **chi ha cambiato cosa e quando**, **collaborare** in più persone senza pestarsi i piedi, e **sperimentare in sicurezza** su linee separate.

2. Nel **centralizzato** (es. SVN) la storia vive su **un unico server**: gli sviluppatori hanno solo l'ultima versione e devono parlare col server per committare o vedere la storia. Nel **distribuito** (es. Git) **ogni sviluppatore ha una copia completa** del repo, storia inclusa, e lavora in locale. Il distribuito ha vinto perché è **più veloce** (quasi tutto in locale), funziona **offline**, ogni copia è un **backup**, ed è pensato per creare e unire **branch** con leggerezza, abilitando il workflow branch + pull request.

3. Un **commit** è uno **snapshot** (una fotografia) del progetto in un dato istante. È composto da un **messaggio** che descrive la modifica e un **identificatore univoco** (un **hash**, es. `a1b2c3d`). È l'unità base della storia: dice come erano i file a quel punto e perché.

4. Le tre aree sono **working directory** (i tuoi file), **staging area/index** (cosa hai preparato per il prossimo commit) e **repository** (la storia committata). I comandi: **`git add`** porta dalla working directory allo staging, **`git commit`** dallo staging al repository (storia locale), **`git push`** dal repository locale al **remote**. Al contrario, **`git pull`** porta i commit nuovi dal remote fino ai tuoi file.

5. Un **branch** (ramo) è una **linea di sviluppo parallela**, tecnicamente un **puntatore mobile** a un commit. Si lavora su un branch per **isolare** una modifica (feature o fix) senza rompere **`main`**, che deve restare sempre funzionante (spesso è la versione in produzione). Se l'idea non funziona, cancelli il branch e `main` non ne risente.

6. Un **merge conflict** si verifica quando **due branch hanno modificato le stesse righe dello stesso file** in modi diversi: Git non sa quale tenere e **si ferma chiedendo a te**. Nel file compaiono i marcatori `<<<<<<<`, `=======`, `>>>>>>>` con le due versioni. Si **risolve** aprendo il file, scegliendo cosa tenere, **cancellando i marcatori**, poi `git add <file>` per segnarlo risolto e `git commit` per concludere il merge. Non è un errore, è una decisione umana richiesta.

7. Il **merge** crea un commit di unione e **conserva** la storia com'è andata (i due rami restano visibili). Il **rebase** **"riscrive" la storia** rimettendo i tuoi commit **in cima** ai commit più recenti dell'altro branch, ottenendo una storia più **lineare e pulita**. Regola d'oro: **non fare rebase su branch condivisi** (su cui lavorano altri), perché riscrivere la storia manda in confusione le loro copie.

8. Una **pull request (PR)** — merge request su GitLab — è la **proposta** di unire il tuo branch in `main`. Tra l'aprirla e il mergiarla scatta la **code review**: i colleghi leggono le modifiche, commentano, chiedono cambiamenti; tu rispondi ed eventualmente fai altri commit. Solo **dopo l'approvazione** (e con la **CI** verde, se configurata) la PR viene **mergiata** in `main`.

9. **`.gitignore`** è un file che elenca i **pattern di file che Git NON deve versionare**. Ci si mettono: **dipendenze** scaricabili (es. `node_modules/`), **segreti** (file `.env`), **artefatti di build** (`dist/`, `build/`), file temporanei di editor e sistema. Regola: nel repo va solo ciò che serve a ricostruire il progetto, non ciò che è rigenerabile o segreto.

10. Esempi validi (basta uno spiegato): **committare segreti** (restano per sempre nella storia permanente — si evita con `.gitignore` e variabili d'ambiente); **messaggi di commit inutili** ("fix", "asdf" — si evita scrivendo cosa e perché); **commit giganti che mescolano dieci cose** (illeggibili in review — si evita con commit piccoli e a tema); **lavorare direttamente su `main`** (rischi di romperlo — si evita usando sempre un feature branch); **non fare `pull` prima di `push`** (il push viene rifiutato e ti ritrovi conflitti — si evita facendo `git pull` prima di iniziare e prima di pushare).

</details>
