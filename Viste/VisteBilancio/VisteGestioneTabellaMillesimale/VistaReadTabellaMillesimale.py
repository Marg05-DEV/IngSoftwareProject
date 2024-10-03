from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaCreateTipoSpesa import VistaCreateTipoSpesa
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaDeleteTabellaMillesimale import VistaDeleteTabellaMillesimale
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaDeleteTipoSpesa import VistaDeleteTipoSpesa


class VistaReadTabellaMillesimale(QWidget):

    def __init__(self, codice_tabella, callback):
        super(VistaReadTabellaMillesimale, self).__init__()
        print("dentro a read condomino 1")
        self.codice_tabella = codice_tabella
        self.callback = callback
        self.tabella_millesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(codice_tabella)
        print(self.tabella_millesimale.getInfoTabellaMillesimale())
        print("dentro a read condomino 2")
        main_layout = QVBoxLayout()
        action_layout1 = QVBoxLayout()
        print("a")
        action_layout1.addWidget(self.new_label("NOME TABELLA", "nome"))
        action_layout1.addWidget(self.new_label("DESCRIZIONE", "descrizione"))
        print("b2")
        action_layout2 = QHBoxLayout()

        self.list_view_tipi_spesa = QListView()
        self.list_view_tipi_spesa.setAlternatingRowColors(True)
        action_layout2.addWidget(self.list_view_tipi_spesa)

        self.button_list = {}
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.create_button("Aggiungi tipo spesa", self.nuovo_tipo_spesa))
        button_layout.addWidget(self.create_button("Rimuovi tipo spesa", self.delete_tipo_spesa, True))
        action_layout2.addLayout(button_layout)
        self.button_list["Aggiungi tipo spesa"].setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.button_list["Rimuovi tipo spesa"].setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.msg = QLabel("Non ci sono condomini assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)
        print("e")
        main_layout.addLayout(action_layout1)
        main_layout.addLayout(action_layout2)
        main_layout.addWidget(self.create_button("Rimuovi Tabella Millesimale", self.delete_tabella_millesimale))
        print("f")
        main_layout.addWidget(self.msg)
        self.update_list()
        print("g")
        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Tabella Millesimale")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def new_label(self, testo, index):
        label = QLabel(testo + ": " + str(self.tabella_millesimale.getInfoTabellaMillesimale()[index]))
        return label

    def update_list(self):
        if not self.tabella_millesimale.tipologieSpesa:
            self.msg.setText("Non ci sono tipi di spesa")
            self.msg.show()
        else:
            self.msg.hide()

        listview_model = QStandardItemModel(self.list_view_tipi_spesa)

        for tipo_spesa_codice in self.tabella_millesimale.tipologieSpesa:
            item = QStandardItem()
            tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(tipo_spesa_codice)
            item.setData(tipo_spesa_codice, Qt.ItemDataRole.UserRole)
            item_text = f"NOME: {tipo_spesa.nome}\nDESC: {tipo_spesa.descrizione}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        print("qui finisce")
        self.list_view_tipi_spesa.setModel(listview_model)
        self.selectionModel = self.list_view_tipi_spesa.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)

    def nuovo_tipo_spesa(self):
        print(Immobile.ricercaImmobileById(self.tabella_millesimale.immobile))
        self.new_tipo_spesa = VistaCreateTipoSpesa(self.tabella_millesimale, Immobile.ricercaImmobileById(self.tabella_millesimale.immobile), self.lista_tipi_spesa_callback, None)
        print("sono qui ora")
        self.new_tipo_spesa.show()

    def delete_tipo_spesa(self):
        print(self.list_view_tipi_spesa.selectedIndexes())
        item = None
        for index in self.list_view_tipi_spesa.selectedIndexes():
            item = self.list_view_tipi_spesa.model().itemFromIndex(index)
            print("item: ", item)
        print("item: ", item)

        print("cacca: ", item.data(Qt.ItemDataRole.UserRole))
        sel_tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(item.data(Qt.ItemDataRole.UserRole))
        self.remove_tipo_spesa = VistaDeleteTipoSpesa(sel_tipo_spesa, self.tabella_millesimale, self.lista_tipi_spesa_callback)
        self.remove_tipo_spesa.show()

    def delete_tabella_millesimale(self):
        print(self.tabella_millesimale)
        self.rimuovi_tabella_millesimale = VistaDeleteTabellaMillesimale(self.tabella_millesimale.codice, self.callback)
        self.close()
        self.rimuovi_tabella_millesimale.show()

    def able_button(self):
        print("selezione cambiata")
        print("lista button", self.button_list)
        if not self.list_view_tipi_spesa.selectedIndexes():
            self.button_list["Rimuovi tipo spesa"].setDisabled(True)
        else:
            self.button_list["Rimuovi tipo spesa"].setDisabled(False)

    def lista_tipi_spesa_callback(self, msg):
        print("entriamo", msg)
        self.tabella_millesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(self.tabella_millesimale.codice)
        self.update_list()
        self.msg.setText(msg)
        self.msg.show()
        self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.tabella_millesimale.tipologieSpesa:
            self.msg.setText("Non ci sono tipi di spesa asseganti")
            self.msg.show()