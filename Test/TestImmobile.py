from unittest import TestCase

from Classes.RegistroAnagrafe.immobile import Immobile

class TestGestioneImmobile(TestCase):
    def test_add_immobile(self):
        self.immobile = Immobile()
        self.immobile.aggiungiImmobile(10, "IM10", "Immobile10", "98765432110", "Offida", "AP", "63073", "Via Roma 10")

        immobili = Immobile.getAllImmobili()

        self.assertIsNotNone(immobili)
        self.assertIn(10, immobili)
        print("dentro add immobili", immobili)

    def test_delete_immobile(self):
        immobili = Immobile.getAllImmobili()

        self.assertIsNotNone(immobili)
        self.assertIn(10, immobili)
        self.immobile = Immobile.ricercaImmobileById(10)
        self.immobile.rimuoviImmobile()

        immobili = Immobile.getAllImmobili()

        self.assertIsNotNone(immobili)
        self.assertNotIn(10, immobili)
        print("dentro test delete", immobili)

    def test_modifica_immobile(self):
        immobili = Immobile.getAllImmobili()

        print(type(immobili))
        self.assertIsNotNone(immobili)
        self.immobile = Immobile.ricercaImmobileByCodice(10)
        self.assertIn(self.immobile.id, immobili)

        print("prima: ", self.immobile.getInfoImmobile())

        old_id = self.immobile.id
        old_citta = self.immobile.citta
        old_provincia = self.immobile.provincia
        old_cap = self.immobile.cap

        self.immobile.modificaImmobile(10, "IM10", "Immobile10", "98765432110", "Ancona", "AN", "60121", "Via Roma 10")
        self.immobile = Immobile.ricercaImmobileById(self.immobile.id)

        print("dopo: ", self.immobile.getInfoImmobile())

        self.assertEqual(self.immobile.id, old_id)
        self.assertNotEqual(self.immobile.citta, old_citta)
        self.assertNotEqual(self.immobile.provincia, old_provincia)
        self.assertNotEqual(self.immobile.cap, old_cap)

    def test_ricercaImmobileByDenominazione(self):
        immobili = Immobile.getAllImmobili()
        self.assertIsNotNone(immobili)
        print(immobili)
        self.immobile = Immobile.ricercaImmobileByDenominazione("Immobile10")
        print(self.immobile)
        self.assertIsNotNone(self.immobile)
        self.assertIn(self.immobile.id, immobili)




            
            

