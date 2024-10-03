from unittest import TestCase

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile


class TestGestioneUnitaImmobiliare(TestCase):
    def test_add_unitaImmobiliare(self):
        self.unitaImmobiliare = UnitaImmobiliare()
        self.unitaImmobiliare.aggiungiUnitaImmobiliare(1, 3, {"CRFRA96N17T714K": "Proprietario"}, 2, 1, "Garage", "B/1",
                                                3, Immobile.ricercaImmobileByCodice(1), 0, "A")

        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliari()
        self.assertIsNotNone(unitaImmobiliari)
        self.assertIn(self.unitaImmobiliare.codice, unitaImmobiliari)

    def test_delete_unitaImmobiliare(self):
        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliari()
        self.assertIsNotNone(unitaImmobiliari)
        self.assertIn(7, unitaImmobiliari)
        self.unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(7)
        self.unitaImmobiliare.rimuoviUnitaImmobiliare()

        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliari()
        self.assertIsNotNone(unitaImmobiliari)
        self.assertNotIn(7, unitaImmobiliari)

    def test_addCondomino(self):
        unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(7)
        condomino = Condomino.ricercaCondominoByCF("GLRLRA95N17T654R")
        self.assertNotIn(condomino.codiceFiscale, unitaImmobiliare.condomini)
        unitaImmobiliare.addCondomino(condomino, "Inquilino")
        unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(unitaImmobiliare.codice)
        self.assertIn(condomino.codiceFiscale, unitaImmobiliare.condomini)

    def test_removeCondomino(self):
        unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(7)
        condomino = Condomino.ricercaCondominoByCF("GLRLRA95N17T654R")
        self.assertIn(condomino.codiceFiscale, unitaImmobiliare.condomini)
        unitaImmobiliare.removeCondomino(condomino)
        unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(unitaImmobiliare.codice)
        self.assertNotIn(condomino.codiceFiscale, unitaImmobiliare.condomini)

    def test_modificaTitoloCondomino(self):
        unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(7)
        condomino = Condomino.ricercaCondominoByCF("GLRLRA95N17T654R")
        self.assertIn(condomino.codiceFiscale, unitaImmobiliare.condomini)
        unitaImmobiliare.modificaTitoloCondomino(condomino, "Comproprietario")
        unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(unitaImmobiliare.codice)
        self.assertEqual("Comproprietario", unitaImmobiliare.condomini["GLRLRA95N17T654R"])

