from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteImmobile import VistaGestioneImmobile
from Viste.VisteImmobile.VistaDeleteImmobile import VistaDeleteImmobile
from Viste.VisteImmobile.VistaUpdateImmobile import VistaUpdateImmobile


class VistaReadAssegnazione(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback):
        super(VistaReadAssegnazione, self).__init__()
        self.sel_immobile = sel_unitaImmobiliare
        self.callback = callback
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("INFORMAZIONI UNITA' IMMOBILIARE:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pair_label("Tipologia Unità Immobiliare", "tipologiaUnitaImmobiliare"))
        main_layout.addLayout(self.pair_label("Scala", "scala"))
        main_layout.addLayout(self.pair_label("Interno", "interno"))

        lbl_frase1 = QLabel("INFORMAZIONI UNITA' IMMOBILIARE:")
        lbl_frase1.setStyleSheet("font-weight: bold;")
        lbl_frase1.setFixedSize(lbl_frase1.sizeHint())

        main_layout.addWidget(lbl_frase1, 0, 1, 1, 2)
        main_layout.addLayout(self.pair_label("Data di Nascita", "dataDiNascita"))
        main_layout.addLayout(self.pair_label("Codice Fiscale", "codiceFiscale"))
        main_layout.addLayout(self.pair_label("Luogo di nascita", "luogoDiNascita"))
        main_layout.addLayout(self.pair_label("Provincia di nascita", "provinciaDiNascita"))
        main_layout.addLayout(self.pair_label("Email", "email"))
        main_layout.addLayout(self.pair_label("Telefono", "telefono"))


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