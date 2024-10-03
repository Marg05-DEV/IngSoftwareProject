import datetime
import os
import shutil
import webbrowser

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QLabel, QWidget, QTableWidget, QPushButton, \
    QSizePolicy, QTableWidgetItem, QAbstractItemView, QHeaderView, QTableView

from Classes.Contabilita.rata import Rata
from Classes.Gestione.gestoreContabilita import GestoreContabilita
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Viste.VisteContabilita.VisteRate.VistaCreateRata import VistaCreateRata
from Viste.VisteContabilita.VisteRate.VistaDeleteRata import VistaDeleteRata
from Viste.VisteContabilita.VisteRate.VistaReadRata import VistaReadRata
from Viste.VisteContabilita.VisteRate.VistaUpdateRata import VistaUpdateRata


class VistaGestioneRate(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneRate, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QHBoxLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca...")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per data di pagamento", "Ricerca per denominazione dell'immobile", "Ricerca per nome del versante"])
        self.searchType.activated.connect(self.avvia_ricerca)
        self.searchbar.textChanged.connect(self.avvia_ricerca)

        find_layout.addWidget(self.searchbar)
        find_layout.addWidget(self.searchType)

        sort_layout = QHBoxLayout()

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Ultimo inserimento", "Data di pagamento", "Denominazione Immobile A -> Z", "Denominazione Immobile Z -> A", "Nominativo versante A -> Z", "Nominativo versante Z -> A"])
        self.sortType.activated.connect(self.avvia_ordinamento)
        sort_layout.addWidget(sortLabel)
        sort_layout.addWidget(self.sortType)

        self.table_rate = QTableWidget()

        button_layout = QHBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Rata", self.goCreateRata))
        button_layout.addWidget(self.create_button("Visualizza Rata", self.goReadRata, True))
        button_layout.addWidget(self.create_button("Modifica Rata", self.goUpdateRata, True))
        button_layout.addWidget(self.create_button("Elimina Rata", self.goDeleteRata, True))
        button_layout.addWidget(self.create_button("Visualizza Ricevuta", self.goReadRicevuta, True))
        message_layout = QHBoxLayout()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        self.rate = []
        self.update_table()

        message_layout.addWidget(self.msg)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(sort_layout)
        main_layout.addWidget(self.table_rate)
        main_layout.addLayout(message_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(800, 540)
        self.setWindowTitle("Gestione Rate")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMinimumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def avvia_ricerca(self):
        self.update_table(True)

    def avvia_ordinamento(self):
        if self.sortType.currentIndex() == 0:
            self.table_rate.sortItems(0, Qt.SortOrder.DescendingOrder)
        elif self.sortType.currentIndex() == 1:
            self.table_rate.sortItems(3, Qt.SortOrder.DescendingOrder)
        elif self.sortType.currentIndex() == 2:
            self.table_rate.sortItems(1, Qt.SortOrder.AscendingOrder)
        elif self.sortType.currentIndex() == 3:
            self.table_rate.sortItems(1, Qt.SortOrder.DescendingOrder)
        elif self.sortType.currentIndex() == 4:
            self.table_rate.sortItems(2, Qt.SortOrder.AscendingOrder)
        elif self.sortType.currentIndex() == 5:
            self.table_rate.sortItems(2, Qt.SortOrder.DescendingOrder)
        else:
            print("Altro")

    def update_table(self, searchActivated=False):
        self.rate = list(Rata.getAllRate().values())

        if searchActivated and self.searchbar.text():
            if self.searchType.currentIndex() == 0 and len(self.searchbar.text()) == 10:  # ricerca per denominazione
                day, month, year = [int(x) for x in self.searchbar.text().split("/")]
                data = datetime.date(year, month, day)
                self.rate = [item for item in self.rate if data == item.dataPagamento]
            elif self.searchType.currentIndex() == 1:  # ricerca per immobile
                self.rate = [item for item in self.rate if self.searchbar.text().upper() in (Immobile.ricercaImmobileById(UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(item.unitaImmobiliare).immobile)).denominazione.upper()]
            elif self.searchType.currentIndex() == 2:  # ricerca per nome versante
                self.rate = [item for item in self.rate if self.searchbar.text().upper() in item.versante.upper()]
        if not self.rate:
            if searchActivated:
                self.msg.setText("Nessuna rata corrisponde alla ricerca")
            else:
                self.msg.setText("Non sono presenti rate")
            self.msg.show()
        elif not self.timer.isActive():
            self.msg.hide()

        self.table_rate.setRowCount(len(self.rate))
        self.table_rate.setColumnCount(7)

        self.table_rate.setHorizontalHeaderLabels(["Cod.", "Immobile", "Condomino", "Data pagamento", "Descrizione", "N° Ricevuta", "Importo"])
        self.table_rate.verticalHeader().setVisible(False)

        i = 0
        for rata in self.rate:
            self.table_rate.setItem(i, 0, QTableWidgetItem())
            self.table_rate.item(i, 0).setData(Qt.ItemDataRole.DisplayRole, rata.codice)
            self.table_rate.item(i, 0).setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            if rata.unitaImmobiliare > 0:
                self.table_rate.setItem(i, 1, QTableWidgetItem((Immobile.ricercaImmobileById((UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(rata.unitaImmobiliare)).immobile)).denominazione))
            else:
                self.table_rate.setItem(i, 1, QTableWidgetItem(""))
            self.table_rate.setItem(i, 2, QTableWidgetItem(rata.versante))
            self.table_rate.setItem(i, 3, QTableWidgetItem(rata.dataPagamento.strftime("%Y/%m/%d")))
            self.table_rate.setItem(i, 4, QTableWidgetItem(rata.descrizione))
            if rata.numeroRicevuta > 0:
                self.table_rate.setItem(i, 5, QTableWidgetItem(str(rata.numeroRicevuta)))
            else:
                self.table_rate.setItem(i, 5, QTableWidgetItem())
            self.table_rate.item(i, 5).setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table_rate.setItem(i, 6, QTableWidgetItem("%.2f" % rata.importo))
            self.table_rate.item(i, 6).setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.table_rate.setItem(i, 7, QTableWidgetItem())
            i += 1

        self.table_rate.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_rate.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.table_rate.sortItems(0, Qt.SortOrder.DescendingOrder)
        self.table_rate.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_rate.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_rate.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_rate.selectionModel().selectionChanged.connect(self.able_button)

    def goCreateRata(self):
        self.vista_nuova_rata = VistaCreateRata(callback=self.callback)
        self.vista_nuova_rata.show()

    def goReadRata(self):
        rata_selezionata = None
        codice_rata = [item.data(0) for item in self.table_rate.verticalHeader().selectionModel().selectedRows()][0]
        rata_selezionata = Rata.ricercaRataByCodice(int(codice_rata))
        self.vista_dettaglio_rata = VistaReadRata(rata_selezionata, callback=self.callback)
        self.vista_dettaglio_rata.show()


    def goUpdateRata(self):
        codice_rata = [item.data(0) for item in self.table_rate.verticalHeader().selectionModel().selectedRows()][0]
        rata_selezionata = Rata.ricercaRataByCodice(int(codice_rata))

        self.vista_modifica_rata = VistaUpdateRata(rata_selezionata, self.callback)
        self.vista_modifica_rata.show()

    def goDeleteRata(self):
        codice_rata = [item.data(0) for item in self.table_rate.verticalHeader().selectionModel().selectedRows()][0]
        rata_selezionata = Rata.ricercaRataByCodice(int(codice_rata))

        self.vista_elimina_rata = VistaDeleteRata(rata_selezionata, callback=self.callback)
        self.vista_elimina_rata.show()

    def goReadRicevuta(self):
        codice_rata = [item.data(0) for item in self.table_rate.verticalHeader().selectionModel().selectedRows()][0]
        rata_selezionata = Rata.ricercaRataByCodice(int(codice_rata))
        directory_file = os.path.dirname(os.path.abspath(__file__)).replace("\\Viste\\VisteContabilita\\VisteRate", "\\Dati\\pdf\\")
        if os.path.isdir(directory_file + "temp\\"):
            shutil.rmtree(directory_file + "temp\\")
        if not os.path.isdir(directory_file + "temp\\"):
            os.makedirs(directory_file + "temp\\")
        pdf = GestoreContabilita.generaRicevuta(rata_selezionata)
        pdf.output(directory_file + "temp\\ricevuta.pdf")
        webbrowser.open(directory_file + "temp\\ricevuta.pdf")



    def able_button(self):
        if not self.table_rate.verticalHeader().selectionModel().selectedRows():
            self.button_list["Visualizza Rata"].setDisabled(True)
            self.button_list["Modifica Rata"].setDisabled(True)
            self.button_list["Elimina Rata"].setDisabled(True)
            self.button_list["Visualizza Ricevuta"].setDisabled(True)
        else:
            self.button_list["Visualizza Rata"].setDisabled(False)
            self.button_list["Modifica Rata"].setDisabled(False)
            self.button_list["Elimina Rata"].setDisabled(False)
            self.button_list["Visualizza Ricevuta"].setDisabled(False)


    def callback(self, msg):
        self.button_list["Visualizza Rata"].setDisabled(True)
        self.button_list["Modifica Rata"].setDisabled(True)
        self.button_list["Elimina Rata"].setDisabled(True)
        self.searchbar.clear()
        self.searchType.clear()
        self.searchType.addItems(["Ricerca per data di pagamento", "Ricerca per denominazione dell'immobile", "Ricerca per nome del versante"])
        self.update_table()
        self.avvia_ordinamento()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.rate:
            self.msg.setText("Non sono presenti immobili")
            self.msg.show()

