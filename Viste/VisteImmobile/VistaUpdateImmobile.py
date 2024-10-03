from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout

from Classes.RegistroAnagrafe.immobile import Immobile


class VistaUpdateImmobile(QWidget):

    def __init__(self, sel_immobile, callback):
        super(VistaUpdateImmobile, self).__init__()
        self.callback = callback
        self.sel_immobile = sel_immobile
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}
        main_layout = QGridLayout()

        lbl_frase = QLabel("Inserisci i nuovi dati dell'immobile da modificare:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Denominazione", "denominazione"), 1, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("CF/Partita IVA", "codiceFiscale"), 2, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Codice Numerico", "codice"), 3, 0)
        main_layout.addLayout(self.pairLabelInput("Sigla", "sigla"), 3, 1)
        main_layout.addLayout(self.pairLabelInput("Città", "citta"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("Provincia", "provincia"), 4, 1)
        main_layout.addLayout(self.pairLabelInput("CAP", "cap"), 5, 0)
        main_layout.addLayout(self.pairLabelInput("Via", "via"), 5, 1)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 6, 0)
        main_layout.addWidget(self.create_button("Annulla Modifica", self.close), 6, 1)

        main_layout.addWidget(self.create_button("Modifica Immobile", self.updateImmobile), 7, 0, 1, 2)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Modifica Immobile")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        self.buttons[testo] = button
        return button

    def pairLabelInput(self, testo, index):
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + ": ")
        input_line = QLineEdit()

        if index == "codice":
            input_line.setValidator(QIntValidator())

        input_line.textChanged.connect(self.input_validation)
        self.input_lines[index] = input_line
        self.input_errors[index] = error

        input_line.setPlaceholderText(str(self.sel_immobile.getInfoImmobile()[index]))
        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def updateImmobile(self):
        temp_immobile = {}
        for attributo in self.input_lines:
            if self.input_lines[attributo].text() == "":
                temp_immobile[attributo] = self.sel_immobile.getInfoImmobile()[attributo]
            else:
                temp_immobile[attributo] = self.input_lines[attributo].text()

        msg = self.sel_immobile.modificaImmobile(int(temp_immobile["codice"]),
                                                 temp_immobile["sigla"],
                                                 temp_immobile["denominazione"],
                                                 temp_immobile["codiceFiscale"],
                                                 temp_immobile["citta"],
                                                 temp_immobile["provincia"],
                                                 temp_immobile["cap"],
                                                 temp_immobile["via"])
        self.callback(msg)
        self.close()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()

    def input_validation(self):
        immobili = Immobile.getAllImmobili()
        num_errors = 0
        unique_fields = ['denominazione', 'sigla', 'codice', 'codiceFiscale']
        there_is_unique_error = {}

        for field in unique_fields:
            there_is_unique_error[field] = False
            for immobile in immobili.values():
                if str(immobile.getInfoImmobile()[field]).upper() != str(self.sel_immobile.getInfoImmobile()[field]).upper():
                    if self.input_lines[field].text().upper() == str(immobile.getInfoImmobile()[field]).upper():
                        num_errors += 1
                        there_is_unique_error[field] = True
                        break
            if there_is_unique_error[field]:
                self.input_errors[field].setText(f"{field} già esistente")
                self.input_errors[field].setVisible(True)
            else:
                self.input_errors[field].setVisible(False)

        if num_errors > 0:
            self.buttons["Modifica Immobile"].setDisabled(True)
        else:
            self.buttons["Modifica Immobile"].setDisabled(False)