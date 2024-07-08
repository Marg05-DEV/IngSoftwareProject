import os.path
import pickle

nome_file = 'Dati/tipiSpesa.pickle'
class TipoSpesa:

    def __init__(self):
        self.codice = 0
        self.descrizione = ""
        self.nome = ""

    def aggiungiTipoSpesa(self, descrizione, nome):
        self.descrizione = descrizione
        self.nome = nome

        tipiSpesa = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tipiSpesa = dict(pickle.load(f))
                if tipiSpesa.keys():
                    self.codice = max(tipiSpesa.keys()) + 1
        tipiSpesa[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(tipiSpesa, f, pickle.HIGHEST_PROTOCOL)
        return "Il tipo di spesa è stato aggiunto"

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
                return None
        else:
            return None


    def getTipoSpesa(self):
        return {
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

    print(tipoSpesa1.getTipoSpesa())
