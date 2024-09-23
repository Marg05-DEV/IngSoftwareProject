import os.path
import pickle
from unittest import TestCase

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

nome_file = 'Dati/UnitaImmobiliari.pickle'
class TestGestioneUnitaImmobiliare(TestCase):
    def test_add_unitaImmobiliare(self):
        self.unitaImmobiliare = UnitaImmobiliare()
        self.unitaImmobiliare.aggiungiUnitaImmobiliare(1,3,"pippo",3,2,"Cella frigorifera", "Negozio","A",2,3,4)

        unitaImmobiliari = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                unitaImmobiliari = dict(pickle.load(f))
        self.assertIsNotNone(unitaImmobiliari)
        self.assertIn(10, unitaImmobiliari)
        print("dentro add unitaImmobiliare", unitaImmobiliari)

    def test_delete_unitaImmobiliare(self):
        unitaImmobiliari = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = pickle.load(f)
        self.assertIsNotNone(unitaImmobiliari)
        self.assertIn(10, unitaImmobiliari)
        self.unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(10)
        self.unitaImmobiliare.rimuoviUnitaImmobiliare()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = pickle.load(f)
        self.assertIsNotNone(unitaImmobiliari)
        self.assertNotIn(10, unitaImmobiliari)
        print("dentro test delete", unitaImmobiliari)

