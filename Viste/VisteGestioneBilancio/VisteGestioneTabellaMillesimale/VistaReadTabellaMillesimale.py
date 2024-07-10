from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Viste.VisteGestioneBilancio.VisteGestioneTabellaMillesimale.VistaCreateTipoSpesa import VistaCreateTipoSpesa
from Viste.VisteGestioneBilancio.VisteGestioneTabellaMillesimale.VistaDeleteTabellaMillesimale import VistaDeleteTabellaMillesimale


class VistaReadTabellaMillesimale(QWidget):

    def __init__(self, codice_tabella, callback):
        super(VistaReadTabellaMillesimale, self).__init__()
        print("dentro a read condomino 1")
        self.codice_tabella = codice_tabella
        self.callback = callback
        self.tabella_millesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(codice_tabella)

        print("dentro a read condomino 2")
        main_layout = QVBoxLayout()
        action_layout1 = QVBoxLayout()
        action_layout1.addLayout(self.new_label("Nome", "nome"))
        action_layout1.addLayout(self.new_label("Descrizione", "descrizione"))

        action_layout2 = QHBoxLayout()

        self.list_view_tipi_spesa = QListView()
        self.list_view_tipi_spesa.setAlternatingRowColors(True)
        action_layout2.addWidget(self.list_view_tipi_spesa)
        self.button_list = {}
        action_layout2.addWidget(self.create_button("Aggiungi tipo spesa", self.nuovo_tipo_spesa))
        action_layout2.addWidget(self.create_button("Rimuovi tipo spesa", self.delete_tipo_spesa, True))

        self.button_list["Aggiungi tipo spesa"].setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.button_list["ARimuovi tipo spesa"].setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.msg = QLabel("Non ci sono condomini assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addLayout(action_layout1)
        main_layout.addLayout(action_layout2)
        main_layout.addWidget(self.create_button("Rimuovi Tabella Millesimale", self.delete_tabella_millesimale))
        main_layout.addWidget(self.msg)
        self.update_list()

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Condomino")

    def create_button(self, testo, action, disabled = False):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def new_label(self, testo, index):
        label = QLabel(testo + ": " + str(self.tabella_millesimale.getInfoTabellaMillesimale()[index]))
        return label

    def update_list(self):
        if not self.tabella_millesimale.tipologiaSpesa:
            self.msg.setText("Non ci sono tipi di spesa")
            self.msg.show()
        else:
            self.msg.hide()

        print("dentro a update 3")
        listview_model = QStandardItemModel(self.list_view_tipi_spesa)
        for tipo_spesa_codice in self.tabella_millesimale.tipologiaSpesa:
            item = QStandardItem()
            tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(tipo_spesa_codice)
            item_text = f"Nome:{tipo_spesa.nome}\nDescrizione:{tipo_spesa.descrizione}"
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
        #finire
        self.new_tipo_spesa = VistaCreateTipoSpesa(self.tabella_millesimale, self.callback)
        self.new_tipo_spesa.show()

    def delete_tipo_spesa(self):
        pass

    def delete_tabella_millesimale(self):
        self.rimuovi_tabella_millesimale = VistaDeleteTabellaMillesimale(self.tabella_millesimale, self.callback)
        self.close()
        self.rimuovi_tabella_millesimale.show()

    def able_button(self):
        print("selezione cambiata")
        print("lista button", self.button_list)
        if not self.list_view_tipi_spesa.selectedIndexes():
            self.button_list["Rimuovi tipo spesa"].setDisabled(True)
        else:
            self.button_list["Rimuovi tipo spesa"].setDisabled(False)

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.tabella_millesimale.tipologiaSpesa:
            self.msg.setText("Non ci sono tipi di spesa asseganti")
            self.msg.show()