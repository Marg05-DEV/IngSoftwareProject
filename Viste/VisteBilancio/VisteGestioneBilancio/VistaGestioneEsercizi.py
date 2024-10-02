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

        new_esercizio_layout = QVBoxLayout()
        date_esercizio_layout = QHBoxLayout()
        button_new_esercizio_layout = QHBoxLayout()

        date_esercizio_layout.addLayout(self.pairLabelInput("Data inizio Esercizio", "inizioEsercizio"))
        date_esercizio_layout.addLayout(self.pairLabelInput("Data fine Esercizio", "fineEsercizio"))

        button_new_esercizio_layout.addWidget(self.create_button("Nuovo Esercizio", self.goNuovoEsercizio, False), Qt.AlignmentFlag.AlignLeft)

        self.button_list["Nuovo Esercizio"].setMaximumSize(150, 50)
        self.button_list["Nuovo Esercizio"].setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        new_esercizio_layout.addLayout(date_esercizio_layout)
        new_esercizio_layout.addLayout(button_new_esercizio_layout)
        print("prima richiamo")


        self.lbl_bilancio_exists = QLabel("Il bilancio è esistente")
        self.lbl_bilancio_exists.setStyleSheet("font-weight: bold;")
        self.input_errors["error"] = self.lbl_bilancio_exists
        self.input_errors["error"].setVisible(False)
        self.input_validation()

        self.msg = QLabel("Non ci sono esercizi")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addLayout(action_layout)
        main_layout.addLayout(new_esercizio_layout)
        main_layout.addWidget(self.lbl_bilancio_exists)
        main_layout.addWidget(self.msg)

        self.update_list()

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Esercizio")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def pairLabelInput(self, testo, index):
        print("da subito")
        input_layout = QVBoxLayout()
        pair_layout = QHBoxLayout()

        error = QLabel("placeholder")
        error.setStyleSheet("color: red; font-style: italic;")
        error.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        error.setVisible(False)

        label = QLabel(testo + "*: ")
        input_line = QDateEdit()
        if index == "inizioEsercizio":
            print("primo controllo")
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
        bilanci_immobile = list(Bilancio.getAllBilanciByImmobile(self.immobile).values())
        Bilancio.ordinaBilancioByDataInizio(bilanci_immobile)

        if not bilanci_immobile:
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()
        elif not self.timer.isActive():
            self.msg.hide()

        self.list_view_bilanci.clear()

        for bilancio in bilanci_immobile:
            print("printando", bilancio.getInfoBilancio())
            item = QListWidgetItem()
            if bilancio.isApprovata:
                item_text = f"Bilancio: {bilancio.inizioEsercizio} - {bilancio.fineEsercizio} -> Approvato il {bilancio.dataApprovazione}"
            else:
                item_text = f"Bilancio: {bilancio.inizioEsercizio} - {bilancio.fineEsercizio} -> Non Approvato"
            item.setText(item_text)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            item.setData(Qt.ItemDataRole.UserRole, bilancio.codice)
            self.list_view_bilanci.addItem(item)

        self.list_view_bilanci.itemSelectionChanged.connect(self.able_button)

    def goBilancio(self):
        bilancio = Bilancio.ricercaBilancioByCodice(self.list_view_bilanci.selectedItems()[0].data(Qt.ItemDataRole.UserRole))
        self.choose_bilancio = VistaGestioneBilancio(bilancio, self.callback)
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
        self.nuovo_esercizio = VistaGestioneBilancio(bilancio, self.callback)
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
        print("a")
        data_inizio = self.input_lines["inizioEsercizio"].text()
        data_inizio = data_inizio.split("/")
        data_inizio = datetime.date(int(data_inizio[2]), int(data_inizio[1]), int(data_inizio[0]))
        print("b")

        data_fine = self.input_lines["fineEsercizio"].text()
        data_fine = data_fine.split("/")
        data_fine = datetime.date(int(data_fine[2]), int(data_fine[1]), int(data_fine[0]))
        print("c")
        bilancio_esistente = False
        for bilancio in Bilancio.getAllBilanciByImmobile(self.immobile).values():
            if (data_inizio >= bilancio.inizioEsercizio and data_inizio <= bilancio.fineEsercizio) or (data_fine >= bilancio.inizioEsercizio and data_fine <= bilancio.fineEsercizio):
                bilancio_esistente = True

        if bilancio_esistente:
            self.input_errors["error"].setVisible(True)
        else:
            self.input_errors["error"].setVisible(False)
        print(self.input_errors["error"].isVisible())
        if data_inizio > data_fine or self.input_errors["error"].isVisible():
            print("e")
            self.button_list["Nuovo Esercizio"].setDisabled(True)
        else:
            print("f")
            self.button_list["Nuovo Esercizio"].setDisabled(False)

    def callback(self, msg=""):
        self.input_validation()
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