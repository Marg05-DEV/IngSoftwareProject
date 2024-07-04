import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit, QDateEdit

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaUpdateUnitaImmobiliare(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback, onlyAnagrafica=False):
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
        n = 5

        if not onlyAnagrafica:
            n = 6
            main_layout.addLayout(self.pairLabelInput("Email", "email"), n, 0, 1, 3)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), n + 1, 0, 1, 3)

        main_layout.addWidget(self.create_button("Modifica Unità Immobiliare", self.updateUnitaImmobiliare), n + 1, 0, 1, 3)

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
            if attributo == "codice" or self.input_lines[attributo].text() == "":
                temp_unitaImmobiliare[attributo] = self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[attributo]
            else:
                temp_unitaImmobiliare[attributo] = self.input_lines[attributo].text()

        print(temp_unitaImmobiliare)

        msg = self.sel_unitaImmobiliare.modificaUnitaImmobiliare(temp_unitaImmobiliare["foglio"],
                                                   temp_unitaImmobiliare["subalterno"],
                                                   temp_unitaImmobiliare["condomini"],
                                                   temp_unitaImmobiliare["particella"],
                                                   temp_unitaImmobiliare["interno"],
                                                   temp_unitaImmobiliare["tipoUnitaImmobiliare"],
                                                   temp_unitaImmobiliare["categoria"],
                                                   temp_unitaImmobiliare["classe"],
                                                 self.sel_unitaImmobiliare.immobile,
                                                 temp_unitaImmobiliare["scala"],
                                                 temp_unitaImmobiliare["ZC"])
        print("fine update condomino")
        self.callback(msg)
        self.close()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()