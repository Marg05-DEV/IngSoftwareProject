class Immobile:
    def __init__(self, codice, sigla, denominazione, codiceFiscale):
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