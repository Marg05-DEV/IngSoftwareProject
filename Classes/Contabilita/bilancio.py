import datetime
import os.path
import pickle

from Classes.Contabilita.rata import Rata
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

nome_file = 'Dati/Bilanci.pickle'


class Bilancio:

    def __init__(self):
        self.codice = 1##
        self.immobile = 0##
        self.inizioEsercizio = datetime.date(year=1970, month=1, day=1)##
        self.fineEsercizio = datetime.date(year=1970, month=1, day=1)##
        self.spesePreventivate = {} ## # {TabMillesimale: {TipoSpesa: valore inserito da noi}, ...}
        self.listaSpeseAConsuntivo = []##
        self.listaSpeseNonAConsuntivo = []##
        self.speseConsuntivate = {}## # {TabMillesimale: {TipoSpesa: valore calcolato dalle spese inserite}, ...}
        self.ripartizioneSpesePreventivate = {}## # {TabMillesimale: {UnitaImmobiliare: valore calcolato tra dict spesePreventivate e tabelle millesimali}, ...}
        self.ripartizioneSpeseConsuntivate = {}## # {TabMillesimale: {UnitaImmobiliare: valore calcolato tra dict speseConsuntivate e tabelle millesimali}, ...}
        self.ripartizioneConguaglio = {}## # {UnitaImmobiliare: differenza ripartizioneSpesePrev - ripartizioneSpeseCons }
        self.conguaglioPrecedente = {}##
        self.rateVersate = {}##
        self.importiDaVersare = {}## # {UnitaImmobiliare: somma spese prev - conguaglio}, ...}
        self.numeroRate = 0##
        self.ratePreventivate = {}## # {UnitaImmobiliare: [rata 1-esima, ..., rata n-esima], ...}
        self.scadenzaRate = []##
        self.rateIsEdited = {}## #{UnitaImmobiliare: [rata 1-esima, ..., rata n-esima],}
        self.isApprovata = False##
        self.dataApprovazione = datetime.date(year=1970, month=1, day=1)##
        self.isLastEsercizio = False##
        self.passaggi = {"spesePreventivate": False, "speseConsuntivate": False, "ripartizioneSpesePreventivate": False, "ripartizioneSpeseConsuntivate": False}##

    def aggiungiBilancio(self, inizioEsercizio, fineEsercizio, immobile):
        self.inizioEsercizio = inizioEsercizio
        self.fineEsercizio = fineEsercizio
        self.immobile = immobile.id

        ultimo_bilancio = Bilancio.getLastBilancio(Immobile.ricercaImmobileById(immobile.id))

        for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(immobile.id)).values():
            there_is_tabella = False
            self.spesePreventivate[tabella.codice] = {}
            self.speseConsuntivate[tabella.codice] = {}
            self.ripartizioneSpeseConsuntivate[tabella.codice] = {}
            self.ripartizioneSpesePreventivate[tabella.codice] = {}
            for cod_tipo_spesa in tabella.tipologieSpesa:
                self.speseConsuntivate[tabella.codice][cod_tipo_spesa] = 0.0
                if ultimo_bilancio:
                    self.conguaglioPrecedente = ultimo_bilancio.ripartizioneConguaglio
                    if tabella.codice in ultimo_bilancio.spesePreventivate:
                        there_is_tabella = True

                    if cod_tipo_spesa in ultimo_bilancio.spesePreventivate[tabella.codice] and there_is_tabella:
                        self.spesePreventivate[tabella.codice][cod_tipo_spesa] = ultimo_bilancio.spesePreventivate[tabella.codice][cod_tipo_spesa]
                    else:
                        self.spesePreventivate[tabella.codice][cod_tipo_spesa] = 0.0
                else:
                    self.spesePreventivate[tabella.codice][cod_tipo_spesa] = 0.0

            for unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(immobile.id)).values():
                self.ripartizioneSpeseConsuntivate[tabella.codice][unita_immobiliare.codice] = 0.0
                self.ripartizioneSpesePreventivate[tabella.codice][unita_immobiliare.codice] = 0.0
                self.ripartizioneConguaglio[unita_immobiliare.codice] = 0.0
                self.rateIsEdited[unita_immobiliare.codice] = []


        listaSpeseNonABilancio = [item.codice for item in Spesa.getAllSpeseByImmobile(immobile).values() if not item.aBilancio]
        print("in aggiungiBilancio -> listaSpesaNonABilancio: ", listaSpeseNonABilancio)
        self.listaSpeseAConsuntivo = [item for item in listaSpeseNonABilancio if Spesa.ricercaSpesaByCodice(item).dataRegistrazione >= inizioEsercizio and Spesa.ricercaSpesaByCodice(item).dataRegistrazione <= fineEsercizio]
        print("in aggiungiBilancio -> listaSpesaAConsuntivo: ", self.listaSpeseAConsuntivo)
        self.listaSpeseNonAConsuntivo = [item for item in listaSpeseNonABilancio if item not in self.listaSpeseAConsuntivo]
        print("in aggiungiBilancio -> listaSpesaNonAConsuntivo: ", self.listaSpeseNonAConsuntivo)

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
            "passaggi": self.passaggi,
            "spesePreventivate": self.spesePreventivate,
            "listaSpeseAConsuntivo": self.listaSpeseAConsuntivo,
            "listaSpeseNonAConsuntivo": self.listaSpeseNonAConsuntivo,
            "speseConsuntivate": self.speseConsuntivate,
            "ripartizioneSpesePreventivate": self.ripartizioneSpesePreventivate,
            "ripartizioneSpeseConsuntivate": self.ripartizioneSpeseConsuntivate,
            "ripartizioneConguaglio": self.ripartizioneConguaglio,
            "conguaglioPrecedente": self.conguaglioPrecedente,
            "rateVersate": self.rateVersate,
            "importiDaVersare": self.importiDaVersare,
            "numeroRate": self.numeroRate,
            "ratePreventivate": self.ratePreventivate,
            "scadenzaRate": self.scadenzaRate,
            "rateIsEdited": self.rateIsEdited,
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
                listaSpeseNonABilancio = [item.codice for item in Spesa.getAllSpeseByImmobile(Immobile.ricercaImmobileById(bilanci[self.codice].immobile)).values() if not item.aBilancio]

                for cod_spesa in listaSpeseNonABilancio:
                    if cod_spesa not in bilanci[self.codice].listaSpeseAConsuntivo and cod_spesa not in bilanci[self.codice].listaSpeseNonAConsuntivo:
                        spesa_nel_limbo = Spesa.ricercaSpesaByCodice(cod_spesa)
                        if spesa_nel_limbo.dataRegistrazione >= bilanci[self.codice].inizioEsercizio and spesa_nel_limbo.dataRegistrazione <= bilanci[self.codice].fineEsercizio:
                            bilanci[self.codice].listaSpeseAConsuntivo.append(cod_spesa)
                        else:
                            bilanci[self.codice].listaSpeseNonAConsuntivo.append(cod_spesa)
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def changeListaConsuntivo(self, cod_spesa):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                if cod_spesa in bilanci[self.codice].listaSpeseAConsuntivo:
                    bilanci[self.codice].listaSpeseAConsuntivo.remove(cod_spesa)
                    bilanci[self.codice].listaSpeseNonAConsuntivo.append(cod_spesa)
                elif cod_spesa in bilanci[self.codice].listaSpeseNonAConsuntivo:
                    bilanci[self.codice].listaSpeseNonAConsuntivo.remove(cod_spesa)
                    bilanci[self.codice].listaSpeseAConsuntivo.append(cod_spesa)
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def calcolaSpeseConsuntivo(self):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))

                for cod_tabella in bilanci[self.codice].speseConsuntivate.keys():
                    for cod_tipo_spesa in bilanci[self.codice].speseConsuntivate[cod_tabella].keys():
                        bilanci[self.codice].speseConsuntivate[cod_tabella][cod_tipo_spesa] = 0.0

                for cod_spesa in bilanci[self.codice].listaSpeseAConsuntivo:
                    spesa = Spesa.ricercaSpesaByCodice(cod_spesa)
                    for cod_tabella in bilanci[self.codice].speseConsuntivate.keys():
                        for cod_tipo_spesa in bilanci[self.codice].speseConsuntivate[cod_tabella].keys():
                            if cod_tipo_spesa == spesa.tipoSpesa:
                                bilanci[self.codice].speseConsuntivate[cod_tabella][cod_tipo_spesa] += spesa.importo
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def passaggioRaggiunto(self, passaggio):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                bilanci[self.codice].passaggi[passaggio] = True
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def calcolaQuotaConsuntivo(self, unita_immobiliare, tabella_millesimale):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                totale_millesimi_tabella = sum(list(tabella_millesimale.millesimi.values()))
                totale_consuntivo_tabella = sum(list(bilanci[self.codice].speseConsuntivate[tabella_millesimale.codice].values()))
                if totale_millesimi_tabella:
                    bilanci[self.codice].ripartizioneSpeseConsuntivate[tabella_millesimale.codice][unita_immobiliare.codice] = (tabella_millesimale.millesimi[unita_immobiliare.codice] * totale_consuntivo_tabella) / totale_millesimi_tabella
                else:
                    bilanci[self.codice].ripartizioneSpeseConsuntivate[tabella_millesimale.codice][unita_immobiliare.codice] = 0.0
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def calcolaQuotaPreventivo(self, unita_immobiliare, tabella_millesimale):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                totale_millesimi_tabella = sum(list(tabella_millesimale.millesimi.values()))
                totale_preventivo_tabella = sum(list(bilanci[self.codice].spesePreventivate[tabella_millesimale.codice].values()))
                if totale_millesimi_tabella:
                    bilanci[self.codice].ripartizioneSpesePreventivate[tabella_millesimale.codice][unita_immobiliare.codice] = (tabella_millesimale.millesimi[unita_immobiliare.codice] * totale_preventivo_tabella) / totale_millesimi_tabella
                else:
                    bilanci[self.codice].ripartizioneSpesePreventivate[tabella_millesimale.codice][unita_immobiliare.codice] = 0.0
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def getConguaglioPrecedente(self):
        ultimo_bilancio = Bilancio.getLastBilancio(Immobile.ricercaImmobileById(self.immobile))
        unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(self.immobile)).values())
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                if ultimo_bilancio:
                    bilanci[self.codice].conguaglioPrecedente = ultimo_bilancio.ripartizioneConguaglio
                    for unita in unita_immobiliari:
                        if unita.codice not in self.conguaglioPrecedente:
                            bilanci[self.codice].conguaglioPrecedente [unita.codice] = 0.0
                else:
                    for unita in unita_immobiliari:
                        bilanci[self.codice].conguaglioPrecedente [unita.codice] = 0.0
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)


    def calcolaRateVersate(self):
        unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(self.immobile)).values())

        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                for unita in unita_immobiliari:
                    rateVersateByUnitaImmobiliare = Rata.getAllRateByUnitaImmobiliare(unita)
                    importi_rate_accettabili = [item.importo for item in rateVersateByUnitaImmobiliare.values() if item.dataPagamento >= self.inizioEsercizio and item.dataPagamento <= self.fineEsercizio]
                    if importi_rate_accettabili:
                        bilanci[self.codice].rateVersate[unita.codice] = sum(importi_rate_accettabili)
                    else:
                        bilanci[self.codice].rateVersate[unita.codice] = 0.0
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def calcolaConguaglio(self, totale_consuntivo_attuale):
        unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(self.immobile)).values())
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                for unita in unita_immobiliari:
                    bilanci[self.codice].ripartizioneConguaglio[unita.codice] = totale_consuntivo_attuale[unita.codice] + bilanci[self.codice].conguaglioPrecedente[unita.codice] - bilanci[self.codice].rateVersate[unita.codice]
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def calcolaImportiDaVersare(self, totale_preventivo_attuale):
        unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(self.immobile)).values())
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                for unita in unita_immobiliari:
                    bilanci[self.codice].importiDaVersare[unita.codice] = totale_preventivo_attuale[unita.codice] + bilanci[self.codice].ripartizioneConguaglio[unita.codice]
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def approvaBilancio(self):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                bilanci[self.codice].isApprovata = True
                bilanci[self.codice].dataApprovazione = datetime.date.today()
                if Bilancio.getLastBilancio(Immobile.ricercaImmobileById(self.immobile)):
                    bilanci[Bilancio.getLastBilancio(Immobile.ricercaImmobileById(self.immobile)).codice].isLastEsercizio = False
                bilanci[self.codice].isLastEsercizio = True
                for cod_spesa in bilanci[self.codice].listaSpeseAConsuntivo:
                    Spesa.ricercaSpesaByCodice(cod_spesa).mettiABilancio()
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def addNumeroRate(self, numeroRate):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                bilanci[self.codice].numeroRate = numeroRate
                unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(self.immobile)).values())
                for unita in unita_immobiliari:
                    bilanci[self.codice].rateIsEdited[unita.codice] = [False] * numeroRate
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def ripartizioneRate(self, cod_unita):
        list_rate = []
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                if bilanci[self.codice].numeroRate:
                    for rate in range(0, bilanci[self.codice].numeroRate):
                        list_rate.append(bilanci[self.codice].importiDaVersare[cod_unita] / bilanci[self.codice].numeroRate)
                    bilanci[self.codice].ratePreventivate[cod_unita] = list_rate
                else:
                    bilanci[self.codice].ratePreventivate[cod_unita] = list_rate
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def initScadenzaRate(self):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                if bilanci[self.codice].numeroRate:
                    months_periods = []
                    if bilanci[self.codice].numeroRate == 5:
                        months_periods = [0, 2, 5, 7, 9]
                    else:
                        months_periods = [int(12 / bilanci[self.codice].numeroRate) * i for i in range(0, bilanci[self.codice].numeroRate)]

                    bilanci[self.codice].scadenzaRate = []
                    for n_rate in range(0, bilanci[self.codice].numeroRate):
                        data_da_aggiungere = datetime.date.today()
                        if n_rate > 0:
                            month = (data_da_aggiungere.month + months_periods[n_rate]) % 12
                            year = data_da_aggiungere.year
                            if month == 0:
                                month = 12
                            if data_da_aggiungere.month + months_periods[n_rate] > 12:
                                year = data_da_aggiungere.year + 1
                            data_da_aggiungere = data_da_aggiungere.replace(year, month, 1)
                        bilanci[self.codice].scadenzaRate.append(data_da_aggiungere)
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def editDataScadenza(self, data, index):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                bilanci[self.codice].scadenzaRate[index] = data
        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)

    def editRataPreventivata(self, unita_immobiliare, numero_rata, valore):
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
                bilanci[self.codice].rateIsEdited[unita_immobiliare.codice][numero_rata] = True
                numRateNotEdited = bilanci[self.codice].rateIsEdited[unita_immobiliare.codice].count(False)
                restanteDaVersare = bilanci[self.codice].importiDaVersare[unita_immobiliare.codice]

                for i in range(0, bilanci[self.codice].numeroRate):
                    if bilanci[self.codice].rateIsEdited[unita_immobiliare.codice][i] and i != numero_rata:
                        restanteDaVersare = restanteDaVersare - bilanci[self.codice].ratePreventivate[unita_immobiliare.codice][i]

                if valore > restanteDaVersare:
                    valore = restanteDaVersare

                bilanci[self.codice].ratePreventivate[unita_immobiliare.codice][numero_rata] = valore
                restanteDaVersare = bilanci[self.codice].importiDaVersare[unita_immobiliare.codice]

                for i in range(0, bilanci[self.codice].numeroRate):
                    if bilanci[self.codice].rateIsEdited[unita_immobiliare.codice][i]:
                        restanteDaVersare = restanteDaVersare - bilanci[self.codice].ratePreventivate[unita_immobiliare.codice][i]

                quotaDaRipartire = float(restanteDaVersare)/numRateNotEdited

                for i in range(0, bilanci[self.codice].numeroRate):
                    if not bilanci[self.codice].rateIsEdited[unita_immobiliare.codice][i]:
                        bilanci[self.codice].ratePreventivate[unita_immobiliare.codice][i] = quotaDaRipartire

        with open(nome_file, "wb") as f:
            pickle.dump(bilanci, f, pickle.HIGHEST_PROTOCOL)
