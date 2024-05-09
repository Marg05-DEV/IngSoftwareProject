class spesaPreventivata:

    def __init__(self):
        self.codice = 0
        self.importo = 0.0
        self.tipologia = None

    def aggiungiSpesaPreventivata(self, codice, importo, tipologia):
        self.codice = codice
        self.importo = importo
        self.tipologia = tipologia




    def getSpetaPreventivata(self):
        return {
            "codice": self.codice,
            "importo": self.importo,
            "tipologia": self.tipologia
        }
