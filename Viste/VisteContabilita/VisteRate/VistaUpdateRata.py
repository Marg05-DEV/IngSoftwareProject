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

        self.callback = callback
        self.rata_selezionata = rata_sel

        main_layout = QVBoxLayout()
        if self.rata_selezionata.unitaImmobiliare > 0:
            self.sel_immobile = Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile).denominazione
            unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare)
            proprietario = [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"]
            if unita.tipoUnitaImmobiliare == "Appartamento":
                if unita.condomini:
                    if proprietario:
                        proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                        self.sel_unita = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}"
                    else:
                        self.sel_unita = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di Nessun Proprietario"
                else:
                    self.sel_unita = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} con Nessun condomino"
            else:
                if unita.condomini:
                    if proprietario:
                        proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                        self.sel_unita = f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"
                    else:
                        self.sel_unita = f"{unita.tipoUnitaImmobiliare} di Nessun Proprietario"
                else:
                    self.sel_unita = f"{unita.tipoUnitaImmobiliare} con Nessun Condomino"
        else:
            self.sel_immobile = None
            self.sel_unita = None
        self.input_lines = {}
        self.input_labels = {}
        self.input_errors = {}
        self.buttons = {}
        self.required_fields = []

        lbl_frase = QLabel("Inserisci i nuovi dati della rata da modificare:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)
        if self.rata_selezionata.importo < 0:
            main_layout.addLayout(self.pairLabelInput("Immobile", "immobile"))
            main_layout.addLayout(self.pairLabelInput("Unita Immobiliare", "unitaImmobiliare"))
            main_layout.addLayout(self.pairLabelInput("Prelevante", "versante"))
            main_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))
            main_layout.addLayout(self.pairLabelInput("Importo", "importo"))
            main_layout.addLayout(self.pairLabelInput("Data Prelievo", "dataPagamento"))
        elif self.rata_selezionata.importo > 0:
            main_layout.addLayout(self.pairLabelInput("Immobile", "immobile"))
            main_layout.addLayout(self.pairLabelInput("Unita Immobiliare", "unitaImmobiliare"))
            main_layout.addLayout(self.pairLabelInput("Versante", "versante"))
            main_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))
            main_layout.addLayout(self.pairLabelInput("Importo", "importo"))
            main_layout.addLayout(self.pairLabelInput("Data Versamento", "dataPagamento"))
            main_layout.addLayout(self.pairLabelInput("Numero Ricevuta", "numeroRicevuta"))
            main_layout.addLayout(self.pairLabelInput("Tipologia Pagamento", "tipoPagamento"))

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        main_layout.addWidget(self.create_button("Modifica Rata", self.updateRata))
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Modifica Rata")

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

        label = QLabel(testo + "*: ")

        self.input_labels[index] = label

        if index == "immobile":
            input_line = QComboBox()
            if self.rata_selezionata.unitaImmobiliare > 0:
                input_line.addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
                input_line.setCurrentText((Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)).denominazione)
            else:
                input_line.setPlaceholderText("Scegli l'immobile del nuovo prelevante...")
                input_line.addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
            input_line.activated.connect(self.immobile_field_dynamic)
            input_line.activated.connect(self.input_validation)
        elif index == "unitaImmobiliare":
            input_line = QComboBox()
            if self.rata_selezionata.unitaImmobiliare > 0:
                for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)).values():
                    proprietario = [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"]
                    if unita.tipoUnitaImmobiliare == "Appartamento":
                        if unita.condomini:
                            if proprietario:
                                proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                                item = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}"
                            else:
                                item = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di Nessun Proprietario"
                        else:
                            item = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} con Nessun Condomino"
                    else:
                        if unita.condomini:
                            if proprietario:
                                proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                                item = f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"
                            else:
                                item = f"{unita.tipoUnitaImmobiliare} di Nessun Proprietario"
                        else:
                            item = f"{unita.tipoUnitaImmobiliare} con Nessun Condomino"

                    input_line.addItem(item, unita.codice)
                    if unita.codice == self.rata_selezionata.unitaImmobiliare:
                        input_line.setCurrentText(item)

                input_line.setItemData(input_line.currentIndex(), self.rata_selezionata.unitaImmobiliare)
            else:
                input_line.setVisible(False)
                label.setVisible(False)
            input_line.activated.connect(self.unita_immobiliare_field_dynamic)
            input_line.activated.connect(self.input_validation)

        elif index == "versante":
            input_line = QLineEdit()
            input_line.setPlaceholderText(self.rata_selezionata.versante)
            if self.rata_selezionata.unitaImmobiliare > 0:
                advisable_versanti_list = [(Condomino.ricercaCondominoByCodice(item).cognome + " " + Condomino.ricercaCondominoByCodice(item).nome) for item in UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).condomini.keys()]
            else:
                advisable_versanti_list = []
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
            input_line.setPlaceholderText(str("%.2f" % abs(self.rata_selezionata.importo)))
            input_line.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*|[0-9]*[.,][0-9]{0,2}")))
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
        for key in self.input_lines.keys():
            self.input_lines[key].clear()

        if self.rata_selezionata.unitaImmobiliare > 0:
            self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
            self.input_lines['immobile'].setCurrentText((Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)).denominazione)
            for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile)).values():
                proprietario = [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"]
                if unita.tipoUnitaImmobiliare == "Appartamento":
                    if unita.condomini:
                        if proprietario:
                            proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                            item = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}"
                        else:
                            item = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di Nessun Proprietario"
                    else:
                        item = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} con Nessun Condomino"
                else:
                    if unita.condomini:
                        if proprietario:
                            proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                            item = f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"
                        else:
                            item = f"{unita.tipoUnitaImmobiliare} di Nessun Proprietario"
                    else:
                        item = f"{unita.tipoUnitaImmobiliare} con Nessun Condomino"

                self.input_lines['unitaImmobiliare'].addItem(item, unita.codice)
                if unita.codice == self.rata_selezionata.unitaImmobiliare:
                    self.input_lines['unitaImmobiliare'].setCurrentText(item)

            if self.rata_selezionata.importo > 0:
                self.input_lines['tipoPagamento'].addItems(["Contanti", "Assegno Bancario", "Bonifico Bancario"])
                self.input_lines['tipoPagamento'].setCurrentText(self.rata_selezionata.tipoPagamento)

            self.sel_immobile = Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare).immobile).denominazione
            unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata_selezionata.unitaImmobiliare)
            proprietario = [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"]
            if unita.tipoUnitaImmobiliare == "Appartamento":
                if unita.condomini:
                    if proprietario:
                        proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                        self.sel_unita = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}"
                    else:
                        self.sel_unita = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di Nessun Proprietario"
                else:
                    self.sel_unita = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} con Nessun Condomino"
            else:
                if unita.condomini:
                    if proprietario:
                        proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                        self.sel_unita = f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"
                    else:
                        self.sel_unita = f"{unita.tipoUnitaImmobiliare} di Nessun Proprietario"
                else:
                    self.sel_unita = f"{unita.tipoUnitaImmobiliare} con Nessun Condomino"
        else:
            self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
            self.input_lines['unitaImmobiliare'].setVisible(False)
            self.input_labels['unitaImmobiliare'].setVisible(False)
        self.input_lines['dataPagamento'].setDate(self.rata_selezionata.dataPagamento)
        self.input_lines['versante'].setPlaceholderText(self.rata_selezionata.versante)

    def updateRata(self):
        temp_rata = {}

        if self.rata_selezionata.getInfoRata()['importo'] < 0:
            for attributo in self.rata_selezionata.getInfoRata().keys():
                if attributo == "unitaImmobiliare":
                    if self.input_lines[attributo].currentIndex() >= 0:
                        temp_rata[attributo] = self.input_lines[attributo].currentData()
                    else:
                        temp_rata[attributo] = 0
                elif attributo in ["codice", "isLast", "tipoPagamento", "numeroRicevuta"] or not self.input_lines[attributo].text():
                    temp_rata[attributo] = self.rata_selezionata.getInfoRata()[attributo]
                elif attributo == 'importo':
                    temp_rata['importo'] = -abs(float((self.input_lines["importo"].text()).replace(",", ".")))
                else:
                    temp_rata[attributo] = self.input_lines[attributo].text()

        else:
            for attributo in self.rata_selezionata.getInfoRata().keys():
                if attributo == "unitaImmobiliare":
                    temp_rata[attributo] = self.input_lines[attributo].currentData()
                elif attributo == "tipoPagamento":
                    temp_rata[attributo] = self.input_lines[attributo].currentText()
                elif attributo in ["codice", "isLast"] or not self.input_lines[attributo].text():
                    temp_rata[attributo] = self.rata_selezionata.getInfoRata()[attributo]
                elif attributo == 'importo':
                    temp_rata['importo'] = abs(float((self.input_lines["importo"].text()).replace(",", ".")))
                else:
                    temp_rata[attributo] = self.input_lines[attributo].text()

        dataPagamento = temp_rata["dataPagamento"].split('/')
        dataPagamento = datetime.date(int(dataPagamento[2]), int(dataPagamento[1]), int(dataPagamento[0]))

        msg = self.rata_selezionata.modificaRata(dataPagamento,
                                                 temp_rata['descrizione'],
                                                 temp_rata['importo'],
                                                 int(temp_rata['numeroRicevuta']),
                                                 temp_rata['tipoPagamento'],
                                                 temp_rata['unitaImmobiliare'],
                                                 temp_rata['versante'])
        self.callback(msg)
        self.close()

    def immobile_field_dynamic(self):
        num_errors = 0
        there_is_unique_error = {}
        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            if self.input_lines['immobile'].currentText():
                self.input_lines['unitaImmobiliare'].clear()
                self.input_lines['unitaImmobiliare'].setPlaceholderText("Seleziona l'unità immobiliare per cui si versa la rata...")
                if 'versante' not in self.required_fields:
                    self.required_fields.append('versante')
                self.sel_unita = None
                self.input_lines['unitaImmobiliare'].setVisible(True)
                self.input_labels['unitaImmobiliare'].setVisible(True)
                self.input_lines['versante'].setVisible(False)
                self.input_labels['versante'].setVisible(False)
                self.sel_immobile = self.input_lines['immobile'].currentText()
                for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
                    proprietario = [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0]
                    if unita.tipoUnitaImmobiliare == "Appartamento":
                        if unita.condomini:
                            if proprietario:
                                proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                                self.input_lines['unitaImmobiliare'].addItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}", unita.codice)
                            else:
                                self.input_lines['unitaImmobiliare'].addItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di Nessun Proprietario", unita.codice)
                        else:
                            self.input_lines['unitaImmobiliare'].addItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} con Nessun Condomino", unita.codice)
                    else:
                        if unita.condomini:
                            if proprietario:
                                proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                                self.input_lines['unitaImmobiliare'].addItem(
                                    f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}", unita.codice)
                            else:
                                self.input_lines['unitaImmobiliare'].addItem(
                                    f"{unita.tipoUnitaImmobiliare} di Nessun Proprietario", unita.codice)
                        else:
                            self.input_lines['unitaImmobiliare'].addItem(
                                f"{unita.tipoUnitaImmobiliare} con Nessun Condomino", unita.codice)

    def unita_immobiliare_field_dynamic(self):
        if self.input_lines['unitaImmobiliare'].currentText() != self.sel_unita:
            if self.input_lines['unitaImmobiliare'].currentText():
                self.input_lines['versante'].clear()
                self.input_lines['versante'].setPlaceholderText("cognome nome")
                if 'versante' not in self.required_fields:
                    self.required_fields.append('versante')
                self.sel_unita = self.input_lines['unitaImmobiliare'].currentText()
                advisable_versanti_list = [(Condomino.ricercaCondominoByCodice(item).cognome + " " + Condomino.ricercaCondominoByCodice(item).nome) for item in UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.input_lines['unitaImmobiliare'].currentData()).condomini.keys()]
                completer = QCompleter(advisable_versanti_list)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                completer.setFilterMode(Qt.MatchFlag.MatchContains)
                self.input_lines['versante'].setCompleter(completer)
                self.input_lines['versante'].setVisible(True)
                self.input_labels['versante'].setVisible(True)

    def input_validation(self):
        num_writed_lines = 0

        for field in self.required_fields:
            if field == 'tipoPagamento':
                if self.input_lines[field].currentText():
                    num_writed_lines += 1
            else:
                if self.input_lines[field].text():
                    num_writed_lines += 1
        if num_writed_lines < len(self.required_fields):
            self.buttons["Modifica Rata"].setDisabled(True)
        else:
            self.buttons["Modifica Rata"].setDisabled(False)