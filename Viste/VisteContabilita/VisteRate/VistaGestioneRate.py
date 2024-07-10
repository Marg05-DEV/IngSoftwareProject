from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QLabel, QWidget, QTableWidget, QPushButton, \
    QSizePolicy

from Classes.Contabilita.rata import Rata

class VistaGestioneRate(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneRate, self).__init__(parent)

        main_layout = QVBoxLayout()

        find_layout = QHBoxLayout()
        
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca...")
        self.searchType = QComboBox()
        self.searchType.addItems(["Ricerca per data di pagamento", "Ricerca per denominazione dell'immobile", "Ricerca per nome del versante"])
        self.searchType.activated.connect(self.avvia_ricerca)
        self.searchbar.textChanged.connect(self.avvia_ricerca)

        find_layout.addWidget(self.searchbar)
        find_layout.addWidget(self.searchType)
        print("ciao")
        sort_layout = QHBoxLayout()

        sortLabel = QLabel("Ordina per:")
        self.sortType = QComboBox()

        self.sortType.addItems(
            ["Ultimo inserimento", "Data di pagamento", "Denominazione Immobile A -> Z", "Denominazione Immobile Z -> A", "Nominativo versante A -> Z", "Nominativo versante Z -> A"])
        self.sortType.activated.connect(self.avvia_ordinamento)
        sort_layout.addWidget(sortLabel)
        sort_layout.addWidget(self.sortType)
        print("ciao")
        self.table_rate = QTableWidget()

        button_layout = QHBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Rata", self.goCreateRata))
        button_layout.addWidget(self.create_button("Visualizza Rata", self.goReadRata,True))
        button_layout.addWidget(self.create_button("Modifica Rata", self.goUpdateRata, True))
        button_layout.addWidget(self.create_button("Elimina Rata", self.goDeleteRata, True))
        button_layout.addWidget(self.create_button("Visualizza Ricevuta", self.goReadRicevuta, True))
        print("ciao")
        message_layout = QHBoxLayout()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()
        print("ciao")
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)
        print("ciao")
        self.lista_rate = []
        self.update_table()

        message_layout.addWidget(self.msg)
        print("ciao")
        main_layout.addLayout(find_layout)
        main_layout.addLayout(sort_layout)
        main_layout.addWidget(self.table_rate)
        main_layout.addLayout(message_layout)
        main_layout.addLayout(button_layout)
        print("ciao")
        self.setLayout(main_layout)
        self.resize(600, 400)
        print("ciao")
        self.setWindowTitle("Gestione Rate")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def avvia_ricerca(self):
        """
        sorting, desc = self.ordina_lista(True)
        self.update_table(sorting, desc, True)
        """

    def avvia_ordinamento(self):
        """
        if self.searchbar.text():
            sorting, desc = self.ordina_lista(True)
            self.update_table(sorting, desc, True)
        else:
            self.ordina_lista(False)
        """


    def ordina_lista(self, fromRicerca=False):
        """
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
        """
        pass


    def update_table(self): #, sorting_function=Rata.ordinaImmobileByDenominazione, decr=False, searchActivated=False ):
        """
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
        """
        pass

    def goCreateRata(self):
        """
        self.vista_nuovo_immobile = VistaCreateImmobile(callback=self.callback)
        self.vista_nuovo_immobile.show()
        """
        pass

    def goReadRata(self):
        """
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
        self.vista_dettaglio_immobile = VistaReadImmobile(sel_immobile, callback=self.callback)
        self.vista_dettaglio_immobile.show()
        """
        pass

    def goUpdateRata(self):
        """
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
        """
        pass

    def goDeleteRata(self):
        """
        item = None
        for index in self.list_view_immobili.selectedIndexes():
            item = self.list_view_immobili.model().itemFromIndex(index)
            print(item.text())
        sel_immobile = Immobile.ricercaImmobileByCodice(int(item.text().split(" ")[0]))
        self.vista_elimina_immobile = VistaDeleteImmobile(sel_immobile, callback=self.callback)
        self.vista_elimina_immobile.show()
        """
        pass

    def goReadRicevuta(self):
        pass

    def able_button(self):
        if not self.list_view_rate.selectedIndexes():
            self.button_list["Visualizza Rata"].setDisabled(True)
            self.button_list["Modifica Rata"].setDisabled(True)
            self.button_list["Elimina Rata"].setDisabled(True)
            self.button_list["Visualizza Ricevuta"].setDisabled(True)
        else:
            self.button_list["Visualizza Rata"].setDisabled(False)
            self.button_list["Modifica Rata"].setDisabled(False)
            self.button_list["Elimina Rata"].setDisabled(False)
            self.button_list["Visualizza Ricevuta"].setDisabled(False)


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

