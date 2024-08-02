from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout


class VistaAvvisoBilancio(QWidget):

    def __init__(self, from_vista, action_conferma, testo, testo_conferma="Conferma", testo_annulla="Annulla"):
        super(VistaAvvisoBilancio, self).__init__()
        self.action_conferma = action_conferma
        self.from_vista = from_vista

        main_layout = QVBoxLayout()

        lbl_frase = QLabel(testo)
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.create_button(testo_conferma, self.action))
        button_layout.addWidget(self.create_button(testo_annulla, self.close))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(350, 150)
        self.setWindowTitle("Avviso")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        return button

    def action(self):
        self.action_conferma()
        self.from_vista.avvisoConfermato()
        self.close()
