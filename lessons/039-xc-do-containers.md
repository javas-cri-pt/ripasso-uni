---
day: 39
topic_id: xc-do-containers
title: "Container e orchestrazione: Docker e Kubernetes"
area: cross-cutting
course: "DevOps & Cloud-native"
grounded_in: null
adjacent: [cloud-virt, xc-do-cicd, xc-do-iac]
completeness_checked: true
quiz_count: 10
---

# Container e orchestrazione: Docker e Kubernetes

> **Perché oggi:** in `cloud-virt` hai visto la virtualizzazione e la nascita dei container; qui scendi al livello operativo, quello che ti chiedono davvero in un colloquio di taglio SWE o DevOps. "Come impacchetti la tua applicazione perché giri uguale sul tuo portatile e in produzione?" La risposta moderna è: la metti in un **container**. E quando i container diventano decine e devono restare in piedi da soli, serve un **orchestratore**: Kubernetes. Oggi vediamo come funzionano entrambi, con i comandi e i file reali che scriveresti.

## Cos'è un container e perché risolve "sul mio PC funziona"
Un **container** è un processo isolato che porta con sé tutto ciò che gli serve per girare: il codice, le librerie, le dipendenze di sistema, le variabili d'ambiente. Non è una macchina virtuale. La differenza è netta e vale la pena fissarla:

- Una **macchina virtuale (VM)** virtualizza l'hardware: sopra l'hardware fisico gira un **hypervisor** (il software che crea e gestisce le VM, es. VMware, KVM), e ogni VM ha dentro un **sistema operativo guest completo**, con il suo kernel. Pesa gigabyte e impiega minuti ad avviarsi.
- Un **container** virtualizza il sistema operativo: tutti i container di una macchina **condividono lo stesso kernel** dell'host e vengono isolati tra loro da due meccanismi del kernel Linux: i **namespace** (danno a ogni container la sua vista privata di processi, rete, filesystem, utenti, così un container non "vede" gli altri) e i **cgroups** (control groups, limitano quanta CPU e memoria un container può consumare). Pesa megabyte e si avvia in millisecondi.

Il container risolve il classico "sul mio PC funziona": siccome l'ambiente è impacchettato insieme al codice, se gira sul tuo portatile gira identico in produzione. Questo è esattamente ciò che serve a valle di una pipeline di `xc-do-cicd`: costruisci l'artefatto una volta e lo esegui ovunque.

## Immagine, container, registry: i tre concetti base di Docker
**Docker** è lo strumento che ha reso i container di massa. Tre termini da non confondere mai:

- **Immagine (image):** il pacchetto **immutabile e di sola lettura** che contiene filesystem e metadati dell'applicazione. È la "ricetta cotta", il template. Le immagini sono fatte a **layer** (strati): ogni istruzione di costruzione aggiunge uno strato sovrapposto ai precedenti, e gli strati sono condivisi e messi in cache tra immagini diverse (per questo ricostruire è veloce).
- **Container:** un'**istanza in esecuzione** di un'immagine. Dall'immagine (read-only) Docker aggiunge sopra un sottile strato scrivibile e avvia il processo. Dalla stessa immagine puoi far partire 1 o 100 container identici.
- **Registry:** il magazzino remoto dove le immagini vengono pubblicate e scaricate (**push** e **pull**). Il più noto è **Docker Hub**; ne esistono di privati (GitHub Container Registry, quelli dei cloud provider).

Analogia: l'immagine sta al container come la **classe** sta all'**oggetto** nella programmazione (vedi `prog-oop`): una definizione, tante istanze.

## Il Dockerfile: come si costruisce un'immagine
Il **Dockerfile** è un file di testo con le istruzioni per costruire l'immagine, passo dopo passo. Ogni istruzione genera un layer. Le principali:

- `FROM`: l'immagine di partenza (la base, es. `python:3.12-slim`). Ogni Dockerfile parte da qui.
- `WORKDIR`: la cartella di lavoro dentro il container.
- `COPY`: copia file dal tuo progetto dentro l'immagine.
- `RUN`: esegue un comando **in fase di costruzione** (es. installare le dipendenze).
- `EXPOSE`: documenta su che porta l'app ascolta.
- `CMD` (o `ENTRYPOINT`): il comando eseguito **all'avvio** del container.

Esempio minimo per una piccola API Python:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Nota l'ordine: si copiano prima `requirements.txt` e si installano le dipendenze, **poi** si copia il resto del codice. Il motivo è la **cache dei layer**: se cambi solo il codice ma non le dipendenze, Docker riusa il layer (già in cache) del `pip install` e la build resta velocissima. Invertire l'ordine butterebbe via la cache a ogni modifica del codice.

I comandi di tutti i giorni:

```bash
docker build -t miaapp:1.0 .      # costruisce l'immagine dal Dockerfile
docker run -p 8000:8000 miaapp:1.0 # avvia un container, mappa la porta host->container
docker ps                          # elenca i container in esecuzione
docker push registry/miaapp:1.0    # pubblica l'immagine nel registry
```

Un accorgimento di qualità: il **multi-stage build**. Usi un primo stadio "pesante" con tutti gli strumenti per compilare, e un secondo stadio "leggero" dove copi solo l'artefatto finale. L'immagine prodotta resta piccola perché gli strumenti di compilazione non finiscono dentro.

## Perché un solo container non basta: nasce l'orchestrazione
In produzione un container da solo pone problemi che nessuno vuole risolvere a mano:
- se il processo va in crash, chi lo **riavvia**?
- se arriva più traffico, chi fa partire **altre copie** (scaling) e chi le bilancia?
- se aggiorni la versione, come fai **senza downtime**?
- come fanno i container a **trovarsi** tra loro sulla rete, visto che nascono e muoiono di continuo?

Queste domande sono il motivo per cui esiste l'**orchestrazione**: un software che gestisce automaticamente il ciclo di vita di molti container su molte macchine. Lo standard di fatto è **Kubernetes** (spesso abbreviato **k8s**: "k", poi 8 lettere, poi "s").

## Kubernetes: il modello dichiarativo e i suoi oggetti
L'idea centrale di Kubernetes è il **modello dichiarativo**: tu non dici "avvia questo container, poi quest'altro" (imperativo); tu dichiari lo **stato desiderato** ("voglio 3 copie di questa app sempre attive") in un file, e Kubernetes lavora in continuazione per far coincidere lo **stato reale** con quello desiderato. Questo ciclo continuo si chiama **reconciliation loop** (anello di riconciliazione): se una copia muore, il sistema se ne accorge e ne crea un'altra, da solo, per tornare a 3.

Un **cluster** Kubernetes ha due parti:
- il **control plane** (il "cervello"): decide e coordina. Contiene l'**API server** (il punto d'ingresso con cui parli), lo **scheduler** (decide su quale macchina mettere ogni container) e **etcd** (il database che conserva lo stato del cluster).
- i **worker node** (i "muscoli"): le macchine dove girano davvero i container. Su ciascuna c'è un agente, il **kubelet**, che esegue gli ordini del control plane.

Gli oggetti che devi conoscere:

- **Pod:** l'unità base di Kubernetes. Un **pod** è un involucro per **uno o più container** che condividono rete e storage e vengono sempre schedulati insieme. Di solito un pod = un container (più eventuali container "sidecar" di supporto). I pod sono **effimeri**: nascono e muoiono, e il loro indirizzo IP cambia.
- **Deployment:** l'oggetto che gestisce un insieme di pod identici. Un **deployment** dichiara "voglio N **repliche** di questo pod" e si occupa di crearle, sostituire quelle morte e fare gli aggiornamenti. È qui che vive la riconciliazione.
- **Service:** siccome i pod cambiano IP, serve un indirizzo stabile. Un **service** è un nome e un IP virtuale fissi davanti a un gruppo di pod, con bilanciamento del carico tra di essi. Chi deve raggiungere l'app parla col service, non coi pod.
- **ReplicaSet:** il meccanismo (gestito dal deployment) che tiene attivo il numero giusto di repliche.

Un deployment minimo in YAML:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: miaapp
spec:
  replicas: 3                 # stato desiderato: 3 copie
  selector:
    matchLabels: {app: miaapp}
  template:
    metadata:
      labels: {app: miaapp}
    spec:
      containers:
        - name: miaapp
          image: registry/miaapp:1.0
          ports:
            - containerPort: 8000
```

Lo applichi con `kubectl apply -f deployment.yaml` (`kubectl` è lo strumento a riga di comando per parlare col cluster). Da quel momento, se un pod muore, torni comunque a 3.

## Aggiornamenti senza downtime e auto-guarigione
Due proprietà che rendono Kubernetes prezioso:
- **Rolling update:** quando cambi l'immagine (es. da `1.0` a `1.1`), il deployment sostituisce i pod **a scaglioni**: ne crea uno nuovo, aspetta che sia sano, spegne uno vecchio, e così via. Il servizio non si interrompe mai. Se qualcosa va storto puoi fare **rollback** alla versione precedente.
- **Self-healing e health check:** Kubernetes controlla la salute dei pod con due sonde. La **liveness probe** chiede "sei vivo?"; se la risposta non arriva, riavvia il container. La **readiness probe** chiede "sei pronto a ricevere traffico?"; finché la risposta è no, il service non manda richieste a quel pod. Insieme evitano di instradare utenti verso un'istanza rotta o non ancora avviata.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 720 300" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="360" y="20" font-weight="700" font-size="13">Un cluster Kubernetes</text>

    <rect x="20" y="40" width="200" height="220" rx="10" fill="var(--card2)" stroke="var(--accent)" stroke-width="1.7"/>
    <text x="120" y="60" font-weight="700" fill="var(--accent)">Control plane</text>
    <rect x="38" y="74" width="164" height="30" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="120" y="93" font-size="11">API server</text>
    <rect x="38" y="112" width="164" height="30" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="120" y="131" font-size="11">Scheduler</text>
    <rect x="38" y="150" width="164" height="30" rx="6" fill="var(--card)" stroke="var(--rule)"/><text x="120" y="169" font-size="11">etcd (stato)</text>
    <text x="120" y="208" font-size="10" fill="var(--muted)">decide e riconcilia:</text>
    <text x="120" y="224" font-size="10" fill="var(--muted)">stato reale = desiderato</text>

    <rect x="270" y="40" width="200" height="220" rx="10" fill="var(--card2)" stroke="var(--rule)"/>
    <text x="370" y="60" font-weight="700">Worker node A</text>
    <text x="370" y="76" font-size="10" fill="var(--muted)">kubelet</text>
    <rect x="288" y="86" width="164" height="36" rx="6" fill="var(--card)" stroke="var(--good)" stroke-width="1.6"/><text x="370" y="108" font-size="11">Pod (container)</text>
    <rect x="288" y="128" width="164" height="36" rx="6" fill="var(--card)" stroke="var(--good)" stroke-width="1.6"/><text x="370" y="150" font-size="11">Pod (container)</text>

    <rect x="500" y="40" width="200" height="220" rx="10" fill="var(--card2)" stroke="var(--rule)"/>
    <text x="600" y="60" font-weight="700">Worker node B</text>
    <text x="600" y="76" font-size="10" fill="var(--muted)">kubelet</text>
    <rect x="518" y="86" width="164" height="36" rx="6" fill="var(--card)" stroke="var(--good)" stroke-width="1.6"/><text x="600" y="108" font-size="11">Pod (container)</text>

    <rect x="288" y="200" width="412" height="44" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/>
    <text x="494" y="220" font-size="11" font-weight="700">Service</text>
    <text x="494" y="236" font-size="10" fill="var(--muted)">IP stabile + bilanciamento sui 3 pod</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.3" fill="none">
    <path d="M220,120 L270,120"/><path d="M220,150 L500,150"/>
    <path d="M370,164 L370,200"/><path d="M600,122 L600,160 L600,200"/>
    <path d="M370,122 L370,164" stroke-dasharray="3 3"/>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Il control plane (a sinistra) decide dove mettere i pod e li riporta sempre al numero desiderato; i worker node li eseguono; il service davanti fornisce un indirizzo stabile e bilancia il traffico sui pod, che restano effimeri.</figcaption>
</figure>

## Esempi concreti
- **Scalare per un picco di traffico:** la tua API gira in un deployment con `replicas: 3`. Arriva una promozione e il carico triplica. Con un comando (`kubectl scale deployment miaapp --replicas=9`) o, meglio, con l'**HPA (Horizontal Pod Autoscaler)** che osserva la CPU e aumenta le repliche da solo, passi a 9 pod; il service distribuisce le richieste su tutti. Finito il picco, si torna a 3.
- **Rilascio di una nuova versione:** hai costruito `miaapp:1.1` nella pipeline, l'hai messa nel registry. Cambi l'immagine nel deployment e `kubectl apply`. Kubernetes fa il rolling update: gli utenti non notano nulla. Un bug grave in `1.1`? `kubectl rollout undo` e sei tornato a `1.0`.
- **Dev locale con più servizi:** sul tuo portatile per far girare insieme API + database usi **Docker Compose**, un file `docker-compose.yml` che descrive più container e li avvia con un solo comando (`docker compose up`). È l'equivalente leggero dell'orchestrazione, per lo sviluppo.

## Notable use case
- **Google** ha eseguito "tutto in container" per anni con il sistema interno **Borg**; da quell'esperienza è nato Kubernetes, donato poi alla community e oggi gestito dalla **CNCF (Cloud Native Computing Foundation)**.
- **Spotify** ha migrato la sua infrastruttura a Kubernetes per unificare come i team distribuiscono i servizi e ridurre i tempi di avvio di nuove istanze.
- Praticamente tutti i grandi cloud offrono Kubernetes "gestito" (il control plane lo mantengono loro): GKE (Google), EKS (Amazon), AKS (Azure). Tu porti solo i tuoi container.

## Fonti
- **Docker docs** — docs.docker.com (guida a Dockerfile, build, Compose)
- **Kubernetes docs** — kubernetes.io/docs/concepts (Pod, Deployment, Service, probe)
- **The Twelve-Factor App** — 12factor.net (principi per app pronte al container)
- **CNCF** — cncf.io (ecosistema cloud-native)

## Concetti adiacenti
- `cloud-virt` — virtualizzazione e container: la teoria sotto la pratica di oggi
- `xc-do-cicd` — la pipeline costruisce l'immagine che qui mandi in esecuzione
- `xc-do-iac` — descrivere l'infrastruttura (anche i cluster) come codice versionato

## Quiz (10 — tutte rispondibili dalla lezione)
1. Qual è la differenza fondamentale tra una macchina virtuale e un container riguardo al kernel del sistema operativo?
2. Quali due meccanismi del kernel Linux isolano i container e cosa fa ciascuno (namespace e cgroups)?
3. Distingui **immagine**, **container** e **registry**: cosa sono e che relazione hanno?
4. In un Dockerfile, perché conviene copiare `requirements.txt` e installare le dipendenze **prima** di copiare il resto del codice?
5. Cosa significa che Kubernetes è **dichiarativo** e cos'è il **reconciliation loop**?
6. Cos'è un **pod** e perché si dice che è effimero?
7. A cosa serve un **deployment** e cosa garantisce il campo `replicas`?
8. Perché serve un **service** se i pod hanno già un indirizzo IP?
9. Cos'è un **rolling update** e come evita il downtime durante un aggiornamento?
10. Spiega la differenza tra **liveness probe** e **readiness probe**.

<details><summary>Risposte</summary>

1. La VM virtualizza l'hardware e include un **sistema operativo guest completo con il suo kernel** (pesa GB, avvio in minuti); il container virtualizza il SO e **condivide il kernel dell'host** (pesa MB, avvio in millisecondi).
2. I **namespace** danno a ogni container una vista privata di processi, rete, filesystem e utenti (lo isolano da ciò che vedono gli altri); i **cgroups** limitano le risorse (CPU, memoria) che il container può consumare.
3. L'**immagine** è il pacchetto immutabile read-only (il template, fatto a layer); il **container** è un'istanza in esecuzione di un'immagine (classe:oggetto); il **registry** è il magazzino remoto dove le immagini si pubblicano (push) e si scaricano (pull), es. Docker Hub.
4. Per sfruttare la **cache dei layer**: se cambi solo il codice ma non le dipendenze, Docker riusa il layer già costruito del `pip install` e la build resta veloce; invertendo l'ordine la cache verrebbe invalidata a ogni modifica del codice.
5. Dichiarativo significa che descrivi lo **stato desiderato** (es. "3 repliche"), non i passi da eseguire; il **reconciliation loop** è il ciclo continuo con cui Kubernetes confronta stato reale e desiderato e agisce per farli coincidere (se un pod muore, ne ricrea uno).
6. Un **pod** è l'unità base: un involucro per uno o più container che condividono rete e storage e vengono schedulati insieme. È **effimero** perché nasce e muore di continuo e il suo IP cambia.
7. Un **deployment** gestisce un insieme di pod identici: li crea, sostituisce quelli morti e gestisce gli aggiornamenti; `replicas` dichiara quante copie devono essere **sempre** attive.
8. Perché i pod sono effimeri e cambiano IP: il **service** fornisce un nome e un IP virtuale **stabili** davanti al gruppo di pod, con bilanciamento del carico tra di essi.
9. È la sostituzione dei pod **a scaglioni** quando cambia l'immagine: crea un pod nuovo, attende che sia sano, spegne uno vecchio, e così via, così il servizio resta sempre disponibile; in caso di problemi si fa rollback.
10. La **liveness probe** verifica se il container è vivo e, in caso contrario, lo **riavvia**; la **readiness probe** verifica se è pronto a ricevere traffico e, finché non lo è, il service **non gli invia** richieste.
</details>

## Esercizi
1. **Scrivi un Dockerfile.** Hai una piccola app Node che si avvia con `node server.js`, ascolta sulla porta `3000` e ha le dipendenze in `package.json`. Scrivi un Dockerfile che sfrutti bene la cache dei layer.
2. **Scrivi un deployment Kubernetes.** Dichiara 2 repliche dell'immagine `registry/webapp:2.0` che ascolta sulla porta `3000`, con una readiness probe HTTP sul path `/health`.
3. **Ragiona sullo scaling.** Il traffico raddoppia di colpo. Elenca due modi per passare da 2 a 4 repliche e spiega chi distribuisce poi le richieste.

<details><summary>Soluzioni</summary>

1. Si copia prima il manifest delle dipendenze, si installa, poi si copia il codice (cache-friendly):
   ```dockerfile
   FROM node:20-slim
   WORKDIR /app
   COPY package.json package-lock.json ./
   RUN npm ci --omit=dev
   COPY . .
   EXPOSE 3000
   CMD ["node", "server.js"]
   ```
   `npm ci` installa in modo riproducibile dal lock file; essendo in un layer separato, resta in cache finché non cambiano le dipendenze.

2. 
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: webapp
   spec:
     replicas: 2
     selector:
       matchLabels: {app: webapp}
     template:
       metadata:
         labels: {app: webapp}
       spec:
         containers:
           - name: webapp
             image: registry/webapp:2.0
             ports:
               - containerPort: 3000
             readinessProbe:
               httpGet: {path: /health, port: 3000}
               initialDelaySeconds: 5
               periodSeconds: 10
   ```
   La readiness probe interroga `GET /health`: finché non risponde OK, il service non manda traffico al pod.

3. Due modi: (a) **manuale/imperativo** `kubectl scale deployment webapp --replicas=4`; (b) **dichiarativo** modificare `replicas: 4` nel file YAML e `kubectl apply -f`. In più, con un **HPA** lo scaling può avvenire da solo in base alla CPU. In tutti i casi è il **service** davanti ai pod a distribuire (bilanciare) le richieste sulle 4 repliche.
</details>
