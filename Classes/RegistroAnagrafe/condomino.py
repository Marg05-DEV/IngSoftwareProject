
import datetime
import os.path
import pickle
from immobile import Immobile
from unitaImmobiliare import UnitaImmobiliare

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
            with open(nome_file, 'wb+') as f:
                condomini = pickle.load(f)
                del condomini[self.codice]
                pickle.dump(condomini, f, pickle.HIGHEST_PROTOCOL)
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
                condomini = pickle.load(f)
                return condomini

    @staticmethod
    def ricercaCondominoByNome(nome):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
                for condomino in condomini:
                    if condomino.nome == nome:
                        return condomino
                return "Condomino non trovato"
        else:
            return " File non esistente"

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

    def modificaUnitaCondomino(self, nome = None, cognome = None, residenza = None, dataDiNascita = None, codiceFiscale = None, luogoDiNascita = None, unitaImmobiliare = None, provinciaDiNascita = None, email = None, telefono = None ):
        if nome is not None:
            self.nome = nome
        if cognome is not None:
            self.cognome = cognome
        if residenza is not None:
            self.residenza = residenza
        if dataDiNascita is not None:
            self.dataDiNascita = dataDiNascita
        if codiceFiscale is not None:
            self.codiceFiscale = codiceFiscale
        if luogoDiNascita is not None:
            self.luogoDiNascita = luogoDiNascita
        if unitaImmobiliare is not None:
            self.unitaImmobiliare = unitaImmobiliare
        if provinciaDiNascita is not None:
            self.provinciaDiNascita = provinciaDiNascita
        if email is not None:
            self.email = email
        if telefono is not None:
            self.telefono = telefono

condomino1 = Condomino()
condomino1.aggiungiCondomino("Mario", "Rossi", "Offida", datetime.datetime(1968, 2, 23), "affe",
                                           "Roma", 1, UnitaImmobiliare().ricercaUnitaImmobiliareInterno(1), "Sbt", "pippo@gmail.com", "3333333333")
condomino2 = Condomino()
condomino2.aggiungiCondomino("Giovanni", "Blu", "Ascoli", datetime.datetime(2002, 5, 14), "ccr",
                                           "Sbt", 2, UnitaImmobiliare().ricercaUnitaImmobiliareInterno(2),"Firenze", "pluto@gmail.com", "4444444444" )
condomino3 = Condomino()
condomino3.aggiungiCondomino("Buls", "Verdi", "Colli", datetime.datetime(1998, 11, 15), "dvd",
                                           "Sbt", 3, UnitaImmobiliare().ricercaUnitaImmobiliareInterno(3),"Roma", "minni@gmail.com", "555555555" )
print(condomino1.getDatiAnagraficiCondomino())
print(condomino2.getDatiAnagraficiCondomino())
print(condomino3.getDatiAnagraficiCondomino())