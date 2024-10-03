import datetime
from unittest import TestCase

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.spesa import Spesa
from Classes.RegistroAnagrafe.immobile import Immobile

class TestGestioneBilancio(TestCase):
    def test_add_bilancio(self):
        self.bilancio = Bilancio()
        self.bilancio.aggiungiBilancio(datetime.date(2024,9,1), datetime.date(2025,1,1), Immobile.ricercaImmobileByCodice(2))

        bilanci = Bilancio.getAllBilanci()
        self.assertIsNotNone(bilanci)
        self.assertIn(self.bilancio.codice, bilanci)

    def test_changeListaConsuntivo(self):
        immobile = Immobile.ricercaImmobileById(2)
        spese_immobile = Spesa.getAllSpeseByImmobile(immobile)

        self.bilancio = Bilancio.ricercaBilancioByCodice(1)
        spesa_scelta = None
        for spesa in spese_immobile.values():
            if not spesa.aBilancio:
                spesa_scelta = Spesa.ricercaSpesaByCodice(spesa.codice)
                break

        if spesa_scelta.codice in self.bilancio.listaSpeseAConsuntivo:
            self.assertNotIn(spesa_scelta.codice, self.bilancio.listaSpeseNonAConsuntivo)
            self.bilancio.changeListaConsuntivo(spesa_scelta.codice)
            self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
            self.assertIn(spesa_scelta.codice, self.bilancio.listaSpeseNonAConsuntivo)
            self.assertNotIn(spesa_scelta.codice, self.bilancio.listaSpeseAConsuntivo)
        elif spesa_scelta.codice in self.bilancio.listaSpeseNonAConsuntivo:
            self.assertNotIn(spesa_scelta.codice, self.bilancio.listaSpeseAConsuntivo)
            self.bilancio.changeListaConsuntivo(spesa_scelta.codice)
            self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
            self.assertIn(spesa_scelta.codice, self.bilancio.listaSpeseAConsuntivo)
            self.assertNotIn(spesa_scelta.codice, self.bilancio.listaSpeseNonAConsuntivo)


    def test_passaggioRaggiunto(self):
        self.bilancio = Bilancio.ricercaBilancioByCodice(1)
        self.bilancio.passaggioRaggiunto("SpesePreventivate")
        self.bilancio = Bilancio.ricercaBilancioByCodice(1)
        self.assertTrue(self.bilancio.passaggi["SpesePreventivate"])
        self.assertFalse(self.bilancio.passaggi["speseConsuntivate"])
        self.assertFalse(self.bilancio.passaggi["ripartizioneSpesePreventivate"])
        self.assertFalse(self.bilancio.passaggi["ripartizioneSpeseConsuntivate"])

    def test_approvaBilancio(self):
        self.bilancio = Bilancio.ricercaBilancioByCodice(1)
        self.bilancio.approvaBilancio()
        self.bilancio = Bilancio.ricercaBilancioByCodice(1)
        self.assertTrue(self.bilancio.isApprovata)
        self.assertTrue(self.bilancio.isLastEsercizio)

