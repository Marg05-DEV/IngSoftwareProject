import datetime

from PyQt6.QtCore import QDate, Qt, QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QLineEdit, QComboBox, \
    QCompleter, QDateEdit, QCheckBox

from Classes.Contabilita.rata import Rata
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare

class VistaCreateRata(QWidget):

    def __init__(self, callback):
        super(VistaCreateRata, self).__init__()
        self.callback = callback
        main_layout = QVBoxLayout()
        self.sel_immobile = None
        self.sel_unita = None
        self.input_lines = {}
        self.input_labels = {}
        self.input_errors = {}
        self.buttons = {}
        self.required_fields = []
        print("create rata, ci siamo dentro")

        scelta_operazione_layout = QHBoxLayout()
        lbl_frase_scelta = QLabel("Scegli l'operazione che vuoi compiere: ")
        self.combo_box_operazione = QComboBox()
        self.combo_box_operazione.setPlaceholderText("Scegli...")
        self.combo_box_operazione.addItems(["Prelievo", "Versamento"])
        self.combo_box_operazione.activated.connect(self.scelta_operazione)

        scelta_operazione_layout.addWidget(lbl_frase_scelta)
        scelta_operazione_layout.addWidget(self.combo_box_operazione)
        main_layout.addLayout(scelta_operazione_layout)

        self.lbl_frase = QLabel("Inserisci i dati della nuova rata: (* Campi obbligatori)")
        self.lbl_frase.setStyleSheet("font-weight: bold;")
        self.lbl_frase.setFixedSize(self.lbl_frase.sizeHint())
        self.lbl_frase.setVisible(False)

        main_layout.addWidget(self.lbl_frase)
        print("create rata, ci siamo dentro")

        main_layout.addLayout(self.pairLabelInput("Immobile", "immobile"))
        main_layout.addLayout(self.pairLabelInput("Unita Immobiliare", "unitaImmobiliare"))
        main_layout.addLayout(self.pairLabelInput("Versante", "versante"))
        main_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))
        main_layout.addLayout(self.pairLabelInput("Numero Ricevuta", "numeroRicevuta"))
        pagamento_layout = QHBoxLayout()
        pagamento_layout.addLayout(self.pairLabelInput("Importo", "importo"))
        pagamento_layout.addLayout(self.pairLabelInput("Data Pagamento", "dataPagamento"))
        main_layout.addLayout(pagamento_layout)

        main_layout.addLayout(self.pairLabelInput("Tipologia Pagamento", "tipoPagamento"))

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        main_layout.addWidget(self.create_button("Aggiungi Rata", self.createRata))

        self.buttons["Aggiungi Rata"].setDisabled(True)

        for label in self.input_labels.values():
            label.setVisible(False)
        for input_line in self.input_lines.values():
            input_line.setVisible(False)
        for button in self.buttons.values():
            button.setVisible(False)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuova Rata")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMinimumHeight(40)
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

        label = QLabel(testo)

        if index == "immobile":
            input_line = QComboBox()
            input_line.setPlaceholderText("Seleziona l'immobile per cui si versa la rata...")
            input_line.addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
            input_line.activated.connect(self.input_validation)
        elif index == "unitaImmobiliare":
            input_line = QComboBox()
            input_line.setPlaceholderText("Seleziona l'unità immobiliare per cui si versa la rata...")
            input_line.activated.connect(self.input_validation)
            input_line.setVisible(False)
            label.setVisible(False)
        elif index == "versante":
            input_line = QLineEdit()
            input_line.setPlaceholderText("cognome nome")
            input_line.textChanged.connect(self.input_validation)
            input_line.setVisible(False)
            label.setVisible(False)
        elif index == "numeroRicevuta":
            input_line = QLineEdit()
            input_line.setValidator(QIntValidator())
            input_line.textChanged.connect(self.input_validation)
        elif index == "importo":
            input_line = QLineEdit()
            input_line.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*|[0-9]*[.,][0-9]{0,2}")))
            input_line.textChanged.connect(self.input_validation)
        elif index == "dataPagamento":
            input_line = QDateEdit()
            input_line.setDate(QDate.currentDate())
            input_line.dateChanged.connect(self.input_validation)
        elif index == "tipoPagamento":
            input_line = QComboBox()
            input_line.setPlaceholderText("Seleziona la tipologia di pagamento...")
            input_line.addItems(["Contanti", "Assegno Bancario", "Bonifico Bancario"])
            input_line.activated.connect(self.input_validation)
        else:
            input_line = QLineEdit()
            input_line.textChanged.connect(self.input_validation)

        self.input_lines[index] = input_line
        self.input_labels[index] = label
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def scelta_operazione(self):
        self.reset()
        visible_field = []
        self.lbl_frase.setVisible(True)

        if self.combo_box_operazione.currentText() == 'Prelievo':
            visible_field = ["immobile", "versante", "descrizione", "importo", "dataPagamento"]
            self.required_fields = ['versante', 'descrizione', 'importo']

            for field in self.input_lines.keys():
                if field in visible_field:
                    self.input_lines[field].setVisible(True)
                    self.input_labels[field].setVisible(True)
                else:
                    self.input_lines[field].setVisible(False)
                    self.input_labels[field].setVisible(False)

            self.input_labels["versante"].setText("Prelevante*:")
            self.input_labels["dataPagamento"].setText("Data prelievo*:")
            self.input_lines["immobile"].setPlaceholderText("Seleziona l'immobile da cui si preleva l'importo...")
            self.input_lines["unitaImmobiliare"].setPlaceholderText("Seleziona l'unità immobiliare a cui è assegnato il prelevante...")

            for button in self.buttons.values():
                button.setVisible(True)

        elif self.combo_box_operazione.currentText() == 'Versamento':
            visible_field = ["immobile", "descrizione", "importo", "numeroRicevuta", "dataPagamento", "tipoPagamento"]
            self.required_fields = ['versante', 'descrizione', 'importo', "numeroRicevuta", "tipoPagamento"]

            for field in self.input_lines.keys():
                if field in visible_field:
                    self.input_lines[field].setVisible(True)
                    self.input_labels[field].setVisible(True)
                else:
                    self.input_lines[field].setVisible(False)
                    self.input_labels[field].setVisible(False)

            self.input_labels["versante"].setText("Versante*:")
            self.input_labels["dataPagamento"].setText("Data versamento*:")
            self.input_lines["immobile"].setPlaceholderText("Seleziona l'immobile per cui si versa la rata...")
            self.input_lines["unitaImmobiliare"].setPlaceholderText("Seleziona l'unità immobiliare per cui si versa la rata...")

            for button in self.buttons.values():
                button.setVisible(True)

    def reset(self):
        self.input_lines['immobile'].clear()
        self.input_lines['immobile'].setPlaceholderText("Seleziona l'immobile per cui si versa la rata...")
        self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
        self.input_lines['tipoPagamento'].clear()
        self.input_lines['tipoPagamento'].setPlaceholderText("Seleziona la tipologia di pagamento...")
        self.input_lines['tipoPagamento'].addItems(["Contanti", "Assegno Bancario", "Bonifico Bancario"])
        self.input_lines['versante'].setVisible(False)
        self.input_labels['versante'].setVisible(False)
        self.input_lines['unitaImmobiliare'].setVisible(False)
        self.input_labels['unitaImmobiliare'].setVisible(False)

        self.input_lines["dataPagamento"].setDate(datetime.date.today())

        self.sel_immobile = None
        self.sel_unita = None
        print("fine reset")

    def createRata(self):
        print("create rata")
        importo = float((self.input_lines["importo"].text()).replace(",", "."))

        if self.combo_box_operazione.currentText() == "Prelievo":
            if self.input_lines["unitaImmobiliare"].currentIndex() < 0:
                unitaImmobiliare = 0
            else:
                unitaImmobiliare = self.input_lines["unitaImmobiliare"].currentData()
            numeroRicevuta = 0
            importo = -abs(importo)
            tipoPagamento = "Contanti"

        elif self.combo_box_operazione.currentText() == "Versamento":
            print("si versa")
            unitaImmobiliare = self.input_lines["unitaImmobiliare"].currentData()
            tipoPagamento = self.input_lines["tipoPagamento"].currentText()
            numeroRicevuta = int(self.input_lines["numeroRicevuta"].text())

        versante = self.input_lines["versante"].text()
        descrizione = self.input_lines["descrizione"].text()

        dataPagamento = self.input_lines["dataPagamento"].text()
        dataPagamento = dataPagamento.split("/")
        dataPagamento = datetime.date(int(dataPagamento[2]), int(dataPagamento[1]), int(dataPagamento[0]))


        print("rata in creazione", dataPagamento, descrizione, importo, numeroRicevuta, tipoPagamento, unitaImmobiliare, versante)
        temp_rata = Rata()
        msg, rata = temp_rata.aggiungiRata(dataPagamento, descrizione, importo, numeroRicevuta, tipoPagamento,
                                           unitaImmobiliare, versante)


        self.callback(msg)
        self.close()

    def immobile_field_dynamic(self):
        print("inizio validation")
        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            print("dentro immobile cambiato")
            if self.input_lines['immobile'].currentText():
                print("dentro immobile cambiato non vuoto")
                self.input_lines['versante'].clear()
                self.input_lines['unitaImmobiliare'].clear()
                self.input_lines['unitaImmobiliare'].setVisible(True)
                self.input_labels['unitaImmobiliare'].setVisible(True)
                self.input_lines['versante'].setVisible(False)
                self.input_labels['versante'].setVisible(False)
                self.sel_immobile = self.input_lines['immobile'].currentText()
                ultima_ricevuta = Rata.lastNumeroRicevuta(Immobile.ricercaImmobileByDenominazione(self.sel_immobile))
                print("dai")
                if ultima_ricevuta > 0:
                    self.input_lines['numeroRicevuta'].setPlaceholderText("L'ultima ricevuta inserita è la n° " + str(ultima_ricevuta))
                else:
                    self.input_lines['numeroRicevuta'].setPlaceholderText("Non ci sono ricevute precedenti")
                print("ciao")
                for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
                    if unita.tipoUnitaImmobiliare == "Appartamento":
                        proprietario = Condomino.ricercaCondominoByCF(
                            [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                        self.input_lines['unitaImmobiliare'].addItem(
                            f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di {proprietario.cognome} {proprietario.nome}",
                            unita.codice)
                    else:
                        proprietario = Condomino.ricercaCondominoByCF(
                            [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                        self.input_lines['unitaImmobiliare'].addItem(
                            f"{unita.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}", unita.codice)
                self.input_lines['unitaImmobiliare'].setVisible(True)
                self.input_labels['unitaImmobiliare'].setVisible(True)
                print("fien validation immobile sel")

    def unita_immobiliare_field_dynamic(self):
        if self.input_lines['unitaImmobiliare'].currentText() != self.sel_unita:
            if self.input_lines['unitaImmobiliare'].currentText():
                self.input_lines['versante'].clear()
                self.sel_unita = self.input_lines['unitaImmobiliare'].currentText()
                advisable_versanti_list = [
                    (Condomino.ricercaCondominoByCF(item).cognome + " " + Condomino.ricercaCondominoByCF(item).nome) for
                    item in UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(
                        self.input_lines['unitaImmobiliare'].currentData()).condomini.keys()]
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
            self.buttons["Aggiungi Rata"].setDisabled(True)
        else:
            self.buttons["Aggiungi Rata"].setDisabled(False)
