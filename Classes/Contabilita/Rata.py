import datetime
import os.path
import pickle

nome_file= 'Dati/Rate.pickle'

class Rata:
    numRateRegistrate = 0
    saldoCassa = 0

    def __init__(self):
        self.codice = 0
        self.dataRegistrazione = datetime.datetime(year=1970, month=1, day=1)
        self.descrizione = ""
        self.importo = 0.0
        self.numeroRicevuta = 0
        self.pagata = False
        self.unitaImmobiliare = None



    def aggiungiRata(self, codice, dataRegistrazione, descrizione, importo, numeroRicevuta, pagata, unitaImmobiliare):
        Rata.numRateRegistrate += 1
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
            "codice": self.codice,
            "dataRegistrazione": self.dataRegistrazione,
            "descrizione": self.descrizione,
            "importo": self.importo,
            "numeroRicevuta": self.numeroRicevuta,
            "pagata": self.pagata,
            "unitaImmobiliare": self.unitaImmobiliare
        }