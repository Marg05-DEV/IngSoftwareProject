import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy, QDateEdit, QComboBox, QListView, QCompleter
import itertools
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Viste.VisteGestioneBilancio.VisteGestioneTabellaMillesimale.VistaCreateTipoSpesa import VistaCreateTipoSpesa


class VistaCreateTabellaMillesimale(QWidget):
    def __init__(self, immobile, callback):
        super(VistaCreateTabellaMillesimale, self).__init__()
        print("ciao bellu")
        self.immobile = immobile
        self.callback = callback
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}
        main_layout = QGridLayout()

        lbl_frase = QLabel("Inserisci i dati della nuova tabella millesimale:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)
        action_layout1 = QHBoxLayout()
        print("ciao pidocchio 1")
        action_layout1.addLayout(self.pairLabelInput("Nome", "nome"), 1, 0, 1, 3)
        print("ciao3")
        action_layout1.addLayout(self.pairLabelInput("Descrizione", "descrizione"), 2, 0, 1, 3)
        print("ciao pidocchio 2")
        action_layout2 = QHBoxLayout()
        completer_list = sorted([item.nome for item in TipoSpesa.getAllTipoSpesa().values()])
        print(completer_list)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca tipo spesa")
        self.tipoSpesa_completer = QCompleter(completer_list)
        self.tipoSpesa_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.searchbar.setCompleter(self.tipoSpesa_completer)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.create_button("Aggiungi altro condomino", self.seleziona_tipo_spesa))

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

        main_layout.addWidget(self.create_button("Aggiungi Tabella Millesimale", self.aggiungiUnitaImmobiliare), 7, 0, 1, 2)
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Condomino")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        self.buttons[testo] = button
        return button

    def pairLabelInput(self, testo, index):
        print("ciao1")
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + "*: ")
        input_line = QLineEdit()

        if index == "nome":
            input_line.setValidator(QIntValidator())

        input_line.textChanged.connect(self.input_validation)
        print("ciao2")
        self.input_lines[index] = input_line
        print("ciao4")
        self.input_errors[index] = error
        print("ciao5")
        pair_layout.addWidget(label)
        print("ciao6")
        pair_layout.addWidget(input_line)
        print("ciao7")
        input_layout.addWidget(error)
        print("ciao8")
        input_layout.addLayout(pair_layout)
        print("ciao9")
        return input_layout

    def aggiungiUnitaImmobiliare(self):
        pass

    def seleziona_tipo_spesa(self):
        self.search_text = self.searchbar.text()
        tipo_spesa = 0
        if self.search_text:
            tipo_spesa = TipoSpesa.ricercaTipoSpesaByNome(self.search_text)

        if not tipo_spesa:
            self.add_tipo_spesa = TabellaMillesimale.addTipoSpesa(tipo_spesa)


    def nuovo_tipo_spesa(self):
        self.new_tipo_spesa = VistaCreateTipoSpesa()
        self.new_tipo_spesa.show()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()

    def input_validation(self):
        tabelleMillesimale = TabellaMillesimale.getAllTabelleMillesimali()
        num_errors = 0
        num_writed_lines = 0
        required_fields = ['nome', 'descrizione']
        unique_fields = ['nome']
        there_is_unique_error = {}

        for field in required_fields:
            if self.input_lines[field].text():
                num_writed_lines += 1
                if field in unique_fields:
                    there_is_unique_error[field] = False
                    print(field)
                    for tabella in tabelleMillesimale.values():
                        if self.input_lines[field].text().upper() == str(tabella.getInfoImmobile()[field]).upper():
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

        if (num_errors > 0 or num_writed_lines < len(required_fields)) and self.search_text:
            self.buttons["Aggiungi Tabella Millesimale"].setDisabled(True)
        else:
            self.buttons["Aggiungi Tabella Millesimale"].setDisabled(False)