class TipoSpesa:
    def __init__(self, codice, descrizione, nome):
        self.codice = codice
        self.descrizione = descrizione
        self.nome = nome

    def getSpesa(self):
        return {
            "codice": self.codice,
            "descrizione": self.descrizione,
            "nome": self.nome
        }
