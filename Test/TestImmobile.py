import os.path
import pickle
from unittest import TestCase

from Classes.RegistroAnagrafe.immobile import Immobile

nome_file = 'Dati/Immobili.pickle'
class TestGestioneImmobile(TestCase):
    def test_add_immobile(self):
        self.immobile = Immobile()
        self.immobile.aggiungiImmobile(10, "IM10", "Immobile10", "98765432110", "Offida", "AP", "63073", "Via Roma 10")

        immobili = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                immobili = dict(pickle.load(f))
        self.assertIsNotNone(immobili)
        self.assertIn(10, immobili)
        print("dentro add immobili", immobili)

    def test_delete_immobile(self):
        immobili = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                immobili = pickle.load(f)
        self.assertIsNotNone(immobili)
        self.assertIn(10, immobili)
        self.immobile = Immobile.ricercaImmobileById(10)
        self.immobile.rimuoviImmobile()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                immobili = pickle.load(f)
        self.assertIsNotNone(immobili)
        self.assertNotIn(10, immobili)
        print("dentro test delete", immobili)

    def test_getAllImmobili(self):
        print()
        pass

    def test_modifica_immobile(self):
        pass

    def test_ricercaImmobileByDenominazione(self):
        pass

    def test_ordinaImmobileByDenominazione(self):
        pass
