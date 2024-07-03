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

        self.list_view_immobili = QListView()
        main_layout.addWidget(self.list_view_immobili)

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
        """
        list_immobili = []
        list_unitaImmobiliare = list(UnitaImmobiliare.getAllUnitaImmobiliari())
        for unitaImmo in list_unitaImmobiliare:
            for condomino in unitaImmo.condomini.key():
                if condomino == self.condomino:
                    list_immobili = unitaImmo.immobile
                else:
                    print("Il condomino non è associato a nessun immobile")
                    return None

        listview_model = QStandardItemModel(self.list_view_immobili)
        flag = 0
        for immobili in list_immobile:
            item = QStandardItem()
            item_text = f"Denominazione: {immobili.denominazione} Sigla: {immobili.sigla}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)
            flag += 1

        if flag == 0:
            print("Non ci sono Unità Immobiliari assegante all'immobile")
            return None

        self.list_view_unitaImmobiliare.setModel(listview_model)
        """
    def updateCondomino(self):
        self.vista_modifica_condomino = VistaUpdateCondomino(self.sel_condomino, callback=self.callback)
        self.vista_modifica_condomino.show()
        self.close()