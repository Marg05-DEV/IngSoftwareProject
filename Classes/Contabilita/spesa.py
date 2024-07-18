import datetime
import os.path
import pickle

nome_file = 'Dati/spese.pickle'
class Spesa:
    #numSpeseRegistrate = 0

    def __init__(self):
        self.codice = 1
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
        self.numeroFattura = 0



    def aggiungiSpesa(self, descrizione, fornitore, importo, tipoSpesa, immobile, pagata, dataPagamento, dataFattura, dataRegistrazione, isRitenuta, numeroFattura):
        #Spesa.numSpeseRegistrate += 1
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
            with (open(nome_file, 'rb') as f):
               spese = dict(pickle.load(f))
               del spese[self.codice]
            with open(nome_file,'"wb') as f:
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
        self.numeroFattura = 0
        del self
        return "Spesa rimossa"
    @staticmethod
    def ricercaSpesaByDataPagamento(dataPagamento):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.dataPagamento == dataPagamento:
                        return spesa
                return "Spesa non Trovata"
        return "File non esistente"

    @staticmethod
    def ricercaSpesaByTipoSpesa(tipo):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.tipoSpesa == tipo:
                        return spesa
                return "Spesa non Trovata"
        return "File non esistente"

    @staticmethod
    def ricercaSpesaByImmobile(nomeImmobile):
        if (os.path.isfile(nome_file)):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.immobile == nomeImmobile:
                        return spesa
                return "Spesa non Trovata"
        return "File non esistente"
    @staticmethod
    def ricercaSpesaByFornitore(fornitore):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = dict(pickle.load(f))
                for spesa in spese.values():
                    if spesa.fornitore == fornitore:
                        return spesa
                return "Spesa non Trovata"
        return "File non esistente"

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
        