import os
import pickle

import Immobile

nome_file = 'Dati/unitaImmobiliari.pickle'
class UnitaImmobiliare:

    def __init__(self, foglio, subalterno, condomini, millesimi, particella, tipoUnitaImmobiliare, interno):
        self.interno = 0
        self.foglio = ""
        self.subalterno = ""
        self.condomini = ""
        self.millesimi = 0
        self.particella = 0
        self.tipoUnitaImmobiliare = ""
        self.categoria = ""
        self.classe = 0
        self.immobile = None
        self.scala = 0
        self.ZC = ""


    def aggiungiUnitaImmobiliare(self, foglio, subalterno, condomini, millesimi, particella, interno, tipoUnitaImmobiliare, categoria, classe, immobile, scala, ZC):
        self.interno = interno
        self.foglio = foglio
        self.subalterno = subalterno
        self.condomini = condomini
        self.millesimi = millesimi
        self.particella = particella
        self.tipoUnitaImmobiliare = tipoUnitaImmobiliare
        self.categoria = categoria
        self.classe = classe
        self.immobile = immobile
        self.scala = scala
        self.ZC = ZC

        unitaImmobiliari = {}
        if os.path.isFile('Dati/unitaImmobiliari.pickle'):
            with open('Dati/unitaImmobiliari.pickle', 'rb' ) as f:
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
            "milleismi": self.millesimi,
            "particella": self.particella,
            "tipoUnitaImmobiliare": self.tipoUnitaImmobiliare,
            "categoria": self.categoria,
            "immobile": self.immobile,
            "scala": self.scala,
            "ZC": self.ZC
        }

    def ricercaUnitaImmobiliareInterno(self,interno):
        if os.path.isfile('Dati/unitaImmobiliari.pickle'):
            with open('Dati/unitaImmobiliari.pickle', 'rb') as f:
                unitaImmobiliari = dict(pickle.loaf(f))
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
        self.millesimi = 0
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
        if millesimi is not None:
            self.millesimi = millesimi
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



