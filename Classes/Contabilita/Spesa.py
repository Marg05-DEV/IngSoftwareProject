import os.path
import pickle
from datetime import datetime


class Spesa:

    def __init__(self):
        self.codice = 0
        self.descrizione = ""
        self.fornitore = None
        self.importo = 0
        self.dataScadenza = datetime(year=1970, month=1, day=1)
        self.immobile = None
        self.pagata = False
        self.dataPagamento = datetime(year=1970, month=1, day=1)
        self.tipoSpesa = ""

    def aggiungiSpesa(self, descrizione, fornitore, importo, codice, tipoSpesa, dataScadenza, immobile, pagata, dataPagamento):
        self.descrizione = descrizione
        self.fornitore = fornitore
        self.codice = codice
        self.importo = importo
        self.dataScadenza = dataScadenza
        self.immobile = immobile
        self.pagata = pagata
        self.dataPagamento = dataPagamento
        self.tipoSpesa = tipoSpesa

        spese = {}
        if os.path.isfile('Dati/spese.pickle'):
            with open('dati/spese.pickle', 'rb') as f:
                spese = pickle.load(f)
        spese[codice] = self
        with open('Dati/spese.pickle', 'wb') as f:
            pickle.dump(spese, f , pickle.HIGHEST_PROTOCOL)

    def ricercaSpesaByDataPagamento(self, dataPagamento):
        if os.path.isfile('Dati/spese.pickle'):
            with open('dati/spese.pickle', 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.dataPagamento == dataPagamento:
                        return spesa
            return "Spesa non Trovata"
        return "File non esistente"

    def ricercaSpesaByTipoSpesa(self, tipo):
        if os.path.isfile('Dati/spese.pickle'):
            with open('dati/spese.pickle', 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.tipoSpesa == tipo:
                        return spesa
            return "Spesa non Trovata"
        return "File non esistente"

    def ricercaSpesaByImmobile(self, nomeImmobile):
        if os.path.isfile('Dati/spese.pickle'):
            with open('dati/spese.pickle', 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.immobile == nomeImmobile:
                        return spesa
            return "Spesa non Trovata"
        return "File non esistente"

    def ricercaSpesaByFornitore(self, fornitore):
        if os.path.isfile('Dati/spese.pickle'):
            with open('dati/spese.pickle', 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.fornitore == fornitore:
                        return spesa
            return "Spesa non Trovata"
        return "File non esistente"



    def getSpesa(self):
        return {
            "descrizione": self.descrizione,
            "fornitore": self.fornitore,
            "importo": self.importo,
            "dataScadenza": self.dataScadenza,
            "immobile": self.immobile,
            "pagata": self.pagata
        }
        