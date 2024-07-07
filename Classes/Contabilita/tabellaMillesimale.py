import os.path
import pickle

nome_file = 'Dati/tabelleMillesimali.pickle'
class TabellaMillesimale:

    def __init__(self):
        self.codice = 0
        self.nome = ""
        self.tipologiaSpesa =[]
        self.descrizione = ""
        self.immobile = 0
        self.millesimi = {}

    def aggiungiTabellaMillesimale(self, nome, tipologieSpesa, descrizione, immobile, millesimi):
        self.nome = nome
        self.tipologiaSpesa = tipologieSpesa
        self.descrizione = descrizione
        self.immobile = immobile
        self.millesimi = millesimi

        tabelleMillesimali = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tabelleMillesimali = dict(pickle.load(f))
                if tabelleMillesimali.keys():
                    self.codice = max(tabelleMillesimali.keys())+1
        tabelleMillesimali[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)
        return "Tabella millesimale aggiunta"


    def getTabellaMillesimale(self):
        return {
            "nome": self.nome,
            "tipologiaSpesa": self.tipologiaSpesa,
            "Descrizione": self.descrizione,
            "Millesimi": self.millesimi
        }

    @staticmethod
    def getAllTabelleMillesimali():
        if os.path.isfile(nome_file):
            print("esiste")
            with open(nome_file, "rb") as f:
                try:
                    tabelleMillesimali = dict(pickle.load(f))
                except EOFError:
                    tabelleMillesimali = {}
                return tabelleMillesimali
        else:
            print("non esiste")
            return {}

    @staticmethod
    def getAllTabelleMillesimaliByImmobile(immobile):
        tabelleMillesimali = TabellaMillesimale.getAllTabelleMillesimali()
        print("ciao bastardo")
        print(tabelleMillesimali)
        if tabelleMillesimali:
            print("i'm back")
            tabellaMillesimaleByImmobile = {}
            for key, value in tabelleMillesimali.items():
                print("value immobile: ", value.immobile.id)
                if value.immobile.id == immobile.id:
                    print("sescesce")
                    tabellaMillesimaleByImmobile[key] = value
                print(tabellaMillesimaleByImmobile)
            return tabellaMillesimaleByImmobile
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
        return "Tabella millesimale rimossa"
    def modificaTabellaMillesimale(self, nome, tipologieSpesa, descrizione, immobile, millesimi):
        msg = "La tabella millesimale dell'immobile " + immobile.denominazione + " è stata modificata"
        if os.path.isfile(nome_file):
            with(nome_file, "rb") as f:
                tabelleMillesimali = dict(pickle.load(f))

                tabelleMillesimali[self.codice].nome = nome
                tabelleMillesimali[self.codice].tipologieSpesa = tipologieSpesa
                tabelleMillesimali[self.codice].descrizione = descrizione
                tabelleMillesimali[self.codice].immobile = immobile.id
                tabelleMillesimali[self.codice].millesimi = millesimi

        with open(nome_file, "wb") as f:
            pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)
        return msg

