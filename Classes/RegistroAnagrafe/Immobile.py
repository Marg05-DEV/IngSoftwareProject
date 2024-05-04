import os.path
import pickle

file_name = 'Dati/Immobile.pickle'

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
        print("oggetto creato: ", self)

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
                immobili = dict(pickle.load(f))
        print(immobili)
        immobili[codice] = self
        with open(file_name, 'wb') as f:
                pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)

        print(immobili)

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
        dict_immobili = {}
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                print("2.1.2")
                dict_immobili = dict(pickle.load(f))
                print("2.1.3")
                return list(dict_immobili.values())
        return []

    def ricercaImmobileByDenominazione(self, denominazione):
        file_name = "../../Dati/Immobile.pickle"
        cont = 0
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for immobile in immobili.values():
                    if immobile.denominazione == denominazione:
                        return immobile
                    elif cont == 0:
                        return "Non ci sono Immobili con questa denominazione"
                return None
        else:
            return "File non esistente"

    @staticmethod
    def ricercaImmobileBySigla(sigla):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = list(pickle.load(f))
                for immobile in immobili.values():
                    if immobile.sigla == sigla:
                        return immobile
                return "Non ci sono Immobili con questa sigla"
        else:
            return "File non esistente"


    def ricercaImmobileByCodice(self, codice):
        file_name = "../../Dati/Immobile.pickle"
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for key in immobili.keys():
                    if key == codice:
                        return immobili[key]

                return "Non ci sono Immobili con questo codice"
        else:
            return "File non esistente"

    def ordinaImmobileByDenominazione(self, crescente):
        file_name = "../../Dati/Immobile.pickle"
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))

                immobili_ordinati = sorted(immobili)
                return immobili_ordinati
        else:
            return "File non esistente"




    def stampa(self):
        if type(self) == str:
            print(self)
        else:
            print(self.getInfoImmobile())


"""
immo1 = Immobile()
immo2 = Immobile()
immo3 = Immobile()
immo1.aggiungiImmobile(1, "ou", "fac", "jnknnf", "Ascoli", "Ascoli", "63073", 'Tesiono')
immo2.aggiungiImmobile(2, "bu", "mic", "sdfasdf", "Offida", "Ascoli", "687120", 'Cozza')
immo3.aggiungiImmobile(7, "ad", "bcc", "jvnak", "ASTI", "aSTI", "98745", 'Azzi')

if os.path.isfile(file_name):
    with open(file_name, 'rb') as f:
        immobili_list1 = list(pickle.load(f))

print(immobili_list1)

immobile1 = Immobile.ricercaImmobileByCodice(45)
print(immobile1.getInfoImmobile())
