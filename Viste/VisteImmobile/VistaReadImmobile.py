from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout

from Classes.RegistroAnagrafe.immobile import Immobile

class VistaReadImmobile(QWidget):

    def __init__(self, sel_immobile):
        super(VistaReadImmobile, self).__init__()
        i = 1

        self.sel_immobile = sel_immobile

        main_layout = QVBoxLayout()

        main_layout.addLayout(self.pair_label("Denominazione", "denominazione"))
        main_layout.addLayout(self.pair_label("CF/Partita IVA", "codiceFiscale"))
        main_layout.addLayout(self.pair_label("Codice Numerico", "codice"))
        print(i)
        i += 1
        main_layout.addLayout(self.pair_label("Sigla", "sigla"))
        main_layout.addLayout(self.pair_label("Città", "citta"))
        main_layout.addLayout(self.pair_label("Provincia", "provincia"))
        print(i)
        i += 1
        main_layout.addLayout(self.pair_label("CAP", "cap"))
        main_layout.addLayout(self.pair_label("Via", "via"))
        print(i)
        i += 1
        main_layout.addWidget(self.create_button("Modifica Immobile", self.updateImmobile))
        main_layout.addWidget(self.create_button("Elimina Immobile", self.deleteImmobile))

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Immobile")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def pair_label(self, testo, index):
        j = 1
        print(" -", j)
        j += 1
        pair_layout = QHBoxLayout()
        print(" -", j)
        j += 1
        lbl_desc = QLabel(testo + ": ")
        print(" -", j)
        j += 1
        lbl_content = QLabel(str(self.sel_immobile.getInfoImmobile()[index]))
        print(" -", j)
        j += 1
        pair_layout.addWidget(lbl_desc)
        pair_layout.addWidget(lbl_content)

        return pair_layout

    def updateImmobile(self):
        pass

    def deleteImmobile(self):
        pass
