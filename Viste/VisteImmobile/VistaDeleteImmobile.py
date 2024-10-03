import qtawesome
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QVBoxLayout

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaDeleteImmobile(QWidget):

    def __init__(self, sel_immobile, callback):
        super(VistaDeleteImmobile, self).__init__()
        self.callback = callback
        self.sel_immobile = sel_immobile
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere l'immobile?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        main_layout.addLayout(self.create_warning_msg("La rimozione dell'immobile comporterà la rimozione \ndi tutti i dati ad esso riferiti"))

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.create_button("Annulla", self.close))
        button_layout.addWidget(self.create_button("Procedi", self.deleteImmobile))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(350, 150)
        self.setWindowTitle("Rimuovi Immobile")

    def create_button(self, testo, action):
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

    def deleteImmobile(self):
        msg = ""
        for unitaImmobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.sel_immobile).values():
            for cf_condominoAssociato in unitaImmobiliare.condomini.keys():
                condomino = Condomino.ricercaCondominoByCF(cf_condominoAssociato)
                msg = unitaImmobiliare.removeCondomino(condomino)
                if not condomino.getImmobiliAssociati():
                    msg = condomino.rimuoviCondomino()
            msg = unitaImmobiliare.rimuoviUnitaImmobiliare()

        msg = self.sel_immobile.rimuoviImmobile()
        self.callback(msg)
        self.close()
