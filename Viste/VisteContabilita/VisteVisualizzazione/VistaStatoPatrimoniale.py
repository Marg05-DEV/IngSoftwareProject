from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView

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

        self.button_layout.addWidget(self.create_button("Seleziona", self.view_stato_patrimoniale))
        self.buttons["Seleziona"].setDisabled(True)
        self.searchbar.textChanged.connect(self.selectioning)
        main_layout.addLayout(self.button_layout)

        self.spese_section = {}
        spesa_layout = QVBoxLayout()
        self.lbl_frase = QLabel("Spese:")
        self.lbl_frase.setFixedSize(self.lbl_frase.sizeHint())
        self.table_spese = QTableWidget()
        self.error_no_spese = QLabel("")
        self.error_no_spese.setStyleSheet("font-weight: bold;")
        self.spese_section["frase"] = self.lbl_frase
        self.spese_section["lista_spese"] = self.table_spese
        self.spese_section["no_spese"] = self.error_no_spese
        self.spese_section["no_spese"].setVisible(False)
        spesa_layout.addWidget(self.lbl_frase)
        spesa_layout.addWidget(self.table_spese)
        spesa_layout.addWidget(self.error_no_spese)

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
        importo_totale = 0.00
        self.rate_da_versare = Bilancio.getLastBilancio(self.immobile)
        if Bilancio.getLastBilancio(self.immobile):
            self.rate_da_versare = Bilancio.getLastBilancio(self.immobile).importiDaVersare
        else:
            self.rate_da_versare = {}
        self.rate_versate = {}
        for unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values():
            totale_versato = 0.0
            if unita_immobiliare.codice not in self.rate_da_versare:
                self.rate_da_versare[unita_immobiliare.codice] = 0.00
            for rata in Rata.getAllRateByUnitaImmobiliare(unita_immobiliare).values():
                if Bilancio.getLastBilancio(self.immobile):
                    if rata.dataPagamento >= Bilancio.getLastBilancio(self.immobile).dataApprovazione and rata.importo >= 0.0:
                        totale_versato += rata.importo
            self.rate_versate[unita_immobiliare.codice] = totale_versato

        self.spese = [item for item in Spesa.getAllSpeseByImmobile(self.immobile).values() if not item.pagata]
        spese_uniche_per_fornitore = []
        for spese in self.spese:
            if spese.fornitore not in spese_uniche_per_fornitore:
                spese_uniche_per_fornitore.append(spese.fornitore)

        importi_tutti_nulli = False
        importi_da_non_rappresentare = []
        self.table_spese.setColumnCount(2)
        self.table_spese.setRowCount(len(spese_uniche_per_fornitore))

        if self.rate_da_versare:
            for r in self.rate_da_versare.values():
                if r <= 0:
                    importi_da_non_rappresentare.append(r)
            if len(importi_da_non_rappresentare) == len(self.rate_da_versare.values()):
                importi_tutti_nulli = True

        if (not self.spese and not self.rate_da_versare) or (not self.spese and importi_tutti_nulli):
            self.rate_section["lista_rate"].setVisible(False)
            self.rate_section["totale"].setVisible(False)
            self.rate_section["frase_totale"].setVisible(False)
            self.rate_section["no_rate"].setText("Non ci sono rate da versare per questo immobile")
            self.rate_section["no_rate"].setVisible(True)

            self.spese_section["lista_spese"].setVisible(False)
            self.spese_section["totale"].setVisible(False)
            self.spese_section["frase_totale"].setVisible(False)
            self.spese_section["no_spese"].setText("Non ci sono spese per questo immobile")
            self.spese_section["no_spese"].setVisible(True)

        elif not self.rate_da_versare or importi_tutti_nulli:
            self.rate_section["lista_rate"].setVisible(False)
            self.rate_section["totale"].setVisible(False)
            self.rate_section["frase_totale"].setVisible(False)

            self.rate_section["no_rate"].setText("Non ci sono rate da versare per questo immobile")
            self.rate_section["no_rate"].setVisible(True)
        elif not self.spese:
            self.spese_section["lista_spese"].setVisible(False)
            self.spese_section["totale"].setVisible(False)
            self.spese_section["frase_totale"].setVisible(False)

            self.spese_section["no_spese"].setText("Non ci sono spese per questo immobile")
            self.spese_section["no_spese"].setVisible(True)

        self.table_spese.setHorizontalHeaderItem(0, QTableWidgetItem("Importo"))
        self.table_spese.setHorizontalHeaderItem(1, QTableWidgetItem("Fornitore"))

        fornitori = []
        for spese in self.spese:
            fornitori.append(spese.fornitore)

        count = 0
        i = 0
        cod_fornitore_analizzato = []
        for spesa in self.spese:
            spesa_totale_fornitore = 0.0
            if spesa.fornitore not in cod_fornitore_analizzato:
                j = 0
                cod_fornitore_analizzato.append(spesa.fornitore)
                for cod_fornitore in fornitori:
                    if cod_fornitore == spesa.fornitore:
                        count += 1
                if count > 1:
                    for spese in self.spese:
                        if spese.fornitore == spesa.fornitore:
                            spesa_totale_fornitore += spese.importo
                    self.table_spese.setItem(i, j, QTableWidgetItem(str("%.2f" % spesa_totale_fornitore)))
                    self.table_spese.setItem(i, j + 1, QTableWidgetItem(Fornitore.ricercaFornitoreByCodice(spesa.fornitore).denominazione))
                else:
                    self.table_spese.setItem(i, j, QTableWidgetItem(str("%.2f" % spesa.importo)))
                    self.table_spese.setItem(i, j + 1, QTableWidgetItem(Fornitore.ricercaFornitoreByCodice(spesa.fornitore).denominazione))
                i += 1

        if self.spese:
            for spesa in self.spese:
                if not spesa.pagata:
                    importo_totale += spesa.importo
            self.spese_section["totale"].setText(str("%.2f" % importo_totale))
            for spese in self.spese_section.values():
                spese.setVisible(True)
            self.spese_section["no_spese"].setVisible(False)

        self.table_spese.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_spese.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.table_spese.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_spese.verticalHeader().setVisible(False)

        self.table_rate.setColumnCount(2)

        count = 0
        for rate_da_visualizzare in self.rate_da_versare.values():
            if rate_da_visualizzare > 0:
                count += 1

        self.table_rate.setRowCount(count)
        self.table_rate.setHorizontalHeaderItem(0, QTableWidgetItem("Unità Immobiliare"))
        self.table_rate.setHorizontalHeaderItem(1, QTableWidgetItem("Importo"))
        i = 0
        for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).keys():
            j = 0
            unita_immo = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(unita)
            if self.rate_da_versare[unita] > 0:
                if unita in self.rate_da_versare.keys():
                    item = QStandardItem()
                    importo = self.rate_da_versare[unita] - self.rate_versate[unita]
                    importo = str("%.2f" % importo)
                    if unita_immo.tipoUnitaImmobiliare == "Appartamento":
                        if unita_immo.condomini:
                            for condomini in unita_immo.condomini.keys():
                                if unita_immo.condomini[condomini] == "Proprietario":
                                    proprietario = Condomino.ricercaCondominoByCF([item for item in unita_immo.condomini.keys() if unita_immo.condomini[item] == "Proprietario"][0])
                                    item_text = f"{unita_immo.tipoUnitaImmobiliare} Scala {unita_immo.scala} Int.{unita_immo.interno} di {proprietario.cognome} {proprietario.nome}"
                                    self.table_rate.setItem(i, j, QTableWidgetItem(item_text))
                                    self.table_rate.setItem(i, j+1, QTableWidgetItem(importo))
                                    break
                                else:
                                    item_text = f"{unita_immo.tipoUnitaImmobiliare} Scala {unita_immo.scala} Int.{unita_immo.interno} di Nessun proprietario"
                                    self.table_rate.setItem(i, j, QTableWidgetItem(item_text))
                                    self.table_rate.setItem(i, j + 1, QTableWidgetItem(importo))
                        else:
                            item_text = f"{unita_immo.tipoUnitaImmobiliare} Scala {unita_immo.scala} Int.{unita_immo.interno} di Nessun proprietario"
                            self.table_rate.setItem(i, j, QTableWidgetItem(item_text))
                            self.table_rate.setItem(i, j + 1, QTableWidgetItem(importo))
                    else:
                        if unita_immo.condomini:
                            for condomini in unita_immo.condomini.keys():
                                if unita_immo.condomini[condomini] == "Proprietario":
                                    proprietario = Condomino.ricercaCondominoByCF([item for item in unita_immo.condomini.keys() if unita_immo.condomini[item] == "Proprietario"][0])
                                    item_text = f"{unita_immo.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome}"
                                    self.table_rate.setItem(i, j, QTableWidgetItem(item_text))
                                    self.table_rate.setItem(i, j + 1, QTableWidgetItem(importo))
                                    break
                                else:
                                    item_text = f"{unita_immo.tipoUnitaImmobiliare} di Nessun proprietario"
                                    self.table_rate.setItem(i, j, QTableWidgetItem(item_text))
                                    self.table_rate.setItem(i, j + 1, QTableWidgetItem(importo))
                        else:
                            item_text = f"{unita_immo.tipoUnitaImmobiliare} di Nessun proprietario"
                            self.table_rate.setItem(i, j, QTableWidgetItem(item_text))
                            self.table_rate.setItem(i, j + 1, QTableWidgetItem(importo))
            i += 1

        importo_totale = 0.00

        if self.rate_da_versare and not importi_tutti_nulli:
            for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).keys():
                if self.rate_da_versare[unita] > 0:
                    if unita in self.rate_da_versare.keys():
                        importo_totale += self.rate_da_versare[unita]
            self.rate_section["totale"].setText(str("%.2f" % importo_totale))
            for rate in self.rate_section.values():
                rate.setVisible(True)
            self.rate_section["no_rate"].setVisible(False)

        self.table_rate.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_rate.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.table_rate.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_rate.verticalHeader().setVisible(False)