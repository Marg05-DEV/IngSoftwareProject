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
        for f in Fornitore.getAllFornitore().values():
            print(f.getInfoFornitore())
        self.spesa = spesa
        self.cambio_fornitore = False
        self.callback = callback
        self.sel_immobile = Immobile.ricercaImmobileById(self.spesa.immobile).denominazione
        self.input_lines = {}
        self.input_labels = {}
        self.input_errors = {}
        self.buttons = {}
        self.checkboxes = {}
        self.required_fields = []
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

        self.error_denominazione = QLabel("")
        self.error_denominazione.setStyleSheet("font-weight: bold;")
        self.input_errors["error"] = self.error_denominazione
        main_layout.addWidget(self.create_button("Cambia fornitore", self.changeFornitore))
        main_layout.addWidget(self.error_denominazione)
        self.input_errors["error"].setVisible(False)

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
        main_layout.addWidget(self.create_checkbox("L'importo si riferisce ad una ritenuta di una spesa", 'isRitenuta'))
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
        if self.spesa.getInfoSpesa()[index]:
            checkbox.setChecked(True)
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
            input_line.setCurrentText(Immobile.ricercaImmobileById(self.spesa.immobile).denominazione)
            input_line.activated.connect(self.input_validation)
        elif index == "tipoSpesa":
            input_line = QComboBox()
            tipo_spesa = []
            tabella_millesimale = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(self.spesa.immobile)).values())
            for tabelle in tabella_millesimale:
                for tipo in tabelle.tipologiaSpesa:
                    tipo_spesa.append(TipoSpesa.ricercaTipoSpesaByCodice(tipo))
            input_line.addItems([item.nome for item in tipo_spesa])
            tipo = TipoSpesa.ricercaTipoSpesaByCodice(self.spesa.tipoSpesa).nome
            input_line.setCurrentText(tipo)
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
            """
            fornitori_list = [item.denominazione for item in Fornitore.getAllFornitore().values()]
            completer = QCompleter(fornitori_list)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            input_line.setCompleter(completer)
            """
            input_line.textChanged.connect(self.input_validation)
        elif index == "cittaSede":
            input_line = QLineEdit()
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            input_line.setPlaceholderText(str(fornitore.cittaSede))
            input_line.textChanged.connect(self.input_validation)
        elif index == "indirizzoSede":
            input_line = QLineEdit()
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            input_line.setPlaceholderText(str(fornitore.indirizzoSede))
            input_line.textChanged.connect(self.input_validation)
        elif index == "partitaIva":
            input_line = QLineEdit()
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            input_line.setPlaceholderText(str(fornitore.partitaIva))
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
    def changeFornitore(self):
        self.input_errors["error"].setVisible(False)
        fornitori_list = [item.denominazione for item in Fornitore.getAllFornitore().values()]
        completer = QCompleter(fornitori_list)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.input_lines["denominazione"].setCompleter(completer)
        self.input_lines["denominazione"].textChanged.connect(self.input_validation)

        for attributo in ['denominazione', 'cittaSede', 'indirizzoSede', 'partitaIva']:
            self.input_lines[attributo].setText("")
            self.input_lines[attributo].setPlaceholderText("")
            self.required_fields.append(attributo)

        self.input_lines['tipoProfessione'].clear()
        self.input_lines['tipoProfessione'].setPlaceholderText("Scegli il tipo di professione...")
        self.input_lines['tipoProfessione'].addItems(['Ditta', 'Professionista', 'AC'])
        self.required_fields.append('tipoProfessione')
        self.cambio_fornitore = True
        self.buttons["Cambia fornitore"].setDisabled(True)
        self.buttons["Modifica Spesa"].setDisabled(True)

    def reset(self):
        for key in self.input_lines.keys():
            self.input_lines[key].clear()

        self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
        self.input_lines['immobile'].setCurrentText(Immobile.ricercaImmobileById(self.spesa.immobile).denominazione)

        self.sel_immobile = self.input_lines['immobile'].currentText()

        tipi_spesa = []
        for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
            tipi_spesa.extend(tabella.tipologiaSpesa)
        for tipo in tipi_spesa:
            self.input_lines['tipoSpesa'].addItem(TipoSpesa.ricercaTipoSpesaByCodice(tipo).nome, tipo)

        self.input_lines['tipoSpesa'].setCurrentText(TipoSpesa.ricercaTipoSpesaByCodice(self.spesa.tipoSpesa).nome)

        self.input_lines['tipoSpesa'].setVisible(True)
        self.input_labels['tipoSpesa'].setVisible(True)

        fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
        self.input_lines['tipoProfessione'].addItems(['Ditta', 'Professionista', 'AC'])
        self.input_lines['tipoProfessione'].setCurrentText(fornitore.tipoProfessione)
        self.input_lines["denominazione"].setPlaceholderText(fornitore.denominazione)
        self.input_lines["cittaSede"].setPlaceholderText(fornitore.cittaSede)
        self.input_lines["indirizzoSede"].setPlaceholderText(fornitore.indirizzoSede)
        self.input_lines["partitaIva"].setPlaceholderText(fornitore.partitaIva)
        self.cambio_fornitore = False
        self.buttons["Cambia fornitore"].setDisabled(False)
        self.buttons["Modifica Spesa"].setDisabled(False)

        if self.spesa.pagata:
            self.checkboxes['pagata'].setCheckState(Qt.CheckState.Checked)
        else:
            self.checkboxes['pagata'].setCheckState(Qt.CheckState.Unchecked)

        if self.spesa.isRitenuta:
            self.checkboxes['isRitenuta'].setCheckState(Qt.CheckState.Checked)
        else:
            self.checkboxes['isRitenuta'].setCheckState(Qt.CheckState.Unchecked)

        self.input_lines['dataPagamento'].setDate(self.spesa.dataPagamento)
        self.input_lines['dataFattura'].setDate(self.spesa.dataFattura)
        self.input_lines["denominazione"].setCompleter(None)

        self.input_errors["error"].setVisible(False)

    def updateSpesa(self):
        temp_spesa = {}
        temp_fornitore = {}
        fornitore_esistente = False
        codice_fornitore = 0
        msg1 = ""
        codice = 0

        if self.cambio_fornitore:
            for fornitore in Fornitore.getAllFornitore().values():
                print(self.input_lines["denominazione"].text() == fornitore.denominazione)
                if self.input_lines["denominazione"].text() == fornitore.denominazione:
                    fornitore_esistente = True
                    codice_fornitore = fornitore.codice
                    fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
                    for attributo in fornitore.getInfoFornitore().keys():
                        print("attributo: ", attributo)
                        if attributo == "tipoProfessione":
                            temp_fornitore[attributo] = self.input_lines[attributo].currentText()
                        elif attributo == "codice" or self.input_lines[attributo].text() == "":
                            temp_fornitore[attributo] = fornitore.getInfoFornitore()[attributo]
                        else:
                            temp_fornitore[attributo] = self.input_lines[attributo].text()

                    """msg1 = fornitore.modificaFornitore(temp_fornitore["cittaSede"], temp_fornitore["denominazione"],
                                                       temp_fornitore["indirizzoSede"],
                                                       temp_fornitore["partitaIva"], temp_fornitore["tipoProfessione"])"""
            if not fornitore_esistente:
                print("sto per aggiungere il fornitore")
                denominazione = self.input_lines["denominazione"].text()
                cittaSede = self.input_lines["cittaSede"].text()
                indirizzoSede = self.input_lines["indirizzoSede"].text()
                partitaIva = self.input_lines["partitaIva"].text()
                tipoProfessione = self.input_lines["tipoProfessione"].currentText()

                temp_fornitore = Fornitore()
                msg, fornitore = temp_fornitore.aggiungiFornitore(cittaSede, denominazione, indirizzoSede, partitaIva, tipoProfessione)
                for f in Fornitore.getAllFornitore().values():
                    print(f.getInfoFornitore())
                print(fornitore.codice)
                codice_fornitore = fornitore.codice

        elif not self.cambio_fornitore:
            self.input_lines["denominazione"].setCompleter(None)
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            for attributo in fornitore.getInfoFornitore().keys():
                print("attributo: ", attributo)
                if attributo == "tipoProfessione":
                    print("if 1: ", attributo)
                    temp_fornitore[attributo] = self.input_lines[attributo].currentText()
                elif attributo == "codice" or self.input_lines[attributo].text() == "":
                    print("elif 1: ", attributo)
                    temp_fornitore[attributo] = fornitore.getInfoFornitore()[attributo]
                else:
                    print("else 1: ", attributo, ": ", self.input_lines[attributo].text())
                    temp_fornitore[attributo] = self.input_lines[attributo].text()

            print("modifica del fornitore", temp_fornitore["cittaSede"], temp_fornitore["denominazione"],
                                               temp_fornitore["indirizzoSede"],
                                               temp_fornitore["partitaIva"], temp_fornitore["tipoProfessione"])

            msg1 = fornitore.modificaFornitore(temp_fornitore["cittaSede"], temp_fornitore["denominazione"],
                                               temp_fornitore["indirizzoSede"],
                                               temp_fornitore["partitaIva"], temp_fornitore["tipoProfessione"])

            codice_fornitore = fornitore.getInfoFornitore()["codice"]
            print("Codice del fornitore modificato: ", codice_fornitore)
            print("fornitore dopo la modifica: ", fornitore.getInfoFornitore())

        for attributo in self.spesa.getInfoSpesa().keys():
            if attributo == "immobile" or attributo == "tipoSpesa":
                if attributo == "immobile":
                    codice = Immobile.ricercaImmobileByDenominazione(self.input_lines[attributo].currentText()).id
                else:
                    codice = TipoSpesa.ricercaTipoSpesaByNome(self.input_lines[attributo].currentText()).codice
                temp_spesa[attributo] = codice
            elif attributo == "fornitore":
                print("nell'elif della spesa: ", Fornitore.ricercaFornitoreByCodice(codice_fornitore).getInfoFornitore())
                temp_spesa[attributo] = codice_fornitore
            elif attributo in ["pagata", "isRitenuta"]:
                if self.checkboxes[attributo].isChecked():
                    temp_spesa[attributo] = True
                else:
                    temp_spesa[attributo] = False
            elif attributo in ["codice", "dataRegistrazione"] or self.input_lines[attributo].text() == "":
                temp_spesa[attributo] = self.spesa.getInfoSpesa()[attributo]
            else:
                print(self.input_lines[attributo].text())
                temp_spesa[attributo] = self.input_lines[attributo].text()

        print("dopo la presa dei valori delle spese")
        dataPagamento = temp_spesa["dataPagamento"].split('/')
        dataPagamento = datetime.date(int(dataPagamento[2]), int(dataPagamento[1]), int(dataPagamento[0]))
        print(dataPagamento)
        dataFattura = temp_spesa["dataFattura"].split('/')
        dataFattura = datetime.date(int(dataFattura[2]), int(dataFattura[1]), int(dataFattura[0]))
        print(dataFattura)
        dataRegistrazione = temp_spesa["dataRegistrazione"]
        print(dataRegistrazione)

        print(temp_spesa["descrizione"], temp_spesa["fornitore"], temp_spesa["importo"],
                                       temp_spesa["tipoSpesa"], temp_spesa["immobile"], temp_spesa["pagata"],
                                       dataPagamento, dataFattura, dataRegistrazione,
                                       temp_spesa["isRitenuta"], int(temp_spesa["numeroFattura"]))

        msg = self.spesa.modificaSpesa(temp_spesa["descrizione"], temp_spesa["fornitore"], temp_spesa["importo"],
                                       temp_spesa["tipoSpesa"], temp_spesa["immobile"], temp_spesa["pagata"],
                                       dataPagamento, dataFattura, dataRegistrazione,
                                       temp_spesa["isRitenuta"], int(temp_spesa["numeroFattura"]))

        self.callback(msg)
        self.close()

    def input_validation(self):

        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            print("immobile modificato")
            if self.input_lines['immobile'].currentText():
                self.required_fields.append('tipoSpesa')
                self.input_lines['tipoSpesa'].clear()
                self.input_lines['tipoSpesa'].setVisible(True)
                self.input_labels['tipoSpesa'].setVisible(True)
                self.sel_immobile = self.input_lines['immobile'].currentText()
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

        if self.input_lines['denominazione'].text():
            self.input_errors["error"].setVisible(False)
            print("nell'if principale")
            denominazioni_fornitori = [item.denominazione.upper() for item in Fornitore.getAllFornitore().values()]

            if self.input_lines['denominazione'].text().upper() in denominazioni_fornitori and not self.cambio_fornitore:
                print("entro nella validazione del secondo elif")
                self.input_errors["error"].setText("La denominazione è già esistente, clicca su cambia fornitore!")
                self.input_errors["error"].setVisible(True)

            elif self.input_lines['denominazione'].text().upper() in denominazioni_fornitori:
                print("entro nella validazione del primo if")
                fornitore = Fornitore.ricercaFornitoreByDenominazione(self.input_lines['denominazione'].text())
                self.input_lines['cittaSede'].setPlaceholderText(fornitore.cittaSede)
                self.input_lines['indirizzoSede'].setPlaceholderText(fornitore.indirizzoSede)
                self.input_lines['partitaIva'].setPlaceholderText(fornitore.partitaIva)
                self.input_lines['tipoProfessione'].setCurrentText(fornitore.tipoProfessione)
                self.isFornitoreTrovatoNow = True

            elif (not (self.input_lines['denominazione'].text().upper() in denominazioni_fornitori)) and self.isFornitoreTrovatoNow:
                print("entro nella validazione del primo elif")
                self.input_lines['cittaSede'].setText("")
                self.input_lines['indirizzoSede'].setText("")
                self.input_lines['partitaIva'].setText("")
                self.input_lines['tipoProfessione'].setCurrentText("")
                self.isFornitoreTrovatoNow = False


        num_writed_lines = 0

        for field in self.required_fields:
            if field in ['tipoSpesa', 'tipoProfessione']:
                if self.input_lines[field].currentText():
                    num_writed_lines += 1
            else:
                if self.input_lines[field].text():
                    num_writed_lines += 1
        print("valore del fornitore trivato: ", self.isFornitoreTrovatoNow)
        if self.isFornitoreTrovatoNow:
            for i in range(0, 4):
                num_writed_lines += 1

        print("il campo dell'errore è visibile: ", self.input_errors["error"].isVisible())
        if num_writed_lines < len(self.required_fields) or self.input_errors["error"].isVisible():
            self.buttons["Modifica Spesa"].setDisabled(True)
        else:
            self.buttons["Modifica Spesa"].setDisabled(False)
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
        for f in Fornitore.getAllFornitore().values():
            print(f.getInfoFornitore())
        self.spesa = spesa
        self.cambio_fornitore = False
        self.callback = callback
        self.sel_immobile = Immobile.ricercaImmobileById(self.spesa.immobile).denominazione
        self.input_lines = {}
        self.input_labels = {}
        self.input_errors = {}
        self.buttons = {}
        self.checkboxes = {}
        self.required_fields = []
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

        self.error_denominazione = QLabel("")
        self.error_denominazione.setStyleSheet("font-weight: bold;")
        self.input_errors["error"] = self.error_denominazione
        main_layout.addWidget(self.create_button("Cambia fornitore", self.changeFornitore))
        main_layout.addWidget(self.error_denominazione)
        self.input_errors["error"].setVisible(False)

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
        main_layout.addWidget(self.create_checkbox("L'importo si riferisce ad una ritenuta di una spesa", 'isRitenuta'))
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
        if self.spesa.getInfoSpesa()[index]:
            checkbox.setChecked(True)
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
            input_line.setCurrentText(Immobile.ricercaImmobileById(self.spesa.immobile).denominazione)
            input_line.activated.connect(self.input_validation)
        elif index == "tipoSpesa":
            input_line = QComboBox()
            tipo_spesa = []
            tabella_millesimale = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileById(self.spesa.immobile)).values())
            for tabelle in tabella_millesimale:
                for tipo in tabelle.tipologiaSpesa:
                    tipo_spesa.append(TipoSpesa.ricercaTipoSpesaByCodice(tipo))
            input_line.addItems([item.nome for item in tipo_spesa])
            tipo = TipoSpesa.ricercaTipoSpesaByCodice(self.spesa.tipoSpesa).nome
            input_line.setCurrentText(tipo)
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
            """
            fornitori_list = [item.denominazione for item in Fornitore.getAllFornitore().values()]
            completer = QCompleter(fornitori_list)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            input_line.setCompleter(completer)
            """
            input_line.textChanged.connect(self.input_validation)
        elif index == "cittaSede":
            input_line = QLineEdit()
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            input_line.setPlaceholderText(str(fornitore.cittaSede))
            input_line.textChanged.connect(self.input_validation)
        elif index == "indirizzoSede":
            input_line = QLineEdit()
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            input_line.setPlaceholderText(str(fornitore.indirizzoSede))
            input_line.textChanged.connect(self.input_validation)
        elif index == "partitaIva":
            input_line = QLineEdit()
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            input_line.setPlaceholderText(str(fornitore.partitaIva))
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
    def changeFornitore(self):
        self.input_errors["error"].setVisible(False)
        fornitori_list = [item.denominazione for item in Fornitore.getAllFornitore().values()]
        completer = QCompleter(fornitori_list)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.input_lines["denominazione"].setCompleter(completer)
        self.input_lines["denominazione"].textChanged.connect(self.input_validation)

        for attributo in ['denominazione', 'cittaSede', 'indirizzoSede', 'partitaIva']:
            self.input_lines[attributo].setText("")
            self.input_lines[attributo].setPlaceholderText("")
            self.required_fields.append(attributo)

        self.input_lines['tipoProfessione'].clear()
        self.input_lines['tipoProfessione'].setPlaceholderText("Scegli il tipo di professione...")
        self.input_lines['tipoProfessione'].addItems(['Ditta', 'Professionista', 'AC'])
        self.required_fields.append('tipoProfessione')
        self.cambio_fornitore = True
        self.buttons["Cambia fornitore"].setDisabled(True)
        self.buttons["Modifica Spesa"].setDisabled(True)

    def reset(self):
        for key in self.input_lines.keys():
            self.input_lines[key].clear()

        self.input_lines['immobile'].addItems([item.denominazione for item in Immobile.getAllImmobili().values()])
        self.input_lines['immobile'].setCurrentText(Immobile.ricercaImmobileById(self.spesa.immobile).denominazione)

        self.sel_immobile = self.input_lines['immobile'].currentText()

        tipi_spesa = []
        for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(Immobile.ricercaImmobileByDenominazione(self.sel_immobile)).values():
            tipi_spesa.extend(tabella.tipologiaSpesa)
        for tipo in tipi_spesa:
            self.input_lines['tipoSpesa'].addItem(TipoSpesa.ricercaTipoSpesaByCodice(tipo).nome, tipo)

        self.input_lines['tipoSpesa'].setCurrentText(TipoSpesa.ricercaTipoSpesaByCodice(self.spesa.tipoSpesa).nome)

        self.input_lines['tipoSpesa'].setVisible(True)
        self.input_labels['tipoSpesa'].setVisible(True)

        fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
        self.input_lines['tipoProfessione'].addItems(['Ditta', 'Professionista', 'AC'])
        self.input_lines['tipoProfessione'].setCurrentText(fornitore.tipoProfessione)
        self.input_lines["denominazione"].setPlaceholderText(fornitore.denominazione)
        self.input_lines["cittaSede"].setPlaceholderText(fornitore.cittaSede)
        self.input_lines["indirizzoSede"].setPlaceholderText(fornitore.indirizzoSede)
        self.input_lines["partitaIva"].setPlaceholderText(fornitore.partitaIva)
        self.cambio_fornitore = False
        self.buttons["Cambia fornitore"].setDisabled(False)
        self.buttons["Modifica Spesa"].setDisabled(False)

        if self.spesa.pagata:
            self.checkboxes['pagata'].setCheckState(Qt.CheckState.Checked)
        else:
            self.checkboxes['pagata'].setCheckState(Qt.CheckState.Unchecked)

        if self.spesa.isRitenuta:
            self.checkboxes['isRitenuta'].setCheckState(Qt.CheckState.Checked)
        else:
            self.checkboxes['isRitenuta'].setCheckState(Qt.CheckState.Unchecked)

        self.input_lines['dataPagamento'].setDate(self.spesa.dataPagamento)
        self.input_lines['dataFattura'].setDate(self.spesa.dataFattura)
        self.input_lines["denominazione"].setCompleter(None)

        self.input_errors["error"].setVisible(False)

    def updateSpesa(self):
        temp_spesa = {}
        temp_fornitore = {}
        fornitore_esistente = False
        codice_fornitore = 0
        msg1 = ""
        codice = 0

        if self.cambio_fornitore:
            for fornitore in Fornitore.getAllFornitore().values():
                if self.input_lines["denominazione"].text() == fornitore.denominazione:
                    fornitore_esistente = True
                    codice_fornitore = fornitore.codice
                    for attributo in fornitore.getInfoFornitore().keys():
                        print("attributo: ", attributo)
                        if attributo == "tipoProfessione":
                            temp_fornitore[attributo] = self.input_lines[attributo].currentText()
                        elif attributo == "codice" or self.input_lines[attributo].text() == "":
                            temp_fornitore[attributo] = fornitore.getInfoFornitore()[attributo]
                        else:
                            temp_fornitore[attributo] = self.input_lines[attributo].text()

                    msg1 = fornitore.modificaFornitore(temp_fornitore["cittaSede"], temp_fornitore["denominazione"],
                                                       temp_fornitore["indirizzoSede"],
                                                       temp_fornitore["partitaIva"], temp_fornitore["tipoProfessione"])
            if not fornitore_esistente:
                print("sto per aggiungere il fornitore")
                denominazione = self.input_lines["denominazione"].text()
                cittaSede = self.input_lines["cittaSede"].text()
                indirizzoSede = self.input_lines["indirizzoSede"].text()
                partitaIva = self.input_lines["partitaIva"].text()
                tipoProfessione = self.input_lines["tipoProfessione"].currentText()

                temp_fornitore = Fornitore()
                msg, fornitore = temp_fornitore.aggiungiFornitore(cittaSede, denominazione, indirizzoSede, partitaIva, tipoProfessione)
                for f in Fornitore.getAllFornitore().values():
                    print(f.getInfoFornitore())
                print(fornitore.codice)
                codice_fornitore = fornitore.codice

        elif not self.cambio_fornitore:
            self.input_lines["denominazione"].setCompleter(None)
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            for attributo in fornitore.getInfoFornitore().keys():
                print("attributo: ", attributo)
                if attributo == "tipoProfessione":
                    print("if 1: ", attributo)
                    temp_fornitore[attributo] = self.input_lines[attributo].currentText()
                elif attributo == "codice" or self.input_lines[attributo].text() == "":
                    print("elif 1: ", attributo)
                    temp_fornitore[attributo] = fornitore.getInfoFornitore()[attributo]
                else:
                    print("else 1: ", attributo, ": ", self.input_lines[attributo].text())
                    temp_fornitore[attributo] = self.input_lines[attributo].text()

            print("modifica del fornitore", temp_fornitore["cittaSede"], temp_fornitore["denominazione"],
                                               temp_fornitore["indirizzoSede"],
                                               temp_fornitore["partitaIva"], temp_fornitore["tipoProfessione"])

            msg1 = fornitore.modificaFornitore(temp_fornitore["cittaSede"], temp_fornitore["denominazione"],
                                               temp_fornitore["indirizzoSede"],
                                               temp_fornitore["partitaIva"], temp_fornitore["tipoProfessione"])

            codice_fornitore = fornitore.getInfoFornitore()["codice"]
            print("Codice del fornitore modificato: ", codice_fornitore)
            print("fornitore dopo la modifica: ", fornitore.getInfoFornitore())

        for attributo in self.spesa.getInfoSpesa().keys():
            if attributo == "immobile" or attributo == "tipoSpesa":
                if attributo == "immobile":
                    codice = Immobile.ricercaImmobileByDenominazione(self.input_lines[attributo].currentText()).id
                else:
                    codice = TipoSpesa.ricercaTipoSpesaByNome(self.input_lines[attributo].currentText()).codice
                temp_spesa[attributo] = codice
            elif attributo == "fornitore":
                print("nell'elif della spesa: ", Fornitore.ricercaFornitoreByCodice(codice_fornitore).getInfoFornitore())
                temp_spesa[attributo] = codice_fornitore
            elif attributo in ["pagata", "isRitenuta"]:
                if self.checkboxes[attributo].isChecked():
                    temp_spesa[attributo] = True
                else:
                    temp_spesa[attributo] = False
            elif attributo in ["codice", "dataRegistrazione"] or self.input_lines[attributo].text() == "":
                temp_spesa[attributo] = self.spesa.getInfoSpesa()[attributo]
            else:
                print(self.input_lines[attributo].text())
                temp_spesa[attributo] = self.input_lines[attributo].text()

        print("dopo la presa dei valori delle spese")
        dataPagamento = temp_spesa["dataPagamento"].split('/')
        dataPagamento = datetime.date(int(dataPagamento[2]), int(dataPagamento[1]), int(dataPagamento[0]))
        print(dataPagamento)
        dataFattura = temp_spesa["dataFattura"].split('/')
        dataFattura = datetime.date(int(dataFattura[2]), int(dataFattura[1]), int(dataFattura[0]))
        print(dataFattura)
        dataRegistrazione = temp_spesa["dataRegistrazione"]
        print(dataRegistrazione)

        print(temp_spesa["descrizione"], temp_spesa["fornitore"], temp_spesa["importo"],
                                       temp_spesa["tipoSpesa"], temp_spesa["immobile"], temp_spesa["pagata"],
                                       dataPagamento, dataFattura, dataRegistrazione,
                                       temp_spesa["isRitenuta"], int(temp_spesa["numeroFattura"]))

        msg = self.spesa.modificaSpesa(temp_spesa["descrizione"], temp_spesa["fornitore"], temp_spesa["importo"],
                                       temp_spesa["tipoSpesa"], temp_spesa["immobile"], temp_spesa["pagata"],
                                       dataPagamento, dataFattura, dataRegistrazione,
                                       temp_spesa["isRitenuta"], int(temp_spesa["numeroFattura"]))

        self.callback(msg)
        self.close()

    def input_validation(self):

        if self.input_lines['immobile'].currentText() != self.sel_immobile:
            print("immobile modificato")
            if self.input_lines['immobile'].currentText():
                self.required_fields.append('tipoSpesa')
                self.input_lines['tipoSpesa'].clear()
                self.input_lines['tipoSpesa'].setVisible(True)
                self.input_labels['tipoSpesa'].setVisible(True)
                self.sel_immobile = self.input_lines['immobile'].currentText()
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

        if self.input_lines['denominazione'].text():
            self.input_errors["error"].setVisible(False)
            print("nell'if principale")
            denominazioni_fornitori = [item.denominazione.upper() for item in Fornitore.getAllFornitore().values()]

            if self.input_lines['denominazione'].text().upper() in denominazioni_fornitori and not self.cambio_fornitore and not self.isFornitoreTrovatoNow:
                print("entro nella validazione del secondo elif")
                self.input_errors["error"].setText("La denominazione è già esistente, clicca su cambia fornitore!")
                self.input_errors["error"].setVisible(True)

            elif self.input_lines['denominazione'].text().upper() in denominazioni_fornitori:
                print("entro nella validazione del primo if")
                fornitore = Fornitore.ricercaFornitoreByDenominazione(self.input_lines['denominazione'].text())
                self.input_lines['cittaSede'].setPlaceholderText(fornitore.cittaSede)
                self.input_lines['indirizzoSede'].setPlaceholderText(fornitore.indirizzoSede)
                self.input_lines['partitaIva'].setPlaceholderText(fornitore.partitaIva)
                self.input_lines['tipoProfessione'].setCurrentText(fornitore.tipoProfessione)
                self.isFornitoreTrovatoNow = True

            elif (not (self.input_lines['denominazione'].text().upper() in denominazioni_fornitori)) and self.isFornitoreTrovatoNow:
                print("entro nella validazione del primo elif")
                self.input_lines['cittaSede'].setText("")
                self.input_lines['indirizzoSede'].setText("")
                self.input_lines['partitaIva'].setText("")
                self.input_lines['tipoProfessione'].setCurrentText("")
                self.isFornitoreTrovatoNow = False

            elif self.isFornitoreTrovatoNow:
                print("sem trvat u fornitor mo lu può modifica")
                self.cambio_fornitore = False


        num_writed_lines = 0

        for field in self.required_fields:
            if field in ['tipoSpesa', 'tipoProfessione']:
                if self.input_lines[field].currentText():
                    num_writed_lines += 1
            else:
                if self.input_lines[field].text():
                    num_writed_lines += 1
        print("valore del fornitore trivato: ", self.isFornitoreTrovatoNow)
        if self.isFornitoreTrovatoNow:
            for i in range(0, 4):
                num_writed_lines += 1

        print("il campo dell'errore è visibile: ", self.input_errors["error"].isVisible())
        if num_writed_lines < len(self.required_fields) or self.input_errors["error"].isVisible():
            self.buttons["Modifica Spesa"].setDisabled(True)
        else:
            self.buttons["Modifica Spesa"].setDisabled(False)

