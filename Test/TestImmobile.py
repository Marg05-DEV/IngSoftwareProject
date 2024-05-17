import os.path
import pickle

from unittest import TestCase
#from Classes.RegistroAnagrafe.immobile import Immobile
class TestImmobile(TestCase):

    def test_aggiungiImmobile(self):
        print(1)
        from Classes.RegistroAnagrafe.immobile import Immobile
        print("ciao")
        print(dir())
        print(dir(Immobile))
        self.immobile = Immobile()
        self.immobile.aggiungiImmobile(4, "sig", "den",
                                       "ccrdhgbgib", "Offida", "AP", "88888", "tesino")
        immobili = None
        if os.path.isfile('Dati/Immobile.pickle'):
            with open('Dati/Immobile.pickle', 'rb') as f:
                immobili = pickle.load(f)
        self.assertIsNotNone(immobili)
        self.assertIn(4, immobili)

