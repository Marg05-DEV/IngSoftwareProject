from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaUpdateCondomino import VistaUpdateCondomino


class VistaReadCondomino(QWidget):

    def __init__(self, sel_condomino, callback):
        super(VistaReadCondomino, self).__init__()
        print("dentro a read condomino 1")
        self.sel_condomino = sel_condomino
        self.callback = callback
        print("dentro a read condomino 2")
        main_layout = QVBoxLayout()

        main_layout.addLayout(self.pair_label("Nome", "nome"))
        main_layout.addLayout(self.pair_label("Cognome", "cognome"))
        main_layout.addLayout(self.pair_label("Codice Fiscale", "codiceFiscale"))
        main_layout.addLayout(self.pair_label("Luogo di Nascita", "luogoDiNascita"))
        main_layout.addLayout(self.pair_label("Provincia di Nascita", "provinciaDiNascita"))
        main_layout.addLayout(self.pair_label("Data di Nascita", "dataDiNascita"))
        main_layout.addLayout(self.pair_label("Residenza", "residenza"))
        main_layout.addLayout(self.pair_label("Telefono", "telefono"))
        main_layout.addLayout(self.pair_label("Email", "email"))
        print("dentro a read condomino 3")
        main_layout.addWidget(self.create_button("Modifica Dati Anagrafici Condomino", self.updateCondomino))

        lbl_frase = QLabel("Immobili a cui il condomino è assegnato:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(lbl_frase)
        print("dentro a read condomino 4")
        action_layout = QHBoxLayout()
        self.list_view_immobili = QListView()
        print("dentro a read condomino 5")

        action_layout.addWidget(self.list_view_immobili)

        message_layout = QHBoxLayout()
        print("dentro a read condomino 6")
        self.msg = QLabel("Non ci sono immobili assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()
        print("dentro a read condomino 7")
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)
        print("dentro a read condomino 8")
        self.update_list()
        print("dentro a read condomino 9")
        message_layout.addWidget(self.msg)
        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)
        print("dentro a read condomino 10")
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
        print("dentro a update 1")
        if not self.list_immobili:
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