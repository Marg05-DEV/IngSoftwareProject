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
        #print("dentro immobile:", dir())
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
            with open(file_name, 'rb') as f:#che succede?Appena chiudi fai il commit
                try:
                    immobili = dict(pickle.load(f))
                except EOFError:
                    immobili = {} #funziona. Ho provato prima ma per ora non lo faccio. C'è sicuramente un problema sulla function rimuoviImmobile
                    #Fra un po finisco lezione. Non so se chiudendo il computer la sessione si blocca. Io mo lo faccio ma se è aspettati che il tempo di arriva e mi ci rimetto
                return immobili
        else:
            return {}#ora esco dalla sessione, 

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
        if os.path.isfile(file_name):
            with open(file_name, "wb+") as f:
                immobili = dict(pickle.load(f))
                del immobili[str(self.codice)]
                pickle.dump(immobili, f, pickle.HIGHEST_PROTOCOL)
        self.codice = 0
        self.sigla = ""
        self.denominazione = ""
        self.codiceFiscale = ""
        self.citta = ""
        self.provincia = ""
        self.cap = ""
        self.via = ""
        del self

# il blocco dentro l'if viene avviato solo se viene avviata direttamente la classe immobile
# Quindi arrivando dal file main non verrà fatto il seguente blocco
# Invece quando fai da terminale python .../Immobilie.py te lo dovrebbe fare

#mi continua a da errore
#EOFError: Ran out of input

if __name__ == "__main__":
    immobile1 = Immobile()
    immobile1.aggiungiImmobile(1, "ccr", "figa", "dvd", "Offida",
                                                    "AP", "63073", "Tesino")
    print(immobile1.getInfoImmobile())

