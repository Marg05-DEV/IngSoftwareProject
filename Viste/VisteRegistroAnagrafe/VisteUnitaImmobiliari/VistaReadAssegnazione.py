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
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaDeleteUnitaImmobiliare import VistaDeleteUnitaImmobiliare


class VistaReadAssegnazione(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback):
        super(VistaReadAssegnazione, self).__init__()
        print("dentro readAssegnazione")
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
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
        action_layout.addWidget(self.list_view_condomini)

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

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
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

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
    def updateUnitaImmobiliare(self):
        self.modifica_unitaImmobiliare = VistaUpdateUnitaImmobiliare(self.sel_unitaImmobiliare, callback=self.callback)
        self.close()
        self.modifica_unitaImmobiliare.show()

    def deleteUnitaImmobiliare(self):
        self.rimuovi_unitaImmobiliare = VistaDeleteUnitaImmobiliare(self.sel_unitaImmobiliare, callback=self.callback)
        self.close()
        self.rimuovi_unitaImmobiliare.show()

    def addCondomino(self):
        # Logica per aggiungere un condominio
        pass

    def updateCondomino(self):
        pass

    def readCondomino(self):
        pass

    def deleteCondomino(self):
        pass