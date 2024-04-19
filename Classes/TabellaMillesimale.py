class TabellaMillesimale:
    def __init__(self, codice, nome, tipologieSpesa):
        self.codice = codice
        self.nome = nome
        self.tipologiaSpesa = tipologieSpesa

    def getTabellaMillesimale(self):
        return {
            "codice": self.codice,
            "nome": self.nome,
            "tipologiaSpesa": self.tipologiaSpesa
        }
