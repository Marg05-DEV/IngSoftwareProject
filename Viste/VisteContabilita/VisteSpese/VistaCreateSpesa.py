import datetime

from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QCompleter, QDateEdit

from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.immobile import Immobile


class VistaCreateSpesa(QWidget):
    def __init__(self, callback):
        super(VistaCreateSpesa, self).__init__()
        self.callback = callback
        main_layout = QVBoxLayout()
        self.sel_immobile = None
        self.fornitore = None
        self.input_lines = {}
        self.input_labels = {}
        self.input_errors = {}
        self.buttons = {}

        lbl_frase = QLabel("Inserisci i dati della nuova Spesa: (* Campi obbligatori)")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)
        main_layout.addLayout(self.pairLabelInput("Immobile", "immobile"))
        main_layout.addLayout(self.pairLabelInput("Tipo Spesa", "tipoSpesa"))
        main_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))

        lbl_frase1 = QLabel("Inserisci i dati del fornitore: (* Campi obbligatori)")
        lbl_frase1.setStyleSheet("font-weight: bold;")
        lbl_frase1.setFixedSize(lbl_frase1.sizeHint())

        main_layout.addWidget(lbl_frase1)
        main_layout.addLayout(self.pairLabelInput("Denominazione", "denominazione"))
        main_layout.addLayout(self.pairLabelInput("Città", "cittaSede"))
        main_layout.addLayout(self.pairLabelInput("Indirizzo", "indirizzoSede"))
        main_layout.addLayout(self.pairLabelInput("CF/PartitaIVA", "partitaIva"))
        main_layout.addLayout(self.pairLabelInput("Tipologia", "tipoProfessione"))

        lbl_frase2 = QLabel("Dati Fattura: (* Campi obbligatori)")
        lbl_frase2.setStyleSheet("font-weight: bold;")
        lbl_frase2.setFixedSize(lbl_frase2.sizeHint())

        main_layout.addWidget(lbl_frase2)
        fattura_layout = QHBoxLayout()
        fattura_layout.addLayout(self.pairLabelInput("Numero Fattura", "numeroFattura"))
        fattura_layout.addLayout(self.pairLabelInput("Data Fattura", "dataFattura"))
        main_layout.addLayout(fattura_layout)

        lbl_frase3 = QLabel("Dati Pagamento: (* Campi obbligatori)")
        lbl_frase3.setStyleSheet("font-weight: bold;")
        lbl_frase3.setFixedSize(lbl_frase3.sizeHint())

        main_layout.addWidget(lbl_frase3)
        main_layout.addLayout(self.pairLabelInput("Importo", "importo"))
        main_layout.addWidget(self.create_checkbox("L'importo si riferisce ad una ritenuta di una spesa", 'ritenuta'))
        pagata_layout = QHBoxLayout()
        pagata_layout.addWidget(self.create_checkbox("La spesa è stata pagata", 'pagata'))
        pagata_layout.addLayout(self.pairLabelInput("Data Pagamento", "dataPagamento"))
        main_layout.addLayout(pagata_layout)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        main_layout.addWidget(self.create_button("Aggiungi Spesa", self.createSpesa))
        self.buttons["Aggiungi Spesa"].setDisabled(True)
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuova Spesa")

    def create_checkbox(self, testo, index):
        checkbox = QCheckBox(testo)
        self.checkboxes[index] = checkbox
        return checkbox
    def drawLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        self.buttons[testo] = button
        return button

    def pairLabelInput(self, testo, index):
        print("dentro pair")
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
            input_line.setPlaceholderText("Seleziona l'immobile per la spesa...")
            input_line.addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
            input_line.activated.connect(self.input_validation)
        elif index == "tipoSpesa":
            input_line = QComboBox()
            input_line.setPlaceholderText("Seleziona il tipo di spesa per la spesa...")
            input_line.activated.connect(self.input_validation)
            input_line.setVisible(False)
            label.setVisible(False)
        elif index == "descrizione":
            input_line = QLineEdit()
            input_line.setPlaceholderText("descrizione")
            input_line.textChanged.connect(self.input_validation)

        elif index == "denominazione":
            input_line = QLineEdit()
            input_line.setPlaceholderText("denominazione")
            input_line.textChanged.connect(self.input_validation)

        elif index == "cittaSede":
            input_line = QLineEdit()
            input_line.setPlaceholderText("cittaSede")
            input_line.textChanged.connect(self.input_validation)

        elif index == "indirizzoSede":
            input_line = QLineEdit()
            input_line.setPlaceholderText("indirizzoSede")
            input_line.textChanged.connect(self.input_validation)

        elif index == "partitaIva":
            input_line = QLineEdit()
            input_line.setPlaceholderText("partitaIva")
            input_line.textChanged.connect(self.input_validation)

        elif index == "tipoProfessione":
            input_line = QLineEdit()
            input_line.setPlaceholderText("tipoProfessione")
            input_line.textChanged.connect(self.input_validation)

        elif index == "numeroFattura":
            input_line = QLineEdit()
            input_line.setValidator(QIntValidator())
            input_line.textChanged.connect(self.input_validation)
        elif index == "dataFattura":
            input_line = QDateEdit()
            input_line.setDate(QDate.currentDate())
            input_line.dateChanged.connect(self.input_validation)

        elif index == "importo":
            input_line = QLineEdit()
            input_line.setValidator(QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*[.,][0-9]{0,2}")))
            input_line.textChanged.connect(self.input_validation)

        elif index == "Pagamento":
            input_line = QComboBox()
            input_line.setPlaceholderText("Seleziona...")
            input_line.addItems(["pagata", "ritenuta"])
            input_line.activated.connect(self.input_validation)

        elif index == "dataPagamento":
            input_line = QDateEdit()
            input_line.setDate(QDate.currentDate())
            input_line.dateChanged.connect(self.input_validation)
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
        self.input_lines['Pagamento'].addItems(["pagata", 'ritenuta'])

        print('reset')
        self.input_lines['tipoSpesa'].setVisible(False)
        self.input_labels['tipoSpesa'].setVisible(False)
        print('reset')

        self.sel_immobile = None

    def createSpesa(self):
        print("in crea")
        immobile = self.input_lines["immobile"].currentData()
        tipoSpesa = self.input_lines["tipoSpesa"].currentData()
        descrizione = self.input_lines["descrizione"].text()
        print("ciao")
        denominazione = self.input_lines["denominazione"].text()
        cittaSede = self.input_lines['cittaSede'].text()
        indirizzoSede = self.input_lines['indirizzoSede'].text()
        partitaIva = self.input_lines['partitaIva'].text()
        tipoProfessione = self.input_lines['tipoProfessione'].currentText()

        numeroFattura = int(self.input_lines['numeroFattura'].text())
        dataFattura = self.input_lines["dataFattura"].text()
        dataFattura = dataFattura.split("/")
        dataFattura = datetime.date(int(dataFattura[2]), int(dataFattura[1]), int(dataFattura[0]))
        importo = float((self.input_lines["importo"].text()).replace(",", "."))
        dataPagamento = self.input_lines["dataPagamento"].text()
        dataPagamento = dataPagamento.split("/")
        dataPagamento = datetime.date(int(dataPagamento[2]), int(dataPagamento[1]), int(dataPagamento[0]))
        print(dataPagamento)
        print(type(dataPagamento))

        input_line = QDateEdit()
        dataRegistrazione = input_line.setDate(QDate.currentDate())
        print(dataRegistrazione)
        print(type(dataRegistrazione))
        dataRegistrazione = dataRegistrazione.split("/")
        dataRegistrazione = datetime.date(int(dataRegistrazione[2]), int(dataRegistrazione[1]), int(dataRegistrazione[0]))

        temp_Spesa = Rata()
        msg, rata = temp_rata.aggiungiRata(dataPagamento, descrizione, importo, numeroRicevuta, True, tipoPagamento,
                                           unitaImmobiliare, versante)

        print("fatto")

        self.callback(msg)
        self.close()

    def input_validation(self):
        print("dentro la validazione")
        required_fields = ['immobile', 'tipoSpesa', 'descrizione', 'denominazione', 'cittaSede', 'indirizzoSede',
                           'partitaIva', 'tipoProfessione', 'numeroFattura', 'importo']

        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            if self.input_lines['immobile'].currentText():
                print("immobile cambiato")
                self.input_lines['tipoSpesa'].clear()
                self.input_lines['tipoSpesa'].setVisible(True)
                self.input_labels['tipoSpesa'].setVisible(True)
                self.sel_immobile = self.input_lines['immobile'].currentText()
                print("disabilizazione")
                tipi_spesa = []
                for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
                    tipi_spesa.extend(tabella.tipologiaSpesa)
                if tipi_spesa:
                    self.input_lines['tipoSpesa'].setPlaceholderText("Seleziona la tipologia di spesa...")
                    for tipo in tipi_spesa:
                        self.input_lines['tipoSpesa'].addItem(TipoSpesa.ricercaTipoSpesaByCodice(tipo).nome, tipo)
                else:

                    self.input_lines['tipoSpesa'].clear()
                    self.input_lines['tipoSpesa'].setPlaceholderText("Nessuna tipologia di spesa per questo immobile")

                self.input_lines['tipoSpesa'].setVisible(True)
                self.input_labels['tipoSpesa'].setVisible(True)

        if self.input_lines['denominazione'].text():
            print("scritto den")
            denominazioni_fornitori = [item.denominazione.upper() for item in Fornitore.getAllFornitore().values()]
            print("den", denominazioni_fornitori)
            if self.input_lines['denominazione'].text().upper() in denominazioni_fornitori:
                print("den trovata")
                fornitore = Fornitore.ricercaFornitoreByDenominazione(self.input_lines['denominazione'].text())
                self.input_lines['cittaSede'].setText(fornitore.cittaSede)
                self.input_lines['indirizzoSede'].setText(fornitore.indirizzoSede)
                self.input_lines['partitaIva'].setText(fornitore.partitaIva)
                self.input_lines['tipoProfessione'].setCurrentText(fornitore.tipoProfessione)
                self.input_lines['cittaSede'].setDisabled(True)
                self.input_lines['indirizzoSede'].setDisabled(True)
                self.input_lines['partitaIva'].setDisabled(True)
                self.input_lines['tipoProfessione'].setDisabled(True)
                self.isFornitoreTrovatoNow = True
            elif (not (self.input_lines['denominazione'].text().upper() in denominazioni_fornitori)) and self.isFornitoreTrovatoNow:
                print("denn non trovata dopo che era trovata")
                self.input_lines['cittaSede'].setText("")
                self.input_lines['indirizzoSede'].setText("")
                self.input_lines['partitaIva'].setText("")
                self.input_lines['tipoProfessione'].setCurrentText("")
                self.input_lines['cittaSede'].setDisabled(False)
                self.input_lines['indirizzoSede'].setDisabled(False)
                self.input_lines['partitaIva'].setDisabled(False)
                self.input_lines['tipoProfessione'].setDisabled(False)
                self.isFornitoreTrovatoNow = False

        print("fine controlli inserimento - inizio required")
        num_writed_lines = 0

        for field in required_fields:
            if field in ['immobile', 'tipoSpesa', 'tipoProfessione']:
                if self.input_lines[field].currentText():
                    num_writed_lines += 1
            else:
                if self.input_lines[field].text():
                    num_writed_lines += 1
        print(num_writed_lines)
        if num_writed_lines < len(required_fields):
            self.buttons["Aggiungi Spesa"].setDisabled(True)
        else:
            self.buttons["Aggiungi Spesa"].setDisabled(False)
