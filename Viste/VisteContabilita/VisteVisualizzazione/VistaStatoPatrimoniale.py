from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView

from Classes.RegistroAnagrafe.immobile import Immobile


class VistaStatoPatrimoniale(QWidget):
    def __init__(self):
        print("class VistaMenuRegistroAnagrafe - __init__ inizio")
        print(Immobile.getAllImmobili())

        super(VistaStatoPatrimoniale, self).__init__()
        self.buttons = {}
        main_layout = QVBoxLayout()

        find_layout = QGridLayout()
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

        find_layout.addWidget(self.lbl_search, 0, 0, 1, 3)
        find_layout.addWidget(self.lbl_searchType, 0, 3)
        find_layout.addWidget(self.searchbar, 1, 0, 1, 3)
        find_layout.addWidget(self.searchType, 1, 3)
        find_layout.addWidget(QLabel("Stai selezionando: "), 2, 0, 1, 1)
        find_layout.addWidget(self.immobile_selezionato, 2, 1, 1, 3)

        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.create_button("Seleziona", self.view_stato_patrimoniale))

        self.searchbar.textChanged.connect(self.selectioning)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(self.button_layout)

        if self.view_stato_patrimoniale():
            lbl_frase = QLabel("Spese:")
            lbl_frase.setStyleSheet("font-weight: bold;")
            lbl_frase.setFixedSize(lbl_frase.sizeHint())

            main_layout.addWidget(lbl_frase)
            spese_layout = QHBoxLayout()
            self.list_view_spese = QListView()
            self.list_view_spese.setAlternatingRowColors(True)
            spese_layout.addWidget(self.list_view_spese)

            lbl_frase1 = QLabel("Rate:")
            lbl_frase1.setStyleSheet("font-weight: bold;")
            main_layout.addWidget(lbl_frase1)

            rate_layout = QHBoxLayout()

            self.list_view_rate = QListView()
            self.list_view_rate.setAlternatingRowColors(True)
            rate_layout.addWidget(self.list_view_rate)
            self.update_list()
            self.msg = QLabel("")
            self.msg.setStyleSheet("color: red; font-weight: bold;")
            self.msg.hide()

            self.timer = QTimer(self)
            self.timer.setInterval(5000)
            self.timer.timeout.connect(self.hide_message)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Stato Patrimoniale")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setFixedSize(275, 55)
        button.setCheckable(True)
        button.clicked.connect(action)
        self.buttons[testo] = button
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
            self.immobile_selezionato.setText(f"{immobile.codice} - {immobile.sigla} - {immobile.denominazione}")
            self.buttons["Seleziona"].setEnabled(True)
        else:
            self.immobile_selezionato.setText("Nessun immobile selezionato")
            self.buttons["Seleziona"].setEnabled(False)

    def sel_tipo_ricerca(self):
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(
            self.searchType.currentText()))
        lista_completamento = []
        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            lista_completamento = sorted([item.denominazione for item in Immobile.getAllImmobili().values()])
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            lista_completamento = sorted([item.sigla for item in Immobile.getAllImmobili().values()])
        elif self.searchType.currentIndex() == 2:  # ricerca per codice
            lista_completamento = sorted([str(item.codice) for item in Immobile.getAllImmobili().values()])
        self.immobili_completer.setModel(QStringListModel(lista_completamento))
        self.selectioning()

    def view_stato_patrimoniale(self):
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
            return True
        else:
            print("no")
            return None

    def update_list(self):
        self.rate = Rata.get

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.sel_unitaImmobiliare.condomini:
            self.msg.setText("Non ci sono condomini assegnati all'unità immobiliare")
            self.msg.show()