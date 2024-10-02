from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, QSizePolicy

from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.immobile import Immobile


class VistaCreateImmobile(QWidget):

    def __init__(self, callback):
        super(VistaCreateImmobile, self).__init__()
        self.callback = callback
        main_layout = QGridLayout()
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}

        lbl_frase = QLabel("Inserisci i dati del nuovo immobile: (* Campi obbligatori)")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

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

        self.buttons["Aggiungi Immobile"].setDisabled(True)
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Immobile")

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

        label = QLabel(testo + "*: ")
        input_line = QLineEdit()

        if index == "codice":
            input_line.setValidator(QIntValidator())

        input_line.textChanged.connect(self.input_validation)
        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def createImmobile(self):
        temp_immobile = Immobile()
        msg, immobile = temp_immobile.aggiungiImmobile(int(self.input_lines["codice"].text()),
                                       self.input_lines["sigla"].text(),
                                       self.input_lines["denominazione"].text(),
                                       self.input_lines["codiceFiscale"].text(),
                                       self.input_lines["citta"].text(),
                                       self.input_lines["provincia"].text(),
                                       self.input_lines["cap"].text(),
                                       self.input_lines["via"].text())

        temp_tabellaMillesimale = TabellaMillesimale()
        m, tm = temp_tabellaMillesimale.aggiungiTabellaMillesimale('Tab A', [], 'Spese generali', immobile.id)

        self.callback(msg)
        self.close()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()

    def input_validation(self):
        immobili = Immobile.getAllImmobili()
        num_errors = 0
        num_writed_lines = 0
        required_fields = ['codice', 'sigla', 'denominazione', 'codiceFiscale', 'citta', 'provincia', 'cap', 'via']
        unique_fields = ['codice', 'sigla', 'denominazione',  'codiceFiscale']
        there_is_unique_error = {}

        for field in required_fields:
            if self.input_lines[field].text():
                num_writed_lines += 1
                if field in unique_fields:
                    there_is_unique_error[field] = False
                    for immobile in immobili.values():
                        if self.input_lines[field].text().upper() == str(immobile.getInfoImmobile()[field]).upper():
                            num_errors += 1
                            there_is_unique_error[field] = True
                            break
                    if there_is_unique_error[field]:
                        self.input_errors[field].setText(f"{field} già esistente")
                        self.input_errors[field].setVisible(True)
                    else:
                        self.input_errors[field].setVisible(False)
            else:
                self.input_errors[field].setVisible(False)

        if num_errors > 0 or num_writed_lines < len(required_fields):
            self.buttons["Aggiungi Immobile"].setDisabled(True)
        else:
            self.buttons["Aggiungi Immobile"].setDisabled(False)
