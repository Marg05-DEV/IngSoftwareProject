import os.path
import pickle

nome_file = 'Dati/tipiSpesa.pickle'
class TipoSpesa:

    def __init__(self):
        self.codice = 0
        self.descrizione = ""
        self.nome = ""

    def aggiungiTipoSpesa(self, codice, descrizione, nome):
        self.codice = codice
        self.descrizione = descrizione
        self.nome = nome

        tipiSpesa = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tipiSpesa = dict(pickle.load(f))
        tipiSpesa[codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(tipiSpesa, f, pickle.HIGHEST_PROTOCOL)

    def rimuoviTipoSpesa(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'wb+') as f:
                tipiSpesa = pickle.load(f)
                del tipiSpesa[self.codice]
        self.codice = 0
        self.descrizione = ""
        self.nome = ""
        del self

    def ricercaTipoSpesaByNome(self,nome):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tipiSpesa = pickle.load(f)
            for tipoSpesa in tipiSpesa:
                if tipoSpesa.nome == nome:
                    return tipoSpesa
                else:
                    return "Tipo spesa non esistente"
        else:
            return "File non esistente"


    def getSpesa(self):
        return {
            "codice": self.codice,
            "descrizione": self.descrizione,
            "nome": self.nome
        }
