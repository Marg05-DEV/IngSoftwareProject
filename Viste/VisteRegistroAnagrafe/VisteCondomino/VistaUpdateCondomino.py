import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, \
    QComboBox, QVBoxLayout

from Classes.RegistroAnagrafe.condomino import Condomino


class VistaUpdateCondomino(QWidget):

    def __init__(self, sel_condomino, callback, ui=None, onlyAnagrafica=False):
        super(VistaUpdateCondomino, self).__init__()
        self.callback = callback
        self.sel_condomino = sel_condomino
        if not onlyAnagrafica:
            self.ui = ui
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}
        self.onlyAnagrafica = onlyAnagrafica

        main_layout = QVBoxLayout()
        lbl_frase = QLabel("Inserisci i nuovi dati del condomino da modificare:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())
        main_layout.addWidget(lbl_frase)

        main_layout.addLayout(self.pairLabelInput("Nome", "nome", ))
        main_layout.addLayout(self.pairLabelInput("Cognome", "cognome"))
        main_layout.addLayout(self.pairLabelInput("Codice Fiscale", "codiceFiscale"))

        nascita_layout = QHBoxLayout()
        nascita_layout.addLayout(self.pairLabelInput("Luogo di nascita", "luogoDiNascita"))
        nascita_layout.addLayout(self.pairLabelInput("Provincia", "provinciaDiNascita"))
        nascita_layout.addLayout(self.pairLabelInput("Data", "dataDiNascita"))
        main_layout.addLayout(nascita_layout)

        main_layout.addLayout(self.pairLabelInput("Residenza", "residenza"))
        main_layout.addLayout(self.pairLabelInput("Telefono", "telefono"))
        main_layout.addLayout(self.pairLabelInput("Email", "email"))

        if not self.onlyAnagrafica:
            main_layout.addLayout(self.pairLabelInput("Titolo dell'Unità Immobiliare", "titolo"))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        button_layout.addWidget(self.create_button("Modifica Condomino", self.updateCondomino))
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Modifica Condomino")

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
        input_line = None

        if testo == "Data":
            input_line = QDateEdit()
            data = self.sel_condomino.getDatiAnagraficiCondomino()[index]
            input_line.setDate(QDate(data.year, data.month, data.day))
            input_line.dateChanged.connect(self.input_validation)
        elif index == "titolo":
            input_line = QComboBox()
            if 'Proprietario' in self.ui.condomini.values():
                input_line.addItems(["Comproprietario", "Inquilino"])
            else:
                input_line.addItems(["Proprietario", "Comproprietario", "Inquilino"])
            input_line.setCurrentText(str(self.ui.condomini[self.sel_condomino.codice]))
            input_line.activated.connect(self.input_validation)
        else:
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.sel_condomino.getDatiAnagraficiCondomino()[index]))
            input_line.textChanged.connect(self.input_validation)

        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def updateCondomino(self):
        temp_condomino = {}
        for attributo in self.sel_condomino.getDatiAnagraficiCondomino().keys():
            if attributo == "codice" or self.input_lines[attributo].text() == "":
                temp_condomino[attributo] = self.sel_condomino.getDatiAnagraficiCondomino()[attributo]
            else:
                temp_condomino[attributo] = self.input_lines[attributo].text()

        dataDiNascita = temp_condomino["dataDiNascita"].split('/')

        dataDiNascita = datetime.date(int(dataDiNascita[2]), int(dataDiNascita[1]), int(dataDiNascita[0]))

        msg = self.sel_condomino.modificaCondomino(temp_condomino["nome"],
                                                   temp_condomino["cognome"],
                                                   temp_condomino["residenza"],
                                                   dataDiNascita,
                                                   temp_condomino["codiceFiscale"],
                                                   temp_condomino["luogoDiNascita"],
                                                   temp_condomino["provinciaDiNascita"],
                                                   temp_condomino["email"],
                                                   temp_condomino["telefono"])

        if not self.onlyAnagrafica:
            titolo = self.input_lines["titolo"].currentText()
            self.ui.modificaTitoloCondomino(self.sel_condomino, titolo)

        self.callback(msg)
        self.close()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()
        if not self.onlyAnagrafica:
            if 'Proprietario' in self.ui.condomini.values():
                self.input_lines['titolo'].addItems(["Comproprietario", "Inquilino"])
            else:
                self.input_lines['titolo'].addItems(["Proprietario", "Comproprietario", "Inquilino"])
            self.input_lines['titolo'].setCurrentText(self.ui.condomini[self.sel_condomino.codice])

        self.input_lines["dataDiNascita"].setDate(self.sel_condomino.dataDiNascita)

    def input_validation(self):
        condomini = Condomino.getAllCondomini()
        num_errors = 0
        unique_fields = ['codiceFiscale']
        there_is_unique_error = {}

        for field in unique_fields:
            there_is_unique_error[field] = False
            for condomino in condomini.values():
                if str(condomino.getDatiAnagraficiCondomino()[field]).upper() != str(self.sel_condomino.getDatiAnagraficiCondomino()[field]).upper():
                    if self.input_lines[field].text().upper() == str(condomino.getDatiAnagraficiCondomino()[field]).upper():
                        num_errors += 1
                        there_is_unique_error[field] = True
                        break
            if there_is_unique_error[field]:
                self.input_errors[field].setText(f"{field} già esistente")
                self.input_errors[field].setVisible(True)
            else:
                self.input_errors[field].setVisible(False)

        if num_errors > 0:
            self.buttons["Modifica Condomino"].setDisabled(True)
        else:
            self.buttons["Modifica Condomino"].setDisabled(False)