import datetime
import os.path
import pickle
nome_file = 'Dati/Bilanci.pickle'

class Bilancio:

    def __init__(self):
        self.codice = 1
        self.immobile = None
        self.inizioEsercizio = datetime.date(year=1970, month=1, day=1)
        self.fineEsercizio = datetime.date(year=1970, month=1, day=1)
        self.spesePreventivate = {} # {TabMillesimale: {TipoSpesa: valore inserito da noi}, ...}
        self.speseConsuntivate = {} # {TabMillesimale: {TipoSpesa: valore calcolato dalle spese inserite}, ...}
        self.ripartizioneSpesePreventivate = {} # {TabMillesimale: {UnitaImmobiliare: valore calcolato tra dict spesePreventivate e tabelle millesimali}, ...}
        self.ripartizioneSpeseConsuntivate = {} # {TabMillesimale: {UnitaImmobiliare: valore calcolato tra dict speseConsuntivate e tabelle millesimali}, ...}
        self.ripartizioneConguaglio = {} # {TabMillesimale: {UnitaImmobiliare: differenza ripartizioneSpesePrev - ripartizioneSpeseCons }, ...}
        self.importiDaVersare = {} # {UnitaImmobiliare: somma spese prev - conguaglio}, ...}
        self.numeroRate = 0
        self.ratePreventivate = {} # {UnitaImmobiliare: [rata 1-esima, ..., rata n-esima], ...}
        
    def aggiungiBilancio(self, fineEsercizio, immobile, importiDaVersare, inizioEsercizio, numeroRate, ratePreventivate, ripartizioneConguaglio,
                         ripartizioneSpeseConsuntivate, ripartizioneSpesePreventivate, speseConsuntivate, spesePreventivate):
        self.fineEsercizio = fineEsercizio
        self.immobile = immobile
        self.importiDaVersare = importiDaVersare
        self.inizioEsercizio = inizioEsercizio
        self.numeroRate = numeroRate
        self.ratePreventivate = ratePreventivate
        self.ripartizioneConguaglio = ripartizioneConguaglio
        self.ripartizioneSpeseConsuntivate = ripartizioneSpeseConsuntivate
        self.ripartizioneSpesePreventivate = ripartizioneSpesePreventivate
        self.speseConsuntivate = speseConsuntivate
        self.spesePreventivate = spesePreventivate

        bilanci = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                bilanci = dict(pickle.load(f))
                if bilanci.keys():
                    self.codice = max(bilanci.keys()) + 1
        bilanci[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)
        return "Il bilancio è stato creato", self

    def getInfoBilancio(self):
        return {
            "codice": self.codice,
            "fineEsercizio": self.fineEsercizio,
            "immobile": self.immobile,
            "importiDaVersore": self.importiDaVersare,
            "inizioEsercizio": self.inizioEsercizio,
            "numeroRate": self.numeroRate,
            "ratePreventivate": self.ratePreventivate,
            "ripartizioneConguaglio": self.ripartizioneConguaglio,
            "ripartizioneSpeseConsuntivate": self.ripartizioneSpeseConsuntivate,
            "ripartizioneSpesePreventivate": self.ripartizioneSpesePreventivate,
            "speseConsuntivate": self.speseConsuntivate,
            "spesePreventivate": self.spesePreventivate
        }

    @staticmethod
    def getAllBilanci():
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                try:
                    bilanci = dict(pickle.load(f))
                except EOFError:
                    bilanci = {}
                return bilanci
        else:
            return {}

    @staticmethod
    def getAllBilanciByImmobile(immobile):
        bilanci = Bilancio.getAllBilanci()
        if bilanci:
            bilanciByImmobile = {}
            for key, value in bilanci.items():
                if value.immobile.id == immobile.id:
                    bilanciByImmobile[key] = value
            return bilanciByImmobile
        else:
            return {}

    @staticmethod
    def ricercaBilancioByDataInizio(data_inizio, immobile):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                bilanci = dict(pickle.load(f))
                for bilancio in bilanci.values():
                    print(str(bilancio.inizioEsercizio))
                    print(data_inizio)
                    print(str(bilancio.inizioEsercizio) == data_inizio and bilancio.immobile.codice == immobile.codice)
                    print(bilancio.immobile, " --- ", immobile)
                    if str(bilancio.inizioEsercizio) == data_inizio and bilancio.immobile.codice == immobile.codice:
                        return bilancio
                return None
        else:
            return None
    @staticmethod
    def ordinaBilancioByDataInizio(list_bilanci):
        sorted_data_inizio = []
        for bilancio in list_bilanci:
            sorted_data_inizio.append(bilancio.inizioEsercizio)
        sorted_data_inizio.sort(reverse=True)

        sorted_bilanci = []
        for inizio_esercizio in sorted_data_inizio:
            for bilancio in list_bilanci:
                if bilancio.inizioEsercizio == inizio_esercizio:
                    sorted_bilanci.append(bilancio)
                    break
        for i in range(len(list_bilanci)):
            list_bilanci[i] = sorted_bilanci[i]

