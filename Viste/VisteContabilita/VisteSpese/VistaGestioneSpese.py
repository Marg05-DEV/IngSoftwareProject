import datetime

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QHBoxLayout, QListView, QLabel, \
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView

from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.Gestione.gestoreRegistroAnagrafe import GestoreRegistroAnagrafe
from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteContabilita.VisteSpese.VistaCreateSpesa import VistaCreateSpesa
from Viste.VisteContabilita.VisteSpese.VistaDeleteSpesa import VistaDeleteSpesa
from Viste.VisteContabilita.VisteSpese.VistaReadFattura import VistaReadFattura
from Viste.VisteContabilita.VisteSpese.VistaReadSpesa import VistaReadSpesa
from Viste.VisteContabilita.VisteSpese.VistaUpdateSpesa import VistaUpdateSpesa
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaDeleteUnitaImmobiliare import VistaDeleteUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaUpdateUnitaImmobiliare import VistaUpdateUnitaImmobiliare


class VistaReadUnitaImmobiliare:
    pass


class VistaGestioneSpese(QWidget):
    def __init__(self, parent=None, sortLabel=None):
        super(VistaGestioneSpese, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QGridLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Spesa")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per dataPagamento", "Ricerca per tipoSpesa", "Ricerca per Immobile", "Ricerca per fornitore"])
        self.searchType.activated.connect(self.avvia_ricerca)
        self.searchbar.textChanged.connect(self.avvia_ricerca)

        find_layout.addWidget(self.searchbar)
        find_layout.addWidget(self.searchType)

        sort_layout = QHBoxLayout()

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Data Di pagamento", "Tipo di Spesa A -> Z", "tipo di Spesa Z -> A", "Immobile A -> Z","Immobile Z -> A", "Fornitore A -> Z",
             "Fornitore Z -> A"])
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
        button_layout.addWidget(self.create_button("Visualizza Fattura", self.goReadFattura, True))
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
        self.resize(600, 400)
        self.setWindowTitle("Gestione Spese")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setFixedSize(110, 55)
        button.setCheckable(True)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def avvia_ricerca(self):
        self.update_table(True)

    def avvia_ordinamento(self):
        if self.sortType.currentIndex() == 0:
            self.table_spese.sortItems(0)
        elif self.sortType.currentIndex() == 1:
            self.table_spese.sortItems(3)
        elif self.sortType.currentIndex() == 2:
            self.table_spese.sortItems(1, Qt.SortOrder.AscendingOrder)
        elif self.sortType.currentIndex() == 3:
            self.table_spese.sortItems(1, Qt.SortOrder.DescendingOrder)
        elif self.sortType.currentIndex() == 4:
            self.table_spese.sortItems(2, Qt.SortOrder.AscendingOrder)
        elif self.sortType.currentIndex() == 5:
            self.table_spese.sortItems(2, Qt.SortOrder.DescendingOrder)
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
                self.spese = [item for item in self.spese if data == item.dataPagamento]
            elif self.searchType.currentIndex() == 1:  # ricerca per tipo Spesa
                self.spese = [item for item in self.spese if self.searchbar.text().upper() in (TipoSpesa.ricercaTipoSpesaByCodice(item.tipoSpesa.codice)).nome.upper()]
            elif self.searchType.currentIndex() == 2:  # ricerca per Immobile
                self.spese = [item for item in self.spese if self.searchbar.text().upper() in (Immobile.ricercaImmobileById(item.immobile.id)).denominazione.upper()]
            elif self.searchType.currentIndex() == 3:  # ricerca per nome versante
                self.spese = [item for item in self.spese if self.searchbar.text().upper() in (Fornitore.ricercaFornitoreByPartitaIVA(item.fornitore.partitaIva)).denominazione.upper()]
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
        self.table_spese.setColumnCount(10)

        print("aiuto")

        self.table_spese.setHorizontalHeaderLabels(
            ["Cod.", "Immobile", "Tipo spesa", "Data registrazione", "Data Pagamento", "Data Fattura", "N° Fattura", "Descrizione", "Fornitore", "Importo"])
        self.table_spese.verticalHeader().setVisible(False)

        i = 0
        for spesa in self.spese:
            print(spesa, spesa.getInfoSpesa())
            self.table_spese.setItem(i, 0, QTableWidgetItem(str(spesa.codice)))
            print("i")
            self.table_spese.setItem(i, 1, QTableWidgetItem(Immobile.ricercaImmobileById(spesa.immobile.id).denominazione))
            print("ii")
            self.table_spese.setItem(i, 2, QTableWidgetItem(TipoSpesa.ricercaTipoSpesaByCodice(spesa.tipoSpesa.codice).nome))
            print("iii")
            self.table_spese.setItem(i, 3, QTableWidgetItem(spesa.dataRegistrazione.strftime("%d/%m/%Y")))
            self.table_spese.setItem(i, 4, QTableWidgetItem(spesa.dataPagamento.strftime("%d/%m/%Y")))
            self.table_spese.setItem(i, 5, QTableWidgetItem(spesa.dataFattura.strftime("%d/%m/%Y")))
            print("iiii")
            self.table_spese.setItem(i, 6, QTableWidgetItem(str(spesa.numeroFattura)))
            self.table_spese.setItem(i, 7, QTableWidgetItem(spesa.descrizione))
            self.table_spese.setItem(i, 8, QTableWidgetItem(Fornitore.ricercaFornitoreByPartitaIVA(spesa.fornitore.partitaIva).denominazione))
            self.table_spese.setItem(i, 9, QTableWidgetItem(str(spesa.importo)))
            i += 1

        print("qui")
        self.table_spese.resizeColumnToContents(0)
        self.table_spese.resizeColumnToContents(9)
        self.table_spese.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_spese.sortItems(0, Qt.SortOrder.DescendingOrder)
        self.table_spese.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_spese.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_spese.selectionModel().selectionChanged.connect(self.able_button)

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
        print(codice_spesa, ": ", spesa_selezionata.getInforSpesa())
        self.vista_elimina_spesa = VistaDeleteSpesa(spesa_selezionata, callback=self.callback)
        self.vista_elimina_spesa.show()

    def goReadFattura(self):
        print("vis ricevuta rata")
        spesa_selezionata = None
        codice_spesa = [item.data(0) for item in self.table_spese.verticalHeader().selectionModel().selectedRows()][0]
        spesa_selezionata = Spesa.ricercaSpesaByCodice(int(codice_spesa))
        print(codice_spesa, ": ", spesa_selezionata.getInfoRata())
        self.vista_leggi_fattura = VistaReadFattura(spesa_selezionata, callback=self.callback)
        self.vista_leggi_fattura.show()

    def able_button(self):
        if not self.table_spese.verticalHeader().selectionModel().selectedRows():
            self.button_list["Visualizza Spesa"].setDisabled(True)
            self.button_list["Modifica Spesa"].setDisabled(True)
            self.button_list["Elimina Spesa"].setDisabled(True)
            self.button_list["Visualizza Fattura"].setDisabled(True)
        else:
            self.button_list["Visualizza Spesa"].setDisabled(False)
            self.button_list["Modifica Spesa"].setDisabled(False)
            self.button_list["Elimina Spesa"].setDisabled(False)
            self.button_list["Visualizza Fattura"].setDisabled(False)

    def callback(self, msg):
        self.button_list["Visualizza Spesa"].setDisabled(True)
        self.button_list["Modifica Spesa"].setDisabled(True)
        self.button_list["Elimina Spesa"].setDisabled(True)
        self.button_list["Visualizza Fattura"].setDisabled(True)
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