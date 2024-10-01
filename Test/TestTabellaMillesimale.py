from unittest import TestCase

from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.immobile import Immobile

nome_file = 'Dati/TabelleMillesimali.pickle'
class TestGestioneTabellaMillesimale(TestCase):
    def test_add_tabellaMillesimale(self):
        self.tabellaMillesimale = TabellaMillesimale()
        self.tabellaMillesimale.aggiungiTabellaMillesimale("Tab K", [1, 3], "Spesa relative all'utilizzo dei spazi comuni", Immobile.ricercaImmobileByCodice(1).id)
        tabelleMillesimali = TabellaMillesimale.getAllTabelleMillesimali()

        self.assertIsNotNone(tabelleMillesimali)
        self.assertIn(self.tabellaMillesimale.codice, tabelleMillesimali)
        print("dentro add tabMill", self.tabellaMillesimale.codice)

    def test_delete_tabellaMillesimale(self):
        tabelleMillesimali = TabellaMillesimale.getAllTabelleMillesimali()
        self.assertIsNotNone(tabelleMillesimali)
        self.assertIn(12, tabelleMillesimali)
        self.tabellaMillesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(12)

        self.tabellaMillesimale.rimuoviTabellaMillesimale()
        tabelleMillesimali = TabellaMillesimale.getAllTabelleMillesimali()
        self.assertIsNotNone(tabelleMillesimali)
        self.assertNotIn(12, tabelleMillesimali)

    def test_addMillesimo(self):
        pass

    def test_removeTipoSpesa(self):
        pass

    def test_addTipoSpesa(self):
        pass