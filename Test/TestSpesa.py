import datetime
from unittest import TestCase

from Classes.Contabilita.spesa import Spesa

class TestGestioneSpesa(TestCase):
    def test_add_spesa(self):
        self.spesa = Spesa()
        self.spesa.aggiungiSpesa("descrizione Test", 2, 160.5, 1, 1, True, datetime.date.today(), datetime.date.today(), datetime.date.today(), True, 1)
        spese = Spesa.getAllSpese()
        self.assertIsNotNone(spese)
        self.assertIn(self.spesa.codice, spese)

    def test_delete_spesa(self):
        spese = Spesa.getAllSpese()

        self.assertIsNotNone(spese)
        self.assertIn(6, spese)
        self.spesa = Spesa.ricercaSpesaByCodice(6)
        self.spesa.rimuoviSpesa()

        spese = Spesa.getAllSpese()
        self.assertIsNotNone(spese)
        self.assertNotIn(6, spese)

    def test_mettiABilancio(self):
        self.spesa = Spesa.ricercaSpesaByCodice(6)
        self.spesa.mettiABilancio()
        self.spesa = Spesa.ricercaSpesaByCodice(self.spesa.codice)
        self.assertTrue(self.spesa.aBilancio)