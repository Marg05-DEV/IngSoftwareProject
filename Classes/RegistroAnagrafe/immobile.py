import os.path
import pickle
import shutil

file_name = 'Dati/Immobili.pickle'
directory_files = os.path.dirname(os.path.abspath(__file__)).replace("Classes\RegistroAnagrafe", "Dati\\pdf\\")
#file_name = '../../Dati/Immobile.pickle'

class Immobile:
    def __init__(self):
        self.id = 1
        self.codice = 0#
        self.sigla = ""#
        self.denominazione = ""#
        self.codiceFiscale = ""#
        self.citta = ""#
        self.provincia = ""#
        self.cap = ""#
        self.via = ""#
        self.files_path = ""

    def aggiungiImmobile(self, codice, sigla, denominazione, codiceFiscale, citta, provincia, cap, via):
        self.codice = codice
        self.sigla = sigla
        self.denominazione = denominazione
        self.codiceFiscale = codiceFiscale
        self.citta = citta
        self.provincia = provincia
        self.cap = cap
        self.via = via

        os.makedirs(directory_files + sigla +"\\")
        self.files_path = directory_files + sigla + "\\"
        print(self.files_path)

        immobili = {}
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = pickle.load(f)
                if immobili.keys():
                    print(max(immobili.keys()))
                    self.id = max(immobili.keys()) + 1
        print(immobili.keys())
        for immobile in immobili.values():
            if immobile.codice == codice:
                return "L'immobile è già esistente"
        immobili[self.id] = self
        with open(file_name, 'wb') as f:
            pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)
        return "Il nuovo immobile " + denominazione + " è stato inserito", self

    def modificaImmobile(self,  codice, sigla, denominazione, codiceFiscale, citta, provincia, cap, via):
        msg = "L'immobile " + self.denominazione + " è stato modificato"
        if os.path.isfile(file_name):
            with open(file_name, "rb") as f:
                immobili = dict(pickle.load(f))

                immobili[self.id].files_path = directory_files + sigla + "\\"
                if sigla != self.sigla:
                    os.rename(self.files_path, immobili[self.id].files_path)
                immobili[self.id].codice = codice
                immobili[self.id].sigla = sigla
                immobili[self.id].denominazione = denominazione
                immobili[self.id].codiceFiscale = codiceFiscale
                immobili[self.id].citta = citta
                immobili[self.id].provincia = provincia
                immobili[self.id].cap = cap
                immobili[self.id].via = via
                print(immobili)
            with open(file_name, "wb") as f:
                pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)

            return msg

    def getInfoImmobile(self):
        return {
            "codice": self.codice,
            "sigla": self.sigla,
            "denominazione": self.denominazione,
            "codiceFiscale": self.codiceFiscale,
            "citta": self.citta,
            "provincia": self.provincia,
            "cap": self.cap,
            "via": self.via,
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
                return None
        else:
            return None

    @staticmethod
    def ricercaImmobileBySigla(sigla):
        print("sigla: " + sigla)
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
        codice = str(codice)
        if codice and codice.isnumeric():
            codice = int(codice)
        else:
            return None
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for immobile in immobili.values():
                    if immobile.codice == codice:
                        return immobile
                return None
        else:
            return None

    @staticmethod
    def ricercaImmobileById(id):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                immobili = dict(pickle.load(f))
                for id_immobile in immobili.keys():
                    if id_immobile == id:
                        return immobili[id_immobile]
                return None
        else:
            return None

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
                del immobili[self.id]
            with open(file_name, "wb") as f:
                pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)
            print("os", self.files_path)
            shutil.rmtree(self.files_path)
            print("os")
            self.codice = -1
            print("os")
            self.id = -1
            self.sigla = ""
            self.denominazione = ""
            self.codiceFiscale = ""
            self.citta = ""
            self.provincia = ""
            self.cap = ""
            self.via = ""
            print("os")
            del self
            print("os")
            return "L'immobile " + nome_immobile + " è stato rimosso"


if __name__ == "__main__":
    print(directory_files)
