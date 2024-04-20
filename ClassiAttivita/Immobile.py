class Immobile:

    def __init__(self):
        self.codice = 0
        self.sigla = ""
        self.denominazione = ""
        self.codiceFiscale = ""
    def aggiungiImmobile(self, codice, sigla, denominazione, codiceFiscale):
        self.codice = codice
        self.sigla = sigla
        self.denominazione = denominazione
        self.codiceFiscale = codiceFiscale

    def getImmobile(self):
        return{
            "codice": self.codice,
            "sigla": self.sigla,
            "denominazione": self.denominazione,
            "codiceFiscale": self.codiceFiscale
        }

    def ricercaImmobile(self):
        pass

