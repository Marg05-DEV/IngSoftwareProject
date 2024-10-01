
import os.path
import pickle
from datetime import datetime

from Classes.RegistroAnagrafe.immobile import Immobile
#from immobile import Immobile
nome_file = 'Dati/UnitaImmobiliari.pickle'
#nome_file = '../../Dati/UnitaImmobiliari.pickle'

class UnitaImmobiliare:

    def __init__(self):
        self.codice = 1
        self.interno = 0#
        self.foglio = 0#
        self.subalterno = 0#
        self.condomini = {}#
        self.particella = 0#
        self.tipoUnitaImmobiliare = ""#
        self.categoria = ""#
        self.classe = 0#
        self.immobile = 0#
        self.scala = 0#
        self.ZC = ""#


    def aggiungiUnitaImmobiliare(self, foglio, subalterno, condomini, particella, interno, tipoUnitaImmobiliare, categoria, classe, immobile, scala, ZC):
        self.interno = interno
        self.foglio = foglio
        self.subalterno = subalterno
        self.condomini = condomini
        self.particella = particella
        self.tipoUnitaImmobiliare = tipoUnitaImmobiliare
        self.categoria = categoria
        self.classe = classe
        self.immobile = immobile.id
        self.scala = scala
        self.ZC = ZC

        unitaImmobiliari = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = dict(pickle.load(f))
                if unitaImmobiliari.keys():
                    self.codice = max(unitaImmobiliari.keys()) + 1
        unitaImmobiliari[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)
        return "L'unità immobiliare è stata inserita ", self

    def modificaUnitaImmobiliare(self, foglio, subalterno, condomini, particella, interno, tipoUnitaImmobiliare,
                                 categoria, classe, immobile, scala, ZC):
        msg = "L'unità immobiliare dell'immobile " + immobile.denominazione + " è stato modificata"
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                unitaImmobiliare = dict(pickle.load(f))

                unitaImmobiliare[self.codice].foglio = foglio
                unitaImmobiliare[self.codice].subalterno = subalterno
                unitaImmobiliare[self.codice].condomini = condomini
                unitaImmobiliare[self.codice].particella = particella
                unitaImmobiliare[self.codice].interno = interno
                unitaImmobiliare[self.codice].tipoUnitaImmobiliare = tipoUnitaImmobiliare
                unitaImmobiliare[self.codice].categoria = categoria
                unitaImmobiliare[self.codice].classe = classe
                unitaImmobiliare[self.codice].immobile = immobile.id
                unitaImmobiliare[self.codice].scala = scala
                unitaImmobiliare[self.codice].ZC = ZC

        with open(nome_file, "wb") as f:
            pickle.dump(unitaImmobiliare, f, pickle.HIGHEST_PROTOCOL)
        return msg

    def rimuoviUnitaImmobiliare(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = pickle.load(f)
                del unitaImmobiliari[self.codice]
            with open(nome_file, 'wb') as f:
                pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)
            self.interno = 0
            self.codice = -1
            self.foglio = 0
            self.subalterno = 0
            self.condomini = {}
            self.particella = 0
            self.tipoUnitaImmobiliare = ""
            self.categoria = ""
            self.classe = 0
            self.immobile = -1
            self.scala = 0
            self.ZC = ""
            del self
            return "L'assegnazione è stata eliminata"

    def getInfoUnitaImmobiliare(self):
        return{
            "interno": self.interno,
            "foglio": self.foglio,
            "subalterno": self.subalterno,
            "condomini": self.condomini,
            "particella": self.particella,
            "tipoUnitaImmobiliare": self.tipoUnitaImmobiliare,
            "categoria": self.categoria,
            "classe": self.classe,
            "immobile": self.immobile,
            "scala": self.scala,
            "ZC": self.ZC
        }

    def getDatiCatastali(self):
        return {
            "Foglio": self.foglio,
            "Particella": self.particella,
            "Subalterno": self.subalterno,
            "ZC": self.ZC,
            "Classe": self.classe,
            "Categoria": self.categoria
        }

    @staticmethod
    def ricercaUnitaImmobiliareByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = dict(pickle.load(f))
                for cod_ui in unitaImmobiliari.keys():
                    if cod_ui == codice:
                        return unitaImmobiliari[cod_ui]
                return None
        else:
            return None

    @staticmethod
    def getAllUnitaImmobiliari():
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                try:
                    unitaImmobiliari = dict(pickle.load(f))
                except EOFError:
                    unitaImmobiliari = {}
                return unitaImmobiliari
        else:
            return {}

    @staticmethod
    def getAllUnitaImmobiliariByImmobile(immobile):
        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliari()
        if unitaImmobiliari:
            unitaImmobiliariByImmobile = {}
            for key, value in unitaImmobiliari.items():
                if value.immobile == immobile.id:
                    unitaImmobiliariByImmobile[key] = value
            return unitaImmobiliariByImmobile
        else:
            return {}

    @staticmethod
    def getAllUnitaImmobiliariByCondomino(condomino):
        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliari()
        if unitaImmobiliari:
            unitaImmobiliariByCondomino = []
            for key, value in unitaImmobiliari.items():
                for codice_fiscale_condomino in value.condomini.keys():
                    if codice_fiscale_condomino == condomino.codiceFiscale:
                        unitaImmobiliariByCondomino.append(key)
            return unitaImmobiliariByCondomino
        else:
            return []

    def addCondomino(self, condomino, titolo):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                unitaImmobiliari = dict(pickle.load(f))
                unitaImmobiliari[self.codice].condomini[condomino.codiceFiscale] = titolo
        with open(nome_file, "wb") as f:
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)

    def modificaTitoloCondomino(self, condomino, titolo):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                unitaImmobiliari = dict(pickle.load(f))
                unitaImmobiliari[self.codice].condomini[condomino.codiceFiscale] = titolo
        with open(nome_file, "wb") as f:
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)

    def removeCondomino(self, condomino):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                unitaImmobiliari = dict(pickle.load(f))
                removed = unitaImmobiliari[self.codice].condomini.pop(condomino.codiceFiscale)
                if removed == "Proprietario" and len(unitaImmobiliari[self.codice].condomini) > 0:
                    for condomino_assoc in unitaImmobiliari[self.codice].condomini.keys():
                        if unitaImmobiliari[self.codice].condomini[condomino_assoc] == "Comproprietario":
                            unitaImmobiliari[self.codice].condomini[condomino_assoc] = "Proprietario"
                            break
            with open(nome_file, "wb") as f:
                pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)




