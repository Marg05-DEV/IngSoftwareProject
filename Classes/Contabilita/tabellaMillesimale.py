import os.path
import pickle

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

nome_file = 'Dati/TabelleMillesimali.pickle'

class TabellaMillesimale:

    def __init__(self):
        self.codice = 1
        self.nome = ""#
        self.tipologieSpesa = []#
        self.descrizione = ""#
        self.immobile = 0#
        self.millesimi = {} # # {unita immobiliare: millesimo}

    def aggiungiTabellaMillesimale(self, nome, tipologieSpesa, descrizione, immobile):
        self.nome = nome
        self.tipologieSpesa = tipologieSpesa
        self.descrizione = descrizione
        self.immobile = immobile
        for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(immobile)).values():
            self.millesimi[unita.codice] = 0.00

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

    def getInfoTabellaMillesimale(self):
        return {
            "nome": self.nome,
            "tipologieSpesa": self.tipologieSpesa,
            "descrizione": self.descrizione,
            "millesimi": self.millesimi
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
        self.tipologieSpesa = []
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

    def addTipoSpesa(self, tipo_spesa):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                tabelleMillesimali = dict(pickle.load(f))
                tabelleMillesimali[self.codice].tipologieSpesa.append(tipo_spesa.codice)
            with open(nome_file, "wb") as f:
                pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)

    def removeTipoSpesa(self, tipo_spesa):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                tabelle_millesimali = dict(pickle.load(f))
                tabelle_millesimali[self.codice].tipologieSpesa.remove(tipo_spesa.codice)
        with open(nome_file, "wb") as f:
            pickle.dump(tabelle_millesimali, f, pickle.HIGHEST_PROTOCOL)

    def addMillesimo(self, unita, valore):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                tabelleMillesimali = dict(pickle.load(f))
                tabelleMillesimali[self.codice].millesimi[unita.codice] = valore
        with open(nome_file, "wb") as f:
            pickle.dump(tabelleMillesimali, f, pickle.HIGHEST_PROTOCOL)

