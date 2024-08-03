Progetto di Ingegneria del Software di Acciarri Davide, Marcucci Giacomo e Carfagna Giorgio.
sviluppo di un software per la gestione del registro anagrafe condominiale e della contabilità condominiale.

# COSE DA FARE
## GENERALI
- Rivedere le dimensioni di Widget e altre cose;
- Migliorare i layout delle viste seguendo i mockup;
- Rivedere le scritte delle finestre (sopratutto i WindowTitle e i label dei campi di input)

## AREA IMMOBILI
- controlli mancanti su modifica Immobile (stessa denominazione, codice, sigla, CF, ...)
- ricontrollare quando si abilita/disabilita i bottoni delle azioni CRUD

## AREA REGISTRO ANAGRAFE

### UNITA IMMOBILIARI (ASSEGNAZIONI)

- Vedere in particolare dimensioni bottoni gestione reg. anagrafe quando non ci sono assegnazioni (Aggiungi assegnazione, visualizza assegnazione. Ci sono i QSpacer)
- Vedere se mettere la dataContratto per gli inquilini come richiesto dal form del registro anagrafe
- vedere perchè non scompare msg = "unità immobiliari non corrispondenti alla ricerca" (da cambiare anche) quando la ricerca non è più attiva
- vedere il reset modifica unità immobiliare

### CONDOMINI
*dovrebbe essere tutto corretto*

## AREA CONTABILITA

### SPESE
- Aggiungere un reset dei soli dividendi in aggiungi spesa
- Rivedere il codice di modifica spesa per vedere se è tutto giusto
- Capire come risolvere checkbox pagata nella lista di gestione spese

### RATE
- fare test sulle rate (dovrebbe funzionare tutto)

### STATO PATRIMONIALE e SALDO CASSA

- Impostare il treeWidget in creditoCondomino e forse in StatoPatrimoniale
- Controllo generale

## AREA BILANCIO

### TABELLE MILLESIMALI
- da fare test per il suo completo funzionamento (dovrebbe funzionare tutto)
- non dare possibilità di assegnare tipi di spesa già assegnati ad altre tabelle millesimali dello stesso immobile(fare ulteriori controlli su aggiungi tipo spesa, rimuovi tipo spesa)

### BILANCIO

- fare prospetti per esercizi con il PDF
- rivedere controlli bilancio, soprattutto le date e rendere possibile l'approvazione del bilancio con dataApprovazione > di data fineEsercizio

## AREA DOCUMENTI

*da fare*

# FARE GLI UNIT TEST

*da fare*