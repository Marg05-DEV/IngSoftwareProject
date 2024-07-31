import re

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLabel, QTableWidgetItem, QSizePolicy, QHeaderView

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tabellaMillesimale import TabellaMillesimale
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.immobile import Immobile


class VistaCalcoloConsuntivo(QWidget):
    def __init__(self, immobile, bilancio):
        super(VistaCalcoloConsuntivo, self).__init__()
        #self.immobile = Immobile.ricercaImmobileById(bilancio.immobile)
        print("dentro calcolo consuntivo")
        self.immobile = immobile
        self.bilancio = bilancio
        print(self.bilancio.listaSpeseAConsuntivo)

        for spese_consuntivo in self.bilancio.listaSpeseAConsuntivo:
            spesa = Spesa.ricercaSpesaByCodice(spese_consuntivo)
            print("dettaglio spesa: ", spesa.getInfoSpesa())
            for tabelle in TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values():
                print("dettaglio tabella: ", tabelle.getInfoTabellaMillesimale())
                if spesa.tipoSpesa in tabelle.tipologieSpesa:
                    print("codice tabella: ", tabelle.codice, "codice tipo spesa: ", spesa.tipoSpesa, "importo: ", str("%.2f" % spesa.importo) )
                    self.bilancio.addImportoConsuntivato(tabelle.codice, spesa.tipoSpesa, spesa.importo)

        main_layout = QVBoxLayout()

        self.table_calcolo_consuntivo = QTableWidget()
        #self.table_calcolo_consuntivo.cellChanged.connect(self.saveMatrix)

        main_layout.addWidget(self.table_calcolo_consuntivo)

        self.update_table()

        self.msg = QLabel("Messaggio")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.hide_message)

        main_layout.addWidget(self.msg)

        self.setLayout(main_layout)
        self.resize(1200, 650)
        self.setWindowTitle("Calcolo Consuntivo")

    def update_table(self):
        #self.table_proposta_preventivo.cellChanged.disconnect(self.saveMatrix)

        #self.bilancio = Bilancio.ricercaBilancioByCodice(self.bilancio.codice)

        tabelle_immobile = list(TabellaMillesimale.getAllTabelleMillesimaliByImmobile(self.immobile).values())
        used_tipi_spesa = []

        for tabella in tabelle_immobile:
            used_tipi_spesa.extend(tabella.tipologieSpesa)

        self.table_calcolo_consuntivo.setRowCount(len(tabelle_immobile) + len(used_tipi_spesa) + 1)
        self.table_calcolo_consuntivo.setColumnCount(2)
        bold_font = QFont()
        bold_font.setBold(True)

        self.table_calcolo_consuntivo.setHorizontalHeaderLabels(["DESCRIZIONE TIPOLOGIA DI SPESA", "IMPORTO EFFETTIVO"])
        """
        self.table_proposta_preventivo.setHorizontalHeaderItem(0, QTableWidgetItem("DESCRIZIONE TIPOLOGIA DI SPESA"))
        self.table_proposta_preventivo.setHorizontalHeaderItem(1, QTableWidgetItem("IMPORTO PREVENTIVATO"))
        """
        self.table_calcolo_consuntivo.horizontalHeader().setFont(bold_font)

        row = 0
        calcolo_consuntivo = 0.0

        for tabella in tabelle_immobile:
            totale_tabella_millesimale = 0.0
            self.table_calcolo_consuntivo.setItem(row, 0, QTableWidgetItem(f"{tabella.nome} - {tabella.descrizione}"))
            row_tabella_millesimale = row
            row += 1
            for cod_tipo_spesa in tabella.tipologieSpesa:
                tipo_spesa = TipoSpesa.ricercaTipoSpesaByCodice(cod_tipo_spesa)
                self.table_calcolo_consuntivo.setItem(row, 0, QTableWidgetItem(f"{tipo_spesa.nome} - {tipo_spesa.descrizione}"))
                self.table_calcolo_consuntivo.setItem(row, 1, QTableWidgetItem("%.2f" % self.bilancio.speseConsuntivate[tabella.codice][cod_tipo_spesa]))

                self.table_calcolo_consuntivo.item(row, 0).setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table_calcolo_consuntivo.item(row, 1).setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)

                self.table_calcolo_consuntivo.item(row, 1).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignRight)
                self.table_calcolo_consuntivo.item(row, 1).setData(Qt.ItemDataRole.UserRole, [tabella.codice, cod_tipo_spesa])
                totale_tabella_millesimale += self.bilancio.speseConsuntivate[tabella.codice][cod_tipo_spesa]
                row += 1

            calcolo_consuntivo += totale_tabella_millesimale
            self.table_calcolo_consuntivo.setItem(row_tabella_millesimale, 1, QTableWidgetItem("%.2f" % totale_tabella_millesimale))
            self.table_calcolo_consuntivo.item(row_tabella_millesimale, 0).setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table_calcolo_consuntivo.item(row_tabella_millesimale, 1).setFlags(Qt.ItemFlag.ItemIsEnabled)

            self.table_calcolo_consuntivo.item(row_tabella_millesimale, 0).setFont(bold_font)
            self.table_calcolo_consuntivo.item(row_tabella_millesimale, 1).setFont(bold_font)

            self.table_calcolo_consuntivo.item(row_tabella_millesimale, 0).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.table_calcolo_consuntivo.item(row_tabella_millesimale, 1).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignRight)

        self.table_calcolo_consuntivo.setItem(len(tabelle_immobile) + len(used_tipi_spesa), 0, QTableWidgetItem("TOTALE"))
        self.table_calcolo_consuntivo.setItem(len(tabelle_immobile) + len(used_tipi_spesa), 1, QTableWidgetItem("%.2f" % calcolo_consuntivo))

        self.table_calcolo_consuntivo.item(len(tabelle_immobile) + len(used_tipi_spesa), 0).setFont(bold_font)
        self.table_calcolo_consuntivo.item(len(tabelle_immobile) + len(used_tipi_spesa), 1).setFont(bold_font)

        self.table_calcolo_consuntivo.item(len(tabelle_immobile) + len(used_tipi_spesa), 0).setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table_calcolo_consuntivo.item(len(tabelle_immobile) + len(used_tipi_spesa), 1).setFlags(Qt.ItemFlag.ItemIsEnabled)

        self.table_calcolo_consuntivo.item(len(tabelle_immobile) + len(used_tipi_spesa), 1).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignRight)

        self.table_calcolo_consuntivo.verticalHeader().setVisible(False)
        self.table_calcolo_consuntivo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table_calcolo_consuntivo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        #self.table_calcolo_consuntivo.cellChanged.connect(self.saveMatrix)

    """def saveMatrix(self, row, column):
        print("edit effettuato", row, column)
        match = re.fullmatch("[0-9]*|[0-9]*[.,][0-9]{0,2}", self.table_proposta_preventivo.item(row, column).text())
        print("matcha?", match)
        coordinate = self.table_proposta_preventivo.item(row, column).data(Qt.ItemDataRole.UserRole)
        if coordinate is not None:
            if match is not None:
                print(match, coordinate)
                importo = float(self.table_proposta_preventivo.item(row, column).text().replace(",", "."))
                self.bilancio.addImportoPreventivato(coordinate[0], coordinate[1], importo)
            else:
                self.msg.setText("Il valore inserito nella cella non è valido")
                self.msg.show()
                self.timer.start()
            self.update_table()"""

    def hide_message(self):
        self.msg.hide()
        self.timer.stop()