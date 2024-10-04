from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QTreeWidget, \
    QTreeWidgetItem

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.rata import Rata
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaStatoPatrimoniale(QWidget):
    def __init__(self):
        super(VistaStatoPatrimoniale, self).__init__()
        self.buttons = {}
        self.immobile = None
        self.lines = []
        main_layout = QVBoxLayout()
        cont = 0

        completer_list = sorted([item.denominazione for item in Immobile.getAllImmobili().values()])
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Immobile")
        self.immobili_completer = QCompleter(completer_list)
        self.immobili_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.searchbar.setCompleter(self.immobili_completer)
        self.lbl_search = QLabel("Ricerca l'immobile da selezionare:")
        self.lbl_searchType = QLabel("Ricerca per:")
        self.lbl_search.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.lbl_searchType.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.searchType = QComboBox()
        self.searchType.addItems(["Denominazione", "Sigla", "Codice"])
        self.searchType.activated.connect(self.sel_tipo_ricerca)

        find_layout = QHBoxLayout()

        search_layout = QVBoxLayout()
        type_layout = QVBoxLayout()

        search_layout.addWidget(self.lbl_search)
        search_layout.addWidget(self.searchbar)
        type_layout.addWidget(self.lbl_searchType)
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
        cont += 1
        print(str(cont))
        self.button_layout.addWidget(self.create_button("Seleziona", self.view_stato_patrimoniale))
        self.buttons["Seleziona"].setDisabled(True)
        self.searchbar.textChanged.connect(self.selectioning)
        main_layout.addLayout(self.button_layout)

        self.spese_section = {}
        spesa_layout = QVBoxLayout()
        self.lbl_frase = QLabel("Spese:")
        self.lbl_frase.setFixedSize(self.lbl_frase.sizeHint())
        self.tree_spese = QTreeWidget()
        self.tree_spese.setColumnCount(2)
        self.tree_spese.setHeaderLabels(["Fornitore/Spesa", "Importo"])
        self.tree_spese.setVisible(False)
        self.error_no_spese = QLabel("")
        self.error_no_spese.setStyleSheet("font-weight: bold;")
        self.spese_section["frase"] = self.lbl_frase
        self.spese_section["lista_spese"] = self.tree_spese
        self.spese_section["no_spese"] = self.error_no_spese
        self.spese_section["no_spese"].setVisible(False)
        spesa_layout.addWidget(self.lbl_frase)
        spesa_layout.addWidget(self.tree_spese)
        spesa_layout.addWidget(self.error_no_spese)
        cont += 1
        print(str(cont))
        totale_spese_layout = QHBoxLayout()
        lbl_frase_totale_spese = QLabel("Debito verso fornitori dell'immobile")
        lbl_totale_spese = QLabel("0.00")

        self.spese_section["frase_totale"] = lbl_frase_totale_spese
        self.spese_section["totale"] = lbl_totale_spese
        totale_spese_layout.addWidget(lbl_frase_totale_spese)
        totale_spese_layout.addWidget(lbl_totale_spese)
        spesa_layout.addLayout(totale_spese_layout)

        self.rate_section = {}

        rata_layout = QVBoxLayout()
        self.lbl_frase1 = QLabel("Rate:")
        self.lbl_frase1.setFixedSize(self.lbl_frase1.sizeHint())
        self.table_rate = QTableWidget()
        self.error_no_rate = QLabel("")
        self.error_no_rate.setStyleSheet("font-weight: bold;")
        self.rate_section["frase"] = self.lbl_frase1
        self.rate_section["lista_rate"] = self.table_rate
        self.rate_section["no_rate"] = self.error_no_rate
        self.rate_section["no_rate"].setVisible(False)
        rata_layout.addWidget(self.lbl_frase1)
        rata_layout.addWidget(self.table_rate)
        rata_layout.addWidget(self.error_no_rate)

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

        self.lines.append(self.drawLine())
        self.lines.append(self.drawLine())

        for line in self.lines:
            line.setVisible(False)
        main_layout.addWidget(self.lines[0])
        main_layout.addLayout(spesa_layout)
        main_layout.addWidget(self.lines[1])
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
        button.setCheckable(False)
        button.clicked.connect(action)
        self.buttons[testo] = button
        return button

    def selectioning(self):
        immobile = None

        if self.searchType.currentIndex() == 0:  # ricerca per denominazione
            immobile = Immobile.ricercaImmobileByDenominazione(self.searchbar.text())
        elif self.searchType.currentIndex() == 1:  # ricerca per sigla
            immobile = Immobile.ricercaImmobileBySigla(self.searchbar.text())
        elif self.searchType.currentIndex() == 2:  # ricerca per codice
            immobile = Immobile.ricercaImmobileByCodice(self.searchbar.text())

        if immobile != None:
            self.immobile_selezionato.setText(f"{immobile.codice} - {immobile.sigla} - {immobile.denominazione}")
            self.buttons["Seleziona"].setDisabled(False)
        else:
            self.immobile_selezionato.setText("Nessun immobile selezionato")
            self.buttons["Seleziona"].setDisabled(True)

    def sel_tipo_ricerca(self):
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
        self.immobile = 0
        if search_text:
            if self.searchType.currentIndex() == 0:  # ricerca per denominazione
                self.immobile = Immobile.ricercaImmobileByDenominazione(search_text)
            elif self.searchType.currentIndex() == 1:  # ricerca per sigla
                self.immobile = Immobile.ricercaImmobileBySigla(search_text)
            elif self.searchType.currentIndex() == 2:  # ricerca per codice
                self.immobile = Immobile.ricercaImmobileByCodice(search_text)
        if self.immobile != None:
            for line in self.lines:
                line.setVisible(True)
            self.update_list()
        else:
            return None

    def update_list(self):
        print("dentro update")
        self.spese = [item for item in Spesa.getAllSpeseByImmobile(self.immobile).values() if not item.pagata]
        spese_per_fornitore = {}

        for spesa in self.spese:
            if spesa.fornitore not in spese_per_fornitore:
                spese_per_fornitore[spesa.fornitore] = {}
            spese_per_fornitore[spesa.fornitore][spesa.codice] = spesa.importo

        for cod_fornitore in spese_per_fornitore.keys():
            fornitore = Fornitore.ricercaFornitoreByCodice(cod_fornitore)
            item = QTreeWidgetItem([fornitore.denominazione, str("%.2f" % sum(spese_per_fornitore[cod_fornitore].values()))])
            for cod_spesa, importo in spese_per_fornitore[cod_fornitore].items():
                spesa = Spesa.ricercaSpesaByCodice(cod_spesa)
                child = child = QTreeWidgetItem([spesa.descrizione, str("%.2f" % importo)])
                item.addChild(child)
            self.tree_spese.addTopLevelItem(item)

        self.tree_spese.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tree_spese.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        if self.spese:
            self.spese_section["totale"].setText(str("%.2f" % sum([sum(item.values()) for item in spese_per_fornitore.values()])))
            print(self.spese_section)
            for spese in self.spese_section.values():
                spese.setVisible(True)
            self.spese_section["no_spese"].setVisible(False)

        rate_da_versare_per_unita = {}
        last_bilancio = Bilancio.getLastBilancio(self.immobile)

        for unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values():
            totale_versato = 0.0
            if last_bilancio:
                for rata in Rata.getAllRateByUnitaImmobiliare(unita_immobiliare).values():
                    if rata.dataPagamento >= last_bilancio.dataApprovazione and rata.importo >= 0.0:
                        totale_versato += rata.importo
                rate_da_versare_per_unita[unita_immobiliare.codice] = last_bilancio.importiDaVersare[unita_immobiliare.codice] - totale_versato
            else:
                rate_da_versare_per_unita[unita_immobiliare.codice] = 0.0

        self.table_rate.setColumnCount(2)
        self.table_rate.setRowCount(len(rate_da_versare_per_unita))

        self.table_rate.setHorizontalHeaderItem(0, QTableWidgetItem("Unità Immobiliare"))
        self.table_rate.setHorizontalHeaderItem(1, QTableWidgetItem("Importo"))

        i = 0
        for cod_unita, importo in rate_da_versare_per_unita.items():
            unita_immobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(cod_unita)
            if importo > 0.0:
                proprietario = [item for item in unita_immobiliare.condomini.keys() if unita_immobiliare.condomini[item] == "Proprietario"]
                if unita_immobiliare.tipoUnitaImmobiliare == "Appartamento":
                    if unita_immobiliare.condomini:
                        if proprietario:
                            proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                            item_text = f"{unita_immobiliare.tipoUnitaImmobiliare} Scala {unita_immobiliare.scala} Int.{unita_immobiliare.interno} di {proprietario.cognome} {proprietario.nome}"
                        else:
                            item_text = f"{unita_immobiliare.tipoUnitaImmobiliare} Scala {unita_immobiliare.scala} Int.{unita_immobiliare.interno} di Nessun Proprietario"
                    else:
                        item_text = f"{unita_immobiliare.tipoUnitaImmobiliare} Scala {unita_immobiliare.scala} Int.{unita_immobiliare.interno} con Nessun Condomino"
                else:
                    if unita_immobiliare.condomini:
                        if proprietario:
                            proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                            item_text = f"{unita_immobiliare.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"
                        else:
                            item_text = f"{unita_immobiliare.tipoUnitaImmobiliare} di Nessun Proprietario"
                    else:
                        item_text = f"{unita_immobiliare.tipoUnitaImmobiliare} con Nessun Condomino"

                self.table_rate.setItem(i, 0, QTableWidgetItem(item_text))
                self.table_rate.setItem(i, 1, QTableWidgetItem(importo))
            i += 1

        importo_totale = sum(rate_da_versare_per_unita.values())

        if rate_da_versare_per_unita and importo_totale:
            self.rate_section["totale"].setText(str("%.2f" % importo_totale))
            for rate in self.rate_section.values():
                rate.setVisible(True)
            self.rate_section["no_rate"].setVisible(False)

        self.table_rate.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_rate.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.table_rate.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_rate.verticalHeader().setVisible(False)

        if not self.spese:
            self.spese_section["lista_spese"].setVisible(False)
            self.spese_section["totale"].setVisible(False)
            self.spese_section["frase_totale"].setVisible(False)
            self.spese_section["no_spese"].setText("Non ci sono spese per questo immobile")
            self.spese_section["no_spese"].setVisible(True)

        if not rate_da_versare_per_unita or not importo_totale:
            self.rate_section["lista_rate"].setVisible(False)
            self.rate_section["totale"].setVisible(False)
            self.rate_section["frase_totale"].setVisible(False)
            self.rate_section["no_rate"].setText("Non ci sono rate da versare per questo immobile")
            self.rate_section["no_rate"].setVisible(True)
