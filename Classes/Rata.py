class Rata:

    def __init__(self):
        self.codice = 0
    def aggiungiRata(self, codice):
        self.codice = codice

    def getRata(self):
        return {
            "codice": self.codice
        }