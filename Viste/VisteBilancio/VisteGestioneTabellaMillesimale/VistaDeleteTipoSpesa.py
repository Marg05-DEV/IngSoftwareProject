from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit

from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale

class VistaDeleteTipoSpesa(QWidget):

    def __init__(self, tipo_spesa, tabella_millesimale, callback):
        super(VistaDeleteTipoSpesa, self).__init__()
        print("siamo in vistaDeleteTipoSpesa")
        self.callback = callback
        self.tabella_millesimale = tabella_millesimale
        self.tipo_spesa = tipo_spesa
        main_layout = QGridLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere il tipo di spesa?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addWidget(self.create_button("Procedi", self.delete_tipo_spesa), 1, 0)
        main_layout.addWidget(self.create_button("Annulla", self.close), 1, 1)


        message_layout = QHBoxLayout()

        self.msg = QLabel("Il tipo di spesa è stato rimosso")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        message_widget = QWidget()
        message_widget.setLayout(message_layout)
        main_layout.addWidget(message_widget, 2, 0, 1, 2)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Rimuovi Tabella Millesimale")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def delete_tipo_spesa(self):
        print("pronto per l'eliminazione")
        msg = ""
        print(self.tabella_millesimale.tipologiaSpesa)
        self.tabella_millesimale.removeTipoSpesa(self.tipo_spesa)
        print(self.tabella_millesimale.tipologiaSpesa)
        msg = "Il tipo di spesa è stato dissociato"
        print(self.tipo_spesa.codice)
        if not self.tipo_spesa.getTabelleMillesimaliAssociate():
            msg = self.tipo_spesa.rimuoviTipoSpesa()
        print("prima della callback")
        self.callback(msg)
        self.close()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()