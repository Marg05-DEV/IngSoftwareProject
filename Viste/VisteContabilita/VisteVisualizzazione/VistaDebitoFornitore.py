from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame, QTreeWidget, QTreeWidgetItem

from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.rata import Rata
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.immobile import Immobile


class VistaDebitoFornitore(QWidget):
    def __init__(self):

        super(VistaDebitoFornitore, self).__init__()
        self.buttons = {}
        self.immobile = None
        self.debito_totale = 0.00
        main_layout = QVBoxLayout()


        completer_list = sorted([item.denominazione for item in Fornitore.getAllFornitore().values()])
        print(completer_list)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Fornitore")
        self.fornitori_completer = QCompleter(completer_list)
        self.fornitori_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        print(self.fornitori_completer.completionModel())
        self.searchbar.setCompleter(self.fornitori_completer)
        self.lbl_search = QLabel("Ricerca fornitore da selezionare:")
        self.lbl_searchType = QLabel("Ricerca per:")
        self.lbl_search.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.lbl_searchType.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.searchType = QComboBox()
        self.searchType.addItems(["Denominazione", "PartitaIva"])
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
        self.fornitore_selezionato = QLabel("Nessun fornitore selezionato")

        msg_layout.addWidget(frase_lbl)
        msg_layout.addWidget(self.fornitore_selezionato)

        main_layout.addLayout(msg_layout)

        if not completer_list:
            frase_lbl.setText("Nessun fornitore presente")
            self.fornitore_selezionato.setVisible(False)

        self.button_layout = QHBoxLayout()
        print("u")

        self.button_layout.addWidget(self.create_button("Seleziona", self.view_debito_fornitore))
        self.buttons["Seleziona"].setEnabled(False)
        self.searchbar.textChanged.connect(self.selectioning)
        print("c")

        """ ------------------------- FINE SELEZIONE IMMOBILE ----------------------- """
        print("d")
        self.drawLine()
        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(["Denominazione Immobile", "Importo"])
        self.tree_widget.setVisible(False)

        self.spese_debito_section = {}
        self.spese_a_debito_non_presenti = QLabel("")
        self.spese_a_debito_non_presenti.setStyleSheet("font-weight: bold;")
        self.spese_debito_section["no_spese"] = self.spese_a_debito_non_presenti
        self.spese_debito_section["no_spese"].setVisible(False)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(self.button_layout)
        main_layout.addWidget(self.tree_widget)
        main_layout.addWidget(self.spese_a_debito_non_presenti)

        self.drawLine()

        self.spese_debito_totale_section = {}
        self.spese_totale = QLabel("")
        self.spese_totale.setStyleSheet("font-weight: bold;")
        self.spese_totale_importo = QLabel("")
        self.spese_totale_importo.setStyleSheet("font-weight: bold;")
        self.lbl_spese_totale_importo = QLabel("Debito totale verso il fornitore selezionato")
        self.lbl_spese_totale_importo.setStyleSheet("font-weight: bold;")
        self.spese_debito_totale_section["all_debito_spese"] = self.spese_totale
        self.spese_debito_totale_section["importo_totale"] = self.spese_totale_importo
        self.spese_debito_totale_section["frase_all_debito"] = self.lbl_spese_totale_importo
        self.spese_debito_totale_section["frase_all_debito"].setVisible(False)
        self.spese_debito_totale_section["importo_totale"].setVisible(False)
        self.spese_debito_totale_section["all_debito_spese"].setVisible(False)
        main_layout.addWidget(self.spese_totale)

        debito_totale_layout = QHBoxLayout()
        debito_totale_layout.addWidget(self.lbl_spese_totale_importo)
        debito_totale_layout.addWidget(self.spese_totale_importo)
        main_layout.addLayout(debito_totale_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Debito Fornitore")

    def drawLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setFixedSize(275, 55)
        button.setCheckable(False)
        button.clicked.connect(action)
        self.buttons[testo] = button
        return button

    def selectioning(self):
        fornitore = None

        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            fornitore = Fornitore.ricercaFornitoreByDenominazione(self.searchbar.text())
            print("imm: ", fornitore)
        elif self.searchType.currentIndex() == 1:  # ricerca per partita iva
            fornitore = Fornitore.ricercaFornitoreByPartitaIVA(self.searchbar.text())
            print("imm: ", fornitore)

        if fornitore != None:
            self.fornitore_selezionato.setText(f"{fornitore.denominazione} - {fornitore.partitaIva}")
            self.buttons["Seleziona"].setEnabled(True)
        else:
            self.fornitore_selezionato.setText("Nessun fornitore selezionato")
            self.buttons["Seleziona"].setEnabled(False)

    def sel_tipo_ricerca(self):
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(
            self.searchType.currentText()))
        lista_completamento = []
        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            lista_completamento = sorted([item.denominazione for item in Fornitore.getAllFornitore().values()])
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            lista_completamento = sorted([item.partitaIva for item in Fornitore.getAllFornitore().values()])

        self.fornitori_completer.setModel(QStringListModel(lista_completamento))
        self.selectioning()

    def view_debito_fornitore(self):
        search_text = self.searchbar.text()
        print(f"Testo della barra di ricerca: {search_text}")
        self.fornitore = 0
        if search_text:
            print("sto cercando...")
            if self.searchType.currentIndex() == 0:  # ricerca per denominazione
                self.fornitore = Fornitore.ricercaFornitoreByDenominazione(search_text)
                print("imm: ", self.fornitore)
            elif self.searchType.currentIndex() == 1:  # ricerca per sigla
                self.fornitore = Fornitore.ricercaFornitoreByPartitaIVA(search_text)
                print("imm: ", self.fornitore)

        if self.fornitore != None:
            self.tree_widget.setVisible(True)
            self.update_list()
        else:
            print("no")
            return None

    def update_list(self):
        self.debito_totale = 0.00
        self.spese_non_pagate = []
        self.spese_fornitore = Spesa.getAllSpeseByFornitore(self.fornitore)
        for spesa in self.spese_fornitore.values():
            if not spesa.pagata:
                self.spese_non_pagate.append(spesa)
                self.debito_totale += spesa.importo

        print(self.spese_non_pagate)

        if not self.spese_non_pagate:
            self.tree_widget.setVisible(False)
            self.spese_debito_section["no_spese"].setText("Non ci sono debiti con questo fornitore")
            self.spese_debito_section["no_spese"].setVisible(True)
            self.spese_debito_totale_section["frase_all_debito"].setVisible(False)
            self.spese_debito_totale_section["importo_totale"].setVisible(False)

        self.tree_widget.clear()
        list_immobili_con_debito = []
        for immobile in Immobile.getAllImmobili().values():
            for spese in self.spese_non_pagate:
                print("if degli immobili: ", immobile.id == spese.immobile)
                if immobile.id == spese.immobile:
                    if immobile not in list_immobili_con_debito:
                        list_immobili_con_debito.append(immobile)

        print("immobili: ", list_immobili_con_debito)
        for immobile in list_immobili_con_debito:
            importo_debito_immobile = 0.00
            for spesa in self.spese_non_pagate:
                if spesa.immobile == immobile.id:
                    importo_debito_immobile += spesa.importo
            item = QTreeWidgetItem([immobile.denominazione, str("%.2f" % importo_debito_immobile)])
            for spese_debito in self.spese_non_pagate:
                print(immobile.id)
                if spese_debito.immobile == immobile.id:
                    child = QTreeWidgetItem([spese_debito.descrizione, str("%.2f" % spese_debito.importo)])
                    item.addChild(child)
            self.tree_widget.addTopLevelItem(item)

        for i in range(self.tree_widget.columnCount()):
            print(i)
            self.tree_widget.resizeColumnToContents(i)

        if self.spese_non_pagate:
            self.spese_debito_section["no_spese"].setVisible(False)
            self.spese_debito_totale_section["all_debito_spese"].setVisible(True)
            self.spese_debito_totale_section["frase_all_debito"].setVisible(True)
            self.spese_debito_totale_section["importo_totale"].setText(str("%.2f" % self.debito_totale))
            self.spese_debito_totale_section["importo_totale"].setVisible(True)
