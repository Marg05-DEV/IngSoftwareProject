import datetime
import os.path
import pickle
from rata import Rata
nome_file = 'Dati/Bilanci.pickle'

class Bilancio:

    def __init__(self):
        self.codice = 0
        self.fineEsercizio = datetime.datetime(year=1970, month=1, day=1)
        self.immobile = None
        self.importiDaVersare = {}
        self.inizioEsercizio = datetime.datetime(year=1970, month=1, day=1)
        self.numeroRate = 0
        self.ratePreventivate = {}
        self.ripartizioneConguaglio = {}
        self.ripartizioneSpeseConsuntivate = {}
        self.ripartizioneSpesePreventivate = {}
        self.speseConsuntivate = {}
        self.spesePreventivate = {}
        
    def aggiungiBilancio(self, codice, fineEsercizio, immobile, importiDaVersare, inizioEsercizio, numeroRate, ratePreventivate, ripartizioneConguaglio,
                         ripartizioneSpeseConsuntivate, ripartizioneSpesePreventivate, speseConsuntivate, spesePreventivate):
        self.codice = codice
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
        bilanci[codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

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


