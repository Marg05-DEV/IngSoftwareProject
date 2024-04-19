class Condomino:

    def __init__(self):
        self.nome = ""
        self.cognome = ""
        self.residenza = ""
        self.codice = 0
        self.dataDiNascita = datetime.datetime(year=1970, month=1, day=1)
        self.codiceFiscale = ""
        self.luogoDiNascita = ""
        self.unitaImmobiliare = None

    def aggiungiCondomino(self, nome, cognome, residenza, dataDiNascita, codiceFiscale, luogoDiNascita, codice, unitaImmobiliare):
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

    def inserisciCondomino(self):
        pass

