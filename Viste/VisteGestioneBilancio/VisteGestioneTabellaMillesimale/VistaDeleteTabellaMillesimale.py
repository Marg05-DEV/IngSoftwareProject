from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit

from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale

class VistaDeleteTabellaMillesimale(QWidget):

    def __init__(self, tabella_millesimale, callback):
        super(VistaDeleteTabellaMillesimale, self).__init__()
        self.callback = callback
        self.tabella_millesimale = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella_millesimale)
        main_layout = QGridLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere la tabella millesimale?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addWidget(self.create_button("Procedi", self.delete_tabella_millesimale), 1, 0)
        main_layout.addWidget(self.create_button("Annulla", self.close), 1, 1)


        message_layout = QHBoxLayout()

        self.msg = QLabel("La tabella millesimale è stata rimossa")
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

    def delete_tabella_millesimale(self):
        print("funzione di eliminazione")
        print(self.tabella_millesimale)
        if self.tabella_millesimale.tipologiaSpesa:
            print(self.tabella_millesimale.tipologiaSpesa)
        else:
            print("è vuota")
        for tipi_spesa_codici in self.tabella_millesimale.tipologiaSpesa:
            tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(tipi_spesa_codici)
            self.tabella_millesimale.removeTipoSpesa(tipo_spesa)
            if not tipo_spesa.getTabelleMillesimaliAssociate():
                msg = tipo_spesa.rimuoviTipoSpesa()
        print("uscito dal for dei tipi")
        msg = self.tabella_millesimale.rimuoviTabellaMillesimale()
        self.callback(msg)
        self.close()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()