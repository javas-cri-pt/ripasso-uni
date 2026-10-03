---
day: 25
topic_id: prog-oop
title: "Principi OOP: incapsulamento, ereditarietà, polimorfismo, astrazione"
area: computer-science
course: "Programmazione & OOP"
grounded_in: null
adjacent: [se-patterns, se-principles, prog-ds]
completeness_checked: true
quiz_count: 10
---

# Principi della programmazione a oggetti

> **Perché oggi:** la **programmazione a oggetti** (OOP, *Object-Oriented Programming*) è il modello con cui sono scritti Java, C#, Python e buona parte del software che userai al lavoro. I suoi quattro pilastri — incapsulamento, ereditarietà, polimorfismo, astrazione — sono la **base di ogni colloquio tecnico** ("spiegami il polimorfismo", "quando usi un'interfaccia?") e sono le **fondamenta** su cui poggiano i design pattern e i principi **SOLID** (cinque principi di progettazione a oggetti, vedi `se-principles`). Capirli bene qui ti fa capire tutto il resto senza fatica.

## Classe e oggetto: la distinzione di base

La **programmazione a oggetti** è un modo di organizzare il codice attorno a **oggetti**: entità che tengono insieme **dati** (cosa sanno) e **comportamenti** (cosa sanno fare), invece di tenere dati e funzioni separati come nella programmazione procedurale.

Due termini da non confondere mai:

- **Classe (class)** — è lo **stampo**, il progetto: descrive *com'è fatto* un certo tipo di cosa (quali dati ha, quali operazioni offre). La classe è codice che scrivi una volta. Esempio: la classe `Automobile` definisce che un'auto ha una targa, un colore, e sa `accelera()` e `frena()`.
- **Oggetto (object)**, detto anche **istanza (instance)** — è l'**esemplare concreto** creato a partire dalla classe, con valori propri. Dalla classe `Automobile` crei l'oggetto "la mia Panda rossa targata AB123CD" e l'oggetto "la Golf nera targata EF456GH": due oggetti distinti, stesso stampo.

Il verbo per creare un oggetto da una classe è **istanziare** (in Java con `new`, in Python chiamando la classe): `Automobile a = new Automobile();`. Ogni oggetto ha il suo **stato** (i valori dei suoi dati in un dato momento) e risponde ai **metodi** (le operazioni) definiti dalla classe.

I dati di un oggetto si chiamano **attributi** (o campi, *fields*); le operazioni si chiamano **metodi** (*methods*).

## Pilastro 1 — Incapsulamento (encapsulation)

L'**incapsulamento** è il principio di **nascondere i dati interni** di un oggetto e permettere l'accesso solo attraverso **metodi pubblici** controllati. L'oggetto diventa una scatola chiusa: dall'esterno non tocchi direttamente i suoi dati, ma gli chiedi di fare qualcosa.

In pratica si realizza con i **modificatori di accesso** (*access modifiers*), parole chiave che dicono chi può vedere cosa:

- **`private`** — visibile **solo dentro la classe**. Gli attributi si tengono quasi sempre private.
- **`public`** — visibile da **chiunque**, da qualsiasi punto del programma. Ci si mettono i metodi che formano l'interfaccia d'uso dell'oggetto.
- **`protected`** — visibile dalla classe stessa e dalle sue **sottoclassi** (utile con l'ereditarietà, vedi sotto).

Per leggere o modificare un attributo privato dall'esterno si usano metodi appositi:

- **getter** — un metodo pubblico che **restituisce** il valore di un attributo (es. `getSaldo()`).
- **setter** — un metodo pubblico che **modifica** un attributo, potendo controllare che il nuovo valore sia valido (es. `setSaldo(x)` che rifiuta valori negativi).

**Perché serve.** Se chiunque potesse scrivere direttamente `conto.saldo = -5000`, lo stato dell'oggetto diventerebbe incoerente e nessuno saprebbe chi l'ha rotto. Tenendo `saldo` private e offrendo `preleva(importo)` che controlla la copertura, **l'oggetto difende da solo le proprie regole** (gli *invarianti*). In più puoi cambiare come è fatto dentro (p.es. come memorizzi il saldo) senza rompere chi usa l'oggetto, perché l'esterno vede solo i metodi pubblici: questo è **basso accoppiamento** (`se-principles`).

## Pilastro 2 — Ereditarietà (inheritance)

L'**ereditarietà** permette a una classe di **riutilizzare** attributi e metodi di un'altra, estendendola. La classe di partenza si chiama **superclasse** (o classe base/genitore); quella che eredita si chiama **sottoclasse** (o classe derivata/figlia).

La relazione che esprime è **"is-a"** ("è un/una"): una sottoclasse **è un caso particolare** della superclasse. `Cane` eredita da `Animale` perché *un cane è un animale*. La sottoclasse prende "gratis" tutto ciò che ha la superclasse e può **aggiungere** roba propria.

Due meccanismi chiave:

- **`super`** — parola chiave con cui la sottoclasse richiama la superclasse: `super()` chiama il **costruttore** del genitore (il metodo speciale che inizializza un nuovo oggetto), `super.metodo()` chiama la versione del metodo definita nel genitore.
- **override (ridefinizione)** — la sottoclasse **ridefinisce** un metodo ereditato, dandogli un comportamento proprio. `Animale` ha `verso()` generico; `Cane` fa override di `verso()` per restituire "Bau".

**I rischi.** L'ereditarietà crea un legame forte: la sottoclasse dipende dai dettagli della superclasse, e un cambiamento nel genitore può rompere i figli (**accoppiamento alto**, fragilità). Un errore classico è usarla per puro riuso di codice anche quando la relazione "is-a" non regge (es. far ereditare `Pila` da `Lista` solo perché "contengono elementi"): si creano gerarchie innaturali che violano il **principio di sostituzione di Liskov** (una sottoclasse deve poter sostituire la superclasse senza rompere il programma; vedi `se-principles`). Regola pratica: eredita **solo** se vale davvero "la sottoclasse *è un* tipo di superclasse".

## Pilastro 3 — Polimorfismo (polymorphism)

**Polimorfismo** significa letteralmente "molte forme": lo stesso **nome** (di metodo) produce **comportamenti diversi** a seconda dell'oggetto su cui agisce. È ciò che rende l'OOP flessibile. Si presenta in due forme da non confondere:

- **Overriding (ridefinizione)** — è il polimorfismo "vero", a **runtime**. Più sottoclassi fanno override dello stesso metodo della superclasse, ciascuna con la propria versione. Chiami `animale.verso()` su una variabile di tipo `Animale`, ma viene eseguita la versione del **tipo reale** dell'oggetto (Cane → "Bau", Gatto → "Miao"). La scelta di *quale* versione eseguire avviene mentre il programma gira, in base all'oggetto effettivo: questo meccanismo si chiama **dynamic dispatch** (o *late binding*, legame ritardato).
- **Overloading (sovraccarico)** — è cosa **diversa**: definire nella stessa classe **più metodi con lo stesso nome** ma **parametri diversi** (numero o tipo). Es. `somma(int, int)` e `somma(double, double)`. Qui la scelta la fa il **compilatore** in base agli argomenti (è statica, a compile-time), non c'entra con l'ereditarietà.

**Esempio concreto del dynamic dispatch.** Hai una lista di `Animale` che contiene cani e gatti mischiati. Scrivi un solo ciclo:

```
for (Animale a : animali) {
    System.out.println(a.verso());   // Bau, Miao, Bau, ...
}
```

Il codice non sa né gli importa quali tipi concreti ci sono: ogni oggetto risponde con il **proprio** verso. Se domani aggiungi la classe `Mucca`, questo ciclo funziona senza una riga di modifica — è l'estensibilità alla base del principio **Open/Closed** (aperto all'estensione, chiuso alla modifica: aggiungi comportamenti senza toccare il codice esistente; vedi `se-principles`).

## Schema: ereditarietà + polimorfismo

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 640 300" style="max-width:100%;height:auto;font-family:inherit">
  <defs><marker id="arOopInh" markerWidth="12" markerHeight="12" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 Z" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
   <rect x="230" y="20" width="180" height="60" rx="9" fill="var(--card)" stroke="var(--accent)" stroke-width="1.8"/>
   <text x="320" y="44" font-size="13">Animale</text>
   <text x="320" y="64" font-size="10.5" fill="var(--muted)">verso() : String</text>

   <rect x="60" y="200" width="200" height="72" rx="9" fill="var(--card)" stroke="var(--rule)"/>
   <text x="160" y="224" font-size="13">Cane</text>
   <text x="160" y="244" font-size="10.5" fill="var(--muted)">override verso()</text>
   <text x="160" y="261" font-size="10.5" fill="var(--muted)">&#8594; "Bau"</text>

   <rect x="380" y="200" width="200" height="72" rx="9" fill="var(--card)" stroke="var(--rule)"/>
   <text x="480" y="224" font-size="13">Gatto</text>
   <text x="480" y="244" font-size="10.5" fill="var(--muted)">override verso()</text>
   <text x="480" y="261" font-size="10.5" fill="var(--muted)">&#8594; "Miao"</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.4" fill="none" marker-end="url(#arOopInh)">
   <path d="M160,200 L285,82"/>
   <path d="M480,200 L355,82"/>
  </g>
  <g font-size="10" fill="var(--muted)" text-anchor="middle">
   <text x="200" y="150">is-a (eredita)</text>
   <text x="440" y="150">is-a (eredita)</text>
  </g>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">Ereditarietà: Cane e Gatto sono-un Animale (freccia vuota verso la superclasse) ed ereditano verso(). Polimorfismo: ciascuno fa override di verso() con la propria versione, e chiamando verso() su un Animale generico viene eseguita quella del tipo reale (dynamic dispatch).</figcaption>
</figure>

## Pilastro 4 — Astrazione (abstraction)

L'**astrazione** è concentrarsi su **cosa** fa un oggetto, nascondendo il **come**. Definisci un "contratto" di operazioni senza (o prima di) dire come sono implementate. Due strumenti la realizzano, e sapere **quando usare l'uno o l'altro** è una domanda da colloquio frequente:

- **Classe astratta (abstract class)** — una classe che **non può essere istanziata** direttamente (non puoi fare `new`) e serve da base comune. Può avere **sia metodi già implementati** (comportamento condiviso) **sia metodi astratti** (dichiarati senza corpo, che le sottoclassi *devono* implementare). Es. `Animale` astratta con `mangia()` già scritto (uguale per tutti) e `verso()` astratto (ognuno il suo).
- **Interfaccia (interface)** — un **puro contratto**: elenca metodi che una classe si impegna a fornire, tradizionalmente **senza implementazione** e sempre **senza stato** (niente attributi d'istanza). Una classe che "implementa" un'interfaccia promette di offrire tutti quei metodi. Es. l'interfaccia `Pagabile` con `paga()`: la implementano classi anche molto diverse tra loro. (Nota: da **Java 8** un'interfaccia può avere anche metodi `default` con un corpo già scritto; resta comunque priva di stato d'istanza — ed è una classica domanda di follow-up "interfaccia vs classe astratta dopo Java 8".)

**Quando l'una, quando l'altra.** Usi la **classe astratta** quando le sottoclassi sono **parenti stretti** che condividono codice e stato (relazione "is-a" forte). Usi l'**interfaccia** quando vuoi dare una **capacità** a classi che non hanno nulla in comune per natura (relazione "is-able-to", "sa fare"): `Pagabile` può essere implementata da `Ordine`, `Abbonamento`, `Multa`. Vincolo importante (tuttora in vigore): in Java una classe può estendere **una sola** classe (astratta o no), ma può implementare **molte** interfacce — quindi le interfacce sono il modo per combinare più capacità.

## Composizione vs ereditarietà ("favor composition")

Oltre all'ereditarietà c'è un secondo modo di riusare codice: la **composizione (composition)**, cioè costruire un oggetto **mettendogli dentro** altri oggetti come attributi, e delegando a loro il lavoro. Relazione **"has-a"** ("ha un/una"): un'`Automobile` *ha un* `Motore`, invece di *essere un* motore.

Il consiglio consolidato (dai **GoF**, *Gang of Four*, i quattro autori del libro *Design Patterns* del 1994, in poi) è **"favor composition over inheritance"**, preferisci la composizione all'ereditarietà. Perché:

- L'ereditarietà lega la sottoclasse ai dettagli interni della superclasse (accoppiamento alto, fragilità) ed è **fissata a compile-time**: non la cambi a programma in esecuzione.
- La composizione crea legami **deboli** (l'oggetto contenuto si usa solo tramite la sua interfaccia pubblica) ed è **flessibile a runtime**: puoi sostituire il pezzo contenuto con un altro. È la base di pattern come **Strategy**, che incapsula algoritmi intercambiabili in oggetti separati e li sostituisce a runtime (`se-patterns`).

Non significa "mai ereditarietà": significa che l'ereditarietà la usi quando la relazione "is-a" è genuina, mentre per il semplice riuso di funzionalità spesso la composizione è più sana.

## Cenni concreti: Java e Python

- **Java** — **tipizzato staticamente** (i tipi sono controllati dal compilatore, a compile-time, prima di eseguire). `class`, `extends` (ereditarietà), `implements` (interfacce), `abstract`, `interface`, `@Override`. Modificatori `private/protected/public` espliciti. Tutto è dentro classi.
- **Python** — più permissivo. Ereditarietà con `class Cane(Animale):`; niente `private` vero, per convenzione un attributo "privato" si prefissa con underscore (`_saldo`). L'override è naturale (ridefinisci il metodo), le classi astratte si fanno col modulo `abc` (*Abstract Base Classes*: `ABC`, `@abstractmethod`). Il polimorfismo è ancora più libero grazie al **duck typing**: "se cammina come un'anatra e fa qua-qua, è un'anatra", cioè conta che l'oggetto **abbia** il metodo, non il suo tipo dichiarato.

## Esempi concreti

Immagina il backend di un sistema di **ticket / segnalazioni** (come quelli su cui lavorerai: assistenza clienti, bug tracking).

- **Classe e incapsulamento.** Una classe `Segnalazione` ha attributi `private`: `id`, `titolo`, `stato`, `assegnatario`. Il campo `stato` non è pubblico: lo cambi solo via metodi come `prendiInCarico()` o `chiudi()`, che **controllano le transizioni valide** (non puoi chiudere una segnalazione mai aperta). Così la regola di business vive dentro l'oggetto e non la può aggirare nessuno.
- **Ereditarietà + override.** `Segnalazione` è astratta; da lei ereditano `Bug`, `RichiestaFunzionalità`, `DomandaCliente`. Tutte condividono `id`, `stato`, `assegna()`, ma ognuna fa **override** di `priorità()`: un `Bug` critico pesa più di una `DomandaCliente`.
- **Polimorfismo.** Il modulo che ordina la coda scorre una lista di `Segnalazione` e chiama `priorità()` su ciascuna senza sapere di che sottotipo sia: dynamic dispatch. Aggiungi domani `IncidenteSicurezza`: la coda lo gestisce senza modifiche.
- **Astrazione via interfaccia.** Un'interfaccia `Notificabile` con `inviaNotifica()` la implementano sia `Segnalazione` sia `Utente` sia `Report`: classi senza parentela, stessa capacità.

## Notable use case

- **Le Collezioni di Java (Java Collections Framework).** Esempio da manuale di astrazione e polimorfismo: `List` è un'**interfaccia** (il contratto: "sa aggiungere, leggere per indice, iterare"), e `ArrayList` e `LinkedList` sono due **implementazioni** diverse. Il tuo codice dichiara `List<String> lista = new ArrayList<>();`: lavora sul **tipo astratto** `List`, così puoi passare a `LinkedList` cambiando una sola riga. Tutto il resto resta uguale (programmare verso l'interfaccia, non l'implementazione).
- **I modelli nei framework.** In **Django** (Python) scrivi le tue **classi** modello che ereditano da `models.Model`: erediti gratis persistenza su database, validazione e serializzazione, e fai override solo di ciò che ti serve — ereditarietà in azione. In **Spring Data** (Java) la stessa comodità arriva via **interfacce**: dichiari un'interfaccia `repository` che estende `JpaRepository` e il framework ne genera da solo l'implementazione. L'OOP (ereditarietà e interfacce) è il linguaggio con cui questi framework ti parlano.

## Fonti

- **Oracle — The Java Tutorials, "Object-Oriented Programming Concepts"** (docs.oracle.com): definizioni ufficiali di classe, oggetto, ereditarietà, interfaccia, polimorfismo nel contesto Java.
- **Python Docs — "Classes"** (docs.python.org, tutorial sez. 9): classi, ereditarietà, override e convenzioni Python; modulo `abc` per le classi astratte.
- **"Design Patterns" (Gang of Four, 1994)** — origine del principio "favor object composition over class inheritance".
- **refactoring.guru** — catalogo illustrato dei design pattern, con spiegazioni visive di principi come "favor composition over inheritance" e pattern come Strategy.

## Concetti adiacenti

- **se-principles** — i principi SOLID e i sintomi del cattivo design (rigidità, fragilità, immobilità): poggiano direttamente sui quattro pilastri visti qui.
- **se-patterns** — i design pattern GoF (Strategy, Observer, Factory...): applicazioni concrete di polimorfismo, astrazione e composizione.
- **prog-ds** — strutture dati: liste, pile, code e mappe, spesso esposte in OOP come interfacce con più implementazioni (vedi le Collezioni Java).

## Quiz (10 — tutte rispondibili dalla lezione)

1. Qual è la differenza tra **classe** e **oggetto** (istanza)? Cosa vuol dire **istanziare**?
2. Cos'è l'**incapsulamento** e con quali strumenti (modificatori di accesso, getter/setter) si realizza?
3. **Perché** l'incapsulamento è utile? Fai l'esempio del saldo di un conto.
4. Cos'è l'**ereditarietà**, quale relazione esprime ("is-a") e a cosa servono `super` e l'**override**?
5. Qual è il **rischio** principale dell'ereditarietà e qual è la regola pratica per decidere se usarla?
6. Distingui **overriding** e **overloading**: quando avviene la scelta della versione in ciascuno dei due?
7. Cos'è il **dynamic dispatch**? Spiegalo con l'esempio della lista di `Animale`.
8. Differenza tra **classe astratta** e **interfaccia**, e **quando** preferire l'una all'altra.
9. Cos'è la **composizione** (relazione "has-a") e perché si dice **"favor composition over inheritance"**?
10. Perché le **Collezioni di Java** (`List` / `ArrayList`) sono un buon esempio di astrazione e polimorfismo?

<details><summary>Risposte</summary>

1. La **classe** è lo **stampo/progetto** (descrive quali dati e operazioni ha un tipo di cosa, la scrivi una volta); l'**oggetto** (o **istanza**) è l'**esemplare concreto** creato dalla classe, con valori propri e uno stato suo. **Istanziare** è creare un oggetto a partire dalla classe (in Java con `new`, in Python chiamando la classe).

2. L'**incapsulamento** è nascondere i dati interni di un oggetto e consentirne l'accesso solo tramite metodi pubblici controllati. Si realizza con i **modificatori di accesso** — `private` (solo dentro la classe), `public` (ovunque), `protected` (classe e sottoclassi) — tenendo gli attributi `private` e offrendo **getter** (leggono un attributo) e **setter** (lo modificano potendo validare il valore).

3. Perché **l'oggetto difende da solo le proprie regole** (invarianti): se chiunque potesse scrivere `conto.saldo = -5000` lo stato diventerebbe incoerente; tenendo `saldo` private e offrendo `preleva(importo)` che controlla la copertura, nessuno può portarlo in uno stato illegale. In più puoi cambiare l'implementazione interna senza rompere chi usa l'oggetto (basso accoppiamento).

4. L'**ereditarietà** permette a una classe (**sottoclasse**) di riutilizzare attributi e metodi di un'altra (**superclasse**). Esprime la relazione **"is-a"**: la sottoclasse è un caso particolare della superclasse (un Cane è un Animale). **`super`** richiama la superclasse (`super()` il suo costruttore, `super.metodo()` la sua versione del metodo); l'**override** è la ridefinizione di un metodo ereditato con un comportamento proprio.

5. Il rischio è l'**accoppiamento alto**: la sottoclasse dipende dai dettagli della superclasse, e un cambiamento nel genitore può rompere i figli (fragilità), inoltre si tende a usarla per puro riuso anche quando "is-a" non regge, creando gerarchie innaturali. Regola pratica: eredita **solo** se vale davvero "la sottoclasse *è un* tipo di superclasse".

6. **Overriding**: più sottoclassi ridefiniscono lo stesso metodo della superclasse; la scelta di quale versione eseguire avviene a **runtime** in base al tipo reale dell'oggetto (dynamic dispatch). **Overloading**: più metodi con lo stesso nome ma parametri diversi nella stessa classe; la scelta la fa il **compilatore** a compile-time in base agli argomenti. L'overloading non c'entra con l'ereditarietà.

7. Il **dynamic dispatch** (o late binding) è il meccanismo per cui, chiamando un metodo su una variabile di tipo base, viene eseguita a runtime la versione del **tipo reale** dell'oggetto. Esempio: una lista di `Animale` con cani e gatti; il ciclo chiama `a.verso()` e ciascun oggetto risponde con il proprio verso (Bau/Miao) senza che il codice sappia i tipi concreti; aggiungendo `Mucca` il ciclo funziona senza modifiche.

8. La **classe astratta** non è istanziabile e può avere **sia metodi implementati sia metodi astratti**, con stato condiviso: si usa per sottoclassi **parenti strette** ("is-a" forte) che condividono codice. L'**interfaccia** è un **puro contratto** di metodi, tradizionalmente senza implementazione e sempre senza stato d'istanza (da Java 8 può avere metodi `default` con un corpo): si usa per dare una **capacità** ("sa fare") a classi diverse e non imparentate. In Java si estende una sola classe ma si implementano molte interfacce.

9. La **composizione** è costruire un oggetto mettendogli **dentro** altri oggetti come attributi e delegando a loro (relazione **"has-a"**: un'Automobile ha un Motore). Si preferisce all'ereditarietà perché crea legami **deboli** (si usa solo l'interfaccia pubblica dell'oggetto contenuto) ed è **flessibile a runtime** (puoi sostituire il pezzo contenuto), mentre l'ereditarietà lega ai dettagli interni della superclasse ed è fissata a compile-time.

10. Perché `List` è un'**interfaccia** (il contratto di operazioni) e `ArrayList`/`LinkedList` ne sono due **implementazioni** diverse: dichiarando `List<String> lista = new ArrayList<>()` lavori sul tipo astratto, così puoi cambiare implementazione modificando una sola riga. È astrazione (programmi verso l'interfaccia) e polimorfismo (lo stesso codice funziona con implementazioni diverse) in azione.

</details>
