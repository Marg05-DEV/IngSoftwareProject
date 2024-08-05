from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QHBoxLayout, QPushButton, QLabel, \
    QCompleter, QFrame, QSizePolicy

from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaGestioneCondomini import VistaGestioneCondomini
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaGestioneRegistroAnagrafe import VistaGestioneRegistroAnagrafe

class VistaMenuRegistroAnagrafe(QWidget):
    def __init__(self, parent=None):
        print("class VistaMenuRegistroAnagrafe - __init__ inizio")
        print(Immobile.getAllImmobili())

        super(VistaMenuRegistroAnagrafe, self).__init__(parent)

        main_layout = QVBoxLayout()

        completer_list = sorted([item.denominazione for item in Immobile.getAllImmobili().values()])
        print(completer_list)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Immobile")
        self.immobili_completer = QCompleter(completer_list)
        self.immobili_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        print(self.immobili_completer.completionModel())
        self.searchbar.setCompleter(self.immobili_completer)
        self.lbl_search = QLabel("Ricerca l'immobile da selezionare:")
        self.lbl_searchType = QLabel("Ricerca per:")
        self.lbl_search.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.lbl_searchType.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.searchType = QComboBox()
        self.searchType.addItems(["Denominazione", "Sigla", "Codice"])
        self.searchType.activated.connect(self.sel_tipo_ricerca)
        self.immobile_selezionato = QLabel("Nessun immobile selezionato")

        find_layout = QHBoxLayout()
        search_layout = QVBoxLayout()
        type_layout = QVBoxLayout()
        selected_layout = QHBoxLayout()

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

        if not completer_list:
            frase_lbl.setText("Nessun immobile presente")
            self.immobile_selezionato.setVisible(False)

        self.button_layout = QHBoxLayout()

        self.select_button = self.create_button("Seleziona", self.go_Gestione_UnitaImmobiliare, True)
        self.select_button.setMaximumWidth(200)
        self.select_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.button_layout.addWidget(self.create_button("Visualizza tutti i Condomini", self.go_Gestione_Condomino))

        self.searchbar.textChanged.connect(self.selectioning)

        selected_layout.addWidget(self.select_button)
        selected_layout.addLayout(msg_layout)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(selected_layout)
        main_layout.addWidget(self.drawLine())
        main_layout.addLayout(self.button_layout)

        self.setLayout(main_layout)
        self.resize(500, 300)
        self.setWindowTitle("Menu Registro Anagrafe Condominiale")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.setCheckable(False)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        return button
    def drawLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line
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
            self.immobile_selezionato.setText(f"{immobile.codice} - {immobile.sigla} - {immobile.denominazione}")
            self.select_button.setEnabled(True)
        else:
            self.immobile_selezionato.setText("Nessun immobile selezionato")
            self.select_button.setEnabled(False)


    def sel_tipo_ricerca(self):
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(self.searchType.currentText()))
        lista_completamento = []
        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            lista_completamento = sorted([item.denominazione for item in Immobile.getAllImmobili().values()])
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            lista_completamento = sorted([item.sigla for item in Immobile.getAllImmobili().values()])
        elif self.searchType.currentIndex() == 2:  # ricerca per codice
            lista_completamento = sorted([str(item.codice) for item in Immobile.getAllImmobili().values()])
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
                print("imm: ", immobile)
            elif self.searchType.currentIndex() == 1:  # ricerca per sigla
                immobile = Immobile.ricercaImmobileBySigla(search_text)
                print("imm: ", immobile)
            elif self.searchType.currentIndex() == 2:  # ricerca per codice
                immobile = Immobile.ricercaImmobileByCodice(search_text)
                print("imm: ", immobile)
        if immobile != None:
            print("si")
            self.vista_Gestione_UnitaImmobiliare = VistaGestioneRegistroAnagrafe(immobile)
            self.vista_Gestione_UnitaImmobiliare.show()
        else:
            print("no")
            return None

    def go_Gestione_Condomino(self):
        self.vista_Gestione_Condomino = VistaGestioneCondomini()
        self.vista_Gestione_Condomino.show()

