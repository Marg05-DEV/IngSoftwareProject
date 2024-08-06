import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIntValidator, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy, QDateEdit, QComboBox, QListView, QCompleter, QListWidget, QListWidgetItem, QFrame
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaCreateTipoSpesa import VistaCreateTipoSpesa


class VistaCreateTabellaMillesimale(QWidget):
    def __init__(self, immobile, callback):
        super(VistaCreateTabellaMillesimale, self).__init__()
        self.immobile = immobile
        self.callback = callback
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}
        self.used_tabella_suggerita = False
        main_layout = QVBoxLayout()

        self.tipi_spesa = []

        lbl_frase = QLabel("Inserisci i dati della nuova tabella millesimale:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())
        main_layout.addWidget(lbl_frase)
        existing_tabella_millesimale_layout = QHBoxLayout()
        existing_tabella_millesimale_data_layout = QVBoxLayout()
        self.lbl_exist = QLabel("La tabella millesimale esistente è: ")
        self.lbl_tabella_millesimale_esistente = QLabel()
        self.lbl_tabella_millesimale_esistente.setStyleSheet("font-weight: bold;")

        self.button_exist = self.create_button("Assegna Tabella millesimale", self.add_tabella_millesimale_esistente)
        self.button_exist.setVisible(False)
        self.lbl_exist.setVisible(False)
        self.lbl_tabella_millesimale_esistente.setVisible(False)
        existing_tabella_millesimale_data_layout.addWidget(self.lbl_exist, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        existing_tabella_millesimale_data_layout.addWidget(self.lbl_tabella_millesimale_esistente, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        existing_tabella_millesimale_layout.addLayout(existing_tabella_millesimale_data_layout)
        existing_tabella_millesimale_layout.addWidget(self.button_exist)
        main_layout.addLayout(existing_tabella_millesimale_layout)
        fields_layout = QVBoxLayout()
        fields_layout.addLayout(self.pairLabelInput("Nome", "nome"))
        fields_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))

        assign_tipo_layout = QHBoxLayout()
        tipi_spesa_utilizzati = []

        for tabella in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values():
            tipi_spesa_utilizzati.extend(tabella.tipologieSpesa)
        tipi_spesa_list = [item for item in TipoSpesa.getAllTipoSpesa().values() if item.codice not in tipi_spesa_utilizzati]

        self.searchbar = QComboBox()
        lbl_frase1 = QLabel("Aggiungi un tipo di spesa esistente che non sia assegnato ad altre tabelle millesimali dello stesso immobile:")

        assign_tipo_layout.addWidget(self.searchbar)
        assign_tipo_layout.addWidget(self.create_button("Aggiungi Tipo di spesa", self.seleziona_tipo_spesa))

        if tipi_spesa_list:
            self.searchbar.setPlaceholderText("Ricerca un tipo di spesa ...")
            self.buttons["Aggiungi Tipo di spesa"].setDisabled(False)
        else:
            self.searchbar.setPlaceholderText("Nessun tipo di spesa disponibile")
            self.buttons["Aggiungi Tipo di spesa"].setDisabled(True)

        for tipo_spesa in tipi_spesa_list:
            self.searchbar.addItem(tipo_spesa.nome, tipo_spesa.codice)
        print("ciao nuova finestravwrijern")
        nuovo_tipo_layout = QHBoxLayout()
        lbl_frase2 = QLabel("Crea un nuovo tipo di spesa e assegnalo alla tabella millesimale corrente:")

        nuovo_tipo_layout.addWidget(lbl_frase2)
        nuovo_tipo_layout.addWidget(self.create_button("Nuovo Tipo di spesa", self.nuovo_tipo_spesa))
        print("ciao nuova finestravwrijern")
        self.list_view_tipi_spesa = QListWidget()
        self.list_view_tipi_spesa.setAlternatingRowColors(True)

        self.msg = QLabel("Non ci sono condomini assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addLayout(fields_layout)
        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(lbl_frase1)
        main_layout.addLayout(assign_tipo_layout)

        oppure_layout = QHBoxLayout()
        oppure_layout.addWidget(self.drawLine())
        oppure_label = QLabel("oppure")
        oppure_layout.addWidget(oppure_label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        oppure_layout.addWidget(self.drawLine())
        main_layout.addLayout(oppure_layout)

        main_layout.addLayout(nuovo_tipo_layout)
        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(self.list_view_tipi_spesa)

        main_layout.addWidget(self.msg)
        main_layout.addWidget(self.create_button("Aggiungi Tabella Millesimale", self.aggiungiTabellaMillesimale))

        self.update_list()

        self.buttons["Aggiungi Tabella Millesimale"].setDisabled(True)
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuova Tabella Millesimale")

    def drawLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

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
        input_line = QLineEdit()

        if index == 'nome':
            input_line.textChanged.connect(self.nome_field_dynamic)

        input_line.textChanged.connect(self.input_validation)

        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)
        return input_layout

    def update_list(self):
        print("update tipi spesa lista 1")
        if not self.tipi_spesa:
            self.msg.setText("Non ci sono tipi di spesa assegnati alla tabella millesimale")
            self.buttons["Aggiungi Tabella Millesimale"].setDisabled(True)
            self.msg.show()
        else:
            self.msg.hide()
        print("update tipi spesa lista 2", self.tipi_spesa)
        self.list_view_tipi_spesa.clear()
        for cod_tipo_spesa in self.tipi_spesa:
            tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(cod_tipo_spesa)
            item = QListWidgetItem(f"{tipo_spesa.nome} - {tipo_spesa.descrizione}")
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            print("update tipi spesa lista 5")
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            self.list_view_tipi_spesa.addItem(item)
        print("update tipi spesa lista 3")

    def aggiungiTabellaMillesimale(self):
        nome = self.input_lines["nome"].text()
        descrizione = self.input_lines["descrizione"].text()
        tipologieSpesa = self.tipi_spesa
        immobile = self.immobile.id

        temp_tabellaMillesimale = TabellaMillesimale()
        msg, tm = temp_tabellaMillesimale.aggiungiTabellaMillesimale(nome, tipologieSpesa, descrizione, immobile)

        print(msg, tm)
        self.callback(msg)
        self.close()

    def seleziona_tipo_spesa(self):
        print("selezionato un tipo di spesa", self.searchbar.currentText())
        if self.searchbar.currentText():
            self.tipi_spesa.append(self.searchbar.currentData())
            print("i", self.searchbar.currentData())
            self.searchbar.removeItem(self.searchbar.currentIndex())
            self.searchbar.setCurrentIndex(-1)

        print("i", self.searchbar.currentData())

        self.update_list()
        self.input_validation()

    def nuovo_tipo_spesa(self):
        self.nuovo_tipo_spesa = VistaCreateTipoSpesa(None, self.callback, self.append_nuovo_tipo_spesa)
        self.nuovo_tipo_spesa.show()

    def append_nuovo_tipo_spesa(self, tipo_spesa):
        if tipo_spesa:
            self.tipi_spesa.append(tipo_spesa.codice)

        self.update_list()
        self.input_validation()

    def add_tabella_millesimale_esistente(self):
        used_tabella_millesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(self.codice_used_tabella)
        self.input_lines['nome'].setText(used_tabella_millesimale.nome)
        self.input_lines['descrizione'].setText(used_tabella_millesimale.descrizione)

        self.used_tabella_suggerita = True
        self.nome_field_dynamic()
        self.input_validation()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()

        self.tipi_spesa = []
        self.update_list()

    def nome_field_dynamic(self):
        all_tabelle_millesimali = list(TabellaMillesimale.getAllTabelleMillesimali().values())
        tabelle_millesimali_immobile = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values())

        existing_tabella = False
        same_immobile = False
        existing_tabella_not_same_immobile = False

        for tabella in all_tabelle_millesimali:
            if self.input_lines['nome'].text().upper() == tabella.nome.upper():
                existing_tabella = True
                if tabelle_millesimali_immobile:
                    for tabella_immobile in tabelle_millesimali_immobile:
                        if self.input_lines['nome'].text().upper() == tabella_immobile.nome.upper():
                            same_immobile = True

            if not same_immobile and existing_tabella:
                self.codice_used_tabella = tabella.codice
                existing_tabella_not_same_immobile = True
                self.lbl_tabella_millesimale_esistente.setText(f"{tabella.nome} - {tabella.descrizione}")
                self.button_exist.setDisabled(True)
                break

        if existing_tabella_not_same_immobile and not self.used_tabella_suggerita:
            self.input_errors['nome'].setText("Nome della tabella millesimale già usato in altri immobili")
            self.input_errors['nome'].setVisible(True)
            self.lbl_exist.setVisible(True)
            self.lbl_tabella_millesimale_esistente.setVisible(True)
            self.button_exist.setVisible(True)
            self.button_exist.setDisabled(False)
        else:
            if not existing_tabella:
                self.used_tabella_suggerita = False
            self.input_errors['nome'].setVisible(False)
            self.lbl_exist.setVisible(False)
            self.lbl_tabella_millesimale_esistente.setVisible(False)
            self.button_exist.setVisible(False)
            self.button_exist.setDisabled(True)

    def input_validation(self):
        tabelle_millesimali_immobile = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values())
        num_writed_lines = 0
        required_fields = ['nome', 'descrizione']
        unique_fields = ['nome']
        there_is_unique_error = False

        for field in required_fields:
            if self.input_lines[field].text():
                num_writed_lines += 1
                if field in unique_fields:
                    for tabella in tabelle_millesimali_immobile:
                        if self.input_lines[field].text().upper() == tabella.nome.upper():
                            there_is_unique_error = True
        if there_is_unique_error:
            self.input_errors['nome'].setVisible(True)
            self.input_errors['nome'].setText("Nome della tabella millesimale già utilizzato nell'immobile selezionato")
        else:
            self.input_errors['nome'].setVisible(False)

        if there_is_unique_error or num_writed_lines < len(required_fields) or not self.tipi_spesa:
            self.buttons["Aggiungi Tabella Millesimale"].setDisabled(True)
        else:
            self.buttons["Aggiungi Tabella Millesimale"].setDisabled(False)

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.tipi_spesa:
            self.msg.setText("Non ci sono tipi di spesa asseganti alla tabella millesimale")
            self.msg.show()
