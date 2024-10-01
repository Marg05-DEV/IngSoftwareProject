from unittest import TestCase

from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa

nome_file = 'Dati/TipiSpesa.pickle'
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
        self.assertIn(10, tipiSpesa)
        self.tipoSpesa = TipoSpesa.ricercaTipoSpesaByCodice(1)
        self.tipoSpesa.rimuoviTipoSpesa()
        tipiSpesa = TipoSpesa.getAllTipoSpesa()

        self.assertIsNotNone(tipiSpesa)
        self.assertNotIn(6, tipiSpesa)

    def test_getTabelleMillesimaleAssociate(self):
        pass