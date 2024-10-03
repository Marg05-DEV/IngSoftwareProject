from unittest import TestCase

from Classes.Contabilita.fornitore import Fornitore

class TestGestioneFornitori(TestCase):
    def test_add_Fornitore(self):
        self.fornitore = Fornitore()
        self.fornitore.aggiungiFornitore("Ascoli Piceno", "Energas", "Via del lavoro", "4751155555", "Ditta")

        fornitori = Fornitore.getAllFornitore()
        self.assertIsNotNone(fornitori)
        self.assertIn(self.fornitore.codice, fornitori)

    def test_delete_fornitore(self):
        fornitori = Fornitore.getAllFornitore()
        self.fornitore = Fornitore.ricercaFornitoreByDenominazione("Energas")

        self.assertIsNotNone(fornitori)
        self.assertIn(self.fornitore.codice, fornitori)
        self.fornitore.rimuoviFornitore()

        fornitori = Fornitore.getAllFornitore()
        self.assertIsNotNone(fornitori)
        self.assertNotIn(self.fornitore.codice, fornitori)