class Condomino:

    def __init__(self, nome, cognome, residenza, dataDiNascita, codiceFiscale, luogoDiNascita, codice, unitaImmobiliare):
        self.nome = nome
        self.cognome = cognome
        self.residenza = residenza
        self.codice = codice
        self.dataDiNascita = dataDiNascita
        self.codiceFiscale = codiceFiscale
        self.luogoDiNascita = luogoDiNascita
        self.unitaImmobiliare = unitaImmobiliare

    def getCondomino(self):
        return {
            "nome": self.nome,
            "cognome": self.cognome,
            "codice": self.codice,
            "residenza": self.residenza,
            "dataDiNascita": self.dataDiNascita,
            "codiceFiscale": self.codiceFiscale,
            "luogoDiNascita": self.luogoDiNascita,
            "unitaImmobiliare": self.unitaImmobiliare
        }