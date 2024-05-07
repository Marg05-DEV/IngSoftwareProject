import datetime
import os.path
import pickle

nome_file= 'Dati/Rate.pickle'

class Rata:
    numRateRegistrate = 0
    saldoCassa = 0

    def __init__(self):
        self.codice = 0
    def aggiungiRata(self, codice):
        self.codice = codice
        self.dataRegistrazione = dataRegistrazione
        self.descrizione = descrizione
        self.importo = importo
        self.numeroRicevuta = numeroRicevuta
        self.pagata = pagata
        self.unitaImmobiliare = unitaImmobiliare

        rate = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = dict(pickle.load(f))
        rate[codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(rate, f, pickle.HIGHEST_PROTOCOL)

    def rimuoviRata(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'wb+') as f:
                rate = pickle.load(f)
                del rate[self.codice]
        self.codice = 0
        del self

    def ricercaRataByDataRegistrazione(self, data):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
            for rata in rate:
                if rata.dataRegistrazione == data:
                    return rata
                else:
                    return "Rata non trovata"
        else:
            return "File non esistente"

    def ricercaRataByCodice(self, codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
            for rata in rate:
                if rata.codice == codice:
                    return rata
            else:
                return "Rata non trovata"
        else:
            return "File non esistente"


    def getRata(self):
        return {
            "codice": self.codice
        }