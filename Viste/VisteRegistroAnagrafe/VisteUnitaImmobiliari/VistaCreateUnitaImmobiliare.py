
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy, QComboBox, QFrame

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaCreateCondomino import VistaCreateCondomino


class VistaCreateUnitaImmobiliare(QWidget):

    def __init__(self, immobile, callback):
        super(VistaCreateUnitaImmobiliare, self).__init__()
        print("eu estou")
        self.immobile = immobile
        self.callback = callback
        main_layout = QVBoxLayout()
        self.input_lines = {}
        self.labels = {}
        self.input_errors = {}
        self.buttons = {}
        self.required_fields = ['tipoUnitaImmobiliare', 'foglio', 'particella', 'subalterno', 'ZC', 'classe', 'categoria']

        lbl_frase = QLabel("Inserisci i dati per la nuova assegnazione: (* Campi Obbligatori)")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        main_layout.addLayout(self.pairLabelInput("Tipologia Unità Immobiliare", "tipoUnitaImmobiliare", ))
        self.dati_appartamento = QHBoxLayout()
        self.dati_appartamento.addLayout(self.pairLabelInput("Scala", "scala"))
        self.dati_appartamento.addLayout(self.pairLabelInput("Interno", "interno"))

        dati_catastali1 = QHBoxLayout()
        dati_catastali1.addLayout(self.pairLabelInput("Foglio", "foglio"))
        dati_catastali1.addLayout(self.pairLabelInput("Particella", "particella"))
        dati_catastali1.addLayout(self.pairLabelInput("Subalterno", "subalterno"))

        dati_catastali2 = QHBoxLayout()
        dati_catastali2.addLayout(self.pairLabelInput("ZC", "ZC"))
        dati_catastali2.addLayout(self.pairLabelInput("Classe", "classe"))
        dati_catastali2.addLayout(self.pairLabelInput("Categoria", "categoria"))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        button_layout.addWidget(self.create_button("Assegna Condomini", self.createUnitaImmobiliare))
        self.buttons["Assegna Condomini"].setDisabled(True)

        main_layout.addLayout(self.dati_appartamento)
        main_layout.addLayout(dati_catastali1)
        main_layout.addLayout(dati_catastali2)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Assegnazione")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.buttons[testo] = button
        button.clicked.connect(action)
        return button

    def pairLabelInput(self, testo, index):
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()
        integer_lines = ['scala', 'interno', 'foglio', 'particella', 'subalterno', 'classe']

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + "*: ")
        if index == "tipoUnitaImmobiliare":
            input_line = QComboBox()
            input_line.setPlaceholderText("Scegli la tipologia di Unità Immobiliare...")
            input_line.addItems(['Appartamento', 'Box', 'Cantina', 'Negozio'])
            input_line.activated.connect(self.scelta_tipologia)
            input_line.activated.connect(self.input_validation)
        else:
            input_line = QLineEdit()
            input_line.textChanged.connect(self.input_validation)

        if index in ['interno', 'scala']:
            label.setVisible(False)
            input_line.setVisible(False)

        if index in integer_lines:
            input_line.setValidator(QIntValidator())

        self.labels[index] = label
        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def scelta_tipologia(self):
        if self.input_lines["tipoUnitaImmobiliare"].currentText() != "Appartamento":
            self.input_lines["interno"].setVisible(False)
            self.input_lines["scala"].setVisible(False)
            self.labels["interno"].setVisible(False)
            self.labels["scala"].setVisible(False)
            if "interno" in self.required_fields and "scala" in self.required_fields:
                self.required_fields.remove("interno")
                self.required_fields.remove("scala")
        else:
            self.input_lines["interno"].setVisible(True)
            self.input_lines["scala"].setVisible(True)
            self.labels["interno"].setVisible(True)
            self.labels["scala"].setVisible(True)
            if not ("interno" in self.required_fields and "scala" in self.required_fields):
                self.required_fields.append("interno")
                self.required_fields.append("scala")
        print(self.required_fields)

    def createUnitaImmobiliare(self):
        foglio = self.input_lines["foglio"].text()
        subalterno = self.input_lines["subalterno"].text()
        particella = self.input_lines["particella"].text()
        interno = 0
        scala = 0

        tipo_unita_immobiliare = self.input_lines["tipoUnitaImmobiliare"].currentText()
        if tipo_unita_immobiliare == "Appartamento":
            interno = int(self.input_lines["interno"].text())
            scala = int(self.input_lines["scala"].text())

        categoria = self.input_lines["categoria"].text()
        classe = self.input_lines["classe"].text()

        zc = self.input_lines["ZC"].text()

        temp_unitaImmobiliare = UnitaImmobiliare()
        msg, ui = temp_unitaImmobiliare.aggiungiUnitaImmobiliare(int(foglio), int(subalterno), {}, int(particella), interno,
                                                             tipo_unita_immobiliare, categoria, int(classe),
                                                             self.immobile, scala, zc)

        self.close()
        self.vista_nuovo_Condomino = VistaCreateCondomino(self.immobile, ui, self.callback, True)
        self.vista_nuovo_Condomino.show()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()
        self.input_lines["tipoUnitaImmobiliare"].addItems(['Appartamento', 'Box', 'Cantina', 'Negozio'])
        self.input_validation()

    def input_validation(self):
        print("scrivendo ...", self.immobile)
        unitaImmobiliari = UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile)
        num_writed_lines = 0
        there_is_unique_pair_error = False

        if self.input_lines['tipoUnitaImmobiliare'].currentText() == "Appartamento":
            for unita in unitaImmobiliari.values():
                if self.input_lines['interno'].text() == str(unita.interno) and self.input_lines['scala'].text() == str(unita.scala):
                    there_is_unique_pair_error = True
                    break
        if there_is_unique_pair_error:
            self.input_errors['scala'].setText("interno già esistente nella scala inserita")
            self.input_errors['interno'].setText("")
            self.input_errors['scala'].setVisible(True)
            self.input_errors['interno'].setVisible(True)
        else:
            self.input_errors['scala'].setVisible(False)
            self.input_errors['interno'].setVisible(False)

        print(self.required_fields)
        for field in self.required_fields:
            if field == 'tipoUnitaImmobiliare':
                if self.input_lines[field].currentIndex() != -1:
                    num_writed_lines += 1
                else:
                    self.input_errors[field].setVisible(False)
            else:
                if self.input_lines[field].text():
                    num_writed_lines += 1
                else:
                    self.input_errors[field].setVisible(False)
        print("numero linee riempite", num_writed_lines)

        if num_writed_lines < len(self.required_fields) or there_is_unique_pair_error:
            self.buttons["Assegna Condomini"].setDisabled(True)
        else:
            self.buttons["Assegna Condomini"].setDisabled(False)