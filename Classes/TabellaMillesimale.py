class TabellaMillesimale:

    def __init__(self):
        self.codice = 0
        self.nome = ""
        self.tipologiaSpesa = None
    def aggiungiTabellaMillesimale(self, codice, nome, tipologieSpesa):
        self.codice = codice
        self.nome = nome
        self.tipologiaSpesa = tipologieSpesa

    def getTabellaMillesimale(self):
        return {
            "codice": self.codice,
            "nome": self.nome,
            "tipologiaSpesa": self.tipologiaSpesa
        }
