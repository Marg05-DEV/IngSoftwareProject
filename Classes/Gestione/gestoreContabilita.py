import os
import pickle

from Classes.Contabilita.rata import Rata
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.fornitore import Fornitore
from Classes.RegistroAnagrafe.condomino import Condomino

class GestoreContabilita:
    def visualizzaCreditoCondomino(self):
        pass

    def visualizzaDebitoFornitore(self):
        pass

    def visualizzaSaldoCassa(self):
        saldo_cassa_contanti = 0.0
        saldo_cassa_A_B = 0.0
        if os.path.isfile("Dati/Rata.pickle"):
            with open("Dati/Rate.pickle", 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.tipoPagamento == "Contanti":
                        saldo_cassa_contanti += rata.importo
                    if rata.tipoPagamento == "Assegno Bancario":
                        saldo_cassa_A_B += rata.importo
                return {saldo_cassa_contanti,
                        saldo_cassa_A_B}

    def visualizzaStatoPatrimonialeSpese(self, immobile):
        if os.path.isfile("Dati/Spesa.pickle"):
            with open("Dati/Spesa.pickle", 'rb') as f:
                spese = pickle.load(f)
                for spesa in spese.values():
                    if spesa.pagata != True and spesa.immobile == immobile:
                        return "Spesa " + spesa.codice + " non pagata dell'immobile selezionato "

    def visualizzaStatoPatrimonialeRate(self):
        if os.path.isfile("Dati/Rate.pickle"):
            with open("Dati/Rate.pickle", 'rb') as f:
                rate = pickle.load(f)
                for rata in rate.values():
                    if rata.pagata != True:
                        return "Rata " + rata.codice + " non versata dell'immobile selezionato "
