import datetime

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QComboBox, QHBoxLayout, QListView, QLabel, \
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QCheckBox

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.immobile import Immobile
from Viste.VisteBilancio.VisteGestioneBilancio.VistaCalcoloConsuntivo import VistaCalcoloConsuntivo

class VistaListaSpese(QWidget):
    def __init__(self, bilancio, callback):
        super(VistaListaSpese, self).__init__()

        self.immobile = Immobile.ricercaImmobileById(bilancio.immobile)
        self.bilancio = bilancio
        self.callback = callback
        self.button_list = {}
        self.checkboxes = {}
        self.checkboxes_pagata = {}
        self.lista_spese = []

        main_layout = QVBoxLayout()

        self.table_spese = QTableWidget()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button("Vai a Consuntivo", self.goCalcolaConsuntivo))

        message_layout = QHBoxLayout()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        self.update_table()
        message_layout.addWidget(self.msg)

        main_layout.addWidget(self.table_spese)
        main_layout.addLayout(message_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(800, 540)
        self.setWindowTitle("Lista Spese")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setMinimumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        button.setCheckable(False)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def update_table(self):
        self.bilancio.aggiornaListaSpeseAConsuntivo()

        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

        if not self.bilancio.listaSpeseAConsuntivo and not self.bilancio.listaSpeseNonAConsuntivo:
            self.msg.setText("Non sono presenti spese in questo esercizio")
            self.msg.show()
        elif not self.timer.isActive():
            self.msg.hide()

        self.table_spese.setRowCount(len(self.bilancio.listaSpeseAConsuntivo) + len(self.bilancio.listaSpeseNonAConsuntivo))
        self.table_spese.setColumnCount(9)
        self.table_spese.setHorizontalHeaderLabels(["Cod.", "Immobile", "Data di pagamento", "Descrizione", "Tipologia di spesa", "Fornitore", "Importo", "Pagata", "A Consuntivo"])
        self.table_spese.verticalHeader().setVisible(False)

        i = 0
        for cod_spesa in self.bilancio.listaSpeseAConsuntivo:
            spesa = Spesa.ricercaSpesaByCodice(cod_spesa)

            self.table_spese.setItem(i, 0, QTableWidgetItem(str(spesa.codice)))
            self.table_spese.item(i, 0).setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table_spese.setItem(i, 1, QTableWidgetItem(Immobile.ricercaImmobileById(spesa.immobile).denominazione))
            if spesa.dataPagamento is not None:
                self.table_spese.setItem(i, 2, QTableWidgetItem(spesa.dataPagamento.strftime("%Y/%m/%d")))
            else:
                self.table_spese.setItem(i, 2, QTableWidgetItem(""))
            self.table_spese.setItem(i, 3, QTableWidgetItem(spesa.descrizione))
            self.table_spese.setItem(i, 4, QTableWidgetItem(TipoSpesa.ricercaTipoSpesaByCodice(spesa.tipoSpesa).nome))
            self.table_spese.setItem(i, 5, QTableWidgetItem(Fornitore.ricercaFornitoreByCodice(spesa.fornitore).denominazione))
            self.table_spese.setItem(i, 6, QTableWidgetItem(str("%.2f" % spesa.importo)))
            self.table_spese.item(i, 6).setTextAlignment(Qt.AlignmentFlag.AlignRight)

            cell_widget = QWidget()
            checkbox_pagata = QCheckBox()
            self.checkboxes_pagata[spesa.codice] = checkbox_pagata
            checkbox_pagata.stateChanged.connect(self.reset_pagata)
            if spesa.pagata:
                checkbox_pagata.setCheckState(Qt.CheckState.Checked)
            else:
                checkbox_pagata.setCheckState(Qt.CheckState.Unchecked)

            checkbox_pagata.setTristate(False)

            checkbox_layout = QHBoxLayout(cell_widget)
            checkbox_layout.addWidget(checkbox_pagata)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(checkbox_layout)

            self.table_spese.setCellWidget(i, 7, cell_widget)
            cell_widget_scelta = QWidget()
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.checkboxes[spesa.codice] = checkbox

            checkbox.stateChanged.connect(self.changeList)

            checkbox_scelta_layout = QHBoxLayout(cell_widget_scelta)
            checkbox_scelta_layout.addWidget(checkbox)
            checkbox_scelta_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_scelta_layout.setContentsMargins(0, 0, 0, 0)
            cell_widget_scelta.setLayout(checkbox_scelta_layout)
            self.table_spese.setCellWidget(i, 8, cell_widget_scelta)
            i += 1

        for cod_spesa in self.bilancio.listaSpeseNonAConsuntivo:
            spesa = Spesa.ricercaSpesaByCodice(cod_spesa)

            self.table_spese.setItem(i, 0, QTableWidgetItem(str(spesa.codice)))
            self.table_spese.item(i, 0).setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table_spese.setItem(i, 1, QTableWidgetItem(Immobile.ricercaImmobileById(spesa.immobile).denominazione))
            if spesa.dataPagamento is not None:
                self.table_spese.setItem(i, 2, QTableWidgetItem(spesa.dataPagamento.strftime("%Y/%m/%d")))
            else:
                self.table_spese.setItem(i, 2, QTableWidgetItem(""))
            self.table_spese.setItem(i, 3, QTableWidgetItem(spesa.descrizione))
            self.table_spese.setItem(i, 4, QTableWidgetItem(TipoSpesa.ricercaTipoSpesaByCodice(spesa.tipoSpesa).nome))
            self.table_spese.setItem(i, 5, QTableWidgetItem(Fornitore.ricercaFornitoreByCodice(spesa.fornitore).denominazione))
            self.table_spese.setItem(i, 6, QTableWidgetItem(str("%.2f" % spesa.importo)))
            self.table_spese.item(i, 6).setTextAlignment(Qt.AlignmentFlag.AlignRight)
            cell_widget = QWidget()
            checkbox_pagata = QCheckBox()
            self.checkboxes_pagata[spesa.codice] = checkbox_pagata
            checkbox_pagata.stateChanged.connect(self.reset_pagata)
            if spesa.pagata:
                checkbox_pagata.setCheckState(Qt.CheckState.Checked)
            else:
                checkbox_pagata.setCheckState(Qt.CheckState.Unchecked)

            checkbox_pagata.setTristate(False)

            checkbox_layout = QHBoxLayout(cell_widget)
            checkbox_layout.addWidget(checkbox_pagata)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(checkbox_layout)

            self.table_spese.setCellWidget(i, 7, cell_widget)
            cell_widget_scelta = QWidget()
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            self.checkboxes[spesa.codice] = checkbox

            checkbox.stateChanged.connect(self.changeList)

            checkbox_scelta_layout = QHBoxLayout(cell_widget_scelta)
            checkbox_scelta_layout.addWidget(checkbox)
            checkbox_scelta_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_scelta_layout.setContentsMargins(0, 0, 0, 0)
            cell_widget_scelta.setLayout(checkbox_scelta_layout)
            self.table_spese.setCellWidget(i, 8, cell_widget_scelta)
            i += 1
        self.table_spese.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_spese.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table_spese.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        self.table_spese.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_spese.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_spese.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def reset_pagata(self):
        checkbox = self.sender()
        for cod_spesa, cell_widget_checkbox in self.checkboxes_pagata.items():
            if cell_widget_checkbox is checkbox:
                spesa = Spesa.ricercaSpesaByCodice(cod_spesa)
        if spesa.pagata:
            checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            checkbox.setCheckState(Qt.CheckState.Unchecked)

    def goCalcolaConsuntivo(self):
        self.bilancio.passaggioRaggiunto("speseConsuntivate")
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        self.bilancio.calcolaSpeseConsuntivo()
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        self.close()
        self.calcolo_consuntivo = VistaCalcoloConsuntivo(self.bilancio, self.callback)
        self.calcolo_consuntivo.show()

    def changeList(self):
        for cod_spesa, checkbox in self.checkboxes.items():
            if checkbox is self.sender():
                self.bilancio.changeListaConsuntivo(cod_spesa)
        self.update_table()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()