import datetime
import os.path
import pickle

nome_file='Dati/condomini.pickle'
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

    def aggiungiCondomino(self, nome, cognome, residenza, dataDiNascita, codiceFiscale, luogoDiNascita, codice, unitaImmobiliare):
        self.nome = nome
        self.cognome = cognome
        self.residenza = residenza
        self.codice = codice
        self.dataDiNascita = dataDiNascita
        self.codiceFiscale = codiceFiscale
        self.luogoDiNascita = luogoDiNascita
        self.unitaImmobiliare = unitaImmobiliare

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
        del self

    def getCondomino(self):
        return {
            "nome": self.nome,
            "cognome": self.cognome,
            "codice": self.codice,
            "residenza": self.residenza,
            "dataDiNascita": self.dataDiNascita,
            "codiceFiscale": self.codiceFiscale,
            "luogoDiNascita": self.luogoDiNascita,
            "unitaImmobiliare": self.unitaImmobiliare
        }

    def ricercaCondominoByNome(self, nome):
        if os.path.isfile(nome_file):
            with open(nome_file, '') as f:
                condomini = pickle.load(f)
                for condomino in condomini:
                    if condomino.nome == nome:
                        return condomino
                    else:
                         return "Condomino non trovato"
        else:
            return " File non esistente"




