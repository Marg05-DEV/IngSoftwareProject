from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, \
    QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QSizePolicy, QHeaderView

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Viste.VisteGestioneBilancio.VisteGestioneTabellaMillesimale.VistaCreateTabellaMillesimale import VistaCreateTabellaMillesimale
from Viste.VisteGestioneBilancio.VisteGestioneTabellaMillesimale.VistaReadTabellaMillesimale import VistaReadTabellaMillesimale
from Viste.VisteGestioneBilancio.VisteGestioneTabellaMillesimale.VistaDeleteTabellaMillesimale import VistaDeleteTabellaMillesimale

class VistaGestioneTabelleMillesimali(QWidget):

    def __init__(self, immobile):
        super(VistaGestioneTabelleMillesimali, self).__init__()
        self.immobile = immobile
        main_layout = QVBoxLayout()
        action_layout = QHBoxLayout()

        self.table_tabellaMillesimale = self.create_table()
        action_layout.addWidget(self.table_tabellaMillesimale)

        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Tabella Millesimale", self.go_add_tabellaMillesimale))
        button_layout.addWidget(self.create_button("Visualizza Tabella Millesimale", self.go_read_tabellaMillesimale, True))
        button_layout.addWidget(self.create_button("Rimuovi Tabella Millesimale", self.go_delete_tabellaMillesimale, True))
        self.table_tabellaMillesimale.horizontalHeader().sectionClicked.connect(self.able_button)
        message_layout = QHBoxLayout()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        message_layout.addWidget(self.msg)
        action_layout.addLayout(button_layout)

        main_layout.addLayout(action_layout)
        main_layout.addLayout(message_layout)

        self.setLayout(main_layout)
        self.resize(1200, 800)
        self.setWindowTitle("Gestione Immobile")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def create_table(self):
        print("crazione tabella")
        table = QTableWidget()
        self.unitaImmobiliari_immobile = UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile)
        self.tabelle_millesimali = TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile)
        table.setRowCount(len(self.unitaImmobiliari_immobile))
        table.setColumnCount(len(self.tabelle_millesimali))
        i = 0
        for unita in self.unitaImmobiliari_immobile.values():
            text_condomini = ""
            condomini = []
            print(unita.condomini.keys())
            for condo in unita.condomini.keys():
                condomino = Condomino.ricercaCondominoByCF(condo)
                nome_condo = f"{condomino.nome} {condomino.cognome}"
                titolo = unita.condomini[condo]
                print(titolo)
                stringa = f"{nome_condo} {titolo}"
                condomini.append(stringa)
            print(condomini)
            cont = 0
            if condomini:
                for condomino in condomini:
                    if not cont:
                        text_condomini = condomino
                    else:
                        text_condomini = text_condomini + ",\n" + condomino
                    cont += 1
            else:
                text_condomini = "Nessun condomino"

            if unita.tipoUnitaImmobiliare == "Appartamento":
                item_text = f"Scala:{unita.scala} Int:{unita.interno}\n Condomini:{text_condomini}"
            else:
                item_text = f"Tipo unità immobiliare:{unita.tipoUnitaImmobiliare}\n Condomini:{text_condomini}"
            item_table = QTableWidgetItem(item_text)
            item_table.setFlags(Qt.ItemFlag.NoItemFlags)
            item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setVerticalHeaderItem(i, item_table)
            i += 1
        print(self.tabelle_millesimali)

        i = 0
        for tabelle in self.tabelle_millesimali.values():
            print("miao")
            print(tabelle.nome)
            item_text = f"{tabelle.nome}\n {tabelle.descrizione}"
            print(item_text)
            item_table = QTableWidgetItem(item_text)
            item_table.setFlags(Qt.ItemFlag.NoItemFlags)
            item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setHorizontalHeaderItem(i, item_table)
            i += 1

        print("create tabella")
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setSectionsClickable(False)
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        header = table.verticalHeader()
        table.setMaximumHeight(header.length())
        print("create tabella")

        return table

    def go_add_tabellaMillesimale(self):
        self.vista_nuovo_immobile = VistaCreateTabellaMillesimale(self.immobile, callback=self.callback)
        self.vista_nuovo_immobile.show()

    def go_read_tabellaMillesimale(self):
        print(self.logicalIndex)
        item = self.table_tabellaMillesimale.horizontalHeaderItem(self.logicalIndex)
        print(item)
        tabelle_millesimali = TabellaMillesimale.getAllTabelleMillesimali()
        print(tabelle_millesimali.values())
        codice_tabella = 0
        for tabelle in tabelle_millesimali.values():
            if item.text().split("\n")[0] == tabelle.nome:
                codice_tabella = tabelle.codice
        print(codice_tabella)
        self.vista_dettaglio_tabella_millesimale = VistaReadTabellaMillesimale(codice_tabella, callback=self.callback)
        self.vista_dettaglio_tabella_millesimale.show()

    def go_delete_tabellaMillesimale(self):
        print(self.logicalIndex)
        item = self.table_tabellaMillesimale.horizontalHeaderItem(self.logicalIndex)
        print(item)
        tabelle_millesimali = TabellaMillesimale.getAllTabelleMillesimali()
        print(tabelle_millesimali.values())
        codice_tabella = 0
        for tabelle in tabelle_millesimali.values():
            if item.text().split("\n")[0] == tabelle.nome:
                codice_tabella = tabelle.codice
        print(codice_tabella)
        self.vista_dettaglio_tabella_millesimale = VistaDeleteTabellaMillesimale(codice_tabella, callback=self.callback)
        self.vista_dettaglio_tabella_millesimale.show()


    def able_button(self, logicalIndex):
        print("ciao")
        print(logicalIndex)
        self.logicalIndex = logicalIndex
        header = self.table_tabellaMillesimale.horizontalHeaderItem(self.logicalIndex)
        print(header.text().split("\n")[0])
        if not header:
            self.button_list["Visualizza Tabella Millesimale"].setDisabled(True)
            self.button_list["Rimuovi Tabella Millesimale"].setDisabled(True)
        else:
            self.button_list["Visualizza Tabella Millesimale"].setDisabled(False)
            self.button_list["Rimuovi Tabella Millesimale"].setDisabled(False)

    def callback(self, msg):
        self.button_list["Visualizza Tabella Millesimale"].setDisabled(True)
        self.button_list["Rimuovi Tabella Millesimale"].setDisabled(True)
        self.create_table()
        if msg:
            self.msg.setText(msg)
            self.msg.show()
            self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()