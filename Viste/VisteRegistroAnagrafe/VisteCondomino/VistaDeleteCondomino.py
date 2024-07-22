import qtawesome
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout

from Classes.RegistroAnagrafe.condomino import Condomino


class VistaDeleteCondomino(QWidget):

    def __init__(self, sel_condomino, unita_immobiliare, callback):
        super(VistaDeleteCondomino, self).__init__()
        self.callback = callback
        self.sel_condomino = sel_condomino
        self.unita_immobiliare = unita_immobiliare
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere il condomino?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        main_layout.addLayout(self.create_warning_msg("Se il condomino non è assegnato a nessun altra unità immobiliare, \nquesto verrà definitivamente rimosso"))

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.create_button("Procedi", self.deleteCondomino))
        button_layout.addWidget(self.create_button("Annulla", self.close))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(350, 150)
        self.setWindowTitle("Rimuovi Condomino")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        return button

    def create_warning_msg(self, testo):
        warning_msg_layout = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(qtawesome.icon('fa.warning').pixmap(QSize(16, 16)))
        icon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label = QLabel(testo)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        label.setStyleSheet("font-size: 10px;")

        warning_msg_layout.addWidget(icon)
        warning_msg_layout.addWidget(label)

        return warning_msg_layout

    def deleteCondomino(self):
        msg = ""
        self.unita_immobiliare.removeCondomino(self.sel_condomino)
        msg = "Il condomino è stato disassegnato dall'unità immobiliare"
        if not self.sel_condomino.getImmobiliAssociati():
            msg = self.sel_condomino.rimuoviCondomino()
        self.callback(msg)
        self.close()
