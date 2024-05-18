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
            with open(nome_file, 'rb') as f:
                tipiSpesa = pickle.load(f)
                del tipiSpesa[self.codice]
            with open(nome_file, 'wb') as f:
                pickle.dump(tipiSpesa, f, pickle.HIGHEST_PROTOCOL)
        self.codice = -1
        self.descrizione = ""
        self.nome = ""
        del self

    @staticmethod
    def ricercaTipoSpesaByNome(nome):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tipiSpesa = pickle.load(f)
                print(type(tipiSpesa))
                for tipoSpesa in tipiSpesa.values():
                    if tipoSpesa.nome == nome:
                        return tipoSpesa
                return "Tipo spesa non esistente"
        else:
            return "File non esistente"


    def getTipoSpesa(self):
        return {
            "codice": self.codice,
            "descrizione": self.descrizione,
            "nome": self.nome
        }

    @staticmethod
    def getAllTipoSpesa():
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                try:
                    tipoSpese = dict(pickle.load(f))
                except EOFError:
                    tipoSpese = {}
                return tipoSpese
        else:
            return {}

if __name__ == "__main__":
    tipoSpesa1 = TipoSpesa()
    tipoSpesa1.aggiungiTipoSpesa(1, "fi", "du")

    print(tipoSpesa1.getTipoSpesa())
