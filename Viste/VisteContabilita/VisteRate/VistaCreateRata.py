from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QLineEdit


class VistaCreateRata(QWidget):

    def __init__(self, callback):
        super(VistaCreateRata, self).__init__()
        self.callback = callback
        main_layout = QVBoxLayout()
        self.input_lines = {}
        self.input_errors = {}
        self.buttons = {}

        lbl_frase = QLabel("Inserisci i dati della nuova rata: (* Campi obbligatori)")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Immobile", "immobile"))
        main_layout.addLayout(self.pairLabelInput("UnitaImmobiliare", "unitaImmobiliare"))
        main_layout.addLayout(self.pairLabelInput("Versante", "versante"))
        main_layout.addLayout(self.pairLabelInput("Descrizione", "descrizione"))
        main_layout.addLayout(self.pairLabelInput("Numero Ricevuta", "numeroRicevuta"))
        main_layout.addLayout(self.pairLabelInput("Importo", "importo"))
        main_layout.addLayout(self.pairLabelInput("Data Pagamento", "dataPagamento"))
        main_layout.addLayout(self.pairLabelInput("Tipologia Pagamento", "tipoPagamento"))

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset))
        main_layout.addWidget(self.create_button("Aggiungi Immobile", self.createRata))

        self.buttons["Aggiungi Rata"].setDisabled(True)
        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Immobile")

    def create_button(self,testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
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

        if index == "codice":
            input_line.setValidator(QIntValidator())

        input_line.textChanged.connect(self.input_validation)
        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout