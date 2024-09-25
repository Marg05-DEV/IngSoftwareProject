from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QHBoxLayout, QPushButton, QLabel, \
    QCompleter

from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteBilancio.VisteGestioneBilancio.VistaGestioneEsercizi import VistaGestioneEsercizi
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaGestioneTabelleMillesimali import VistaGestioneTabelleMillesimali
from Viste.VisteBilancio.VisteGestioneBilancio.VistaGestioneBilancio import VistaGestioneBilancio
class VistaMenuGestioneBilancio(QWidget):
    def __init__(self, parent=None):

        super(VistaMenuGestioneBilancio, self).__init__(parent)

        main_layout = QVBoxLayout()

        completer_list = [item.denominazione for item in Immobile.getAllImmobili().values()]
        print(completer_list)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Immobile")
        self.immobili_completer = QCompleter(completer_list)
        self.immobili_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        print(self.immobili_completer.completionModel())
        self.searchbar.setCompleter(self.immobili_completer)
        self.lbl_search = QLabel("Ricerca l'immobile da selezionare:")
        self.lbl_searchType = QLabel("Ricerca per:")
        self.searchType = QComboBox()
        self.searchType.addItems(["Denominazione", "Sigla", "Codice"])
        self.searchType.activated.connect(self.sel_tipo_ricerca)


        find_layout = QHBoxLayout()

        search_layout = QVBoxLayout()
        type_layout = QVBoxLayout()

        search_layout.addWidget(self.lbl_search)
        type_layout.addWidget(self.lbl_searchType)
        search_layout.addWidget(self.searchbar)
        type_layout.addWidget(self.searchType)

        find_layout.addLayout(search_layout)
        find_layout.addLayout(type_layout)

        main_layout.addLayout(find_layout)

        msg_layout = QHBoxLayout()

        frase_lbl = QLabel("Stai selezionando: ")
        self.immobile_selezionato = QLabel("Nessun immobile selezionato")

        msg_layout.addWidget(frase_lbl)
        msg_layout.addWidget(self.immobile_selezionato)

        main_layout.addLayout(msg_layout)

        if not completer_list:
            frase_lbl.setText("Nessun immobile presente")
            self.immobile_selezionato.setVisible(False)

        self.button_layout = QHBoxLayout()
        self.select_button = self.create_button("Vai alla gestione delle tabelle millesimali", self.go_Gestione_TabelleMillesimali, True)
        self.button_layout.addWidget(self.select_button)
        self.select_button1 = self.create_button("Vai alla gestione del bilancio", self.go_Gestione_Bilancio, True)
        self.button_layout.addWidget(self.select_button1)
        self.searchbar.textChanged.connect(self.selectioning)

        main_layout.addLayout(self.button_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Menu Gestione Bilancio")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setFixedSize(275, 55)
        button.setCheckable(False)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        return button

    def selectioning(self):
        immobile = None

        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            immobile = Immobile.ricercaImmobileByDenominazione(self.searchbar.text())
            print("imm: ", immobile)
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            immobile = Immobile.ricercaImmobileBySigla(self.searchbar.text())
            print("imm: ", immobile)
        elif self.searchType.currentIndex() == 2:  # ricerca per codice
            immobile = Immobile.ricercaImmobileByCodice(self.searchbar.text())
            print("imm: ", immobile)

        if immobile != None:
            print("immobile trovato")
            self.immobile_selezionato.setText(f"{immobile.codice} - {immobile.sigla} - {immobile.denominazione}")
            self.select_button.setEnabled(True)
            self.select_button1.setEnabled(True)
        else:
            print("Nessun immobile trovato")
            self.immobile_selezionato.setText("Nessun immobile selezionato")
            self.select_button.setEnabled(False)
            self.select_button1.setEnabled(False)


    def sel_tipo_ricerca(self):
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(self.searchType.currentText()))
        lista_completamento = []
        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            lista_completamento = [item.denominazione for item in Immobile.getAllImmobili().values()]
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            lista_completamento = [item.sigla for item in Immobile.getAllImmobili().values()]
        elif self.searchType.currentIndex() == 2:  # ricerca per codice
            lista_completamento = [str(item.codice) for item in Immobile.getAllImmobili().values()]
        print("Lista completamento", lista_completamento)
        self.immobili_completer.setModel(QStringListModel(lista_completamento))
        self.selectioning()

    def go_Gestione_TabelleMillesimali(self):
        search_text = self.searchbar.text()
        immobile = 0
        if search_text:
            if self.searchType.currentIndex() == 0:  # ricerca per denominazione
                immobile = Immobile.ricercaImmobileByDenominazione(search_text)
                print("imm: ", immobile)
            elif self.searchType.currentIndex() == 1:  # ricerca per sigla
                immobile = Immobile.ricercaImmobileBySigla(search_text)
                print("imm: ", immobile)
            elif self.searchType.currentIndex() == 2:  # ricerca per codice
                immobile = Immobile.ricercaImmobileByCodice(search_text)
                print("imm: ", immobile)
        if immobile != None:
            print("si")
            self.vista_gestione_tabellaMillesimale = VistaGestioneTabelleMillesimali(immobile)
            self.vista_gestione_tabellaMillesimale.show()
        else:
            print("no")
            return None

    def go_Gestione_Bilancio(self):
        search_text = self.searchbar.text()
        immobile = 0
        if search_text:
            if self.searchType.currentIndex() == 0:  # ricerca per denominazione
                immobile = Immobile.ricercaImmobileByDenominazione(search_text)
                print("imm: ", immobile)
            elif self.searchType.currentIndex() == 1:  # ricerca per sigla
                immobile = Immobile.ricercaImmobileBySigla(search_text)
                print("imm: ", immobile)
            elif self.searchType.currentIndex() == 2:  # ricerca per codice
                immobile = Immobile.ricercaImmobileByCodice(search_text)
                print("imm: ", immobile)
        if immobile != None:
            print("si")
            self.vista_gestione_bilancio = VistaGestioneEsercizi(immobile)
            self.vista_gestione_bilancio.show()
        else:
            print("no")
            return None