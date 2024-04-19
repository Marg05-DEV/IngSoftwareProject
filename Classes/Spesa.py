class Spesa:

    def __init__(self):
        self.descrizione = ""
        self.fornitore = None
        self.importo = 0
        self.dataScadenza = datetime.datetime(year=1970, month=1, day=1)
        self.immobile = None
        self.pagata = False
    def aggiungiSpesa(self, descrizione, fornitore, importo, dataScadenza, immobile, pagata):
        self.descrizione = descrizione
        self.fornitore = fornitore
        self.importo = importo
        self.dataScadenza = dataScadenza
        self.immobile = immobile
        self.pagata = pagata

    def getSpesa(self):
        return {
            "descrizione": self.descrizione,
            "fornitore": self.fornitore,
            "importo": self.importo,
            "dataScadenza": self.dataScadenza,
            "immobile": self.immobile,
            "pagata": self.pagata
        }
        