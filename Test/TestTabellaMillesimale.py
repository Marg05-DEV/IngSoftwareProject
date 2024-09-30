import os.path
import pickle
from unittest import TestCase

from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.immobile import Immobile

nome_file = 'Dati/TabelleMillesimali.pickle'
class TestGestioneTabellaMillesimale(TestCase):
    def test_add_immobile(self):
        self.tabellaMillesimale = TabellaMillesimale()
        self.tabellaMillesimale.aggiungiTabellaMillesimale("Tab K", [1, 3], "Spesa relative all'utilizzo dei spazi comuni", Immobile.ricercaImmobileByCodice(1).id)


        tabelleMillesimali = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                tabelleMillesimali = dict(pickle.load(f))
        self.assertIsNotNone(tabelleMillesimali)
        self.assertIn(10, tabelleMillesimali)
        print("dentro add immobili", tabelleMillesimali)

    def test_delete_tabellaMillesimale(self):
        tabelleMillesimali = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tabelleMillesimali = pickle.load(f)
        self.assertIsNotNone(tabelleMillesimali)
        self.assertIn(10, tabelleMillesimali)
        self.tabellaMillesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(1)
        self.tabellaMillesimale.rimuoviTabellaMillesimale()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tabelleMillesimali = pickle.load(f)
        self.assertIsNotNone(tabelleMillesimali)
        self.assertNotIn(10, tabelleMillesimali)
        print("dentro test delete", tabelleMillesimali)

    def test_addMillesimo(self):
        pass

    def test_removeTipoSpesa(self):
        pass

    def test_addTipoSpesa(self):
        pass