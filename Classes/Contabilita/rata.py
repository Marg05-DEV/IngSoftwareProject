import datetime
import os.path
import pickle

nome_file = 'Dati/Rate.pickle'

class Rata:
    def __init__(self):
        self.codice = 1
        self.dataPagamento = datetime.date(year=1970, month=1, day=1)
        self.descrizione = ""
        self.importo = 0.0
        self.numeroRicevuta = 0
        self.pagata = False
        self.tipoPagamento = ""
        self.unitaImmobiliare = None
        self.versante = ""

    def aggiungiRata(self, dataPagamento, descrizione, importo, numeroRicevuta, pagata, tipoPagamento, unitaImmobiliare, versante):
        self.dataPagamento = dataPagamento
        self.descrizione = descrizione
        self.importo = importo
        self.numeroRicevuta = numeroRicevuta
        self.pagata = pagata
        self.tipoPagamento = tipoPagamento
        self.unitaImmobiliare = unitaImmobiliare
        self.versante = versante

        rate = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = dict(pickle.load(f))
                if rate.keys():
                    print(max(rate.keys()))
                    self.codice = max(rate.keys()) + 1
        rate[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(rate, f, pickle.HIGHEST_PROTOCOL)
        return "Rata aggiunta", self

    def modificaRata(self, dataPagamento, descrizione, importo, numeroRicevuta, pagata, tipoPagamento, unitaImmobiliare, versante):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                rate = dict(pickle.load(f))
                rate[self.codice].dataPagamento = dataPagamento
                rate[self.codice].descrizione = descrizione
                rate[self.codice].importo = importo
                rate[self.codice].numeroRicevuta = numeroRicevuta
                rate[self.codice].pagata = pagata
                rate[self.codice].tipoPagamento = tipoPagamento
                rate[self.codice].unitaImmobiliare = unitaImmobiliare
                rate[self.codice].versante = versante
        with open(nome_file, "wb") as f:
            pickle.dump(rate, f, pickle.HIGHEST_PROTOCOL)
        return "La rata è stata modificata"

    def rimuoviRata(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
                del rate[self.codice]
            with open(nome_file, 'wb') as f:
                pickle.dump(rate, f, pickle.HIGHEST_PROTOCOL)
        self.codice = -1
        self.dataPagamento = datetime.datetime(year=1970, month=1, day=1)
        self.descrizione = ""
        self.importo = 0.0
        self.numeroRicevuta = 0
        self.pagata = False
        self.tipoPagamento = ""
        self.unitaImmobiliare = None
        self.versante = ""
        del self
        return "Rata rimossa"
    def getInfoRata(self):
        return {
            "codice": self.codice,
            "dataPagamento": self.dataPagamento,
            "descrizione": self.descrizione,
            "importo": self.importo,
            "numeroRicevuta": self.numeroRicevuta,
            "pagata": self.pagata,
            "tipoPagamento": self.tipoPagamento,
            "unitaImmobiliare": self.unitaImmobiliare,
            "versante": self.versante
        }

    @staticmethod
    def getAllRate():
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                try:
                    rate = dict(pickle.load(f))
                except EOFError:
                    rate = {}
                return rate
        else:
            return {}

    @staticmethod
    def ricercaRataByDataPagamento(data):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.dataPagamento == data:
                        return rata
                return "Rata non trovata"
        else:
            return "File non esistente"

    @staticmethod
    def ricercaRataByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.codice == codice:
                        return rata
                return "Rata non trovata"
        else:
            return "File non esistente"



