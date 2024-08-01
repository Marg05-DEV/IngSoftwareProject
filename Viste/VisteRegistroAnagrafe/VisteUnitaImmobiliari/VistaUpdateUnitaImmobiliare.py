import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit, QDateEdit, \
    QVBoxLayout, QComboBox

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaUpdateUnitaImmobiliare(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback):
        super(VistaUpdateUnitaImmobiliare, self).__init__()
        self.callback = callback
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
        self.labels = {}
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}
        main_layout = QVBoxLayout()

        self.lbl_frase = QLabel("Inserisci i nuovi dati dell'unità immobiliare da modificare:")
        self.lbl_frase.setStyleSheet("font-weight: bold;")
        self.lbl_frase.setFixedSize(self.lbl_frase.sizeHint())

        main_layout.addWidget(self.lbl_frase)

        main_layout.addLayout(self.pairLabelInput("Tipologia Unità Immobiliare", "tipoUnitaImmobiliare"))
        self.dati_appartamento = QHBoxLayout()
        self.dati_appartamento.addLayout(self.pairLabelInput("Scala", "scala"))
        self.dati_appartamento.addLayout(self.pairLabelInput("Interno", "interno"))

        dati_catastali1 = QHBoxLayout()
        dati_catastali1.addLayout(self.pairLabelInput("Foglio", "foglio"))
        dati_catastali1.addLayout(self.pairLabelInput("Particella", "particella"))
        dati_catastali1.addLayout(self.pairLabelInput("Subalterno", "subalterno"))

        dati_catastali2 = QHBoxLayout()
        dati_catastali2.addLayout(self.pairLabelInput("ZC", "ZC"))
        dati_catastali2.addLayout(self.pairLabelInput("Classe", "classe"))
        dati_catastali2.addLayout(self.pairLabelInput("Categoria", "categoria"))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        button_layout.addWidget(self.create_button("Modifica Unità Immobiliare", self.updateUnitaImmobiliare))

        main_layout.addLayout(self.dati_appartamento)
        main_layout.addLayout(dati_catastali1)
        main_layout.addLayout(dati_catastali2)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Modifica Condomino")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.buttons[testo] = button
        button.clicked.connect(action)
        return button

    def pairLabelInput(self, testo, index):
        print("---------------------- creazione "+ index + " --------------------------")
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()
        integer_lines = ['scala', 'interno', 'foglio', 'particella', 'subalterno', 'classe']
        print("fine inizializzazione")

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)
        print("fine errori")


        label = QLabel(testo + ": ")
        print("fine label")

        if index == "tipoUnitaImmobiliare":
            input_line = QComboBox()
            input_line.addItems(['Appartamento', 'Box', 'Cantina', 'Negozio'])
            input_line.setCurrentText(self.sel_unitaImmobiliare.tipoUnitaImmobiliare)
            input_line.activated.connect(self.input_validation)
        else:
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[index]))
            input_line.textChanged.connect(self.input_validation)
        print("fine input")


        if index in ['interno', 'scala'] and self.sel_unitaImmobiliare.tipoUnitaImmobiliare != "Appartamento":
            label.setVisible(False)
            input_line.setVisible(False)

        if index in integer_lines:
            input_line.setValidator(QIntValidator())

        self.input_lines[index] = input_line
        self.labels[index] = label
        self.input_errors[index] = error
        print("fine aggiunta array")

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)
        print("fine aggiunta layout")


        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)
        print(input_line)
        print(self.input_lines)
        print("---------------------- fine creazione " + index + " --------------------------")
        return input_layout

    def updateUnitaImmobiliare(self):
        temp_unitaImmobiliare = {}
        for attributo in self.sel_unitaImmobiliare.getInfoUnitaImmobiliare().keys():
            if attributo == "tipoUnitaImmobiliare":
                temp_unitaImmobiliare[attributo] = self.input_lines[attributo].currentText()
            elif attributo == "codice" or attributo == "condomini" or attributo == "immobile" or self.input_lines[attributo].text() == "":
                temp_unitaImmobiliare[attributo] = self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[attributo]
            else:
                temp_unitaImmobiliare[attributo] = self.input_lines[attributo].text()
        if temp_unitaImmobiliare['tipoUnitaImmobiliare'] != "Appartamento":
            temp_unitaImmobiliare['scala'] = "0"
            temp_unitaImmobiliare['interno'] = "0"
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
        self.callback(msg)
        self.close()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()
        self.input_lines["tipoUnitaImmobiliare"].addItems(['Appartamento', 'Box', 'Cantina', 'Negozio'])
        self.input_lines["tipoUnitaImmobiliare"].setCurrentText(self.sel_unitaImmobiliare.tipoUnitaImmobiliare)
        if self.input_lines['tipoUnitaImmobiliare'].currentText() == "Appartamento":
            self.input_lines["interno"].setVisible(True)
            self.input_lines["scala"].setVisible(True)
            self.labels["interno"].setVisible(True)
            self.labels["scala"].setVisible(True)
        self.input_errors['scala'].setVisible(False)
        self.input_errors['interno'].setVisible(False)

    def input_validation(self):
        print("scrivendo ...")
        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileByCodice(self.sel_unitaImmobiliare.immobile))
        there_is_unique_pair_error = False

        required_fields = []
        interno = self.sel_unitaImmobiliare.interno
        scala = self.sel_unitaImmobiliare.scala

        if self.input_lines['tipoUnitaImmobiliare'].currentText() == "Appartamento":
            self.input_lines["interno"].setVisible(True)
            self.input_lines["scala"].setVisible(True)
            self.labels["interno"].setVisible(True)
            self.labels["scala"].setVisible(True)
            if self.sel_unitaImmobiliare.tipoUnitaImmobiliare == "Appartamento":
                required_fields = []
            else:
                print("interno - scala", self.sel_unitaImmobiliare.interno, self.sel_unitaImmobiliare.scala)
                self.input_lines['scala'].setPlaceholderText("")
                self.input_lines['interno'].setPlaceholderText("")
                self.labels['scala'].setText("Scala*: ")
                self.labels['interno'].setText("Interno*: ")
                self.lbl_frase.setText("Inserisci i nuovi dati dell'unità immobiliare da modificare: (* Campi Obbligatori)")
                required_fields = ['interno', 'scala']
                for unita in unitaImmobiliari.values():
                    if self.input_lines['interno'].text() == str(unita.interno) and self.input_lines['scala'].text() == str(unita.scala):
                        there_is_unique_pair_error = True
                        break
        else:
            self.lbl_frase.setText("Inserisci i nuovi dati dell'unità immobiliare da modificare:")
            self.input_lines["interno"].setVisible(False)
            self.input_lines["scala"].setVisible(False)
            self.labels["interno"].setVisible(False)
            self.labels["scala"].setVisible(False)

        if self.input_lines['scala'].text():
            scala = int(self.input_lines['scala'].text())
        else:
            scala = self.sel_unitaImmobiliare.scala

        if self.input_lines['interno'].text():
            interno = int(self.input_lines['interno'].text())
        else:
            interno = self.sel_unitaImmobiliare.interno

        for unita in unitaImmobiliari.values():
            if not unita.codice == self.sel_unitaImmobiliare.codice:
                if scala != 0 and interno != 0:
                    if scala == unita.scala and interno == unita.interno:
                        there_is_unique_pair_error = True
                        break

        num_writed_lines = 0
        for field in required_fields:
            if self.input_lines[field].text():
                num_writed_lines += 1
            else:
                self.input_errors[field].setVisible(False)

        if there_is_unique_pair_error:
            self.input_errors['scala'].setText("interno già esistente nella scala inserita")
            self.input_errors['interno'].setText("")
            self.input_errors['scala'].setVisible(True)
            self.input_errors['interno'].setVisible(True)
        else:
            self.input_errors['scala'].setVisible(False)
            self.input_errors['interno'].setVisible(False)

        if num_writed_lines < len(required_fields) or there_is_unique_pair_error:
            self.buttons["Modifica Unità Immobiliare"].setDisabled(True)
        else:
            self.buttons["Modifica Unità Immobiliare"].setDisabled(False)