import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit, QDateEdit

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaUpdateUnitaImmobiliare(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback):
        super(VistaUpdateUnitaImmobiliare, self).__init__()
        self.callback = callback
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
        self.input_lines = {}
        main_layout = QGridLayout()

        lbl_frase = QLabel("Inserisci i nuovi dati dell'unità immobiliare da modificare:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Tipologia Unita Immobiliare", "tipoUnitaImmobiliare"), 1, 0, 1, 3)
        main_layout.addLayout(self.pairLabelInput("Scala", "scala"), 2, 0)
        main_layout.addLayout(self.pairLabelInput("Interno", "interno"), 2, 1)
        main_layout.addLayout(self.pairLabelInput("Foglio", "foglio"), 3, 0)
        main_layout.addLayout(self.pairLabelInput("Particella", "particella"), 3, 1)
        main_layout.addLayout(self.pairLabelInput("Subalterno", "subalterno"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("ZC", "ZC"), 4, 1)
        main_layout.addLayout(self.pairLabelInput("Classe", "classe"), 5, 0)
        main_layout.addLayout(self.pairLabelInput("Categoria", "categoria"), 5, 1)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 6, 0)

        main_layout.addWidget(self.create_button("Modifica Unità Immobiliare", self.updateUnitaImmobiliare), 6, 1)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Modifica Condomino")

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
            data = self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[index]
            input_line.setDate(QDate(data.year, data.month, data.day))
        else:
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[index]))
        self.input_lines[index] = input_line

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        return pair_layout

    def updateUnitaImmobiliare(self):
        print("inizio update condomino")
        temp_unitaImmobiliare = {}
        print(self.sel_unitaImmobiliare.getInfoUnitaImmobiliare().keys())
        for attributo in self.sel_unitaImmobiliare.getInfoUnitaImmobiliare().keys():
            print(attributo)
            print(attributo == "codice" or attributo == "condomini" or attributo == "immobile" or self.input_lines[attributo].text() == "")
            if attributo == "codice" or attributo == "condomini" or attributo == "immobile" or self.input_lines[attributo].text() == "" :
                print("attr1: ", attributo)
                temp_unitaImmobiliare[attributo] = self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[attributo]
            else:
                print("attr2: ", attributo)
                temp_unitaImmobiliare[attributo] = self.input_lines[attributo].text()

        print(temp_unitaImmobiliare)

        msg = self.sel_unitaImmobiliare.modificaUnitaImmobiliare(int(temp_unitaImmobiliare["foglio"]),
                                                   int(temp_unitaImmobiliare["subalterno"]),
                                                   self.sel_unitaImmobiliare.condomini,
                                                   int(temp_unitaImmobiliare["particella"]),
                                                   int(temp_unitaImmobiliare["interno"]),
                                                   temp_unitaImmobiliare["tipoUnitaImmobiliare"],
                                                   temp_unitaImmobiliare["categoria"],
                                                   int(temp_unitaImmobiliare["classe"]),
                                                   Immobile.ricercaImmobileById(self.sel_unitaImmobiliare.immobile),
                                                   int(temp_unitaImmobiliare["scala"]),
                                                   temp_unitaImmobiliare["ZC"])
        print("fine update condomino")
        self.callback(msg)
        self.close()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()