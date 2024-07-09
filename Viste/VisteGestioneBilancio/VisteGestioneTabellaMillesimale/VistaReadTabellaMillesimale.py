from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale

class VistaReadTabellaMillesimale(QWidget):

    def __init__(self, codice_tabella, callback):
        super(VistaReadTabellaMillesimale, self).__init__()
        print("dentro a read condomino 1")
        #self.codice_tabella = codice_tabella
        self.callback = callback
        tutte_le_tabelle = list(TabellaMillesimale.getAllTabelleMillesimali().values())
        print(tutte_le_tabelle)
        nome_tabella_millesimale = ""
        for i in tutte_le_tabelle:
            print(i.codice)
            if i.codice == codice_tabella:
                self.tabella_millesimale = i


        print("dentro a read condomino 2")
        main_layout = QVBoxLayout()

        main_layout.addLayout(self.pair_label("Nome", "nome"))
        main_layout.addLayout(self.pair_label("Descrizione", "descrizione"))


        self.msg = QLabel("Non ci sono condomini assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        main_layout.addWidget()
        main_layout.addWidget(self.msg)
        self.update_list()

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Condomino")

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
        lbl_content = QLabel(str(self.sel_condomino.getDatiAnagraficiCondomino()[index]))

        pair_layout.addWidget(lbl_desc)
        pair_layout.addWidget(lbl_content)

        return pair_layout

    def update_list(self):
        print("dentro a update 1")
        self.list_immobili = self.sel_condomino.getImmobiliAssociati()
        print("dentro a update 1", self.list_immobili)
        if not self.list_immobili:
            print("ciao")
            self.msg.setText("Non ci sono immobili assegnati al condomino selezionato")
            self.msg.show()
        else:
            self.msg.hide()
        print("dentro a update 2")
        listview_model = QStandardItemModel(self.list_view_immobili)

        for immobile in self.list_immobili:
            item = QStandardItem()
            item_text = f"{immobile.codice} - {immobile.sigla} - {immobile.denominazione}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        self.list_view_immobili.setModel(listview_model)

    def updateCondomino(self):
        print("ciao")
        self.vista_modifica_condomino = VistaUpdateCondomino(self.sel_condomino, callback=self.callback, onlyAnagrafica=True)
        print("ciao ciao")
        self.close()
        self.vista_modifica_condomino.show()


    def hide_message(self):
        self.msg.hide()
        self.timer.stop()