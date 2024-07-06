from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView, \
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView

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
        """
        main_layout.addWidget(self.new_label("Foglio", "foglio"), 4, 0)
        main_layout.addWidget(self.new_label("Particella", "particella"), 4, 1)
        main_layout.addWidget(self.new_label("Subalterno", "subalterno"), 5, 0)
        main_layout.addWidget(self.new_label("ZC", "ZC"), 5, 1)
        main_layout.addWidget(self.new_label("Classe", "classe"), 6, 0)
        main_layout.addWidget(self.new_label("Categoria", "categoria"), 6, 1)
        print("FINE GRID")
        """
        self.table_dati_catastali = self.create_table()
        main_layout.addWidget(self.table_dati_catastali, 5, 0, 1, 2)

        self.button_list = {}
        main_layout.addWidget(self.create_button("Modifica Unità Immobiliare", self.updateUnitaImmobiliare), 7, 0, 1, 2)
        main_layout.addWidget(self.create_button("Rimuovi Unità Immobiliare", self.deleteUnitaImmobiliare), 8, 0, 1, 2)
        print("Prossimo problema")

        condomini_label = QLabel("CONDOMINI ASSEGNATI:")
        condomini_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(condomini_label, 9, 0, 1, 2)

        self.list_view_condomini = QListView()
        self.list_view_condomini.setAlternatingRowColors(True)
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
        table = QTableWidget()
        table.setRowCount(1)
        table.setColumnCount(6)
        print("create tabella")

        dati_catastali = self.sel_unitaImmobiliare.getDatiCatastali()
        print("create tabella")

        header = list(dati_catastali.keys())
        dati = list(dati_catastali.values())
        print("create tabella")

        i = 0
        for h in header:
            item = QTableWidgetItem(h)
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setHorizontalHeaderItem(i, item)
            i += 1
        print("create tabella")

        i = 0
        for d in dati:
            item = QTableWidgetItem(str(d))
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(0, i, item)
            i += 1

        table.verticalHeader().setVisible(False)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Stretch columns to fit the table width
        table.horizontalHeader().setStretchLastSection(True)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        table.resizeRowsToContents()
        return table

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
