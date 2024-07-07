from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, \
    QPushButton, QSizePolicy

from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteImmobile.VistaCreateImmobile import VistaCreateImmobile
from Viste.VisteImmobile.VistaDeleteImmobile import VistaDeleteImmobile
from Viste.VisteImmobile.VistaReadImmobile import VistaReadImmobile
from Viste.VisteImmobile.VistaUpdateImmobile import VistaUpdateImmobile


class VistaGestioneImmobile(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneImmobile, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QGridLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca...")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per denominazione", "Ricerca per sigla", "Ricerca per codice"])
        self.searchType.activated.connect(self.avvia_ricerca)
        self.searchbar.textChanged.connect(self.avvia_ricerca)

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Denominazione A -> Z", "Denominazione Z -> A", "Sigla A -> Z", "Sigla Z -> A", "Codice crescente",
             "Codice decrescente"])
        self.sortType.activated.connect(self.avvia_ordinamento)
        find_layout.addWidget(self.searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(self.sortType, 1, 1)

        action_layout = QHBoxLayout()

        self.list_view_immobili = QListView()

        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Immobile", self.go_Create_immobile))
        button_layout.addWidget(self.create_button("Visualizza Immobile", self.go_Read_immobile,True))
        button_layout.addWidget(self.create_button("Modifica Immobile", self.go_Update_immobile, True))
        button_layout.addWidget(self.create_button("Elimina Immobile", self.go_Delete_immobile, True))

        action_layout.addWidget(self.list_view_immobili)

        message_layout = QHBoxLayout()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        self.lista_immobili = []
        self.update_list()

        message_layout.addWidget(self.msg)
        action_layout.addLayout(button_layout)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Immobile")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def avvia_ricerca(self):
        sorting, desc = self.ordina_lista(True)
        self.update_list(sorting, desc, True)

    def avvia_ordinamento(self):
        if self.searchbar.text():
            sorting, desc = self.ordina_lista(True)
            self.update_list(sorting, desc, True)
        else:
            self.ordina_lista(False)


    def ordina_lista(self, fromRicerca=False):
        if self.sortType.currentIndex() == 0:
            if fromRicerca:
                return Immobile.ordinaImmobileByDenominazione, False
            self.update_list()
        elif self.sortType.currentIndex() == 1:
            if fromRicerca:
                return Immobile.ordinaImmobileByDenominazione, True
            self.update_list(decr=True)
        elif self.sortType.currentIndex() == 2:
            if fromRicerca:
                return Immobile.ordinaImmobileBySigla, False
            self.update_list(Immobile.ordinaImmobileBySigla)
        elif self.sortType.currentIndex() == 3:
            if fromRicerca:
                return Immobile.ordinaImmobileBySigla, True
            self.update_list(Immobile.ordinaImmobileBySigla, True)
        elif self.sortType.currentIndex() == 4:
            if fromRicerca:
                return Immobile.ordinaImmobileByCodice, False
            self.update_list(Immobile.ordinaImmobileByCodice)
        elif self.sortType.currentIndex() == 5:
            if fromRicerca:
                return Immobile.ordinaImmobileByCodice, True
            self.update_list(Immobile.ordinaImmobileByCodice, True)
        else:
            print("Altro")

    def update_list(self, sorting_function=Immobile.ordinaImmobileByDenominazione, decr=False, searchActivated=False):
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


    def go_Create_immobile(self):
        self.vista_nuovo_immobile = VistaCreateImmobile(callback=self.callback)
        self.vista_nuovo_immobile.show()

    def go_Read_immobile(self):
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
        self.vista_dettaglio_immobile = VistaReadImmobile(sel_immobile, callback=self.callback)
        self.vista_dettaglio_immobile.show()

    def go_Update_immobile(self):
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

    def go_Delete_immobile(self):
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
        self.vista_elimina_immobile = VistaDeleteImmobile(sel_immobile, callback=self.callback)
        self.vista_elimina_immobile.show()


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
        self.searchbar.clear()
        self.searchType.clear()
        self.searchType.addItems(["Ricerca per denominazione", "Ricerca per sigla", "Ricerca per codice"])
        sort, desc = self.ordina_lista(True)
        self.update_list(sort, desc)
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.lista_immobili:
            self.msg.setText("Non sono presenti immobili")
            self.msg.show()

