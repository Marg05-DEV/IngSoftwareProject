import datetime
from unittest import TestCase

from Classes.Contabilita.rata import Rata
from Classes.RegistroAnagrafe.immobile import Immobile

nome_file = 'Dati/Rate.pickle'
class TestGestioneRata(TestCase):
    def test_add_rata(self):
        self.rata = Rata()
        self.rata.aggiungiRata(datetime.date.today(), "Versamento Rata 22/24", 130.60, 4, "Bonifico bancario", 1, "Gianni Rossi")

        rate = Rata.getAllRate()
        self.assertIsNotNone(rate)
        self.assertIn(self.rata.codice, rate)
        print(self.rata.codice)

    def test_delete_rata(self):
        rate = Rata.getAllRate()

        self.assertIsNotNone(rate)
        self.assertIn(5, rate)
        self.rata = Rata.ricercaRataByCodice(5)
        self.rata.rimuoviRata()

        rate = Rata.getAllRate()
        self.assertIsNotNone(rate)
        self.assertNotIn(5, rate)

    def test_lastNumeroRicevuta(self):
        immobile = Immobile.ricercaImmobileById(1)

        last_ricevuta = Rata.lastNumeroRicevuta(immobile)
        self.assertIsInstance(last_ricevuta, int)

        rate_immobile = Rata.getAllRateByImmobile(immobile)
        for rate in rate_immobile.values():
            self.assertGreaterEqual(last_ricevuta, rate.numeroRicevuta)
