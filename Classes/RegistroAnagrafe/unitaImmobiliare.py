
import os.path
import pickle
from Classes.RegistroAnagrafe.immobile import Immobile
nome_file = 'Dati/UnitaImmobiliari.pickle'
#nome_file = '../../Dati/UnitaImmobiliari.pickle'

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
        print(nome_file)
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
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
    def getAllUnitaImmobiliari():
        try:
            with open(nome_file, 'rb') as f:
                data = pickle.load(f)
                print("Dati caricati:", data)
                print("Tipo di dati caricati:", type(data))
        except EOFError:
            print("EOFError: il file è vuoto.")
        except pickle.UnpicklingError as e:
            print(f"UnpicklingError: errore durante il caricamento del file - {e}")
        except Exception as e:
            print(f"Errore sconosciuto: {e}")

        if os.path.isfile(nome_file):
            print("dentro")
            with open(nome_file, 'rb') as f:
                try:
                    print("dentro al try")
                    unitaImmobiliari = dict(pickle.load(f))
                except EOFError:
                    print("EOF")
                    unitaImmobiliari = {}
                #print(unitaImmobiliari.values())
                return unitaImmobiliari
        else:
            return {}

    @staticmethod
    def ricercaUnitaImmobiliareInterno(interno):
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
    def ordinaCondominoByInterno(list_unitaImmobiliari, isDecrescente):
        print("presente")
        sorted_dati_catastali = []
        for unitaImmobiliare in list_unitaImmobiliari:
            sorted_dati_catastali.append(unitaImmobiliare.interno)
        sorted_dati_catastali.sort(reverse=isDecrescente)
        sorted_unitaImmobilairi = []
        for interno in sorted_dati_catastali:
            for unitaImmobiliare in list_unitaImmobiliari:
                if unitaImmobiliare.interno == interno:
                    sorted_unitaImmobilairi.append(unitaImmobiliare)
                    break

        for i in range(len(list_unitaImmobiliari)):
            list_unitaImmobiliari[i] = sorted_unitaImmobilairi[i]


    def rimuoviUnitaImmobiliare(self):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = pickle.load(f)
                del unitaImmobiliari[self.interno]
            with open(nome_file, 'wb') as f:
                pickle.dump(unitaImmobiliari, f, pickle.HIGHEST_PROTOCOL)
        self.interno = -1
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

    def modificaUnitaImmobiliare(self, foglio = None, subalterno = None, condomini = None, particella = None, interno = None, tipoUnitaImmobiliare = None, categoria = None, classe = None, immobile = None, scala = None, ZC = None ):
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