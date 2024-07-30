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
- Mettere DataPagamento = None in aggiungi spesa quando la spesa non è pagata e modificare visualizza spesa di conseguenza
- Aggiungere un reset dei soli dividendi in aggiungi spesa
- Rivedere il codice di modifica spesa per vedere se è tutto giusto
- Capire come risolvere checkbox pagata nelle spese

### RATE
- fare test sulle rate (dovrebbe funzionare tutto)

### STATO PATRIMONIALE e SALDO CASSA
- vedere selezione tipo ricerca in debito fornitore
- rivedere saldo cassa e debito immobile 
- fare credito condomino e correggere stato patrimoniale immobile dopo aver fatto il bilancio

## AREA BILANCIO

### TABELLE MILLESIMALI
- da fare test per il suo completo funzionamento (dovrebbe funzionare tutto)
- non dare possibilità di assegnare tipi di spesa già assegnati ad altre tabelle millesimali dello stesso immobile

### BILANCIO

*praticamente da iniziare (fatta parte gestione esercizi di un immobile)*

- nella creazione nuovo esercizio togliere controllo distanza di un anno (si potrebbe stabilire la data di fine automatica dopo aver inserito la data di inizio (data fine = data inizio  + 1 anno - 1 giorno))
- controllo esercizio già esistente nelle date inserite
- punti precedenti fatti ma capire come fare meglio i controlli
- per i prospetti capire come mettere colonne unite si una tabella

## AREA DOCUMENTI

*da fare*

# FARE GLI UNIT TEST
