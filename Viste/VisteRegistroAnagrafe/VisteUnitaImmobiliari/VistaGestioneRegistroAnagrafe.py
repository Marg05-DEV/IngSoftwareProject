import os
import webbrowser

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, \
    QPushButton, QSizePolicy, QSpacerItem

from Classes.Gestione.gestoreRegistroAnagrafe import GestoreRegistroAnagrafe
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
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
        #button_layout.addSpacerItem(QSpacerItem(20, 75, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        button_layout.addWidget(self.create_button("Aggiungi Assegnazione", self.go_Add_Assegnazione))
        #button_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        button_layout.addWidget(self.create_button("Visualizza Assegnazione", self.go_Read_Assegnazione, True))
        #button_layout.addSpacerItem(QSpacerItem(20, 75, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        action_layout.addWidget(self.list_view_unitaImmobiliare)

        bottom_layout = QVBoxLayout()

        self.msg = QLabel("Non ci sono unità immobiliari")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        bottom_layout.addWidget(self.msg)
        bottom_layout.addWidget(self.create_button("Mostra Registro Anagrafe Condominiale", self.go_pdf_RegAn), Qt.AlignmentFlag.AlignCenter)
        action_layout.addLayout(button_layout)

        self.lista_unitaImmobiliari = []
        self.update_list()

        main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Registro Anagrafe Condominiale dell'immobile: " + self.immobile.denominazione)

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        if testo == "Mostra Registro Anagrafe Condominiale":
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        else:
            button.setMaximumHeight(40)
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
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
        if self.searchbar.text():
            sorting, desc = self.ordina_lista(True)
            self.update_list(sorting, desc, True)
        else:
            self.ordina_lista(False)

    def ordina_lista(self, fromRicerca=False):
        if self.sortType.currentIndex() == 0: #scala
            if fromRicerca:
                return GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByScala, False
            self.update_list()
        elif self.sortType.currentIndex() == 1: #interno
            if fromRicerca:
                return GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByInterno, False
            self.update_list(GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByInterno)
        elif self.sortType.currentIndex() == 2: #nominativo proprietario A - Z
            if fromRicerca:
                return GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByNominativoProprietario, False
            self.update_list(GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByNominativoProprietario, False)
        elif self.sortType.currentIndex() == 3: #nominativo proprietario Z - A
            if fromRicerca:
                return GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByNominativoProprietario, True
            self.update_list(GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByNominativoProprietario, True)
        else:
            print("Altro")

    def update_list(self, sorting_function=GestoreRegistroAnagrafe.ordinaUnitaImmobiliariByScala, decr=False, searchActivated=False):
        self.lista_unitaImmobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values())

        if searchActivated and self.searchbar.text():
            print("sto cercando...")
            if self.searchType.currentIndex() == 0:  # ricerca per scala
                self.lista_unitaImmobiliari = [item for item in self.lista_unitaImmobiliari if self.searchbar.text().upper() in str(item.scala).upper()]
            if self.searchType.currentIndex() == 1:  # ricerca per interno
                self.lista_unitaImmobiliari = [item for item in self.lista_unitaImmobiliari if self.searchbar.text().upper() in str(item.interno).upper()]
            elif self.searchType.currentIndex() == 2:  # ricerca per nominativo condomino
                condomini = {item.codice: '    '.join([Condomino.ricercaCondominoByCF(cf).cognome + " " + Condomino.ricercaCondominoByCF(cf).nome for cf in item.condomini.keys()])
                             for item in self.lista_unitaImmobiliari}

                self.lista_unitaImmobiliari = [UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(item) for item in condomini.keys() if self.searchbar.text().upper() in condomini[item].upper()]
        sorting_function(self.lista_unitaImmobiliari, decr)


        if not self.lista_unitaImmobiliari:
            self.msg.setText("Non ci sono unità immobiliari assegnate all'immobile selezionato")
            self.msg.show()

        listview_model = QStandardItemModel(self.list_view_unitaImmobiliare)
        for unitaImmobiliare in self.lista_unitaImmobiliari:
            item = QStandardItem()
            print(unitaImmobiliare.condomini)
            proprietario = [(Condomino.ricercaCondominoByCF(item).cognome + " " + Condomino.ricercaCondominoByCF(item).nome) for item in unitaImmobiliare.condomini.keys() if unitaImmobiliare.condomini[item] == "Proprietario"]
            if not proprietario:
                proprietario_text = "Nessun proprietario"
                if not unitaImmobiliare.condomini:
                    proprietario_text = "Nessun condomino"
            else:
                proprietario_text = "PROPRIETARIO: " + proprietario[0]

            if unitaImmobiliare.tipoUnitaImmobiliare.upper() == "APPARTAMENTO":
                item_text = f"{unitaImmobiliare.tipoUnitaImmobiliare} Scala {unitaImmobiliare.scala}  Int. {unitaImmobiliare.interno} - {proprietario_text}"
            else:
                item_text = f"{unitaImmobiliare.tipoUnitaImmobiliare} - {proprietario_text}"
            item.setData(unitaImmobiliare.codice)
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        self.list_view_unitaImmobiliare.setModel(listview_model)
        self.list_view_unitaImmobiliare.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.selectionModel = self.list_view_unitaImmobiliare.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)


    def go_Add_Assegnazione(self):
        self.vista_nuova_Assegnazione = VistaCreateUnitaImmobiliare(self.immobile, callback=self.callback)
        self.vista_nuova_Assegnazione.show()

    def go_Read_Assegnazione(self):
        item = None
        for index in self.list_view_unitaImmobiliare.selectedIndexes():
            item = self.list_view_unitaImmobiliare.model().itemFromIndex(index)
        sel_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(item.data())
        self.vista_dettaglio_assegnazione = VistaReadAssegnazione(sel_unitaImmobiliare, self.immobile, callback=self.callback)
        self.vista_dettaglio_assegnazione.show()

    def go_pdf_RegAn(self):
        pdf = GestoreRegistroAnagrafe.generaPDFRegistroAnagrafeCondominiale(self.immobile)
        directory_files = os.path.dirname(os.path.abspath(__file__)).replace(
            "Viste\\VisteRegistroAnagrafe\\VisteUnitaImmobiliari", "Dati\\pdf\\")
        print(directory_files)

        pdf.output(directory_files + self.immobile.sigla + "\\RegistroAnagrafeCondominiale.pdf")
        webbrowser.open(directory_files + f"{self.immobile.sigla}\\RegistroAnagrafeCondominiale.pdf")

    def able_button(self):
        if not self.list_view_unitaImmobiliare.selectedIndexes():
            self.button_list["Visualizza Assegnazione"].setDisabled(True)
        else:
            self.button_list["Visualizza Assegnazione"].setDisabled(False)

    def callback(self, msg=""):
        self.button_list["Visualizza Assegnazione"].setDisabled(True)
        self.searchbar.clear()
        self.searchType.clear()
        self.searchType.addItems(["Ricerca per scala", "Ricerca per interno", "Ricerca per condomino"])
        sort, desc = self.ordina_lista(True)
        self.update_list(sort, desc)
        if msg:
            self.msg.setText(msg)
            self.msg.show()
            self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.lista_unitaImmobiliari:
            self.msg.setText("Non ci sono unità immobiliari assegnate all'immobile selezionato")
            self.msg.show()