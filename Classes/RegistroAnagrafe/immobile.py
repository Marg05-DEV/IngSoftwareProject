import os.path
import pickle

file_name = 'Dati/Immobile.pickle'
#file_name = '../../Dati/Immobile.pickle'

class Immobile:
    #print("dentro immobile:", dir())
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

        immobili = {}
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = pickle.load(f)
        print(immobili.keys())
        for key_codice in immobili.keys():
            if key_codice == codice:
                return "L'immobile è già esistente"
        immobili[codice] = self
        with open(file_name, 'wb') as f:
            pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)
        return "Il nuovo immobile " + denominazione + " è stato inserito"

    def modificaImmobile(self,  codice = None, sigla = None, denominazione = None, codiceFiscale = None, citta = None, provincia = None, cap = None, via = None):
        if codice is not None:
            self.codice = codice
        if sigla is not None:
            self.sigla = sigla
        if denominazione is not None:
            self.denominazione = denominazione
        if codiceFiscale is not None:
            self.codiceFiscale = codiceFiscale
        if citta is not None:
            self.citta = citta
        if provincia is not None:
            self.provincia = provincia
        if cap is not None:
            self.cap = cap
        if via is not None:
            self.via = via



    def getInfoImmobile(self):
        return {
            "codice": self.codice,
            "sigla": self.sigla,
            "denominazione": self.denominazione,
            "codiceFiscale": self.codiceFiscale,
            "citta": self.citta,
            "provincia": self.provincia,
            "cap": self.cap,
            "via": self.via
        }

    @staticmethod
    def getAllImmobili():
        if os.path.isfile(file_name):
            print(2)
            with open(file_name, 'rb') as f:
                try:
                    immobili = dict(pickle.load(f))
                except EOFError:
                    immobili = {}
                return immobili
        else:
            return {}
    @staticmethod
    def ricercaImmobileByDenominazione(denominazione):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for immobile in immobili.values(): #l'errore è dato quando il file è vuoto. Fammi fa la prova da app per vedere se funziona la vista aggiungi immobile
                    if immobile.denominazione == denominazione:
                        return immobile
                return "Immobile non trovato"
        else:
            return "File non esistente"

    def ricercaImmobileBySigla(self, sigla):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for immobile in immobili.values():
                    if immobile.sigla == sigla:
                        return immobile
                return None
        else:
            return None

    @staticmethod
    def ricercaImmobileByCodice(codice):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for key in immobili.keys():
                    if key == codice:
                        return immobili[key]
                return "Immobile non trovato"
        else:
            return "File non esistente"

    @staticmethod
    def ordinaImmobileByDenominazione(isDecrescente):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                sorted_denominazione = []
                for immobile in immobili.values():
                    sorted_denominazione.append(immobile.denominazione)
                sorted_denominazione.sort(reverse=isDecrescente)

                sorted_immobili = []
                for denom in sorted_denominazione:
                    for immobile in immobili.values():
                        if immobile.denominazione == denom:
                            sorted_immobili.append(immobile)
                            break
                return sorted_immobili
        else:
            return None

    @staticmethod
    def ordinaImmobileBySigla(isDecrescente):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                sorted_sigla = []
                for immobile in immobili.values():
                    sorted_sigla.append(immobile.sigla)
                sorted_sigla.sort(reverse=isDecrescente)

                sorted_immobili = []
                for sigla in sorted_sigla:
                    for immobile in immobili.values():
                        if immobile.sigla == sigla:
                            sorted_immobili.append(immobile)
                            break
                return sorted_immobili
        else:
            return None

    @staticmethod
    def ordinaImmobileByCodice(isDecrescente):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                sorted_codice = []
                for immobile in immobili.values():
                    sorted_codice.append(immobile.codice)
                sorted_codice.sort(reverse=isDecrescente)

                sorted_immobili = []
                for codice in sorted_codice:
                    for immobile in immobili.values():
                        if immobile.codice == codice:
                            sorted_immobili.append(immobile)
                            break
                return sorted_immobili
        else:
            return None

    def rimuoviImmobile(self):
        immobili = {}
        if os.path.isfile(file_name):
            with open(file_name, "rb") as f:
                print(immobili)
                immobili = dict(pickle.load(f))
                del immobili[self.codice]
            with open(file_name, "wb") as f:
                pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)
                print("b", immobili)
            self.codice = -1
            self.sigla = ""
            self.denominazione = ""
            self.codiceFiscale = ""
            self.citta = ""
            self.provincia = ""
            self.cap = ""
            self.via = ""
            del self

if __name__ == "__main__":
    immobile1 = Immobile()
    immobile1.aggiungiImmobile(5, "ccr", "figa", "dvd", "Offida",
                                                    "AP", "63073", "Tesino")
    print(immobile1.getInfoImmobile())

