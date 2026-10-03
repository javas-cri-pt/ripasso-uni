---
day: 22
topic_id: xc-pm-metrics
title: "Metriche di prodotto — North Star, AARRR, funnel, retention"
area: cross-cutting
course: Product Management
grounded_in: "POLITO Decision Making & AI for Business + lavoro reale (MaiCare, Samec)"
adjacent: [xc-pm-prioritization, dm-analysis, xc-pm-experiment, bp-financials]
completeness_checked: true
quiz_count: 10
rule: "Ogni cosa che il quiz chiede è spiegata per esteso nel corpo."
---

# Metriche di prodotto — North Star, AARRR, funnel, retention

> **Perché oggi:** un Product (o Project) Manager decide con i **numeri giusti**. Sapere quali metriche contano, e soprattutto quali **ingannano**, è chiesto ai colloqui di prodotto e ti serve per ragionare MaiCare o un business plan come Samec: non "quanti utenti", ma "quanti **tornano** e **creano valore**".

## Il principio: misura il valore, non la vanità
Una **vanity metric** (metrica di vanità) è un numero che **sale e fa sentire bene ma non guida decisioni**: download totali, iscritti totali, follower, page view. Cresce quasi sempre e non ti dice se il prodotto **funziona**. L'opposto è una **actionable metric** (metrica azionabile): legata a un comportamento di valore, confrontabile nel tempo, e che se cambia ti dice **cosa fare**. Regola pratica: se una metrica "solo può salire" (cumulativa), diffida; guarda i **tassi** e le **coorti**.

## North Star Metric (la stella polare)
La **North Star Metric (NSM)** è **l'unica metrica** che cattura meglio il **valore che consegni all'utente**, scelta perché la sua crescita **trascina** la crescita sana del business. Esempi noti: per Airbnb *notti prenotate*, per Spotify *tempo di ascolto*, per WhatsApp *messaggi inviati*. Non è il fatturato (è una conseguenza) né i download (è vanità): è il **momento di valore ripetuto**. Serve a **allineare** il team su una direzione sola invece di ottimizzare metriche scollegate.

## AARRR — l'imbuto del ciclo di vita utente
**AARRR** ("Pirate Metrics", di Dave McClure) scompone il percorso dell'utente in **cinque stadi**, ognuno con la sua metrica. Ti dice **dove** stai perdendo persone.

<svg viewBox="0 0 620 250" style="max-width:100%;height:auto;font-family:inherit">
  <g font-size="12.5" fill="var(--ink)">
    <polygon points="60,26 560,26 500,66 120,66" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/>
    <text x="310" y="51" text-anchor="middle" font-weight="700">Acquisition — come ti trovano</text>
    <polygon points="120,70 500,70 462,110 158,110" fill="var(--card)" stroke="var(--rule)"/>
    <text x="310" y="95" text-anchor="middle" font-weight="700">Activation — primo "aha", valore subito</text>
    <polygon points="158,114 462,114 424,154 196,154" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/>
    <text x="310" y="139" text-anchor="middle" font-weight="700">Retention — tornano (la più importante)</text>
    <polygon points="196,158 424,158 386,198 234,198" fill="var(--card)" stroke="var(--rule)"/>
    <text x="310" y="183" text-anchor="middle" font-weight="700">Revenue — pagano</text>
    <polygon points="234,202 386,202 348,240 272,240" fill="var(--card)" stroke="var(--rule)"/>
    <text x="310" y="226" text-anchor="middle" font-weight="700">Referral — invitano</text>
  </g>
  <text x="588" y="130" text-anchor="middle" font-size="11" fill="var(--muted)" transform="rotate(90 588 130)">meno persone a ogni stadio</text>
</svg>

I cinque stadi (ognuno spiegato):
1. **Acquisition (acquisizione):** come le persone **arrivano** (ricerca, passaparola, ads). Metrica tipica: visitatori/nuovi utenti per canale, e il **CAC** (*Customer Acquisition Cost*, quanto costa acquisire un cliente).
2. **Activation (attivazione):** l'utente raggiunge il primo **"aha moment"**, cioè prova il valore vero abbastanza presto da capire perché resterebbe. Metrica: % di nuovi che completano l'azione-chiave (es. per un gestionale, "ha creato il primo progetto").
3. **Retention (retention):** **tornano** a usarlo nel tempo. È lo stadio **più importante**: senza retention riempi un secchio bucato, ogni acquisizione evapora.
4. **Revenue (ricavo):** monetizzi (abbonamento, transazione). Metriche: tasso di conversione a pagante, **LTV** (*Lifetime Value*, valore totale che un cliente porta nella sua vita).
5. **Referral (passaparola):** gli utenti **invitano** altri, chiudendo un loop di crescita. Metrica: quanti nuovi utenti genera in media un utente esistente.

## Retention e funnel (i due strumenti che userai di più)
**Funnel (imbuto):** una sequenza di passi verso un obiettivo (es. *visita → registrazione → primo progetto → invito*), dove misuri **quanti passano** da un passo al successivo. Serve a **trovare il buco**: se il 70% si registra ma solo il 10% attiva, il problema è l'onboarding, non l'acquisizione. Ottimizzi lo **step peggiore**, non a caso.

**Retention e coorti:** la **retention** è la % di utenti ancora attivi dopo N giorni/settimane. Si legge per **coorte** (*cohort*): raggruppi gli utenti per **quando** sono entrati (es. "iscritti di marzo") e ne segui il comportamento nel tempo. Così confronti mele con mele e vedi se le modifiche al prodotto migliorano davvero chi è entrato **dopo**. La **curva di retention** che si **appiattisce** su un valore positivo (invece di scendere a zero) è il segnale di **product-market fit**: esiste uno zoccolo di utenti a cui il prodotto serve sul serio.

Metriche di attività di supporto: **DAU / MAU** (*Daily / Monthly Active Users*, utenti attivi al giorno/mese) e il loro rapporto **DAU/MAU** come proxy di "quanto è appiccicoso" il prodotto (0,5 = l'utente medio lo usa metà dei giorni del mese). Da sole non bastano: vanno lette con la retention per coorte.

## Esempio concreto (roba tua)
Per **MaiCare**, la NSM sensata non è "download" ma qualcosa come *sintomi tracciati per paziente attivo a settimana*: cattura il valore ripetuto (la paziente torna e registra), che a sua volta trascina fidelizzazione dei medici e dati per la ricerca. L'imbuto AARRR ti dice dove intervenire: se l'**activation** (prima settimana di tracking) è bassa, lavori sull'onboarding prima di spendere in acquisizione. In un business plan come **Samec**, le stesse metriche entrano nel modello: CAC e LTV decidono se l'unit economics regge (`LTV > CAC`).

## Completeness check (integrato da me)
- **La gerarchia giusta:** una **NSM** in cima, scomposta in pochi **driver** (input metrics) su cui il team può agire direttamente; sotto, metriche di guardia (**guardrail metrics**) che non devono peggiorare mentre spingi la NSM (es. non gonfiare l'uso peggiorando la soddisfazione).
- **Leading vs lagging:** metriche **leading** (anticipatrici, es. attivazione) predicono le **lagging** (di risultato, es. ricavo). Guidi con le leading perché le lagging arrivano quando è tardi.
- **Il legame coi soldi:** LTV e CAC (giorno 17, financials) sono il ponte tra prodotto e sostenibilità: un imbuto sano è quello dove `LTV > CAC` con margine.

## Fonti
- **Lenny's Newsletter** — lennysnewsletter.com (metriche di prodotto, esempi reali)
- **Amplitude — North Star Playbook** (amplitude.com)
- **"Lean Analytics"**, Croll & Yoskovitz (quale metrica in quale fase)

## Concetti adiacenti
- `xc-pm-prioritization` — RICE, MoSCoW (decidere cosa fare con questi numeri)
- `xc-pm-experiment` — A/B testing e build-measure-learn (muovere le metriche)
- `bp-financials` — CAC, LTV, unit economics (il lato soldi del funnel)

## Quiz (10 — tutte rispondibili dalla lezione)
1. Cos'è una **vanity metric** e perché è pericolosa? Fai un esempio.
2. Cos'è la **North Star Metric** e perché non è il fatturato né i download?
3. Cosa significa l'acronimo **AARRR** (i cinque stadi)?
4. Cos'è l'**activation** e l'**"aha moment"**?
5. Perché la **retention** è definita lo stadio più importante?
6. A cosa serve un **funnel** e come lo usi per decidere dove intervenire?
7. Cos'è una **coorte** e perché si legge la retention per coorte?
8. Cosa indica una **curva di retention che si appiattisce** su un valore positivo?
9. Cosa sono **DAU/MAU** e cosa misura il loro rapporto?
10. Differenza tra metriche **leading** e **lagging** e perché si guida con le leading?

<details><summary>Risposte</summary>

1. Un numero che **sale e gratifica ma non guida decisioni** (es. download totali, follower): cresce quasi sempre e non dice se il prodotto funziona.
2. L'**unica metrica** che cattura il **valore ripetuto** consegnato all'utente e ne trascina la crescita sana; il fatturato è una **conseguenza** e i download sono **vanità**.
3. **Acquisition, Activation, Retention, Revenue, Referral** (acquisizione, attivazione, retention, ricavo, passaparola).
4. L'**attivazione** è quando il nuovo utente raggiunge il primo momento di valore (**"aha"**) abbastanza presto da capire perché resterebbe.
5. Perché senza retention **ogni acquisizione evapora** (secchio bucato): è la base su cui poggiano ricavo e passaparola.
6. Misura **quanti utenti passano** da un passo al successivo; individui lo **step peggiore** e ottimizzi quello invece di intervenire a caso.
7. Una **coorte** raggruppa gli utenti per **quando sono entrati**; leggerla per coorte confronta gruppi omogenei e mostra se le modifiche migliorano chi entra **dopo**.
8. **Product-market fit**: esiste uno zoccolo di utenti a cui il prodotto serve davvero (la retention non scende a zero).
9. **Daily/Monthly Active Users** (utenti attivi al giorno/mese); il rapporto **DAU/MAU** misura quanto è "appiccicoso" il prodotto.
10. Le **leading** anticipano (es. attivazione), le **lagging** sono di risultato (es. ricavo); si guida con le leading perché le lagging arrivano quando è **troppo tardi** per correggere.
</details>
