from unittest import TestCase

from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa

class TestGestioneTipoSpesa(TestCase):
    def test_add_tipoSpesa(self):
        self.tipoSpesa = TipoSpesa()
        self.tipoSpesa.aggiungiTipoSpesa("Spese per la manutenzione della caldaia", "Manutenzione Caldaia")

        tipiSpesa = TipoSpesa.getAllTipoSpesa()
        self.assertIsNotNone(tipiSpesa)
        self.assertIn(6, tipiSpesa)

    def test_delete_tipoSpesa(self):
        tipiSpesa = TipoSpesa.getAllTipoSpesa()

        self.assertIsNotNone(tipiSpesa)
        self.assertIn(6, tipiSpesa)
        self.tipoSpesa = TipoSpesa.ricercaTipoSpesaByCodice(6)
        self.tipoSpesa.rimuoviTipoSpesa()
        tipiSpesa = TipoSpesa.getAllTipoSpesa()

        self.assertIsNotNone(tipiSpesa)
        self.assertNotIn(6, tipiSpesa)

    def test_getTabelleMillesimaleAssociate(self):
        tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(6)
        tabelle_associate = tipo_spesa.getTabelleMillesimaliAssociate()

        tabella_da_associare = None
        for tabella in TabellaMillesimale.getAllTabelleMillesimali().values():
            if tipo_spesa.codice not in tabella.tipologieSpesa:
                tabella_da_associare = tabella
                break

        tabella_da_associare.addTipoSpesa(tipo_spesa)
        tabella_da_associare = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella_da_associare.codice)

        self.assertIn(tipo_spesa.codice, tabella_da_associare.tipologieSpesa)
        tabelle_associate_dopo = tipo_spesa.getTabelleMillesimaliAssociate()
        self.assertNotEqual(tabelle_associate, tabelle_associate_dopo)

