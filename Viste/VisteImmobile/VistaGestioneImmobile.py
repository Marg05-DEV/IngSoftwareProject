from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, \
    QPushButton

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
        self.sortType.activated.connect(self.debugComboBox2)
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

        action_layout.addLayout(button_layout)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)

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

    def debugComboBox2(self, combo):
        print("pre")
        print("selected index SORTING: " + str(self.sortType.currentIndex()) + " -> " + str(self.sortType.currentText()))
        print("post")

    def update_list(self):
        print("cazzi1")

        print("cazzi2")
        self.lista_immobili = []
        self.lista_immobili = list(Immobile.getAllImmobili().values())
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
        self.vista_nuovo_immobile = VistaCreateImmobile(callback=self.update_list)
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
        self.vista_modifica_immobile = VistaUpdateImmobile(sel_immobile, callback=self.update_list)
        self.vista_modifica_immobile.show()

    def go_Delete_immobile(self):
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
        self.vista_elimina_immobile = VistaDeleteImmobile(sel_immobile, callback=self.update_list)
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
