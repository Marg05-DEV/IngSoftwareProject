from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout

from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteImmobile import VistaGestioneImmobile
from Viste.VisteImmobile.VistaDeleteImmobile import VistaDeleteImmobile
from Viste.VisteImmobile.VistaUpdateImmobile import VistaUpdateImmobile


class VistaReadImmobile(QWidget):

    def __init__(self, sel_immobile, callback):
        super(VistaReadImmobile, self).__init__()
        self.sel_immobile = sel_immobile
        self.callback = callback

        main_layout = QVBoxLayout()

        main_layout.addLayout(self.pair_label("Denominazione", "denominazione"))
        main_layout.addLayout(self.pair_label("CF/Partita IVA", "codiceFiscale"))
        main_layout.addLayout(self.pair_label("Codice Numerico", "codice"))
        main_layout.addLayout(self.pair_label("Sigla", "sigla"))
        main_layout.addLayout(self.pair_label("Città", "citta"))
        main_layout.addLayout(self.pair_label("Provincia", "provincia"))
        main_layout.addLayout(self.pair_label("CAP", "cap"))
        main_layout.addLayout(self.pair_label("Via", "via"))

        main_layout.addWidget(self.create_button("Modifica Immobile", self.updateImmobile))
        main_layout.addWidget(self.create_button("Rimuovi Immobile", self.deleteImmobile))

        self.setLayout(main_layout)

        self.resize(300, 400)
        self.setWindowTitle("Dettaglio Immobile")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        return button

    def pair_label(self, testo, index):
        pair_layout = QHBoxLayout()

        lbl_desc = QLabel(testo + ": ")
        lbl_content = QLabel(str(self.sel_immobile.getInfoImmobile()[index]))

        pair_layout.addWidget(lbl_desc)
        pair_layout.addWidget(lbl_content)

        return pair_layout

    def updateImmobile(self):
        self.vista_modifica_immobile = VistaUpdateImmobile(self.sel_immobile, callback=self.callback)
        self.vista_modifica_immobile.show()
        self.close()

    def deleteImmobile(self):
        self.vista_elimina_immobile = VistaDeleteImmobile(self.sel_immobile, callback=self.callback)
        self.vista_elimina_immobile.show()
        self.close()
