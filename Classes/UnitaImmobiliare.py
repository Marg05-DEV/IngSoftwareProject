class UnitaImmobiliare:
    numUnitaImmobiliare = 0
    def __init__(self, foglio, subalterno):
        self.numUnitaImmobiliare += 1
        self.codice = self.numUnitaImmobiliare
        self.foglio = foglio
        self.subalterno = subalterno