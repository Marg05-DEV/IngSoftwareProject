import datetime

from PyQt6.QtGui import QIntValidator, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy, QDateEdit, QComboBox, QListView
import itertools
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale



class VistaCreateTabellaMillesimale(QWidget):
    def __init__(self, immobile, callback):
        super(VistaCreateTabellaMillesimale, self).__init__()
        self.immobile = immobile
        self.callback = callback
        self.input_lines = {}
        self.input_errors = {}
        main_layout = QGridLayout()

        lbl_frase = QLabel("Inserisci i dati della nuova tabella millesimale:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)
        action_layout1 = QHBoxLayout()
        action_layout1.addLayout(self.pairLabelInput("Nome", "nome", ), 1, 0, 1, 3)
        action_layout1.addLayout(self.pairLabelInput("Descrizione", "descrizione"), 2, 0, 1, 3)

        action_layout2 = QHBoxLayout
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca tipo spesa")
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.create_button("Aggiungi altro condomino", self.add_tipo_spesa))

        action_layout2.addLayout(self.searchbar)
        action_layout2.addLayout(button_layout)

        action_layout3 = QHBoxLayout()
        lbl_frase = QLabel("Inserisci i dati della nuova tabella millesimale:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        button_layout1 = QVBoxLayout()
        button_layout1.addWidget(self.create_button("Aggiungi", self.seleziona_tipo_spesa))
        action_layout3.addWidget(lbl_frase)
        action_layout3.addLayout(button_layout1)

        tipi_spesa_layout = QHBoxLayout()

        self.list_view_tipi_spesa = QListView()
        self.list_view_tipi_spesa.setAlternatingRowColors(True)
        tipi_spesa_layout.addWidget(self.list_view_tipi_spesa)
        main_layout.addLayout(action_layout1, 3, 0, 1, 2)
        main_layout.addLayout(action_layout2, 4, 0, 1, 2)
        main_layout.addLayout(action_layout3, 5, 0, 1, 2)
        main_layout.addLayout(tipi_spesa_layout, 6, 0, 1, 2)

        main_layout.addWidget(self.create_button("Aggiungi Unita Immobiliare", self.aggiungiUnitaImmobiliare), 7, 0, 1, 2)
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

    def aggiungiUnitaImmobiliare(self):
        pass

    def seleziona_tipo_spesa(self):
        self.tipo_spesa = list(TipoSpesa.getAllTipoSpesa().values())

    def nuovo_tipo_spesa(self):
        #self.new_tipo_spesa = VistaCreateTipoSpesa()
        self.new_tipo_spesa.show()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()