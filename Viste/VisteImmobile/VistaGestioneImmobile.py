from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, QPushButton

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
        self.sortType.activated.connect(self.ordina_lista)
        find_layout.addWidget(searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(self.sortType, 1, 1)

        action_layout = QHBoxLayout()

        self.list_view_immobili = QListView()


        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Immobile", self.go_Create_immobile))
        button_layout.addWidget(self.create_button("Visualizza Immobile", self.go_Read_immobile, True))
        button_layout.addWidget(self.create_button("Modifica Immobile", self.go_Update_immobile, True))
        button_layout.addWidget(self.create_button("Elimina Immobile", self.go_Delete_immobile, True))

        action_layout.addWidget(self.list_view_immobili)

        self.update_list()

        self.selectionModel = self.list_view_immobili.selectionModel()
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
        self.setWindowTitle("Gestione Immobile")

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

    def ordina_lista(self):
        print("pre")
        print("selected index SORTING: " + str(self.sortType.currentIndex()) + " -> " + str(self.sortType.currentText()))
        print("post")
        if self.sortType.currentIndex() == 0:
            self.update_list()
        elif self.sortType.currentIndex() == 1:
            self.update_list(decr=True)
        elif self.sortType.currentIndex() == 2:
            self.update_list(Immobile.ordinaImmobileBySigla)
        elif self.sortType.currentIndex() == 3:
            self.update_list(Immobile.ordinaImmobileBySigla, True)
        elif self.sortType.currentIndex() == 4:
            self.update_list(Immobile.ordinaImmobileByCodice)
        elif self.sortType.currentIndex() == 5:
            self.update_list(Immobile.ordinaImmobileByCodice, True)
        else:
            print("Altro")

    def update_list(self, sorting_function=Immobile.ordinaImmobileByDenominazione, decr=False):
        self.lista_immobili = []
        self.lista_immobili = list(Immobile.getAllImmobili().values())
        sorting_function(self.lista_immobili, decr)
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


    def go_Create_immobile(self):
        self.vista_nuovo_immobile = VistaCreateImmobile(callback=self.callback)
        self.vista_nuovo_immobile.show()

    def go_Read_immobile(self):
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
        self.vista_dettaglio_immobile = VistaReadImmobile(sel_immobile)
        self.vista_dettaglio_immobile.show()

    def go_Update_immobile(self):
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
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
        print("selezione cambiata")
        if not self.list_view_immobili.selectedIndexes():
            self.button_list["Visualizza Immobile"].setDisabled(True)
            self.button_list["Modifica Immobile"].setDisabled(True)
            self.button_list["Elimina Immobile"].setDisabled(True)
        else:
            self.button_list["Visualizza Immobile"].setDisabled(False)
            self.button_list["Modifica Immobile"].setDisabled(False)
            self.button_list["Elimina Immobile"].setDisabled(False)

    def callback(self, msg):
        self.update_list()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()

