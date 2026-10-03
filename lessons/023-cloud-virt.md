---
day: 23
topic_id: cloud-virt
title: "Virtualizzazione e container — VM, Docker, immagini, Kubernetes"
area: management
course: Cloud Computing Technologies
grounded_in: "POLITO/secondo anno/Cloud Computing Technologies + lavoro (Docker/K8s/Terraform)"
adjacent: [cloud-models, xc-do-containers, xc-do-cicd, os-processes]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo."
---

# Virtualizzazione e container — VM, Docker, immagini, Kubernetes

> **Perché oggi:** "gira sul mio computer ma non in produzione" è il problema che i container risolvono, ed è ovunque nel lavoro reale. L'hai già toccato (Docker, Kubernetes e Terraform in ALTEN; KVM/Docker/K8s nel corso di Cloud). Capire **VM vs container** e cos'è un'**immagine** è chiesto a quasi ogni colloquio con una parte infrastrutturale.

## Il problema che risolve la virtualizzazione
Un server fisico è potente ma **uno**: ci giri sopra più applicazioni e si pestano i piedi (versioni di librerie diverse, una crasha e porta giù le altre). La **virtualizzazione** spezza una macchina fisica in **tante unità isolate**, così ognuna crede di avere il suo ambiente. Due livelli di isolamento, con costi diversi: **macchine virtuali** e **container**.

## Macchine virtuali (VM)
Una **VM (Virtual Machine)** emula un **computer intero**: ha un suo **sistema operativo completo** (kernel incluso). A orchestrarle c'è l'**hypervisor** (es. KVM, VMware, VirtualBox): un software che divide CPU/RAM/disco reali tra le VM e le tiene isolate. Ogni VM è come un PC dentro il PC.

- **Pro:** isolamento **forte** (kernel separati), puoi far girare OS diversi (Windows dentro Linux).
- **Contro:** **pesante** — ogni VM porta con sé un OS intero (giga di disco, RAM dedicata, avvio in **minuti**).

## Container
Un **container** impacchetta **l'applicazione e le sue dipendenze** (librerie, file, configurazione) ma **condivide il kernel** del sistema operativo ospite. Non emula un computer: isola un **processo** usando funzioni del kernel Linux (**namespace** = ogni container vede solo i suoi processi/rete/filesystem; **cgroup** = limiti su CPU/RAM). Risultato: leggero e velocissimo.

- **Pro:** **leggero** (megabyte, non giga), avvio in **millisecondi/secondi**, tanti container sulla stessa macchina; "impacchetti una volta, gira uguale ovunque".
- **Contro:** isolamento **più debole** della VM (kernel condiviso), e i container **Linux** girano su kernel Linux (su Mac/Windows Docker usa una piccola VM Linux sotto).

<svg viewBox="0 0 620 250" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="11.5" fill="var(--ink)" text-anchor="middle">
    <text x="160" y="20" font-weight="700">Macchine virtuali</text>
    <rect x="40" y="30" width="240" height="30" fill="var(--card2)" stroke="var(--rule)"/><text x="160" y="50">Hardware fisico</text>
    <rect x="40" y="62" width="240" height="26" fill="var(--card2)" stroke="var(--rule)"/><text x="160" y="80">Hypervisor</text>
    <g>
      <rect x="46" y="94" width="112" height="120" rx="6" fill="var(--card)" stroke="var(--rule)"/>
      <rect x="162" y="94" width="112" height="120" rx="6" fill="var(--card)" stroke="var(--rule)"/>
      <text x="102" y="112">App A</text><text x="218" y="112">App B</text>
      <text x="102" y="132" font-size="10.5" fill="var(--muted)">librerie</text><text x="218" y="132" font-size="10.5" fill="var(--muted)">librerie</text>
      <rect x="52" y="150" width="100" height="56" rx="5" fill="var(--card2)" stroke="var(--accent2)"/><text x="102" y="174" font-size="11">OS ospite</text><text x="102" y="190" font-size="10" fill="var(--muted)">kernel incluso</text>
      <rect x="168" y="150" width="100" height="56" rx="5" fill="var(--card2)" stroke="var(--accent2)"/><text x="218" y="174" font-size="11">OS ospite</text><text x="218" y="190" font-size="10" fill="var(--muted)">kernel incluso</text>
    </g>

    <text x="460" y="20" font-weight="700">Container</text>
    <rect x="340" y="30" width="240" height="30" fill="var(--card2)" stroke="var(--rule)"/><text x="460" y="50">Hardware fisico</text>
    <rect x="340" y="62" width="240" height="26" fill="var(--card2)" stroke="var(--accent)" stroke-width="1.6"/><text x="460" y="80">OS ospite unico (kernel condiviso)</text>
    <rect x="340" y="90" width="240" height="24" fill="var(--card2)" stroke="var(--rule)"/><text x="460" y="106">Container runtime (Docker)</text>
    <g>
      <rect x="346" y="120" width="72" height="90" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="382" y="150">App A</text><text x="382" y="168" font-size="10" fill="var(--muted)">+ librerie</text>
      <rect x="424" y="120" width="72" height="90" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="460" y="150">App B</text><text x="460" y="168" font-size="10" fill="var(--muted)">+ librerie</text>
      <rect x="502" y="120" width="72" height="90" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="538" y="150">App C</text><text x="538" y="168" font-size="10" fill="var(--muted)">+ librerie</text>
    </g>
  </g>
</svg>

**In una frase:** la VM virtualizza l'**hardware** (OS completo per ognuna); il container virtualizza il **sistema operativo** (un kernel condiviso, un processo isolato per ognuno). Per questo i container sono molto più leggeri.

## Docker: immagini e container
**Docker** è lo strumento che ha reso i container mainstream. Due concetti da non confondere:
- **Immagine (image):** un **pacchetto immutabile** e versionato che contiene app + dipendenze + istruzioni di avvio. È la "ricetta congelata". La costruisci da un **Dockerfile** (un file di testo con i passi: parti da `python:3.12`, copia il codice, installa le librerie, comando di avvio). Le immagini stanno in un **registry** (es. Docker Hub) da cui si scaricano.
- **Container:** un'**istanza in esecuzione** di un'immagine. Dall'immagine (classe) accendi tanti container (oggetti). Sono **effimeri**: se muoiono, quello che avevano scritto dentro sparisce, a meno di montare un **volume** (spazio disco persistente esterno al container). Regola: lo **stato** (DB, file utente) va fuori dal container.

Perché piace: l'immagine **incapsula l'ambiente**, quindi "gira uguale" dal tuo laptop alla produzione — la fine di "sul mio computer funziona".

## Orchestrazione: Kubernetes
Con **pochi** container basta Docker. Con **tanti**, su **tante** macchine, serve un **orchestratore**. **Kubernetes (K8s)** automatizza: **deployment** (quali container e quante copie), **scaling** (aggiungi/togli copie col carico), **self-healing** (se un container muore lo **riavvia** altrove), **networking e load balancing** tra le copie. Tu dichiari lo **stato desiderato** ("voglio 3 repliche di questo servizio") e K8s lavora per farlo combaciare in continuazione (modello **dichiarativo**, come Terraform per l'infrastruttura). Unità base: il **pod** (uno o più container che vivono insieme).

## Esempio concreto (roba tua)
In **ALTEN** hai lavorato con **Docker, Kubernetes e Terraform**: containerizzare un servizio, orchestrarlo, e descrivere l'infrastruttura come codice. Nel corso di **Cloud Computing** hai visto lo stack completo (KVM come hypervisor, Docker per i container, K8s per orchestrarli, Ansible per la configurazione): è la stessa piramide di questa lezione, dall'hardware fino all'app.

## Completeness check (integrato da me)
- **Il legame con IaaS/PaaS/SaaS (cloud-models):** le VM sono il mattone tipico di **IaaS** (affitti macchine); i container gestiti e le piattaforme che "prendono la tua immagine e la fanno girare" sono **PaaS**. Cloudflare Workers (che usi per Job Pipeline) è un modello ancora più leggero (isolate serverless), cugino distante del container.
- **Immutabilità:** immagini e infrastruttura **immutabili** (non modifichi un container vivo: ne costruisci una nuova versione e sostituisci) sono ciò che rende deploy e rollback affidabili — lo stesso principio di "design for rollback" del tuo lavoro.
- **Container ≠ sicurezza forte:** kernel condiviso = superficie d'attacco; per isolamento forte servono comunque VM o sandbox dedicate.

## Fonti
- **Docker — Get Started** (docs.docker.com/get-started)
- **Kubernetes — Concepts** (kubernetes.io/docs/concepts)
- **"The Illustrated Children's Guide to Kubernetes"** (video, deploy.equinix.com) — la metafora base

## Concetti adiacenti
- `cloud-models` — IaaS/PaaS/SaaS: dove si collocano VM e container
- `xc-do-cicd` — CI/CD: costruire e spedire immagini in automatico
- `os-processes` — namespace/cgroup poggiano sui processi del kernel (giorno 13)

## Quiz (10 — tutte rispondibili dalla lezione)
1. Qual è la differenza fondamentale tra una **VM** e un **container** (cosa virtualizza ciascuno)?
2. Cos'è un **hypervisor**?
3. Perché i container sono molto più **leggeri** e veloci ad avviarsi delle VM?
4. Quali funzioni del kernel danno l'isolamento a un container (nomi e ruolo)?
5. Differenza tra **immagine** e **container** in Docker?
6. Cos'è un **Dockerfile** e a cosa serve un **registry**?
7. Perché lo **stato** (dati) va tenuto fuori dal container, e con quale meccanismo?
8. Cosa fa **Kubernetes** che Docker da solo non fa (cita almeno tre cose)?
9. Cosa significa che K8s (e Terraform) sono **dichiarativi**?
10. Perché "gira sul mio computer ma non in produzione" sparisce con i container?

<details><summary>Risposte</summary>

1. La **VM** virtualizza l'**hardware** (OS completo, kernel incluso, per ognuna); il **container** virtualizza il **sistema operativo** (kernel **condiviso**, isola un processo).
2. Il software che divide CPU/RAM/disco reali tra più **VM** e le tiene isolate (es. KVM, VMware).
3. Perché **condividono il kernel** dell'host e non portano un OS intero: megabyte invece di giga, avvio in secondi invece di minuti.
4. **Namespace** (ogni container vede solo i suoi processi/rete/filesystem) e **cgroup** (limiti su CPU/RAM).
5. L'**immagine** è il pacchetto immutabile e versionato (la ricetta); il **container** è un'**istanza in esecuzione** di quell'immagine.
6. Il **Dockerfile** è il file di testo con i passi per costruire l'immagine; il **registry** è dove le immagini si pubblicano e scaricano (es. Docker Hub).
7. Perché i container sono **effimeri**: se muoiono perdono ciò che hanno scritto dentro; lo stato si mette in un **volume** (disco persistente esterno).
8. **Deployment** di molte copie, **scaling** automatico col carico, **self-healing** (riavvio dei container morti), networking/load balancing tra le repliche.
9. Dichiari lo **stato desiderato** (es. "3 repliche") e il sistema lavora per farlo combaciare, invece di eseguire comandi passo-passo.
10. Perché l'**immagine incapsula l'ambiente** (app + dipendenze + config): lo stesso pacchetto gira identico dal laptop alla produzione.
</details>
