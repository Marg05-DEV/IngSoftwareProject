from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit


class VistaUpdateImmobile(QWidget):

    def __init__(self, sel_immobile, callback):
        super(VistaUpdateImmobile, self).__init__()
        self.callback = callback
        self.sel_immobile = sel_immobile
        main_layout = QGridLayout()

        lbl_frase = QLabel("Inserisci i nuovi dati dell'immobile da modificare:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Denominazione", "denominazione"), 1, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("CF/Partita IVA", "codiceFiscale"), 2, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Codice Numerico", "codice"), 3, 0)
        main_layout.addLayout(self.pairLabelInput("Sigla", "sigla"), 3, 1)
        main_layout.addLayout(self.pairLabelInput("Città", "citta"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("Provincia", "provincia"), 4, 1)
        main_layout.addLayout(self.pairLabelInput("CAP", "cap"), 5, 0)
        main_layout.addLayout(self.pairLabelInput("Via", "via"), 5, 1)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 6, 0)
        main_layout.addWidget(self.create_button("Annulla Modifica", self.close), 6, 1)

        main_layout.addWidget(self.create_button("Modifica Immobile", self.updateImmobile), 7, 0, 1, 2)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Modifica Immobile")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def pairLabelInput(self, testo, index):
        pair_layout = QHBoxLayout()

        label = QLabel(testo + ": ")
        input_line = QLineEdit()
        input_line.setPlaceholderText(str(self.sel_immobile.getInfoImmobile()[index]))
        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        return pair_layout

    def updateImmobile(self):
        self.callback()
        self.close()

    def reset(self):
        pass