from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout, QListView, \
    QFrame

from Classes.Contabilita.fornitore import Fornitore
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Viste.VisteContabilita.VisteRate.VistaDeleteRata import VistaDeleteRata
from Viste.VisteContabilita.VisteRate.VistaUpdateRata import VistaUpdateRata
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaCreateTipoSpesa import VistaCreateTipoSpesa
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaDeleteTabellaMillesimale import VistaDeleteTabellaMillesimale
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaDeleteTipoSpesa import VistaDeleteTipoSpesa
from Viste.VisteContabilita.VisteSpese.VistaDeleteSpesa import VistaDeleteSpesa
from Viste.VisteContabilita.VisteSpese.VistaUpdateSpesa import VistaUpdateSpesa


class VistaReadSpesa(QWidget):

    def __init__(self, spesa, callback):
        super(VistaReadSpesa, self).__init__()
        print("dentro a read condomino 1")
        self.spesa = spesa
        self.callback = callback

        main_layout = QVBoxLayout()

        main_layout.addLayout(self.pair_label("Codice", "codice"))
        main_layout.addLayout(self.pair_label("Immobile", "immobile"))
        main_layout.addLayout(self.pair_label("Descrizione", "descrizione"))
        main_layout.addLayout(self.pair_label("Tipo Spesa", "tipoSpesa"))

        lbl_frase1 = QLabel("Dati fornitore:")
        lbl_frase1.setStyleSheet("font-weight: bold;")
        lbl_frase1.setFixedSize(lbl_frase1.sizeHint())

        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(lbl_frase1)

        main_layout.addLayout(self.pair_label("Denominazione", "denominazione"))
        main_layout.addLayout(self.pair_label("Città", "cittaSede"))
        main_layout.addLayout(self.pair_label("Indirizzo", "indirizzoSede"))
        main_layout.addLayout(self.pair_label("CF/Partita Iva", "partitaIva"))
        main_layout.addLayout(self.pair_label("Tipologia", "tipoProfessione"))

        lbl_frase2 = QLabel("Dati Fattura:")
        lbl_frase2.setStyleSheet("font-weight: bold;")
        lbl_frase2.setFixedSize(lbl_frase2.sizeHint())

        main_layout.addWidget(self.drawLine())
        main_layout.addWidget(lbl_frase2)

        main_layout.addLayout(self.pair_label("Numero Fattura", "numeroFattura"))
        main_layout.addLayout(self.pair_label("Data Fattura", "dataFattura"))

        main_layout.addWidget(self.drawLine())

        main_layout.addLayout(self.pair_label("Importo", "importo"))
        main_layout.addLayout(self.pair_label("Ritenuta", "isRitenuta"))
        main_layout.addLayout(self.pair_label("Pagata", "pagata"))
        main_layout.addLayout(self.pair_label("Data Pagamento", "dataPagamento"))

        main_layout.addWidget(self.create_button("Modifica Spesa", self.updateSpesa))
        main_layout.addWidget(self.create_button("Rimuovi Spesa", self.deleteSpesa))

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Dettaglio Rata")

    def drawLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def pair_label(self, testo, index):
        pair_layout = QHBoxLayout()
        lbl_content = ""
        lbl_desc = QLabel(testo + ": ")
        if index == "denominazione" or index == "cittaSede" or index == "indirizzoSede" or index == "partitaIva" or index == "tipoProfessione":
            fornitore = Fornitore.ricercaFornitoreByCodice(self.spesa.fornitore)
            lbl_content = QLabel(str(fornitore.getInfoFornitore()[index]))
        elif index == "importo":
            lbl_content = QLabel(str("%.2f" % self.spesa.importo))
        elif index == "immobile":
            lbl_content = QLabel(str(Immobile.ricercaImmobileById(self.spesa.getInfoSpesa()["immobile"]).denominazione))
        elif index == "tipoSpesa":
            lbl_content = QLabel(str(TipoSpesa.ricercaTipoSpesaByCodice(self.spesa.getInfoSpesa()["tipoSpesa"]).nome))
        elif index == "isRitenuta":
            if self.spesa.getInfoSpesa()["isRitenuta"]:
                lbl_content = QLabel("La spesa è una ritenuta")
            else:
                lbl_content = QLabel("La spesa non è una ritenuta")
        elif index == "pagata":
            if self.spesa.getInfoSpesa()["pagata"]:
                lbl_content = QLabel("La spesa è stata pagata")
            else:
                lbl_content = QLabel("La spesa non è stata pagata")
        elif index == "dataPagamento":
            if self.spesa.getInfoSpesa()["pagata"]:
                lbl_content = QLabel(str(self.spesa.getInfoSpesa()["dataPagamento"]))
            else:
                lbl_content = QLabel("-")
        else:
            lbl_content = QLabel(str(self.spesa.getInfoSpesa()[index]))
        pair_layout.addWidget(lbl_desc)
        pair_layout.addWidget(lbl_content)

        return pair_layout

    def updateSpesa(self):
        self.vista_modifica_spesa = VistaUpdateSpesa(self.spesa, callback=self.callback)
        self.vista_modifica_spesa.show()
        self.close()

    def deleteSpesa(self):
        self.vista_elimina_spesa = VistaDeleteSpesa(self.spesa, callback=self.callback)
        self.vista_elimina_spesa.show()
        self.close()