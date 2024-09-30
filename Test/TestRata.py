import datetime
import os.path
import pickle
from unittest import TestCase

from Classes.Contabilita.rata import Rata

nome_file = 'Dati/Rate.pickle'
class TestGestioneRata(TestCase):
    def test_add_rata(self):
        self.rata = Rata()
        self.rata.aggiungiRata(datetime.date.today(), "Versamento Rata 22/24", 130.60, 1, "Bonifico bancario", 1, "Gianni Rossi")


        rate = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                rate = dict(pickle.load(f))
        self.assertIsNotNone(rate)
        self.assertIn(10, rate)
        print("dentro add immobili", rate)

    def test_delete_rata(self):
        rate = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
        self.assertIsNotNone(rate)
        self.assertIn(10, rate)
        self.rata = Rata.ricercaRataByCodice(1)
        self.rata.rimuoviRata()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                rate = pickle.load(f)
        self.assertIsNotNone(rate)
        self.assertNotIn(10, rate)
        print("dentro test delete", rate)

    def test_lastNumeroRicevuta(self):
        pass