---
day: 51
topic_id: xc-do-cicd
title: "CI/CD: integrazione e consegna continua"
area: cross-cutting
course: "DevOps & Cloud-native"
grounded_in: null
adjacent: [sa-devops, xc-do-containers, se-vcs, xc-swe-tdd]
completeness_checked: true
quiz_count: 10
---

# CI/CD: integrazione e consegna continua

> **Perché oggi:** in `se-vcs` hai imparato a lavorare con Git, branch e pull request; in `xc-do-containers` hai visto come impacchettare l'app in un'immagine. CI/CD è il nastro trasportatore che collega le due cose: ogni volta che qualcuno fa push del codice, una **pipeline** automatica lo compila, lo testa, costruisce l'artefatto e lo porta fino in produzione, senza che nessuno esegua passi a mano. È una delle pratiche più citate nei colloqui e una delle poche cose che distingue un progetto "giocattolo" da uno che un team può mantenere. Oggi vediamo cosa significano le tre lettere, com'è fatta una pipeline e come se ne scrive uno step reale.

## Cosa vogliono dire CI, CD e CD
**CI/CD** sta per **Continuous Integration / Continuous Delivery (o Deployment)**. Sono tre pratiche collegate, spesso confuse:

- **CI, Continuous Integration (integrazione continua):** la pratica per cui ogni sviluppatore **integra spesso** il proprio lavoro nel ramo principale (anche più volte al giorno), e a ogni integrazione un sistema automatico **compila ed esegue i test**. L'obiettivo è scoprire subito se una modifica rompe qualcosa, quando è ancora piccola e facile da sistemare, invece di accumulare settimane di lavoro che poi non si fondono più ("integration hell").
- **CD, Continuous Delivery (consegna continua):** l'estensione della CI che, dopo i test, prepara **automaticamente un artefatto rilasciabile** e lo porta fino alla soglia della produzione. Il rilascio finale resta un gesto umano: qualcuno clicca "approva". In ogni momento c'è una versione **pronta** da rilasciare.
- **CD, Continuous Deployment (distribuzione continua):** un passo più in là. Se tutti i test passano, la modifica va **in produzione da sola**, senza approvazione manuale. Richiede grande fiducia nei test e nel monitoraggio.

In breve: la Delivery ti lascia il bottone "vai" da premere; il Deployment preme il bottone al posto tuo.

## La pipeline: il concetto centrale
Una **pipeline** è la sequenza automatizzata di passi che il codice attraversa dal commit alla produzione. È definita come **codice** (un file di configurazione versionato insieme al progetto, es. `.github/workflows/ci.yml`), così la ricetta della build vive accanto al software e cambia con esso.

Vocabolario di base (vale, con piccole differenze di nome, per GitHub Actions, GitLab CI, Jenkins):
- **Trigger (evento scatenante):** cosa fa partire la pipeline. Tipicamente un **push** su un branch o l'apertura di una **pull request**.
- **Stage (fase):** un blocco logico della pipeline (build, test, deploy).
- **Job (lavoro):** un insieme di passi eseguiti sulla stessa macchina. Job diversi possono girare **in parallelo**.
- **Step (passo):** la singola azione dentro un job (es. "esegui i test").
- **Runner (esecutore):** la macchina (spesso un container effimero) su cui la pipeline viene eseguita. Parte pulita a ogni esecuzione, garantendo che la build non dipenda dallo stato di un PC.
- **Artefatto (artifact):** l'output da conservare e far passare agli stage successivi (un binario, un pacchetto, un'immagine container).

## Le fasi tipiche di una pipeline
Dal commit alla produzione, gli stage ricorrenti sono:

1. **Checkout e build:** la pipeline scarica il codice e lo **compila** (o prepara le dipendenze per i linguaggi interpretati).
2. **Lint e analisi statica:** un **linter** controlla stile e errori sospetti senza eseguire il codice; strumenti di **SAST (Static Application Security Testing)** cercano vulnerabilità note analizzando il sorgente.
3. **Test automatici:** si eseguono i test. La **test pyramid** (vedi `xc-swe-tdd`) suggerisce molti **unit test** veloci alla base, meno **test di integrazione** sopra, pochissimi **test end-to-end (e2e)** in cima. Qui si misura spesso la **code coverage** (percentuale di codice eseguito dai test).
4. **Build dell'artefatto:** si produce ciò che verrà rilasciato. Nel mondo cloud-native, di solito un'**immagine container** che viene mandata (push) in un **registry** (il concetto visto in `xc-do-containers`).
5. **Deploy in staging:** l'artefatto viene messo in un ambiente di prova (**staging**) il più possibile identico alla produzione, dove girano test e2e e controlli finali.
6. **Deploy in produzione:** con approvazione (Delivery) o automatico (Deployment).

Un principio d'oro attraversa tutto: **build once, deploy many** (costruisci una volta sola, distribuisci ovunque). L'artefatto testato in staging deve essere **esattamente** quello che va in produzione; non si ricostruisce da capo, perché una nuova build potrebbe introdurre differenze. È qui che i container danno il meglio: la stessa immagine attraversa tutti gli ambienti.

## Perché la pipeline deve essere veloce e affidabile
Una pipeline ha valore solo se le persone si fidano del suo esito. Due nemici:
- **Lentezza:** se i test ci mettono un'ora, nessuno aspetta e la CI viene aggirata. Si combatte con la **cache** delle dipendenze, i job in **parallelo** e il tenere veloci gli unit test.
- **Test "flaky" (ballerini):** test che a volte passano e a volte no senza che il codice sia cambiato. Erodono la fiducia: dopo due falsi allarmi, la gente ignora anche gli allarmi veri. Vanno isolati e sistemati.

La metrica chiave della CI è **mantenere il ramo principale sempre "verde"** (tutti i test passano): così chiunque può partire da lì sapendo che è sano.

## Strategie di rilascio sicuro
Portare codice in produzione senza spaventarsi richiede tecniche che limitano il danno di un eventuale bug:
- **Rolling deploy:** si sostituiscono le istanze a scaglioni (la stessa idea del rolling update visto in `xc-do-containers`).
- **Blue-green:** si tengono due ambienti identici, **blue** (attuale) e **green** (nuova versione). Quando green è pronto e testato, si **sposta tutto il traffico** su green in un colpo; se qualcosa va storto, si torna istantaneamente a blue.
- **Canary:** si manda la nuova versione a una **piccola fetta** di utenti (il "canarino nella miniera"); se le metriche restano sane, si estende gradualmente a tutti, altrimenti si ferma.
- **Feature flag:** si rilascia il codice **spento** dietro un interruttore e lo si accende quando si vuole, anche per pochi utenti, scollegando il *deploy* dal *rilascio* della funzionalità.

Accanto va sempre il **rollback**: la capacità di tornare rapidamente alla versione precedente. Una pipeline matura rende il rollback banale quanto il deploy.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 760 210" style="max-width:100%;height:auto;font-family:inherit">
  <defs>
    <marker id="arrcicd" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 z" fill="var(--muted)"/>
    </marker>
  </defs>
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
    <text x="380" y="20" font-weight="700" font-size="13">Una pipeline CI/CD</text>

    <rect x="12" y="66" width="96" height="48" rx="8" fill="var(--card2)" stroke="var(--accent)" stroke-width="1.6"/>
    <text x="60" y="86" font-weight="700" font-size="11">push / PR</text><text x="60" y="102" font-size="9.5" fill="var(--muted)">trigger</text>

    <rect x="132" y="66" width="96" height="48" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="180" y="88" font-size="11">Build</text><text x="180" y="103" font-size="9" fill="var(--muted)">compila + cache</text>

    <rect x="252" y="66" width="96" height="48" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="300" y="88" font-size="11">Lint + Test</text><text x="300" y="103" font-size="9" fill="var(--muted)">unit/integr.</text>

    <rect x="372" y="66" width="104" height="48" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="424" y="88" font-size="11">Build immagine</text><text x="424" y="103" font-size="9" fill="var(--muted)">push al registry</text>

    <rect x="500" y="66" width="96" height="48" rx="8" fill="var(--card)" stroke="var(--rule)"/>
    <text x="548" y="88" font-size="11">Staging</text><text x="548" y="103" font-size="9" fill="var(--muted)">test e2e</text>

    <rect x="620" y="66" width="120" height="48" rx="8" fill="var(--card2)" stroke="var(--good)" stroke-width="1.7"/>
    <text x="680" y="86" font-weight="700" font-size="11">Produzione</text><text x="680" y="102" font-size="9" fill="var(--muted)">approva / auto</text>

    <text x="300" y="150" font-size="10" fill="var(--muted)">rosso qui = pipeline fallita, niente va avanti</text>
    <text x="548" y="150" font-size="10" fill="var(--muted)">build once,</text>
    <text x="548" y="164" font-size="10" fill="var(--muted)">deploy many</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arrcicd)">
    <path d="M108,90 L130,90"/><path d="M228,90 L250,90"/><path d="M348,90 L370,90"/>
    <path d="M476,90 L498,90"/><path d="M596,90 L618,90"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Dal push alla produzione: ogni stage deve passare perché il successivo parta. L'immagine costruita una volta è la stessa che attraversa staging e produzione (build once, deploy many).</figcaption>
</figure>

## Esempi concreti
- **Pull request protetta:** un collega apre una PR. GitHub Actions fa partire la pipeline: build, lint, test. Se anche un solo test fallisce, la PR mostra il check rosso e le regole del repository **impediscono il merge**. Il ramo principale resta verde per tutti.
- **Dal commit al rilascio automatico:** fai push su `main`. La pipeline costruisce l'immagine `app:abc123` (etichettata con l'hash del commit), la testa in staging, poi fa un rollout canary al 5% degli utenti. Le metriche reggono, l'estensione arriva al 100%. Nessun intervento manuale: è Continuous Deployment.
- **Build riproducibile:** un bug appare solo in produzione. Siccome l'artefatto è etichettato con l'hash del commit e costruito una volta sola, sai **esattamente** quale codice è in esecuzione e puoi fare rollback alla tag precedente con un comando.

## Notable use case
- **Amazon** ha reso celebre l'idea di deploy continui a frequenza altissima: migliaia di rilasci al giorno resi possibili da pipeline automatiche e deploy a basso rischio.
- Il programma di ricerca **DORA (DevOps Research and Assessment)** di Google ha codificato le quattro metriche con cui si misura un team: frequenza di deploy, lead time (tempo da commit a produzione), tasso di fallimento dei cambi, tempo di ripristino. CI/CD è la leva principale per migliorarle.
- **GitLab** pubblica il proprio manuale di pipeline e pratica il "dogfooding", usando la propria CI per rilasciare il proprio prodotto.

## Fonti
- **GitHub Actions docs** — docs.github.com/actions (workflow, job, step, runner)
- **GitLab CI/CD docs** — docs.gitlab.com/ee/ci (stage, pipeline, artifact)
- **Continuous Delivery** — Jez Humble, David Farley (il libro di riferimento)
- **DORA / State of DevOps** — dora.dev (le quattro metriche chiave)

## Concetti adiacenti
- `se-vcs` — Git, branch e pull request: ciò che fa scattare la pipeline
- `xc-do-containers` — l'immagine container è l'artefatto che la pipeline costruisce e rilascia
- `xc-swe-tdd` — la test pyramid che popola lo stage di test
- `sa-devops` — automazione e amministrazione, il ponte culturale verso il DevOps

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cosa significano le sigle CI, CD (Delivery) e CD (Deployment), e qual è la differenza pratica tra Delivery e Deployment?
2. Qual è l'obiettivo della Continuous Integration e quale problema evita ("integration hell")?
3. Definisci **trigger**, **job** e **step** di una pipeline.
4. Cos'è un **runner** e perché il fatto che parta "pulito" a ogni esecuzione è un vantaggio?
5. Elenca in ordine le fasi tipiche di una pipeline dal commit alla produzione.
6. Cosa afferma il principio **build once, deploy many** e perché è importante non ricostruire l'artefatto per la produzione?
7. Cos'è un test **flaky** e perché è dannoso per la fiducia nella CI?
8. Spiega la differenza tra deploy **blue-green** e deploy **canary**.
9. Cos'è un **feature flag** e cosa permette di scollegare?
10. Perché "tenere il ramo principale verde" è considerato l'obiettivo centrale della CI?

<details><summary>Risposte</summary>

1. **CI = Continuous Integration** (integra e testa spesso); **CD = Continuous Delivery** (prepara un artefatto sempre rilasciabile, il rilascio finale è manuale); **CD = Continuous Deployment** (se i test passano, va in produzione da solo). La Delivery lascia a te il bottone "vai", il Deployment lo preme automaticamente.
2. Scoprire **subito** se una modifica rompe qualcosa, quando è piccola; evita l'"integration hell", cioè l'accumulo di tanto lavoro non integrato che poi diventa difficilissimo da fondere.
3. **Trigger:** l'evento che avvia la pipeline (push, PR). **Job:** un insieme di step sulla stessa macchina (job diversi possono girare in parallelo). **Step:** la singola azione dentro un job.
4. Il **runner** è la macchina (spesso un container effimero) che esegue la pipeline. Partendo pulita a ogni esecuzione garantisce che la build non dipenda dallo stato residuo di un PC: il risultato è riproducibile.
5. Checkout/build → lint e analisi statica → test automatici → build dell'artefatto (immagine) → deploy in staging → deploy in produzione (manuale o automatico).
6. Afferma di costruire l'artefatto **una sola volta** e di promuovere **quello stesso** attraverso tutti gli ambienti. Ricostruire per la produzione rischia di introdurre differenze: ciò che va live non sarebbe più esattamente ciò che è stato testato.
7. Un test **flaky** a volte passa e a volte fallisce senza che il codice cambi. È dannoso perché genera falsi allarmi: dopo un po' la gente ignora anche i fallimenti veri.
8. **Blue-green:** due ambienti identici, si sposta **tutto** il traffico dal vecchio (blue) al nuovo (green) in un colpo, con ritorno immediato in caso di problemi. **Canary:** si manda la nuova versione a una **piccola fetta** di utenti e si estende gradualmente solo se le metriche reggono.
9. Un **feature flag** è un interruttore che tiene il codice spento finché non lo si accende; permette di **scollegare il deploy dal rilascio** della funzionalità (il codice è in produzione ma inattivo).
10. Perché se il ramo principale ha sempre tutti i test verdi, chiunque può partire da lì sapendo di basarsi su codice sano; è la garanzia che rende la CI utile.
</details>

## Esercizi
1. **Scrivi uno step di pipeline CI.** In un workflow GitHub Actions, scrivi un job che, a ogni push, faccia checkout del codice, installi le dipendenze Node e lanci i test. (Pseudo-YAML accettato, ma coerente.)
2. **Progetta gli stage.** Per un'app containerizzata, elenca gli stage della pipeline dal push alla produzione e di' quale artefatto passa da uno stage all'altro.
3. **Scegli la strategia di rilascio.** Devi rilasciare una modifica rischiosa al sistema di pagamento, con molti utenti. Quale strategia tra blue-green, canary e feature flag scegli e perché? Come fai rollback?

<details><summary>Soluzioni</summary>

1. 
   ```yaml
   name: CI
   on: [push]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with: {node-version: '20', cache: 'npm'}
         - run: npm ci
         - run: npm test
   ```
   `on: [push]` è il trigger; il job `test` gira su un runner pulito; gli step fanno checkout, preparano Node (con cache delle dipendenze per velocità) e lanciano `npm test`. Se `npm test` esce con errore, il job fallisce e il check risulta rosso.

2. Stage: **checkout+build** → **lint+test** (unit/integrazione) → **build immagine** (push nel registry con tag = hash del commit) → **deploy staging** (test e2e) → **deploy produzione**. L'artefatto che passa da uno stage all'altro è l'**immagine container**, costruita una volta sola (build once, deploy many) e promossa identica fino alla produzione.

3. Per una modifica rischiosa e molti utenti conviene il **canary** (eventualmente combinato con un **feature flag**): si espone la nuova versione a una piccola percentuale, si osservano le metriche (errori, latenza, tassi di pagamento) e si estende solo se reggono. Il feature flag aggiunge la possibilità di **spegnere** la funzionalità all'istante senza un nuovo deploy. Il **rollback**: con il canary si riporta il traffico al 100% sulla versione precedente (o si rilascia di nuovo l'immagine con il tag vecchio); con il flag basta disattivare l'interruttore. Il blue-green sarebbe un'alternativa valida ma espone tutti gli utenti in un colpo, meno prudente per un cambio ad alto rischio.
</details>
