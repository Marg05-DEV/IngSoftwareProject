from unittest import TestCase

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile


nome_file = 'Dati/UnitaImmobiliari.pickle'
class TestGestioneUnitaImmobiliare(TestCase):
    def test_add_unitaImmobiliare(self):
        self.unitaImmobiliare = UnitaImmobiliare()
        self.unitaImmobiliare.aggiungiUnitaImmobiliare(1, 3, {"CRFRA96N17T714K": "Proprietario"}, 2, 1, "Garage", "B/1",
                                                3, Immobile.ricercaImmobileByCodice(1), 0, "A")

        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliari()
        self.assertIsNotNone(unitaImmobiliari)
        self.assertIn(self.unitaImmobiliare.codice, unitaImmobiliari)
        print("dentro add unitaImmobiliare", self.unitaImmobiliare.codice)

    def test_delete_unitaImmobiliare(self):
        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliari()
        self.assertIsNotNone(unitaImmobiliari)
        self.assertIn(7, unitaImmobiliari)
        self.unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(7)
        self.unitaImmobiliare.rimuoviUnitaImmobiliare()

        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliari()
        self.assertIsNotNone(unitaImmobiliari)
        self.assertNotIn(7, unitaImmobiliari)
        print("dentro test delete", unitaImmobiliari)

    def test_addCondomino(self):
        pass

    def test_removeCondomino(self):
        pass

    def test_modificaTitoloCondomino(self):
        pass

