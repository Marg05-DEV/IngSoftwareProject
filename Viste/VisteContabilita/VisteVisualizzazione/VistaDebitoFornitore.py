from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame

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

        find_layout = QGridLayout()
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
        self.fornitore_selezionato = QLabel("Nessun fornitore selezionato")

        find_layout.addWidget(self.lbl_search, 0, 0, 1, 3)
        find_layout.addWidget(self.lbl_searchType, 0, 3)
        find_layout.addWidget(self.searchbar, 1, 0, 1, 3)
        find_layout.addWidget(self.searchType, 1, 3)
        find_layout.addWidget(QLabel("Stai selezionando: "), 2, 0, 1, 1)
        find_layout.addWidget(self.fornitore_selezionato, 2, 1, 1, 3)

        self.button_layout = QHBoxLayout()
        print("u")

        self.button_layout.addWidget(self.create_button("Seleziona", self.view_debito_fornitore))
        self.buttons["Seleziona"].setEnabled(False)
        self.searchbar.textChanged.connect(self.selectioning)
        print("c")

        """ ------------------------- FINE SELEZIONE IMMOBILE ----------------------- """
        print("d")
        self.drawLine()
        print("e")
        self.spese_section = {}
        self.debito_fornitore_totale = {}
        spesa_layout = QVBoxLayout()
        self.lbl_frase = QLabel("Spese:")
        self.lbl_frase.setFixedSize(self.lbl_frase.sizeHint())
        self.list_view_spese = QListView()
        self.list_view_spese.setAlternatingRowColors(True)
        self.error_no_spese = QLabel("")
        self.error_no_spese.setStyleSheet("font-weight: bold;")
        self.spese_section["frase"] = self.lbl_frase
        self.spese_section["lista_spese"] = self.list_view_spese
        self.spese_section["no_spese"] = self.error_no_spese
        self.spese_section["no_spese"].setVisible(False)
        spesa_layout.addWidget(self.lbl_frase)
        spesa_layout.addWidget(self.list_view_spese)
        spesa_layout.addWidget(self.error_no_spese)

        totale_spese_layout = QHBoxLayout()
        lbl_frase_totale_spese = QLabel("Debito dell'immobile")
        lbl_totale_spese = QLabel("0.00")

        self.spese_section["frase_totale"] = lbl_frase_totale_spese
        self.spese_section["totale"] = lbl_totale_spese
        totale_spese_layout.addWidget(lbl_frase_totale_spese)
        totale_spese_layout.addWidget(lbl_totale_spese)
        spesa_layout.addLayout(totale_spese_layout)

        for widget in self.spese_section.values():
            widget.setVisible(False)

        debito_totale_layout = QHBoxLayout()
        frase_debito = QLabel("Debito verso il fornitore selezionato")
        totale_debito = QLabel("0.00")
        self.debito_fornitore_totale["frase_debito_totale"] = frase_debito
        self.debito_fornitore_totale["totale_debito"] = totale_debito
        debito_totale_layout.addWidget(frase_debito)
        debito_totale_layout.addWidget(totale_debito)

        for widget in self.debito_fornitore_totale.values():
            widget.setVisible(False)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(self.button_layout)
        main_layout.addLayout(spesa_layout)
        self.drawLine()
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
            self.fornitore_selezionato.setText(f"{fornitore.codice} - {fornitore.denominazione} - {fornitore.partitaIva}")
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
            """
            for immobile in Immobile.getAllImmobili().values():
                for spesa in Spesa.getAllSpeseByImmobile(immobile):
                    if spesa.fornitore.codice == self.fornitore.codice:
            """
            self.update_list()
        else:
            print("no")
            return None

    def update_list(self):
        importo_totale = 0.00
        print("inizio")

        self.spesa_debito = [item for item in Spesa.getAllSpeseByFornitore(self.fornitore).values() if not item.pagata]

        for spese in self.spesa_debito:
            self.debito_totale += spese.importo
        if self.spesa_debito:
            self.debito_fornitore_totale["frase_debito_totale"].setVisible(True)
            self.debito_fornitore_totale["totale_debito"].setText(str("%.2f" % self.debito_totale))
            self.debito_fornitore_totale["totale_debito"].setVisible(True)
        print("rata:", self.spesa_debito)
        if not self.spesa_debito:
            self.spese_section["lista_spese"].setVisible(False)
            self.spese_section["totale"].setVisible(False)
            self.spese_section["frase_totale"].setVisible(False)
            self.debito_fornitore_totale["frase_debito_totale"].setVisible(False)
            self.debito_fornitore_totale["totale_debito"].setVisible(False)

            self.spese_section["no_spese"].setText("Non ci sono spese a debito per questo fornitore")
            self.spese_section["no_spese"].setVisible(True)

        for immobile in Immobile.getAllImmobili().values():
            for spese_a_debito_per_immobile in Spesa.getAllSpeseByImmobile(immobile).values():
                listview_model = QStandardItemModel(self.list_view_spese)
                for spesa in self.spesa_debito:
                    item = QStandardItem()
                    if not spesa.pagata and spesa.immobile == spese_a_debito_per_immobile.codice:
                        importo = str("%.2f" % spesa.importo)
                        item_text = f"{importo}€ verso {Fornitore.ricercaFornitoreByCodice(spesa.fornitore).denominazione}"
                        item.setText(item_text)
                        item.setEditable(False)
                        font = item.font()
                        font.setPointSize(12)
                        item.setFont(font)
                        listview_model.appendRow(item)

                print("spese fatee in list -....")
                self.list_view_spese.setModel(listview_model)
                if self.spesa_debito:
                    for spesa in self.spesa_debito:
                        if not spesa.pagata and spesa.immobile == spese_a_debito_per_immobile.codice:
                            importo_totale += spesa.importo
                    self.spese_section["totale"].setText(str("%.2f" % importo_totale))
                    for spese in self.spese_section.values():
                        spese.setVisible(True)

    def saldo(self, testo):
        label = QLabel(testo + " ..... " + str("%.2f" % self.debito_totale))
        return label
