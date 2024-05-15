import os.path
import pickle

file_name = 'Dati/Immobile.pickle'
#file_name = '../../Dati/Immobile.pickle'

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

        immobili = {}
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = pickle.load(f)
        immobili[codice] = self
        with open(file_name, 'wb') as f:
            pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)

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
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                return immobili

    @staticmethod
    def ricercaImmobileByDenominazione(denominazione):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for immobile in immobili.values():
                    if immobile.denominazione == denominazione:
                        return immobile
                return "Immobile non trovato"
        else:
            return "File non esistente"

    @staticmethod
    def ricercaImmobileBySigla(sigla):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for immobile in immobili.values():
                    if immobile.sigla == sigla:
                        return immobile
                return "Immobile non trovato"
        else:
            return "File non esistente"

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
                        if(immobile.denominazione == denom):
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
                        if (immobile.sigla == sigla):
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
                        if (immobile.codice == codice):
                            sorted_immobili.append(immobile)
                            break
                return sorted_immobili
        else:
            return None

    def rimuoviImmobile(self):
        if os.path.isfile(file_name):
            with open(file_name, "wb+") as f:
                immobili = dict(pickle.load(f))
                del immobili[self.codice]
                pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)
            self.codice = 0
            self.sigla = ""
            self.denominazione = ""
            self.codiceFiscale = ""
            self.citta = ""
            self.provincia = ""
            self.cap = ""
            self.via = ""
