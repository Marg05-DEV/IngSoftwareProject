from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaDeleteCondomino import VistaDeleteCondomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaUpdateCondomino import VistaUpdateCondomino


class VistaReadCondomino(QWidget):

    def __init__(self, sel_condomino, callback, fromUnitaImmobiliare, unita_immobiliare=None):
        super(VistaReadCondomino, self).__init__()
        self.sel_condomino = sel_condomino
        self.fromUnitaImmobiliare = fromUnitaImmobiliare
        if fromUnitaImmobiliare:
            self.unita_immobiliare = unita_immobiliare
        self.callback = callback
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

        if fromUnitaImmobiliare:
            titolo_layout = QHBoxLayout()
            button_layout = QVBoxLayout()

            lbl_desc = QLabel("Titolo nell'unità immobiliare: ")
            lbl_content = QLabel(str(self.unita_immobiliare.condomini[self.sel_condomino.codiceFiscale]))

            titolo_layout.addWidget(lbl_desc)
            titolo_layout.addWidget(lbl_content)

            button_layout.addWidget(self.create_button("Modifica Condomino", self.updateCondomino))
            button_layout.addWidget(self.create_button("Rimuovi Condomino", self.removeCondomino))

            main_layout.addLayout(titolo_layout)
            main_layout.addLayout(button_layout)
        else:
            main_layout.addWidget(self.create_button("Modifica Dati Anagrafici Condomino", self.updateCondomino))

            lbl_frase = QLabel("Immobili a cui il condomino è assegnato:")
            lbl_frase.setStyleSheet("font-weight: bold;")
            main_layout.addWidget(lbl_frase)

            self.list_view_immobili = QListView()

            self.msg = QLabel("Non ci sono condomini assegnati")
            self.msg.setStyleSheet("color: red; font-weight: bold;")
            self.msg.hide()

            main_layout.addWidget(self.list_view_immobili)
            main_layout.addWidget(self.msg)
            self.update_list()

        self.setLayout(main_layout)
        self.resize(300, 500)
        if fromUnitaImmobiliare:
            self.setWindowTitle("Dettaglio Condomino")
        else:
            self.setWindowTitle("Dati Anagrafici Condomino")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
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
        self.list_immobili = self.sel_condomino.getImmobiliAssociati()
        if not self.list_immobili:
            self.msg.setText("Non ci sono immobili assegnati al condomino selezionato")
            self.msg.show()
        else:
            self.msg.hide()
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
        if self.fromUnitaImmobiliare:
            self.vista_modifica_condomino = VistaUpdateCondomino(self.sel_condomino, self.callback, self.unita_immobiliare, onlyAnagrafica=False)
        else:
            self.vista_modifica_condomino = VistaUpdateCondomino(self.sel_condomino, callback=self.callback, onlyAnagrafica=True)
        self.close()
        self.vista_modifica_condomino.show()

    def removeCondomino(self):
        self.vista_elimina_condomino = VistaDeleteCondomino(self.sel_condomino, self.unita_immobiliare, self.callback)
        self.close()
        self.vista_elimina_condomino.show()