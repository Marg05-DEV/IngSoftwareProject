import datetime
import os.path
import pickle
from unittest import TestCase

from Classes.Contabilita.bilancio import Bilancio

nome_file = 'Dati/Bilanci.pickle'
class TestGestioneBilancio(TestCase):
    def test_add_bilancio(self):
        self.bilancio = Bilancio()
        self.bilancio.aggiungiBilancio(datetime.date(2024,3,4), datetime.date(2024,5,5), 2)

        bilanci = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                bilanci = dict(pickle.load(f))
        self.assertIsNotNone(bilanci)
        self.assertIn(10, bilanci)
        print("dentro add immobili", bilanci)

    def test_delete_bilancio(self):
        bilanci = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                bilanci = pickle.load(f)
        self.assertIsNotNone(bilanci)
        self.assertIn(10, bilanci)
        self.bilancio = Bilancio.ricercaBilancioByCodice(2)
        self.bilancio.rimuoviBilancio()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                bilanci = pickle.load(f)
        self.assertIsNotNone(bilanci)
        self.assertNotIn(10, bilanci)
        print("dentro test delete", bilanci)

