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

