from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, QPushButton

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Viste.VisteUnitaImmobiliare.VistaCreateUnitaImmobiliare import VistaCreateUnitaImmobiliare
from Viste.VisteUnitaImmobiliare.VistaDeleteUnitaImmobiliare import VistaDeleteUnitaImmobiliare
from Viste.VisteUnitaImmobiliare.VistaReadUnitaImmobiliare import VistaReadUnitaImmobiliare
from Viste.VisteUnitaImmobiliare.VistaUpdateUnitaImmobiliare import VistaUpdateUnitaImmobiliare


class VistaGestioneUnitaImmobiliare(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneUnitaImmobiliare, self).__init__(parent)

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
        self.sortType.activated.connect(self.debugComboBox2)
        find_layout.addWidget(searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(self.sortType, 1, 1)

        action_layout = QHBoxLayout()

        self.list_view_unitaImmobiliare = QListView()


        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Unità Immobiliare", self.go_Create_unitaImmobiliare))
        button_layout.addWidget(self.create_button("Visualizza Unità Immobiliare", self.go_Read_unitaImmobiliare, True))
        button_layout.addWidget(self.create_button("Modifica Unità Immobiliare", self.go_Update_unitaImmobiliare, True))
        button_layout.addWidget(self.create_button("Elimina Unità Immobiliare", self.go_Delete_unitaImmobiliare, True))

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
        print("cazzi1")

        print("cazzi2")
        self.lista_unitaImmobiliari = []
        self.lista_unitaImmobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliari().values())
        listview_model = QStandardItemModel(self.list_view_unitaImmobiliare)

        for unitaImmobiliare in self.lista_unitaImmobiliari:
            item = QStandardItem()
            item_text = f"{unitaImmobiliare.codice} {unitaImmobiliare.sigla} - {unitaImmobiliare.denominazione}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        self.list_view_unitaImmobiliare.setModel(listview_model)

    def go_Create_unitaImmobiliare(self):
        self.vista_nuovo_unitaImmobiliare = VistaCreateUnitaImmobiliare(callback=self.callback)
        self.vista_nuovo_unitaImmobiliare.show()

    def go_Read_unitaImmobiliare(self):
        item = None
        for index in self.list_view_unitaImmobiliare.selectedIndexes():
            item = self.list_view_unitaImmobiliare.model().itemFromIndex(index)
            print(item.text())
        sel_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareInterno(int(item.text().split(" ")[0]))
        self.vista_dettaglio_unitaImmobiliare = VistaReadUnitaImmobiliare(sel_unitaImmobiliare)
        self.vista_dettaglio_unitaImmobiliare.show()

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
            self.button_list["Visualizza Unità Immobiliare"].setDisabled(True)
            self.button_list["Modifica Unità Immobiliare"].setDisabled(True)
            self.button_list["Elimina Unità Immobiliare"].setDisabled(True)
        else:
            self.button_list["Visualizza Unità Immobiliare"].setDisabled(False)
            self.button_list["Modifica Unità Immobiliare"].setDisabled(False)
            self.button_list["Elimina Unità Immobiliare"].setDisabled(False)

    def callback(self, msg):
        self.update_list()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()