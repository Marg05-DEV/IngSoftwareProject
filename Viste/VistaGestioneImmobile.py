from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, \
    QPushButton

from Classes.RegistroAnagrafe.Immobile import Immobile


class VistaGestioneImmobile(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneImmobile, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QGridLayout()

        searchbar = QLineEdit()
        searchbar.setPlaceholderText("Ricerca...")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per denominazione", "Ricerca per sigla", "Ricerca per codice"])
        print(self.searchType.currentIndex)
        self.searchType.activated.connect(self.debugComboBox)
        sortLabel = QLabel("Ordina per:")
        sortType = QComboBox()
        sortType.addItems(["Denominazione A -> Z", "Denominazione Z -> A", "Sigla A -> Z", "Sigla Z -> A", "Codice crescente", "Codice decrescente"])
        find_layout.addWidget(searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(sortType, 1, 1)

        action_layout = QHBoxLayout()

        print("1")
        self.lista_immobili = QListView()
        print("2")
        self.update_list()
        print("3")
        button_layout = QVBoxLayout()

        createBtn = QPushButton("Aggiungi Immobile")
        readBtn = QPushButton("Visualizza Immobile")
        updateBtn = QPushButton("Modifica immobile")
        deleteBtn = QPushButton("Elimina Immobile")

        button_layout.addWidget(createBtn)
        button_layout.addWidget(readBtn)
        button_layout.addWidget(updateBtn)
        button_layout.addWidget(deleteBtn)

        action_layout.addWidget(self.lista_immobili)
        action_layout.addLayout(button_layout)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Immobile")

    def debugComboBox(self, combo):
        print("pre")
        print("selected index: " + str(self.searchType.currentIndex()) + " -> " + str(self.searchType.currentText()))
        print("post")

    def update_list(self):
        print("2.1")
        self.lista_immobili = []
        print(type(Immobile.getAllImmobili()))
        self.lista_immobili.extend(Immobile.getAllImmobili())
        print("2.2")
        listview_model = QStandardItemModel(self.lista_immobili)
        for immobile in self.lista_immobili:
            item = QStandardItem()
            item_text = f"{immobile.codice} {immobile.sigla} - {immobile.denominazione}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(18)
            item.setFont(font)
            listview_model.appendRow(item)
            print("2.3")
        self.lista_immobili.setModel(listview_model)
