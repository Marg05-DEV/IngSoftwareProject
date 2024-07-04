from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, QPushButton

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaDeleteUnitaImmobiliare import VistaDeleteUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaUpdateUnitaImmobiliare import VistaUpdateUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaCreateUnitaImmobiliare import VistaCreateUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaReadAssegnazione import VistaReadAssegnazione

class VistaGestioneRegistroAnagrafe(QWidget):

    def __init__(self, immobile):
        super(VistaGestioneRegistroAnagrafe, self).__init__()
        self.immobile = immobile
        main_layout = QVBoxLayout()

        find_layout = QGridLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Assegnazione")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per scala", "Ricerca per interno", "Ricerca per condomino"])
        self.searchType.activated.connect(self.avvia_ricerca)
        self.searchbar.textChanged.connect(self.avvia_ricerca)

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Scala", "Interno", "Nominativo condomino A-Z", "Nominativo condomino Z-A"])
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
        button_layout.addWidget(self.create_button("Visualizza Assegnazione", self.go_Read_Assegnazione, True))

        action_layout.addWidget(self.list_view_unitaImmobiliare)

        message_layout = QHBoxLayout()

        self.msg = QLabel("Non ci sono unità immobiliari")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        message_layout.addWidget(self.msg)
        action_layout.addLayout(button_layout)

        self.update_list()

        main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Unità Immobiliare")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setFixedSize(150, 55)
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
                return UnitaImmobiliare.ordinaUnitaImmobiliariByInterno, False
            self.update_list()
        elif self.sortType.currentIndex() == 1:
            if fromRicerca:
                return UnitaImmobiliare.ordinaUnitaImmobiliariByInterno, True
            self.update_list(decr=True)
        elif self.sortType.currentIndex() == 2:
            if fromRicerca:
                return UnitaImmobiliare.ordinaUnitaImmobiliariByName, False
            self.update_list(UnitaImmobiliare.ordinaUnitaImmobiliariByName, False)
        elif self.sortType.currentIndex() == 3:
            if fromRicerca:
                return UnitaImmobiliare.ordinaUnitaImmobiliariByName(), True
            self.update_list(UnitaImmobiliare.ordinaUnitaImmobiliariByName, True)
        else:
            print("Altro")

    def update_list(self, sorting_function=UnitaImmobiliare.ordinaUnitaImmobiliariByInterno, decr=False, searchActivated=False):
        print("class VistaGestioneImmobile - update_list inizio")
        self.lista_unitaImmobiliari = []
        self.lista_unitaImmobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values())
        if searchActivated and self.searchbar.text():
            print("sto cercando...")
            if self.searchType.currentIndex() == 0:  # ricerca per dati catastali
                self.lista_unitaImmobiliari = [item for item in self.lista_unitaImmobiliari if self.searchbar.text().upper() in item.interno.upper()]
            elif self.searchType.currentIndex() == 1:  # ricerca per nominativo condomino
                self.lista_unitaImmobiliari = [item for item in self.lista_unitaImmobiliari if self.searchbar.text().upper() in item.condomini.values().upper()]
        sorting_function(self.lista_unitaImmobiliari, decr)

        listview_model = QStandardItemModel(self.list_view_unitaImmobiliare)
        print("cazzi")
        for unitaImmobiliare in self.lista_unitaImmobiliari:
            item = QStandardItem()
            print(unitaImmobiliare.condomini)
            proprietario = [(item.cognome + " " + item.nome) for item in unitaImmobiliare.condomini.keys() if unitaImmobiliare.condomini[item] == "proprietario"]
            item_text = f"Scala {unitaImmobiliare.scala}  Int. {unitaImmobiliare.interno} {unitaImmobiliare.tipoUnitaImmobiliare} - PROPRIETARIO: {proprietario[0]}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)
        print("cazzi2", self.lista_unitaImmobiliari)

        if not self.lista_unitaImmobiliari:
            print("ciao")
            self.msg.setText("Non ci sono unità immobiliari assegnate all'immobile selezionato")
            self.msg.show()
            print("Non ci sono Unità Immobiliari assegante all'immobile")
            return None

        print("cazzi3")
        self.list_view_unitaImmobiliare.setModel(listview_model)

        self.selectionModel = self.list_view_unitaImmobiliare.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)


    def go_Add_Assegnazione(self):
        self.vista_nuova_Assegnazione = VistaCreateUnitaImmobiliare(self.immobile, callback=self.callback)
        self.vista_nuova_Assegnazione.show()

    def go_Read_Assegnazione(self):
        print("uiui")
        item = None
        print("uiui")
        for index in self.list_view_unitaImmobiliare.selectedIndexes():
            item = self.list_view_unitaImmobiliare.model().itemFromIndex(index)
            print(item.text())
        print(item.text().split(" "))
        sel_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareInterno(int(item.text().split(" ")[4]))
        print("si",sel_unitaImmobiliare.getInfoUnitaImmobiliare())
        self.vista_dettaglio_assegnazione = VistaReadAssegnazione(sel_unitaImmobiliare, callback=self.callback)
        self.vista_dettaglio_assegnazione.show()

    def go_Update_unitaImmobiliare(self):
        item = None
        for index in self.list_view_unitaImmobiliare.selectedIndexes():
            item = self.list_view_unitaImmobiliare.model().itemFromIndex(index)
            print(item.text())
        sel_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareInterno(int(item.text().split(" ")[0]))
        self.vista_modifica_unitaImmobiliare = VistaUpdateUnitaImmobiliare(sel_unitaImmobiliare, callback=self.callback)
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
        if not self.list_view_unitaImmobiliare.selectedIndexes():
            self.button_list["Visualizza Assegnazione"].setDisabled(True)
        else:
            self.button_list["Visualizza Assegnazione"].setDisabled(False)
    def callback(self, msg):
        self.button_list["Visualizza Assegnazione"].setDisabled(True)
        sort, desc = self.ordina_lista(True)
        self.update_list(sort, desc)
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()