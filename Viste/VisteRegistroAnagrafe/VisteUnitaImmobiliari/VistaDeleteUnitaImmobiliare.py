from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit

from Classes.Gestione.gestoreRegistroAnagrafe import GestoreRegistroAnagrafe
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaDeleteUnitaImmobiliare(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback):
        super(VistaDeleteUnitaImmobiliare, self).__init__()
        self.callback = callback
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
        main_layout = QGridLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere l'unità immobiliare?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addWidget(self.create_button("Procedi", self.deleteUnitaImmobiliare), 1, 0)
        main_layout.addWidget(self.create_button("Annulla", self.close), 1, 1)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Rimuovi Unità Immobiliare")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def deleteUnitaImmobiliare(self):
        for cf_condominoAssociato in self.sel_unitaImmobiliare.condomini.keys():
            condomino = Condomino.ricercaCondominoByCF(cf_condominoAssociato)
            self.sel_unitaImmobiliare.removeCondomino(condomino)
            if not condomino.getImmobiliAssociati():
                msg = condomino.rimuoviCondomino()
        msg = self.sel_unitaImmobiliare.rimuoviUnitaImmobiliare()
        self.callback(msg)
        self.close()