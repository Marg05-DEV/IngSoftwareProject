import os
import pickle


class UnitaImmobiliare:

    def __init__(self, foglio, subalterno, condomini, millesimi, particella, tipoUnitaImmobiliare, interno):
        self.interno = 0
        self.foglio = ""
        self.subalterno = ""
        self.condomini = ""
        self.millesimi = 0
        self.particella = 0
        self.tipoUnitaImmobiliare = ""


    def aggiungiUnitaImmobiliare(self, foglio, subalterno, condomini, millesimi, particella, interno, tipoUnitaImmobiliare):
        self.interno = interno
        self.foglio = foglio
        self.subalterno = subalterno
        self.condomini = condomini
        self.millesimi = millesimi
        self.particella = particella
        self.tipoUnitaImmobiliare = tipoUnitaImmobiliare

        unitaImmobiliari = {}
        if os.path.isFile('Dati/unitaImmobiliari.pickle'):
            with open('Dati/unitaImmobiliari.pickle', 'rb' ) as f:
                unitaImmobiliari = pickle.load(f)
        unitaImmobiliari[interno] = self
        with open('Dati/unitaImmobiliari.pickle', 'wb') as f:
            pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)


    def getInfoUnitaImmobiliare(self):
        return{
            "interno": self.interno,
            "foglio": self.foglio,
            "subalterno": self.subalterno,
            "condomini": self.condomini,
            "milleismi": self.millesimi,
            "particella": self.particella,
            "tipoUnitaImmobiliare": self.tipoUnitaImmobiliare
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




