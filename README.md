Progetto di Ingegneria del Software di Acciarri Davide, Marcucci Giacomo e Carfagna Giorgio.
sviluppo di un software per la gestione del registro anagrafe condominiale e della contabilità condominiale.

# COSE DA FARE
## GENERALI
- Rivedere le dimensioni di Widget e altre cose;
- Migliorare i layout delle viste seguendo i mockup;
- Rivedere le scritte delle finestre (sopratutto i WindowTitle e i label dei campi di input)
- Fare controlli quando si ricercano i proprietari e non sono presenti. Guarda il bilancio
- Controllare ogni volta che si fa una qualsiasi ricerca, che i bottoni si disattivino (basta mettere le disabilitazioni nelle funzioni collegate al signal) (per i tablewidget non dovrebbe servire)

## AREA IMMOBILI

## AREA REGISTRO ANAGRAFE

### UNITA IMMOBILIARI (ASSEGNAZIONI)

- Vedere se mettere la dataContratto per gli inquilini come richiesto dal form del registro anagrafe

### CONDOMINI
*dovrebbe essere tutto corretto*

## AREA CONTABILITA
- Controlla cosa succede quando si visualizza una ricevuta per prelievo

### SPESE
- Aggiungere un reset dei soli dividendi in aggiungi spesa
- Rivedere il codice di modifica spesa per vedere se è tutto giusto

### RATE
- fare test sulle rate (dovrebbe funzionare tutto)

### STATO PATRIMONIALE e SALDO CASSA

- Impostare il treeWidget in creditoCondomino e forse in StatoPatrimoniale
- In stato patrimoniale e altri fare controlli: esempio gestire esistenza o meno dell'ultimo bilancio, propretario assente o dizionari non completi: esempio chiave = codice unità immobiliare mancante
- Controllo generale
- In credito condomino migliorare ricerca condomino con possibili colonne per il combo box (colonna per Cf e una per nome cognome. Così da risolvere omonimi)
## AREA BILANCIO

### TABELLE MILLESIMALI
- da fare test per il suo completo funzionamento (dovrebbe funzionare tutto)
- non dare possibilità di assegnare tipi di spesa già assegnati ad altre tabelle millesimali dello stesso immobile(fare ulteriori controlli su aggiungi tipo spesa, rimuovi tipo spesa)

### BILANCIO

- mettere la possibilità di modificare le rate preventivate con una funzione di adattamento
- mettere la data di scadenza delle rate preventivate
- fatti i due punti precedenti modificare il pdf dei prospetti 
- rivedere controlli bilancio, soprattutto le date e rendere possibile l'approvazione del bilancio con dataApprovazione > di data fineEsercizio

## AREA DOCUMENTI

# FARE GLI UNIT TEST

- fatti per immobile. Fare per altre classi in modo analogo. FUNZIONANO

*attenzione a lanciarli partendo dalla cartella di progetto IngSoftProject e non da quella dei test*