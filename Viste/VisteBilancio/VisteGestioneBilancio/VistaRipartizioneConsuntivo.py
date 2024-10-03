import datetime

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QSizePolicy

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaRipartizioneConsuntivo(QWidget):
    def __init__(self, bilancio, callback):
        super(VistaRipartizioneConsuntivo, self).__init__()
        self.bilancio = bilancio
        self.callback = callback
        self.immobile = Immobile.ricercaImmobileById(self.bilancio.immobile)
        self.input_lines = {}
        self.input_errors = {}
        main_layout = QVBoxLayout()

        self.table_ripartizioneConsuntivo = QTableWidget()
        self.update_table()

        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addWidget(self.table_ripartizioneConsuntivo)
        main_layout.addWidget(self.msg)

        self.setLayout(main_layout)
        self.resize(1200, 650)
        self.setWindowTitle("Ripartizione Consuntivo")
    def update_table(self):
        unita_immobiliari = list(UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(self.immobile).values())
        tabelle_millesimali = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values())

        self.table_ripartizioneConsuntivo.setRowCount(len(unita_immobiliari) + 3)
        self.table_ripartizioneConsuntivo.setColumnCount((len(tabelle_millesimali))*2 + 5)

        bold_font = QFont()
        bold_font.setBold(True)

        self.table_ripartizioneConsuntivo.horizontalHeader().setFont(bold_font)

        self.table_ripartizioneConsuntivo.setItem(0, 0, QTableWidgetItem("Tabelle Millesimali - Millesimi"))
        self.table_ripartizioneConsuntivo.setItem(0, len(tabelle_millesimali), QTableWidgetItem("Unita Immobilari"))
        self.table_ripartizioneConsuntivo.setItem(0, len(tabelle_millesimali) + 1, QTableWidgetItem("Tab. Millesimali - Quote"))
        self.table_ripartizioneConsuntivo.setItem(0, 2 * len(tabelle_millesimali) + 1, QTableWidgetItem(f"RIPARTIZIONE CONSUNTIVO ESERCIZIO {datetime.date.strftime(self.bilancio.inizioEsercizio, '%d/%m/%Y')} - {datetime.date.strftime(self.bilancio.fineEsercizio, '%d/%m/%Y')}"))

        self.table_ripartizioneConsuntivo.item(0, 0).setFont(bold_font)
        self.table_ripartizioneConsuntivo.item(0, len(tabelle_millesimali)).setFont(bold_font)
        self.table_ripartizioneConsuntivo.item(0, len(tabelle_millesimali) + 1).setFont(bold_font)
        self.table_ripartizioneConsuntivo.item(0, 2 * len(tabelle_millesimali) + 1).setFont(bold_font)

        self.table_ripartizioneConsuntivo.setSpan(0, 0, 1, len(tabelle_millesimali))
        self.table_ripartizioneConsuntivo.setSpan(0, len(tabelle_millesimali) + 1, 1, len(tabelle_millesimali))
        self.table_ripartizioneConsuntivo.setSpan(0, 2 * len(tabelle_millesimali) + 1, 1, 4)

        j = 0
        for tabella in tabelle_millesimali:
            self.table_ripartizioneConsuntivo.setItem(1, j, QTableWidgetItem(f"{tabella.nome}\n{tabella.descrizione}"))
            self.table_ripartizioneConsuntivo.setItem(1, j + 1 + len(tabelle_millesimali), QTableWidgetItem(f"{tabella.nome}\nQuote"))
            self.table_ripartizioneConsuntivo.item(1, j).setFont(bold_font)
            self.table_ripartizioneConsuntivo.item(1, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_ripartizioneConsuntivo.item(1, j + 1 + len(tabelle_millesimali)).setFont(bold_font)
            self.table_ripartizioneConsuntivo.item(1, j + 1 + len(tabelle_millesimali)).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            j += 1

        self.table_ripartizioneConsuntivo.setItem(1, len(tabelle_millesimali), QTableWidgetItem(f"Unità Immobiliari\nCondomino Proprietario"))
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)).setFont(bold_font)
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_ripartizioneConsuntivo.setItem(1, len(tabelle_millesimali)*2 + 1, QTableWidgetItem(f"Totale Consuntivo\nAnno Attuale"))
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)*2 + 1).setFont(bold_font)
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)*2 + 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_ripartizioneConsuntivo.setItem(1, len(tabelle_millesimali)*2 + 2, QTableWidgetItem(f"Conguaglio\nAnno Precedente"))
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)*2 + 2).setFont(bold_font)
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)*2 + 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_ripartizioneConsuntivo.setItem(1, len(tabelle_millesimali)*2 + 3, QTableWidgetItem(f"Totale Versato"))
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)*2 + 3).setFont(bold_font)
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)*2 + 3).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_ripartizioneConsuntivo.setItem(1, len(tabelle_millesimali)*2 + 4, QTableWidgetItem(f"Conguaglio\nAnno Attuale"))
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)*2 + 4).setFont(bold_font)
        self.table_ripartizioneConsuntivo.item(1, len(tabelle_millesimali)*2 + 4).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_ripartizioneConsuntivo.setItem(len(unita_immobiliari)+2, len(tabelle_millesimali), QTableWidgetItem(f"TOTALE"))
        self.table_ripartizioneConsuntivo.item(len(unita_immobiliari)+2, len(tabelle_millesimali)).setFont(bold_font)

        j = 0
        totale_consuntivo_attuale = {}

        for tabella in tabelle_millesimali:
            i = 2
            totale_millesimi_tabella = 0.0
            totale_consuntivo_tabella = 0.0
            for unita in unita_immobiliari:
                if unita.condomini:
                    if unita.tipoUnitaImmobiliare == "Appartamento":
                        for condomini in unita.condomini.keys():
                            if unita.condomini[condomini] == "Proprietario":
                                proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                                self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di\n{proprietario.cognome} {proprietario.nome}"))
                                break
                            else:
                                self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno} di\nNessun Proprietario"))
                    else:
                        for condomini in unita.condomini.keys():
                            if unita.condomini[condomini] == "Proprietario":
                                proprietario = Condomino.ricercaCondominoByCF([item for item in unita.condomini.keys() if unita.condomini[item] == "Proprietario"][0])
                                self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} di\n{proprietario.cognome} {proprietario.nome}"))
                                break
                            else:
                                self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(f"{unita.tipoUnitaImmobiliare} di\nNessun Proprietario"))
                else:
                    self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali), QTableWidgetItem(
                        f"{unita.tipoUnitaImmobiliare} di\nNessun Proprietario"))
                self.table_ripartizioneConsuntivo.item(i, len(tabelle_millesimali)).setData(Qt.ItemDataRole.UserRole, unita.codice)

                if unita.codice not in tabella.millesimi:
                    tabella.addMillesimo(unita, 0.00)
                    tabella = TabellaMillesimale.ricercaTabelleMillesimaliByCodice(tabella.codice)

                self.bilancio.calcolaQuotaConsuntivo(unita, tabella)
                self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
                self.table_ripartizioneConsuntivo.setItem(i, j + 1 + len(tabelle_millesimali), QTableWidgetItem("%.2f" % self.bilancio.ripartizioneSpeseConsuntivate[tabella.codice][unita.codice]))
                totale_consuntivo_tabella += self.bilancio.ripartizioneSpeseConsuntivate[tabella.codice][unita.codice]
                self.table_ripartizioneConsuntivo.setItem(len(unita_immobiliari)+2, j + 1 + len(tabelle_millesimali), QTableWidgetItem("%.2f" % totale_consuntivo_tabella))
                totale_millesimi_tabella += tabella.millesimi[unita.codice]

                self.table_ripartizioneConsuntivo.setItem(i, j, QTableWidgetItem("%.2f" % tabella.millesimi[unita.codice]))
                if unita.codice in totale_consuntivo_attuale:
                    totale_consuntivo_attuale[unita.codice] += self.bilancio.ripartizioneSpeseConsuntivate[tabella.codice][unita.codice]
                else:
                    totale_consuntivo_attuale[unita.codice] = self.bilancio.ripartizioneSpeseConsuntivate[tabella.codice][unita.codice]
                i += 1
            self.table_ripartizioneConsuntivo.setItem(len(unita_immobiliari) + 2, j, QTableWidgetItem("%.2f" % totale_millesimi_tabella))

            j += 1
        self.bilancio.getConguaglioPrecedente()

        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        self.bilancio.calcolaRateVersate()
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)
        self.bilancio.calcolaConguaglio(totale_consuntivo_attuale)
        self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

        for i in range(2, len(unita_immobiliari)+2):
            cod_unita = self.table_ripartizioneConsuntivo.item(i, len(tabelle_millesimali)).data(Qt.ItemDataRole.UserRole)
            self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali) * 2 + 1, QTableWidgetItem("%.2f" % totale_consuntivo_attuale[cod_unita]))
            self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali)*2 + 2, QTableWidgetItem("%.2f" % self.bilancio.conguaglioPrecedente[cod_unita]))
            self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali)*2 + 3, QTableWidgetItem("%.2f" % self.bilancio.rateVersate[cod_unita]))
            self.table_ripartizioneConsuntivo.setItem(i, len(tabelle_millesimali)*2 + 4, QTableWidgetItem("%.2f" % self.bilancio.ripartizioneConguaglio[cod_unita]))

        self.table_ripartizioneConsuntivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 1, QTableWidgetItem("%.2f" % sum(list(totale_consuntivo_attuale.values()))))
        self.table_ripartizioneConsuntivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 2, QTableWidgetItem("%.2f" % sum(list(self.bilancio.conguaglioPrecedente.values()))))
        self.table_ripartizioneConsuntivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 3, QTableWidgetItem("%.2f" % sum(list(self.bilancio.rateVersate.values()))))
        self.table_ripartizioneConsuntivo.setItem(len(unita_immobiliari) + 2, len(tabelle_millesimali) * 2 + 4, QTableWidgetItem("%.2f" % sum(list(self.bilancio.ripartizioneConguaglio.values()))))

        self.table_ripartizioneConsuntivo.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_ripartizioneConsuntivo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_ripartizioneConsuntivo.horizontalHeader().setSectionResizeMode(len(tabelle_millesimali), QHeaderView.ResizeMode.Stretch)
        self.table_ripartizioneConsuntivo.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_ripartizioneConsuntivo.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table_ripartizioneConsuntivo.verticalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_ripartizioneConsuntivo.verticalHeader().setSectionResizeMode(len(unita_immobiliari) + 2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_ripartizioneConsuntivo.horizontalHeader().setVisible(False)
        self.table_ripartizioneConsuntivo.verticalHeader().setVisible(False)
        self.table_ripartizioneConsuntivo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.table_ripartizioneConsuntivo.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()
        if not list(Bilancio.getAllBilanciByImmobile(self.immobile).values()):
            self.msg.setText("Non ci sono bilanci definiti")
            self.msg.show()

    def closeEvent(self, event):
        self.callback()