from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QSizePolicy

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaRipartizionePreventivo(QWidget):
    def __init__(self, bilancio):
        super(VistaRipartizionePreventivo, self).__init__()
        self.bilancio = bilancio
        self.immobile = Immobile.ricercaImmobileById(self.bilancio.immobile)
        self.input_lines = {}
        self.input_errors = {}
        main_layout = QVBoxLayout()

        self.table_ripartizionePreventivo = QTableWidget()
        self.update_table()

        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addWidget(self.table_ripartizionePreventivo)
        main_layout.addWidget(self.msg)

        self.setLayout(main_layout)
        self.resize(1200, 650)
        self.setWindowTitle("Ripartizione Preventivo")

    def update_table(self):
        unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values())
        tabelle_millesimali = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values())

        self.table_ripartizionePreventivo.setRowCount(len(unita_immobiliari) + 3)
        self.table_ripartizionePreventivo.setColumnCount((len(tabelle_millesimali))*2 + 4)

        bold_font = QFont()
        bold_font.setBold(True)

        self.table_ripartizionePreventivo.horizontalHeader().setFont(bold_font)

        j = 0
        for tabella in tabelle_millesimali:
            self.table_ripartizionePreventivo.setItem(1, j, QTableWidgetItem(f"{tabella.nome}\n{tabella.descrizione}"))
            self.table_ripartizionePreventivo.setItem(1, j + 1 + len(tabelle_millesimali), QTableWidgetItem(f"{tabella.nome}\nQuote:"))
            self.table_ripartizionePreventivo.item(1, j).setFont(bold_font)
            self.table_ripartizionePreventivo.item(1, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_ripartizionePreventivo.item(1, j + 1 + len(tabelle_millesimali)).setFont(bold_font)
            self.table_ripartizionePreventivo.item(1, j + 1 + len(tabelle_millesimali)).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            j += 1
        self.table_ripartizionePreventivo.setItem(1, len(tabelle_millesimali), QTableWidgetItem(f"Unità Immobiliari\nCondomino Proprietario"))
        self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali)).setFont(bold_font)
        self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali)).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_ripartizionePreventivo.setItem(1, len(tabelle_millesimali)*2 + 1, QTableWidgetItem(f"Totale Preventivo\nAnno Attuale"))
        self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali)*2 + 1).setFont(bold_font)
        self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali)*2 + 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_ripartizionePreventivo.setItem(1, len(tabelle_millesimali)*2 + 2, QTableWidgetItem(f"Conguaglio\nAnno Attuale"))
        self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali)*2 + 2).setFont(bold_font)
        self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali)*2 + 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_ripartizionePreventivo.setItem(1, len(tabelle_millesimali)*2 + 3, QTableWidgetItem(f"Totale\nDa Versare"))
        self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali)*2 + 3).setFont(bold_font)
        self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali)*2 + 3).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        """if self.bilancio.numeroRate != 0:
            for k in range(0, self.bilancio.numeroRate):
                self.table_ripartizionePreventivo.setItem(1, len(tabelle_millesimali) * 2 + 3 + k + 1, QTableWidgetItem(f"Rata {k + 1}"))
                self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali) * 2 + 3 + k + 1).setFont(bold_font)
                self.table_ripartizionePreventivo.item(1, len(tabelle_millesimali) * 2 + 3 + k + 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
"""
        self.table_ripartizionePreventivo.setItem(len(unita_immobiliari)+2, len(tabelle_millesimali), QTableWidgetItem(f"TOTALE"))
        self.table_ripartizionePreventivo.item(len(unita_immobiliari)+2, len(tabelle_millesimali)).setFont(bold_font)
        #self.table_ripartizionePreventivo.item(len(unita_immobiliari)+2, len(tabelle_millesimali)).setTextAlignment()

        j = 0
        totale_preventivo_attuale = {}

        for tabella in tabelle_millesimali:
            i = 2
            totale_millesimi_tabella = 0.0
            totale_preventivo_tabella = 0.0
            for unita in unita_immobiliari:
                if unita.tipoUnitaImmobiliare == "Appartamento":
                    proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                    self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di\n{proprietario.cognome} {proprietario.nome}"))
                else:
                    proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                    self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} di\n{proprietario.cognome} {proprietario.nome}"))

                self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali)).setData(Qt.ItemDataRole.UserRole, unita.codice)
                print("prima del richiamo")

                if unita.codice not in tabella.millesimi:
                    tabella.addMillesimo(unita, 0.00)
                    tabella = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella.codice)

                self.bilancio.calcolaQuotaPreventivo(unita, tabella)
                self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

                self.table_ripartizionePreventivo.setItem(i, j + 1 + len(tabelle_millesimali), QTableWidgetItem("%.2f" % self.bilancio.ripartizioneSpesePreventivate[tabella.codice][unita.codice]))
                totale_preventivo_tabella += self.bilancio.ripartizioneSpesePreventivate[tabella.codice][unita.codice]
                self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, j + 1 + len(tabelle_millesimali), QTableWidgetItem("%.2f" % totale_preventivo_tabella))

                totale_millesimi_tabella += tabella.millesimi[unita.codice]

                self.table_ripartizionePreventivo.setItem(i, j, QTableWidgetItem("%.2f" % tabella.millesimi[unita.codice]))

                if unita.codice in totale_preventivo_attuale:
                    totale_preventivo_attuale[unita.codice] += self.bilancio.ripartizioneSpesePreventivate[tabella.codice][unita.codice]
                else:
                    totale_preventivo_attuale[unita.codice] = self.bilancio.ripartizioneSpesePreventivate[tabella.codice][unita.codice]
                i += 1
            self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, j, QTableWidgetItem("%.2f" % totale_millesimi_tabella))

            j += 1

        self.bilancio.calcolaImportiDaVersare(totale_preventivo_attuale)
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

        for i in range(2, len(unita_immobiliari) + 2):
            cod_unita = self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali)).data(Qt.ItemDataRole.UserRole)
            self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali) * 2 + 1, QTableWidgetItem("%.2f" % totale_preventivo_attuale[cod_unita]))
            self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali) * 2 + 2, QTableWidgetItem("%.2f" % self.bilancio.ripartizioneConguaglio[cod_unita]))
            self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali) * 2 + 3, QTableWidgetItem("%.2f" % self.bilancio.importiDaVersare[cod_unita]))

        self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 1, QTableWidgetItem("%.2f" % sum(list(totale_preventivo_attuale.values()))))
        self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 2, QTableWidgetItem("%.2f" % sum(list(self.bilancio.ripartizioneConguaglio.values()))))
        self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 3, QTableWidgetItem("%.2f" % sum(list(self.bilancio.importiDaVersare.values()))))

        self.table_ripartizionePreventivo.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_ripartizionePreventivo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_ripartizionePreventivo.horizontalHeader().setSectionResizeMode(len(tabelle_millesimali), QHeaderView.ResizeMode.Stretch)
        self.table_ripartizionePreventivo.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_ripartizionePreventivo.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table_ripartizionePreventivo.verticalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_ripartizionePreventivo.verticalHeader().setSectionResizeMode(len(unita_immobiliari) + 2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_ripartizionePreventivo.horizontalHeader().setVisible(False)
        self.table_ripartizionePreventivo.verticalHeader().setVisible(False)
        self.table_ripartizionePreventivo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.table_ripartizionePreventivo.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not list(Bilancio.getAllBilanciByImmobile(self.immobile).values()):
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()