from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit

from Classes.RegistroAnagrafe.condomino import Condomino


class VistaDeleteCondomino(QWidget):

    def __init__(self, sel_condomino, callback):
        super(VistaDeleteCondomino, self).__init__()
        self.callback = callback
        self.sel_condomino = sel_condomino
        main_layout = QGridLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere il condomino?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addWidget(self.create_button("Procedi", self.deleteCondomino), 1, 0)
        main_layout.addWidget(self.create_button("Annulla", self.close), 1, 1)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Rimuovi Condomino")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def deleteCondomino(self):
        self.sel_condomino.rimuoviCondomino()
        self.callback()
        self.close()