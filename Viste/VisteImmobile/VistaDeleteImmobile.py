from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaDeleteImmobile(QWidget):

    def __init__(self, sel_immobile, callback):
        super(VistaDeleteImmobile, self).__init__()
        self.callback = callback
        self.sel_immobile = sel_immobile
        main_layout = QGridLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere l'immobile?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addWidget(self.create_button("Procedi", self.deleteImmobile), 1, 0)
        main_layout.addWidget(self.create_button("Annulla", self.close), 1, 1)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Rimuovi Immobile")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def deleteImmobile(self):
        msg = ""
        for unitaImmobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.sel_immobile).values():
            for cf_condominoAssociato in unitaImmobiliare.condomini.keys():
                print("sto per eliminare il condomino con cf", cf_condominoAssociato)
                condomino = Condomino.ricercaCondominoByCF(cf_condominoAssociato)
                msg = unitaImmobiliare.removeCondomino(condomino)
                if not condomino.getImmobiliAssociati():
                    msg = condomino.rimuoviCondomino()
            msg = unitaImmobiliare.rimuoviUnitaImmobiliare()

        msg = self.sel_immobile.rimuoviImmobile()
        self.callback(msg)
        self.close()
