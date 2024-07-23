from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame

from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.rata import Rata
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.immobile import Immobile


class VistaStatoPatrimoniale(QWidget):
    def __init__(self):
        print("class VistaMenuRegistroAnagrafe - __init__ inizio")
        print(Immobile.getAllImmobili())

        super(VistaStatoPatrimoniale, self).__init__()
        self.buttons = {}
        self.immobile = None
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
        print("u")

        self.button_layout.addWidget(self.create_button("Seleziona", self.view_stato_patrimoniale))
        self.buttons["Seleziona"].setEnabled(False)
        self.searchbar.textChanged.connect(self.selectioning)
        print("c")

        """ ------------------------- FINE SELEZIONE IMMOBILE ----------------------- """
        """ ------------------------------ SEZIONE SPESE ---------------------------- """

        self.spese_section = {}
        print("che cazzo vuoi")
        spesa_layout = QVBoxLayout()
        self.lbl_frase = QLabel("Spese:")
        self.lbl_frase.setFixedSize(self.lbl_frase.sizeHint())
        self.list_view_spese = QListView()
        self.list_view_spese.setAlternatingRowColors(True)
        self.spese_section["frase"] = self.lbl_frase
        self.spese_section["lista_spese"] = self.list_view_spese

        spesa_layout.addWidget(self.lbl_frase)
        spesa_layout.addWidget(self.list_view_spese)

        totale_spese_layout = QHBoxLayout()
        lbl_frase_totale_spese = QLabel("Debito verso fornitori dell'immobile")
        lbl_totale_spese = QLabel("0.00")

        self.spese_section["frase_totale"] = lbl_frase_totale_spese
        self.spese_section["totale"] = lbl_totale_spese
        totale_spese_layout.addWidget(lbl_frase_totale_spese)
        totale_spese_layout.addWidget(lbl_totale_spese)
        spesa_layout.addLayout(totale_spese_layout)

        """ ------------------------------ SEZIONE RATE ---------------------------- """

        self.rate_section = {}

        rata_layout = QVBoxLayout()
        self.lbl_frase1 = QLabel("Rate:")
        self.lbl_frase1.setFixedSize(self.lbl_frase1.sizeHint())
        self.list_view_rate = QListView()
        self.list_view_rate.setAlternatingRowColors(True)
        self.rate_section["frase"] = self.lbl_frase1
        self.rate_section["lista_rate"] = self.list_view_rate
        rata_layout.addWidget(self.lbl_frase1)
        rata_layout.addWidget(self.list_view_rate)

        totale_rate_layout = QHBoxLayout()
        lbl_frase_totale_rate = QLabel("Credito verso condomini dell'immobile")
        lbl_totale_rate = QLabel("0.00")

        self.rate_section["frase_totale"] = lbl_frase_totale_rate
        self.rate_section["totale"] = lbl_totale_rate
        totale_rate_layout.addWidget(lbl_frase_totale_rate)
        totale_rate_layout.addWidget(lbl_totale_rate)
        rata_layout.addLayout(totale_rate_layout)

        for widget in self.rate_section.values():
            widget.setVisible(False)

        for widget in self.spese_section.values():
            widget.setVisible(False)

        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(self.button_layout)
        main_layout.addLayout(spesa_layout)
        self.drawLine()
        main_layout.addLayout(rata_layout)
        main_layout.addWidget(self.msg)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Stato Patrimoniale")

    def drawLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

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
        self.immobile = 0
        if search_text:
            print("sto cercando...")
            if self.searchType.currentIndex() == 0:  # ricerca per denominazione
                self.immobile = Immobile.ricercaImmobileByDenominazione(search_text)
                print("imm: ", self.immobile)
            elif self.searchType.currentIndex() == 1:  # ricerca per sigla
                self.immobile = Immobile.ricercaImmobileBySigla(search_text)
                print("imm: ", self.immobile)
            elif self.searchType.currentIndex() == 2:  # ricerca per codice
                self.immobile = Immobile.ricercaImmobileByCodice(search_text)
                print("imm: ", self.immobile)
        if self.immobile != None:
            self.update_list()
        else:
            print("no")
            return None

    def update_list(self):
        importo_totale = 0.00
        print("inizio")

        self.rate = [item for item in Rata.getAllRateByImmobile(self.immobile).values() if not item.pagata]
        self.spese = [item for item in Spesa.getAllSpeseByImmobile(self.immobile).values() if not item.pagata]
        print("rata:", self.rate)
        print("spesa", self.spese)
        if not self.spese and not self.rate:
            self.msg.setText("Non ci sono nè spese nè rate per questo immobile")
            self.msg.show()
        elif not self.rate:
            self.msg.setText("Non ci sono rate per questo immobile")
            self.msg.show()
        elif not self.spese:
            self.msg.setText("Non ci sono spese per questo immobile")
            self.msg.show()

        listview_model = QStandardItemModel(self.list_view_spese)
        for spesa in self.spese:
            item = QStandardItem()
            if not spesa.pagata:
                importo = str("%.2f" % spesa.importo)
                item_text = f"{importo} verso {Fornitore.ricercaFornitoreByCodice(spesa.fornitore).denominazione}"
                item.setText(item_text)
                item.setEditable(False)
                font = item.font()
                font.setPointSize(12)
                item.setFont(font)
                listview_model.appendRow(item)

        print("spese fatee in list -....")
        self.list_view_spese.setModel(listview_model)
        if self.list_view_spese:
            for spesa in self.spese:
                if not spesa.pagata:
                    importo_totale += spesa.importo
            self.spese_section["totale"].setText(str("%.2f" % importo_totale))
            for spese in self.spese_section.values():
                spese.setVisible(True)

        listview_model1 = QStandardItemModel(self.list_view_rate)
        for rata in self.rate:
            item = QStandardItem()
            if not rata.pagata:
                importo = str("%.2f" % rata.importo)
                item_text = f"{importo}"
                item.setText(item_text)
                item.setEditable(False)
                font = item.font()
                font.setPointSize(12)
                item.setFont(font)
                listview_model1.appendRow(item)

        importo_totale = 0.00
        print("qui finisce")
        self.list_view_rate.setModel(listview_model1)
        if self.list_view_rate:
            for rata in self.rate:
                if not rata.pagata:
                    importo_totale += rata.importo
            self.rate_section["totale"].setText(str("%.2f" % importo_totale))
            for rate in self.rate_section.values():
                rate.setVisible(True)

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.spese and not self.rate:
            self.msg.setText("Non ci sono nè spese nè rate per questo immobile")
            self.msg.show()
        elif not self.rate:
            self.msg.setText("Non ci sono rate per questo immobile")
            self.msg.show()
        elif not self.spese:
            self.msg.setText("Non ci sono spese per questo immobile")
            self.msg.show()
