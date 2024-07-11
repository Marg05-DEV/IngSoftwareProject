import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIntValidator, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy, QDateEdit, QComboBox, QListView, QCompleter
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Viste.VisteGestioneBilancio.VisteGestioneTabellaMillesimale.VistaCreateTipoSpesa import VistaCreateTipoSpesa


class VistaCreateTabellaMillesimale(QWidget):
    def __init__(self, immobile, callback):
        super(VistaCreateTabellaMillesimale, self).__init__()
        print("ciao bellu")
        self.immobile = immobile
        self.callback = callback
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}
        main_layout = QVBoxLayout()

        self.tipi_spesa = []

        lbl_frase = QLabel("Inserisci i dati della nuova tabella millesimale:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)
        action_layout1 = QVBoxLayout()
        print("ciao pidocchio 1")
        action_layout1.addLayout(self.pairLabelInput("Nome", "nome"))
        print("ciao3")
        action_layout1.addLayout(self.pairLabelInput("Descrizione", "descrizione"))
        print("ciao pidocchio 2")

        action_layout2 = QHBoxLayout()
        completer_list = sorted([item.nome for item in TipoSpesa.getAllTipoSpesa().values()])
        print(completer_list)
        self.searchbar = QComboBox()
        self.searchbar.setPlaceholderText("Ricerca un tipo di spesa ...")
        self.searchbar.addItems(completer_list)
        print("sisi")

        lbl_frase1 = QLabel("Aggiungi un tipo di spesa esistente:")
        lbl_frase1.setFixedSize(lbl_frase.sizeHint())

        action_layout2.addWidget(self.searchbar)
        action_layout2.addWidget(self.create_button("Aggiungi", self.seleziona_tipo_spesa))
        print("ciao2")
        action_layout3 = QHBoxLayout()

        lbl_frase2 = QLabel("Aggiungi un tipo di spesa esistente:")
        lbl_frase2.setFixedSize(lbl_frase.sizeHint())

        action_layout3.addWidget(lbl_frase2)
        action_layout3.addWidget(self.create_button("Aggiungi Tipo di Spesa", self.nuovo_tipo_spesa))
        print("ciao3")
        self.list_view_tipi_spesa = QListView()
        self.list_view_tipi_spesa.setAlternatingRowColors(True)
        print("ciao4")
        self.msg = QLabel("Non ci sono condomini assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()
        print("ciao8")
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addLayout(action_layout1)
        main_layout.addWidget(lbl_frase1)
        main_layout.addLayout(action_layout2)
        main_layout.addLayout(action_layout3)
        main_layout.addWidget(self.list_view_tipi_spesa)

        main_layout.addWidget(self.create_button("Aggiungi Tabella Millesimale", self.aggiungiTabellaMillesimale))
        self.update_list()
        main_layout.addWidget(self.msg)
        self.buttons["Aggiungi Tabella Millesimale"].setDisabled(True)
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Condomino")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        self.buttons[testo] = button
        return button

    def pairLabelInput(self, testo, index):
        print("ciao1")
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + "*: ")
        input_line = QLineEdit()

        input_line.textChanged.connect(self.input_validation)
        self.input_lines[index] = input_line
        self.input_errors[index] = error
        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)
        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)
        return input_layout

    def update_list(self):
        print("ciao5")
        if not self.tipi_spesa:
            self.msg.setText("Non ci sono tipi di spesa assegnati alla tabella millesimale")
            self.msg.show()
        else:
            self.msg.hide()
        print("ciao6")
        listview_model = QStandardItemModel(self.list_view_tipi_spesa)

        for tipi_spesa in self.tipi_spesa:
            item = QStandardItem()
            tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(tipi_spesa)
            item_text = f"Nome:{tipo_spesa.nome}\nDescrizione:{tipo_spesa.descrizione}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        print("qui finisce")
        self.list_view_tipi_spesa.setModel(listview_model)

    def aggiungiTabellaMillesimale(self):
        nome = self.input_lines["nome"].text()
        descrizione = self.input_lines["descrizione"].text()
        tipologiaSpesa = self.tipi_spesa
        immobile = self.immobile

        temp_tabellaMillesimale = TabellaMillesimale()
        msg, tm = temp_tabellaMillesimale.aggiungiTabellaMillesimale(
            nome, tipologiaSpesa, descrizione, immobile, {})

        print(msg, tm)
        self.callback(msg)
        self.close()

    def seleziona_tipo_spesa(self):
        self.search_text = self.searchbar.currentText()
        tipo_spesa = None
        if self.search_text:
            tipo_spesa = TipoSpesa.ricercaTipoSpesaByNome(self.search_text)
        if tipo_spesa:
            self.tipi_spesa.append(tipo_spesa.codice)
        print(self.tipi_spesa)
        self.input_validation()
        self.update_list()

    def nuovo_tipo_spesa(self):
        self.nuovo_tipo_spesa = VistaCreateTipoSpesa(None, self.callback, self.callback_for_append_tipo_spesa)
        self.input_validation()
        self.nuovo_tipo_spesa.show()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()

    def input_validation(self):
        print("ciao7")
        tabelleMillesimale = TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile)
        num_errors = 0
        num_writed_lines = 0
        required_fields = ['nome', 'descrizione']
        unique_fields = ['nome']
        there_is_unique_error = {}
        there_is_unique_pair_error = False

        for tabelle in tabelleMillesimale.values():
            if self.input_lines['nome'].text() == tabelle.nome:
                there_is_unique_pair_error = True
                break
        if there_is_unique_pair_error:
            self.input_errors['nome'].setText("Nome della tabella millesimale già esistente")
            self.input_errors["descrizione"].setText("")
            self.input_errors['nome'].setVisible(True)
            self.input_errors['descrizione'].setVisible(True)
        else:
            self.input_errors['nome'].setVisible(False)
            self.input_errors['descrizione'].setVisible(False)

        for field in required_fields:
            if self.input_lines[field].text():
                num_writed_lines += 1
                if field in unique_fields:
                    there_is_unique_error[field] = False
                    print(field)
                    for tabella in tabelleMillesimale.values():
                        print(self.input_lines[field].text().upper())
                        print(str(tabella.getInfoTabellaMillesimale()[field]).upper())
                        if self.input_lines[field].text().upper() == str(tabella.getInfoTabellaMillesimale()[field]).upper():
                            num_errors += 1
                            there_is_unique_error[field] = True
                            break
                    if there_is_unique_error[field]:
                        self.input_errors[field].setText(f"{field} già esistente")
                        self.input_errors[field].setVisible(True)
                    else:
                        self.input_errors[field].setVisible(False)
            else:
                self.input_errors[field].setVisible(False)

        if num_errors > 0 or num_writed_lines < len(required_fields) or not self.tipi_spesa:
            self.buttons["Aggiungi Tabella Millesimale"].setDisabled(True)
        else:
            self.buttons["Aggiungi Tabella Millesimale"].setDisabled(False)

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.tipi_spesa:
            self.msg.setText("Non ci sono tipi di spesa asseganti alla tabella millesimale")
            self.msg.show()

    def callback_for_append_tipo_spesa(self, tipo_spesa):
        self.tipi_spesa.append(tipo_spesa.codice)
        self.update_list()