from unittest import TestCase

from Classes.RegistroAnagrafe.immobile import Immobile

class TestGestioneImmobile(TestCase):
    def test_add_immobile(self):
        self.immobile = Immobile()
        self.immobile.aggiungiImmobile(10, "IM10", "Immobile10", "98765432110", "Offida", "AP", "63073", "Via Roma 10")

        immobili = Immobile.getAllImmobili()

        self.assertIsNotNone(immobili)
        self.assertIn(10, immobili)
        print("dentro add immobili", immobili)

    def test_delete_immobile(self):
        immobili = Immobile.getAllImmobili()

        self.assertIsNotNone(immobili)
        self.assertIn(10, immobili)
        self.immobile = Immobile.ricercaImmobileById(10)
        self.immobile.rimuoviImmobile()

        immobili = Immobile.getAllImmobili()

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
