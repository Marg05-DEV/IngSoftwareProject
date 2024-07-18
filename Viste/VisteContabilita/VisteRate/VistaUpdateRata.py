import datetime

from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QDateEdit, QCompleter

from Classes.Contabilita.rata import Rata
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaUpdateRata(QWidget):

    def __init__(self, callback, rata_sel):
        super(VistaUpdateRata, self).__init__()
        self.callback = callback
        self.rata_selezionata = rata_sel
        main_layout = QVBoxLayout()
        self.sel_immobile = Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile).denominazione
        unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare)
        if unita.tipoUnitaImmobiliare == "Appartamento":
            proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
            self.sel_unita = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}"
        else:
            proprietario = Condomino.ricercaCondominoByCF(
                [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
            self.sel_unita = f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"
        self.input_lines = {}
        self.input_labels = {}
        self.input_errors = {}
        self.buttons = {}

        lbl_frase = QLabel("Inserisci i nuovi dati della rata da modificare:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)
        print("i")
        main_layout.addLayout(self.pairLabelInput("Immobile", "immobile"))
        print("i")
        main_layout.addLayout(self.pairLabelInput("Unita Immobiliare", "unitaImmobiliare"))
        main_layout.addLayout(self.pairLabelInput("Versante", "versante"))
        main_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))
        main_layout.addLayout(self.pairLabelInput("Numero Ricevuta", "numeroRicevuta"))
        main_layout.addLayout(self.pairLabelInput("Importo", "importo"))
        main_layout.addLayout(self.pairLabelInput("Data Pagamento", "dataPagamento"))
        main_layout.addLayout(self.pairLabelInput("Tipologia Pagamento", "tipoPagamento"))
        print("ii")
        main_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        main_layout.addWidget(self.create_button("Modifica Rata", self.updateRata))
        print("iii")
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Modifica Rata")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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

        self.input_labels[index] = label

        if index == "immobile":
            input_line = QComboBox()
            input_line.addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
            input_line.setCurrentText((Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)).denominazione)
            input_line.activated.connect(self.input_validation)
        elif index == "unitaImmobiliare":
            input_line = QComboBox()
            for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)).values():
                if unita.tipoUnitaImmobiliare == "Appartamento":
                    proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                    item = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}"
                else:
                    proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                    item = f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"

                input_line.addItem(item, unita.codice)
                if unita.codice == self.rata_selezionata.unitaImmobiliare:
                    input_line.setCurrentText(item)
            input_line.activated.connect(self.input_validation)
        elif index == "versante":
            input_line = QLineEdit()
            input_line.setPlaceholderText(self.rata_selezionata.versante)
            input_line.textChanged.connect(self.input_validation)
        elif index == "numeroRicevuta":
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.rata_selezionata.numeroRicevuta))
            input_line.setValidator(QIntValidator())
            input_line.textChanged.connect(self.input_validation)
        elif index == "importo":
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.rata_selezionata.importo))
            input_line.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*[.,][0-9]{0,2}")))
            input_line.textChanged.connect(self.input_validation)
        elif index == "dataPagamento":
            input_line = QDateEdit()
            input_line.setDate(self.rata_selezionata.dataPagamento)
            input_line.dateChanged.connect(self.input_validation)
        elif index == "tipoPagamento":
            input_line = QComboBox()
            input_line.addItems(["Contanti", "Assegno Bancario", "Bonifico Bancario"])
            input_line.setCurrentText(self.rata_selezionata.tipoPagamento)
            input_line.activated.connect(self.input_validation)
        else:
            input_line = QLineEdit()
            input_line.setPlaceholderText(self.rata_selezionata.getInfoRata()[index])
            input_line.textChanged.connect(self.input_validation)

        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def reset(self):
        print('reset')
        for key in self.input_lines.keys():
            print("si", key, self.input_lines[key])
            self.input_lines[key].clear()

        print('reset')

        self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
        self.input_lines['immobile'].setCurrentText((Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)).denominazione)

        for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)).values():
            if unita.tipoUnitaImmobiliare == "Appartamento":
                proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                item = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}"
            else:
                proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                item = f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"

            self.input_lines['unitaImmobiliare'].addItem(item, unita.codice)
            if unita.codice == self.rata_selezionata.unitaImmobiliare:
                self.input_lines['unitaImmobiliare'].setCurrentText(item)

        self.input_lines['tipoPagamento'].addItems(["Contanti", "Assegno Bancario", "Bonifico Bancario"])
        self.input_lines['tipoPagamento'].setCurrentText(self.rata_selezionata.tipoPagamento)

        self.sel_immobile = Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile).denominazione
        unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare)
        if unita.tipoUnitaImmobiliare == "Appartamento":
            proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
            self.sel_unita = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}"
        else:
            proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
            self.sel_unita = f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"

        self.input_lines['dataPagamento'].setDate(self.rata_selezionata.dataPagamento)

    def updateRata(self):
        print("in crea")
        unitaImmobiliare = self.input_lines["unitaImmobiliare"].currentData()
        versante = self.input_lines["versante"].text()
        descrizione = self.input_lines["descrizione"].text()
        numeroRicevuta = int(self.input_lines["numeroRicevuta"].text())
        importo = float((self.input_lines["importo"].text()).replace(",", "."))
        print(importo)
        dataPagamento = self.input_lines["dataPagamento"].text()
        dataPagamento = dataPagamento.split("/")
        dataPagamento = datetime.date(int(dataPagamento[2]), int(dataPagamento[1]), int(dataPagamento[0]))

        tipoPagamento = self.input_lines["tipoPagamento"].currentText()

        temp_rata = Rata()
        msg, rata = temp_rata.aggiungiRata(dataPagamento, descrizione, importo, numeroRicevuta, True, tipoPagamento,
                                           unitaImmobiliare, versante)

        self.callback(msg)
        self.close()

    def input_validation(self):
        if self.input_lines['immobile'].currentText() != self.sel_immobile:
                self.input_lines['unitaImmobiliare'].clear()
                self.input_lines['unitaImmobiliare'].setVisible(True)
                self.input_labels['unitaImmobiliare'].setVisible(True)
                self.input_lines['versante'].setVisible(False)
                self.input_labels['versante'].setVisible(False)
                self.sel_immobile = self.input_lines['immobile'].currentText()
                for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
                    if unita.tipoUnitaImmobiliare == "Appartamento":
                        proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                        self.input_lines['unitaImmobiliare'].addItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}", unita.codice)
                    else:
                        proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                        self.input_lines['unitaImmobiliare'].addItem(f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}", unita.codice)
                self.input_lines['unitaImmobiliare'].setVisible(True)
                self.input_labels['unitaImmobiliare'].setVisible(True)

        if self.input_lines['unitaImmobiliare'].currentText() != self.sel_unita:
            if self.input_lines['unitaImmobiliare'].currentText():
                self.input_lines['versante'].clear()
                self.sel_unita = self.input_lines['unitaImmobiliare'].currentText()
                advisable_versanti_list = [(Condomino.ricercaCondominoByCF(item).cognome + " " + Condomino.ricercaCondominoByCF(item).nome) for item in UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.input_lines['unitaImmobiliare'].currentData()).condomini.keys()]
                completer = QCompleter(advisable_versanti_list)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                completer.setFilterMode(Qt.MatchFlag.MatchContains)
                self.input_lines['versante'].setCompleter(completer)
                self.input_lines['versante'].setVisible(True)
                self.input_labels['versante'].setVisible(True)
