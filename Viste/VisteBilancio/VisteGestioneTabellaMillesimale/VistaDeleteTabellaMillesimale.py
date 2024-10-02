from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout

from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale


class VistaDeleteTabellaMillesimale(QWidget):

    def __init__(self, tabella_millesimale, callback):
        super(VistaDeleteTabellaMillesimale, self).__init__()
        self.callback = callback
        self.tabella_millesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella_millesimale)
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere la tabella millesimale?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.create_button("Procedi", self.delete_tabella_millesimale))
        button_layout.addWidget(self.create_button("Annulla", self.close))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(350, 150)
        self.setWindowTitle("Rimuovi Tabella Millesimale")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        return button

    def delete_tabella_millesimale(self):
        for tipi_spesa_codici in self.tabella_millesimale.tipologieSpesa:
            tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(tipi_spesa_codici)
            self.tabella_millesimale.removeTipoSpesa(tipo_spesa)

        msg = self.tabella_millesimale.rimuoviTabellaMillesimale()
        self.callback(msg)
        self.close()
