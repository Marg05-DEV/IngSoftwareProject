import os
import webbrowser

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QLineEdit

from Classes.Contabilita.bilancio import Bilancio
from Classes.Gestione.gestoreBilancio import GestoreBilancio
from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteBilancio.VisteGestioneBilancio.VistaAvvisoBilancio import VistaAvvisoBilancio
from Viste.VisteBilancio.VisteGestioneBilancio.VistaListaSpese import VistaListaSpese
from Viste.VisteBilancio.VisteGestioneBilancio.VistaPropostaPreventivo import VistaPropostaPreventivo
from Viste.VisteBilancio.VisteGestioneBilancio.VistaRipartizioneConsuntivo import VistaRipartizioneConsuntivo
from Viste.VisteBilancio.VisteGestioneBilancio.VistaRipartizionePreventivo import VistaRipartizionePreventivo


class VistaCalcolaBilancio:
    pass


class VistaGestioneBilancio(QWidget):

    def __init__(self, bilancio, callback_lista_esercizi):
        print("ciao")
        print(bilancio.getInfoBilancio())
        super(VistaGestioneBilancio, self).__init__()
        self.immobile = Immobile.ricercaImmobileById(bilancio.immobile)
        self.bilancio = bilancio
        self.callback_lista_esercizi = callback_lista_esercizi
        self.setWindowTitle("Gestione Bilancio")
        self.buttons = {}
        self.input_lines = {}
        self.input_errors = {}
        vertical_layout = QVBoxLayout()
        action_layout1 = QHBoxLayout()
        action_layout1.addWidget(self.new_label("Immobile", "denominazione"))

        action_layout3 = QHBoxLayout()
        action_layout3.addWidget(self.getButton("Proposta Preventivo",
                                                 "Inerisci le spese ipotizzate che verranno\nfatte nel prssimo esercizio.",
                                                 self.goPropostaPreventivo))
        action_layout3.addWidget(self.getButton("Calcola consuntivo",
                                                 "Recupera le spese effettive dell'esercizio conclutosi\ne dividile per tipo di spesa.",
                                                self.goElencoSpese))
        vertical_layout.addLayout(action_layout1)
        vertical_layout.addLayout(action_layout3)

        vertical_layout.addWidget(self.getButton("Ripartizione Consuntivo",
                                                 "Calcola le rate che le unità immobiliari dovranno versare nel prossimo esercizio basandosi sulle spese ipotizzate\n e il conguaglio restante dall'esercizio precedente.",
                                                 self.goRipartizioneConsuntivo))

        vertical_layout.addWidget(self.getButton("Ripartizione Preventivo",
                                                 "Dividi in base alle tabelle millesimali le spese effettive per ogni unità immobiliare e calcola il conguaglio facendo\n la differenza con le rate versate durante l'esercizio conclutosi.",
                                                 self.goRipartizionePreventivo))

        vertical_layout.addWidget(self.getButton("Visualizza i prospetti del bilancio dell'esercizio", "",
                                                 self.goProspettiEsercizio))
        vertical_layout.addWidget(self.getButton("Calcola Bilancio dell'esercizio",
                                                 "",
                                                 self.goCalcolaBilancio))

        self.gestisciBottoni()

        self.setLayout(vertical_layout)
        self.resize(600, 400)
        print("ciao")

    def getButton(self, testo, sottotesto, on_click):
        button = QPushButton(testo)
        button.setText(button.text() + "\n" + sottotesto)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button.clicked.connect(on_click)
        self.buttons[testo] = button
        return button

    def new_label(self, testo, index):
        print("dentro label: ", testo, " ", index)
        label = QLabel(testo + ": " + str(self.immobile.getInfoImmobile()[index]))
        print(label)
        return label

    def gestisciBottoni(self):
        if self.bilancio.isApprovata:
            self.buttons["Proposta Preventivo"].setDisabled(True)
            self.buttons["Calcola consuntivo"].setDisabled(True)
            self.buttons["Ripartizione Consuntivo"].setDisabled(True)
            self.buttons["Ripartizione Preventivo"].setDisabled(True)
            self.buttons["Visualizza i prospetti del bilancio dell'esercizio"].setDisabled(False)
            self.buttons["Calcola Bilancio dell'esercizio"].setDisabled(True)
        else:
            self.buttons["Proposta Preventivo"].setDisabled(False)
            self.buttons["Calcola consuntivo"].setDisabled(False)
            self.buttons["Ripartizione Consuntivo"].setDisabled(True)
            self.buttons["Ripartizione Preventivo"].setDisabled(True)
            self.buttons["Visualizza i prospetti del bilancio dell'esercizio"].setDisabled(True)
            self.buttons["Calcola Bilancio dell'esercizio"].setDisabled(True)

            if self.bilancio.passaggi["ripartizioneSpesePreventivate"]:
                self.buttons["Calcola Bilancio dell'esercizio"].setDisabled(False)

            if self.bilancio.passaggi["ripartizioneSpeseConsuntivate"] and self.bilancio.passaggi["spesePreventivate"]:
                self.buttons["Ripartizione Preventivo"].setDisabled(False)

            if self.bilancio.passaggi["speseConsuntivate"]:
                self.buttons["Ripartizione Consuntivo"].setDisabled(False)

    def goPropostaPreventivo(self):
        self.bilancio.passaggioRaggiunto("spesePreventivate")
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        self.proposta_preventivo = VistaPropostaPreventivo(self.bilancio, self.callback)
        self.proposta_preventivo.show()

    def goElencoSpese(self):
        self.lista_spese = VistaListaSpese(self.bilancio, self.callback)
        self.lista_spese.show()

    def goRipartizionePreventivo(self):
        self.bilancio.passaggioRaggiunto("ripartizioneSpesePreventivate")
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        self.ripartizione_preventivo = VistaRipartizionePreventivo(self.bilancio, self.callback)
        self.ripartizione_preventivo.show()

    def goRipartizioneConsuntivo(self):
        self.bilancio.passaggioRaggiunto("ripartizioneSpeseConsuntivate")
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        self.ripartizione_consuntivo = VistaRipartizioneConsuntivo(self.bilancio, self.callback)
        self.ripartizione_consuntivo.show()

    def goProspettiEsercizio(self):
        print("prospetti esercizio")
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        pdf = GestoreBilancio.visualizzaProspettiEsercizio(self.bilancio)

        directory_files = os.path.dirname(os.path.abspath(__file__)).replace("Viste\\VisteBilancio\\VisteGestioneBilancio", "Dati\\pdf\\")

        nome_file = f"Esercizio{self.bilancio.inizioEsercizio.year}-{self.bilancio.fineEsercizio.year}"
        print(nome_file)

        pdf.output(f"{directory_files}{self.immobile.sigla}\\{nome_file}.pdf")
        webbrowser.open(f"{directory_files}{self.immobile.sigla}\\{nome_file}.pdf")

    def goCalcolaBilancio(self):
        self.calcola_bilancio = VistaAvvisoBilancio(self, self.bilancio.approvaBilancio,
                                                    "Approvando il bilancio non sarai più in grado di modificarlo.\nSei sicuro di voler procedere?",
                                                    "Approva")
        self.calcola_bilancio.show()

    def callback(self):
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        print(" -------------- dentro la callback per aggiornare i bottoni -----------------")
        print(self.bilancio.getInfoBilancio())
        self.gestisciBottoni()

    def avvisoConfermato(self):
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        self.gestisciBottoni()

    def closeEvent(self, event):
        self.callback_lista_esercizi()
