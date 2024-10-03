from unittest import TestCase

from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

class TestGestioneTabellaMillesimale(TestCase):
    def test_add_tabellaMillesimale(self):
        self.tabellaMillesimale = TabellaMillesimale()
        self.tabellaMillesimale.aggiungiTabellaMillesimale("Tab K", [1, 3], "Spesa relative all'utilizzo dei spazi comuni", Immobile.ricercaImmobileByCodice(1).id)
        tabelleMillesimali = TabellaMillesimale.getAllTabelleMillesimali()

        self.assertIsNotNone(tabelleMillesimali)
        self.assertIn(self.tabellaMillesimale.codice, tabelleMillesimali)

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
        tabellaMillesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(12)
        tabellaMillesimale.addMillesimo(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(1), 100.56)
        tabellaMillesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabellaMillesimale.codice)

        self.assertEqual(100.56, tabellaMillesimale.millesimi[1])

    def test_addTipoSpesa(self):
        tabellaMillesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(12)
        tipoSpesa = TipoSpesa.ricercaTipoSpesaByCodice(2)

        self.assertNotIn(tipoSpesa.codice, tabellaMillesimale.tipologieSpesa)
        tabellaMillesimale.addTipoSpesa(tipoSpesa)
        tabellaMillesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabellaMillesimale.codice)
        self.assertIn(tipoSpesa.codice, tabellaMillesimale.tipologieSpesa)


    def test_removeTipoSpesa(self):
        tabellaMillesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(12)
        tipoSpesa = TipoSpesa.ricercaTipoSpesaByCodice(2)
        self.assertIn(tipoSpesa.codice, tabellaMillesimale.tipologieSpesa)
        tabellaMillesimale.removeTipoSpesa(tipoSpesa)
        tabellaMillesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabellaMillesimale.codice)
        self.assertNotIn(tipoSpesa.codice, tabellaMillesimale.tipologieSpesa)
