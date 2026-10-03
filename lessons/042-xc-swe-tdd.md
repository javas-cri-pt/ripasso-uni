---
day: 42
topic_id: xc-swe-tdd
title: "Strategia di test: unit/integration/e2e, TDD, mocking, test pyramid"
area: cross-cutting
course: "Software Engineering (craft del lavoro)"
grounded_in: null
adjacent: [se-testing, prog-testing, xc-swe-clean, xc-swe-refactor]
completeness_checked: true
quiz_count: 10
---

# Strategia di test: unit/integration/e2e, TDD, mocking, test pyramid

> **Perché oggi:** scrivere codice che funziona è metà del mestiere; l'altra metà è **dimostrare** che funziona e accorgersi quando qualcosa lo rompe. Una buona strategia di test è ciò che permette di cambiare il codice senza paura, ed è esattamente quello che SOLID e il clean code di `xc-swe-clean` rendono possibile (una classe con le dipendenze iniettate è una classe facile da testare). Nei colloqui tecnici tornano quasi sempre domande su TDD, mock e piramide dei test. Qui vediamo i tipi di test, come comporli, il ciclo TDD, i vari "test double" e l'errore classico del mocking.

## I tre livelli di test
Si distinguono i test per **quanto** sistema mettono alla prova in una volta.

- **Unit test (test di unità):** verificano **una singola unità** in isolamento (una funzione, una classe), senza toccare database, rete o filesystem. Sono **piccoli, velocissimi** (migliaia in pochi secondi) e, quando falliscono, dicono con precisione **dove** è il problema.
- **Integration test (test di integrazione):** verificano che **più componenti collaborino** correttamente, es. il codice più un vero database o una vera API. Sono più lenti e più fragili degli unit, ma colgono i bug che stanno **tra** i pezzi (uno schema sbagliato, un contratto frainteso) che gli unit, isolando tutto, non vedono.
- **End-to-end test (E2E, "da un capo all'altro"):** verificano un **intero flusso** dal punto di vista dell'utente, es. un browser che clicca sul sito reale dal login al pagamento. Sono i più realistici ma anche i più **lenti, costosi e fragili** (si rompono per un bottone spostato).

## La piramide dei test
La **piramide dei test** (resa popolare da Mike Cohn) è una regola su **quante** prove scrivere di ciascun tipo. La forma è quella di una piramide:

- **Base larga: molti unit test** (veloci ed economici).
- **Mezzo: alcuni integration test.**
- **Punta stretta: pochi E2E** (lenti e costosi), solo per i percorsi critici.

L'idea è spingere la maggior parte delle verifiche verso il basso, dove i test sono veloci e precisi, e tenere in cima solo il minimo indispensabile. L'**anti-pattern** si chiama **"cono gelato" (ice-cream cone):** la piramide capovolta, tanti E2E manuali o automatici in cima e pochissimi unit alla base. Risultato: una suite lenta, instabile e che, quando è rossa, non ti dice dove guardare.

<figure style="margin:18px 0;text-align:center">
<svg viewBox="0 0 640 260" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12" fill="var(--ink)" text-anchor="middle">
    <polygon points="250,30 330,30 390,100 190,100" fill="var(--card)" stroke="var(--accent)" stroke-width="1.7"/>
    <text x="290" y="72" font-size="11.5">E2E</text><text x="290" y="88" font-size="9.5" fill="var(--muted)">pochi</text>
    <polygon points="190,104 390,104 445,174 135,174" fill="var(--card)" stroke="var(--rule)"/>
    <text x="290" y="142" font-size="11.5">Integration</text><text x="290" y="158" font-size="9.5" fill="var(--muted)">alcuni</text>
    <polygon points="135,178 445,178 500,248 80,248" fill="var(--card2)" stroke="var(--rule)"/>
    <text x="290" y="214" font-size="11.5">Unit</text><text x="290" y="230" font-size="9.5" fill="var(--muted)">molti, veloci</text>
  </g>
  <g font-size="10.5" fill="var(--muted)">
    <text x="560" y="60">più lenti</text>
    <text x="560" y="74">più costosi</text>
    <text x="560" y="222">più veloci</text>
    <text x="560" y="236">più economici</text>
  </g>
  <g stroke="var(--muted)" stroke-width="1.2" fill="none" marker-end="url(#arr-tdd)">
    <path d="M530,95 L530,205"/>
  </g>
  <text x="530" y="150" font-size="9.5" fill="var(--muted)" transform="rotate(90 530 150)">realismo ↑ / velocità ↓</text>
  <defs><marker id="arr-tdd" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="var(--muted)" stroke-width="1.4"/></marker></defs>
</svg>
<figcaption style="font-size:12px;color:var(--muted);margin-top:4px">La piramide dei test: molti unit alla base (veloci, economici, precisi), alcuni integration nel mezzo, pochi E2E in cima (realistici ma lenti e fragili). Capovolgerla è l'anti-pattern "cono gelato".</figcaption>
</figure>

## TDD: il ciclo red-green-refactor
Il **TDD** (*Test-Driven Development*, "sviluppo guidato dai test") ribalta l'ordine: **prima il test, poi il codice**. Il ciclo ha tre passi, spesso detto **red-green-refactor**:

1. **Red (rosso):** scrivi un test per un comportamento che **non esiste ancora**. Lo esegui e **fallisce** (rosso). Questo dimostra che il test misura davvero qualcosa.
2. **Green (verde):** scrivi il **minimo** codice che fa passare il test (verde), anche brutto.
3. **Refactor:** ora che la rete di sicurezza è verde, **pulisci** il codice (nomi, duplicazione, struttura) senza cambiarne il comportamento, e ri-esegui i test per confermare che restano verdi.

Vantaggi: il design nasce **testabile** (sei costretta a pensare all'interfaccia prima dell'implementazione), hai una suite di regressione fin da subito, e il test funge da **specifica eseguibile** di cosa deve fare il codice.

## La struttura di un buon test: AAA e FIRST
Un test leggibile segue lo schema **AAA (Arrange, Act, Assert)**: **Arrange** prepara i dati e il contesto, **Act** esegue l'azione da testare (idealmente una sola), **Assert** verifica il risultato atteso. Tre blocchi chiari, in quest'ordine.

```python
def test_sconto_premium():
    # Arrange
    sconto = Premium()
    # Act
    risultato = sconto.applica(100)
    # Assert
    assert risultato == 90
```

I buoni unit test rispettano l'acronimo **FIRST**:
- **Fast:** veloci (girano a ogni salvataggio).
- **Isolated / Independent:** indipendenti l'uno dall'altro e non dipendono dall'ordine di esecuzione.
- **Repeatable:** danno lo stesso esito ovunque e sempre (niente data di oggi, niente rete).
- **Self-validating:** passano o falliscono da soli, senza ispezione manuale dell'output.
- **Timely:** scritti al momento giusto (con TDD, prima del codice).

## Test double: dummy, stub, fake, spy, mock
Per isolare l'unità sotto test dalle sue dipendenze (database, rete, orologio) si usano i **test double** ("controfigure"): oggetti finti messi al posto di quelli veri. La tassonomia classica è di **Gerard Meszaros**:

- **Dummy:** un oggetto passato solo per **riempire** un parametro, mai davvero usato (es. un utente fittizio richiesto dalla firma ma ignorato dal test).
- **Stub:** fornisce **risposte predefinite** alle chiamate (es. `get_prezzo()` che restituisce sempre `10`). Serve a **pilotare l'input** indiretto dell'unità.
- **Fake:** un'implementazione **funzionante ma semplificata**, inadatta alla produzione (es. un database in memoria con un dizionario al posto di Postgres). Fa il lavoro davvero, ma in modo leggero.
- **Spy:** come uno stub, ma **registra** come è stato chiamato (quali argomenti, quante volte), così puoi verificarlo dopo.
- **Mock:** un double **pre-programmato con aspettative**: sa in anticipo quali chiamate deve ricevere e **fallisce il test** se non arrivano come previsto. La differenza chiave: lo stub verifica lo **stato** (il risultato), il mock verifica il **comportamento** (che una certa chiamata sia avvenuta).

In pratica, nel codice e nei colloqui, "mock" si usa spesso come termine generico per tutti; ma sapere la distinzione (stato contro comportamento) è una domanda frequente.

## L'errore classico del mocking: dove applicare la patch
Negli strumenti come `unittest.mock` di Python si "sostituisce" temporaneamente un oggetto con `patch("percorso.del.nome")`. La regola d'oro, che quasi tutti sbagliano la prima volta: **si applica la patch dove il nome viene cercato, non dove è definito.** Se il modulo `ordini.py` scrive `from pagamenti import addebita` e poi usa `addebita(...)`, quel nome ora vive come `ordini.addebita`: devi scrivere `patch("ordini.addebita")`, **non** `patch("pagamenti.addebita")`. Patchare l'origine non ha effetto, perché `ordini` ha già la propria referenza al nome importato. Sbagliare questo è la causa numero uno di mock "che non funzionano".

## Un caveat onesto: copertura non è correttezza
La **code coverage** (copertura) misura **quale percentuale** del codice viene eseguita dai test. È utile per **trovare i buchi** (codice mai toccato da nessun test), ma non misura la qualità: un test che esegue una funzione senza **nessuna assert** significativa conta come "coperta" pur non verificando niente. Il 100% di copertura con assert deboli dà **falsa sicurezza**. La copertura dice cosa *non* è testato, non che ciò che è testato sia *giusto*.

## Esempi concreti
- **Dependency injection = testabilità (collega `xc-swe-clean`).** Una classe che riceve il `db` dal costruttore (DIP) si testa passandole un **fake** in memoria: niente database vero, test in millisecondi. Se invece fa `self.db = Postgres()` dentro di sé, sei costretta a un integration test lento.
- **Stub dell'orologio per test ripetibili (la R di FIRST).** Una funzione che usa `datetime.now()` non è ripetibile (il risultato cambia ogni giorno). Si inietta una sorgente di tempo e nel test le si passa uno **stub** che restituisce una data fissa.
- **Il contratto che solo l'integration coglie.** Due unit test verdi su due moduli non garantiscono che insieme funzionino: se uno manda un campo `userId` e l'altro si aspetta `user_id`, serve un **integration test** per scoprirlo.

## Notable use case
- **Google e la piramide.** Google documenta pubblicamente la pratica di molti test piccoli e pochi grandi (la classificazione small/medium/large), per tenere la suite veloce e stabile su una base di codice enorme.
- **CI che blocca il merge.** Nei progetti open source e aziendali la test-suite gira in **continuous integration** a ogni pull request: se i test sono rossi, il merge è bloccato. È la piramide che diventa un cancello automatico sulla qualità.
- **`pytest` e `unittest.mock` in Python.** L'ecosistema Python standard offre `unittest`/`pytest` per scrivere i test e `unittest.mock` (con `patch` e `MagicMock`) per i double: sono gli strumenti con cui si mette in pratica tutto quanto sopra.

## Fonti
- **Kent Beck** — *Test-Driven Development: By Example* (il testo che ha reso popolare il TDD e il ciclo red-green-refactor)
- **Gerard Meszaros** — *xUnit Test Patterns* e xunitpatterns.com (la tassonomia dei test double)
- **Martin Fowler** — martinfowler.com/articles/mocksArentStubs.html e l'articolo sulla Test Pyramid
- **Documentazione Python** — docs.python.org/3/library/unittest.mock.html

## Concetti adiacenti
- `se-testing` — testing e qualità del software nella trattazione universitaria (tecniche black-box/white-box, copertura)
- `prog-testing` — unit test e JUnit, il testing dal lato pratico della programmazione
- `xc-swe-clean` — clean code e SOLID: le dipendenze iniettate (DIP) sono ciò che rende il codice testabile
- `xc-swe-refactor` — il passo "refactor" del ciclo TDD: la rete di test verdi è ciò che permette di rifattorizzare senza paura

## Quiz (10 — tutte rispondibili dalla lezione)
1. Qual è la differenza tra **unit**, **integration** ed **E2E** test in termini di cosa mettono alla prova e di velocità/costo?
2. Cosa prescrive la **piramide dei test** riguardo a quanti test di ciascun tipo scrivere?
3. Cos'è l'anti-pattern **"cono gelato"** e perché è un problema?
4. Descrivi il ciclo **red-green-refactor** del TDD, passo per passo.
5. Cita un vantaggio concreto dello scrivere il test **prima** del codice.
6. Cosa significa lo schema **AAA** in un test?
7. Cosa dice l'acronimo **FIRST**? Spiega almeno la "F" e la "R".
8. Qual è la differenza tra uno **stub** e un **mock** (cosa verifica ciascuno)?
9. Enuncia la regola "**patcha dove il nome viene cercato, non dove è definito**" con l'esempio `from pagamenti import addebita` usato in `ordini.py`.
10. Perché una **copertura** del 100% non garantisce che il codice sia corretto?

<details><summary>Risposte</summary>

1. **Unit:** una singola unità in isolamento, piccoli e velocissimi, dicono con precisione dove è il bug. **Integration:** più componenti insieme (es. codice + vero database), più lenti/fragili, colgono i bug *tra* i pezzi. **E2E:** un intero flusso dal punto di vista dell'utente, i più realistici ma i più lenti, costosi e fragili.
2. Molti **unit** alla base (veloci ed economici), **alcuni integration** nel mezzo, **pochi E2E** in punta (lenti e costosi), solo per i percorsi critici: la maggior parte delle verifiche in basso.
3. È la piramide **capovolta**: tanti E2E in cima e pochissimi unit alla base. Problema: suite lenta, instabile e che quando è rossa non dice dove guardare.
4. **Red:** scrivi un test per un comportamento che non esiste ancora e lo vedi **fallire**. **Green:** scrivi il minimo codice per farlo **passare**. **Refactor:** con i test verdi, pulisci il codice senza cambiarne il comportamento e ri-esegui i test.
5. Il design nasce **testabile** (pensi all'interfaccia prima dell'implementazione); in più hai subito una suite di regressione e il test è una **specifica eseguibile**. (Basta uno di questi.)
6. **Arrange** (prepara dati/contesto), **Act** (esegui l'azione da testare, idealmente una sola), **Assert** (verifica il risultato atteso).
7. **Fast, Isolated/Independent, Repeatable, Self-validating, Timely.** F: veloci, girano a ogni salvataggio. R: ripetibili, stesso esito ovunque e sempre (niente data di oggi o rete).
8. Lo **stub** fornisce risposte predefinite e si verifica lo **stato** (il risultato finale); il **mock** è pre-programmato con aspettative e verifica il **comportamento** (che una certa chiamata sia avvenuta come previsto), facendo fallire il test altrimenti.
9. Quando `ordini.py` fa `from pagamenti import addebita`, il nome vive come `ordini.addebita`: la patch va su **`ordini.addebita`** (dove viene cercato/usato), non su `pagamenti.addebita` (dove è definito), altrimenti non ha effetto perché `ordini` ha già la propria referenza al nome importato.
10. Perché la **copertura** misura solo *quale* codice viene eseguito, non se le **assert** verificano le cose giuste: un test che esegue una funzione senza assert significative conta come "coperta" senza controllare nulla. Dà falsa sicurezza; dice cosa non è testato, non che il testato sia corretto.
</details>

## Esercizi
1. **Scrivi un test con uno stub + verifica di comportamento.** La classe `Checkout` dipende da un `gateway` di pagamento iniettato. Scrivi (con `unittest.mock`) un test che: pilota `gateway.addebita` a restituire `True` (stub), chiama `paga(100)`, verifica che il risultato sia `"ok"` **e** che `gateway.addebita` sia stato chiamato una volta con `100` (spy/mock).
   ```python
   class Checkout:
       def __init__(self, gateway):
           self.gateway = gateway
       def paga(self, importo):
           if self.gateway.addebita(importo):
               return "ok"
           return "fallito"
   ```
2. **Correggi la patch sbagliata.** Il test seguente non sostituisce davvero la funzione e chiama la rete vera. Il modulo `report.py` contiene `from meteo import temperatura_attuale` e la usa dentro `riassunto()`. Correggi il target della patch.
   ```python
   # report.py
   from meteo import temperatura_attuale
   def riassunto():
       return f"Ora ci sono {temperatura_attuale()} gradi"

   # test
   from unittest.mock import patch
   import report
   def test_riassunto():
       with patch("meteo.temperatura_attuale", return_value=20):  # <-- sbagliato
           assert report.riassunto() == "Ora ci sono 20 gradi"
   ```
3. **TDD in miniatura.** Devi scrivere una funzione `fizzbuzz(n)` che restituisce `"Fizz"` se `n` è divisibile per 3, `"Buzz"` se per 5, `"FizzBuzz"` se per entrambi, altrimenti la stringa del numero. Scrivi prima **tre test** (red) che coprano i casi, poi l'implementazione minima (green).

<details><summary>Soluzioni</summary>

1. Uso un `MagicMock` come gateway: ne pilsto il valore di ritorno (stub) e poi ne ispeziono le chiamate (verifica di comportamento).
   ```python
   from unittest.mock import MagicMock
   def test_paga_ok():
       gateway = MagicMock()
       gateway.addebita.return_value = True        # stub: risposta predefinita
       checkout = Checkout(gateway)
       assert checkout.paga(100) == "ok"           # verifica di stato
       gateway.addebita.assert_called_once_with(100)  # verifica di comportamento
   ```
2. Il nome è usato in `report`, quindi vive come `report.temperatura_attuale`: la patch va su quel target.
   ```python
   def test_riassunto():
       with patch("report.temperatura_attuale", return_value=20):  # dove viene cercato
           assert report.riassunto() == "Ora ci sono 20 gradi"
   ```
3. Prima i test (falliscono perché `fizzbuzz` non esiste ancora), poi l'implementazione minima.
   ```python
   def test_fizz():     assert fizzbuzz(9)  == "Fizz"
   def test_buzz():     assert fizzbuzz(10) == "Buzz"
   def test_fizzbuzz(): assert fizzbuzz(15) == "FizzBuzz"
   def test_numero():   assert fizzbuzz(7)  == "7"

   def fizzbuzz(n):
       if n % 15 == 0: return "FizzBuzz"
       if n % 3 == 0:  return "Fizz"
       if n % 5 == 0:  return "Buzz"
       return str(n)
   ```
   Nota: il caso divisibile per entrambi (15) va controllato **per primo**, altrimenti `n % 3` lo intercetterebbe prima e restituirebbe solo `"Fizz"`.
</details>
