import datetime
import os.path
import pickle
from unittest import TestCase

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare



class TestGestioneImmobile(TestCase):
    def test_add_condomini(self):
        self.condomino = Condomino()
        self.condomino.aggiungiCondomino("Franco", "Pucci", "Ascoli Piceno", datetime.date(1975, 5, 12), "FRNPCC75M12C023P",
                                             "Ascoli Piceno", "AP", "franco.pucci@email.it", "3451234567")

        condomini = Condomino.getAllCondomini()
        self.assertIsNotNone(condomini)
        print("Dentro a condomini")

    def test_delete_condomino(self):
        condomini =Condomino.getAllCondomini()
        self.assertIsNotNone(condomini)
        self.assertIn(10, condomini)
        self.condomino = Condomino.ricercaCondominoByCF("GRN45HK785LM")
        self.condomino.rimuoviCondomino()
        condomini = Condomino.getAllCondomini()
        self.assertIsNotNone(condomini)
        self.assertNotIn(10, condomini)
        print("dentro test delete", condomini)

    def test_getImmmobiliAssociati(self):
        condomini = Condomino.getAllCondomini()
        self.assertIsNotNone(condomini)
        condomino = Condomino.ricercaCondominoByCF("BNCGIO80T03H123Q")
        self.assertIsNotNone(condomino)
        immobili_associati = condomino.getImmobiliAssociati()
        print("prima: ", immobili_associati)
        self.assertIsNotNone(immobili_associati)

        for immo in immobili_associati:
            print(immo.getInfoImmobile())

        unita_da_associare = None
        for unita in UnitaImmobiliare.getAllUnitaImmobiliari().values():
            if Immobile.ricercaImmobileById(unita.immobile) not in immobili_associati:
                unita_da_associare = unita
                break

        self.assertIsNotNone(unita_da_associare)
        unita_da_associare.addCondomino(condomino, "Inquilino")
        self.assertIn(condomino.codiceFiscale, unita_da_associare.condomini)
        immobili_associati1 = condomino.getImmobiliAssociati()
        print("dopo: ", immobili_associati1)
        self.assertNotEqual(immobili_associati, immobili_associati1)
