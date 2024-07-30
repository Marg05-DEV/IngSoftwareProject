import datetime
import qtawesome

from PyQt6.QtCore import Qt, QDate, QRegularExpression, QLine
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QComboBox, QLineEdit, \
    QCompleter, QDateEdit, QFrame, QCheckBox

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
        self.checkboxes = {}
        self.isFornitoreTrovatoNow = False
        self.numDividendi = 0
        self.tipi_spesa = []

        self.required_fields = ['immobile', 'tipoSpesa0', 'descrizione', 'denominazione', 'cittaSede', 'indirizzoSede',
                                'partitaIva', 'tipoProfessione', 'numeroFattura', 'importo']

        lbl_frase = QLabel("Inserisci i dati della nuova spesa: (* Campi obbligatori)")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)
        main_layout.addLayout(self.pairLabelInput("Immobile", "immobile"))

        self.dividendi_layout = QVBoxLayout()

        btn_aggiungiDividendi = self.create_button("Aggiungi Dividendo", self.addDividendo)
        self.dividendi_layout.addWidget(btn_aggiungiDividendi, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        btn_aggiungiDividendi.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        btn_aggiungiDividendi.setVisible(False)
        btn_aggiungiDividendi.setIcon(qtawesome.icon("fa.plus"))

        self.addDividendo()
        main_layout.addLayout(self.dividendi_layout)

        main_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))

        lbl_frase1 = QLabel("Inserisci i dati del fornitore: (* Campi obbligatori)")
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

        lbl_frase2 = QLabel("Dati Fattura: (* Campi obbligatori)")
        lbl_frase2.setStyleSheet("font-weight: bold;")
        lbl_frase2.setFixedSize(lbl_frase2.sizeHint())

        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(lbl_frase2)
        fattura_layout = QHBoxLayout()
        fattura_layout.addLayout(self.pairLabelInput("Numero Fattura", "numeroFattura"))
        fattura_layout.addLayout(self.pairLabelInput("Data Fattura", "dataFattura"))
        main_layout.addLayout(fattura_layout)

        lbl_frase3 = QLabel("Dati Pagamento: (* Campi obbligatori)")
        lbl_frase3.setStyleSheet("font-weight: bold;")
        lbl_frase3.setFixedSize(lbl_frase3.sizeHint())

        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(lbl_frase3)
        main_layout.addLayout(self.pairLabelInput("Importo", "importo"))
        main_layout.addWidget(self.create_checkbox("L'importo si riferisce ad una ritenuta di una spesa", 'isRitenuta'))
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
        button.setCheckable(False)
        button.setMaximumHeight(40)
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
            input_line.setPlaceholderText("Seleziona l'immobile a cui si riferisce la spesa...")
            input_line.addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
            input_line.activated.connect(self.immobile_field_dynamic)
            input_line.activated.connect(self.input_validation)
        elif "tipoSpesa" in index:
            input_line = QComboBox()
            input_line.setPlaceholderText("Seleziona la tipologia di spesa...")
            input_line.activated.connect(self.dividendi_fields_dynamic)
            input_line.activated.connect(self.input_validation)
            input_line.setVisible(False)
            label.setVisible(False)
        elif "dividendo" in index:
            print("inizio dividendo in pair", testo)
            input_line = QLineEdit()
            input_line.setPlaceholderText("in percentuale")
            input_line.setValidator(QIntValidator(0, 99))
            input_line.textChanged.connect(self.dividendi_fields_dynamic)
            input_line.textChanged.connect(self.input_validation)
            input_line.setVisible(False)
            label.setVisible(False)
            print("fine dividendo in pair")
        elif index == "numeroFattura":
            input_line = QLineEdit()
            input_line.setValidator(QIntValidator())
            input_line.textChanged.connect(self.input_validation)
        elif index == "dataFattura":
            input_line = QDateEdit()
            input_line.dateChanged.connect(self.input_validation)
        elif index == "importo":
            input_line = QLineEdit()
            input_line.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*|([0-9]*[.,][0-9]{0,2})")))
            input_line.textChanged.connect(self.input_validation)
        elif index == "dataPagamento":
            input_line = QDateEdit()
            input_line.setDate(QDate.currentDate())
            input_line.dateChanged.connect(self.input_validation)
        elif index == 'denominazione':
            input_line = QLineEdit()
            fornitori_list = [item.denominazione for item in Fornitore.getAllFornitore().values()]
            completer = QCompleter(fornitori_list)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            input_line.setCompleter(completer)
            input_line.textChanged.connect(self.fornitore_fields_dynamic)
            input_line.textChanged.connect(self.input_validation)
        elif index == "tipoProfessione":
            input_line = QComboBox()
            input_line.setPlaceholderText("Seleziona il tipo di professione del fornitore...")
            input_line.addItems(['Ditta', 'Professionista', 'AC'])
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

    def addDividendo(self):
        dividendo_layout = QHBoxLayout()

        dividendo_layout.addLayout(self.pairLabelInput("Tipo Spesa", "tipoSpesa" + str(self.numDividendi)))
        dividendo_layout.addLayout(self.pairLabelInput("%", "dividendo" + str(self.numDividendi)))

        if self.numDividendi > 0:
            if 'dividendo0' not in self.required_fields:
                self.required_fields.append('dividendo0')
            self.buttons['Aggiungi Spesa'].setDisabled(True)
            self.required_fields.append(f"tipoSpesa{self.numDividendi}")
            self.required_fields.append(f"dividendo{self.numDividendi}")
            self.input_lines["dividendo0"].setVisible(True)
            self.input_labels["dividendo0"].setVisible(True)
            self.input_lines[f"tipoSpesa{self.numDividendi}"].setVisible(True)
            self.input_labels[f"tipoSpesa{self.numDividendi}"].setVisible(True)
            self.input_lines[f"dividendo{self.numDividendi}"].setVisible(True)
            self.input_labels[f"dividendo{self.numDividendi}"].setVisible(True)

            self.tipi_spesa = []

            for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
                self.tipi_spesa.extend(tabella.tipologieSpesa)

            for cod_tipo in self.tipi_spesa:
                tipo_just_selected = False

                tipo = TipoSpesa.ricercaTipoSpesaByCodice(cod_tipo)
                for i in range(self.numDividendi):
                    if self.input_lines[f'tipoSpesa{i}'].currentText():
                        if self.input_lines[f'tipoSpesa{i}'].currentText() == tipo.nome:
                            tipo_just_selected = True

                if not tipo_just_selected:
                    self.input_lines[f'tipoSpesa{self.numDividendi}'].addItem(tipo.nome, cod_tipo)

        self.numDividendi += 1

        if self.numDividendi >= len(self.tipi_spesa):
            self.buttons["Aggiungi Dividendo"].setDisabled(True)

        print("fatto, num dividendi attuale", self.numDividendi)
        self.dividendi_layout.insertLayout(self.numDividendi - 1, dividendo_layout)
        self.dividendi_layout.removeWidget(self.buttons["Aggiungi Dividendo"])
        self.dividendi_layout.insertWidget(self.numDividendi, self.buttons["Aggiungi Dividendo"])


    def reset(self):
        print("input lin pre reset", self.input_lines)
        for input_line in self.input_lines.values():
            input_line.clear()

        self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])

        self.input_lines['tipoSpesa0'].setVisible(False)
        self.input_labels['tipoSpesa0'].setVisible(False)
        self.input_lines['dividendo0'].setVisible(False)
        self.input_labels['dividendo0'].setVisible(False)

        if self.numDividendi > 1:
            for i in range(1, self.numDividendi):
                self.dividendi_layout.removeWidget(self.input_lines['tipoSpesa' + str(i)])
                self.dividendi_layout.removeWidget(self.input_labels['tipoSpesa' + str(i)])
                self.dividendi_layout.removeWidget(self.input_lines['dividendo' + str(i)])
                self.dividendi_layout.removeWidget(self.input_labels['dividendo' + str(i)])
                del self.input_lines['tipoSpesa' + str(i)]
                del self.input_labels['tipoSpesa' + str(i)]
                del self.input_lines['dividendo' + str(i)]
                del self.input_labels['dividendo' + str(i)]

        self.buttons["Aggiungi Dividendo"].setVisible(False)
        self.numDividendi = 1

        self.input_lines["dataPagamento"].setDate(datetime.date.today())
        self.input_lines["dataFattura"].setDate(datetime.date(2000, 1, 1))
        self.input_lines['tipoProfessione'].addItems(['Ditta', 'Professionista', 'AC'])

        self.sel_immobile = None

        self.required_fields = ['immobile', 'tipoSpesa0', 'descrizione', 'denominazione', 'cittaSede', 'indirizzoSede',
                                'partitaIva', 'tipoProfessione', 'numeroFattura', 'importo']

    def createSpesa(self):
        immobile = Immobile.ricercaImmobileByDenominazione(self.input_lines["immobile"].currentText()).id

        descrizione = self.input_lines["descrizione"].text()
        denominazione = self.input_lines["denominazione"].text()
        cittaSede = self.input_lines['cittaSede'].text()
        indirizzoSede = self.input_lines['indirizzoSede'].text()
        partitaIva = self.input_lines['partitaIva'].text()
        tipoProfessione = self.input_lines['tipoProfessione'].currentText()

        numeroFattura = int(self.input_lines['numeroFattura'].text())

        dataFattura = self.input_lines["dataFattura"].text()
        dataFattura = dataFattura.split("/")
        dataFattura = datetime.date(int(dataFattura[2]), int(dataFattura[1]), int(dataFattura[0]))

        dataPagamento = self.input_lines["dataPagamento"].text()
        dataPagamento = dataPagamento.split("/")
        dataPagamento = datetime.date(int(dataPagamento[2]), int(dataPagamento[1]), int(dataPagamento[0]))

        if not self.checkboxes['pagata'].isChecked():
            dataPagamento = None

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

        for i in range(self.numDividendi):
            importo = float((self.input_lines["importo"].text()).replace(",", "."))
            tipoSpesa = self.input_lines[f"tipoSpesa{i}"].currentData()
            if self.numDividendi > 1:
                importo = importo * int(self.input_lines[f"dividendo{i}"].text()) / 100

            temp_spesa = Spesa()
            msg, spesa = temp_spesa.aggiungiSpesa(descrizione, fornitore.codice, importo, tipoSpesa, immobile,
                                                  self.checkboxes['pagata'].isChecked(), dataPagamento, dataFattura,
                                                  datetime.date.today(), self.checkboxes['isRitenuta'].isChecked(),
                                                  numeroFattura)
        self.callback(msg)
        self.close()

    def immobile_field_dynamic(self):
        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            if self.input_lines['immobile'].currentText():
                self.input_lines['tipoSpesa0'].clear()
                self.input_lines['tipoSpesa0'].setVisible(True)
                self.input_labels['tipoSpesa0'].setVisible(True)
                self.input_lines['dividendo0'].setVisible(False)
                self.input_labels['dividendo0'].setVisible(False)
                if 'dividendo0' in self.required_fields:
                    self.required_fields.remove('dividendo0')
                if self.numDividendi > 1:
                    for i in range(1, self.numDividendi):
                        self.required_fields.remove('tipoSpesa' + str(i))
                        self.required_fields.remove('dividendo' + str(i))
                        self.dividendi_layout.removeWidget(self.input_lines['tipoSpesa' + str(i)])
                        self.dividendi_layout.removeWidget(self.input_labels['tipoSpesa' + str(i)])
                        self.dividendi_layout.removeWidget(self.input_lines['dividendo' + str(i)])
                        self.dividendi_layout.removeWidget(self.input_labels['dividendo' + str(i)])
                        del self.input_lines['tipoSpesa' + str(i)]
                        del self.input_labels['tipoSpesa' + str(i)]
                        del self.input_lines['dividendo' + str(i)]
                        del self.input_labels['dividendo' + str(i)]
                self.numDividendi = 1

                self.buttons['Aggiungi Dividendo'].setVisible(True)
                self.sel_immobile = self.input_lines['immobile'].currentText()

                self.tipi_spesa = []

                for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
                    self.tipi_spesa.extend(tabella.tipologieSpesa)

                if self.tipi_spesa:
                    self.buttons['Aggiungi Dividendo'].setDisabled(False)
                    self.input_lines['tipoSpesa0'].setPlaceholderText("Seleziona la tipologia di spesa...")

                    for tipo in self.tipi_spesa:
                        self.input_lines['tipoSpesa0'].addItem(TipoSpesa.ricercaTipoSpesaByCodice(tipo).nome, tipo)
                else:
                    self.buttons['Aggiungi Dividendo'].setDisabled(True)

                    self.input_lines['tipoSpesa0'].clear()
                    self.input_lines['tipoSpesa0'].setPlaceholderText("Nessuna tipologia di spesa per questo immobile. Aggiungile nella sezione Tabelle Millesimali")

    def fornitore_fields_dynamic(self):
        if self.input_lines['denominazione'].text():
            denominazioni_fornitori = [item.denominazione.upper() for item in Fornitore.getAllFornitore().values()]

            if self.input_lines['denominazione'].text().upper() in denominazioni_fornitori:

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

    def dividendi_fields_dynamic(self):
        self.tipi_spesa = []

        for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
            self.tipi_spesa.extend(tabella.tipologieSpesa)

        available_tipi_spesa = self.tipi_spesa

        for i in range(self.numDividendi):
            if self.input_lines[f'tipoSpesa{i}'].currentText():
                for tipo in self.tipi_spesa:
                    if self.input_lines[f'tipoSpesa{i}'].currentData() == tipo:
                        available_tipi_spesa.remove(tipo)

        for i in range(self.numDividendi):
            if self.input_lines[f'tipoSpesa{i}'].currentText():

                current_choice = [self.input_lines[f'tipoSpesa{i}'].currentText(), self.input_lines[f'tipoSpesa{i}'].currentData()]

                self.input_lines[f'tipoSpesa{i}'].clear()
                self.input_lines[f'tipoSpesa{i}'].addItem(current_choice[0], current_choice[1])
                self.input_lines[f'tipoSpesa{i}'].setCurrentText(current_choice[0])
                for tipo in available_tipi_spesa:
                    self.input_lines[f'tipoSpesa{i}'].addItem(TipoSpesa.ricercaTipoSpesaByCodice(tipo).nome, tipo)
            else:
                self.input_lines[f'tipoSpesa{i}'].clear()
                self.input_lines[f'tipoSpesa{i}'].setPlaceholderText("Seleziona la tipologia di spesa...")
                for tipo in available_tipi_spesa:
                    self.input_lines[f'tipoSpesa{i}'].addItem(TipoSpesa.ricercaTipoSpesaByCodice(tipo).nome, tipo)

        totale_dividendi = 100
        num_filled_dividendi_fields = 1

        if self.numDividendi > 1:
            totale_dividendi = 0
            num_filled_dividendi_fields = 0
            for i in range(self.numDividendi):
                if self.input_lines[f'dividendo{i}'].text():
                    num_filled_dividendi_fields += 1
                    totale_dividendi += int(self.input_lines[f'dividendo{i}'].text())

        if totale_dividendi != 100 and num_filled_dividendi_fields == self.numDividendi:
            self.input_errors['dividendo0'].setText('La somma dei dividendi deve essero 100')
            self.input_errors['tipoSpesa0'].setText('')
            self.input_errors['dividendo0'].setVisible(True)
            self.input_errors['tipoSpesa0'].setVisible(True)
            self.buttons['Aggiungi Spesa'].setDisabled(True)
        else:
            self.input_errors['dividendo0'].setVisible(False)
            self.input_errors['tipoSpesa0'].setVisible(False)
            self.buttons['Aggiungi Spesa'].setDisabled(False)

    def input_validation(self):
        num_writed_lines = 0

        print("richiesto:", self.required_fields)
        combo_box_fields = ['immobile', 'tipoProfessione']
        combo_box_fields.extend([item for item in self.input_lines.keys() if 'tipoSpesa' in item])
        print(combo_box_fields)

        for field in self.required_fields:
            if field in combo_box_fields:
                if self.input_lines[field].currentText():
                    num_writed_lines += 1
            else:
                if self.input_lines[field].text():
                    num_writed_lines += 1

        if num_writed_lines < len(self.required_fields):
            self.buttons["Aggiungi Spesa"].setDisabled(True)
        else:
            self.buttons["Aggiungi Spesa"].setDisabled(False)
