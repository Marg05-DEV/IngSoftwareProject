from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QHBoxLayout, QPushButton, QLabel, \
    QCompleter

from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaGestioneCondomino import VistaGestioneCondomino
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliare.VistaGestioneUnitaImmobiliare import VistaGestioneUnitaImmobiliare

class VistaMenuRegistroAnagrafe(QWidget):
    def __init__(self, parent=None):
        print("class VistaMenuRegistroAnagrafe - __init__ inizio")
        print(Immobile.getAllImmobili())

        super(VistaMenuRegistroAnagrafe, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QGridLayout()
        completer_list = [item.denominazione for item in Immobile.getAllImmobili().values()]
        print(completer_list)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Immobile")
        self.immobili_completer = QCompleter(completer_list)
        #self.immobili_completer.setCaseSensitivity(Qt.UncaseSensitive)
        print(self.immobili_completer.completionModel())
        self.searchbar.setCompleter(self.immobili_completer)
        self.lbl_search = QLabel("Ricerca l'immobile da selezionare:")
        self.lbl_searchType = QLabel("Ricerca per:")
        self.searchType = QComboBox()
        self.searchType.addItems(["Denominazione", "Sigla", "Codice"])
        self.searchType.activated.connect(self.sel_tipo_ricerca)
        self.immobile_selezionato = QLabel("Nessun immobile selezionato")

        find_layout.addWidget(self.lbl_search, 0, 0, 1, 3)
        find_layout.addWidget(self.lbl_searchType, 0, 3)
        find_layout.addWidget(self.searchbar, 1, 0, 1, 3)
        find_layout.addWidget(self.searchType, 1, 3)
        find_layout.addWidget(QLabel("Stai selezionando: "), 2, 0, 1, 1)
        find_layout.addWidget(self.immobile_selezionato, 2, 1, 1, 3)

        self.button_layout = QHBoxLayout()

        self.select_button = self.create_button("Seleziona", self.go_Gestione_UnitaImmobiliare, True)
        self.button_layout.addWidget(self.select_button)
        self.button_layout.addWidget(self.create_button("Visualizza tutti i Condomini", self.go_Gestione_Condomino))

        self.searchbar.textChanged.connect(self.able_button)
        self.searchbar.textChanged.connect(self.selectioning)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(self.button_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Menu Registro Anagrafe")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setFixedSize(275, 55)
        button.setCheckable(True)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        return button

    def selectioning(self):
        immobile = None

        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            immobile = Immobile.ricercaImmobileByDenominazione(self.searchbar.text())
            print(immobile)
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            immobile = Immobile.ricercaImmobileBySigla(self.searchbar.text())
            print(immobile)
        elif self.searchType.currentIndex() == 2:  # ricerca per codice
            immobile = Immobile.ricercaImmobileByCodice(self.searchbar.text())
            print(immobile)

        if immobile != None:
            self.immobile_selezionato.setText(f"{immobile.codice} - {immobile.sigla} - {immobile.denominazione}")
        else:
            self.immobile_selezionato.setText("Nessun immobile selezionato")


    def sel_tipo_ricerca(self):
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(self.searchType.currentText()))
        lista_completamento = []
        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            lista_completamento = [item.denominazione for item in Immobile.getAllImmobili().values()]
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            lista_completamento = [item.sigla for item in Immobile.getAllImmobili().values()]
        elif self.searchType.currentIndex() == 2:  # ricerca per codice
            lista_completamento = [str(item.codice) for item in Immobile.getAllImmobili().values()]

        self.immobili_completer.setModel(QStringListModel(lista_completamento))

        self.selectioning()

    def go_Gestione_UnitaImmobiliare(self):
        search_text = self.searchbar.text()
        print(f"Testo della barra di ricerca: {search_text}")
        immobile = 0
        if search_text:
            print("sto cercando...")
            if self.searchType.currentIndex() == 0:  # ricerca per denominazione
                immobile = Immobile.ricercaImmobileByDenominazione(search_text)
                print(immobile)
            elif self.searchType.currentIndex() == 1:  # ricerca per sigla
                immobile = Immobile.ricercaImmobileBySigla(search_text)
                print(immobile)
            elif self.searchType.currentIndex() == 2:  # ricerca per codice
                immobile = Immobile.ricercaImmobileByCodice(search_text)
                print(immobile)
        if immobile != None:
            print("si")
            self.vista_Gestione_UnitaImmobiliare = VistaGestioneUnitaImmobiliare(search_text)
            self.vista_Gestione_UnitaImmobiliare.show()
        else:
            print("no")
            return None

    def go_Gestione_Condomino(self):
        self.vista_Gestione_Condomino = VistaGestioneCondomino()
        self.vista_Gestione_Condomino.show()

    def able_button(self):
        print("selezione cambiata")
        if self.searchbar.text().strip():
            self.select_button.setEnabled(True)
        else:
            self.select_button.setEnabled(False)
