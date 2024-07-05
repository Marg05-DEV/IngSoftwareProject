from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, \
    QListWidget, QListView

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteImmobile import VistaGestioneImmobile
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari import VistaDeleteUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaUpdateUnitaImmobiliare import VistaUpdateUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaCreateCondomino import VistaCreateCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaUpdateCondomino import VistaUpdateCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaDeleteCondomino import VistaDeleteCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaReadCondomino import VistaReadCondomino


class VistaReadAssegnazione(QWidget):

    def __init__(self, sel_unitaImmobiliare, immobile, callback):
        super(VistaReadAssegnazione, self).__init__()
        print("dentro readAssegnazione")
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
        self.immobile = immobile
        self.callback = callback
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("INFORMAZIONI UNITA' IMMOBILIARE:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(lbl_frase)

        main_layout.addLayout(self.pair_label("Tipologia Unità Immobiliare", "tipoUnitaImmobiliare"))
        main_layout.addLayout(self.pair_label("Scala", "scala"))
        main_layout.addLayout(self.pair_label("Interno", "interno"))

        lbl_frase1 = QLabel("DATI CATASTALI: ")
        lbl_frase1.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(lbl_frase1)
        dati_catastali_layout = QGridLayout()

        self.add_to_grid(dati_catastali_layout, "Foglio", "foglio", 0, 0)
        self.add_to_grid(dati_catastali_layout, "Particella", "particella", 0, 1)
        self.add_to_grid(dati_catastali_layout, "Subalterno", "subalterno", 0, 2)
        self.add_to_grid(dati_catastali_layout, "ZC", "ZC", 1, 0)
        self.add_to_grid(dati_catastali_layout, "Classe", "classe", 1, 1)
        self.add_to_grid(dati_catastali_layout, "Categoria", "categoria", 1, 2)

        main_layout.addLayout(dati_catastali_layout)
        main_layout.addWidget(self.create_button("Modifica Unità Immobiliare", self.updateUnitaImmobiliare))
        main_layout.addWidget(self.create_button("Rimuovi Unità Immobiliare", self.deleteUnitaImmobiliare))
        print("Prossimo problema")

        condomini_label = QLabel("CONDOMINI ASSEGNATI:")
        condomini_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(condomini_label)

        action_layout = QHBoxLayout()
        self.list_view_condomini = QListView()
        main_layout.addWidget(self.list_view_condomini, 10, 0, 5, 2)

        main_layout.addWidget(self.create_button("Aggiungi Condomino", self.addCondomino))
        main_layout.addWidget(self.create_button("Modifica Condomino", self.updateCondomino))
        main_layout.addWidget(self.create_button("Visualizza Condomino", self.readCondomino))
        main_layout.addWidget(self.create_button("Rimuovi Condomino", self.deleteCondomino))

        message_layout = QHBoxLayout()

        self.msg = QLabel("Non ci sono condomini assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        self.update_list()

        message_layout.addWidget(self.msg)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)

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

    def pair_label(self, testo, index):
        pair_layout = QHBoxLayout()

        lbl_desc = QLabel(testo + ": ")
        lbl_content = QLabel(str(self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[index]))

        pair_layout.addWidget(lbl_desc)
        pair_layout.addWidget(lbl_content)
        return pair_layout

    def add_to_grid(self, layout, testo, index, row, col):
        lbl_desc = QLabel(testo + ": ")
        lbl_content = QLabel(str(self.sel_unitaImmobiliare.getInfoUnitaImmobiliare()[index]))
        layout.addWidget(lbl_desc, row, col * 2)
        layout.addWidget(lbl_content, row, col * 2 + 1)

    def update_list(self):
        print("dentro a update 1")
        self.list_condomini = self.sel_unitaImmobiliare.getCondominiAssociati()
        print("dentro a update 1")
        if not self.list_condomini:
            self.msg.setText("Non ci sono immobili assegnati al condomino selezionato")
            self.msg.show()
        else:
            self.msg.hide()
        print("dentro a update 2")
        listview_model = QStandardItemModel(self.list_view_condomini)

        for condomino in self.list_condomini:
            item = QStandardItem()
            item_text = f"{condomino.nome}  {condomino.cognome} - {condomino.codiceFiscale}"
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
        print("in modifica")
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
