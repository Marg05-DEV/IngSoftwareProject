import datetime
import os.path
import pickle

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

#nome_file='../../Dati/Condomini.pickle'
nome_file = 'Dati/Condomini.pickle'

class Condomino:
    def __init__(self):
        self.nome = ""
        self.cognome = ""
        self.residenza = ""
        self.codice = 1
        self.dataDiNascita = datetime.date(year=1970, month=1, day=1)
        self.codiceFiscale = ""
        self.luogoDiNascita = ""
        self.provinciaDiNascita = ""
        self.email = ""
        self.telefono = ""

    def aggiungiCondomino(self, nome, cognome, residenza, dataDiNascita, codiceFiscale, luogoDiNascita, provincia, email, telefono):
        self.nome = nome
        self.cognome = cognome
        self.residenza = residenza
        self.dataDiNascita = dataDiNascita
        self.codiceFiscale = codiceFiscale
        self.luogoDiNascita = luogoDiNascita
        self.provinciaDiNascita = provincia
        self.email = email
        self.telefono = telefono

        condomini = {}

        if os.path.isfile(nome_file):
            print("il file è esistente")
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
                if condomini.keys():
                    self.codice = max(condomini.keys()) + 1
        condomini[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(condomini, f, pickle.HIGHEST_PROTOCOL)
        return "Il condomino è stato aggiunto", self

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
        self.dataDiNascita = datetime.date(year=1970, month=1, day=1)
        self.codiceFiscale = ""
        self.luogoDiNascita = ""
        self.provinciaDiNascita = ""
        self.email = ""
        self.telefono = ""
        del self
        return "Il condomino è stato rimosso definitivamente"

    def getDatiAnagraficiCondomino(self):
        return {
            "nome": self.nome,
            "cognome": self.cognome,
            "codice": self.codice,
            "residenza": self.residenza,
            "dataDiNascita": self.dataDiNascita,
            "codiceFiscale": self.codiceFiscale,
            "luogoDiNascita": self.luogoDiNascita,
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
    def ricercaCondominoByCF(CF):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
                for condomino in condomini.values():
                    if condomino.codiceFiscale == CF:
                        return condomino
                return None
        else:
            return None

    @staticmethod
    def ordinaCondominoByNominativo(list_condomini, isDecrescente):
        sorted_nominativo = []
        for condomino in list_condomini:
            sorted_nominativo.append(condomino.cognome + " "+ condomino.nome)
        sorted_nominativo.sort(reverse=isDecrescente)
        sorted_condomini = []
        for nominativo in sorted_nominativo:
            for condomino in list_condomini:
                if (condomino.cognome + " " +condomino.nome) == nominativo:
                    sorted_condomini.append(condomino)
                    break
        for i in range(len(list_condomini)):
            list_condomini[i] = sorted_condomini[i]

    def modificaCondomino(self, nome, cognome, residenza, dataDiNascita, codiceFiscale, luogoDiNascita, provincia, email, telefono):
        print("ciao")
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                condomini = dict(pickle.load(f))
                print(condomini)
                condomini[self.codice].nome = nome
                condomini[self.codice].cognome = cognome
                condomini[self.codice].residenza = residenza
                condomini[self.codice].dataDiNascita = dataDiNascita
                condomini[self.codice].codiceFiscale = codiceFiscale
                condomini[self.codice].luogoDiNascita = luogoDiNascita
                condomini[self.codice].provincia = provincia
                condomini[self.codice].email = email
                condomini[self.codice].telefono = telefono
            with open(nome_file, "wb") as f:
                pickle.dump(condomini, f, pickle.HIGHEST_PROTOCOL)
                print("b", condomini)

            return "Il condomino " + cognome + " " + nome + " è stato modificato"

    def getImmobiliAssociati(self):
        immobili_associati = []
        flag = False
        unitaImmobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliari().values())
        for unitaImmobiliare in unitaImmobiliari:
            for immobileAssociato in immobili_associati:
                if immobileAssociato.codice == unitaImmobiliare.immobile.codice:
                    flag = True
            if not flag:
                for condomino in unitaImmobiliare.condomini.keys():
                    if condomino.codice == self.codice:
                        immobili_associati.append(unitaImmobiliare.immobile)
            else:
                flag = False

        return immobili_associati
