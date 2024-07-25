import os.path
import pickle

nome_file = 'Dati/TabelleMillesimali.pickle'

class TabellaMillesimale:

    def __init__(self):
        self.codice = 1
        self.nome = ""
        self.tipologiaSpesa = []
        self.descrizione = ""
        self.immobile = 0
        self.millesimi = {}  # {unita immobiliare: millesimo}

    def aggiungiTabellaMillesimale(self, nome, tipologieSpesa, descrizione, immobile, millesimi):
        print("in aggiunta tabella millesimale")
        self.nome = nome
        print("nome fatto")
        self.tipologiaSpesa = tipologieSpesa
        print("tipo fatto")
        self.descrizione = descrizione
        print("desc fatto")
        self.immobile = immobile
        print("immobile fatto")
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
        return "Tabella millesimale aggiunta", self

    def addTipoSpesa(self, tipo_spesa):
        print("bha")
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                tabelleMillesimali = dict(pickle.load(f))
                print(tabelleMillesimali[self.codice].tipologiaSpesa)
                tabelleMillesimali[self.codice].tipologiaSpesa.append(tipo_spesa.codice)
                print(tabelleMillesimali[self.codice].tipologiaSpesa)
            with open(nome_file, "wb") as f:
                pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)
    def getInfoTabellaMillesimale(self):
        return {
            "nome": self.nome,
            "tipologiaSpesa": self.tipologiaSpesa,
            "Descrizione": self.descrizione,
            "Millesimi": self.millesimi
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

    @staticmethod
    def getAllTabelleMillesimaliByImmobile(immobile):
        tabelleMillesimali = TabellaMillesimale.getAllTabelleMillesimali()
        if tabelleMillesimali:
            tabellaMillesimaleByImmobile = {}
            print(tabelleMillesimali)
            for key, value in tabelleMillesimali.items():
                if value.immobile == immobile.id:
                    tabellaMillesimaleByImmobile[key] = value
            return tabellaMillesimaleByImmobile
        else:
            return {}

    def rimuoviTabellaMillesimale(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tabelleMillesimali = pickle.load(f)
                del tabelleMillesimali[self.codice]
            with open(nome_file, 'wb') as f:
                pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)
        self.codice = -1
        self.nome = ""
        self.tipologiaSpesa = []
        self.descrizione = ""
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

    @staticmethod
    def ricercaTabelleMillesimaliByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tabelleMillesimali = dict(pickle.load(f))
                for cod_tm in tabelleMillesimali.keys():
                    if cod_tm == codice:
                        return tabelleMillesimali[cod_tm]
                return None
        else:
            return None

    @staticmethod
    def ricercaTabelleMillesimaliByNome(nome):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tabelleMillesimali = dict(pickle.load(f))
                for tabella in tabelleMillesimali.values():
                    if tabella.nome == nome:
                        return tabella
                return None
        else:
            return None

    def removeTipoSpesa(self, tipo_spesa):
        print("dentro la funzione removeTipoSpesa")
        print(tipo_spesa.codice)
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                print("prima del dict")
                tabelle_millesimali = dict(pickle.load(f))
                print(tabelle_millesimali[self.codice].tipologiaSpesa)
                tabelle_millesimali[self.codice].tipologiaSpesa.remove(tipo_spesa.codice)
                print(tabelle_millesimali[self.codice].tipologiaSpesa)
            with open(nome_file, "wb") as f:
                pickle.dump(tabelle_millesimali, f, pickle.HIGHEST_PROTOCOL)

    def addMillesimo(self, ui, valore_millesimo):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                tabelleMillesimali = dict(pickle.load(f))
                tabelleMillesimali[self.codice].mllesimi[ui.codice] = valore_millesimo
        with open(nome_file, "wb") as f:
            pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)

