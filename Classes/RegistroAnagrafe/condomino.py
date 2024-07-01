
import datetime
import os.path
import pickle

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

nome_file = 'Dati/Condomini.pickle'
class Condomino:
    def __init__(self):
        self.nome = ""
        self.cognome = ""
        self.residenza = ""
        self.codice = 0
        self.dataDiNascita = datetime.datetime(year=1970, month=1, day=1)
        self.codiceFiscale = ""
        self.luogoDiNascita = ""
        self.unitaImmobiliare = None
        self.provinciaDiNascita = ""
        self.email = ""
        self.telefono = ""

    def aggiungiCondomino(self, nome, cognome, residenza, dataDiNascita, codiceFiscale, luogoDiNascita, codice, unitaImmobiliare, provincia, email, telefono):
        self.nome = nome
        self.cognome = cognome
        self.residenza = residenza
        self.codice = codice
        self.dataDiNascita = dataDiNascita
        self.codiceFiscale = codiceFiscale
        self.luogoDiNascita = luogoDiNascita
        self.unitaImmobiliare = unitaImmobiliare
        self.provinciaDiNascita = provincia
        self.email = email
        self.telefono = telefono

        condomini = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
        condomini[codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(condomini, f, pickle.HIGHEST_PROTOCOL)

    def rimuoviCondomino(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
                del condomini[self.codice]
            with open(nome_file, 'wb') as f:
                pickle.dump(condomini, f, pickle.HIGHEST_PROTOCOL)
        self.nome = ""
        self.cognome = ""
        self.residenza = ""
        self.codice = -1
        self.dataDiNascita = datetime.datetime(year=1970, month=1, day=1)
        self.codiceFiscale = ""
        self.luogoDiNascita = ""
        self.unitaImmobiliare = None
        self.provinciaDiNascita = ""
        self.email = ""
        self.telefono = ""
        del self

    def getDatiAnagraficiCondomino(self):
        return {
            "nome": self.nome,
            "cognome": self.cognome,
            "codice": self.codice,
            "residenza": self.residenza,
            "dataDiNascita": self.dataDiNascita,
            "codiceFiscale": self.codiceFiscale,
            "luogoDiNascita": self.luogoDiNascita,
            "unitaImmobiliare": self.unitaImmobiliare,
            "provinciaDiNascita" : self.provinciaDiNascita,
            "email" : self.email,
            "telefono" : self.telefono
        }

    @staticmethod
    def getAllCondomini():
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                try:
                    condomini = dict(pickle.load(f))
                except EOFError:
                    condomini = {}
                return condomini
        else:
            return {}

    @staticmethod
    def ricercaCondominoByNome(nome):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
                for condomino in condomini.values():
                    if condomino.nome == nome:
                        return condomino
                return None
        else:
            return None

    @staticmethod
    def ordinaCondominoByName(isDecrescente):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = dict(pickle.load(f))
                sorted_nome = []
                for condomino in condomini.values():
                    sorted_nome.append(condomino.nome)
                sorted_nome.sort(reverse=isDecrescente)
                sorted_condomini = []
                for nome in sorted_nome:
                    for condomino in condomini.values():
                        if (condomino.nome == nome):
                            sorted_condomini.append(condomino)
                            break
                return sorted_condomini
        else:
            return None

    def modificaUnitaCondomino(self, nome, cognome, residenza, dataDiNascita, codiceFiscale, luogoDiNascita, codice, unitaImmobiliare, provincia, email, telefono):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                condomini = dict(pickle.load(f))
                condomini[self.codice].codice = codice
                condomini[self.codice].nome = nome
                condomini[self.codice].cognome = cognome
                condomini[self.codice].residenza = residenza
                condomini[self.codice].dataDiNascita = dataDiNascita
                condomini[self.codice].codiceFiscale = codiceFiscale
                condomini[self.codice].luogoDiNascita = luogoDiNascita
                condomini[self.codice].unitaImmobiliare = unitaImmobiliare
                condomini[self.codice].provincia = provincia
                condomini[self.codice].email = email
                condomini[self.codice].telefono = telefono
                condomini[codice] = condomini[self.codice]
                del condomini[self.codice]
            with open(nome_file, "wb") as f:
                pickle.dump(condomini, f, pickle.HIGHEST_PROTOCOL)
                print("b", condomini)

            return "Il condomino"
if __name__ == "__main__":
    condomino1 = Condomino()
    condomino1.aggiungiCondomino("Mario", "Rossi", "Offida", datetime.datetime(1968, 2, 23), "affe",
                                               "Roma", 1, UnitaImmobiliare().ricercaUnitaImmobiliareInterno(1), "Sbt", "pippo@gmail.com", "3333333333")
    condomino2 = Condomino()
    condomino2.aggiungiCondomino("Giovanni", "Blu", "Ascoli", datetime.datetime(2002, 5, 14), "ccr",
                                               "Sbt", 2, UnitaImmobiliare().ricercaUnitaImmobiliareInterno(2),"Firenze", "pluto@gmail.com", "4444444444" )
    condomino3 = Condomino()
    condomino3.aggiungiCondomino("Buls", "Verdi", "Colli", datetime.datetime(1998, 11, 15), "dvd",
                                               "Sbt", 3, UnitaImmobiliare().ricercaUnitaImmobiliareInterno(3),"Roma", "minni@gmail.com", "555555555" )
    #print(condomino1.getDatiAnagraficiCondomino())
    condomino1.modificaUnitaCondomino("Fica", "Rossi", "Offida", datetime.datetime(1968, 2, 23), "affe",
                                               "Roma", 1, UnitaImmobiliare().ricercaUnitaImmobiliareInterno(2), "Sbt", "pippo@gmail.com", "3333333333")
    #print(condomino1.getDatiAnagraficiCondomino())

    print(Condomino.getAllCondomini())