import os.path
import pickle
from unittest import TestCase

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile


nome_file = 'Dati/UnitaImmobiliari.pickle'
class TestGestioneUnitaImmobiliare(TestCase):
    def test_add_unitaImmobiliare(self):
        self.unitaImmobiliare = UnitaImmobiliare()
        self.unitaImmobiliare.aggiungiUnitaImmobiliare(1, 3, {"CRFRA96N17T714K": "Proprietario"}, 2, 1, "Garage", "B/1",
                                                3, Immobile.ricercaImmobileByCodice(1), 0, "A")

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
        self.unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(1)
        self.unitaImmobiliare.rimuoviUnitaImmobiliare()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                unitaImmobiliari = pickle.load(f)
        self.assertIsNotNone(unitaImmobiliari)
        self.assertNotIn(10, unitaImmobiliari)
        print("dentro test delete", unitaImmobiliari)

    def test_addCondomino(self):
        pass

    def test_removeCondomino(self):
        pass

    def test_modificaTitoloCondomino(self):
        pass

