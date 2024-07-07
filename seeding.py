import datetime
import os
import shutil

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

def up():
    # Seeding Immobili
    immobile = Immobile()

    for i in range(1, 10):
        immobile.aggiungiImmobile(i, 'IM' + str(i), "Immobile" + str(i), "987654321" + str(i), "Offida", "AP",
                                  "63073", "Via Roma " + str(i))

    print("tutti immobili inseriti")
    for immobile in Immobile.getAllImmobili().values():
        print(immobile.getInfoImmobile())

    print("\n ------------------------------------------------- \n")
    # Seeding Condomini
    condomino = Condomino()

    condomino.aggiungiCondomino("Maria", "Verdi", "Ascoli Piceno", datetime.date(1975, 5, 12), "VRDMRA75M12C023P",
                                             "Ascoli Piceno", "AP", "maria.verdi@email.it", "3451234567")

    condomino.aggiungiCondomino("Giovanni", "Bianchi", "San Benedetto del Tronto", datetime.date(1980, 10, 3), "BNCGIO80T03H123Q",
                                             "San Benedetto del Tronto", "AP", "giovanni.bianchi@pec.it", "3384567890")


    condomino.aggiungiCondomino("Laura", "Gialli", "Offida", datetime.date(1995, 11, 17), "GLRLRA95N17T654R",
                                             "Offida", "AP", "laura.gialli@yahoo.it", "3398765432")


    condomino.aggiungiCondomino("Marco", "Rossi", "Ascoli Piceno", datetime.date(1990, 8, 4), "RSSMRCO90A04H321G",
                                             "Ascoli Piceno", "AP", "marco.rossi@libero.it", "3209876543")


    condomino.aggiungiCondomino("Anna", "Bianchi", "San Benedetto del Tronto", datetime.date(2002, 6, 25), "BNCANNA02F25G897T",
                                             "San Benedetto del Tronto", "AP", "anna.bianchi@gmail.com", "3401234567")


    condomino.aggiungiCondomino("Francesco", "Verdi", "Offida", datetime.date(1983, 3, 9), "VRDFRA83C09H456P",
                                             "Offida", "AP", "francesco.verdi@alice.it", "3356543210")


    condomino.aggiungiCondomino("Lucia", "Gialli", "Ascoli Piceno", datetime.date(1965, 9, 12), "GLLLUC65I12H123Q",
                                             "Ascoli Piceno", "AP", "lucia.gialli@hotmail.it", "3313245678")


    condomino.aggiungiCondomino("Roberto", "Rossi", "San Benedetto del Tronto", datetime.date(1972, 4, 18), "RSSRBTO72D18H789P",
                                             "San Benedetto del Tronto", "AP", "roberto.rossi@pec.it", "3367895643")


    condomino.aggiungiCondomino("Elena", "Bianchi", "Offida", datetime.date(1988, 1, 6), "BNCELNA88A06T321G",
                                              "Offida", "AP", "elena.bianchi@libero.it", "3332145678")

    print("tutti condomini inseriti")
    for condomino in Condomino.getAllCondomini().values():
        print(condomino.getDatiAnagraficiCondomino())

    print("\n ------------------------------------------------- \n")
    # Seeding Unità Immobiliari
    unitaImmobiliare = UnitaImmobiliare()
    unitaImmobiliare.aggiungiUnitaImmobiliare(1, 1, {"VRDMRA75M12C023P": "Proprietario", "BNCGIO80T03H123Q": "Coproprietario"}, 1, 1, "Appartamento", "A/2",
                                                1, Immobile.ricercaImmobileByCodice(1), 1, "A")

    unitaImmobiliare.aggiungiUnitaImmobiliare(2, 2, {"BNCELNA88A06T321G": "Proprietario"}, 2, 2, "Appartamento", "A/2",
                                                2, Immobile.ricercaImmobileByCodice(2), 2, "B")

    unitaImmobiliare.aggiungiUnitaImmobiliare(3, 3, {"GLRLRA95N17T654R": "Proprietario"}, 3, 0, "Box", "B/1",
                                                3, Immobile.ricercaImmobileByCodice(1), 0, "C")

    unitaImmobiliare.aggiungiUnitaImmobiliare(3, 3, {"RSSRBTO72D18H789P": "Proprietario", "GLLLUC65I12H123Q": "Coproprietario"}, 3, 0, "Negozio", "B/1",
                                              3, Immobile.ricercaImmobileByCodice(1), 0, "C")

    unitaImmobiliare.aggiungiUnitaImmobiliare(2, 2, {"BNCGIO80T03H123Q": "Proprietario"}, 2, 4, "Appartamento", "A/2",
                                              2, Immobile.ricercaImmobileByCodice(3), 1, "B")

    unitaImmobiliare.aggiungiUnitaImmobiliare(2, 2, {"VRDMRA75M12C023P": "Proprietario", "BNCGIO80T03H123Q": "Coproprietario"}, 2, 0, "Negozio", "A/2",
                                              2, Immobile.ricercaImmobileByCodice(3), 0, "B")
    print("tutti unità immobiliari inseriti")
    for unitaImmobiliare in UnitaImmobiliare.getAllUnitaImmobiliari().values():
        print(unitaImmobiliare.getInfoUnitaImmobiliare())

    print("\n ------------------------------------------------- \n")

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    risposta = input("Avvia seeding (y per si) ")
    if risposta == "y":
        os.makedirs(directory + "\\Dati\\pdf")
        up()
        exit()

    risposta = input("Refresh seeding (y per si) ")
    if risposta == "y":
        print(directory + "\\Dati")
        shutil.rmtree(directory + "\\Dati")
        os.makedirs(directory + "\\Dati\\pdf")
        up()
        exit()

    risposta = input("Rimozione seeding (y per si) ")
    if risposta == "y":
        print(directory + "\\Dati")
        shutil.rmtree(directory + "\\Dati")