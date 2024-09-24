import datetime
import os.path
import pickle
from unittest import TestCase

from Classes.RegistroAnagrafe.condomino import Condomino

nome_file = 'Dati/Condomimi.pickle'


class TestGestioneImmobile(TestCase):
    def test_add_condomini(self):
        self.condomino = Condomino()
        self.condomino.aggiungiCondomino("Gianni", "Rossi", "Offida", datetime.date(1992, 8, 23), "GRN45HK785LM",
                                             "Ascoli Piceno", "AP", "gianni.rossi@libero.it", "344585857")

        condomini = None
        if os.path.isfile(nome_file):
            with open(nome_file, "rb") as f:
                condomini = dict(pickle.load(f))
        self.assertIsNotNone(condomini)
        self.assertIn(10, condomini)
        print("Dentro a condomini")

    def test_delete_condomino(self):
        condomini = None
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
        self.assertIsNotNone(condomini)
        self.assertIn(10, condomini)
        self.condomino = Condomino.ricercaCondominoByCF("GRN45HK785LM")
        self.condomino.rimuoviCondomino()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
        self.assertIsNotNone(condomini)
        self.assertNotIn(10, condomini)
        print("dentro test delete", condomini)
