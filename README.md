Progetto di Ingegneria del Software di Acciarri Davide, Marcucci Giacomo e Carfagna Giorgio.
sviluppo di un software per la gestione del registro anagrafe condominiale e della contabilità condominiale.

# COSE DA FARE
## GENERALI
- Rivedere le dimensioni di Widget e altre cose;
- Migliorare i layout delle viste seguendo i mockup;
- Rivedere le scritte delle finestre (sopratutto i WindowTitle e i label dei campi di input)
- ~~Fare controlli quando si ricercano i proprietari e non sono presenti. Guarda il bilancio~~
- Controllare ogni volta che si fa una qualsiasi ricerca, che i bottoni si disattivino (basta mettere le disabilitazioni nelle funzioni collegate al signal) (per i tablewidget non dovrebbe servire)

## AREA IMMOBILI

## AREA REGISTRO ANAGRAFE

### UNITA IMMOBILIARI (ASSEGNAZIONI)

- ~~Vedere se mettere la dataContratto per gli inquilini come richiesto dal form del registro anagrafe~~

### CONDOMINI
*dovrebbe essere tutto corretto*

## AREA CONTABILITA
- Controlla cosa succede quando si visualizza una ricevuta per prelievo

### SPESE
*dovrebbe esser fatto*

### RATE
*dovrebbe esser fatto*

### STATO PATRIMONIALE e SALDO CASSA
*dovrebbe esser fatto*

## AREA BILANCIO

### TABELLE MILLESIMALI
- da fare test per il suo completo funzionamento (dovrebbe funzionare tutto)
- non dare possibilità di assegnare tipi di spesa già assegnati ad altre tabelle millesimali dello stesso immobile(fare ulteriori controlli su aggiungi tipo spesa, rimuovi tipo spesa)

### BILANCIO 

- rivedere i totali delle quote in ripartizione preventivo che sono uguali a quelle di ripartizioen consuntivo ( forse scambio di variabili )
- rivedere controlli bilancio, soprattutto le __date__ e rendere possibile l'approvazione del bilancio con dataApprovazione > di data fineEsercizio

## AREA DOCUMENTI

# FARE GLI UNIT TEST

- fatti per immobile. Fare per altre classi in modo analogo. FUNZIONANO

*attenzione a lanciarli partendo dalla cartella di progetto IngSoftProject e non da quella dei test*