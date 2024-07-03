import datetime

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

# Seeding Immobili



# Seeding Condomini
condomino = Condomino()

condomino.aggiungiCondomino("Maria", "Verdi", "Ascoli Piceno", datetime.datetime(1975, 5, 12), "VRDMRA75M12C023P",
                                         "Ascoli Piceno", "AP", "maria.verdi@email.it", "3451234567")

condomino.aggiungiCondomino("Giovanni", "Bianchi", "San Benedetto del Tronto", datetime.datetime(1980, 10, 3), "BNCGIO80T03H123Q",
                                         "San Benedetto del Tronto", "AP", "giovanni.bianchi@pec.it", "3384567890")


condomino.aggiungiCondomino("Laura", "Gialli", "Offida", datetime.datetime(1995, 11, 17), "GLRLRA95N17T654R",
                                         "Offida", "AP", "laura.gialli@yahoo.it", "3398765432")


condomino.aggiungiCondomino("Marco", "Rossi", "Ascoli Piceno", datetime.datetime(1990, 8, 4), "RSSMRCO90A04H321G",
                                         "Ascoli Piceno", "AP", "marco.rossi@libero.it", "3209876543")


condomino.aggiungiCondomino("Anna", "Bianchi", "San Benedetto del Tronto", datetime.datetime(2002, 6, 25), "BNCANNA02F25G897T",
                                         "San Benedetto del Tronto", "AP", "anna.bianchi@gmail.com", "3401234567")


condomino.aggiungiCondomino("Francesco", "Verdi", "Offida", datetime.datetime(1983, 3, 9), "VRDFRA83C09H456P",
                                         "Offida", "AP", "francesco.verdi@alice.it", "3356543210")


condomino.aggiungiCondomino("Lucia", "Gialli", "Ascoli Piceno", datetime.datetime(1965, 9, 12), "GLLLUC65I12H123Q",
                                         "Ascoli Piceno", "AP", "lucia.gialli@hotmail.it", "3313245678")


condomino.aggiungiCondomino("Roberto", "Rossi", "San Benedetto del Tronto", datetime.datetime(1972, 4, 18), "RSSRBTO72D18H789P",
                                         "San Benedetto del Tronto", "AP", "roberto.rossi@pec.it", "3367895643")


condomino.aggiungiCondomino("Elena", "Bianchi", "Offida", datetime.datetime(1988, 1, 6), "BNCELNA88A06T321G",
                                          "Offida", "AP", "elena.bianchi@libero.it", "3332145678")

# Seeding Unità Immobiliari
unitaImmobiliare = UnitaImmobiliare()
unitaImmobiliare.aggiungiUnitaImmobiliare(1, 1, {Condomino.ricercaCondominoByNome("Maria"): "proprietario", Condomino.ricercaCondominoByNome("Giovanni"): "coproprietario"}, 1, 1, "appartamento", "A/2",
                                            1, Immobile.ricercaImmobileByCodice(1), 1, "a")

unitaImmobiliare.aggiungiUnitaImmobiliare(2, 2, {Condomino.ricercaCondominoByNome("Elena"): "proprietario"}, 2, 2, "appartamento", "A/2",
                                            2, Immobile.ricercaImmobileByCodice(2), 2, "b")

unitaImmobiliare.aggiungiUnitaImmobiliare(3, 3, {Condomino.ricercaCondominoByNome("Laura"): "proprietario"}, 3, 3, "garage", "B/1",
                                            3, Immobile.ricercaImmobileByCodice(1), 2, "c")
