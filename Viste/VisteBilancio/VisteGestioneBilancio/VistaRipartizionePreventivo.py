from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaRipartizionePreventivo(QWidget):
    def __init__(self, bilancio):
        super(VistaRipartizionePreventivo, self).__init__()
        self.bilancio = bilancio
        self.immobile = Immobile.ricercaImmobileById(self.bilancio.immobile)
        self.input_lines = {}
        self.input_errors = {}
        main_layout = QVBoxLayout()

        self.table_ripartizionePreventivo = QTableWidget()
        self.update_table()

        self.msg = QLabel("Non preventivi da effettuare")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Ripartizione Preventivo")

    

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not list(Bilancio.getAllBilanciByImmobile(self.immobile).values()):
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()