import datetime

from PyQt6.QtCore import QTimer, Qt, QDate
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QLabel, QTableWidgetItem, QSizePolicy, \
    QHeaderView, QDateEdit

from Classes.Contabilita.rata import Rata
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaSaldoCassa(QWidget):
    def __init__(self):
        super(VistaSaldoCassa, self).__init__()
        print("busso")
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.new_label("Saldo cassa del giorno"))
        print("busso1")
        self.table_rate = QTableWidget()
        self.update_table()
        main_layout.addWidget(self.table_rate)

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addWidget(self.msg)
        main_layout.addWidget(self.saldo("Saldo in Contanti", "Contanti"))
        main_layout.addWidget(self.saldo("Saldo in Assegni Bancari ", "Assegno Bancario"))
        self.setLayout(main_layout)
        self.resize(1200, 650)
        self.setWindowTitle("Proposta Preventivo")

    def update_table(self):
        print("crazione tabella")
        rate_pagate = []
        self.all_rate = Rata.getAllRate()
        for rate in self.all_rate.values():
            if rate.pagata:
                rate_pagate.append(rate.codice)
        self.table_rate.setRowCount(len(rate_pagate))
        self.table_rate.setColumnCount(3)

        self.table_rate.setHorizontalHeaderLabels(["Rata", "Importo", "A/B o Contanti"])
        i = 0
        for rata in rate_pagate:
            rata_pagata = Rata.ricercaRataByCodice(rata)
            item_text = f"Versante:{rata_pagata.versante}\n"
            item_table = QTableWidgetItem(item_text)

            item_text1 = f"{rata_pagata.importo}"
            item_table1 = QTableWidgetItem(item_text1)

            item_text2 = f"{rata_pagata.tipoPagamento}"
            item_table2 = QTableWidgetItem(item_text2)

            item_table.setFlags(Qt.ItemFlag.NoItemFlags)
            item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_rate.setItem(i, 0, item_table)
            self.table_rate.setItem(i, 1, item_table1)
            self.table_rate.setItem(i, 2, item_table2)
            i += 1

        self.table_rate.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_rate.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_rate.horizontalHeader().setStretchLastSection(True)
        self.table_rate.verticalHeader().setSectionsClickable(False)
        self.table_rate.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table_rate.resizeRowsToContents()
        self.table_rate.resizeColumnsToContents()
        header = self.table_rate.verticalHeader()
        self.table_rate.setMaximumHeight(header.height())
        print("create tabella")

        return self.table_rate
    def new_label(self, testo):
        print("io")
        print(datetime.date.today())
        label = QLabel(testo + "   " + str(datetime.date.today()))
        return label
    def saldo(self, testo, tipo_pagameto):
        importo_totale = 0.0
        for rate in self.all_rate.values():
            if rate.pagata:
                if rate.tipoPagamento == tipo_pagameto:
                    importo_totale += rate.importo
        label = QLabel(testo + " ..... " + str(importo_totale))
        return label
    def callback(self, msg, tab):
        print(" callback chiamata", msg)
        self.update_table()
        if msg:
            self.msg.setText(msg)
            self.msg.show()
            self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()