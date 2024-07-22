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

    def __init__(self, rata_sel, callback):
        super(VistaUpdateRata, self).__init__()
        print("mimi")
        self.callback = callback
        self.rata_selezionata = rata_sel
        main_layout = QVBoxLayout()
        print(self.rata_selezionata)
        print(self.rata_selezionata.unitaImmobiliare)
        print(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)
        self.sel_immobile = Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile).denominazione
        unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare)
        print("uuu")
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
        print("2")
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + "*: ")

        self.input_labels[index] = label
        print("aio")
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

            input_line.setItemData(input_line.currentIndex(), self.rata_selezionata.unitaImmobiliare)
            input_line.activated.connect(self.input_validation)

        elif index == "versante":
            input_line = QLineEdit()
            input_line.setPlaceholderText(self.rata_selezionata.versante)
            advisable_versanti_list = [(Condomino.ricercaCondominoByCF(item).cognome + " " + Condomino.ricercaCondominoByCF(item).nome) for item in UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).condomini.keys()]
            completer = QCompleter(advisable_versanti_list)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            input_line.setCompleter(completer)
            input_line.textChanged.connect(self.input_validation)
        elif index == "numeroRicevuta":
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.rata_selezionata.numeroRicevuta))
            input_line.setValidator(QIntValidator())
            input_line.textChanged.connect(self.input_validation)
        elif index == "importo":
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.rata_selezionata.importo))
            input_line.setValidator(QRegularExpressionValidator(QRegularExpression("(-){0,1}[0-9]*[.,][0-9]{0,2}")))
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
        print("cici")
        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def reset(self):
        for key in self.input_lines.keys():
            print("si", key, self.input_lines[key])
            self.input_lines[key].clear()

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
        self.input_lines['versante'].setPlaceholderText(self.rata_selezionata.versante)

    def updateRata(self):
        temp_rata = {}
        print("si modifica")
        for attributo in self.rata_selezionata.getInfoRata().keys():
            print("si modifica", attributo)
            if attributo == "unitaImmobiliare":
                temp_rata[attributo] = self.input_lines[attributo].currentData()
            elif attributo == "tipoPagamento":
                temp_rata[attributo] = self.input_lines[attributo].currentText()
            elif attributo in ["codice", "pagata"] or not self.input_lines[attributo].text():
                temp_rata[attributo] = self.rata_selezionata.getInfoRata()[attributo]
            else:
                temp_rata[attributo] = self.input_lines[attributo].text()

        print(temp_rata)

        dataPagamento = temp_rata["dataPagamento"].split('/')
        dataPagamento = datetime.date(int(dataPagamento[2]), int(dataPagamento[1]), int(dataPagamento[0]))

        msg = self.rata_selezionata.modificaRata(dataPagamento,
                                                 temp_rata['descrizione'],
                                                 float(temp_rata['importo']),
                                                 int(temp_rata['numeroRicevuta']),
                                                 True,
                                                 temp_rata['tipoPagamento'],
                                                 int(temp_rata['unitaImmobiliare']),
                                                 temp_rata['versante'])
        self.callback(msg)
        self.close()

    def input_validation(self):
        required_fields = []
        num_errors = 0
        there_is_unique_error = {}
        print('validation')
        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            if self.input_lines['immobile'].currentText():
                self.input_lines['unitaImmobiliare'].clear()
                self.input_lines['unitaImmobiliare'].setPlaceholderText("Seleziona l'unità immobiliare per cui si versa la rata...")
                required_fields.append('versante')
                self.sel_unita = None
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

        if self.input_lines['unitaImmobiliare'].currentText() != self.sel_unita:
            if self.input_lines['unitaImmobiliare'].currentText():
                self.input_lines['versante'].clear()
                self.input_lines['versante'].setPlaceholderText("cognome nome")
                required_fields.append('versante')
                self.sel_unita = self.input_lines['unitaImmobiliare'].currentText()
                advisable_versanti_list = [(Condomino.ricercaCondominoByCF(item).cognome + " " + Condomino.ricercaCondominoByCF(item).nome) for item in UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.input_lines['unitaImmobiliare'].currentData()).condomini.keys()]
                completer = QCompleter(advisable_versanti_list)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                completer.setFilterMode(Qt.MatchFlag.MatchContains)
                self.input_lines['versante'].setCompleter(completer)
                self.input_lines['versante'].setVisible(True)
                self.input_labels['versante'].setVisible(True)
        print("prima della ricevuta")
        if self.input_lines['numeroRicevuta'].text():
            rate = Rata.getAllRateByImmobile(Immobile.ricercaImmobileByDenominazione(self.input_lines['immobile'].currentText())).values()
            for rata in rate:
                print(rata)
                there_is_unique_error["numeroRicevuta"] = False

                print(str(rata.getInfoRata()["numeroRicevuta"]))
                print(str(self.rata_selezionata.getInfoRata()["numeroRicevuta"]))
                print(self.input_lines["numeroRicevuta"].text())
                print(str(rata.getInfoRata()["numeroRicevuta"]))

                if str(rata.getInfoRata()["numeroRicevuta"]) != str(self.rata_selezionata.getInfoRata()["numeroRicevuta"]):
                    if self.input_lines["numeroRicevuta"].text() == str(rata.getInfoRata["numeroRicevuta"]):
                        num_errors += 1
                        there_is_unique_error["numeroRicevuta"] = True
                        break
            if there_is_unique_error["numeroRicevuta"]:
                self.input_errors["numeroRicevuta"].setText(f"nuemero ricevuta già esistente")
                self.input_errors["numeroRicevuta"].setVisible(True)
            else:
                self.input_errors["numeroRicevuta"].setVisible(False)

        num_writed_lines = 0

        for field in required_fields:
            if field == 'tipoPagamento':
                if self.input_lines[field].currentText():
                    num_writed_lines += 1
            else:
                if self.input_lines[field].text():
                    num_writed_lines += 1
        print(num_writed_lines)
        if num_writed_lines < len(required_fields):
            self.buttons["Modifica Rata"].setDisabled(True)
        else:
            self.buttons["Modifica Rata"].setDisabled(False)