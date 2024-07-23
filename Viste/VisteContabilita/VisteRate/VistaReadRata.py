
from PyQt6.QtWidgets import QWidget, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Viste.VisteContabilita.VisteRate.VistaDeleteRata import VistaDeleteRata
from Viste.VisteContabilita.VisteRate.VistaUpdateRata import VistaUpdateRata


class VistaReadRata(QWidget):

    def __init__(self, rata, callback):
        super(VistaReadRata, self).__init__()
        print("dentro a read condomino 1")
        self.rata = rata
        self.callback = callback

        main_layout = QVBoxLayout()
        print("ciaociao")
        main_layout.addLayout(self.pair_label("Codice", "codice"))
        main_layout.addLayout(self.pair_label("Immobile", "immobile"))
        print("ciao")
        main_layout.addLayout(self.pair_label("Unità Immobiliare", "unitaImmobiliare"))
        print("bho")
        main_layout.addLayout(self.pair_label("Descrizione", "descrizione"))
        main_layout.addLayout(self.pair_label("Numero Ricevuta", "numeroRicevuta"))
        main_layout.addLayout(self.pair_label("Importo", "importo"))
        main_layout.addLayout(self.pair_label("Versante", "versante"))
        main_layout.addLayout(self.pair_label("Data pagamento", "dataPagamento"))
        main_layout.addLayout(self.pair_label("Tipologia pagamento", "tipoPagamento"))

        main_layout.addWidget(self.create_button("Modifica Rata", self.updateRata))
        main_layout.addWidget(self.create_button("Rimuovi Rata", self.deleteRata))

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Rata")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def pair_label(self, testo, index):
        print("top")
        pair_layout = QHBoxLayout()
        lbl_content = ""
        condomino = None
        lbl_desc = QLabel(testo + ": ")
        if index == "unitaImmobiliare":
            unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata.unitaImmobiliare)
            for item in unita.condomini.keys():
                if unita.condomini[item] == "Proprietario":
                    condomino = Condomino.ricercaCondominoByCF(item)
            if unita.tipoUnitaImmobiliare == "Appartamento":
                item_text = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Interno {unita.interno} di {condomino.nome} {condomino.cognome}"
                lbl_content = QLabel(item_text)
            else:
                item_text = f"{unita.tipoUnitaImmobiliare} di {condomino.nome} {condomino.cognome}"
                lbl_content = QLabel(item_text)

        elif index == "immobile":
            unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(self.rata.unitaImmobiliare)
            immobile = Immobile.ricercaImmobileById(unita.immobile)
            lbl_content = QLabel(str(immobile.denominazione))

        elif index == "importo":
            lbl_content = QLabel(str("%.2f" % self.rata.importo))
        else:
            lbl_content = QLabel(str(self.rata.getInfoRata()[index]))
        pair_layout.addWidget(lbl_desc)
        pair_layout.addWidget(lbl_content)
        return pair_layout

    def updateRata(self):
        self.vista_modifica_rata = VistaUpdateRata(self.rata, self.callback)
        self.vista_modifica_rata.show()
        self.close()

    def deleteRata(self):
        self.vista_elimina_rata = VistaDeleteRata(self.rata, self.callback)
        self.vista_elimina_rata.show()
        self.close()
