import os
import pickle

nome_file='Dati/Fornitori.pickle'
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
