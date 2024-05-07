from Classes.RegistroAnagrafe.Immobile import Immobile

import os.path
import pickle

from unittest import TestCase


class TestImmobile(TestCase):

    def test_aggiungiImmobile(self):
        immobile = Immobile.Immobile()
        immobile.aggiungiImmobile(4, "sig","den", "ccrdhgbgib", "Offida", "AP", "88888", "tesino")

        immobili = None
        if os.path.isfile("Dati/Immobile.pickle"):
            with open("Dati/Immobile.pickle", 'rb') as f:
                immobili = pickle.load(f)
            self.assertIsNotNone(immobili)
            self.assertIn(immobile.codice, immobili)
