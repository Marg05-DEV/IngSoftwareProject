import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy, QDateEdit, QComboBox
import itertools
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino



class VistaCreateCondomino(QWidget):
    def __init__(self, immobile, ui, callback, isIterable):
        super(VistaCreateCondomino, self).__init__()
        print("------------------------------------------------- create condomino --------------------------------")
        self.immobile = immobile
        self.unitaImmobiliare = ui
        self.callback = callback
        self.isIterable = isIterable
        main_layout = QVBoxLayout()
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}

        lbl_frase = QLabel("Inserisci i dati per l'aggiunta di un nuovo condomino: (* Campi obbligatori)")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        existing_condomino_layout = QHBoxLayout()
        existing_condomino_data_layout = QVBoxLayout()
        existing_condomino_button_layout = QVBoxLayout()
        self.lbl_exist = QLabel("Il condomino esistente è: ")
        self.lbl_condomino_esistente = QLabel()
        self.lbl_condomino_esistente.setStyleSheet("font-weight: bold;")
        if isIterable:
            self.button_exist_continue = self.create_button("Assegna il condomino esistente e continua ad assegnare condomini", self.add_condomino_esistente_continue)
            self.button_exist_stop = self.create_button("Assegna il condomino esistente e termina assegnazione", self.add_condomino_esistente_stop)
            self.button_exist_continue.setVisible(False)
            self.button_exist_stop.setVisible(False)
            existing_condomino_button_layout.addWidget(self.button_exist_continue)
        else:
            self.button_exist_stop = self.create_button("Assegna il condomino esistente", self.add_condomino_esistente_stop)
            self.button_exist_stop.setVisible(False)

        self.lbl_exist.setVisible(False)
        self.lbl_condomino_esistente.setVisible(False)
        self.error_exist = QLabel("Inserire il titolo prima di assegnarlo")
        self.error_exist.setStyleSheet("color: red; font-style: italic;")
        self.error_exist.setVisible(False)

        existing_condomino_data_layout.addWidget(self.lbl_exist, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        existing_condomino_data_layout.addWidget(self.lbl_condomino_esistente, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        existing_condomino_button_layout.addWidget(self.error_exist, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        existing_condomino_button_layout.addWidget(self.button_exist_stop)

        existing_condomino_layout.addLayout(existing_condomino_data_layout)
        existing_condomino_layout.addLayout(existing_condomino_button_layout)
        main_layout.addLayout(existing_condomino_layout)

        main_layout.addLayout(self.pairLabelInput("Codice Fiscale", "codiceFiscale"))
        main_layout.addLayout(self.pairLabelInput("Nome", "nome"))
        main_layout.addLayout(self.pairLabelInput("Cognome", "cognome"))

        nascita_layout = QHBoxLayout()
        nascita_layout.addLayout(self.pairLabelInput("Luogo di nascita", "luogoDiNascita"))
        nascita_layout.addLayout(self.pairLabelInput("Provincia", "provinciaDiNascita"))
        nascita_layout.addLayout(self.pairLabelInput("Data", "dataDiNascita"))
        main_layout.addLayout(nascita_layout)

        main_layout.addLayout(self.pairLabelInput("Residenza", "residenza"))
        main_layout.addLayout(self.pairLabelInput("Telefono", "telefono"))
        main_layout.addLayout(self.pairLabelInput("Email", "email"))
        main_layout.addLayout(self.pairLabelInput("Titolo dell'unità immobiliare", "titolo"))

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset))

        if isIterable:
            button_layout = QHBoxLayout()
            button_layout.addWidget(self.create_button("Termina Assegnazione", self.terminaAssegnazione))
            button_layout.addWidget(self.create_button("Aggiungi altro condomino", self.altroCondomino))
            self.buttons["Termina Assegnazione"].setDisabled(True)
            self.buttons["Aggiungi altro condomino"].setDisabled(True)
            main_layout.addLayout(button_layout)
        else:
            main_layout.addWidget(self.create_button("Aggiungi Condomino", self.terminaAssegnazione))
            self.buttons["Aggiungi Condomino"].setDisabled(True)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Condomino")

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
        if testo == "Data":
            input_line = QDateEdit()
            input_line.dateChanged.connect(self.input_validation)
        elif index == "titolo":
            input_line = QComboBox()
            input_line.setPlaceholderText("Scegli un titolo per il condomino...")
            if 'Proprietario' in self.unitaImmobiliare.condomini.values():
                input_line.addItems(["Comproprietario", "Inquilino"])
            else:
                input_line.addItems(["Proprietario", "Comproprietario", "Inquilino"])
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

    def closeEvent(self, event):
        self.callback("")

    def aggiungiCondomino(self):
        print("stiamo per aggiungere")
        nome = self.input_lines["nome"].text()
        cognome = self.input_lines["cognome"].text()
        residenza = self.input_lines["residenza"].text()
        dataDiNascita = self.input_lines["dataDiNascita"].text()
        dataDiNascita = dataDiNascita.split("/")
        dataDiNascita = datetime.date(int(dataDiNascita[2]), int(dataDiNascita[1]), int(dataDiNascita[0]))
        codiceFiscale = self.input_lines["codiceFiscale"].text()
        luogoDiNascita = self.input_lines["luogoDiNascita"].text()
        provinciaDiNascita = self.input_lines["provinciaDiNascita"].text()
        email = self.input_lines["email"].text()
        telefono = self.input_lines["telefono"].text()

        temp_condomino = Condomino()
        msg, condomino = temp_condomino.aggiungiCondomino(nome, cognome, residenza, dataDiNascita, codiceFiscale,
                                                          luogoDiNascita, provinciaDiNascita,
                                                          email, telefono)

        titolo = self.input_lines["titolo"].currentText()

        self.unitaImmobiliare.addCondomino(condomino, titolo)

        print("aggiunta in corso...")

        return msg

    def terminaAssegnazione(self):
        msg = self.aggiungiCondomino()
        print("stiamo per uscire", msg)
        print("f di callback", self.callback)
        self.callback(msg)
        self.close()

    def altroCondomino(self):
        msg = self.aggiungiCondomino()
        self.close()
        self.vista_nuovo_condomino = VistaCreateCondomino(self.immobile, self.unitaImmobiliare, self.callback, True)
        self.vista_nuovo_condomino.show()

    def add_condomino_esistente_stop(self):
        self.add_condomino_esistente()
        self.callback("Il condomino è stato aggiunto")
        self.close()

    def add_condomino_esistente_continue(self):
        self.add_condomino_esistente()
        self.close()
        self.vista_nuovo_condomino = VistaCreateCondomino(self.immobile, UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.unitaImmobiliare.codice), self.callback, True)
        self.vista_nuovo_condomino.show()

    def add_condomino_esistente(self):
        condomino = Condomino.ricercaCondominoByCF(self.lbl_condomino_esistente.text().split(" (")[1].split(")")[0])
        titolo = self.input_lines["titolo"].currentText()

        self.unitaImmobiliare.addCondomino(condomino, titolo)

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()

        if 'Proprietario' in self.unitaImmobiliare.condomini.values():
            self.input_lines['titolo'].addItems(["Comproprietario", "Inquilino"])
        else:
            self.input_lines['titolo'].addItems(["Proprietario", "Comproprietario", "Inquilino"])

        self.input_lines["dataDiNascita"].setDate(datetime.date(2000, 1, 1))

        self.lbl_exist.setVisible(False)
        self.lbl_condomino_esistente.setVisible(False)
        self.button_exist_stop.setVisible(False)
        self.error_exist.setVisible(False)
        if self.isIterable:
            self.button_exist_continue.setVisible(False)

    def input_validation(self):
        print("--------------validazione-------------")
        condomini = Condomino.getAllCondomini()
        num_errors = 0
        num_writed_lines = 0
        required_fields = ['nome', 'cognome', 'codiceFiscale', 'luogoDiNascita', 'provinciaDiNascita', 'residenza',
                           'telefono', 'email', 'titolo']

        unique_fields = ['codiceFiscale']
        there_is_unique_error = {}
        same_ui = False

        for field in required_fields:
            print("campo:", field)
            pieno = False
            if field != 'titolo':
                if self.input_lines[field].text():
                    print("PIENO")
                    pieno = True
                else:
                    self.input_errors[field].setVisible(False)
            else:
                print("è proprio titolo")
                if self.input_lines[field].currentIndex() > -1:
                    print("PIENO")
                    pieno = True
                else:
                    self.input_errors[field].setVisible(False)

            if pieno:
                num_writed_lines += 1
                print("num writed", num_writed_lines)
                if field in unique_fields:
                    there_is_unique_error[field] = False
                    print("campo unique", field)
                    for condomino in condomini.values():
                        if self.input_lines[field].text().upper() == str(condomino.getDatiAnagraficiCondomino()[field]).upper():
                            num_errors += 1
                            there_is_unique_error[field] = True
                            if condomino.codiceFiscale in self.unitaImmobiliare.condomini.keys():
                                same_ui = True
                            if not same_ui:
                                if self.input_lines['titolo'].currentIndex() > -1:
                                    self.lbl_condomino_esistente.setText(f"{condomino.cognome} {condomino.nome} ({condomino.codiceFiscale})")
                                    self.button_exist_stop.setDisabled(False)
                                    self.error_exist.setVisible(False)
                                    if self.isIterable:
                                        self.button_exist_continue.setDisabled(False)
                                else:
                                    self.lbl_condomino_esistente.setText(f"{condomino.cognome} {condomino.nome} ({condomino.codiceFiscale})")
                                    self.button_exist_stop.setDisabled(True)
                                    self.error_exist.setVisible(True)
                                    if self.isIterable:
                                        self.button_exist_continue.setDisabled(True)
                            break
                    if there_is_unique_error[field]:
                        self.input_errors[field].setVisible(True)
                        if not same_ui:
                            self.input_errors[field].setText(f"condomino esistente")
                            self.lbl_exist.setVisible(True)
                            self.lbl_condomino_esistente.setVisible(True)
                            self.button_exist_stop.setVisible(True)
                            if self.isIterable:
                                self.button_exist_continue.setVisible(True)
                        else:
                            self.input_errors[field].setText(f"condomino già assegnato all'unità immobiliare")
                    else:
                        self.input_errors[field].setVisible(False)
                        self.lbl_exist.setVisible(False)
                        self.lbl_condomino_esistente.setVisible(False)
                        self.button_exist_stop.setVisible(False)
                        if self.isIterable:
                            self.button_exist_continue.setVisible(False)
                else:
                    self.input_errors[field].setVisible(False)

        print("fine for")
        if num_errors > 0 or num_writed_lines < len(required_fields):
            if self.isIterable:
                self.buttons["Termina Assegnazione"].setDisabled(True)
                self.buttons["Aggiungi altro condomino"].setDisabled(True)
            else:
                self.buttons["Aggiungi Condomino"].setDisabled(True)
        else:
            if self.isIterable:
                self.buttons["Termina Assegnazione"].setDisabled(False)
                self.buttons["Aggiungi altro condomino"].setDisabled(False)
            else:
                self.buttons["Aggiungi Condomino"].setDisabled(False)

