from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, \
    QPushButton, QTableWidget

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaGestioneTabelleMillesimali(QWidget):

    def __init__(self, immobile):
        super(VistaGestioneTabelleMillesimali, self).__init__()
        self.immobile = immobile
        main_layout = QVBoxLayout()
        action_layout = QHBoxLayout()

        self.table_tabellaMillesimale = self.create_table()
        main_layout.addWidget(self.table_tabellaMillesimale)

        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Tabella Millesimale", self.go_add_unitaImmobiliare()))
        button_layout.addWidget(self.create_button("Visualizza Tabella Millesimale", self.go_read_unitaImmobiliare(),True))
        button_layout.addWidget(self.create_button("Rimuovi Tabella Millesimale", self.go_delete_unitaImmobiliare(), True))

        message_layout = QHBoxLayout()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)


        self.update_list()

        message_layout.addWidget(self.msg)
        action_layout.addLayout(button_layout)

        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Immobile")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setFixedSize(115, 60)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def create_table(self):
        table = QTableWidget()
        self.unitaImmobiliari_immobile = UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile)
        table.setRowCount(len(self.unitaImmobiliari_immobile)+1)


    def update_list(self, sorting_function=Immobile.ordinaImmobileByDenominazione, decr=False, searchActivated=False):
        self.lista_immobili = []
        self.lista_immobili = list(Immobile.getAllImmobili().values())
        print(Immobile.getAllImmobili().values())
        print(self.lista_immobili)
        if searchActivated and self.searchbar.text():
            if self.searchType.currentIndex() == 0: # ricerca per denominazione
                self.lista_immobili = [item for item in self.lista_immobili if self.searchbar.text().upper() in item.denominazione.upper()]
            elif self.searchType.currentIndex() == 1: # ricerca per sigla
                self.lista_immobili = [item for item in self.lista_immobili if self.searchbar.text().upper() in item.sigla.upper()]
            elif self.searchType.currentIndex() == 2: # ricerca per codice
                self.lista_immobili = [item for item in self.lista_immobili if self.searchbar.text() in str(item.codice)]

        sorting_function(self.lista_immobili, decr)

        if not self.lista_immobili:
            if searchActivated:
                self.msg.setText("Nessun immobile corrisponde alla ricerca")
            else:
                self.msg.setText("Non sono presenti immobili")
            self.msg.show()
        elif not self.timer.isActive():
            self.msg.hide()

        listview_model = QStandardItemModel(self.list_view_immobili)

        for immobile in self.lista_immobili:
            item = QStandardItem()
            item_text = f"{immobile.codice} {immobile.sigla} - {immobile.denominazione}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        self.list_view_immobili.setModel(listview_model)

        self.selectionModel = self.list_view_immobili.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)
        print(type(self.selectionModel))


    def go_add_unitaImmobiliare(self):
        self.vista_nuovo_immobile = VistaCreateImmobile(callback=self.callback)
        self.vista_nuovo_immobile.show()

    def go_read_unitaImmobiliare(self):
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
        self.vista_dettaglio_immobile = VistaReadImmobile(sel_immobile, callback=self.callback)
        self.vista_dettaglio_immobile.show()

    def go_delete_unitaImmobiliare(self):
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
            print("ciao")
            print(int(item.text().split(" ")[0]))
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
        print(sel_immobile, ": ", sel_immobile.getInfoImmobile())
        self.vista_modifica_immobile = VistaUpdateImmobile(sel_immobile, callback=self.callback)
        self.vista_modifica_immobile.show()



    def able_button(self):
        if not self.list_view_immobili.selectedIndexes():
            self.button_list["Visualizza Immobile"].setDisabled(True)
            self.button_list["Modifica Immobile"].setDisabled(True)
            self.button_list["Elimina Immobile"].setDisabled(True)
        else:
            self.button_list["Visualizza Immobile"].setDisabled(False)
            self.button_list["Modifica Immobile"].setDisabled(False)
            self.button_list["Elimina Immobile"].setDisabled(False)

    def callback(self, msg):
        self.button_list["Visualizza Immobile"].setDisabled(True)
        self.button_list["Modifica Immobile"].setDisabled(True)
        self.button_list["Elimina Immobile"].setDisabled(True)
        sort, desc = self.ordina_lista(True)
        self.update_list(sort, desc)
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()