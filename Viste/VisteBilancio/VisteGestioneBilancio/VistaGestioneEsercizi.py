import datetime
import os
import webbrowser

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListView, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QDateEdit

from Classes.Contabilita.bilancio import Bilancio
from Classes.Gestione.gestoreRegistroAnagrafe import GestoreRegistroAnagrafe
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteBilancio.VisteGestioneBilancio.VistaGestioneBilancio import VistaGestioneBilancio
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaCreateUnitaImmobiliare import VistaCreateUnitaImmobiliare
from Viste.VisteRegistroAnagrafe.VisteUnitaImmobiliari.VistaReadAssegnazione import VistaReadAssegnazione

class VistaGestioneEsercizi(QWidget):

    def __init__(self, immobile):
        super(VistaGestioneEsercizi, self).__init__()
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
        action_data.addWidget(self.create_button("Nuovo Esercizio", self.goNuovoEsercizio, False))
        #self.button_list["Nuovo Esercizio"].setDisabled(False)

        self.msg = QLabel("Non ci sono Esercizi")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addLayout(action_layout)
        main_layout.addLayout(action_data)
        main_layout.addWidget(self.msg)

        self.update_list()

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

    def pairLabelInput(self, testo, index):
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + "*: ")
        input_line = QDateEdit()
        if index == "inizioEsercizio":
            input_line.setDate(datetime.date.today())
            input_line.dateChanged.connect(self.autoset_data_fine)
            input_line.dateChanged.connect(self.input_validation)

        if index == "fineEsercizio":
            data_fine_esercizio = self.input_lines["inizioEsercizio"].text().split('/')
            data_fine_esercizio = datetime.date(int(data_fine_esercizio[2]), int(data_fine_esercizio[1]), int(data_fine_esercizio[0]))
            input_line.setDate(data_fine_esercizio + datetime.timedelta(days=364))
            input_line.dateChanged.connect(self.input_validation)

        self.input_lines[index] = input_line
        self.input_errors[index] = error

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        input_layout.addWidget(error)
        input_layout.addLayout(pair_layout)

        return input_layout

    def update_list(self):
        self.all_bilanci = list(Bilancio.getAllBilanciByImmobile(self.immobile).values())
        Bilancio.ordinaBilancioByDataInizio(self.all_bilanci)

        if not self.all_bilanci:
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()
        elif not self.timer.isActive():
            self.msg.hide()

        listview_model = QStandardItemModel(self.list_view_bilanci)
        for bilancio in self.all_bilanci:
            item = QStandardItem()
            if bilancio.isApprovata:
                item_text = f"Bilancio: {bilancio.inizioEsercizio} - {bilancio.fineEsercizio} -> Approvato il {bilancio.dataApprovazione}"
            else:
                item_text = f"Bilancio: {bilancio.inizioEsercizio} - {bilancio.fineEsercizio} -> Non Approvato"
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
        item = None
        for index in self.list_view_bilanci.selectedIndexes():
            item = self.list_view_bilanci.model().itemFromIndex(index)
        bilancio = Bilancio.ricercaBilancioByDataInizio(item.text().split(" ")[1], self.immobile)
        self.choose_bilancio = VistaGestioneBilancio(self.immobile, bilancio)
        self.choose_bilancio.show()

    def goNuovoEsercizio(self):
        data_inizio = self.input_lines["inizioEsercizio"].text()
        data_inizio = data_inizio.split("/")
        data_inizio = datetime.date(int(data_inizio[2]), int(data_inizio[1]), int(data_inizio[0]))

        data_fine = self.input_lines["fineEsercizio"].text()
        data_fine = data_fine.split("/")
        data_fine = datetime.date(int(data_fine[2]), int(data_fine[1]), int(data_fine[0]))
        temp_bilancio = Bilancio()
        msg, bilancio = temp_bilancio.aggiungiBilancio(data_fine, self.immobile, {}, data_inizio, 0,
                                                       {}, {}, {}, {}, {}, {}, False, None)
        self.callback(msg)
        self.nuovo_esercizio = VistaGestioneBilancio(self.immobile, bilancio)
        self.nuovo_esercizio.show()


    def able_button(self):
        if not self.list_view_bilanci.selectedIndexes():
            self.button_list["Vai al bilancio"].setDisabled(True)
        else:
            self.button_list["Vai al bilancio"].setDisabled(False)

    def autoset_data_fine(self):
        data_inizio = self.input_lines["inizioEsercizio"].text()
        data_inizio = data_inizio.split("/")
        data_inizio = datetime.date(int(data_inizio[2]), int(data_inizio[1]), int(data_inizio[0]))
        data_fine = data_inizio + datetime.timedelta(days=364)
        self.input_lines["fineEsercizio"].setDate(data_fine)

    def input_validation(self):
        data_inizio = self.input_lines["inizioEsercizio"].text()
        data_inizio = data_inizio.split("/")
        data_inizio = datetime.date(int(data_inizio[2]), int(data_inizio[1]), int(data_inizio[0]))

        data_fine = self.input_lines["fineEsercizio"].text()
        data_fine = data_fine.split("/")
        data_fine = datetime.date(int(data_fine[2]), int(data_fine[1]), int(data_fine[0]))

        if data_inizio > data_fine:
            self.button_list["Nuovo Esercizio"].setDisabled(True)
        else:
            self.button_list["Nuovo Esercizio"].setDisabled(False)

    def callback(self, msg=""):
        print("sono nella callback")
        self.button_list["Vai al bilancio"].setDisabled(True)
        self.button_list["Nuovo Esercizio"].setDisabled(False)
        self.update_list()
        if msg:
            self.msg.setText(msg)
            self.msg.show()
            self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not self.all_bilanci:
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()