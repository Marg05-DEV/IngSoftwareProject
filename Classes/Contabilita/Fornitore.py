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
        self.codice = 0

    def aggiungiFornitore(self , cittaSede, denominazione, indirizzoSede, partitaIva, tipoProfessione, codice):
        self.cittaSede = cittaSede
        self.denominazione = denominazione
        self.indirizzoSede = indirizzoSede
        self.partitaIva = partitaIva
        self.tipoProfessione = tipoProfessione
        self.codice = codice

        fornitori = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = dict(pickle.load(f))
        fornitori[codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(fornitori, f, pickle.HIGHEST_PROTOCOL)

    def getFornitore(self):
        return {
            "cittaSede": self.cittaSede,
            "denominazione": self.denominazione,
            "indirizzoSede": self.indirizzoSede,
            "partitaIva": self.partitaIva,
            "tipoProfessione": self.tipoProfessione,
            "codice:": self.codice
        }
