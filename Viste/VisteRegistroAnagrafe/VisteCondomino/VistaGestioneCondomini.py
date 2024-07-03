from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QListView, QLabel, QHBoxLayout, QPushButton, QComboBox, \
    QLineEdit

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaReadCondomino import VistaReadCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaUpdateCondomino import VistaUpdateCondomino


class VistaGestioneCondomini(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneCondomini, self).__init__(parent)
        print("sono in gestione condomini")
        main_layout = QVBoxLayout()

        find_layout = QGridLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca...")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca nome"])
        self.searchType.activated.connect(self.avvia_ricerca)
        self.searchbar.textChanged.connect(self.avvia_ricerca)

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Nome A -> Z", "Nome Z -> A"])
        self.sortType.activated.connect(self.avvia_ordinamento)
        find_layout.addWidget(self.searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(self.sortType, 1, 1)


        action_layout = QHBoxLayout()

        self.list_view_condomino = QListView()


        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Visualizza Condomino", self.go_Read_condomino, True))
        button_layout.addWidget(self.create_button("Modifica Condomino", self.go_Update_condomino, True))

        action_layout.addWidget(self.list_view_condomino)

        self.update_list()

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
        self.setWindowTitle("Gestione Condomino")
        print("fine classe VistaGestioneCondomini")

    def create_button(self, testo, action, disabled=False):
        print("bottoni ok")
        button = QPushButton(testo)
        button.setFixedSize(110, 55)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        print("uscita bottone")
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
                return Condomino.ricercaCondominoByNome, False
            self.update_list()
        elif self.sortType.currentIndex() == 1:
            if fromRicerca:
                return Condomino.ricercaCondominoByNome, True
            self.update_list(decr=True)
        else:
            print("Altro")

    def update_list(self, sorting_function=Condomino.ordinaCondominoByName, decr=False, searchActivated=False):
        print("dentro a update list")
        self.lista_condomini = []
        self.lista_condomini = list(Condomino.getAllCondomini().values())
        print(Condomino.getAllCondomini().values())
        print(searchActivated and self.searchbar.text())
        if searchActivated and self.searchbar.text():
            print("sto cercando...")
            if self.searchType.currentIndex() == 0:
                self.lista_condomini = [item for item in self.lista_condomini if self.searchbar.text().upper() in item.nome.upper()]
        print(self.lista_condomini)
        sorting_function(self.lista_condomini, decr)
        print(self.lista_condomini)
        print("ciao 1")
        listview_model = QStandardItemModel(self.list_view_condomino)

        for condomino in self.lista_condomini:
            item = QStandardItem()
            item_text = f"{condomino.codice} {condomino.nome} - {condomino.cognome}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        if not self.lista_condomini:
            print("ciao")
            self.msg.setText("Non ci sono unità immobiliari assegnate all'immobile selezionato")
            self.msg.show()
            print("Non ci sono Unità Immobiliari assegante all'immobile")
            return None

        self.list_view_condomino.setModel(listview_model)

        self.selectionModel = self.list_view_condomino.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)

    def go_Read_condomino(self):
        item = None
        for index in self.list_view_condomino.selectedIndexes():
            item = self.list_view_condomino.model().itemFromIndex(index)
            print(item.text())
        sel_condomino = Condomino.ricercaCondominoByNome(item.text().split(" ")[1])
        self.vista_dettaglio_condomino = VistaReadCondomino(sel_condomino, self.callback)
        self.vista_dettaglio_condomino.show()

    def go_Update_condomino(self):
        item = None
        for index in self.list_view_condomino.selectedIndexes():
            item = self.list_view_condomino.model().itemFromIndex(index)
            print(item.text())
        sel_condomino = Condomino.ricercaCondominoByNome(item.text().split(" ")[1])
        self.vista_modifica_condomino = VistaUpdateCondomino(sel_condomino, callback=self.callback)
        self.vista_modifica_condomino.show()


    def able_button(self):
        print("selezione cambiata")
        if not self.list_view_condomino.selectedIndexes():
            self.button_list["Visualizza Condomino"].setDisabled(True)
            self.button_list["Modifica Condomino"].setDisabled(True)
        else:
            self.button_list["Visualizza Condomino"].setDisabled(False)
            self.button_list["Modifica Condomino"].setDisabled(False)

    def callback(self, msg):
        self.update_list()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()