class Spesa:
    def __init__(self, descrizione, fornitore, importo, dataScadenza, immobile, pagata):
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
        