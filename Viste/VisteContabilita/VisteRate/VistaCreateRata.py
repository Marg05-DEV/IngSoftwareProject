import datetime

from PyQt6.QtCore import QDate, Qt, QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QLineEdit, QComboBox, \
    QCompleter, QDateEdit

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

        lbl_frase = QLabel("Inserisci i dati della nuova rata: (* Campi obbligatori)")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

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
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuova Rata")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
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

        label = QLabel(testo + "*: ")

        self.input_labels[index] = label

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
            input_line.setValidator(QRegularExpressionValidator(QRegularExpression("(-){0,1}[0-9]*[.,][0-9]{0,2}")))
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
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def reset(self):
        print('reset')
        for input_line in self.input_lines.values():
            input_line.clear()

        self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
        self.input_lines['tipoPagamento'].addItems(["Contanti", "Assegno Bancario", "Bonifico Bancario"])
        self.input_lines['versante'].setVisible(False)
        self.input_labels['versante'].setVisible(False)
        self.input_lines['unitaImmobiliare'].setVisible(False)
        self.input_labels['unitaImmobiliare'].setVisible(False)

        self.input_lines["dataPagamento"].setDate(datetime.date.today())

        self.sel_immobile = None
        self.sel_unita = None

    def createRata(self):
        unitaImmobiliare = self.input_lines["unitaImmobiliare"].currentData()
        versante = self.input_lines["versante"].text()
        descrizione = self.input_lines["descrizione"].text()
        numeroRicevuta = int(self.input_lines["numeroRicevuta"].text())
        importo = float((self.input_lines["importo"].text()).replace(",", "."))

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
        required_fields = ['versante', 'descrizione', 'numeroRicevuta', 'importo', 'tipoPagamento']

        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            if self.input_lines['immobile'].currentText():
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

        num_writed_lines = 0

        for field in required_fields:
            if field == 'tipoPagamento':
                if self.input_lines[field].currentText():
                    num_writed_lines += 1
            else:
                if self.input_lines[field].text():
                    num_writed_lines += 1

        if num_writed_lines < len(required_fields):
            self.buttons["Aggiungi Rata"].setDisabled(True)
        else:
            self.buttons["Aggiungi Rata"].setDisabled(False)
