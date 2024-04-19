class UnitaImmobiliare:
    numUnitaImmobiliare = 0
    def __init__(self, foglio, subalterno, condomini, millesimi, particella, tipoUnitaImmobiliare):
        self.numUnitaImmobiliare += 1
        self.codice = self.numUnitaImmobiliare
        self.foglio = foglio
        self.subalterno = subalterno
        self.condomini = condomini
        self.millesimi = millesimi
        self.particella = particella
        self.tipoUnitaImmobiliare = tipoUnitaImmobiliare

    def getUnitaImmobiliare(self):
        return {
            "numUnitaImmobiliare": self.numUnitaImmobiliare,
            "codice": self.codice,
            "foglio": self.foglio,
            "subalterno": self.subalterno,
            "condomini": self.condomini,
            "milleismi": self.millesimi,
            "particella": self.particella,
            "tipoUnitaImmobiliare": self.tipoUnitaImmobiliare
        }