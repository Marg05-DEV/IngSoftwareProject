from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QHBoxLayout, QPushButton

from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaGestioneCondomino import VistaGestioneCondomino
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliare.VistaGestioneUnitaImmobiliare import VistaGestioneUnitaImmobiliare

class VistaMenuRegistroAnagrafe(QWidget):
    def __init__(self, parent=None):
        print("class VistaMenuRegistroAnagrafe - __init__ inizio")

        super(VistaMenuRegistroAnagrafe, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QGridLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Immobile")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per denominazione", "Ricerca per sigla", "Ricerca per codice"])
        self.searchType.activated.connect(self.debugComboBox1)

        find_layout.addWidget(self.searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)

        action_layout = QHBoxLayout()

        self.button_layout1 = QVBoxLayout()
        button_layout2 = QVBoxLayout()

        self.select_button = self.button_layout1.addWidget(self.create_button("Seleziona", self.go_Gestione_UnitaImmobiliare, True))
        self.button_layout1.addWidget(self.select_button)
        button_layout2.addWidget(self.create_button("Visualizza i Condomini", self.go_Gestione_Condomino))

        self.searchbar.textChanged.connect(self.able_button)
        action_layout.addLayout(self.button_layout1)
        action_layout.addLayout(button_layout2)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Menu Registro Anagrafe")
        print("class VistaGestioneImmobile - __init__ fine")

    def create_button(self, testo, action, disabled=False):
        print("class VistaGestioneImmobile - create_button inizio: bottone " + testo)
        button = QPushButton(testo)
        button.setFixedSize(110, 55)
        button.setCheckable(True)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        print("class VistaGestioneImmobile - create_button fine: bottone " + testo)
        print()
        return button

    def debugComboBox1(self, combo):
        print("pre")
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(
            self.searchType.currentText()))
        print("post")

    def go_Gestione_UnitaImmobiliare(self):
        self.vista_Gestione_UnitaImmobiliare = VistaGestioneUnitaImmobiliare()
        self.vista_Gestione_UnitaImmobiliare.show()

    def go_Gestione_Condomino(self):
        self.vista_Gestione_Condomino = VistaGestioneCondomino()
        self.vista_Gestione_Condomino.show()

    def able_button(self):
        print("selezione cambiata")
        if self.searchbar.text().strip():
            self.select_button.setEnabled(True)
        else:
            self.select_button.setEnabled(False)
