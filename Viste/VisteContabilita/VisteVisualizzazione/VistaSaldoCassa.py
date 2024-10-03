import datetime

from PyQt6.QtCore import QTimer, Qt, QDate
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QLabel, QTableWidgetItem, QSizePolicy, \
    QHeaderView, QDateEdit, QAbstractItemView

from Classes.Contabilita.rata import Rata
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaSaldoCassa(QWidget):
    def __init__(self):
        super(VistaSaldoCassa, self).__init__()
        self.saldo_contanti = 0.00
        self.saldo_assegni = 0.00
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.new_label("Saldo cassa del giorno"), alignment=Qt.AlignmentFlag.AlignLeft)
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
        self.setWindowTitle("Saldo cassa del " + datetime.date.today().strftime("%d-%m-%Y"))

    def update_table(self):
        all_rate = [item for item in Rata.getAllRate().values()]
        rate_pagate_oggi = [item for item in all_rate if item.dataPagamento == datetime.date.today()]

        self.table_rate.setRowCount(len(rate_pagate_oggi)+1)
        self.table_rate.setColumnCount(3)

        self.table_rate.setHorizontalHeaderLabels(["Descrizione movimento", "Importo", "A/B o Contanti"])

        rimanenza = 0.00

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        for rata in all_rate:
            if yesterday >= rata.dataPagamento:
                if rata.tipoPagamento == "Contanti":
                    rimanenza += rata.importo

        for n in range(len(rate_pagate_oggi)+1):
            if n == 0:
                self.table_rate.setItem(0, 0, QTableWidgetItem(f"Rimanenze fino al giorno {yesterday}"))
                self.table_rate.setItem(0, 1, QTableWidgetItem("%.2f" % rimanenza))
                self.table_rate.setItem(0, 2, QTableWidgetItem(""))

                self.saldo_contanti += rimanenza

            if n > 0:
                self.table_rate.setItem(n, 0, QTableWidgetItem(f"{rate_pagate_oggi[n-1].descrizione} di {rate_pagate_oggi[n-1].versante}"))
                self.table_rate.setItem(n, 1, QTableWidgetItem("%.2f" % rate_pagate_oggi[n-1].importo))
                self.table_rate.setItem(n, 2, QTableWidgetItem(rate_pagate_oggi[n-1].tipoPagamento))

                if rate_pagate_oggi[n-1].tipoPagamento == "Contanti":
                    self.saldo_contanti += rate_pagate_oggi[n-1].importo
                elif rate_pagate_oggi[n-1].tipoPagamento == "Assegno Bancario":
                    self.saldo_assegni += rate_pagate_oggi[n-1].importo

        self.table_rate.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_rate.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_rate.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_rate.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table_rate.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_rate.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        return self.table_rate
    def new_label(self, testo):
        label = QLabel(testo + "   " + str(datetime.date.today()))
        return label

    def saldo(self, testo, tipo_pagamento):
        label = QLabel("")
        if tipo_pagamento == "Contanti":
            label = QLabel(testo + " ..... " + str("%.2f" % self.saldo_contanti))
        elif tipo_pagamento == "Assegno Bancario":
            label = QLabel(testo + " ..... " + str("%.2f" % self.saldo_assegni))
        return label

    def callback(self, msg, tab):
        self.update_table()
        if msg:
            self.msg.setText(msg)
            self.msg.show()
            self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()