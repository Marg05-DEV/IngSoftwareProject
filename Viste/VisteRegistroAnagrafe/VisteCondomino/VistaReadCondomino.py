from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteCondomino import VistaGestioneCondomini
from Viste.VisteRegistroAnagrafe.VisteCondomino import VistaUpdateCondomino


class VistaReadCondomino(QWidget):

    def __init__(self, sel_condomino, callback):
        super(VistaReadCondomino, self).__init__()
        print("dentro a read condomino")
        self.sel_condomino = sel_condomino
        self.callback = callback

        main_layout = QVBoxLayout()

        main_layout.addLayout(self.pair_label("Nome", "nome"))
        main_layout.addLayout(self.pair_label("Cognome", "cognome"))
        main_layout.addLayout(self.pair_label("Codice Fiscale", "codiceFiscale"))
        main_layout.addLayout(self.pair_label("Luogo di Nascita", "luogoDiNascita"))
        main_layout.addLayout(self.pair_label("Provincia di Nascita", "provinciaDiNascita"))
        main_layout.addLayout(self.pair_label("Residenza", "residenza"))
        main_layout.addLayout(self.pair_label("Telefono", "telefono"))
        main_layout.addLayout(self.pair_label("Email", "email"))

        main_layout.addWidget(self.create_button("Modifica Dati Anagrafici Condomino", self.updateCondomino))

        lbl_frase = QLabel("Immobili a cui il condomino è assegnato:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(lbl_frase)

        action_layout = QHBoxLayout()
        self.list_view_immobili = QListView()
        action_layout.addWidget(self.list_view_immobili)

        message_layout = QHBoxLayout()

        self.msg = QLabel("Non ci sono immobili assegnati")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        message_layout.addWidget(self.msg)
        self.listImmobiliAssegnati()
        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Immobile")

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

    def listImmobiliAssegnati(self):
        print("entrato")
        self.list_immobili = []
        self.list_unitaImmobiliare = list(UnitaImmobiliare.getAllUnitaImmobiliari().values())
        print(self.list_unitaImmobiliare)
        for unita in self.list_unitaImmobiliare:
            if unita.condomini:
                for condomino in unita.condomini.keys():
                   if condomino.codice == self.sel_condomino.codice:
                        print("popolamento")
                        self.list_immobili.append(unita.immobile)

        listview_model = QStandardItemModel(self.list_view_immobili)

        for immobili in self.list_immobili:
            print("so boccato")
            print("scorro la lista ", immobili.denominazione, " ", immobili.sigla )
            item = QStandardItem()
            item_text = f"Denominazione: {immobili.denominazione} Sigla: {immobili.sigla}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)
            print("forse entro qui")

        if not self.list_immobili:
            print("impossibile che entro qui")
            self.msg.setText("Non ci sono unità immobiliari assegnate all'immobile selezionato")
            self.msg.show()
            return None

        print(listview_model)
        self.list_view_immobili.setModel(listview_model)

    def updateCondomino(self):
        self.vista_modifica_condomino = VistaUpdateCondomino(self.sel_condomino, callback=self.callback)
        self.vista_modifica_condomino.show()
        self.close()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()