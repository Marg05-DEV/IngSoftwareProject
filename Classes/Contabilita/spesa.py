import os.path
import pickle
from datetime import datetime

nome_file = 'Dati/spese.pickle'
class Spesa:
    numSpeseRegistrate = 0

    def __init__(self):
        self.codice = 0
        self.dataFattura = datetime(year=1970, month=1, day=1)
        self.dataRegistrazione = datetime(year=1970, month=1, day=1)
        self.dataPagamento = datetime(year=1970, month=1, day=1)
        self.descrizione = ""
        self.fornitore = None
        self.importo = 0.0
        self.immobile = None
        self.isRitenuta = False
        self.tipoSpesa = None
        self.pagata = False
        self.numeroFattura = 0



    def aggiungiSpesa(self, descrizione, fornitore, importo, codice, tipoSpesa, immobile, pagata, dataPagamento, dataFattura, dataRegistrazione, isRitenuta, numeroFattura):
        Spesa.numSpeseRegistrate += 1
        self.codice = codice
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
        spese[codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(spese, f, pickle.HIGHEST_PROTOCOL)

    def modificaSpesa(self, descrizione = None, fornitore = None, importo = None, codice = None, tipoSpesa = None, immobile = None,
                      pagata = None, dataPagamento = None, dataFattura = None, dataRegistrazione = None, isRitenuta = None, numeroFattura = None):
        if descrizione is not None:
            self.descrizione = descrizione
        if fornitore is not None:
            self.fornitore = fornitore
        if codice is not None:
            self.codice = codice
        if importo is not None:
            self.importo = importo
        if tipoSpesa is not None:
            self.tipoSpesa = tipoSpesa
        if immobile is not None:
            self.immobile = immobile
        if pagata is not None:
            self.pagata = pagata
        if dataPagamento is not None:
            self.dataPagamento = dataPagamento
        if dataFattura is not None:
            self.dataFattura = dataFattura
        if dataRegistrazione is not None:
            self.dataRegistrazione = dataRegistrazione
        if isRitenuta is not None:
            self.isRitenuta = isRitenuta
        if numeroFattura is not None:
            self.numeroFattura = numeroFattura




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

    @staticmethod
    def ordinaCondominoByDataRegistrazione():
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                sorted_dataRegistrazione = []
                for spesa in spese.values():
                    sorted_dataRegistrazione.append(spesa.dataRegistrazione)
                sorted_dataRegistrazione.sort()
                sorted_spese = []
                for dataRegistrazione in sorted_dataRegistrazione:
                    for spesa in spese.values():
                        if spesa.dataRegistrazione == dataRegistrazione:
                            sorted_spese.append(spesa)
                            break
                return sorted_spese
        else:
            return None

    @staticmethod
    def ordinaCondominoByTipoSpesa(isDecrescente):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                sorted_tipoSpesa = []
                for spesa in spese.values():
                    sorted_tipoSpesa.append(spesa.tipoSpesa)
                sorted_tipoSpesa.sort(reverse=isDecrescente)
                sorted_spese = []
                for tipoSpesa in sorted_tipoSpesa:
                    for spesa in spese.values():
                        if spesa.tipoSpesa == tipoSpesa:
                            sorted_spese.append(spesa)
                            break
                return sorted_spese
        else:
            return None

    @staticmethod
    def ordinaCondominoByImmobile(isDecrescente):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                sorted_immobile = []
                for spesa in spese.values():
                    sorted_immobile.append(spesa.immobile)
                sorted_immobile.sort(reverse=isDecrescente)
                sorted_spese = []
                for immobile in sorted_immobile:
                    for spesa in spese.values():
                        if spesa.immobile == immobile:
                            sorted_spese.append(spesa)
                            break
                return sorted_spese
        else:
            return None

    @staticmethod
    def ordinaCondominoByFornitore(isDecrescente):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                sorted_fornitore = []
                for spesa in spese.values():
                    sorted_fornitore.append(spesa.fornitore)
                sorted_fornitore.sort(reverse=isDecrescente)
                sorted_spese = []
                for fornitore in sorted_fornitore:
                    for spesa in spese.values():
                        if spesa.fornitore == fornitore:
                            sorted_spese.append(spesa)
                            break
                return sorted_spese
        else:
            return None


    def getSpesa(self):
        if self.pagata:
            pagata = "si"
        else:
            pagata = "no"
        return {
        "Numero spese Registrate" : Spesa.numSpeseRegistrate,
        "Codice" : self.codice,
        "Data Fattura" : self.dataFattura,
        "Data Registrazione" : self.dataRegistrazione,
        "Data Pagamento" : self.dataPagamento,
        "Descrizione" : self.descrizione,
        "Fornitore" : self.fornitore,
        "Importo" : self.importo,
        "Immobile" : self.immobile,
        "IsRitenuta" : self.isRitenuta,
        "TipoSpesa" : self.tipoSpesa,
        "Pagata" : pagata,
        "NumeroFattura" : self.numeroFattura
        }
        