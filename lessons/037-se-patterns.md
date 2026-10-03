---
day: 37
topic_id: se-patterns
title: "Design pattern GoF: creazionali, strutturali, comportamentali"
area: computer-science
course: "Ingegneria del Software"
grounded_in: null
adjacent: [prog-oop, xc-pat-review, se-principles, xc-swe-clean]
completeness_checked: true
quiz_count: 10
---

# Design pattern GoF: creazionali, strutturali, comportamentali

> **Perché oggi:** quando risolvi lo stesso problema di progettazione per la decima volta, scopri che esiste già un nome e una soluzione collaudata. I **design pattern** sono quel vocabolario condiviso: dire "qui userei una Factory" o "questo è un Observer" fa capire al volo un'intera struttura a chi ascolta. Nei colloqui tornano spessissimo ("conosci qualche design pattern? me ne spieghi uno?") e nelle code review sono il modo rapido di proporre una soluzione. Nei temi `xc-swe-clean` abbiamo visto i principi (SOLID); i pattern sono quei principi **confezionati** in soluzioni ricorrenti. Qui li organizziamo nelle tre famiglie e ne vediamo i più usati, con attenzione alle coppie che si confondono.

## Cosa sono (e cosa non sono) i design pattern
Un **design pattern** è una soluzione **generale e riutilizzabile** a un problema di progettazione che ricorre spesso. Non è codice da copiare, è uno **schema**: una descrizione di come far collaborare alcune classi/oggetti per risolvere quel problema. Il libro di riferimento è *Design Patterns* (1994) della **"Gang of Four" (GoF)**, i quattro autori Gamma, Helm, Johnson e Vlissides, che cataloga **23 pattern** divisi in tre famiglie:

- **Creazionali (5):** come si **creano** gli oggetti, nascondendo i dettagli di costruzione.
- **Strutturali (7):** come si **compongono** classi e oggetti in strutture più grandi.
- **Comportamentali (11):** come gli oggetti **collaborano** e si distribuiscono le responsabilità a runtime.

Il libro si regge su due principi guida che tornano in quasi tutti i pattern:

- **"Programma verso un'interfaccia, non verso un'implementazione".** Dipendi dal *cosa* (il contratto astratto), non dal *come* (la classe concreta): così puoi scambiare l'implementazione senza toccare chi la usa. È lo stesso spirito del Dependency Inversion visto in `xc-swe-clean`.
- **"Preferisci la composizione all'ereditarietà".** Comporre oggetti (un oggetto ne contiene un altro e gli delega del lavoro) è più flessibile che ereditare, perché il comportamento si può cambiare a runtime e non si eredita una gerarchia rigida.

## Famiglia 1 — Creazionali
Isolano il "come nasce" un oggetto.

- **Singleton:** garantisce che di una classe esista **una sola istanza** e offre un punto di accesso globale ad essa (es. un gestore di configurazione o un pool di connessioni). Attenzione: è il più criticato, perché introduce uno **stato globale** che rende i test difficili e nasconde le dipendenze.
- **Factory Method:** definisce un **metodo** per creare un oggetto, ma lascia alle sottoclassi decidere **quale** classe concreta istanziare. Il codice chiama `crea()` e riceve il prodotto giusto senza conoscere il costruttore concreto.
- **Abstract Factory:** fornisce un'interfaccia per creare **famiglie di oggetti correlati** (es. tutti i widget "tema scuro": bottone scuro, menu scuro, casella scura) senza specificarne le classi concrete. Differenza chiave dal Factory Method: il Factory Method crea **un** prodotto, l'Abstract Factory crea **un insieme coerente** di prodotti.
- **Builder:** costruisce un oggetto complesso **passo per passo**, separando la costruzione dalla rappresentazione finale. Utile quando ci sono molti parametri opzionali: invece di un costruttore con quindici argomenti, incateni `.con_x(...).con_y(...).build()`.
- **Prototype:** crea nuovi oggetti **clonando** un prototipo esistente, invece di costruirli da zero. Utile quando la costruzione è costosa o quando serve un oggetto "come quello lì ma con due cose diverse".

```python
# Factory Method: chi chiama non conosce la classe concreta
class Documento:
    def apri(self): raise NotImplementedError
class Pdf(Documento):
    def apri(self): return "apro un PDF"
class Testo(Documento):
    def apri(self): return "apro un .txt"

def crea_documento(estensione) -> Documento:   # la factory
    return {"pdf": Pdf, "txt": Testo}[estensione]()

doc = crea_documento("pdf")   # ricevo un Documento, non mi importa quale concreto
```

## Famiglia 2 — Strutturali
Compongono oggetti in strutture più grandi.

- **Adapter (adattatore):** fa collaborare due interfacce **incompatibili** facendo da traduttore. Avvolge un oggetto e ne espone l'interfaccia che il client si aspetta (come un adattatore di presa elettrica). Serve a **far combaciare** qualcosa che già esiste.
- **Facade (facciata):** offre un'**interfaccia unica e semplice** davanti a un sottosistema complicato di molte classi. Non traduce e non aggiunge comportamento: **semplifica** l'uso nascondendo la complessità dietro un unico punto d'ingresso.
- **Decorator (decoratore):** **aggiunge responsabilità** a un oggetto avvolgendolo in un altro con la **stessa interfaccia**, a runtime e in modo componibile (es. uno stream a cui aggiungi compressione, poi cifratura). Differenza da Adapter: il Decorator mantiene la stessa interfaccia e **aggiunge** comportamento; l'Adapter **cambia** l'interfaccia senza aggiungere comportamento.
- **Proxy:** mette un **sostituto** davanti a un oggetto, con la **stessa interfaccia**, per controllarne l'accesso: caricamento pigro (lazy), cache, controllo dei permessi, chiamata remota. Differenza dal Decorator: il Proxy **controlla l'accesso** allo stesso comportamento; il Decorator **aggiunge** comportamento nuovo.
- **Composite:** tratta in modo **uniforme** oggetti singoli e loro raggruppamenti, tipicamente in strutture ad albero (es. un file e una cartella che contiene file e cartelle, entrambi con `dimensione()`).
- **Bridge** e **Flyweight** completano la famiglia: il Bridge separa un'astrazione dalla sua implementazione così che varino indipendentemente; il Flyweight condivide oggetti leggeri per risparmiare memoria quando ce ne sono moltissimi.

> Nota su Python: il decoratore con la `@` (es. `@staticmethod`, `@app.route`) è una **funzionalità del linguaggio** per avvolgere funzioni, non il **pattern GoF Decorator** (che avvolge oggetti mantenendone l'interfaccia). Si somigliano nell'idea di "avvolgere", ma non sono la stessa cosa: non confonderli al colloquio.

## Famiglia 3 — Comportamentali
Regolano come gli oggetti collaborano a runtime.

- **Strategy (strategia):** incapsula una **famiglia di algoritmi** interscambiabili dietro una stessa interfaccia, così il client può scegliere o cambiare l'algoritmo a runtime (es. diverse politiche di ordinamento, diversi metodi di pagamento). È il modo "pattern" di evitare un grosso `if/elif` sul tipo (il problema OCP visto in `xc-swe-clean`).
- **Observer (osservatore):** definisce una dipendenza **uno-a-molti**: quando un oggetto (il *subject*) cambia stato, tutti i suoi **osservatori** vengono notificati automaticamente. È la base del pattern publish/subscribe e della reattività delle UI.
- **State (stato):** fa cambiare il **comportamento** di un oggetto al variare del suo **stato interno**, come se cambiasse classe (es. un ordine che si comporta diversamente se è "in attesa", "spedito", "consegnato"). Differenza da Strategy: strutturalmente si somigliano (si delega a un oggetto interscambiabile), ma lo **scopo** è diverso. Strategy: scelgo **io** un algoritmo tra alternative equivalenti. State: l'oggetto **transita da solo** da uno stato all'altro e il comportamento cambia di conseguenza.
- **Command (comando):** incapsula una richiesta in un **oggetto**, così da poterla passare, accodare, registrare o annullare (undo). Sta dietro le code di operazioni e i sistemi di undo/redo.
- **Template Method:** definisce lo **scheletro** di un algoritmo in un metodo della classe base, lasciando alle sottoclassi il riempimento di alcuni passi (senza cambiare la struttura generale).
- **Iterator:** fornisce un modo per **scorrere** gli elementi di una collezione senza esporne la struttura interna (in Python è il protocollo `for x in ...`).

```python
# Strategy: l'algoritmo è iniettato e interscambiabile a runtime
class OrdinamentoPerPrezzo:
    def ordina(self, prodotti): return sorted(prodotti, key=lambda p: p["prezzo"])
class OrdinamentoPerNome:
    def ordina(self, prodotti): return sorted(prodotti, key=lambda p: p["nome"])

class Catalogo:
    def __init__(self, strategia): self.strategia = strategia
    def mostra(self, prodotti): return self.strategia.ordina(prodotti)

c = Catalogo(OrdinamentoPerPrezzo())   # posso passare un'altra strategia quando voglio
```

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 680 290" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <rect x="16" y="14" width="202" height="258" rx="10" fill="var(--card2)" stroke="var(--rule)"/>
    <rect x="239" y="14" width="202" height="258" rx="10" fill="var(--card2)" stroke="var(--rule)"/>
    <rect x="462" y="14" width="202" height="258" rx="10" fill="var(--card2)" stroke="var(--rule)"/>
    <text x="117" y="36" font-weight="700" fill="var(--accent)">Creazionali (5)</text>
    <text x="340" y="36" font-weight="700" fill="var(--accent)">Strutturali (7)</text>
    <text x="563" y="36" font-weight="700" fill="var(--accent)">Comportamentali (11)</text>
    <text x="117" y="52" font-size="10" fill="var(--muted)">come si creano</text>
    <text x="340" y="52" font-size="10" fill="var(--muted)">come si compongono</text>
    <text x="563" y="52" font-size="10" fill="var(--muted)">come collaborano</text>
  </g>
  <g font-size="11" fill="var(--ink)" text-anchor="middle">
    <rect x="32" y="64" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="117" y="80">Singleton</text>
    <rect x="32" y="92" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="117" y="108">Factory Method</text>
    <rect x="32" y="120" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="117" y="136">Abstract Factory</text>
    <rect x="32" y="148" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="117" y="164">Builder</text>
    <rect x="32" y="176" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="117" y="192">Prototype</text>

    <rect x="255" y="64" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="340" y="80">Adapter</text>
    <rect x="255" y="92" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="340" y="108">Facade</text>
    <rect x="255" y="120" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="340" y="136">Decorator</text>
    <rect x="255" y="148" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="340" y="164">Proxy</text>
    <rect x="255" y="176" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="340" y="192">Composite</text>
    <rect x="255" y="204" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="340" y="220">Bridge · Flyweight</text>

    <rect x="478" y="64" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="563" y="80">Strategy</text>
    <rect x="478" y="92" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="563" y="108">Observer</text>
    <rect x="478" y="120" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/><text x="563" y="136">State</text>
    <rect x="478" y="148" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="563" y="164">Command</text>
    <rect x="478" y="176" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="563" y="192">Template Method</text>
    <rect x="478" y="204" width="170" height="24" rx="5" fill="var(--card)" stroke="var(--rule)"/><text x="563" y="220">Iterator · altri</text>
  </g>
  <text x="340" y="252" font-size="10.5" fill="var(--muted)" text-anchor="middle">in evidenza: le coppie che si confondono (Decorator/Proxy, Strategy/State)</text>
  <text x="340" y="268" font-size="10.5" fill="var(--muted)" text-anchor="middle">23 pattern GoF in tutto · 5 + 7 + 11</text>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">I 23 pattern GoF nelle tre famiglie. Evidenziate le coppie strutturalmente simili ma con scopo diverso: Decorator (aggiunge comportamento) contro Proxy (controlla l'accesso), e Strategy (scelgo io l'algoritmo) contro State (l'oggetto transita da solo).</figcaption>
</figure>

## Esempi concreti
- **Strategy al posto del grosso `if` (visto in `xc-swe-clean`).** Un checkout con `if metodo == "carta" ... elif "paypal" ...` diventa una `StrategiaPagamento` iniettata: ogni metodo è una classe, aggiungerne uno non tocca il codice del checkout. Questo è l'OCP reso concreto da un pattern.
- **Adapter per una libreria che non controlli.** Due librerie di pagamento con metodi diversi (`.pay()` contro `.charge()`): invece di riempire il codice di `if`, scrivi un adapter che espone l'interfaccia `PagamentoGateway` uniforme che il resto del sistema si aspetta.
- **Observer in una UI o in un sistema a eventi.** Un carrello (subject) notifica l'icona del carrello, il totale e il badge (observer) ogni volta che aggiungi un prodotto: il carrello non deve conoscerli uno per uno, li avvisa tutti con un `notifica()`.

## Notable use case
- **Java I/O e le collezioni.** Le classi di stream (`BufferedReader` che avvolge un `Reader`) sono un caso da manuale di **Decorator**; l'intero framework delle collezioni usa l'**Iterator** per lo scorrimento uniforme.
- **React e il publish/subscribe.** Le librerie di gestione dello stato e i sistemi a eventi del front-end sono applicazioni su larga scala dell'**Observer**: i componenti si "iscrivono" allo stato e vengono rinotificati quando cambia.
- **Factory e Builder negli SDK cloud.** Molti SDK (per database, client HTTP, servizi cloud) espongono un **Builder** (`Client.builder().region(...).timeout(...).build()`) per configurare oggetti complessi in modo leggibile, e **Factory** per nascondere quale implementazione concreta restituire.

## Fonti
- **Gamma, Helm, Johnson, Vlissides (Gang of Four)** — *Design Patterns: Elements of Reusable Object-Oriented Software* (1994), il testo fondativo
- **Refactoring.Guru** — refactoring.guru/design-patterns (spiegazioni ed esempi per ogni pattern, con codice)
- **Martin Fowler** — martinfowler.com (articoli su pattern e architettura)

## Concetti adiacenti
- `prog-oop` — incapsulamento, ereditarietà, polimorfismo e astrazione: i pattern sono OOP applicata con metodo
- `xc-pat-review` — i pattern GoF più ricorrenti nel lavoro reale, con taglio pratico
- `se-principles` — i principi di progettazione (SOLID, rigidità/fragilità) che i pattern mettono in pratica
- `xc-swe-clean` — clean code e SOLID: i pattern sono quei principi confezionati in soluzioni ricorrenti

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cos'è un design pattern e perché "non è codice da copiare"? Chi è la "Gang of Four" e in quante famiglie dividono i 23 pattern?
2. Enuncia i due principi guida del libro GoF ("programma verso..." e "preferisci...").
3. A cosa serve il **Singleton** e qual è la critica principale che gli si muove?
4. Qual è la differenza tra **Factory Method** e **Abstract Factory**?
5. A cosa serve il **Builder** e in quale situazione tipica conviene?
6. Qual è la differenza tra **Adapter** e **Facade**?
7. Qual è la differenza tra **Decorator** e **Proxy** (entrambi "avvolgono" con la stessa interfaccia)?
8. In Python, il decoratore con la `@` è il pattern GoF **Decorator**? Spiega.
9. A cosa serve lo **Strategy**, e qual è la differenza di **scopo** rispetto allo **State**?
10. Cosa descrive l'**Observer** (che tipo di dipendenza), e cosa succede quando il subject cambia stato?

<details><summary>Risposte</summary>

1. È una soluzione **generale e riutilizzabile** a un problema di progettazione ricorrente: uno **schema** di collaborazione tra classi/oggetti, non codice pronto da incollare. La **Gang of Four** sono i quattro autori (Gamma, Helm, Johnson, Vlissides) di *Design Patterns* (1994); dividono i 23 pattern in **tre** famiglie: creazionali, strutturali, comportamentali.
2. **"Programma verso un'interfaccia, non verso un'implementazione"** (dipendi dal contratto astratto, non dalla classe concreta) e **"preferisci la composizione all'ereditarietà"** (comporre oggetti è più flessibile che ereditare).
3. Il **Singleton** garantisce **una sola istanza** di una classe con un punto di accesso globale. Critica: introduce **stato globale**, che rende i test difficili e nasconde le dipendenze.
4. Il **Factory Method** crea **un** prodotto lasciando alle sottoclassi quale classe concreta istanziare; l'**Abstract Factory** crea **una famiglia di oggetti correlati e coerenti** (più prodotti che vanno insieme) senza specificarne le classi concrete.
5. Il **Builder** costruisce un oggetto complesso **passo per passo**, separando costruzione e rappresentazione; conviene quando ci sono molti parametri opzionali (al posto di un costruttore con tanti argomenti).
6. L'**Adapter** fa da traduttore tra due interfacce **incompatibili** (cambia l'interfaccia per farle combaciare); la **Facade** offre un'**interfaccia unica e semplice** davanti a un sottosistema complesso (semplifica, non traduce).
7. Entrambi avvolgono un oggetto con la stessa interfaccia, ma: il **Decorator aggiunge comportamento** nuovo (componibile); il **Proxy controlla l'accesso** allo stesso comportamento (lazy, cache, permessi, chiamata remota).
8. No. Il decoratore `@` di Python è una **funzionalità del linguaggio** per avvolgere funzioni; il **Decorator GoF** avvolge **oggetti** mantenendone l'interfaccia per aggiungere responsabilità. Si somigliano nell'idea di "avvolgere" ma non sono la stessa cosa.
9. Lo **Strategy** incapsula una famiglia di **algoritmi interscambiabili** dietro una stessa interfaccia, scelti/cambiati a runtime. Differenza di scopo con lo **State**: con Strategy sono **io** a scegliere un algoritmo tra alternative equivalenti; con State è l'**oggetto a transitare da solo** da uno stato all'altro, cambiando comportamento di conseguenza.
10. L'**Observer** descrive una dipendenza **uno-a-molti**: quando il subject cambia stato, tutti i suoi **osservatori** vengono **notificati automaticamente**.
</details>

## Esercizi
1. **Applica lo Strategy.** Riscrivi questa funzione eliminando l'`if/elif` sul tipo, in modo che aggiungere un nuovo tipo di sconto non richieda di modificare il codice che applica lo sconto.
   ```python
   def prezzo_finale(prezzo, tipo_cliente):
       if tipo_cliente == "standard":  return prezzo
       elif tipo_cliente == "premium": return prezzo * 0.9
       elif tipo_cliente == "vip":     return prezzo * 0.8
       else: raise ValueError("tipo sconosciuto")
   ```
2. **Riconosci il pattern.** Per ciascuno di questi tre scenari, indica quale pattern GoF useresti e in una riga perché: (a) hai una libreria esterna con metodo `fetch_rows()` ma il tuo codice si aspetta ovunque un oggetto con `get_all()`; (b) vuoi che, quando un ordine cambia stato, si aggiornino da soli la dashboard, la mail al cliente e il log, senza che l'ordine li conosca uno per uno; (c) vuoi aggiungere "logging" e poi "cache" attorno a un servizio esistente, in modo componibile e senza modificarlo.
3. **Implementa un Observer minimo.** Scrivi una classe `Soggetto` con `iscrivi(osservatore)` e `notifica(evento)`, e due osservatori che reagiscono stampando qualcosa. Mostra l'uso.

<details><summary>Soluzioni</summary>

1. Ogni politica di sconto diventa una strategia; un registro mappa il tipo alla strategia. Aggiungere un tipo = una classe nuova, zero modifiche a `prezzo_finale` (OCP).
   ```python
   class Sconto:
       def applica(self, prezzo): raise NotImplementedError
   class Nessuno(Sconto):
       def applica(self, prezzo): return prezzo
   class Premium(Sconto):
       def applica(self, prezzo): return prezzo * 0.9
   class Vip(Sconto):
       def applica(self, prezzo): return prezzo * 0.8

   SCONTI = {"standard": Nessuno(), "premium": Premium(), "vip": Vip()}
   def prezzo_finale(prezzo, tipo_cliente):
       return SCONTI[tipo_cliente].applica(prezzo)
   ```
2. (a) **Adapter**: avvolgi la libreria esponendo `get_all()` che internamente chiama `fetch_rows()`, così il resto del codice non cambia. (b) **Observer**: l'ordine è il subject, dashboard/mail/log sono osservatori iscritti; al cambio di stato chiama `notifica()` e li avvisa tutti senza conoscerli singolarmente. (c) **Decorator**: avvolgi il servizio in un decoratore di logging, poi quello in un decoratore di cache, tutti con la stessa interfaccia del servizio; li componi a piacere senza toccarlo.
3. Un Observer essenziale:
   ```python
   class Soggetto:
       def __init__(self): self._osservatori = []
       def iscrivi(self, osservatore): self._osservatori.append(osservatore)
       def notifica(self, evento):
           for o in self._osservatori:
               o.aggiorna(evento)

   class LogObserver:
       def aggiorna(self, evento): print(f"[log] ricevuto: {evento}")
   class MailObserver:
       def aggiorna(self, evento): print(f"[mail] invio notifica per: {evento}")

   s = Soggetto()
   s.iscrivi(LogObserver())
   s.iscrivi(MailObserver())
   s.notifica("ordine spedito")
   # stampa: [log] ricevuto: ordine spedito / [mail] invio notifica per: ordine spedito
   ```
</details>
