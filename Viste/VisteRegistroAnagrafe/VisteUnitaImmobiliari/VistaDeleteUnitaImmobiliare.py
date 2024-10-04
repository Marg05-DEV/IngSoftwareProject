import qtawesome
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout

from Classes.RegistroAnagrafe.condomino import Condomino


class VistaDeleteUnitaImmobiliare(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback):
        super(VistaDeleteUnitaImmobiliare, self).__init__()
        self.callback = callback
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere l'unità immobiliare?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        main_layout.addLayout(self.create_warning_msg("La rimozione dell'unità immobiliare comporterà la rimozione \ndella sua assegnazione"))

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.create_button("Annulla", self.close))
        button_layout.addWidget(self.create_button("Procedi", self.deleteUnitaImmobiliare))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(350, 150)
        self.setWindowTitle("Rimuovi Unità Immobiliare")

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

    def deleteUnitaImmobiliare(self):
        for cf_condominoAssociato in self.sel_unitaImmobiliare.condomini.keys():
            condomino = Condomino.ricercaCondominoByCF(cf_condominoAssociato)
            self.sel_unitaImmobiliare.removeCondomino(condomino)
            if not condomino.getImmobiliAssociati():
                msg = condomino.rimuoviCondomino()
                
        msg = self.sel_unitaImmobiliare.rimuoviUnitaImmobiliare()
        self.callback(msg)
        self.close()
