from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QLineEdit

from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteGestioneBilancio.VisteBilancio.VistaCalcolaBilancio import VistaCalcolaBilancio
from Viste.VisteGestioneBilancio.VisteBilancio.VistaCalcoloConsuntivo import VistaCalcoloConsuntivo
from Viste.VisteGestioneBilancio.VisteBilancio.VistaNuovoEsercizio import VistaNuovoEsercizio
from Viste.VisteGestioneBilancio.VisteBilancio.VistaPropostaPreventivo import VistaPropostaPreventivo
from Viste.VisteGestioneBilancio.VisteBilancio.VistaProspettiEsercizio import VistaProspettiEsercizio
from Viste.VisteGestioneBilancio.VisteBilancio.VistaRipartizioneConsuntivo import VistaRipartizioneConsuntivo
from Viste.VisteGestioneBilancio.VisteBilancio.VistaRipartizionePreventivo import VistaRipartizionePreventivo


class VistaBilancio(QWidget):

    def __init__(self, immobile):
        print("ciao")
        super(VistaBilancio, self).__init__()
        self.immobile = immobile
        self.setWindowTitle("Gestione Bilancio")
        self.input_lines = {}
        self.input_errors = {}
        vertical_layout = QVBoxLayout()
        action_layout1 = QHBoxLayout()
        action_layout1.addWidget(self.new_label("Immobile", "denominazione"))

        action_data = QHBoxLayout()
        action_data.addLayout(self.pairLabelInput("Data inizio Esercizio", "inizioEsercizio"))
        action_data.addLayout(self.pairLabelInput("Data fine Esercizio", "fineEsercizio"))

        action_layout2 = QHBoxLayout()
        action_layout2.addWidget(self.getButton("Nuovo Esercizio",
                                                "",
                                                self.goNuovoEsercizio))
        action_layout3 = QHBoxLayout()
        action_layout3.addWidget(self.getButton("Proposta Preventivo",
                                                 "Inerisci le spese ipotizzate che verranno fatte nel prssimo esercizio.",
                                                 self.goPropostaPreventivo))
        action_layout3.addWidget(self.getButton("Calcola consuntivo",
                                                 "Recupera le spese effettive dell'esercizio conclutosi e dividile per tipo di spesa.",
                                                self.goCalcolaConsuntivo))
        vertical_layout.addLayout(action_layout1)
        vertical_layout.addLayout(action_data)
        vertical_layout.addLayout(action_layout2)
        vertical_layout.addLayout(action_layout3)

        vertical_layout.addWidget(self.getButton("Ripartizione Preventivo",
                                                 "Dividi in base alle tabelle millesimali le spese effettive per ogni unità immobiliare e calcola il conguaglio facendo\n la differenza con le rate versate durante l'esercizio conclutosi.",
                                                 self.goRipartizionePreventivo))
        vertical_layout.addWidget(self.getButton("Ripartizione Consuntivo",
                                                 "Calcola le rate che le unità immobiliari dovranno versare nel prossimo esercizio basandosi sulle spese ipotizzate\n e il conguaglio restante dall'esercizio precedente.",
                                                 self.goRipartizioneConsuntivo))
        vertical_layout.addWidget(self.getButton("Visualizza i prospetti del bilancio dell'esercizio ", "",
                                                 self.goProspettiEsercizio))
        vertical_layout.addWidget(self.getButton("Calcola Bilancio dell'esercizio",
                                                 "",
                                                 self.goCalcolaBilancio))
        self.setLayout(vertical_layout)
        self.resize(600, 400)
        print("ciao")

    def getButton(self, testo, sottotesto, on_click):
        button = QPushButton(testo)
        button.setText(button.text() + "\n" + sottotesto)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button.clicked.connect(on_click)
        return button
    def new_label(self, testo, index):
        print("dentro label: ", testo, " ", index)
        label = QLabel(testo + ": " + str(self.immobile.getInfoImmobile()[index]))
        print(label)
        return label

    def pairLabelInput(self, testo, index):
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + "*: ")
        input_line = QLineEdit()

        input_line.textChanged.connect(self.input_validation)
        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def goNuovoEsercizio(self):
        self.nuovo_esercizio = VistaNuovoEsercizio()
        self.nuovo_esercizio.show()
    def goPropostaPreventivo(self):
        self.proposta_preventivo = VistaPropostaPreventivo(self.immobile)
        self.proposta_preventivo.show()

    def goCalcolaConsuntivo(self):
        self.calcola_consuntivo = VistaCalcoloConsuntivo(self.immobile)
        self.calcola_consuntivo.show()
    def goRipartizionePreventivo(self):
        self.ripartizione_preventivo = VistaRipartizionePreventivo()
        self.ripartizione_preventivo.show()

    def goRipartizioneConsuntivo(self):
        self.ripartizione_consuntivo = VistaRipartizioneConsuntivo()
        self.ripartizione_consuntivo.show()

    def goProspettiEsercizio(self):
        self.prospetti_esercizio = VistaProspettiEsercizio()
        self.prospetti_esercizio.show()

    def goCalcolaBilancio(self):
        self.calcola_bilancio = VistaCalcolaBilancio()
        self.calcola_bilancio.show()

    def input_validation(self):
        pass