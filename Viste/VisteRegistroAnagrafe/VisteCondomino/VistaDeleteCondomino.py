from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit

from Classes.RegistroAnagrafe.condomino import Condomino


class VistaDeleteCondomino(QWidget):

    def __init__(self, sel_condomino, unita_immobiliare, callback):
        super(VistaDeleteCondomino, self).__init__()
        self.callback = callback
        self.sel_condomino = sel_condomino
        self.unita_immobiliare = unita_immobiliare
        main_layout = QGridLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere il condomino?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addWidget(self.create_button("Procedi", self.deleteCondomino), 1, 0)
        main_layout.addWidget(self.create_button("Annulla", self.close), 1, 1)


        message_layout = QHBoxLayout()

        self.msg = QLabel("Il condomino è stato rimosso")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        message_widget = QWidget()
        message_widget.setLayout(message_layout)
        main_layout.addWidget(message_widget, 2, 0, 1, 2)

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
        msg = ""
        self.unita_immobiliare.removeCondomino(Condomino.ricercaCondominoByCF(self.sel_condomino.codiceFiscale))
        msg = "Il condomino è stato disassegnato dall'unità immobiliare"
        print("dissasociato", self.sel_condomino.getImmobiliAssociati())
        if not self.sel_condomino.getImmobiliAssociati():
            msg = self.sel_condomino.rimuoviCondomino()
        self.callback(msg)
        self.close()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()