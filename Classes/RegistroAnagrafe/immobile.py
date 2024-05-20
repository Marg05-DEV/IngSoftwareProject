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

    def modificaImmobile(self,  codice, sigla, denominazione, codiceFiscale, citta, provincia, cap, via):
        if os.path.isfile(file_name):
            with open(file_name, "rb") as f:
                immobili = dict(pickle.load(f))
                immobili[self.codice].codice = codice
                immobili[self.codice].sigla = sigla
                immobili[self.codice].denominazione = denominazione
                immobili[self.codice].codiceFiscale = codiceFiscale
                immobili[self.codice].citta = citta
                immobili[self.codice].provincia = provincia
                immobili[self.codice].cap = cap
                immobili[self.codice].via = via
                immobili[codice] = immobili[self.codice]
                del immobili[self.codice]
            with open(file_name, "wb") as f:
                pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)
                print("b", immobili)

            return "L'immobile "

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
                for immobile in immobili.values():
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
    def ordinaImmobileByDenominazione(list_immobili, isDecrescente):
        sorted_denominazione = []
        for immobile in list_immobili:
            sorted_denominazione.append(immobile.denominazione)
        sorted_denominazione.sort(reverse=isDecrescente)

        sorted_immobili = []
        for denominazione in sorted_denominazione:
            for immobile in list_immobili:
                if immobile.denominazione == denominazione:
                    sorted_immobili.append(immobile)
                    break
        for i in range(len(list_immobili)):
            list_immobili[i] = sorted_immobili[i]

    @staticmethod
    def ordinaImmobileBySigla(list_immobili, isDecrescente):
        sorted_sigla = []
        for immobile in list_immobili:
            sorted_sigla.append(immobile.sigla)
        sorted_sigla.sort(reverse=isDecrescente)

        sorted_immobili = []
        for sigla in sorted_sigla:
            for immobile in list_immobili:
                if immobile.sigla == sigla:
                    sorted_immobili.append(immobile)
                    break
        for i in range(len(list_immobili)):
            list_immobili[i] = sorted_immobili[i]

    @staticmethod
    def ordinaImmobileByCodice(list_immobili, isDecrescente=False):
        sorted_codice = []
        for immobile in list_immobili:
            sorted_codice.append(immobile.codice)
        sorted_codice.sort(reverse=isDecrescente)

        sorted_immobili = []
        for codice in sorted_codice:
            for immobile in list_immobili:
                if immobile.codice == codice:
                    sorted_immobili.append(immobile)
                    break
        for i in range(len(list_immobili)):
            list_immobili[i] = sorted_immobili[i]


    def rimuoviImmobile(self):
        immobili = {}
        nome_immobile = self.denominazione
        if os.path.isfile(file_name):
            with open(file_name, "rb") as f:
                immobili = dict(pickle.load(f))
                del immobili[self.codice]
            with open(file_name, "wb") as f:
                pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)
            self.codice = -1
            self.sigla = ""
            self.denominazione = ""
            self.codiceFiscale = ""
            self.citta = ""
            self.provincia = ""
            self.cap = ""
            self.via = ""
            del self
            return "L'immobile " + nome_immobile + " è stato rimosso"


if __name__ == "__main__":
    immobile1 = Immobile()
    immobile1.aggiungiImmobile(5, "ccr", "figa", "dvd", "Offida",
                                                    "AP", "63073", "Tesino")
    print(immobile1.getInfoImmobile())

