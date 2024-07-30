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


class VistaCreateTipoSpesa(QWidget):
    def __init__(self, tabella_millesimale, callback, callback_append_tipo_spesa):
        super(VistaCreateTipoSpesa, self).__init__()
        self.tabella_millesimale = tabella_millesimale
        self.callback = callback
        self.callback_append_tipo_spesa = callback_append_tipo_spesa
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}
        main_layout = QVBoxLayout()


        lbl_frase = QLabel("Inserisci i dati del nuovo tipo di spesa:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)
        existing_tipo_spesa_layout = QHBoxLayout()
        existing_tipo_spesa_data_layout = QVBoxLayout()
        existing_tipo_spesa_button_layout = QVBoxLayout()
        self.lbl_exist = QLabel("Il tipo di spesa esistente è: ")
        self.lbl_tipo_spesa_esistente = QLabel()
        self.lbl_tipo_spesa_esistente.setStyleSheet("font-weight: bold;")
        self.button_exist = self.create_button("Assegna Tipo Spesa", self.add_tipo_spesa_esistente)
        self.button_exist.setVisible(False)
        self.lbl_exist.setVisible(False)
        self.lbl_tipo_spesa_esistente.setVisible(False)

        existing_tipo_spesa_data_layout.addWidget(self.lbl_exist, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        existing_tipo_spesa_data_layout.addWidget(self.lbl_tipo_spesa_esistente, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        existing_tipo_spesa_button_layout.addWidget(self.button_exist)

        existing_tipo_spesa_layout.addLayout(existing_tipo_spesa_data_layout)
        existing_tipo_spesa_layout.addLayout(existing_tipo_spesa_button_layout)
        main_layout.addLayout(existing_tipo_spesa_layout)

        action_layout1 = QVBoxLayout()
        action_layout1.addLayout(self.pairLabelInput("Nome", "nome"))
        action_layout1.addLayout(self.pairLabelInput("Descrizione", "descrizione"))

        main_layout.addLayout(action_layout1)
        main_layout.addWidget(self.create_button("Aggiungi Tipo Spesa", self.aggiungi_tipo_spesa))
        main_layout.addWidget(self.create_button("Annulla", self.reset))

        self.buttons["Aggiungi Tipo Spesa"].setDisabled(True)
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo tipo Spesa")

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
        input_line = QLineEdit()

        input_line.textChanged.connect(self.input_validation)
        self.input_lines[index] = input_line
        self.input_errors[index] = error
        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)
        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)
        return input_layout


    def aggiungi_tipo_spesa(self):
        nome = self.input_lines["nome"].text()
        descrizione = self.input_lines["descrizione"].text()

        temp_tipo_spesa = TipoSpesa()
        msg, ts = temp_tipo_spesa.aggiungiTipoSpesa(descrizione, nome)
        print(msg, ts)
        if self.tabella_millesimale != None:
            self.tabella_millesimale.addTipoSpesa(ts)
        else:
            self.callback_append_tipo_spesa(ts)
        self.callback(msg)
        self.close()

    def add_tipo_spesa_esistente(self):
        tipo_spesa = TipoSpesa.ricercaTipoSpesaByNome(self.lbl_tipo_spesa_esistente.text().split("\n")[0].split(":")[1])
        print(tipo_spesa)
        if self.tabella_millesimale != None:
            print("wow")
            self.tabella_millesimale.addTipoSpesa(tipo_spesa)
        else:
            print("wowow")
            self.callback_append_tipo_spesa(tipo_spesa)
        self.callback("Spesa aggiunta")
        self.close()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()
        self.lbl_exist.setVisible(False)
        self.lbl_tipo_spesa_esistente.setVisible(False)
        self.button_exist.setVisible(False)
    def input_validation(self):
        print("dentro la validazione")
        all_tipo_spesa = list(TipoSpesa.getAllTipoSpesa().values())

        tipo_spesa = []
        if self.tabella_millesimale != None:
            for tipo in self.tabella_millesimale.tipologieSpesa:
                value = TipoSpesa.ricercaTipoSpesaByCodice(tipo)
                tipo_spesa.append(value)

        num_errors = 0
        num_writed_lines = 0
        required_fields = ['nome', 'descrizione']
        there_is_unique_pair_error = False
        same_tb = False

        for field in required_fields:
            if self.input_lines[field].text():
                num_writed_lines += 1
                for all_tipi in all_tipo_spesa:
                    if self.input_lines['nome'].text().upper() == all_tipi.nome.upper():
                        num_errors += 1
                        there_is_unique_pair_error = True
                        if tipo_spesa:
                            for tipo in tipo_spesa:
                                if self.input_lines['nome'].text().upper() == tipo.nome.upper():
                                    same_tb = True
                        if not same_tb:
                            self.lbl_tipo_spesa_esistente.setText(f"Nome:{all_tipi.nome}\nDescrizione:{all_tipi.descrizione}")
                            self.button_exist.setDisabled(False)
                        break
        if there_is_unique_pair_error:
            self.input_errors['nome'].setVisible(True)
            if not same_tb:
                self.input_errors['nome'].setText(f"Nome del tipo è esistente ma non in questa tabella millesimale")
                self.lbl_exist.setVisible(True)
                self.lbl_tipo_spesa_esistente.setVisible(True)
                self.button_exist.setVisible(True)
            else:
                self.input_errors['nome'].setText(f"Nome del tipo spesa già esistente nella tabella millesimale")

        else:
            self.input_errors['nome'].setVisible(False)
            self.lbl_exist.setVisible(False)
            self.lbl_tipo_spesa_esistente.setVisible(False)
            self.button_exist.setVisible(False)

        if num_errors > 0 or num_writed_lines < len(required_fields):
            self.buttons["Aggiungi Tipo Spesa"].setDisabled(True)
        else:
            self.buttons["Aggiungi Tipo Spesa"].setDisabled(False)
