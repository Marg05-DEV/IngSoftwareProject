import datetime
import os.path
import pickle

from Classes.Contabilita.fornitore import Fornitore
from Classes.RegistroAnagrafe.immobile import Immobile

nome_file = 'Dati/Spese.pickle'
class Spesa:
    #numSpeseRegistrate = 0

    def __init__(self):
        self.codice = 1
        self.dataFattura = datetime.date(year=1970, month=1, day=1)#
        self.dataRegistrazione = datetime.date(year=1970, month=1, day=1)#
        self.dataPagamento = datetime.date(year=1970, month=1, day=1)#
        self.descrizione = ""#
        self.fornitore = 0#
        self.importo = 0.0#
        self.immobile = 0#
        self.isRitenuta = False#
        self.tipoSpesa = 0#
        self.pagata = False#
        self.numeroFattura = 0#
        self.aBilancio = False

    def aggiungiSpesa(self, descrizione, fornitore, importo, tipoSpesa, immobile, pagata, dataPagamento, dataFattura, dataRegistrazione, isRitenuta, numeroFattura):
        self.dataFattura = dataFattura
        self.dataRegistrazione = dataRegistrazione
        self.dataPagamento = dataPagamento
        self.descrizione = descrizione
        self.fornitore = fornitore
        self.importo = importo
        self.immobile = immobile
        self.isRitenuta = isRitenuta
        self.tipoSpesa = tipoSpesa
        self.pagata = pagata
        self.numeroFattura = numeroFattura

        spese = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = pickle.load(f)
                if spese.keys():
                    self.codice = max(spese.keys())+1
        spese[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(spese, f, pickle.HIGHEST_PROTOCOL)
        return "Spesa aggiunta", self

    def modificaSpesa(self, descrizione, fornitore, importo, tipoSpesa, immobile,
                      pagata, dataPagamento, dataFattura, dataRegistrazione, isRitenuta, numeroFattura):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                spese = dict(pickle.load(f))
                spese[self.codice].descrizione = descrizione
                spese[self.codice].fornitore = fornitore
                spese[self.codice].importo = importo
                spese[self.codice].tipoSpesa = tipoSpesa
                spese[self.codice].pagata = pagata
                spese[self.codice].immobile = immobile
                spese[self.codice].pagata = pagata
                spese[self.codice].dataPagamento = dataPagamento
                spese[self.codice].dataFattura = dataFattura
                spese[self.codice].dataRegistrazione = dataRegistrazione
                spese[self.codice].isRitenuta = isRitenuta
                spese[self.codice].numeroFattura = numeroFattura
        with open(nome_file, "wb") as f:
            pickle.dump(spese, f, pickle.HIGHEST_PROTOCOL)
        return "La rata è stata modificata"

    def rimuoviSpesa(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
               spese = dict(pickle.load(f))
               del spese[self.codice]
            with open(nome_file,'wb') as f:
                pickle.dump(spese, f, pickle.HIGHEST_PROTOCOL)
        self.codice = -1
        self.dataFattura = datetime.date(year=1970, month=1, day=1)
        self.dataRegistrazione = datetime.date(year=1970, month=1, day=1)
        self.dataPagamento = datetime.date(year=1970, month=1, day=1)
        self.descrizione = ""
        self.fornitore = None
        self.importo = 0.0
        self.immobile = None
        self.isRitenuta = False
        self.tipoSpesa = None
        self.pagata = False
        self.aBilancio = False
        self.numeroFattura = 0
        del self
        return "Spesa rimossa"

    @staticmethod
    def ricercaSpesaByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.codice == codice:
                        return spesa
                return None
        return None

    @staticmethod
    def ricercaSpesaByDataPagamento(dataPagamento):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.dataPagamento == dataPagamento:
                        return spesa
                return None
        return None

    @staticmethod
    def ricercaSpesaByTipoSpesa(tipo):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.tipoSpesa.codice == tipo.codice:
                        return spesa
                return None
        return None

    @staticmethod
    def ricercaSpesaByImmobile(nomeImmobile):
        if (os.path.isfile(nome_file)):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.immobile.codice == nomeImmobile.codice:
                        return spesa
                return None
        return None

    @staticmethod
    def ricercaSpesaByFornitore(fornitore):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.fornitore.codice == fornitore.codice:
                        return spesa
                return None
        return None

    @staticmethod
    def getAllSpese():
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                try:
                    spese = dict(pickle.load(f))
                except EOFError:
                    spese = {}
                return spese
        else:
            return {}

    def getInfoSpesa(self):
        return {
        "codice" : self.codice,
        "dataFattura" : self.dataFattura,
        "dataRegistrazione" : self.dataRegistrazione,
        "dataPagamento" : self.dataPagamento,
        "descrizione" : self.descrizione,
        "fornitore" : self.fornitore,
        "importo" : self.importo,
        "immobile" : self.immobile,
        "isRitenuta" : self.isRitenuta,
        "tipoSpesa" : self.tipoSpesa,
        "pagata" : self.pagata,
        "aBilancio" : self.aBilancio,
        "numeroFattura" : self.numeroFattura
        }

    @staticmethod
    def getAllSpeseByImmobile(immobile):
        spese = Spesa.getAllSpese()
        if spese:
            speseByImmobile = {}
            for key, value in spese.items():
                immo = Immobile.ricercaImmobileByCodice(value.immobile)
                if immo.id == immobile.id:
                    speseByImmobile[key] = value
            return speseByImmobile
        else:
            return {}

    @staticmethod
    def getAllSpeseByFornitore(fornitore):
        spese = Spesa.getAllSpese()
        if spese:
            speseByFornitore = {}
            for key, value in spese.items():
                forni = Fornitore.ricercaFornitoreByCodice(value.fornitore)
                if forni.codice == fornitore.codice:
                    speseByFornitore[key] = value
            return speseByFornitore
        else:
            return {}

    @staticmethod
    def getAllSpeseByPeriodoBilancio(immobile, data_inizio, data_fine):
        spese = Spesa.getAllSpeseByImmobile(immobile)
        if spese:
            speseByPeriodoBilancio = {}
            for key, value in spese.items():
                if value.dataRegistrazione >= data_inizio and value.dataRegistrazione <= data_fine:
                    speseByPeriodoBilancio[key] = value
            return speseByPeriodoBilancio
        else:
            return {}

    def mettiABilancio(self):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                spese = dict(pickle.load(f))
                spese[self.codice].aBilancio = True
        with open(nome_file, "wb") as f:
            pickle.dump(spese, f, pickle.HIGHEST_PROTOCOL)
