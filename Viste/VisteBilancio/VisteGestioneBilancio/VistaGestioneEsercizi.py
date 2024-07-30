import datetime
import os
import webbrowser

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QDateEdit, QListWidget, \
    QListWidgetItem

from Classes.Contabilita.bilancio import Bilancio
from Viste.VisteBilancio.VisteGestioneBilancio.VistaGestioneBilancio import VistaGestioneBilancio

class VistaGestioneEsercizi(QWidget):

    def __init__(self, immobile):
        super(VistaGestioneEsercizi, self).__init__()
        print("costruttore gest esercizi")
        self.immobile = immobile
        self.input_lines = {}
        self.input_errors = {}
        main_layout = QVBoxLayout()
        action_layout = QHBoxLayout()

        print("print lista bilanci")
        self.list_view_bilanci = QListWidget()

        button_layout = QVBoxLayout()
        self.button_list = {}
        button_layout.addWidget(self.create_button("Vai al bilancio", self.goBilancio, True))
        action_layout.addWidget(self.list_view_bilanci)
        action_layout.addLayout(button_layout)

        action_data = QHBoxLayout()
        action_data.addLayout(self.pairLabelInput("Data inizio Esercizio", "inizioEsercizio"))
        action_data.addLayout(self.pairLabelInput("Data fine Esercizio", "fineEsercizio"))
        action_data.addWidget(self.create_button("Nuovo Esercizio", self.goNuovoEsercizio, False))

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
        print(self.immobile)
        bilanci_immobile = list(Bilancio.getAllBilanciByImmobile(self.immobile).values())
        print(bilanci_immobile)
        Bilancio.ordinaBilancioByDataInizio(bilanci_immobile)

        print(bilanci_immobile)

        if not bilanci_immobile:
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()
        elif not self.timer.isActive():
            self.msg.hide()

        for bilancio in bilanci_immobile:
            print("printando", bilancio.getInfoBilancio())
            item = QListWidgetItem()
            if bilancio.isApprovata:
                item_text = f"Bilancio: {bilancio.inizioEsercizio} - {bilancio.fineEsercizio} -> Approvato il {bilancio.dataApprovazione}"
            else:
                item_text = f"Bilancio: {bilancio.inizioEsercizio} - {bilancio.fineEsercizio} -> Non Approvato"
            print("i")
            item.setText(item_text)
            print("i")
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            print("i")
            font = item.font()
            print("i")
            font.setPointSize(12)
            print("i")
            item.setFont(font)
            item.setData(Qt.ItemDataRole.UserRole, bilancio.codice)
            print("i")
            self.list_view_bilanci.addItem(item)
            print("ii")

        self.list_view_bilanci.itemSelectionChanged.connect(self.able_button)
        print("ii")

    def goBilancio(self):
        bilancio = Bilancio.ricercaBilancioByCodice(self.list_view_bilanci.selectedItems()[0].data(Qt.ItemDataRole.UserRole))
        self.choose_bilancio = VistaGestioneBilancio(bilancio)
        self.choose_bilancio.show()

    def goNuovoEsercizio(self):
        data_inizio = self.input_lines["inizioEsercizio"].text()
        data_inizio = data_inizio.split("/")
        data_inizio = datetime.date(int(data_inizio[2]), int(data_inizio[1]), int(data_inizio[0]))

        data_fine = self.input_lines["fineEsercizio"].text()
        data_fine = data_fine.split("/")
        data_fine = datetime.date(int(data_fine[2]), int(data_fine[1]), int(data_fine[0]))

        temp_bilancio = Bilancio()
        msg, bilancio = temp_bilancio.aggiungiBilancio(data_inizio, data_fine, self.immobile)

        self.callback(msg)
        print("fine callback")
        self.nuovo_esercizio = VistaGestioneBilancio(bilancio)

        self.nuovo_esercizio.show()


    def able_button(self):
        if not self.list_view_bilanci.selectedItems():
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
        if not list(Bilancio.getAllBilanciByImmobile(self.immobile).values()):
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()