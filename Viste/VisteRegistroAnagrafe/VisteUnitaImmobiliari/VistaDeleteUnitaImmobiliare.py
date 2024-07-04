from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QLineEdit

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaDeleteUnitaImmobiliare(QWidget):

    def __init__(self, sel_unitaImmobiliare, callback):
        print("sono nella classe deleteUnita")
        super(VistaDeleteUnitaImmobiliare, self).__init__()
        self.callback = callback
        self.sel_unitaImmobiliare = sel_unitaImmobiliare
        main_layout = QGridLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere l'unità immobiliare?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addWidget(self.create_button("Procedi", self.deleteUnitaImmobiliare), 1, 0)
        main_layout.addWidget(self.create_button("Annulla", self.close), 1, 1)
        print("dai giovanotto")
        message_layout = QHBoxLayout()
        print("valore 1")
        self.msg = QLabel("L'assegnazione è stata rimossa")
        print("valore 2")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        message_widget = QWidget()
        message_widget.setLayout(message_layout)
        main_layout.addWidget(message_widget, 2, 0, 1, 2)
        print("apposto")

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Rimuovi Unità Immobiliare")

    @staticmethod
    def create_button(testo, action):
        print("bottoni ok")
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        print("esco dai bottoni")
        return button

    def deleteUnitaImmobiliare(self):
        print("rimozione...")
        self.sel_unitaImmobiliare.rimuoviUnitaImmobiliare()
        self.callback()
        self.close()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()