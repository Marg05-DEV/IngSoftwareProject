from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame, QTreeWidget, QTreeWidgetItem

from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.rata import Rata
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile


class VistaCreditoCondomino(QWidget):
    def __init__(self):

        super(VistaCreditoCondomino, self).__init__()
        self.buttons = {}
        self.immobile = None
        self.debito_totale = 0.00
        main_layout = QVBoxLayout()

        find_layout = QGridLayout()
        completer_list = sorted([(item.codiceFiscale, item.nome, item.cognome) for item in Condomino.getAllCondomini().values()])
        print(completer_list)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Condomino")
        self.condomini_completer = QCompleter(completer_list)
        self.condomini_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        print(self.condomini_completer.completionModel())
        self.searchbar.setCompleter(self.condomini_completer)
        """
        self.lbl_search = QLabel("Ricerca fornitore da selezionare:")
        self.lbl_searchType = QLabel("Ricerca per:")
        self.lbl_search.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.lbl_searchType.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.searchType = QComboBox()
        self.searchType.addItems(["Denominazione", "PartitaIva"])
        self.searchType.activated.connect(self.sel_tipo_ricerca)
        """
        self.condomino_selezionato = QLabel("Nessun condomino selezionato")
        """
        find_layout.addWidget(self.lbl_search, 0, 0, 1, 3)
        find_layout.addWidget(self.lbl_searchType, 0, 3)
        """
        find_layout.addWidget(self.searchbar, 1, 0, 1, 3)
        #find_layout.addWidget(self.searchType, 1, 3)
        find_layout.addWidget(QLabel("Stai selezionando: "), 2, 0, 1, 1)
        find_layout.addWidget(self.condomino_selezionato, 2, 1, 1, 3)

        self.button_layout = QHBoxLayout()
        print("u")

        self.button_layout.addWidget(self.create_button("Seleziona", self.view_credito_condomino))
        self.buttons["Seleziona"].setEnabled(False)
        self.searchbar.textChanged.connect(self.selectioning)
        print("c")

        """ ------------------------- FINE SELEZIONE IMMOBILE ----------------------- """
        print("d")
        self.drawLine()
        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(["Condomino", "Importo"])
        self.tree_widget.setVisible(False)

        self.rate_credito_section = {}
        self.rate_a_credito_non_presenti = QLabel("")
        self.rate_a_credito_non_presenti.setStyleSheet("font-weight: bold;")
        self.rate_credito_section["no_rate"] = self.rate_a_credito_non_presenti
        self.rate_credito_section["no_rate"].setVisible(False)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(self.button_layout)
        main_layout.addWidget(self.tree_widget)
        main_layout.addWidget(self.rate_a_credito_non_presenti)

        self.drawLine()

        self.rate_credito_totale_section = {}
        self.rate_totali = QLabel("")
        self.rate_totali.setStyleSheet("font-weight: bold;")
        self.rate_totali_importo = QLabel("")
        self.rate_totali_importo.setStyleSheet("font-weight: bold;")
        self.lbl_rate_totali_importo = QLabel("Debito totale verso il fornitore selezionato")
        self.lbl_rate_totali_importo.setStyleSheet("font-weight: bold;")
        self.rate_credito_totale_section["all_credito_rate"] = self.rate_totali
        self.rate_credito_totale_section["importo_totale"] = self.rate_totali_importo
        self.rate_credito_totale_section["frase_all_credito"] = self.lbl_rate_totali_importo
        self.rate_credito_totale_section["frase_all_credito"].setVisible(False)
        self.rate_credito_totale_section["importo_totale"].setVisible(False)
        self.rate_credito_totale_section["all_credito_rate"].setVisible(False)
        main_layout.addWidget(self.rate_totali)

        credito_totale_layout = QHBoxLayout()
        credito_totale_layout.addWidget(self.lbl_rate_totali_importo)
        credito_totale_layout.addWidget(self.rate_totali_importo)
        main_layout.addLayout(credito_totale_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Credito Condomino")

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
        condomino = None
        print(self.searchbar.text())
        condomino = Condomino.ricercaCondominoByCF(self.searchbar.text())

        if condomino != None:
            self.condomino_selezionato.setText(f"{condomino.nome} - {condomino.cognome}")
            self.buttons["Seleziona"].setEnabled(True)
        else:
            self.condomino_selezionato.setText("Nessun condomino selezionato")
            self.buttons["Seleziona"].setEnabled(False)
    """
    def sel_tipo_ricerca(self):
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(
            self.searchType.currentText()))
        lista_completamento = []
        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            lista_completamento = sorted([item.denominazione for item in Fornitore.getAllFornitore().values()])
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            lista_completamento = sorted([item.partitaIva for item in Fornitore.getAllFornitore().values()])

        self.condomini_completer.setModel(QStringListModel(lista_completamento))
        self.selectioning()
    """

    def view_credito_condomino(self):
        search_text = self.searchbar.text()
        print(f"Testo della barra di ricerca: {search_text}")
        self.condomino = 0
        if search_text:
            self.condomino = Condomino.ricercaCondominoByCF(search_text)

        if self.condomino != None:
            self.tree_widget.setVisible(True)
            self.update_list()
        else:
            print("no")
            return None

    def update_list(self):
        self.credito_totale = 0.00
        self.rate_non_pagate = []
        self.spese_fornitore = Spesa.getAllSpeseByFornitore(self.fornitore)
        for spesa in self.spese_fornitore.values():
            if not spesa.pagata:
                self.spese_non_pagate.append(spesa)
                self.debito_totale += spesa.importo

        print(self.spese_non_pagate)

        if not self.spese_non_pagate:
            self.tree_widget.setVisible(False)
            self.rate_credito_section["no_rate"].setText("Questo condomino non ha credito verso alcun immobile")
            self.rate_credito_section["no_rate"].setVisible(True)
            self.rate_credito_totale_section["frase_all_credito"].setVisible(False)
            self.rate_credito_totale_section["importo_totale"].setVisible(False)

        self.tree_widget.clear()
        list_immobili_con_debito = []
        for immobile in Immobile.getAllImmobili().values():
            for spese in self.spese_non_pagate:
                print("if degli immobili: ", immobile.id == spese.immobile)
                if immobile.id == spese.immobile:
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
            self.rate_credito_totale_section["all_credito_spese"].setVisible(True)
            self.rate_credito_totale_section["frase_all_credito"].setVisible(True)
            self.rate_credito_totale_section["importo_totale"].setText(str("%.2f" % self.debito_totale))
            self.rate_credito_totale_section["importo_totale"].setVisible(True)
