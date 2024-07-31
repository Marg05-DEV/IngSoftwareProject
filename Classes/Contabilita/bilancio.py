import datetime
import os.path
import pickle

from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.immobile import Immobile

nome_file = 'Dati/Bilanci.pickle'


class Bilancio:

    def __init__(self):
        self.codice = 1
        self.immobile = None
        self.inizioEsercizio = datetime.date(year=1970, month=1, day=1)
        self.fineEsercizio = datetime.date(year=1970, month=1, day=1)
        self.spesePreventivate = {} # {TabMillesimale: {TipoSpesa: valore inserito da noi}, ...}
        self.listaSpeseAConsuntivo = []
        self.speseConsuntivate = {} # {TabMillesimale: {TipoSpesa: valore calcolato dalle spese inserite}, ...}
        self.ripartizioneSpesePreventivate = {} # {TabMillesimale: {UnitaImmobiliare: valore calcolato tra dict spesePreventivate e tabelle millesimali}, ...}
        self.ripartizioneSpeseConsuntivate = {} # {TabMillesimale: {UnitaImmobiliare: valore calcolato tra dict speseConsuntivate e tabelle millesimali}, ...}
        self.ripartizioneConguaglio = {} # {TabMillesimale: {UnitaImmobiliare: differenza ripartizioneSpesePrev - ripartizioneSpeseCons }, ...}
        self.importiDaVersare = {} # {UnitaImmobiliare: somma spese prev - conguaglio}, ...}
        self.numeroRate = 0
        self.ratePreventivate = {} # {UnitaImmobiliare: [rata 1-esima, ..., rata n-esima], ...}
        self.isApprovata = False
        self.dataApprovazione = datetime.date(year=1970, month=1, day=1)
        self.isLastEsercizio = False
        
    def aggiungiBilancio(self, inizioEsercizio, fineEsercizio, immobile):
        self.inizioEsercizio = inizioEsercizio
        self.fineEsercizio = fineEsercizio
        self.immobile = immobile.id

        ultimo_bilancio = Bilancio.getLastBilancio(Immobile.ricercaImmobileById(immobile))

        for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(immobile.id)).values():
            there_is_tabella = False
            self.spesePreventivate[tabella.codice] = {}
            self.speseConsuntivate[tabella.codice] = {}
            for cod_tipo_spesa in tabella.tipologieSpesa:
                self.speseConsuntivate[tabella.codice][cod_tipo_spesa] = 0.0
                if ultimo_bilancio:
                    if tabella.codice in ultimo_bilancio.spesePreventivate:
                        there_is_tabella = True
                    if cod_tipo_spesa in ultimo_bilancio.spesePreventivate[tabella.codice] and there_is_tabella:
                        self.spesePreventivate[tabella.codice][cod_tipo_spesa] = ultimo_bilancio.spesePreventivate[tabella.codice][cod_tipo_spesa]
                    else:
                        self.spesePreventivate[tabella.codice][cod_tipo_spesa] = 0.0
                else:
                    self.spesePreventivate[tabella.codice][cod_tipo_spesa] = 0.0

        self.listaSpeseAConsuntivo = [item.codice for item in Spesa.getAllSpeseByPeriodoBilancio(immobile, inizioEsercizio, fineEsercizio).values()]

        print(self.spesePreventivate)
        print(self.speseConsuntivate)
        print(self.listaSpeseAConsuntivo)

        bilanci = {}
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                bilanci = dict(pickle.load(f))
                if bilanci.keys():
                    self.codice = max(bilanci.keys()) + 1
        bilanci[self.codice] = self
        with open(nome_file, 'wb') as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)
        return "Il bilancio è stato creato", self

    def getInfoBilancio(self):
        return {
            "codice": self.codice,
            "inizioEsercizio": self.inizioEsercizio,
            "fineEsercizio": self.fineEsercizio,
            "immobile": self.immobile,
            "spesePreventivate": self.spesePreventivate,
            "listaSpeseAConsuntivo": self.listaSpeseAConsuntivo,
            "speseConsuntivate": self.speseConsuntivate,
            "ripartizioneSpesePreventivate": self.ripartizioneSpesePreventivate,
            "ripartizioneSpeseConsuntivate": self.ripartizioneSpeseConsuntivate,
            "ripartizioneConguaglio": self.ripartizioneConguaglio,
            "importiDaVersare": self.importiDaVersare,
            "numeroRate": self.numeroRate,
            "ratePreventivate": self.ratePreventivate,
            "isApprovata": self.isApprovata,
            "dataApprovazione": self.dataApprovazione,
            "isLastEsercizio": self.isLastEsercizio
        }

    @staticmethod
    def getAllBilanci():
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                try:
                    bilanci = dict(pickle.load(f))
                except EOFError:
                    bilanci = {}
                return bilanci
        else:
            return {}

    @staticmethod
    def getAllBilanciByImmobile(immobile):
        bilanci = Bilancio.getAllBilanci()
        if bilanci:
            bilanciByImmobile = {}
            for key, value in bilanci.items():
                if value.immobile == immobile.id:
                    bilanciByImmobile[key] = value
            return bilanciByImmobile
        else:
            return {}

    @staticmethod
    def getLastBilancio(immobile):
        bilanci_immobile = Bilancio.getAllBilanciByImmobile(immobile)
        ultimo_bilancio = 0

        for bilancio in bilanci_immobile.values():
            if bilancio.isLastEsercizio:
                ultimo_bilancio = bilancio

        return ultimo_bilancio

    @staticmethod
    def ricercaBilancioByCodice(codice):
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                bilanci = dict(pickle.load(f))
                for bilancio in bilanci.values():
                    if bilancio.codice == codice:
                        return bilancio
                return None
        else:
            return None
    @staticmethod
    def ordinaBilancioByDataInizio(list_bilanci):
        sorted_data_inizio = []
        for bilancio in list_bilanci:
            sorted_data_inizio.append(bilancio.inizioEsercizio)
        sorted_data_inizio.sort(reverse=True)

        sorted_bilanci = []
        for inizio_esercizio in sorted_data_inizio:
            for bilancio in list_bilanci:
                if bilancio.inizioEsercizio == inizio_esercizio:
                    sorted_bilanci.append(bilancio)
                    break
        for i in range(len(list_bilanci)):
            list_bilanci[i] = sorted_bilanci[i]

    def addImportoPreventivato(self, cod_tabella, cod_tipo_spesa, importo):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                bilanci[self.codice].spesePreventivate[cod_tabella][cod_tipo_spesa] = importo
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def addImportoConsuntivato(self, codice_tabella_millesimale, codice_tipo_spesa, importo):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                bilanci[self.codice].speseConsuntivate[codice_tabella_millesimale][codice_tipo_spesa] = importo
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def aggiornaListaSpeseAConsuntivo(self):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                bilanci[self.codice].listaSpeseAConsuntivo = [item.codice for item in Spesa.getAllSpeseByPeriodoBilancio(Immobile.ricercaImmobileById(self.immobile), self.inizioEsercizio, self.fineEsercizio).values()]
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def calcolaSpeseConsuntivo(self):
        print("dentro calcola spese consuntivo")
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))

                for cod_tabella in bilanci[self.codice].speseConsuntivate.keys():
                    for cod_tipo_spesa in bilanci[self.codice].speseConsuntivate[cod_tabella].keys():
                        bilanci[self.codice].speseConsuntivate[cod_tabella][cod_tipo_spesa] = 0.0

                for cod_spesa in bilanci[self.codice].listaSpeseAConsuntivo:
                    spesa = Spesa.ricercaSpesaByCodice(cod_spesa)
                    print("scorrendo spese", spesa.getInfoSpesa())
                    print("bilancio selezioanto", bilanci[self.codice].getInfoBilancio())
                    for cod_tabella in bilanci[self.codice].speseConsuntivate.keys():
                        print("---------- scorrendo tabelle", cod_tabella)
                        for cod_tipo_spesa in bilanci[self.codice].speseConsuntivate[cod_tabella].keys():
                            print("---------------------- scorrendo tipi spesa", cod_tipo_spesa)
                            if cod_tipo_spesa == spesa.tipoSpesa:
                                bilanci[self.codice].speseConsuntivate[cod_tabella][cod_tipo_spesa] += spesa.importo
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)


