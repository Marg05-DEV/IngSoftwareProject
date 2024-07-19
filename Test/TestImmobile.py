import os.path
import pickle

from unittest import TestCase
from Classes.RegistroAnagrafe.immobile import Immobile
class TestImmobile(TestCase):

    def test_aggiungiImmobile(self):
        print(1)
        print(dir())
        print(dir(Immobile))
        self.immobile = Immobile()
        self.immobile.aggiungiImmobile(1,"fi", "bo", "ou", "ci", "ap", "eeee", "rrrr")
        immobili = None
        if os.path.isfile('Dati/Immobile.pickle'):
            with open('Dati/Immobile.pickle', 'rb') as f:
                immobili = pickle.load(f)
        self.assertIsNotNone(immobili)
        self.assertIn(4, immobili)

test = TestImmobile()
test.test_aggiungiImmobile()