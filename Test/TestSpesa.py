import datetime
import os.path
import pickle
from unittest import TestCase

from Classes.Contabilita.spesa import Spesa

nome_file = 'Dati/Spesa.pickle'
class TestGestioneSpesa(TestCase):
    def test_add_spesa(self):
        self.spesa = Spesa()
        self.    spesa.aggiungiSpesa("descrizione Test", 2, 160, 1, 1, True, datetime.date.today(), datetime.date.today(), datetime.date.today(), True, 1)

        spese = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                spese = dict(pickle.load(f))
        self.assertIsNotNone(spese)
        self.assertIn(10, spese)
        print("dentro add spese", spese)

    def test_delete_spesa(self):
        spese = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = pickle.load(f)
        self.assertIsNotNone(spese)
        self.assertIn(10, spese)
        self.spesa = Spesa.ricercaSpesaByCodice(1)
        self.spesa.rimuoviSpesa()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                spese = pickle.load(f)
        self.assertIsNotNone(spese)
        self.assertNotIn(10, spese)
        print("dentro test delete", spese)

    def test_mettiABilancio(self):
        pass