import os
import pickle

nome_file = 'Dati/Fornitori.pickle'
class Fornitore:

    def __init__(self):
        self.cittaSede = ""
        self.denominazione = ""
        self.indirizzoSede = ""
        self.partitaIva = ""
        self.tipoProfessione = ""

    def aggiungiFornitore(self , cittaSede, denominazione, indirizzoSede, partitaIva, tipoProfessione):
        self.cittaSede = cittaSede
        self.denominazione = denominazione
        self.indirizzoSede = indirizzoSede
        self.partitaIva = partitaIva
        self.tipoProfessione = tipoProfessione

        fornitori = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
        fornitori[denominazione] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(fornitori, f, pickle.HIGHEST_PROTOCOL)

    def getFornitore(self):
        return {
            "cittaSede": self.cittaSede,
            "denominazione": self.denominazione,
            "indirizzoSede": self.indirizzoSede,
            "partitaIva": self.partitaIva,
            "tipoProfessione": self.tipoProfessione,
        }
    @staticmethod
    def ricercaFornitoreByPartitaIVA(partitaIva):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
                for fornitore in fornitori.values():
                    fornitore.partitaIVA = partitaIva
                    return fornitore
                return "fornitore non trovato"
        return "File non trovato"

    def rimuoviFornitore(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
                del fornitori[self.partitaIva]
            with open(nome_file, 'wb+') as f:
                pickle.load(fornitori, f, pickle.HIGHEST_PROTOCOL)
        self.cittaSede = ""
        self.denominazione = ""
        self.indirizzoSede = ""
        self.partitaIva = ""
        self.tipoProfessione = ""
        del self

    def modificaFornitore(self, cittaSede = None, denominazione = None, indirizzoSede = None, partitaIva = None, tipoProfessione = None):
        if cittaSede is not None:
            self.cittaSede = cittaSede
        if denominazione is not None:
            self.denominazione = denominazione
        if partitaIva is not None:
            self.partitaIva = partitaIva
        if tipoProfessione is not None:
            self.tipoProfessione = tipoProfessione
        if indirizzoSede is not None:
            self.indirizzoSede = indirizzoSede
