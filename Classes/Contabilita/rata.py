import datetime
import os.path
import pickle

nome_file= 'Dati/Rate.pickle'

class Rata:
    numRateRegistrate = 0
    saldoCassa = 0

    def __init__(self):
        self.codice = 0
        self.dataPagamento = datetime.datetime(year=1970, month=1, day=1)
        self.descrizione = ""
        self.importo = 0.0
        self.numeroRicevuta = 0
        self.pagata = False
        self.tipoPagamento = ""
        self.unitaImmobiliare = None



    def aggiungiRata(self, codice, dataPagamento, descrizione, importo, numeroRicevuta, pagata, tipoPagamento, unitaImmobiliare):
        Rata.numRateRegistrate += 1
        self.codice = codice
        self.dataPagamento = dataPagamento
        self.descrizione = descrizione
        self.importo = importo
        self.numeroRicevuta = numeroRicevuta
        self.pagata = pagata
        self.tipoPagamento = tipoPagamento
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

    def ricercaRataByDataPagamento(self, data):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.dataPagamento == data:
                        return rata
                return "Rata non trovata"
        else:
            return "File non esistente"

    def ricercaRataByCodice(self, codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.codice == codice:
                        return rata
                return "Rata non trovata"
        else:
            return "File non esistente"


    def getRata(self):
        if self.pagata:
            pagata = "si"
        else:
            pagata = "no"

        return {
            "codice": self.codice,
            "dataPagamento": self.dataPagamento,
            "descrizione": self.descrizione,
            "importo": self.importo,
            "numeroRicevuta": self.numeroRicevuta,
            "Pagata": pagata,
            "tipoPagamento": self.tipoPagamento,
            "unitaImmobiliare": self.unitaImmobiliare
        }

    def modificaRata(self, codice = None, dataPagamento = None, descrizione = None, importo = None, numeroRicevuta = None,
                     pagata = None, tipoPagamento = None, unitaImmobiliare = None):
        if codice is not None:
            self.codice = codice
        if dataPagamento is not None:
            self.dataPagamento = dataPagamento
        if descrizione is not None:
            self.descrizione = descrizione
        if importo is not None:
            self.importo = importo
        if numeroRicevuta is not None:
            self.numeroRicevuta = numeroRicevuta
        if pagata is not None:
            self.pagata = pagata
        if tipoPagamento is not None:
            self.tipoPagamento = tipoPagamento
        if unitaImmobiliare is not None:
            self.unitaImmobiliare = unitaImmobiliare


