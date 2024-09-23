import os.path
import pickle
from unittest import TestCase

from Classes.Contabilita.tipoSpesa import TipoSpesa

nome_file = 'Dati/TipiSpesa.pickle'
class TestGestioneTipoSpesa(TestCase):
    def test_add_tipoSpesa(self):
        self.tipoSpesa = TipoSpesa()
        self.tipoSpesa.aggiungiTipoSpesa("bolletta", "gas")
        tipiSpesa = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                tipiSpesa = dict(pickle.load(f))
        self.assertIsNotNone(tipiSpesa)
        self.assertIn(10, tipiSpesa)
        print("dentro add immobili", tipiSpesa)

    def test_delete_tipoSpesa(self):
        tipiSpesa = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tipiSpesa = pickle.load(f)
        self.assertIsNotNone(tipiSpesa)
        self.assertIn(10, tipiSpesa)
        self.tipoSpesa = TipoSpesa.ricercaTipoSpesaByCodice(1)
        self.tipoSpesa.rimuoviTipoSpesa()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                tipiSpesa = pickle.load(f)
        self.assertIsNotNone(tipiSpesa)
        self.assertNotIn(10, tipiSpesa)
        print("dentro test delete", tipiSpesa)