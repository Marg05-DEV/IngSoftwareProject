from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, QSizePolicy


class VistaCreateImmobile(QWidget):

    def __init__(self, callback):
        super(VistaCreateImmobile, self).__init__()
        self.callback = callback
        main_layout = QGridLayout()

        lbl_frase = QLabel("Inserisci i dati del nuovo immobile:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Denominazione"), 1, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("CF/Partita IVA"), 2, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Codice Numerico"), 3, 0)
        main_layout.addLayout(self.pairLabelInput("Sigla"), 3, 1)
        main_layout.addLayout(self.pairLabelInput("Città"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("Provincia"), 4, 1)
        main_layout.addLayout(self.pairLabelInput("CAP"), 5, 0)
        main_layout.addLayout(self.pairLabelInput("Via"), 5, 1)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 6, 0, 1, 2)
        main_layout.addWidget(self.create_button("Aggiungi Immobile", self.createImmobile), 7, 0, 1, 2)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Immobile")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    @staticmethod
    def pairLabelInput(testo):
        pair_layout = QHBoxLayout()

        label = QLabel(testo + ": ")
        input_line = QLineEdit()
        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        return pair_layout

    def createImmobile(self):
        self.callback()
        self.close()

    def reset(self):
        pass
