import datetime
import os.path
import pickle

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

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
        self.unitaImmobiliare = 0
        self.versante = ""
        self.isLast = False

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
                    self.codice = max(rate.keys()) + 1
        print(rate)
        if numeroRicevuta > 0:
            for rata in rate.values():
                print("------------------------ALTrO CICLO in rate.py-----------------------")
                print("codice unità immobiliare", self.unitaImmobiliare, " - codice unità immobilare che scorre delle rate", rata.unitaImmobiliare)
                if rata.unitaImmobiliare > 0:
                    if UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(rata.unitaImmobiliare).immobile == UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.unitaImmobiliare).immobile:
                        print("altra rata stesso immobile")
                        rata.isLast = False
                    print("fuori if")
            self.isLast = True
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
        self.dataPagamento = datetime.date(year=1970, month=1, day=1)
        self.descrizione = ""
        self.importo = 0.0
        self.numeroRicevuta = 0
        self.pagata = False
        self.tipoPagamento = ""
        self.unitaImmobiliare = 0
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
            "versante": self.versante,
            "isLast": self.isLast
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
                return None
        else:
            return None
    @staticmethod
    def ricercaRataByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.codice == codice:
                        return rata
                return None
        else:
            return None

    @staticmethod
    def getAllRateByImmobile(immobile):
        rate = Rata.getAllRate()
        print(rate)
        print("immobile selezionato", immobile)
        rateByImmobile = {}
        if rate:
            for cod_rata, rata in rate.items():
                if rata.unitaImmobiliare > 0:
                    obj_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(rata.unitaImmobiliare)
                    if immobile.id == obj_unitaImmobiliare.immobile:
                        rateByImmobile[cod_rata] = rata
            return rateByImmobile
        else:
            return {}

    @staticmethod
    def lastNumeroRicevuta(immobile):
        #{1: cardinalità di 1, 2: cardinalità di 2, ..., n: cardinalità di n}
        print(immobile)
        rate_immobile = Rata.getAllRateByImmobile(immobile)
        print("dai dai")
        if not rate_immobile:
            return 0
        for rata in rate_immobile.values():
            print(rata.getInfoRata())

        return [item for item in rate_immobile.values() if item.isLast][0].numeroRicevuta
