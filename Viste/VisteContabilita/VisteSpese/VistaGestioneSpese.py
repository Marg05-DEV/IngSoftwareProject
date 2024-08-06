import datetime

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QHBoxLayout, QListView, QLabel, \
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QCheckBox

from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteContabilita.VisteSpese.VistaCreateSpesa import VistaCreateSpesa
from Viste.VisteContabilita.VisteSpese.VistaDeleteSpesa import VistaDeleteSpesa
from Viste.VisteContabilita.VisteSpese.VistaReadSpesa import VistaReadSpesa
from Viste.VisteContabilita.VisteSpese.VistaUpdateSpesa import VistaUpdateSpesa

class VistaGestioneSpese(QWidget):
    def __init__(self):
        super(VistaGestioneSpese, self).__init__()
        print("soono nelle spese")
        main_layout = QVBoxLayout()

        find_layout = QHBoxLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Spesa")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per data di pagamento", "Ricerca per tipologia di spesa", "Ricerca per immobile", "Ricerca per fornitore"])
        self.searchType.activated.connect(self.avvia_ricerca)
        self.searchbar.textChanged.connect(self.avvia_ricerca)

        self.checkboxes = {}
        find_layout.addWidget(self.searchbar)
        find_layout.addWidget(self.searchType)

        sort_layout = QHBoxLayout()

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Ultimo inserito", "Data di pagamento", "Tipo di spesa A -> Z", "Tipo di spesa Z -> A", "Denominazione Immobile A -> Z", "Denominazione Immobile Z -> A", "Denominazione Fornitore A -> Z", "Denomianzione Fornitore Z -> A"])
        self.sortType.activated.connect(self.avvia_ordinamento)
        sort_layout.addWidget(sortLabel)
        sort_layout.addWidget(self.sortType)

        self.table_spese = QTableWidget()
        self.lista_spese = []

        button_layout = QHBoxLayout()
        self.button_list = {}
        button_layout.addWidget(self.create_button("Aggiungi Spesa", self.goCreateSpesa))
        button_layout.addWidget(self.create_button("Visualizza Spesa", self.goReadSpesa, True))
        button_layout.addWidget(self.create_button("Modifica Spesa", self.goUpdateSpesa, True))
        button_layout.addWidget(self.create_button("Elimina Spesa", self.goDeleteSpesa, True))
        message_layout = QHBoxLayout()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        self.update_table()
        message_layout.addWidget(self.msg)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(sort_layout)
        main_layout.addWidget(self.table_spese)
        main_layout.addLayout(message_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(800, 540)
        self.setWindowTitle("Gestione Spese")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setMinimumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        button.setCheckable(False)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def avvia_ricerca(self):
        self.update_table(True)

    def avvia_ordinamento(self):
        if self.sortType.currentIndex() == 0:
            self.table_spese.sortItems(0, Qt.SortOrder.DescendingOrder)
        elif self.sortType.currentIndex() == 1:
            self.table_spese.sortItems(2, Qt.SortOrder.DescendingOrder)
        elif self.sortType.currentIndex() == 2:
            self.table_spese.sortItems(4, Qt.SortOrder.AscendingOrder)
        elif self.sortType.currentIndex() == 3:
            self.table_spese.sortItems(4, Qt.SortOrder.DescendingOrder)
        elif self.sortType.currentIndex() == 4:
            self.table_spese.sortItems(1, Qt.SortOrder.AscendingOrder)
        elif self.sortType.currentIndex() == 5:
            self.table_spese.sortItems(1, Qt.SortOrder.DescendingOrder)
        elif self.sortType.currentIndex() == 6:
            self.table_spese.sortItems(5, Qt.SortOrder.AscendingOrder)
        elif self.sortType.currentIndex() == 7:
            self.table_spese.sortItems(5, Qt.SortOrder.DescendingOrder)
        else:
            print("Altro")

    def update_table(self, searchActivated=False):
        self.spese = list(Spesa.getAllSpese().values())

        print("update")

        if searchActivated and self.searchbar.text():
            print("in ricerca")
            if self.searchType.currentIndex() == 0 and len(self.searchbar.text()) == 10:  # ricerca per data Pagamento
                day, month, year = [int(x) for x in self.searchbar.text().split("/")]
                data = datetime.date(year, month, day)
                self.spese = [item for item in self.spese if data == item.dataPagamento and item.pagata]
            elif self.searchType.currentIndex() == 1:  # ricerca per tipo Spesa
                self.spese = [item for item in self.spese if self.searchbar.text().upper() in (TipoSpesa.ricercaTipoSpesaByCodice(item.tipoSpesa)).nome.upper()]
            elif self.searchType.currentIndex() == 2:  # ricerca per Immobile
                self.spese = [item for item in self.spese if self.searchbar.text().upper() in (Immobile.ricercaImmobileById(item.immobile)).denominazione.upper()]
            elif self.searchType.currentIndex() == 3:  # ricerca per denominazione fornitore
                self.spese = [item for item in self.spese if self.searchbar.text().upper() in (Fornitore.ricercaFornitoreByCodice(item.fornitore)).denominazione.upper()]
        if not self.spese:
            print("vuoto")
            if searchActivated:
                self.msg.setText("Nessuna spesa corrisponde alla ricerca")
            else:
                self.msg.setText("Non sono presenti spese")
            self.msg.show()
        elif not self.timer.isActive():
            self.msg.hide()

        self.table_spese.setRowCount(len(self.spese))
        self.table_spese.setColumnCount(8)

        print("aiuto")

        self.table_spese.setHorizontalHeaderLabels(["Cod.", "Immobile", "Data di pagamento", "Descrizione", "Tipologia di spesa", "Fornitore", "Importo", "Pagata"])
        self.table_spese.verticalHeader().setVisible(False)

        i = 0
        for spesa in self.spese:
            print(spesa, spesa.getInfoSpesa())
            self.table_spese.setItem(i, 0, QTableWidgetItem())
            self.table_spese.item(i, 0).setData(Qt.ItemDataRole.DisplayRole, spesa.codice)
            self.table_spese.item(i, 0).setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table_spese.setItem(i, 1, QTableWidgetItem(Immobile.ricercaImmobileById(spesa.immobile).denominazione))
            if spesa.pagata:
                self.table_spese.setItem(i, 2, QTableWidgetItem(spesa.dataPagamento.strftime("%Y/%m/%d")))
            else:
                self.table_spese.setItem(i, 2, QTableWidgetItem(""))
            self.table_spese.setItem(i, 3, QTableWidgetItem(spesa.descrizione))
            self.table_spese.setItem(i, 4, QTableWidgetItem(TipoSpesa.ricercaTipoSpesaByCodice(spesa.tipoSpesa).nome))
            print("prima di fornitore")
            self.table_spese.setItem(i, 5, QTableWidgetItem(Fornitore.ricercaFornitoreByCodice(spesa.fornitore).denominazione))
            print("prima di inserire importo")
            self.table_spese.setItem(i, 6, QTableWidgetItem(str("%.2f" % spesa.importo)))
            print("dopo inserimento importo")
            self.table_spese.item(i, 6).setTextAlignment(Qt.AlignmentFlag.AlignRight)
            cell_widget = QWidget()
            checkbox = QCheckBox()
            self.checkboxes[spesa.codice] = checkbox
            checkbox.stateChanged.connect(self.reset_pagata)
            print("b")
            if spesa.pagata:
                checkbox.setCheckState(Qt.CheckState.Checked)
            else:
                checkbox.setCheckState(Qt.CheckState.Unchecked)

            checkbox.setTristate(False)

            checkbox_layout = QHBoxLayout(cell_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(checkbox_layout)

            self.table_spese.setCellWidget(i, 7, cell_widget)
            print("c")
            i += 1

        self.table_spese.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_spese.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table_spese.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        self.table_spese.sortItems(0, Qt.SortOrder.DescendingOrder)
        self.table_spese.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_spese.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_spese.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_spese.selectionModel().selectionChanged.connect(self.able_button)

    def reset_pagata(self):
        checkbox = self.sender()
        for cod_spesa, cell_widget_checkbox in self.checkboxes.items():
            if cell_widget_checkbox is checkbox:
                spesa = Spesa.ricercaSpesaByCodice(cod_spesa)
        if spesa.pagata:
            checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            checkbox.setCheckState(Qt.CheckState.Unchecked)

    def goCreateSpesa(self):
        print("creazione rata")
        self.vista_nuova_spesa = VistaCreateSpesa(callback=self.callback)
        self.vista_nuova_spesa.show()

    def goReadSpesa(self):
        print("visualizzazione rata")
        spesa_selezionata = None
        codice_spesa = [item.data(0) for item in self.table_spese.verticalHeader().selectionModel().selectedRows()][0]
        spesa_selezionata = Spesa.ricercaSpesaByCodice(int(codice_spesa))
        print(codice_spesa, ": ", spesa_selezionata.getInfoSpesa())
        self.vista_dettaglio_spesa = VistaReadSpesa(spesa_selezionata, callback=self.callback)
        self.vista_dettaglio_spesa.show()

    def goUpdateSpesa(self):
        print("modifica rata")
        spesa_selezionata = None
        codice_spesa = [item.data(0) for item in self.table_spese.verticalHeader().selectionModel().selectedRows()][0]
        spesa_selezionata = Spesa.ricercaSpesaByCodice(int(codice_spesa))
        print(codice_spesa, ": ", spesa_selezionata.getInfoSpesa())
        self.vista_modifica_spesa = VistaUpdateSpesa(spesa_selezionata, callback=self.callback)
        self.vista_modifica_spesa.show()

    def goDeleteSpesa(self):
        print("modifica rata")
        spesa_selezionata = None
        codice_spesa = [item.data(0) for item in self.table_spese.verticalHeader().selectionModel().selectedRows()][0]
        spesa_selezionata = Spesa.ricercaSpesaByCodice(int(codice_spesa))
        print(codice_spesa, ": ", spesa_selezionata.getInfoSpesa())
        self.vista_elimina_spesa = VistaDeleteSpesa(spesa_selezionata, callback=self.callback)
        self.vista_elimina_spesa.show()


    def able_button(self):
        if not self.table_spese.verticalHeader().selectionModel().selectedRows():
            self.button_list["Visualizza Spesa"].setDisabled(True)
            self.button_list["Modifica Spesa"].setDisabled(True)
            self.button_list["Elimina Spesa"].setDisabled(True)
        else:
            self.button_list["Visualizza Spesa"].setDisabled(False)
            self.button_list["Modifica Spesa"].setDisabled(False)
            self.button_list["Elimina Spesa"].setDisabled(False)

    def callback(self, msg):
        self.button_list["Visualizza Spesa"].setDisabled(True)
        self.button_list["Modifica Spesa"].setDisabled(True)
        self.button_list["Elimina Spesa"].setDisabled(True)
        self.searchbar.clear()
        self.searchType.clear()
        self.searchType.addItems(["Ricerca per dataPagamento", "Ricerca per tipoSpesa", "Ricerca per Immobile", "Ricerca per fornitore"])
        self.update_table()
        self.avvia_ordinamento()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()