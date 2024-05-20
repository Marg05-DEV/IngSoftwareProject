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

    def visualizzaStatoPatrimoniale(self):
        pass
