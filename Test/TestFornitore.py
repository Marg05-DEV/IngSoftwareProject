import os.path
import pickle
from unittest import TestCase

from Classes.Contabilita.fornitore import Fornitore

nome_file = 'Dati/Fornitori.pickle'
class TestGestioneFornitori(TestCase):
    def test_add_Fornitore(self):
        self.fornitore = Fornitore()
        self.fornitore.aggiungiFornitore("Ascoli Piceno", "IM10", "contrada delle contrade", "98765432110", "spaccitt")

        fornitori = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                fornitori = dict(pickle.load(f))
        self.assertIsNotNone(fornitori)
        self.assertIn(10, fornitori)
        print("dentro add immobili", fornitori)

    def test_delete_fornitore(self):
        fornitori = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = pickle.load(f)
        self.assertIsNotNone(fornitori)
        self.assertIn(10, fornitori)
        self.fornitore = Fornitore.ricercaFornitoreByDenominazione("IM10")
        self.fornitore.rimuoviFornitore()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                fornitori = pickle.load(f)
        self.assertIsNotNone(fornitori)
        self.assertNotIn(10, fornitori)
        print("dentro test delete", fornitori)