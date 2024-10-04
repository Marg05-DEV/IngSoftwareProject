import re

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QSizePolicy, QHeaderView, QAbstractItemView

from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaCreateTabellaMillesimale import \
    VistaCreateTabellaMillesimale
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaReadTabellaMillesimale import VistaReadTabellaMillesimale
from Viste.VisteBilancio.VisteGestioneTabellaMillesimale.VistaDeleteTabellaMillesimale import \
    VistaDeleteTabellaMillesimale


class VistaGestioneTabelleMillesimali(QWidget):

    def __init__(self, immobile):
        super(VistaGestioneTabelleMillesimali, self).__init__()
        self.immobile = immobile
        main_layout = QVBoxLayout()
        action_layout = QHBoxLayout()

        self.table_tabellaMillesimale = QTableWidget()
        self.table_tabellaMillesimale.cellChanged.connect(self.saveMatrix)
        self.update_table()

        action_layout.addWidget(self.table_tabellaMillesimale)

        button_layout = QVBoxLayout()
        self.button_list = {}

        button_layout.addWidget(self.create_button("Aggiungi Tabella Millesimale", self.go_add_tabellaMillesimale))
        button_layout.addWidget(
            self.create_button("Visualizza Tabella Millesimale", self.go_read_tabellaMillesimale, True))
        button_layout.addWidget(
            self.create_button("Rimuovi Tabella Millesimale", self.go_delete_tabellaMillesimale, True))
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
        self.resize(1200, 650)
        self.setWindowTitle("Gestione Immobile")

    def create_button(self, testo, action, disabled=False):
        button = QPushButton(testo)
        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        button.clicked.connect(action)
        button.setDisabled(disabled)
        self.button_list[testo] = button
        return button

    def update_table(self):
        self.table_tabellaMillesimale.cellChanged.disconnect(self.saveMatrix)
        unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values())
        tabelle_millesimali = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values())

        self.table_tabellaMillesimale.setRowCount(len(unita_immobiliari) + 1)
        self.table_tabellaMillesimale.setColumnCount(len(tabelle_millesimali))

        i = 0
        for tabella in tabelle_millesimali:
            self.table_tabellaMillesimale.setHorizontalHeaderItem(i, QTableWidgetItem(
                f"{tabella.nome}\n{tabella.descrizione}"))
            self.table_tabellaMillesimale.horizontalHeaderItem(i).setData(Qt.ItemDataRole.UserRole, tabella.codice)
            i += 1

        totale_millesimi_tabella = {}
        i = 0
        for unita in unita_immobiliari:
            proprietario = [item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"]
            if unita.tipoUnitaImmobiliare == "Appartamento":
                if unita.condomini:
                    if proprietario:
                            proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                            self.table_tabellaMillesimale.setVerticalHeaderItem(i, QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di\n{proprietario.cognome} {proprietario.nome}"))
                    else:
                        self.table_tabellaMillesimale.setVerticalHeaderItem(i, QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di\nNessun Proprietario"))
                else:
                    self.table_tabellaMillesimale.setVerticalHeaderItem(i, QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} con\nNessun Condomino"))
            else:
                if unita.condomini:
                    if proprietario:
                        proprietario = Condomino.ricercaCondominoByCodice(proprietario[0])
                        self.table_tabellaMillesimale.setVerticalHeaderItem(i, QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} di\n{proprietario.cognome} {proprietario.nome}"))
                    else:
                        self.table_tabellaMillesimale.setVerticalHeaderItem(i, QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} di\nNessun Proprietario"))
                else:
                    self.table_tabellaMillesimale.setVerticalHeaderItem(i, QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} con\nNessun Condomino"))

            j = 0
            for tabella in tabelle_millesimali:
                if unita.codice not in tabella.millesimi:
                    tabella.addMillesimo(unita, 0.00)
                    tabella = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella.codice)

                if j in totale_millesimi_tabella:
                    totale_millesimi_tabella[j] += tabella.millesimi[unita.codice]
                else:
                    totale_millesimi_tabella[j] = tabella.millesimi[unita.codice]

                self.table_tabellaMillesimale.setItem(i, j, QTableWidgetItem("%.2f" % tabella.millesimi[unita.codice]))
                self.table_tabellaMillesimale.item(i, j).setData(Qt.ItemDataRole.UserRole,[unita.codice, tabella.codice])
                j += 1

            i += 1

        self.table_tabellaMillesimale.setVerticalHeaderItem(len(unita_immobiliari),
                                                            QTableWidgetItem("TOTALE MILLESIMI"))

        for tabella, totale in totale_millesimi_tabella.items():
            self.table_tabellaMillesimale.setItem(len(unita_immobiliari), tabella, QTableWidgetItem("%.2f" % totale))
            self.table_tabellaMillesimale.item(len(unita_immobiliari), tabella).setFlags(Qt.ItemFlag.ItemIsEnabled)

        self.table_tabellaMillesimale.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_tabellaMillesimale.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.table_tabellaMillesimale.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_tabellaMillesimale.verticalHeader().setSectionResizeMode(len(unita_immobiliari),
                                                                            QHeaderView.ResizeMode.ResizeToContents)
        self.table_tabellaMillesimale.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table_tabellaMillesimale.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table_tabellaMillesimale.cellChanged.connect(self.saveMatrix)

    def saveMatrix(self, row, column):
        match = re.fullmatch("[0-9]*|[0-9]*[.,][0-9]{0,2}", self.table_tabellaMillesimale.item(row, column).text())
        coordinate = self.table_tabellaMillesimale.item(row, column).data(Qt.ItemDataRole.UserRole)
        if coordinate is not None:
            if match is not None:
                millesimo = float(self.table_tabellaMillesimale.item(row, column).text().replace(",", "."))
                TabellaMillesimale.ricercaTabelleMillesimaliByCodice(coordinate[1]).addMillesimo(
                    UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(coordinate[0]), millesimo)
            else:
                self.msg.setText("Il valore inserito nella cella non è valido")
                self.msg.show()
                self.timer.start()
            self.update_table()

    def go_add_tabellaMillesimale(self):
        self.vista_nuova_tabella_millesimale = VistaCreateTabellaMillesimale(self.immobile, callback=self.callback)
        self.vista_nuova_tabella_millesimale.show()

    def go_read_tabellaMillesimale(self):
        codice_tabella_selezionata = self.table_tabellaMillesimale.horizontalHeaderItem(self.tabella_selezionata).data(
            Qt.ItemDataRole.UserRole)
        self.vista_dettaglio_tabella_millesimale = VistaReadTabellaMillesimale(codice_tabella_selezionata,
                                                                               callback=self.callback)
        self.vista_dettaglio_tabella_millesimale.show()

    def go_delete_tabellaMillesimale(self):
        codice_tabella_selezionata = self.table_tabellaMillesimale.horizontalHeaderItem(self.tabella_selezionata).data(
            Qt.ItemDataRole.UserRole)
        self.vista_dettaglio_tabella_millesimale = VistaDeleteTabellaMillesimale(codice_tabella_selezionata,
                                                                                 callback=self.callback)
        self.vista_dettaglio_tabella_millesimale.show()

    def able_button(self, logicalIndex):
        self.tabella_selezionata = logicalIndex
        header = self.table_tabellaMillesimale.horizontalHeaderItem(self.tabella_selezionata)
        if not header:
            self.button_list["Visualizza Tabella Millesimale"].setDisabled(True)
            self.button_list["Rimuovi Tabella Millesimale"].setDisabled(True)
        else:
            self.button_list["Visualizza Tabella Millesimale"].setDisabled(False)
            self.button_list["Rimuovi Tabella Millesimale"].setDisabled(False)

    def callback(self, msg):
        self.button_list["Visualizza Tabella Millesimale"].setDisabled(True)
        self.button_list["Rimuovi Tabella Millesimale"].setDisabled(True)
        self.update_table()
        if msg:
            self.msg.setText(msg)
            self.msg.show()
            self.timer.start()

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()