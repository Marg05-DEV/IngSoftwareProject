from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit


class VistaUpdateCondomino(QWidget):

    def __init__(self, sel_condomino, callback):
        super(VistaUpdateCondomino, self).__init__()
        self.callback = callback
        self.sel_condomino = sel_condomino
        self.input_lines = {}
        main_layout = QGridLayout()

        lbl_frase = QLabel("Inserisci i nuovi dati del condomino da modificare:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Nome", "nome"), 1, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Cognome", "cognome"), 2, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Codice Fiscale", "codiceFiscale"), 3, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Luogo di nascita", "luogoDiNascita"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("Provincia di nascita", "provinciaDiNascita"), 4, 1)
        main_layout.addLayout(self.pairLabelInput("Data", "dataDiNascita"), 4, 2)
        main_layout.addLayout(self.pairLabelInput("Residenza", "residenza"), 5, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Telefono", "telefono"), 6, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Email", "email"), 7, 0, 1, 2)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 8, 0)
        main_layout.addWidget(self.create_button("Modifica Immobile", self.updateCondomino), 8, 1)

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
        self.input_lines[index] = input_line
        input_line.setPlaceholderText(str(self.sel_condomino.getDatiAnagraficiCondomino()[index]))
        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        return pair_layout

    def updateCondomino(self):
        print("inizio update condomino")
        temp_condomino = {}
        print(self.sel_condomino.getDatiAnagraficiCondomino().keys())
        for attributo in self.sel_condomino.getDatiAnagraficiCondomino().keys():
            if self.input_lines[attributo].text() == "":
                temp_condomino[attributo] = self.sel_condomino.getDatiAnagraficiCondomino()[attributo]
            else:
                temp_condomino[attributo] = self.input_lines[attributo].text()

        print(temp_condomino)
        msg = self.sel_condomino.modificaUnitaCondomino((temp_condomino["nome"]),
                                                 temp_condomino["cognome"],
                                                 temp_condomino["residenza"],
                                                 temp_condomino["dataDiNascita"],
                                                 temp_condomino["codiceFiscale"],
                                                 temp_condomino["luogoDiNascita"],
                                                 temp_condomino["provincia"],
                                                 temp_condomino["email"],
                                                 temp_condomino["telefono"])
        print("fine update condomino")
        self.callback(msg)
        self.close()

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()