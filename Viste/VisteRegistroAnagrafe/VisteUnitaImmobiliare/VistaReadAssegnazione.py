from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, \
    QListWidget

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteImmobile import VistaGestioneImmobile
from Viste.VisteImmobile.VistaDeleteImmobile import VistaDeleteImmobile
from Viste.VisteImmobile.VistaUpdateImmobile import VistaUpdateImmobile


class VistaReadAssegnazione(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback):
        super(VistaReadAssegnazione, self).__init__()
        print("dentro readAssegnazione")
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
        self.callback = callback
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("INFORMAZIONI UNITA' IMMOBILIARE:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(lbl_frase)

        main_layout.addLayout(self.pair_label("Tipologia Unità Immobiliare", "tipoUnitaImmobiliare"))
        main_layout.addLayout(self.pair_label("Scala", "scala"))
        main_layout.addLayout(self.pair_label("Interno", "interno"))

        lbl_frase1 = QLabel("DATI CATASTALI: ")
        lbl_frase1.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(lbl_frase1)
        dati_catastali_layout = QGridLayout()

        self.add_to_grid(dati_catastali_layout, "Foglio", "foglio", 0, 0)
        self.add_to_grid(dati_catastali_layout, "Particella", "particella", 0, 1)
        self.add_to_grid(dati_catastali_layout, "Subalterno", "subalterno", 0, 2)
        self.add_to_grid(dati_catastali_layout, "ZC", "ZC", 1, 0)
        self.add_to_grid(dati_catastali_layout, "Classe", "classe", 1, 1)
        self.add_to_grid(dati_catastali_layout, "Categoria", "categoria", 1, 2)

        main_layout.addLayout(dati_catastali_layout)
        main_layout.addWidget(self.create_button("Modifica Unità Immobiliare", self.updateUnitaImmobiliare))
        main_layout.addWidget(self.create_button("Rimuovi Unità Immobiliare", self.deleteUnitaImmobiliare))
        print("Prossimo problema")

        condomini_label = QLabel("CONDOMINI ASSEGNATI:")
        condomini_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(condomini_label)

        self.condomini_list = QListWidget()
        for condomino in self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()["condomini"]:
            self.condomini_list.addItem(condomino)
        main_layout.addWidget(self.condomini_list)

        main_layout.addWidget(self.create_button("Aggiungi Condomino", self.addCondomino))
        main_layout.addWidget(self.create_button("Modifica Condomino", self.updateCondomino))
        main_layout.addWidget(self.create_button("Visualizza Condomino", self.readCondomino))
        main_layout.addWidget(self.create_button("Rimuovi Condomino", self.deleteCondomino))

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Assegnazione")

    @staticmethod
    def create_button(testo, action):
        print("botoni ok")
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def pair_label(self, testo, index):
        pair_layout = QHBoxLayout()

        lbl_desc = QLabel(testo + ": ")
        lbl_content = QLabel(str(self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[index]))

        pair_layout.addWidget(lbl_desc)
        pair_layout.addWidget(lbl_content)
        return pair_layout

    def add_to_grid(self, layout, testo, index, row, col):
        print("dentro grid")
        lbl_desc = QLabel(testo + ": ")
        lbl_content = QLabel(str(self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[index]))
        layout.addWidget(lbl_desc, row, col * 2)
        layout.addWidget(lbl_content, row, col * 2 + 1)
        print("esci da qua")

    def updateUnitaImmobiliare(self):
        # Logica per aggiornare l'unità immobiliare
        pass

    def deleteUnitaImmobiliare(self):
        # Logica per rimuovere l'unità immobiliare
        pass

    def addCondomino(self):
        # Logica per aggiungere un condominio
        pass

    def updateCondomino(self):
        pass

    def readCondomino(self):
        pass

    def deleteCondomino(self):
        pass