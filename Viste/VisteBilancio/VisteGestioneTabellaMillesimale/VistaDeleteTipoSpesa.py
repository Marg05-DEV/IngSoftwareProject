import qtawesome
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QVBoxLayout

from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale

class VistaDeleteTipoSpesa(QWidget):

    def __init__(self, tipo_spesa, tabella_millesimale, callback):

        super(VistaDeleteTipoSpesa, self).__init__()
        self.callback = callback
        self.tabella_millesimale = tabella_millesimale
        self.tipo_spesa = tipo_spesa
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere il tipo di spesa?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        main_layout.addLayout(self.create_warning_msg("Se il tipo di spesa non è assegnato a nessun altra tabella millesimale, \nquesto verrà definitivamente rimosso"))

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.create_button("Procedi", self.delete_tipo_spesa))
        button_layout.addWidget(self.create_button("Annulla", self.close))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(350, 150)
        self.setWindowTitle("Rimuovi Tipo spesa")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        return button

    def delete_tipo_spesa(self):
        self.tabella_millesimale.removeTipoSpesa(self.tipo_spesa)
        msg = "Il tipo di spesa è stato dissociato"
        self.callback(msg)
        self.close()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()