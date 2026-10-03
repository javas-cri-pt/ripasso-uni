---
day: 32
topic_id: xc-swe-clean
title: "Clean code e principi SOLID in pratica"
area: cross-cutting
course: "Software Engineering (craft del lavoro)"
grounded_in: null
adjacent: [se-principles, prog-oop, xc-swe-refactor, se-patterns]
completeness_checked: true
quiz_count: 10
---

# Clean code e principi SOLID in pratica

> **Perché oggi:** il codice si scrive una volta e si legge cento. Quasi tutto il tempo di un ingegnere se ne va a leggere codice esistente, capirlo e cambiarlo senza romperlo. "Clean code" e i principi **SOLID** sono il vocabolario con cui si parla di *qualità interna* del software: perché un modulo è facile o doloroso da modificare. È una delle domande da colloquio più frequenti ("mi spieghi i principi SOLID con un esempio?") e il metro con cui viene giudicato il tuo codice in una code review. Qui li vediamo uno per uno, ciascuno con uno snippet che li viola e uno che li rispetta.

## Cosa intendiamo per "clean code"
Per **clean code** si intende codice che un altro sviluppatore (o tu stessa fra sei mesi) riesce a leggere, capire e modificare in fretta e con pochi rischi. Non è una questione estetica: è **qualità interna**, cioè quanto è economico far evolvere il software. La qualità esterna (fa la cosa giusta?) la vede l'utente; la qualità interna la pagano gli sviluppatori a ogni modifica. Tre regole base, prima dei principi grandi:

- **Nomi che rivelano l'intento.** Una variabile `d` non dice nulla; `giorni_trascorsi` sì. Il nome giusto rende superfluo il commento. Evito nomi generici (`data`, `info`, `tmp`, `manager`) e abbreviazioni oscure.
- **Funzioni piccole che fanno una cosa sola.** Una funzione dovrebbe stare a un solo **livello di astrazione** e avere pochi parametri. Se per spiegarla devo dire "fa questo *e* quest'altro", va spezzata.
- **Niente commenti che spiegano codice brutto.** Il commento giusto spiega il *perché* (una scelta non ovvia), non il *cosa* (quello lo dice il codice se è pulito). Un commento che descrive una riga ovvia è rumore che va aggiornato a ogni modifica.

## Tre acronimi prima di SOLID: DRY, KISS, YAGNI
Sono tre euristiche che guidano le scelte quotidiane.

- **DRY** (*Don't Repeat Yourself*, "non ripeterti"): ogni pezzo di conoscenza deve avere **una sola rappresentazione** nel sistema. Se la stessa regola (es. "l'IVA è il 22%") è copiata in cinque punti, cambiarla significa trovarli tutti e cinque, e dimenticarne uno è un bug. La si estrae in un unico posto. Cautela: DRY riguarda la *conoscenza*, non le righe che per caso si somigliano; unificare due cose che cambiano per ragioni diverse crea un accoppiamento falso.
- **KISS** (*Keep It Simple, Stupid*, "tienila semplice"): a parità di risultato, la soluzione più semplice è la migliore. La complessità va aggiunta solo quando serve davvero, perché ogni astrazione in più è altro codice da capire.
- **YAGNI** (*You Aren't Gonna Need It*, "non ti servirà"): non costruire funzionalità o generalizzazioni "per il futuro" finché non servono per davvero. Il codice speculativo è quasi sempre sbagliato, e intanto è peso morto da mantenere.

Tienili a mente leggendo SOLID: i principi servono a rendere il codice flessibile dove serve, non a riempirlo di astrazioni per sport.

## SOLID: i cinque principi, uno per uno
**SOLID** è un acronimo che raccoglie cinque principi di progettazione orientata agli oggetti, resi popolari da Robert C. Martin. Puntano tutti allo stesso bersaglio: codice che si estende **aggiungendo** cose nuove invece di **modificare** (e rischiare di rompere) cose che già funzionano.

### S — Single Responsibility Principle (SRP)
**Principio di singola responsabilità:** una classe deve avere **una sola ragione per cambiare**, cioè servire un solo "committente" o aspetto del sistema. Se una classe gestisce insieme logica di business, salvataggio su database e formattazione di un report, un cambiamento in uno qualsiasi dei tre la fa modificare: tre ragioni per cambiare, troppa roba insieme.

```python
# VIOLA SRP: la classe calcola, salva e stampa
class Report:
    def calcola_totale(self): ...
    def salva_su_db(self): ...        # motivo di cambiamento: lo storage
    def formatta_html(self): ...      # motivo di cambiamento: la presentazione

# RISPETTA SRP: ogni responsabilità in una classe
class Report:
    def calcola_totale(self): ...
class ReportRepository:
    def salva(self, report): ...
class ReportFormatter:
    def to_html(self, report): ...
```

### O — Open/Closed Principle (OCP)
**Principio aperto/chiuso:** un modulo deve essere **aperto all'estensione ma chiuso alla modifica**. Devo poter aggiungere un comportamento nuovo senza toccare il codice esistente, di solito introducendo un'astrazione (un'interfaccia) e nuove implementazioni. Il segnale d'allarme è un `if/elif` sul "tipo" che cresce a ogni nuovo caso.

```python
# VIOLA OCP: ogni nuova forma richiede di modificare questa funzione
def area(forma):
    if forma.tipo == "cerchio":   return 3.14 * forma.r ** 2
    elif forma.tipo == "quadrato": return forma.lato ** 2
    # aggiungere "triangolo" significa riaprire e modificare qui

# RISPETTA OCP: ogni forma porta la propria area; aggiungerne una non tocca il resto
class Forma:
    def area(self): raise NotImplementedError
class Cerchio(Forma):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2
class Quadrato(Forma):
    def __init__(self, lato): self.lato = lato
    def area(self): return self.lato ** 2
def area_totale(forme): return sum(f.area() for f in forme)
```

### L — Liskov Substitution Principle (LSP)
**Principio di sostituzione di Liskov:** un oggetto di una sottoclasse deve poter sostituire un oggetto della superclasse **senza rompere** il comportamento atteso. Se un sottotipo richiede di più o garantisce di meno del tipo base, l'ereditarietà sta mentendo. L'esempio classico è **Quadrato come sottoclasse di Rettangolo**: concettualmente un quadrato "è un" rettangolo, ma se imposto larghezza e altezza in modo indipendente, il quadrato è costretto a cambiarle entrambe e viola le aspettative di chi usa un Rettangolo.

```python
# VIOLA LSP
class Rettangolo:
    def __init__(self, b, h): self._b, self._h = b, h
    def set_base(self, b): self._b = b
    def set_altezza(self, h): self._h = h
    def area(self): return self._b * self._h

class Quadrato(Rettangolo):          # "è un" rettangolo?
    def set_base(self, b): self._b = self._h = b      # effetto collaterale sorpresa
    def set_altezza(self, h): self._b = self._h = h

def allarga_a_10x4(r: Rettangolo):
    r.set_base(10); r.set_altezza(4)
    assert r.area() == 40            # vero per Rettangolo, FALSO per Quadrato (16)
```

La soluzione non è forzare l'ereditarietà: è non far ereditare Quadrato da Rettangolo (modellarli come due tipi separati, magari con una `Forma` comune). L'ereditarietà esprime una vera relazione "è un", non una somiglianza superficiale.

### I — Interface Segregation Principle (ISP)
**Principio di segregazione delle interfacce:** meglio **tante interfacce piccole e specifiche** che una grande e generica. Un client non deve essere costretto a dipendere da metodi che non usa. Un'interfaccia `Lavoratore` con `lavora()` e `mangia()` costringe un `RobotLavoratore` a implementare `mangia()` che non ha senso: va spezzata.

```python
# VIOLA ISP: interfaccia troppo grassa
class Macchina:
    def stampa(self): ...
    def invia_fax(self): ...     # una stampante base non fa il fax

# RISPETTA ISP: ruoli separati, ogni client dipende solo da ciò che usa
class Stampante:
    def stampa(self): ...
class Fax:
    def invia_fax(self): ...
```

### D — Dependency Inversion Principle (DIP)
**Principio di inversione delle dipendenze:** i moduli di alto livello (la logica di business) non devono dipendere dai moduli di basso livello (dettagli come il database o un servizio esterno); **entrambi devono dipendere da un'astrazione**. In pratica, invece di creare dentro una classe l'oggetto concreto che le serve, glielo si **passa dall'esterno** (constructor injection) tramite un'interfaccia. Questo è il cuore della testabilità: in un test posso iniettare un finto al posto del vero database.

```python
# VIOLA DIP: Notificatore crea e dipende dal dettaglio concreto EmailSender
class EmailSender:
    def send(self, msg): ...
class Notificatore:
    def __init__(self): self.sender = EmailSender()   # legato per sempre all'email
    def avvisa(self, msg): self.sender.send(msg)

# RISPETTA DIP: dipende da un'astrazione, il dettaglio arriva dall'esterno
class Sender:                         # astrazione
    def send(self, msg): raise NotImplementedError
class EmailSender(Sender):
    def send(self, msg): ...
class SmsSender(Sender):
    def send(self, msg): ...
class Notificatore:
    def __init__(self, sender: Sender):      # iniezione via costruttore
        self.sender = sender
    def avvisa(self, msg): self.sender.send(msg)
# ora posso passare Email, Sms o un finto da test senza toccare Notificatore
```

## Due concetti trasversali: accoppiamento e coesione
Sotto a tutto SOLID ci sono due misure.

- **Accoppiamento (coupling):** quanto un modulo dipende da un altro. Alto accoppiamento significa che toccare A rompe B: si punta a tenerlo **basso**.
- **Coesione (cohesion):** quanto le parti di un modulo appartengono davvero insieme. Alta coesione significa che una classe fa un lavoro ben definito: si punta a tenerla **alta**.

Lo slogan è "**loose coupling, high cohesion**" (accoppiamento lasco, coesione alta). SRP alza la coesione; DIP e OCP abbassano l'accoppiamento.

## Il rovescio della medaglia: non esagerare
SOLID serve a gestire il cambiamento, ma applicato alla cieca produce **over-engineering**: interfacce con un solo implementatore, livelli di astrazione inutili, fabbriche di fabbriche. Ogni astrazione ha un costo (più file, più indirezioni da seguire con gli occhi). La regola pratica: introduci l'astrazione **quando il cambiamento si presenta davvero** (un secondo tipo, una seconda implementazione), non prima. È lo stesso spirito di YAGNI. Un codice troppo rigido e uno troppo astratto sono entrambi difficili da leggere.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 680 250" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <text x="165" y="20" font-weight="700">Senza DIP</text>
    <rect x="95" y="36" width="140" height="40" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="165" y="60">Notificatore</text>
    <rect x="95" y="150" width="140" height="40" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="165" y="174">EmailSender</text>
    <text x="165" y="118" font-size="10.5" fill="var(--muted)">dipende dal</text>
    <text x="165" y="132" font-size="10.5" fill="var(--muted)">dettaglio concreto</text>
    <text x="515" y="20" font-weight="700">Con DIP</text>
    <rect x="445" y="36" width="140" height="40" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="515" y="60">Notificatore</text>
    <rect x="445" y="93" width="140" height="36" rx="8" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/><text x="515" y="115" font-size="11.5">Sender (astrazione)</text>
    <rect x="378" y="188" width="128" height="38" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="442" y="211" font-size="11">EmailSender</text>
    <rect x="524" y="188" width="128" height="38" rx="8" fill="var(--card)" stroke="var(--rule)"/><text x="588" y="211" font-size="11">SmsSender</text>
    <text x="515" y="160" font-size="10" fill="var(--muted)">entrambi dipendono dall'astrazione</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arr-clean)">
    <path d="M165,78 L165,148"/>
    <path d="M515,78 L515,91"/>
    <path d="M442,186 L470,131"/>
    <path d="M588,186 L560,131"/>
  </g>
  <defs><marker id="arr-clean" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">L'inversione delle dipendenze: a sinistra la logica di alto livello punta direttamente al dettaglio concreto (rigido). A destra la freccia si "inverte": sia la logica sia i dettagli puntano a un'astrazione comune, e il dettaglio vero si inietta dall'esterno.</figcaption>
</figure>

## Esempi concreti
- **Il `WHERE` dell'IVA sparso ovunque (DRY).** Se l'aliquota 22% compare in dieci funzioni, il giorno che cambia diventa una caccia al tesoro con bug garantiti. La estraggo in una sola costante/funzione (`aliquota_iva()`) e la richiamo: una sola ragione per cambiare, un solo posto da toccare.
- **Il parametro `is_test=True` (OCP violato).** Una funzione piena di `if is_test:` che cambia comportamento a seconda del contesto va riaperta a ogni nuovo caso. Meglio un'astrazione iniettata (es. un `Gateway` finto in test, uno vero in produzione): il comportamento si estende senza toccare la funzione.
- **Constructor injection per testare (DIP).** Una classe che fa `self.db = Postgres()` dentro di sé non si può testare senza un vero database. Se il `db` arriva dal costruttore, nel test gli passo un finto in memoria e verifico la logica in millisecondi. Questo collega clean code direttamente alla strategia di test (vedi `xc-swe-tdd`).

## Notable use case
- **Lo stile di Google (Google Style Guides).** Google pubblica guide di stile per ogni linguaggio e impone **readability review**: prima di poter approvare codice in un linguaggio devi dimostrare di scriverlo in modo pulito e leggibile secondo lo standard interno.
- **PEP 8 e `black` in Python.** La comunità Python ha una guida di stile ufficiale (**PEP 8**) e strumenti che la applicano automaticamente (`black`, `ruff`): la formattazione smette di essere oggetto di dibattito perché è automatizzata.
- **ESLint / Prettier nel mondo JavaScript.** Linter e formatter girano in automatico a ogni commit per tenere lo stile uniforme su tutta la squadra, così le review discutono di sostanza e non di spazi.

## Fonti
- **Robert C. Martin** — *Clean Code* e *Agile Software Development, Principles, Patterns, and Practices* (la fonte dei principi SOLID)
- **Martin Fowler** — martinfowler.com (articoli su accoppiamento, coesione, code smell)
- **PEP 8** — peps.python.org/pep-0008 (la guida di stile ufficiale di Python)
- **Google Style Guides** — google.github.io/styleguide

## Concetti adiacenti
- `se-principles` — i principi di progettazione all'università: rigidità, fragilità, immobilità, e SOLID nella trattazione teorica
- `prog-oop` — incapsulamento, ereditarietà, polimorfismo e astrazione, i mattoni OOP su cui SOLID poggia
- `xc-swe-refactor` — come migliorare codice esistente (e ripagare il debito tecnico) applicando questi principi a posteriori
- `se-patterns` — i design pattern GoF, che sono SOLID "confezionato" in soluzioni ricorrenti

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cosa si intende per "qualità interna" del codice, e in che senso è diversa dalla qualità esterna?
2. Cosa dice **DRY**, e qual è la cautela da ricordare (DRY riguarda cosa, esattamente)?
3. Qual è la differenza tra **KISS** e **YAGNI**?
4. Enuncia il **Single Responsibility Principle** usando l'espressione "ragione per cambiare".
5. Cosa significa che un modulo è "**aperto all'estensione ma chiuso alla modifica**" (OCP), e qual è il tipico segnale che lo stai violando?
6. Perché l'esempio **Quadrato/Rettangolo** viola il **Liskov Substitution Principle**?
7. Cosa dice l'**Interface Segregation Principle** e che problema evita?
8. Enuncia il **Dependency Inversion Principle** e spiega cos'è la **constructor injection**.
9. Definisci **accoppiamento** e **coesione**: quale si vuole basso e quale alto?
10. Cos'è l'**over-engineering** e qual è la regola pratica per decidere quando introdurre un'astrazione?

<details><summary>Risposte</summary>

1. La **qualità interna** è quanto è economico leggere, capire e modificare il codice (la pagano gli sviluppatori a ogni modifica); la **qualità esterna** è se il software fa la cosa giusta (la vede l'utente). Clean code riguarda la prima.
2. **Don't Repeat Yourself:** ogni pezzo di conoscenza ha una sola rappresentazione nel sistema. Cautela: riguarda la **conoscenza/regola**, non le righe che per caso si somigliano; unificare cose che cambiano per ragioni diverse crea un accoppiamento falso.
3. **KISS** (Keep It Simple): a parità di risultato scegli la soluzione più semplice. **YAGNI** (You Aren't Gonna Need It): non costruire funzionalità o generalizzazioni per un futuro ipotetico finché non servono davvero. Uno parla di semplicità del presente, l'altro di non anticipare il futuro.
4. **Single Responsibility Principle:** una classe deve avere **una sola ragione per cambiare**, cioè servire un solo aspetto/committente del sistema.
5. Significa che devo poter aggiungere comportamento **nuovo** senza modificare il codice **esistente**, di solito tramite un'astrazione e nuove implementazioni. Segnale di violazione: un `if/elif` sul "tipo" che cresce a ogni nuovo caso.
6. Perché un `Quadrato` sottoclasse di `Rettangolo` non può onorare le aspettative su un Rettangolo: impostando base e altezza in modo indipendente il quadrato le cambia entrambe, così codice che si aspetta `area == base*altezza` si rompe. Il sottotipo non è sostituibile al tipo base.
7. **Interface Segregation Principle:** meglio tante interfacce piccole e specifiche che una grande e generica; evita che un client sia costretto a dipendere (e implementare) metodi che non usa.
8. **Dependency Inversion Principle:** i moduli di alto livello e quelli di basso livello devono entrambi dipendere da un'**astrazione**, non l'alto dal basso. La **constructor injection** è passare la dipendenza (l'implementazione concreta) dall'esterno attraverso il costruttore, invece di crearla dentro la classe.
9. **Accoppiamento:** quanto un modulo dipende da un altro, si vuole **basso**. **Coesione:** quanto le parti di un modulo appartengono insieme, si vuole **alta**. Slogan: loose coupling, high cohesion.
10. L'**over-engineering** è aggiungere astrazioni inutili (interfacce con un solo implementatore, livelli superflui) che costano leggibilità senza dare flessibilità reale. Regola pratica: introduci l'astrazione **quando il cambiamento si presenta davvero** (un secondo caso/implementazione), non prima.
</details>

## Esercizi
1. **Refactor SRP + DIP.** La classe seguente viola SRP (calcola, salva e notifica) e DIP (crea dentro di sé i dettagli concreti). Riscrivila separando le responsabilità e iniettando le dipendenze dall'esterno.
   ```python
   class GestoreOrdine:
       def processa(self, ordine):
           totale = sum(r["prezzo"] * r["qta"] for r in ordine["righe"])
           # salvataggio
           import sqlite3
           con = sqlite3.connect("ordini.db")
           con.execute("INSERT INTO ordini VALUES (?,?)", (ordine["id"], totale))
           con.commit()
           # notifica
           print(f"Email a {ordine['email']}: ordine {ordine['id']} totale {totale}")
           return totale
   ```
2. **Elimina l'`if` sul tipo (OCP).** Questa funzione va riaperta a ogni nuovo metodo di spedizione. Riscrivila in modo che aggiungere un corriere nuovo non richieda di toccare `costo_spedizione`.
   ```python
   def costo_spedizione(tipo, peso):
       if tipo == "standard": return 5 + 0.5 * peso
       elif tipo == "express": return 12 + 0.9 * peso
       elif tipo == "ritiro":  return 0
       else: raise ValueError("tipo sconosciuto")
   ```
3. **Trova la violazione.** In questo frammento c'è una violazione di LSP: individuala e spiega perché, poi proponi come modellare le classi diversamente.
   ```python
   class Uccello:
       def vola(self): return "sto volando"
   class Pinguino(Uccello):
       def vola(self): raise NotImplementedError("i pinguini non volano")
   def fai_volare(u: Uccello): print(u.vola())
   ```

<details><summary>Soluzioni</summary>

1. Separo le tre responsabilità in tre collaboratori e li inietto nel costruttore (DIP). `GestoreOrdine` ora ha una sola ragione per cambiare (la logica dell'ordine) e in test posso passare un repository e un notificatore finti.
   ```python
   class GestoreOrdine:
       def __init__(self, repo, notificatore):
           self.repo = repo
           self.notificatore = notificatore
       def processa(self, ordine):
           totale = sum(r["prezzo"] * r["qta"] for r in ordine["righe"])
           self.repo.salva(ordine["id"], totale)
           self.notificatore.invia(ordine["email"], ordine["id"], totale)
           return totale

   class OrdineRepository:          # responsabilità: persistenza
       def __init__(self, con): self.con = con
       def salva(self, id_ordine, totale):
           self.con.execute("INSERT INTO ordini VALUES (?,?)", (id_ordine, totale))
           self.con.commit()

   class EmailNotificatore:         # responsabilità: notifica
       def invia(self, email, id_ordine, totale):
           print(f"Email a {email}: ordine {id_ordine} totale {totale}")
   ```
2. Trasformo ogni corriere in una strategia con un metodo `costo`, e uso un registro. Aggiungere un corriere significa aggiungere una classe, non modificare la funzione (OCP rispettato).
   ```python
   class Corriere:
       def costo(self, peso): raise NotImplementedError
   class Standard(Corriere):
       def costo(self, peso): return 5 + 0.5 * peso
   class Express(Corriere):
       def costo(self, peso): return 12 + 0.9 * peso
   class Ritiro(Corriere):
       def costo(self, peso): return 0

   CORRIERI = {"standard": Standard(), "express": Express(), "ritiro": Ritiro()}
   def costo_spedizione(tipo, peso):
       return CORRIERI[tipo].costo(peso)
   # un corriere nuovo = nuova classe + una riga nel registro, zero modifiche alla logica
   ```
3. Viola **LSP**: `Pinguino` è dichiarato sottotipo di `Uccello` ma non può onorare il contratto `vola()` (lo fa esplodere). Chi scrive `fai_volare(u: Uccello)` si aspetta che ogni `Uccello` voli, e un `Pinguino` lo rompe. Modellazione corretta: non mettere `vola()` nella base. Separare la capacità: una base `Uccello` senza volo, e un'interfaccia/mixin `Volatore` con `vola()` implementata solo dagli uccelli che volano. Così `fai_volare` accetta `Volatore`, e un `Pinguino` semplicemente non è un `Volatore`.
   ```python
   class Uccello: ...
   class Volatore:
       def vola(self): raise NotImplementedError
   class Rondine(Uccello, Volatore):
       def vola(self): return "sto volando"
   class Pinguino(Uccello): ...            # niente vola(): non è un Volatore
   def fai_volare(v: Volatore): print(v.vola())
   ```
</details>
