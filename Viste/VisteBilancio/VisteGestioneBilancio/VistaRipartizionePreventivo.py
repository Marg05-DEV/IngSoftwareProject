import datetime
import re

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QSizePolicy, QLineEdit, QHBoxLayout, QDateEdit, QAbstractSpinBox

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaRipartizionePreventivo(QWidget):
    def __init__(self, bilancio, callback):
        super(VistaRipartizionePreventivo, self).__init__()
        self.bilancio = bilancio
        self.callback = callback
        self.immobile = Immobile.ricercaImmobileById(self.bilancio.immobile)
        self.input_lines = {}
        self.input_errors = {}
        self.date_lines_rate = {}
        main_layout = QVBoxLayout()
        ricevuta_layout = QHBoxLayout()

        lbl_label = QLabel("Numero Rate")
        input_line = QLineEdit()

        input_line.setPlaceholderText("max 6")
        if self.bilancio.numeroRate != 0:
            input_line.setText(str(self.bilancio.numeroRate))
        input_line.setValidator(QIntValidator(0, 6))
        self.input_lines["numeroRate"] = input_line
        self.input_lines["numeroRate"].editingFinished.connect(self.update_numero_rate)
        ricevuta_layout.addWidget(lbl_label)
        ricevuta_layout.addWidget(input_line)

        self.table_ripartizionePreventivo = QTableWidget()
        self.table_ripartizionePreventivo.cellChanged.connect(self.editingRate)
        self.update_table()

        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)
        main_layout.addLayout(ricevuta_layout)
        main_layout.addWidget(self.table_ripartizionePreventivo)
        main_layout.addWidget(self.msg)

        self.setLayout(main_layout)
        self.resize(1500, 650)
        self.setWindowTitle("Ripartizione Preventivo")

    def update_numero_rate(self):
        numero_rate = int(self.input_lines["numeroRate"].text())
        if numero_rate != self.bilancio.numeroRate:
            self.bilancio.addNumeroRate(numero_rate)
            self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
            self.bilancio.initScadenzaRate()
            self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

            unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values())
            tabelle_millesimali = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values())
            for i in range(2, len(unita_immobiliari) + 2):
                cod_unita = self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali)).data(Qt.ItemDataRole.UserRole)
                self.bilancio.ripartizioneRate(cod_unita)
                self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
            self.update_table()

    def dataScadenzaChanged(self):
        print("fine cambiamento")

        for key, data in self.date_lines_rate.items():
            if data is self.sender():
                data_da_mettere = data.text().split("/")
                data_da_mettere = datetime.date(int(data_da_mettere[2]), int(data_da_mettere[1]), int(data_da_mettere[0]))
                self.bilancio.editDataScadenza(data_da_mettere, key)
                self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

    def update_table(self):
        print("a")
        self.table_ripartizionePreventivo.cellChanged.disconnect(self.editingRate)
        print("aa")
        # prendo le list necessarie
        unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values())
        tabelle_millesimali = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values())

        #setto row e colum della tabella
        self.table_ripartizionePreventivo.setRowCount(len(unita_immobiliari) + 3)
        self.table_ripartizionePreventivo.setColumnCount((len(tabelle_millesimali)) * 2 + 4 + self.bilancio.numeroRate)

        bold_font = QFont()
        bold_font.setBold(True)

        self.table_ripartizionePreventivo.horizontalHeader().setFont(bold_font)

        self.table_ripartizionePreventivo.setItem(0, 0, QTableWidgetItem("Tabelle Millesimali - Millesimi"))
        print("i")
        self.table_ripartizionePreventivo.setItem(0, len(tabelle_millesimali), QTableWidgetItem("Unita Immobilari"))
        print("i")
        self.table_ripartizionePreventivo.setItem(0, len(tabelle_millesimali) + 1, QTableWidgetItem("Tab. Millesimali - Quote"))
        self.table_ripartizionePreventivo.setItem(0, 2 * len(tabelle_millesimali) + 1, QTableWidgetItem(f"RIPARTIZIONE PREVENTIVO ESERCIZIO {datetime.date.strftime(self.bilancio.inizioEsercizio, '%d/%m/%Y')} - {datetime.date.strftime(self.bilancio.fineEsercizio, '%d/%m/%Y')}"))

        self.table_ripartizionePreventivo.item(0, 0).setFont(bold_font)
        self.table_ripartizionePreventivo.item(0, len(tabelle_millesimali)).setFont(bold_font)
        self.table_ripartizionePreventivo.item(0, len(tabelle_millesimali) + 1).setFont(bold_font)
        self.table_ripartizionePreventivo.item(0, 2 * len(tabelle_millesimali) + 1).setFont(bold_font)
        print(" ---- RIGA 100")
        self.table_ripartizionePreventivo.item(0, 0).setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table_ripartizionePreventivo.item(0, len(tabelle_millesimali)).setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table_ripartizionePreventivo.item(0, len(tabelle_millesimali) + 1).setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table_ripartizionePreventivo.item(0, 2 * len(tabelle_millesimali) + 1).setFlags(Qt.ItemFlag.ItemIsEnabled)
        print(" ---- RIGA 105")
        self.table_ripartizionePreventivo.setSpan(0, 0, 1, len(tabelle_millesimali))
        self.table_ripartizionePreventivo.setSpan(0, len(tabelle_millesimali) + 1, 1, len(tabelle_millesimali))
        self.table_ripartizionePreventivo.setSpan(0, 2 * len(tabelle_millesimali) + 1, 1, 3)

        j = 0
        for tabella in tabelle_millesimali:
            self.table_ripartizionePreventivo.setItem(1, j, QTableWidgetItem(f"{tabella.nome}"))
            self.table_ripartizionePreventivo.setItem(1, j + 1 + len(tabelle_millesimali), QTableWidgetItem(f"{tabella.nome}"))
            self.table_ripartizionePreventivo.item(1, j).setFont(bold_font)
            self.table_ripartizionePreventivo.item(1, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_ripartizionePreventivo.item(1, j + 1 + len(tabelle_millesimali)).setFont(bold_font)
            self.table_ripartizionePreventivo.item(1, j + 1 + len(tabelle_millesimali)).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_ripartizionePreventivo.item(1, j).setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table_ripartizionePreventivo.item(1, j + 1 + len(tabelle_millesimali)).setFlags(Qt.ItemFlag.ItemIsEnabled)
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

        if self.bilancio.numeroRate > 0:
            for k in range(0, self.bilancio.numeroRate):
                self.table_ripartizionePreventivo.setItem(0, len(tabelle_millesimali) * 2 + 3 + k + 1, QTableWidgetItem(f"Rata {k + 1}"))
                self.table_ripartizionePreventivo.item(0, len(tabelle_millesimali) * 2 + 3 + k + 1).setFont(bold_font)
                self.table_ripartizionePreventivo.item(0, len(tabelle_millesimali) * 2 + 3 + k + 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                widget = QWidget()
                layout = QVBoxLayout()
                label = QLabel("Data scadenza:")
                layout.addWidget(label, Qt.AlignmentFlag.AlignHCenter)
                data = QDateEdit(self.bilancio.scadenzaRate[k])
                data.editingFinished.connect(self.dataScadenzaChanged)
                self.date_lines_rate[k] = data
                layout.addWidget(data)
                data.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
                widget.setLayout(layout)
                self.table_ripartizionePreventivo.setCellWidget(1, len(tabelle_millesimali) * 2 + 3 + k + 1, widget)

        print(" ---- RIGA 160")
        self.table_ripartizionePreventivo.setItem(len(unita_immobiliari)+2, len(tabelle_millesimali), QTableWidgetItem(f"TOTALE"))
        self.table_ripartizionePreventivo.item(len(unita_immobiliari)+2, len(tabelle_millesimali)).setFont(bold_font)

        j = 0
        totale_preventivo_attuale = {}

        for tabella in tabelle_millesimali:
            i = 2
            totale_millesimi_tabella = 0.0
            totale_preventivo_tabella = 0.0
            print(" ---- RIGA 173")
            for unita in unita_immobiliari:
                if unita.condomini:
                    if unita.tipoUnitaImmobiliare == "Appartamento":
                        for condomini in unita.condomini.keys():
                            if unita.condomini[condomini] == "Proprietario":
                                proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                                self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di\n{proprietario.cognome} {proprietario.nome}"))
                                break
                            else:
                                self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di\nNessun Proprietario"))
                    else:
                        for condomini in unita.condomini.keys():
                            if unita.condomini[condomini] == "Proprietario":
                                proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                                self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} di\n{proprietario.cognome} {proprietario.nome}"))
                                break
                            else:
                                self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} di\nNessun Proprietario"))
                else:
                    self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} di\nNessun Proprietario"))
                self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali)).setData(Qt.ItemDataRole.UserRole, unita.codice)
                self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali)).setFlags(Qt.ItemFlag.ItemIsEnabled)
                print("prima del richiamo")

                if unita.codice not in tabella.millesimi:
                    tabella.addMillesimo(unita, 0.00)
                    tabella = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella.codice)

                self.bilancio.calcolaQuotaPreventivo(unita, tabella)
                self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

                self.table_ripartizionePreventivo.setItem(i, j + 1 + len(tabelle_millesimali), QTableWidgetItem("%.2f" % self.bilancio.ripartizioneSpesePreventivate[tabella.codice][unita.codice]))
                self.table_ripartizionePreventivo.item(i, j + 1 + len(tabelle_millesimali)).setFlags(Qt.ItemFlag.ItemIsEnabled)
                totale_preventivo_tabella += self.bilancio.ripartizioneSpesePreventivate[tabella.codice][unita.codice]
                self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, j + 1 + len(tabelle_millesimali), QTableWidgetItem("%.2f" % totale_preventivo_tabella))
                self.table_ripartizionePreventivo.item(len(unita_immobiliari) + 2, j + 1 + len(tabelle_millesimali)).setFlags(Qt.ItemFlag.ItemIsEnabled)

                totale_millesimi_tabella += tabella.millesimi[unita.codice]

                self.table_ripartizionePreventivo.setItem(i, j, QTableWidgetItem("%.2f" % tabella.millesimi[unita.codice]))
                self.table_ripartizionePreventivo.item(i, j).setFlags(Qt.ItemFlag.ItemIsEnabled)

                if unita.codice in totale_preventivo_attuale:
                    totale_preventivo_attuale[unita.codice] += self.bilancio.ripartizioneSpesePreventivate[tabella.codice][unita.codice]
                else:
                    totale_preventivo_attuale[unita.codice] = self.bilancio.ripartizioneSpesePreventivate[tabella.codice][unita.codice]
                i += 1
            self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, j, QTableWidgetItem("%.2f" % totale_millesimi_tabella))
            self.table_ripartizionePreventivo.item(len(unita_immobiliari) + 2, j).setFlags(Qt.ItemFlag.ItemIsEnabled)

            j += 1

        self.bilancio.calcolaImportiDaVersare(totale_preventivo_attuale)
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

        for i in range(2, len(unita_immobiliari) + 2):
            cod_unita = self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali)).data(Qt.ItemDataRole.UserRole)

            self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali) * 2 + 1, QTableWidgetItem("%.2f" % totale_preventivo_attuale[cod_unita]))
            self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali) * 2 + 2, QTableWidgetItem("%.2f" % self.bilancio.ripartizioneConguaglio[cod_unita]))
            self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali) * 2 + 3, QTableWidgetItem("%.2f" % self.bilancio.importiDaVersare[cod_unita]))

            self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali) * 2 + 1).setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali) * 2 + 2).setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali) * 2 + 3).setFlags(Qt.ItemFlag.ItemIsEnabled)

            #QUI NO
            for r in range(0, self.bilancio.numeroRate):
                self.table_ripartizionePreventivo.setItem(i, len(tabelle_millesimali) * 2 + 4 + r, QTableWidgetItem("%.2f" % self.bilancio.ratePreventivate[cod_unita][r]))
                self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali) * 2 + 4 + r).setData(Qt.ItemDataRole.UserRole, [cod_unita, r])
                if r == (self.bilancio.numeroRate - 1):
                    self.table_ripartizionePreventivo.item(i, len(tabelle_millesimali) * 2 + 4 + r).setFlags(Qt.ItemFlag.ItemIsEnabled)

        self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 1, QTableWidgetItem("%.2f" % sum(list(totale_preventivo_attuale.values()))))
        self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 2, QTableWidgetItem("%.2f" % sum(list(self.bilancio.ripartizioneConguaglio.values()))))
        self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 3, QTableWidgetItem("%.2f" % sum(list(self.bilancio.importiDaVersare.values()))))

        self.table_ripartizionePreventivo.item(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 1).setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table_ripartizionePreventivo.item(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 2).setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table_ripartizionePreventivo.item(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 3).setFlags(Qt.ItemFlag.ItemIsEnabled)

        for r in range(0, self.bilancio.numeroRate):
            somma = 0.0
            for chiave in self.bilancio.ratePreventivate.keys():
                somma += self.bilancio.ratePreventivate[chiave][r]

            self.table_ripartizionePreventivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 4 + r, QTableWidgetItem("%.2f" % somma))
            self.table_ripartizionePreventivo.item(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 4 + r).setFlags(Qt.ItemFlag.ItemIsEnabled)

        self.table_ripartizionePreventivo.cellChanged.connect(self.editingRate)
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

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not list(Bilancio.getAllBilanciByImmobile(self.immobile).values()):
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()

    def closeEvent(self, event):
        self.callback()
