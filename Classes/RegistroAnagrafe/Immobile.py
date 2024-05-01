import os.path
import pickle


class Immobile:

    def __init__(self):
        self.codice = 0
        self.sigla = ""
        self.denominazione = ""
        self.codiceFiscale = ""
        self.citta = ""
        self.provincia = ""
        self.cap = ""
        self.via = ""

    def aggiungiImmobile(self, codice, sigla, denominazione, codiceFiscale, citta, provincia, cap, via):
        self.codice = codice
        self.sigla = sigla
        self.denominazione = denominazione
        self.codiceFiscale = codiceFiscale
        self.citta = citta
        self.provincia = provincia
        self.cap = cap
        self.via = via

        immobile = {}
        if os.path.isfile('../../Dati/Immobile.pickle'):
            with open('../../Dati/Immobile.pickle', 'rb') as f:
                immobile = pickle.load(f)
        immobile[codice] = self
        with open('../../Dati/Immobile.pickle', 'wb') as f:
            pickle.dump(immobile, f, pickle.HIGHEST_PROTOCOL)

    def getImmobile(self):
        return{
            "codice": self.codice,
            "sigla": self.sigla,
            "denominazione": self.denominazione,
            "codiceFiscale": self.codiceFiscale
        }

    def ricercaImmobile(self):
        pass

immo = Immobile()
immo.aggiungiImmobile(1, "thg","hvn", "irn","rgvjh","63073", "63073", "jbnt" )