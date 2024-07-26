import os.path
import pickle

from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
nome_file = 'Dati/TipiSpesa.pickle'

class TipoSpesa:

    def __init__(self):
        self.codice = 1
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
        return "Il tipo di spesa è stato aggiunto", self

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
        return "Tipo spesa rimosso definitivamente"

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

    @staticmethod
    def ricercaTipoSpesaByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tipiSpesa = pickle.load(f)
                for tipoSpesa in tipiSpesa.values():
                    if tipoSpesa.codice == codice:
                        return tipoSpesa
                return None
        else:
            return None


    def getInfoTipoSpesa(self):
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


    def getTabelleMillesimaliAssociate(self):
        tabelle_millesimali_associate = []
        flag = False
        tabelle_millesimali = list(TabellaMillesimale.getAllTabelleMillesimali().values())
        for tabella in tabelle_millesimali:
            for tabellaAssociata in tabelle_millesimali_associate:
                if tabellaAssociata.codice == tabella.codice:
                    flag = True
            if not flag:
                for tipo_spesa_codice in tabella.tipologiaSpesa:
                    if tipo_spesa_codice == self.codice:
                        valore = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella.codice)
                        tabelle_millesimali_associate.append(TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella.codice))
            else:
                flag = False
        return tabelle_millesimali_associate