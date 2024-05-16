from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, QSizePolicy

from Classes.RegistroAnagrafe.immobile import Immobile


class VistaCreateImmobile(QWidget):

    def __init__(self, callback):
        super(VistaCreateImmobile, self).__init__()
        self.callback = callback
        main_layout = QGridLayout()
        self.input_lines = {}

        lbl_frase = QLabel("Inserisci i dati del nuovo immobile:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)
        print(1)

        main_layout.addLayout(self.pairLabelInput("Denominazione", "denominazione", ), 1, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("CF/Partita IVA", "codiceFiscale"), 2, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Codice Numerico", "codice"), 3, 0)
        main_layout.addLayout(self.pairLabelInput("Sigla", "sigla"), 3, 1)
        main_layout.addLayout(self.pairLabelInput("Città", "citta"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("Provincia", "provincia"), 4, 1)
        main_layout.addLayout(self.pairLabelInput("CAP", "cap"), 5, 0)
        main_layout.addLayout(self.pairLabelInput("Via", "via"), 5, 1)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 6, 0, 1, 2)
        main_layout.addWidget(self.create_button("Aggiungi Immobile", self.createImmobile), 7, 0, 1, 2)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Immobile")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def pairLabelInput(self, testo, index):
        pair_layout = QHBoxLayout()

        label = QLabel(testo + ": ")
        input_line = QLineEdit()
        print(1)
        if index == "codice":
            input_line.setValidator(QIntValidator())
            print(1)
        self.input_lines[index] = input_line

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        return pair_layout

    def createImmobile(self):
        temp_immobile = Immobile()
        temp_immobile.aggiungiImmobile(int(self.input_lines["codice"].text()),
                                       self.input_lines["sigla"].text(),
                                       self.input_lines["denominazione"].text(),
                                       self.input_lines["codiceFiscale"].text(),
                                       self.input_lines["citta"].text(),
                                       self.input_lines["provincia"].text(),
                                       self.input_lines["cap"].text(),
                                       self.input_lines["via"].text())
        self.callback()
        self.close()

    def reset(self):
        pass
