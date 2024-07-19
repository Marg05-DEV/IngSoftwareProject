import datetime

from PyQt6.QtCore import Qt, QDate, QRegularExpression, QLine
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QCompleter, QDateEdit, QFrame, QCheckBox

from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.immobile import Immobile


class VistaUpdateSpesa(QWidget):
    def __init__(self, spesa, callback):
        super(VistaUpdateSpesa, self).__init__()
        self.spesa = spesa
        self.callback = callback
        self.sel_immobile = Immobile.ricercaImmobileById(self.spesa.immobile).denominazione
        self.input_lines = {}
        self.input_labels = {}
        self.input_errors = {}
        self.buttons = {}
        self.checkboxes = {}
        self.isFornitoreTrovatoNow = False
        main_layout = QVBoxLayout()
        lbl_frase = QLabel("Modifica Spesa:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)
        main_layout.addLayout(self.pairLabelInput("Immobile", "immobile"))
        main_layout.addLayout(self.pairLabelInput("Tipo Spesa", "tipoSpesa"))
        main_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))

        lbl_frase1 = QLabel("Modifica dati fornitore:")
        lbl_frase1.setStyleSheet("font-weight: bold;")
        lbl_frase1.setFixedSize(lbl_frase1.sizeHint())

        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(lbl_frase1)
        main_layout.addLayout(self.pairLabelInput("Denominazione", "denominazione"))
        luogo_fornitore_layout = QHBoxLayout()
        luogo_fornitore_layout.addLayout(self.pairLabelInput("Città", "cittaSede"))
        luogo_fornitore_layout.addLayout(self.pairLabelInput("Indirizzo", "indirizzoSede"))
        info_fornitore_layout = QHBoxLayout()
        info_fornitore_layout.addLayout(self.pairLabelInput("CF/Partita IVA", "partitaIva"))
        info_fornitore_layout.addLayout(self.pairLabelInput("Tipologia", "tipoProfessione"))

        main_layout.addLayout(luogo_fornitore_layout)
        main_layout.addLayout(info_fornitore_layout)

        lbl_frase2 = QLabel("Modifica dati fattura")
        lbl_frase2.setStyleSheet("font-weight: bold;")
        lbl_frase2.setFixedSize(lbl_frase2.sizeHint())

        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(lbl_frase2)
        fattura_layout = QHBoxLayout()
        fattura_layout.addLayout(self.pairLabelInput("Numero Fattura", "numeroFattura"))
        fattura_layout.addLayout(self.pairLabelInput("Data Fattura", "dataFattura"))
        main_layout.addLayout(fattura_layout)

        lbl_frase3 = QLabel("Modifica dati pagamento:")
        lbl_frase3.setStyleSheet("font-weight: bold;")
        lbl_frase3.setFixedSize(lbl_frase3.sizeHint())

        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(lbl_frase3)
        main_layout.addLayout(self.pairLabelInput("Importo", "importo"))
        main_layout.addWidget(self.create_checkbox("L'importo si riferisce ad una ritenuta di una spesa", 'ritenuta'))
        pagata_layout = QHBoxLayout()
        pagata_layout.addWidget(self.create_checkbox("La spesa è stata pagata", 'pagata'))
        pagata_layout.addLayout(self.pairLabelInput("Data Pagamento", "dataPagamento"))
        main_layout.addLayout(pagata_layout)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        main_layout.addWidget(self.create_button("Modifica Spesa", self.updateSpesa))
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Modifica Spesa")
    def create_checkbox(self, testo, index):
        checkbox = QCheckBox(testo)
        self.checkboxes[index] = checkbox
        if self.spesa.getInfoSpesa()[index]:
            checkbox.checkStateSet()
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
            input_line.addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
            input_line.setCurrentText(Immobile.ricercaImmobileById(self.spesa.immobile).denominazione)
            input_line.activated.connect(self.input_validation)
        elif index == "tipoSpesa":
            input_line = QComboBox()
            tipo = TipoSpesa.ricercaTipoSpesaByCodice(self.spesa.tipoSpesa).nome
            input_line.setPlaceholderText(tipo)
            input_line.activated.connect(self.input_validation)
        elif index == "numeroFattura":
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.spesa.numeroFattura))
            input_line.setValidator(QIntValidator())
            input_line.textChanged.connect(self.input_validation)
        elif index == "dataFattura":
            input_line = QDateEdit()
            input_line.setDate(self.spesa.dataFattura)
            input_line.dateChanged.connect(self.input_validation)
        elif index == "importo":
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.spesa.importo))
            input_line.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*[.,][0-9]{0,2}")))
            input_line.textChanged.connect(self.input_validation)
        elif index == "dataPagamento":
            input_line = QDateEdit()
            input_line.setDate(self.spesa.dataPagamento)
            input_line.dateChanged.connect(self.input_validation)
        elif index == 'denominazione':
            input_line = QLineEdit()
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore).denominazione
            input_line.setPlaceholderText(str(fornitore))
            fornitori_list = [item.denominazione for item in Fornitore.getAllFornitore().values()]
            completer = QCompleter(fornitori_list)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            input_line.setCompleter(completer)
            input_line.textChanged.connect(self.input_validation)
        elif index == "tipoProfessione":
            input_line = QComboBox()
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore).tipoProfessione
            input_line.addItems(['Ditta', 'Professionista', 'AC'])
            input_line.setCurrentText(str(fornitore))
            input_line.activated.connect(self.input_validation)
        else:
            input_line = QLineEdit()
            input_line.setPlaceholderText(str(self.spesa.getInfoSpesa()[index]))
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
            print("si", key, self.input_lines[key])
            self.input_lines[key].clear()

        self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
        self.input_lines['immobile'].setCurrentText(Immobile.ricercaImmobileById(self.spesa.immobile).denominazione)

        for tabelle in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(self.spesa.immobile)).values():
            for tipo in tabelle:
                if tipo.tipologiaSpesa:
                    self.input_lines['tipoSpesa'].addItems
        self.input_lines['tipoSpesa'].setVisible(False)
        self.input_labels['tipoSpesa'].setVisible(False)
        print('reset')
        fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
        self.input_lines['tipoProfessione'].addItems(['Ditta', 'Professionista', 'AC'])
        self.input_lines['tipoProfessione'].setCurrentText(fornitore.tipoProfessione)
        print('fine reset')

        if self.spesa.pagata:
            self.checkboxes['pagata'].setCheckState(Qt.CheckState.Checked)
        else:
            print('non pagata')
            print(self.checkboxes['pagata'])
            self.checkboxes['pagata'].setCheckState(Qt.CheckState.Unchecked)
        print("fineprimo check")
        if self.spesa.isRitenuta:
            self.checkboxes['isRitenuta'].setCheckState(Qt.CheckState.Checked)
        else:
            self.checkboxes['isRitenuta'].setCheckState(Qt.CheckState.Unchecked)
        print("fine fcheck")
        self.input_lines['dataPagamento'].setDate(self.spesa.dataPagamento)
        self.input_lines['dataFattura'].setDate(self.spesa.dataFattura)
        print("fine fine rest")


    def updateSpesa(self):
        print("in crea")
        immobile = Immobile.ricercaImmobileByDenominazione(self.input_lines["immobile"].currentText()).id
        print("ciao")
        tipoSpesa = self.input_lines["tipoSpesa"].currentData()
        print("ciao")
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

        fornitore_esistente = False
        for fornitore in Fornitore.getAllFornitore().values():
            if fornitore.denominazione == denominazione:
                fornitore_esistente = True

        if fornitore_esistente:
            fornitore = Fornitore.ricercaFornitoreByDenominazione(denominazione)
        else:
            temp_fornitore = Fornitore()
            msg, fornitore = temp_fornitore.aggiungiFornitore(cittaSede, denominazione, indirizzoSede, partitaIva,
                                                              tipoProfessione)

        temp_spesa = Spesa()
        msg, spesa = temp_spesa.aggiungiSpesa(descrizione, fornitore.codice, importo, tipoSpesa, immobile,
                                              self.checkboxes['pagata'].isChecked(), dataPagamento, dataFattura,
                                              datetime.date.today(), self.checkboxes['ritenuta'].isChecked(),
                                              numeroFattura)
        self.callback(msg)
        self.close()

    def input_validation(self):
        print("dentro la validazione")
        required_fields = ['immobile', 'tipoSpesa', 'descrizione', 'denominazione', 'cittaSede', 'indirizzoSede',
                           'partitaIva', 'tipoProfessione', 'numeroFattura', 'importo']

        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            print("immobile modificato")
            if self.input_lines['immobile'].currentText():
                print("immobile valido")
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
            denominazioni_fornitori = [item.denominazione.upper() for item in Fornitore.getAllFornitore().values()]
            if self.input_lines['denominazione'].text().upper() in denominazioni_fornitori:
                print("den trovata")
                fornitore = Fornitore.ricercaFornitoreByDenominazione(self.input_lines['denominazione'].text())
                self.input_lines['cittaSede'].setText(fornitore.cittaSede)
                self.input_lines['indirizzoSede'].setText(fornitore.indirizzoSede)
                self.input_lines['partitaIva'].setText(fornitore.partitaIva)
                self.input_lines['tipoProfessione'].setCurrentText(fornitore.tipoProfessione)
                self.isFornitoreTrovatoNow = True
            elif (not (self.input_lines['denominazione'].text().upper() in denominazioni_fornitori)) and self.isFornitoreTrovatoNow:
                print("denn non trovata dopo che era trovata")
                self.input_lines['cittaSede'].setText("")
                self.input_lines['indirizzoSede'].setText("")
                self.input_lines['partitaIva'].setText("")
                self.input_lines['tipoProfessione'].setCurrentText("")
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

        if num_writed_lines < len(required_fields):
            self.buttons["Aggiungi Spesa"].setDisabled(True)
        else:
            self.buttons["Aggiungi Spesa"].setDisabled(False)
