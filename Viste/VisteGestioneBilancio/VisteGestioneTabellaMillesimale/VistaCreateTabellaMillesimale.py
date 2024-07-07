import datetime

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy, QDateEdit, QComboBox
import itertools
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale



class VistaCreateTabellaMillesimale(QWidget):
    def __init__(self, immobile, ui, callback, isIterable):
        super(VistaCreateTabellaMillesimale, self).__init__()
        self.immobile = immobile
        self.unitaImmobiliare = ui
        self.callback = callback
        main_layout = QGridLayout()
        self.input_lines = {}

        lbl_frase = QLabel("Inserisci i dati per l'aggiunta di un nuovo condomino:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Nome", "nome", ), 1, 0, 1, 3)
        main_layout.addLayout(self.pairLabelInput("Cognome", "cognome"), 2, 0, 1, 3)
        main_layout.addLayout(self.pairLabelInput("Codice Fiscale", "codiceFiscale"), 3, 0, 1, 3)
        main_layout.addLayout(self.pairLabelInput("Luogo di nascita", "luogoDiNascita"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("Provincia", "provinciaDiNascita"), 4, 1)
        main_layout.addLayout(self.pairLabelInput("Data", "dataDiNascita"), 4, 2)
        main_layout.addLayout(self.pairLabelInput("Residenza", "residenza"), 5, 0, 1, 3)
        main_layout.addLayout(self.pairLabelInput("Telefono", "telefono"), 6, 0, 1, 3)
        main_layout.addLayout(self.pairLabelInput("Email", "email"), 7, 0, 1, 3)
        main_layout.addLayout(self.pairLabelInput("Titolo dell'unità immobiliare", "titolo"), 8, 0, 1, 3)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 9, 0, 1, 3)
        if isIterable:
            button_layout = QHBoxLayout()
            button_layout.addWidget(self.create_button("Termina Assegnazione", self.terminaAssegnazione))
            button_layout.addWidget(self.create_button("Aggiungi altro condomino", self.altroCondomino))
            main_layout.addLayout(button_layout, 10, 0, 1, 3)
        else:
            main_layout.addWidget(self.create_button("Aggiungi Condomino", self.terminaAssegnazione), 10, 0, 1, 3)


        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Condomino")

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
        if testo == "Data":
            input_line = QDateEdit()
        elif index == "titolo":
            input_line = QComboBox()
            input_line.setPlaceholderText("Scegli un titolo per il condomino...")
            input_line.addItems(["Proprietario", "Coproprietario", "Inquilino"])
        else:
            input_line = QLineEdit()

        self.input_lines[index] = input_line

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        return pair_layout

    def aggiungiCondomino(self):
        print("stiamo per aggiungere")
        nome = self.input_lines["nome"].text()
        cognome = self.input_lines["cognome"].text()
        residenza = self.input_lines["residenza"].text()
        dataDiNascita = self.input_lines["dataDiNascita"].text()
        dataDiNascita = dataDiNascita.split("/")
        dataDiNascita = datetime.date(int(dataDiNascita[2]), int(dataDiNascita[1]), int(dataDiNascita[0]))
        codiceFiscale = self.input_lines["codiceFiscale"].text()
        luogoDiNascita = self.input_lines["luogoDiNascita"].text()
        provinciaDiNascita = self.input_lines["provinciaDiNascita"].text()
        email = self.input_lines["email"].text()
        telefono = self.input_lines["telefono"].text()

        temp_condomino = Condomino()
        msg, condomino = temp_condomino.aggiungiCondomino(nome, cognome, residenza, dataDiNascita, codiceFiscale,
                                                          luogoDiNascita, provinciaDiNascita,
                                                          email, telefono)

        titolo = self.input_lines["titolo"].currentText()

        self.unitaImmobiliare.addCondomino(condomino, titolo)

        print("aggiunta in corso...")

        return msg

    def terminaAssegnazione(self):
        msg = self.aggiungiCondomino()
        print("stiamo per uscire", msg)
        print("f di callback", self.callback)
        self.callback(msg)
        self.close()

    def altroCondomino(self):
        msg = self.aggiungiCondomino()
        self.close()
        self.vista_nuovo_condomino = VistaCreateCondomino(self.immobile, self.unitaImmobiliare, self.callback, True)
        self.vista_nuovo_condomino.show()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()