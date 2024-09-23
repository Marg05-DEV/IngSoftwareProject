import datetime
import os.path
import pickle
from unittest import TestCase

from Classes.RegistroAnagrafe.condomino import Condomino

nome_file = 'Dati/Condomimi.pickle'


class TestGestioneImmobile(TestCase):
    def test_add_condomini(self):
        self.condomino = Condomino()
        self.condomino.aggiungiCondomino("Gianni", "Giannini", "Porchia", datetime.date(2002,3,2), "CHDGD%/S&%/", "Offida", "AP","giannigiannini@hotmail.it", "3333343434")

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
        self.condomino = Condomino.ricercaCondominoByCF("CHDGD%/S&%/")
        self.condomino.rimuoviCondomino()
        if os.path.isfile(nome_file):
            with open(nome_file, 'rb') as f:
                condomini = pickle.load(f)
        self.assertIsNotNone(condomini)
        self.assertNotIn(10, condomini)
        print("dentro test delete", condomini)
