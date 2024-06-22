from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino


class VistaAddCondomino(QWidget):
    def __init__(self, immo, interno):
        super(VistaAddCondomino, self).__init__()
        self.interno = interno
        self.immo = immo
        main_layout = QGridLayout()
        self.input_lines = {}

        lbl_frase = QLabel("Inserisci i dati per l'aggiunta di un nuovo condomino:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Nome", "nome", ), 1, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Cognome", "cognome"), 2, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Codice Fiscale", "codiceFiscale"), 3, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Luogo di nascita", "luogoDiNascita"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("Provincia", "provinciaDiNascita"), 1, 1)
        main_layout.addLayout(self.pairLabelInput("Data", "dataDiNascita"), 4, 2)
        main_layout.addLayout(self.pairLabelInput("Residenza", "residenza"), 5, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Telefono", "telefono"), 6, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Email", "email"), 7, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Ttolo dell'unità immobiliare", "titoloUnitaImmobiliare"), 8, 0, 1, 2)


        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 9, 0, 1, 2)
        main_layout.addWidget(self.create_button("Termina Assegnazione", self.terminaAssegnazione()), 10, 0)
        main_layout.addWidget(self.create_button("Aggiungi altro condomino", self.aggiungiCondomino()), 10, 1)


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
        input_line = QLineEdit()

        if index == "codice":
            input_line.setValidator(QIntValidator())

        self.input_lines[index] = input_line

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        return pair_layout

    def terminaAssegnazione(self):
        self.lista_unitaImmobiliare = []
        self.lista_unitaImmobiliare = list(UnitaImmobiliare.getAllUnitaImmobiliari().values())
        unitaImmobiliare = UnitaImmobiliare()

        for unita in self.lista_unitaImmobiliare:
            if unita.interno == self.interno:
                unitaImmobiliare = unita

        temp_Condomino = Condomino()
        msg = temp_Condomino.aggiungiCondomino(int(self.input_lines["nome"].text()),
                                                             self.input_lines["cognome"].text(),
                                                             {},
                                                             self.input_lines["residenza"].text(),
                                                             self.input_lines["dataDiNascita"].text(),
                                                             self.input_lines["codiceFiscale"].text(),
                                                             self.input_lines["luogoDiNascita"].text(),
                                                             unitaImmobiliare,
                                                             self.input_lines["provinciaDiNascita"].text(),
                                                             self.input_lines["email"].text(),
                                                             self.input_lines["telefono"].text()),
        self.callback(msg)
        self.close()

    def aggiungiCondomino(self):
        self.lista_unitaImmobiliare = []
        self.lista_unitaImmobiliare = list(UnitaImmobiliare.getAllUnitaImmobiliari().values())
        unitaImmobiliare = UnitaImmobiliare()

        for unita in self.lista_unitaImmobiliare:
            if unita.interno == self.interno:
                unitaImmobiliare = unita

        temp_Condomino = Condomino()
        msg = temp_Condomino.aggiungiCondomino(int(self.input_lines["nome"].text()),
                                                             self.input_lines["cognome"].text(),
                                                             {},
                                                             self.input_lines["residenza"].text(),
                                                             self.input_lines["dataDiNascita"].text(),
                                                             self.input_lines["codiceFiscale"].text(),
                                                             self.input_lines["luogoDiNascita"].text(),
                                                             unitaImmobiliare,
                                                             self.input_lines["provinciaDiNascita"].text(),
                                                             self.input_lines["email"].text(),
                                                             self.input_lines["telefono"].text()),
        self.callback(msg)
        self.close()
        self.vista_nuovo_condomino = VistaAddCondomino(self.immo, self.interno)
        self.vista_nuovo_condomino.show()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()