import os.path
import pickle

nome_file = 'Dati/tabelleMillesimali.pickle'
class TabellaMillesimale:

    def __init__(self):
        self.codice = 0
        self.nome = ""
        self.tipologiaSpesa =[]
        self.descrizione = ""
        self.immobile = None
        self.millesimi = {}

    def aggiungiTabellaMillesimale(self, codice, nome, tipologieSpesa, descrizione, immobile, millesimi):
        self.codice = codice
        self.nome = nome
        self.tipologiaSpesa = tipologieSpesa
        self.descrizione = descrizione
        self.immobile = immobile
        self.millesimi = millesimi

        tabelleMillesimali = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tabelleMillesimali = dict(pickle.load(f))
        tabelleMillesimali[codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)


    def getTabellaMillesimale(self):
        return {
            "codice": self.codice,
            "nome": self.nome,
            "tipologiaSpesa": self.tipologiaSpesa,
            "Descrizione": self.descrizione
        }

    @staticmethod
    def getAllTabelleMillesimali():
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                try:
                    tabelleMillesimali = dict(pickle.load(f))
                except EOFError:
                    tabelleMillesimali = {}
                return tabelleMillesimali
        else:
            return {}

    def rimuoviTabellaMillesimale(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'wb+') as f:
                tabelleMillesimali = pickle.load(f)
                del tabelleMillesimali[self.codice]
            with open(nome_file, 'wb') as f:
                pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)
        self.codice = -1
        self.nome = ""
        self.tipologiaSpesa = []
        self.descrizione = ()
        self.immobile = None
        self.millesimi = {}
        del self



