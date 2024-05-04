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
                print(sorted_denominazione)
                sorted_denominazione.sort(reverse=isDecrescente)
                print(sorted_denominazione)

                sorted_immobili = []
                for denom in sorted_denominazione:
                    for immobile in immobili.values():
                        if(immobile.denominazione == denom):
                            sorted_immobili.append(immobile)
                            break
                print(sorted_immobili)
                return sorted_immobili
        else:
            return None

    def rimuoviImmobile(self):
        pass




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

immobile1 = Immobile.ricercaImmobileByCodice(2)
Immobile.stampa(immobile1)

immobile2 = Immobile.ricercaImmobileByDenominazione("hvn")
Immobile.stampa(immobile2)

immobile3 = Immobile.ricercaImmobileBySigla("bu")
Immobile.stampa(immobile3)

immobile4 = Immobile.ordinaImmobileByDenominazione(False)
print(immobile4)
for immobile123 in immobile4:
    print(immobile123.getInfoImmobile())


#print(type(Immobile.getAllImmobili()))



print(type(Immobile.getAllImmobili()))
for immobile in Immobile.getAllImmobili():
    print(immobile)
    print(type(immobile))
    print(immobile.getInfoImmobile())
"""