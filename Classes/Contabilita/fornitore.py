import os
import pickle

nome_file = 'Dati/Fornitori.pickle'
class Fornitore:

    def __init__(self):
        self.codice = 1
        self.cittaSede = ""#
        self.denominazione = ""#
        self.indirizzoSede = ""#
        self.partitaIva = ""#
        self.tipoProfessione = ""#

    def aggiungiFornitore(self, cittaSede, denominazione, indirizzoSede, partitaIva, tipoProfessione):
        self.cittaSede = cittaSede
        self.denominazione = denominazione
        self.indirizzoSede = indirizzoSede
        self.partitaIva = partitaIva
        self.tipoProfessione = tipoProfessione

        fornitori = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
                if fornitori.keys():
                    self.codice = max(fornitori.keys())+1
        fornitori[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(fornitori, f, pickle.HIGHEST_PROTOCOL)
        return "Fornitore aggiunto", self

    def modificaFornitore(self, cittaSede, denominazione, indirizzoSede, partitaIva, tipoProfessione):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = pickle.load(f)
                fornitori[self.codice].cittaSede = cittaSede
                fornitori[self.codice].denominazione = denominazione
                fornitori[self.codice].indirizzoSede = indirizzoSede
                fornitori[self.codice].partitaIva = partitaIva
                fornitori[self.codice].tipoProfessione = tipoProfessione
        with open(nome_file, "wb") as f:
            pickle.dump(fornitori, f, pickle.HIGHEST_PROTOCOL)
        return "Il fornitore è stato modificato"

    def rimuoviFornitore(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
                del fornitori[self.partitaIva]
            with open(nome_file, 'wb') as f:
                pickle.dump(fornitori, f, pickle.HIGHEST_PROTOCOL)
        self.codice = -1
        self.cittaSede = ""
        self.denominazione = ""
        self.indirizzoSede = ""
        self.partitaIva = ""
        self.tipoProfessione = ""
        del self
        return "Fornitore rimosso"

    def getInfoFornitore(self):
        return {
            "codice": self.codice,
            "cittaSede": self.cittaSede,
            "denominazione": self.denominazione,
            "indirizzoSede": self.indirizzoSede,
            "partitaIva": self.partitaIva,
            "tipoProfessione": self.tipoProfessione,
        }

    @staticmethod
    def getAllFornitore():
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                try:
                    fornitori = dict(pickle.load(f))
                except EOFError:
                    fornitori = {}
                return fornitori
        else:
            return {}

    @staticmethod
    def ricercaFornitoreByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
                for fornitore in fornitori.values():
                    if fornitore.codice == codice:
                        return fornitore
                return None
        return None

    @staticmethod
    def ricercaFornitoreByPartitaIVA(partitaIva):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
                for fornitore in fornitori.values():
                    if fornitore.partitaIva == partitaIva:
                        return fornitore
                return None
        return None

    @staticmethod
    def ricercaFornitoreByDenominazione(denominazione):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
                for fornitore in fornitori.values():
                    if fornitore.denominazione == denominazione:
                        return fornitore
                return None
        return None



