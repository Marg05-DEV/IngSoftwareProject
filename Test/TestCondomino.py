import datetime
from unittest import TestCase

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare



class TestGestioneImmobile(TestCase):
    def test_add_condomini(self):
        self.condomino = Condomino()
        self.condomino.aggiungiCondomino("Franco", "Pucci", "Ascoli Piceno", datetime.date(1975, 5, 12), "FRNPCC75M12C023P",
                                             "Ascoli Piceno", "AP", "franco.pucci@email.it", "3451234567")

        condomini = Condomino.getAllCondomini()

        self.assertIsNotNone(condomini)
        self.assertIn(self.condomino.codice, condomini)
        print(self.condomino.codice)

    def test_delete_condomino(self):
        condomini = Condomino.getAllCondomini()

        self.condomino = Condomino.ricercaCondominoByCF("FRNPCC75M12C023P")
        self.assertIsNotNone(condomini)

        self.condomino.rimuoviCondomino()

        condomini = Condomino.getAllCondomini()
        self.assertIsNotNone(condomini)
        self.assertNotIn(self.condomino.codice, condomini)

    def test_getImmobiliAssociati(self):
        condomino = Condomino.ricercaCondominoByCF("BNCGIO80T03H123Q")
        self.assertIsNotNone(condomino)

        immobili_associati = condomino.getImmobiliAssociati()
        self.assertIsNotNone(immobili_associati)

        esiste = False
        unita_da_associare = None
        for unita in UnitaImmobiliare.getAllUnitaImmobiliari().values():
            esiste = False
            for immobile in immobili_associati:
                if unita.immobile == immobile.codice:
                    esiste = True
                    break
            if not esiste:
                unita_da_associare = unita
                break

        self.assertIsNotNone(unita_da_associare)

        unita_da_associare.addCondomino(condomino, "Inquilino")
        unita_da_associare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(unita_da_associare.codice)
        self.assertIn(condomino.codiceFiscale, unita_da_associare.condomini)

        immobili_associati_dopo = condomino.getImmobiliAssociati()

        self.assertNotEqual(immobili_associati, immobili_associati_dopo)
