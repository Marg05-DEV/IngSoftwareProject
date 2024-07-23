from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame

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
        self.searchbar.textChanged.connect(self.selectioning)
        print("c")
        spesa_layout = QVBoxLayout()
        self.lbl_frase = QLabel("Spese:")
        self.lbl_frase.setFixedSize(self.lbl_frase.sizeHint())
        self.list_view_spese = QListView()
        self.list_view_spese.setAlternatingRowColors(True)
        self.lbl_frase.setVisible(False)
        self.list_view_spese.setVisible(False)
        spesa_layout.addWidget(self.lbl_frase)
        spesa_layout.addWidget(self.list_view_spese)
        print("d")
        spesa_layout.addWidget(self.newLabel("Debito verso fornitori dell'immobile", True))
        print("e")

        rata_layout = QVBoxLayout()
        self.lbl_frase1 = QLabel("Rate:")
        self.lbl_frase1.setFixedSize(self.lbl_frase1.sizeHint())
        self.list_view_rate = QListView()
        self.list_view_rate.setAlternatingRowColors(True)
        self.lbl_frase1.setVisible(False)
        self.list_view_rate.setVisible(False)
        rata_layout.addWidget(self.lbl_frase1)
        rata_layout.addWidget(self.list_view_rate)
        rata_layout.addWidget(self.newLabel("credito verso condomini dell'immobile", False))

        main_layout.addLayout(find_layout)
        main_layout.addLayout(self.button_layout)
        main_layout.addLayout(spesa_layout)
        main_layout.addLayout(rata_layout)
        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

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
    def newLabel(self, testo, isSpesa):
        print("qui")
        label = QLabel("")
        if self.immobile != None:
            print(self.immobile)
            print("xaxa")
            self.speseByImmobile = Spesa.getAllSpeseByImmobile(self.immobile)
            print("xuxu")
            self.rateByImmobile = Rata.getAllRateByImmobile(self.immobile)
            print("xixi")
            importo_totale = 0.0
            if isSpesa:
                print("dentro")
                print(self.speseByImmobile.values())
                for spesa in self.speseByImmobile.values():
                    print(spesa.importo)
                    if not spesa.pagata:
                      importo_totale += spesa.importo
                print(importo_totale)
            else:
                for rata in self.rateByImmobile.values():
                    if not rata.pagata:
                        importo_totale += rata.importo
            label = QLabel(testo + "....." + importo_totale)
        print("quo")
        return label
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
        print(self.immobile)
        self.rate = Rata.getAllRateByImmobile(self.immobile)
        self.spese = Spesa.getAllSpeseByImmobile(self.immobile)
        if not self.rate:
            self.msg.setText("Non ci sono rate per questo immobile")
            self.msg.show()
        if not self.spese:
            self.msg.setText("Non ci sono sepse per questo immobile")
            self.msg.show()
        spesa_non_pagata = False
        rata_non_pagata = False

        listview_model = QStandardItemModel(self.list_view_spese)
        for spesa in self.spese.values():
            item = QStandardItem()
            non_pagata = ""
            tipoSpesa = TipoSpesa.ricercaTipoSpesaByCodice(spesa.tipoSpesa)
            if not spesa.pagata:
                non_pagata = "La spesa non è stata pagata"
                item_text = f"{tipoSpesa.nome}: {non_pagata}"
                item.setText(item_text)
                item.setEditable(False)
                font = item.font()
                font.setPointSize(12)
                item.setFont(font)
                listview_model.appendRow(item)
                spesa_non_pagata = True

        print("qui finisce")
        self.list_view_spese.setModel(listview_model)
        if spesa_non_pagata:
            self.lbl_frase.setVisible(True)
            self.list_view_spese.setVisible(True)


        listview_model1 = QStandardItemModel(self.list_view_rate)
        for rata in self.rate.values():
            item = QStandardItem()
            non_versata = ""
            if not rata.pagata:
                non_versata = "non versata"
                item_text = f"La Rata {rata.numeroRicevuta} risulta {non_versata}"
                item.setText(item_text)
                item.setEditable(False)
                font = item.font()
                font.setPointSize(12)
                item.setFont(font)
                listview_model1.appendRow(item)
                rata_non_pagata = True


        print("qui finisce")
        self.list_view_rate.setModel(listview_model1)
        if rata_non_pagata:
            self.lbl_frase1.setVisible(True)
            self.list_view_rate.setVisible(True)

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.rate:
            self.msg.setText("Non ci sono rate per questo immobile")
            self.msg.show()
        if not self.spese:
            self.msg.setText("Non ci sono sepse per questo immobile")
            self.msg.show()