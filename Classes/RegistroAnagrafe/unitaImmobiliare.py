
import os.path
import pickle
from Classes.RegistroAnagrafe.immobile import Immobile
#from immobile import Immobile
nome_file = 'Dati/UnitaImmobiliari.pickle'
#nome_file = '../../Dati/UnitaImmobiliari.pickle'

class UnitaImmobiliare:

    def __init__(self):
        self.codice = 1
        self.interno = 0
        self.foglio = 0
        self.subalterno = 0
        self.condomini = {}
        self.particella = 0
        self.tipoUnitaImmobiliare = ""
        self.categoria = ""
        self.classe = 0
        self.immobile = None
        self.scala = 0
        self.ZC = ""


    def aggiungiUnitaImmobiliare(self, foglio, subalterno, condomini, particella, interno, tipoUnitaImmobiliare, categoria, classe, immobile, scala, ZC):
        self.interno = interno
        self.foglio = foglio
        self.subalterno = subalterno
        self.condomini = condomini
        self.particella = particella
        self.tipoUnitaImmobiliare = tipoUnitaImmobiliare
        self.categoria = categoria
        self.classe = classe
        self.immobile = immobile
        self.scala = scala
        self.ZC = ZC

        unitaImmobiliari = {}
        print(nome_file)
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = dict(pickle.load(f))
                if unitaImmobiliari.keys():
                    self.codice = max(unitaImmobiliari.keys()) + 1
        unitaImmobiliari[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)
        return "L'unità immobiliare è stata inserita ", self


    def getInfoUnitaImmobiliare(self):
        print("cont: ")
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
                if value.immobile.codice == immobile.codice:
                    unitaImmobiliariByImmobile[key] = value
            return unitaImmobiliariByImmobile
        else:
            return {}


    @staticmethod
    def ricercaUnitaImmobiliareInterno(interno):
        print("dentro la ricerca")
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = dict(pickle.load(f))
                for unitaImmobiliare in unitaImmobiliari.values():
                    if unitaImmobiliare.interno == interno:
                        return unitaImmobiliare
                return None
        else:
            return None

    @staticmethod
    def ricercaUnitaImmobiliareByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = dict(pickle.load(f))
                print(unitaImmobiliari)
                print(codice)
                for cod_ui in unitaImmobiliari.keys():
                    print(cod_ui)
                    if cod_ui == codice:
                        print("dentor")
                        return unitaImmobiliari[cod_ui]
                return None
        else:
            return None

    @staticmethod
    def ordinaUnitaImmobiliariByInterno(list_unitaImmobiliari, isDecrescente):
        sorted_interno = []
        for unitaImmobiliare in list_unitaImmobiliari:
            sorted_interno.append(unitaImmobiliare.interno)
        sorted_interno.sort(reverse=isDecrescente)
        sorted_unitaImmobiliari = []
        for interno in sorted_interno:
            for unitaImmobiliare in list_unitaImmobiliari:
                if unitaImmobiliare.interno == interno:
                    sorted_unitaImmobiliari.append(unitaImmobiliare)
                    break
        for i in range(len(list_unitaImmobiliari)):
            list_unitaImmobiliari[i] = sorted_unitaImmobiliari[i]

    @staticmethod
    def ordinaUnitaImmobiliariByName(list_unitaImmobiliari, isDecrescente):
        pass

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
            self.immobile = None
            self.scala = 0
            self.ZC = ""
            del self
            return "L'assegnazione è stata eliminata"

    def addCondomino(self, condomino, titolo):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                unitaImmobiliari = dict(pickle.load(f))
                unitaImmobiliari[self.codice].condomini[condomino] = titolo
        with open(nome_file, "wb") as f:
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)
        print("oh si")

    def modificaTitoloCondomino(self, condomino, titolo):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                unitaImmobiliari = dict(pickle.load(f))
                for condomino_assoc in self.condomini.keys():
                    if condomino_assoc.codice == condomino.codice:
                        unitaImmobiliari[self.codice].condomini[condomino_assoc] = titolo
        with open(nome_file, "wb") as f:
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)

    def removeCondomino(self, condomino):
        print("condomino da eliminare", condomino)
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                unitaImmobiliari = dict(pickle.load(f))
                print("rimozione", self.getInfoUnitaImmobiliare())
                for condomino_assoc in unitaImmobiliari[self.codice].condomini.keys():
                    print("condomino ", condomino_assoc, condomino_assoc.getDatiAnagraficiCondomino())
                    if condomino_assoc.codice == condomino.codice:
                        print("rimozione", unitaImmobiliari[self.codice].condomini[condomino_assoc])
                        removed = unitaImmobiliari[self.codice].condomini.pop(condomino_assoc)
                        print(unitaImmobiliari[self.codice].condomini)
        with open(nome_file, "wb") as f:
            print("fine")
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)
            print("firn")

    def modificaUnitaImmobiliare(self, foglio, subalterno, condomini, particella, interno, tipoUnitaImmobiliare, categoria, classe, immobile, scala, ZC):
        msg = "L'Unità immobiliare dell'immobile " + self.immobile.denominazione + " è stato modificata"
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
                unitaImmobiliare[self.codice].immobile = immobile
                unitaImmobiliare[self.codice].scala = scala
                unitaImmobiliare[self.codice].ZC = ZC
                
        with open(nome_file, "wb") as f:
            pickle.dump(unitaImmobiliare, f, pickle.HIGHEST_PROTOCOL)
        return msg


    def getCondominiAssociati(self):
        condomini_associati = []
        print("ci sono")
        print("condomini: ", self.condomini)
        print(self.codice)
        ui = self.ricercaUnitaImmobiliareByCodice(self.codice)
        if ui.condomini:
            print("chiavi: ", ui.condomini.keys())
            return list(ui.condomini.keys())
        else:
            print("Non ci sono condomini associati")
            return []



if __name__ == "__main__":
    unitaImmobiliare_1 = UnitaImmobiliare()
    unitaImmobiliare_1.aggiungiUnitaImmobiliare(1, 1, {}, 1, 1, "viva", "all", 1, Immobile().ricercaImmobileByCodice(1), 1, "a")
    unitaImmobiliare_2 = UnitaImmobiliare()
    unitaImmobiliare_2.aggiungiUnitaImmobiliare(2, 2, {}, 2, 3, "negozio", "Sesso",
                                                                     2, Immobile().ricercaImmobileByCodice(1), 3, "b")
    unitaImmobiliare_3 = UnitaImmobiliare()
    unitaImmobiliare_3.aggiungiUnitaImmobiliare(3, 3, {}, 3, 4, "negozio", "Sesso",
                                                                     3, Immobile().ricercaImmobileByCodice(1),2,"c")

    print(unitaImmobiliare_3.getInfoUnitaImmobiliare())
    print(Immobile.ricercaImmobileByCodice(1))