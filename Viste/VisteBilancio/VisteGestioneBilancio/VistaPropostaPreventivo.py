from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QLabel, QTableWidgetItem, QSizePolicy, \
    QHeaderView

from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa

class VistaPropostaPreventivo(QWidget):
    def __init__(self, immobile):
        super(VistaPropostaPreventivo, self).__init__()
        self.immobile = immobile
        main_layout = QVBoxLayout()
        action_layout = QHBoxLayout()

        self.tab_mill = TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile)
        if self.tab_mill:
            for tab in self.tab_mill.values():
                if tab.tipologieSpesa:
                    self.table_tabellaMillesimale = QTableWidget()
                    self.update_table(tab)
                    main_layout.addWidget(self.table_tabellaMillesimale)
                    main_layout.addWidget(self.new_label("Totale preventivato per la tabella ", tab, False))
                else:
                    lbl_frase = QLabel("Tipi di spesa per la " + tab.nome + " inesistenti")
                    lbl_frase.setStyleSheet("font-weight: bold;")
                    main_layout.addWidget(lbl_frase)
        else:
            self.callback("Non ci sono tabelle millesimali associate all'immobile")


        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        action_layout.addWidget(self.msg)

        main_layout.addLayout(action_layout)
        main_layout.addWidget(self.new_label("Totale Preventivato", None, True))

        self.setLayout(main_layout)
        self.resize(1200, 650)
        self.setWindowTitle("Proposta Preventivo")

    def update_table(self, tab):
        print("crazione tabella")
        self.tab = tab
        self.table_tabellaMillesimale.setRowCount(len(self.tab.tipologieSpesa))
        self.table_tabellaMillesimale.setColumnCount(2)

        self.table_tabellaMillesimale.setHorizontalHeaderLabels(["Tipo di spesa", "Importo Ipotizzato"])
        i = 0
        for tipo_spesa in self.tab.tipologieSpesa:
            tipo = TipoSpesa.ricercaTipoSpesaByCodice(tipo_spesa)
            item_text = f"Nome:{tipo.nome}\nDescrizione:{tipo.descrizione}"
            item_table = QTableWidgetItem(item_text)
            item_table.setFlags(Qt.ItemFlag.NoItemFlags)
            item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_tabellaMillesimale.setItem(i, 0, item_table)
            self.table_tabellaMillesimale.setItem(i, 1, QTableWidgetItem("00.00"))
            i += 1

        self.table_tabellaMillesimale.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_tabellaMillesimale.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_tabellaMillesimale.horizontalHeader().setStretchLastSection(True)
        self.table_tabellaMillesimale.verticalHeader().setSectionsClickable(False)
        self.table_tabellaMillesimale.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table_tabellaMillesimale.resizeRowsToContents()
        self.table_tabellaMillesimale.resizeColumnsToContents()
        header = self.table_tabellaMillesimale.verticalHeader()
        self.table_tabellaMillesimale.setMaximumHeight(header.height())
        print("create tabella")

        return self.table_tabellaMillesimale
    def new_label(self, testo, tabella, valore_totale):
        if not valore_totale:
            importo = 00.00
            label = QLabel(testo + tabella.nome + "   " + str(importo))
        else:
            importo = 00.00
            for t in self.tab_mill.values():
                importo = 00.00
            label = QLabel(testo + "   " + str(importo))
        return label
    def callback(self, msg, tab):
        print(" callback chiamata", msg)
        self.update_table(tab)
        if msg:
            self.msg.setText(msg)
            self.msg.show()
            self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()