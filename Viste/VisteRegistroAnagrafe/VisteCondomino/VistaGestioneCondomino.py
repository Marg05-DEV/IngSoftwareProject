from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QListView, QLabel, QHBoxLayout, QPushButton

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaAddCondomino import VistaAddCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaDeleteCondomino import VistaDeleteCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaReadCondomino import VistaReadCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaUpdateCondomino import VistaUpdateCondomino


class VistaGestioneCondomino(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneCondomino, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QGridLayout()
        """
        searchbar = QLineEdit()
        searchbar.setPlaceholderText("Ricerca...")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per denominazione", "Ricerca per sigla", "Ricerca per codice"])
        self.searchType.activated.connect(self.debugComboBox1)

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Denominazione A -> Z", "Denominazione Z -> A", "Sigla A -> Z", "Sigla Z -> A", "Codice crescente",
             "Codice decrescente"])
        self.sortType.activated.connect(self.debugComboBox2)
        find_layout.addWidget(searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(self.sortType, 1, 1)
        """

        action_layout = QHBoxLayout()

        self.list_view_condomino = QListView()


        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Condomino", self.go_Create_condomino))
        button_layout.addWidget(self.create_button("Visualizza Condomino", self.go_Read_condomino, True))
        button_layout.addWidget(self.create_button("Modifica Condomino", self.go_Update_condomino, True))
        button_layout.addWidget(self.create_button("Elimina Condomino", self.go_Delete_condomino, True))

        action_layout.addWidget(self.list_view_condomino)

        self.update_list()

        self.selectionModel = self.list_view_condomino.selectionModel()
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

        #main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Condomino")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setFixedSize(110, 55)
        button.setCheckable(True)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def debugComboBox1(self, combo):
        print("pre")
        print("selected index SEARCHING: " + str(self.searchType.currentIndex()) + " -> " + str(self.searchType.currentText()))
        print("post")

    def debugComboBox2(self, combo):
        print("pre")
        print("selected index SORTING: " + str(self.sortType.currentIndex()) + " -> " + str(self.sortType.currentText()))
        print("post")

    def update_list(self):
        self.lista_condomini = []
        self.lista_condomini = list(Condomino.getAllCondomini().values())
        listview_model = QStandardItemModel(self.list_view_condomino)

        for condomino in self.lista_condomini:
            item = QStandardItem()
            item_text = f"{condomino.codice} {condomino.nome} - {condomino.cognome} - {condomino.unitaImmobiliare}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        self.list_view_condomino.setModel(listview_model)

    def go_Create_condomino(self):
        self.vista_nuovo_condomino = VistaAddCondomino(callback=self.callback)
        self.vista_nuovo_condomino.show()

    def go_Read_condomino(self):
        item = None
        for index in self.list_view_condomino.selectedIndexes():
            item = self.list_view_condomino.model().itemFromIndex(index)
            print(item.text())
        sel_condomino = Condomino.ricercaUnitaImmobiliareInterno(int(item.text().split(" ")[0]))
        self.vista_dettaglio_condomino = VistaReadCondomino(sel_condomino)
        self.vista_dettaglio_condomino.show()

    def go_Update_condomino(self):
        item = None
        for index in self.list_view_condomino.selectedIndexes():
            item = self.list_view_condomino.model().itemFromIndex(index)
            print(item.text())
        sel_condomino = Condomino.ricercaCondominoByNome(int(item.text().split(" ")[0]))
        self.vista_modifica_condomino = VistaUpdateCondomino(sel_condomino, callback=self.callback)
        self.vista_modifica_condomino.show()

    def go_Delete_condomino(self):
        item = None
        for index in self.list_view_condomino.selectedIndexes():
            item = self.list_view_condomino.model().itemFromIndex(index)
            print(item.text())
        sel_condomino = Condomino.ricercaCondominoByNome(int(item.text().split(" ")[0]))
        self.vista_elimina_condomino = VistaDeleteCondomino(sel_condomino, callback=self.callback)
        self.vista_elimina_condomino.show()


    def able_button(self):
        print("selezione cambiata")
        if not self.list_view_condomino.selectedIndexes():
            self.button_list["Visualizza Condomino"].setDisabled(True)
            self.button_list["Modifica Condomino"].setDisabled(True)
            self.button_list["Elimina Condomino"].setDisabled(True)
        else:
            self.button_list["Visualizza Condomino"].setDisabled(False)
            self.button_list["Modifica Condomino"].setDisabled(False)
            self.button_list["Elimina Condomino"].setDisabled(False)

    def callback(self, msg):
        self.update_list()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()