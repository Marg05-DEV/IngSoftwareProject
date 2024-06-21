from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QHBoxLayout, QListView, QLabel, \
    QPushButton
from Classes.Contabilita.spesa import Spesa

class VistaGestioneSpese(QWidget):
    def __init__(self, parent=None, sortLabel=None):
        super(VistaGestioneSpese, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QGridLayout()

        searchbar = QLineEdit()
        searchbar.setPlaceholderText("Ricerca Spesa")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per denominazione", "Ricerca per sigla", "Ricerca per codice"])
        self.searchType.activated.connect(self.debugComboBox1)

        self.sortType.addItems(
            ["Data Di pagamento", "Tipo di Spesa A -> Z", "tipo di Spesa Z -> A", "Immobile A -> Z","Immobile Z -> A", "Fornitore A -> Z",
             "Fornitore Z -> A"])
        self.sortType.activated.connect(self.debugComboBox2)
        find_layout.addWidget(searchbar, 0, 0, 1, 3)
        find_layout.addWidget(self.searchType, 0, 3)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(self.sortType, 1, 1)

        action_layout = QHBoxLayout()

        self.list_view_spese = QListView()

        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Spesa", self.go_Create_spesa))
        button_layout.addWidget(self.create_button("Visualizza Spesa", self.go_Read_spesa, True))
        button_layout.addWidget(self.create_button("Modifica Spesa", self.go_Update_spesa, True))
        button_layout.addWidget(self.create_button("Elimina Spesa", self.go_Delete_spesa, True))

        action_layout.addWidget(self.list_view_spesa)

        self.update_list()

        self.selectionModel = self.list_view_spesa.selectionModel()
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
        self.setWindowTitle("Gestione Spese")

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
        self.lista_spese = []
        self.lista_spese = list(Spesa.getAllSpese().values())
        listview_model = QStandardItemModel(self.list_view_spese)

        for spese in self.lista_spese:
            item = QStandardItem()
            item_text = f"{unitaImmobiliare.interno} {unitaImmobiliare.immobile} - {unitaImmobiliare.condomini}"
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