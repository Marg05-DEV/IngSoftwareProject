import os
import webbrowser

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, \
    QPushButton, QSizePolicy, QSpacerItem

from Classes.Contabilita.bilancio import Bilancio
from Classes.Gestione.gestoreRegistroAnagrafe import GestoreRegistroAnagrafe
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteGestioneBilancio.VisteBilancio.VistaBilancio import VistaBilancio
from Viste.VisteGestioneBilancio.VisteBilancio.VistaNuovoEsercizio import VistaNuovoEsercizio
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaCreateUnitaImmobiliare import VistaCreateUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaReadAssegnazione import VistaReadAssegnazione

class VistaGestisciBilancio(QWidget):

    def __init__(self, immobile):
        super(VistaGestisciBilancio, self).__init__()
        self.immobile = immobile
        self.input_lines = {}
        self.input_errors = {}
        main_layout = QVBoxLayout()
        action_layout = QHBoxLayout()

        self.list_view_bilanci = QListView()

        button_layout = QVBoxLayout()
        self.button_list = {}
        button_layout.addWidget(self.create_button("Vai al bilancio", self.goBilancio, True))
        action_layout.addWidget(self.list_view_bilanci)
        action_layout.addLayout(button_layout)

        action_data = QHBoxLayout()
        action_data.addLayout(self.pairLabelInput("Data inizio Esercizio", "inizioEsercizio"))
        action_data.addLayout(self.pairLabelInput("Data fine Esercizio", "fineEsercizio"))
        action_data.addWidget(self.create_button("Nuovo Esercizio", self.goNuovoEsercizio, True))

        self.msg = QLabel("Non ci sono Esercizi")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()
        self.update_list()
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addLayout(action_layout)
        main_layout.addLayout(action_data)
        main_layout.addLayout(self.msg)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Bilancio")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def update_list(self):
        self.all_bilanci = Bilancio.getAllBilanci().values()
        if not self.all_bilanci:
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()

        listview_model = QStandardItemModel(self.list_view_bilanci)
        for bilancio in self.all_bilanci:
            item = QStandardItem()
            item_text = f"Bilancio: {bilancio.inizioEsercizio} - {bilancio.fineEsercizio}"
            item.setText(item_text)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            listview_model.appendRow(item)

        self.list_view_bilanci.setModel(listview_model)

        self.selectionModel = self.list_view_bilanci.selectionModel()
        self.selectionModel.selectionChanged.connect(self.able_button)


    def goBilancio(self):
        self.choose_bilancio = VistaBilancio(self.immobile)
        self.choose_bilancio.show()

    def goNuovoEsercizio(self):
        self.nuovo_esercizio = VistaBilancio(self.immobile)
        self.nuovo_esercizio.show()

    def pairLabelInput(self, testo, index):
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + "*: ")
        input_line = QLineEdit()

        input_line.textChanged.connect(self.input_validation)
        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout
    def able_button(self):
        if not self.list_view_bilanci.selectedIndexes():
            self.button_list["Vai al bilancio"].setDisabled(True)
        else:
            self.button_list["Vai al bilancio"].setDisabled(False)

    def input_validation(self):
        pass

    def callback(self, msg=""):
        self.button_list["Vai al bilancio"].setDisabled(True)
        self.button_list["Nuovo Esercizio"].setDisabled(True)
        self.update_list()
        if msg:
            self.msg.setText(msg)
            self.msg.show()
            self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.all_bilanci:
            self.msg.setText("Non ci sono unità bilanci definiti")
            self.msg.show()