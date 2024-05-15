
import os
import pickle
from Immobile import Immobile
nome_file = 'Dati/UnitaImmobiliari.pickle'
class UnitaImmobiliare:

    def __init__(self):
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
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb' ) as f:
                unitaImmobiliari = dict(pickle.load(f))
        unitaImmobiliari[interno] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)


    def getInfoUnitaImmobiliare(self):
        return{
            "interno": self.interno,
            "foglio": self.foglio,
            "subalterno": self.subalterno,
            "condomini": self.condomini,
            "particella": self.particella,
            "tipoUnitaImmobiliare": self.tipoUnitaImmobiliare,
            "categoria": self.categoria,
            "immobile": self.immobile,
            "scala": self.scala,
            "ZC": self.ZC
        }

    @staticmethod
    def ricercaUnitaImmobiliareInterno(interno):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = dict(pickle.load(f))
                for unitaImmobiliare in unitaImmobiliari.values():
                    if unitaImmobiliari.interno == interno:
                        return unitaImmobiliare
                return "L'unita' immobiliare cercata non e' presente"
        else:
            return "File non esistente"


    def rimuoviUnitaImmobiliare(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'wb+') as f:
                unitaImmobiliari = pickle.load(f)
                del unitaImmobiliari[self.interno]
        self.interno = 0
        self.foglio = ""
        self.subalterno = ""
        self.condomini = ""
        self.particella = 0
        self.tipoUnitaImmobiliare = ""
        self.categoria = ""
        self.classe = 0
        self.immobile = None
        self.scala = 0
        self.ZC = ""
        del self

    def modificaUnitaImmobiliare(self, interno = None, foglio = None, subalterno = None, condomini = None, millesimi = None, particella = None, tipoUnitaImmobiliare = None, categoria = None, immobile = None, scala = None, ZC = None ):
        if interno is not None:
            self.interno = interno
        if foglio is not None:
            self.foglio = foglio
        if subalterno is not None:
            self.subalterno = subalterno
        if condomini is not None:
            self.condomini = condomini
        if particella is not None:
            self.particella = particella
        if tipoUnitaImmobiliare is not None:
            self.tipoUnitaImmobiliare = tipoUnitaImmobiliare
        if categoria is not None:
            self.categoria = categoria
        if immobile is not None:
            self.immobile = immobile
        if scala is not None:
            self.scala = scala
        if ZC is not None:
            self.ZC = ZC

unitaImmobiliare_1 = UnitaImmobiliare()
unitaImmobiliare_1.aggiungiUnitaImmobiliare("bofo", "sodmk", "edkel,e",
                                                                 1, 34, 1, "Sesso",
                                                                 "cella", 2, Immobile.ricercaImmobileBySigla("ccr"), 1, "e" )
unitaImmobiliare_2 = UnitaImmobiliare()
unitaImmobiliare_2.aggiungiUnitaImmobiliare("sx", "rfv", "rc,e", 3, 33, 2,
                                 "tipo", "dfjejn", 2, Immobile.ricercaImmobileBySigla("ccr"), 2, "s")
unitaImmobiliare_3 = UnitaImmobiliare()
unitaImmobiliare_3.aggiungiUnitaImmobiliare("eff", "ede", "edee", 2, 35, 3,
                                            "kikko", "rnjg", 2, Immobile.ricercaImmobileBySigla("ccr"),3,"d")
