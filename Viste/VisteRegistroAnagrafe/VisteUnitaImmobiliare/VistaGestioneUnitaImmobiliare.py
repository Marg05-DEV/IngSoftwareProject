from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, QPushButton

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliare.VistaCreateUnitaImmobiliare import VistaCreateUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliare.VistaDeleteUnitaImmobiliare import VistaDeleteUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliare.VistaReadUnitaImmobiliare import VistaReadUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliare.VistaUpdateUnitaImmobiliare import VistaUpdateUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliare.VistaAddAssegnazione import VistaAddAssegnazione
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliare.VistaReadAssegnazione import VistaReadAssegnazione


class VistaGestioneUnitaImmobiliare(QWidget):

    def __init__(self, search_text):
        print("hello")
        super(VistaGestioneUnitaImmobiliare, self).__init__()
        print("hello1")
        self.search_text = search_text
        main_layout = QVBoxLayout()

        find_layout = QGridLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Assegnazione")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per denominazione", "Ricerca per sigla", "Ricerca per codice"])
        self.searchType.activated.connect(self.debugComboBox1)

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Dati catastali", "Nominativo condomino A-Z", "Nominativo condomino Z-A"])
        self.sortType.activated.connect(self.avvia_ordinamento)
        find_layout.addWidget(self.searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(self.sortType, 1, 1)

        action_layout = QHBoxLayout()

        self.list_view_unitaImmobiliare = QListView()


        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Assegnazione", self.go_Add_Assegnazione))
        button_layout.addWidget(self.create_button("Visualizza Asseganzione", self.go_Read_Assegnazione, True))

        action_layout.addWidget(self.list_view_unitaImmobiliare)

        self.update_list()

        self.selectionModel = self.list_view_unitaImmobiliare.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)

        message_layout = QHBoxLayout()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        message_layout.addWidget(self.msg)
        action_layout.addLayout(button_layout)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Unità Immobiliare")
        print("fine")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setFixedSize(110, 55)
        button.setCheckable(True)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button
    def avvia_ricerca(self):
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(self.searchType.currentText()))
        sorting, desc = self.ordina_lista(True)
        self.update_list(sorting, desc, True)

    def avvia_ordinamento(self):
        print("selected index SORTING: " + str(self.sortType.currentIndex()) + " -> " + str(self.sortType.currentText()))
        self.ordina_lista(False)

    def ordina_lista(self, fromRicerca=False):
        if self.sortType.currentIndex() == 0:
            if fromRicerca:
                return UnitaImmobiliare.ordinaCondominoByInterno, False
            self.update_list()
        elif self.sortType.currentIndex() == 1:
            if fromRicerca:
                return UnitaImmobiliare.ordinaCondominoByInterno, True
            self.update_list(decr = True)
        elif self.sortType.currentIndex() == 2:
            if fromRicerca:
                return Condomino.ordinaCondominoByName, False
            self.update_list(Condomino.ordinaCondominoByName, False)
        elif self.sortType.currentIndex() == 3:
            if fromRicerca:
                return Condomino.ordinaCondominoByName, True
            self.update_list(Condomino.ordinaCondominoByName, True)
        else:
            print("Altro")

    def update_list(self, sorting_function=UnitaImmobiliare.ordinaCondominoByInterno, decr=False, searchActivated=False):
        print("class VistaGestioneImmobile - update_list inizio")
        self.lista_unitaImmobiliari = []
        self.lista_unitaImmobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliari().values())
        print(UnitaImmobiliare.getAllUnitaImmobiliari().values())
        print(searchActivated and self.searchbar.text())
        if searchActivated and self.searchbar.text():
            print("sto cercando...")
            if self.searchType.currentIndex() == 0:  # ricerca per dati catastali
                self.lista_unitaImmobiliari = [item for item in self.lista_unitaImmobiliari if
                                       self.searchbar.text().upper() in item.interno.upper()]
            elif self.searchType.currentIndex() == 1:  # ricerca per nominativo condomino
                self.lista_unitaImmobiliari = [item for item in self.lista_unitaImmobiliari if
                                       self.searchbar.text().upper() in item.condomini.values().upper()]

        sorting_function(self.lista_unitaImmobiliari, decr)
        print(self.lista_unitaImmobiliari)

        listview_model = QStandardItemModel(self.list_view_unitaImmobiliare)

        for unitaImmobiliare in self.lista_unitaImmobiliari:
            flag = 0
            if unitaImmobiliare.immobile == self.search_text:
                item = QStandardItem()
                item_text = f"{unitaImmobiliare.codice} {unitaImmobiliare.denominazione} - {unitaImmobiliare.denominazione}"
                item.setText(item_text)
                item.setEditable(False)
                font = item.font()
                font.setPointSize(12)
                item.setFont(font)
                listview_model.appendRow(item)
                flag  += 1
            elif flag == 0:
                print("Non ci sono Unità Immobiliari assegante all'immobile")
                return None

        self.list_view_unitaImmobiliare.setModel(listview_model)

        self.selectionModel = self.list_view_unitaImmobiliare.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)
        print(type(self.selectionModel))


    def go_Add_Assegnazione(self):
        self.vista_nuova_Assegnazione = VistaAddAssegnazione()
        self.vista_nuova_Assegnazione.show()

    def go_Read_Assegnazione(self):
        item = None
        for index in self.list_view_unitaImmobiliare.selectedIndexes():
            item = self.list_view_unitaImmobiliare.model().itemFromIndex(index)
            print(item.text())
        sel_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareInterno(int(item.text().split(" ")[0]))
        self.vista_dettaglio_Assegnazione = VistaReadAssegnazione(sel_unitaImmobiliare)
        self.vista_dettaglio_Assegnazione.show()

    def go_Update_unitaImmobiliare(self):
        item = None
        for index in self.list_view_unitaImmobiliare.selectedIndexes():
            item = self.list_view_unitaImmobiliare.model().itemFromIndex(index)
            print(item.text())
        sel_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareInterno(int(item.text().split(" ")[0]))
        self.vista_modifica_immobile = VistaUpdateUnitaImmobiliare(sel_unitaImmobiliare, callback=self.callback)
        self.vista_modifica_unitaImmobiliare.show()

    def go_Delete_unitaImmobiliare(self):
        item = None
        for index in self.list_view_unitaImmobiliare.selectedIndexes():
            item = self.list_view_unitaImmobiliare.model().itemFromIndex(index)
            print(item.text())
        sel_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareInterno(int(item.text().split(" ")[0]))
        self.vista_elimina_unitaImmobiliare = VistaDeleteUnitaImmobiliare(sel_unitaImmobiliare, callback=self.callback)
        self.vista_elimina_unitaImmobiliare.show()


    def able_button(self):
        print("selezione cambiata")
        if not self.list_view_unitaImmobiliare.selectedIndexes():
            self.button_list["Visualizza Assegnazione"].setDisabled(True)
        else:
            self.button_list["Visualizza Assegnazione"].setDisabled(False)

    def callback(self, msg):
        self.update_list()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()