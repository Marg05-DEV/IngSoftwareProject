from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, \
    QListWidget, QListView, QTableWidget, QTableWidgetItem
from PyQt6.uic.properties import QtWidgets

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteImmobile import VistaGestioneImmobile
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaDeleteUnitaImmobiliare  import VistaDeleteUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaUpdateUnitaImmobiliare import VistaUpdateUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaCreateCondomino import VistaCreateCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaUpdateCondomino import VistaUpdateCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaDeleteCondomino import VistaDeleteCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaReadCondomino import VistaReadCondomino


class VistaReadAssegnazione(QWidget):

    def __init__(self, sel_unitaImmobiliare, immobile, callback):
        super(VistaReadAssegnazione, self).__init__()
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
        self.immobile = immobile
        self.callback = callback
        main_layout = QGridLayout()

        lbl_frase = QLabel("INFORMAZIONI UNITA' IMMOBILIARE:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addWidget(self.new_label("Tipologia Unità Immobiliare", "tipoUnitaImmobiliare"), 1, 0, 1, 2)
        main_layout.addWidget(self.new_label("Scala", "scala"), 2, 0)
        main_layout.addWidget(self.new_label("Interno", "interno"),2, 1)

        lbl_frase1 = QLabel("DATI CATASTALI: ")
        lbl_frase1.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(lbl_frase1, 3, 0, 1, 2)

        main_layout.addWidget(self.new_label("Foglio", "foglio"), 4, 0)
        main_layout.addWidget(self.new_label("Particella", "particella"), 4, 1)
        main_layout.addWidget(self.new_label("Subalterno", "subalterno"), 5, 0)
        main_layout.addWidget(self.new_label("ZC", "ZC"), 5, 1)
        main_layout.addWidget(self.new_label("Classe", "classe"), 6, 0)
        main_layout.addWidget(self.new_label("Categoria", "categoria"), 6, 1)
        print("FINE GRID")

        self.create_table()

        """
        # Crea la tabella
        self.table = QTableWidget()
        self.table.setRowCount(2)  # Imposta il numero di righe
        self.table.setColumnCount(6)  # Imposta il numero di colonne
        self.table.setHorizontalHeaderLabels(["Proprietà", "Valore"])  # Imposta le intestazioni delle colonne

        # Aggiungi i dati alla tabella
        self.table.setItem(0, 0, QTableWidgetItem("Foglio"))
        self.table.setItem(0, 1, QTableWidgetItem("foglio"))

        self.table.setItem(1, 0, QTableWidgetItem("Particella"))
        self.table.setItem(1, 1, QTableWidgetItem("particella"))

        self.table.setItem(2, 0, QTableWidgetItem("Subalterno"))
        self.table.setItem(2, 1, QTableWidgetItem("subalterno"))

        self.table.setItem(3, 0, QTableWidgetItem("ZC"))
        self.table.setItem(3, 1, QTableWidgetItem("ZC"))

        self.table.setItem(4, 0, QTableWidgetItem("Classe"))
        self.table.setItem(4, 1, QTableWidgetItem("classe"))

        self.table.setItem(5, 0, QTableWidgetItem("Categoria"))
        self.table.setItem(5, 1, QTableWidgetItem("categoria"))

        # Aggiungi la tabella al layout
        main_layout.addWidget(self.table, 1, 0, 1, 2)
        """
        self.button_list = {}
        main_layout.addWidget(self.create_button("Modifica Unità Immobiliare", self.updateUnitaImmobiliare), 7, 0, 1, 2)
        main_layout.addWidget(self.create_button("Rimuovi Unità Immobiliare", self.deleteUnitaImmobiliare), 8, 0, 1, 2)
        print("Prossimo problema")

        condomini_label = QLabel("CONDOMINI ASSEGNATI:")
        condomini_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(condomini_label, 9, 0, 1, 2)

        self.list_view_condomini = QListView()
        main_layout.addWidget(self.list_view_condomini, 10, 0, 5, 2)

        self.msg = QLabel("Non ci sono condomini assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addWidget(self.msg, 16, 0, 1, 2)

        main_layout.addWidget(self.create_button("Aggiungi Condomino", self.addCondomino), 17, 0, 1, 2)
        main_layout.addWidget(self.create_button("Modifica Condomino", self.updateCondomino, True), 18, 0, 1, 2)
        main_layout.addWidget(self.create_button("Visualizza Condomino", self.readCondomino, True), 19, 0, 1, 2)
        main_layout.addWidget(self.create_button("Rimuovi Condomino", self.deleteCondomino, True), 20, 0, 1, 2)

        self.update_list()

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Assegnazione")


    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def create_table(self):
        self.dati_catastali = self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()
        columns = len(self.dati_catastali)
        rows = 2

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(columns)

    def new_label(self, testo, index):
        label = QLabel(testo + ": " + str(self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[index]))
        return label

    def update_list(self):

        if not self.sel_unitaImmobiliare.condomini:
            self.msg.setText("Non ci sono condomini assegnati all'unità immobiliare")
            self.msg.show()
        else:
            self.msg.hide()
        print("dentro a update 3")
        listview_model = QStandardItemModel(self.list_view_condomini)
        print(self.sel_unitaImmobiliare.condomini.items())
        for condomino_cf, titolo in self.sel_unitaImmobiliare.condomini.items():
            item = QStandardItem()
            condomino = Condomino.ricercaCondominoByCF(condomino_cf)
            item_text = f"{condomino.nome}  {condomino.cognome} - {condomino_cf} ({titolo.upper()})"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        print("qui finisce")
        self.list_view_condomini.setModel(listview_model)
        self.selectionModel = self.list_view_condomini.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)

    def closeEvent(self, event):
        self.callback()

    def updateUnitaImmobiliare(self):
        self.modifica_unitaImmobiliare = VistaUpdateUnitaImmobiliare(self.sel_unitaImmobiliare, callback=self.callback)
        self.close()
        self.modifica_unitaImmobiliare.show()

    def deleteUnitaImmobiliare(self):
        self.rimuovi_unitaImmobiliare = VistaDeleteUnitaImmobiliare(self.sel_unitaImmobiliare, callback=self.callback)
        self.close()
        self.rimuovi_unitaImmobiliare.show()

    def addCondomino(self):
        self.vista_nuovo_condomino = VistaCreateCondomino(self.immobile, self.sel_unitaImmobiliare, self.lista_condomini_callback,  False)
        self.vista_nuovo_condomino.show()

    def updateCondomino(self):
        item = None
        print(self.list_view_condomini.selectedIndexes())
        for index in self.list_view_condomini.selectedIndexes():
            item = self.list_view_condomini.model().itemFromIndex(index)
        print(item.text().split(" (")[0].split(" - ")[1])
        sel_condomino = Condomino.ricercaCondominoByCF(item.text().split(" (")[0].split(" - ")[1])
        print("si va a modificare", sel_condomino)
        self.vista_modifica_condomino = VistaUpdateCondomino(sel_condomino, self.lista_condomini_callback, self.sel_unitaImmobiliare, onlyAnagrafica=False)
        print("si va a modificare")
        self.vista_modifica_condomino.show()

    def readCondomino(self):
        item = None
        for index in self.list_view_condomini.selectedIndexes():
            item = self.list_view_condomini.model().itemFromIndex(index)
        sel_condomino = Condomino.ricercaCondominoByCF(item.text().split(" (")[0].split(" - ")[1])
        self.vista_visualizza_condomino = VistaReadCondomino(sel_condomino, self.lista_condomini_callback, True, self.sel_unitaImmobiliare)
        self.vista_visualizza_condomino.show()

    def deleteCondomino(self):
        item = None
        for index in self.list_view_condomini.selectedIndexes():
            item = self.list_view_condomini.model().itemFromIndex(index)
        sel_condomino = Condomino.ricercaCondominoByCF(item.text().split(" (")[0].split(" - ")[1])
        self.vista_rimuovi_condomino = VistaDeleteCondomino(sel_condomino, self.sel_unitaImmobiliare, callback=self.lista_condomini_callback)
        self.vista_rimuovi_condomino.show()

    def able_button(self):
        print("selezione cambiata")
        print("lista button", self.button_list)
        if not self.list_view_condomini.selectedIndexes():
            self.button_list["Modifica Condomino"].setDisabled(True)
            self.button_list["Visualizza Condomino"].setDisabled(True)
            self.button_list["Rimuovi Condomino"].setDisabled(True)
        else:
            self.button_list["Modifica Condomino"].setDisabled(False)
            self.button_list["Visualizza Condomino"].setDisabled(False)
            self.button_list["Rimuovi Condomino"].setDisabled(False)

    def lista_condomini_callback(self, msg):
        self.button_list["Modifica Condomino"].setDisabled(True)
        self.button_list["Visualizza Condomino"].setDisabled(True)
        self.button_list["Rimuovi Condomino"].setDisabled(True)
        self.sel_unitaImmobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.sel_unitaImmobiliare.codice)
        self.update_list()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
