from PyQt6.QtCore import Qt, QAbstractProxyModel, QModelIndex
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QCompleter, QLabel, QHBoxLayout, QPushButton, QFrame,
                             QTreeWidget, QTreeWidgetItem, QHeaderView, QTableView, QTableWidget, QTableWidgetItem)

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.rata import Rata
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaCreditoCondomino(QWidget):
    def __init__(self):

        super(VistaCreditoCondomino, self).__init__()
        self.condomino = None
        self.buttons = {}
        self.condomino_section = {}
        self.immobile = None
        self.credito_totale = 0.0
        self.lines = []
        main_layout = QVBoxLayout()

        self.completer_table = QTableWidget()
        self.condomini_completer = QCompleter()
        popup_type = QTableView()
        self.condomini_completer.setPopup(popup_type)
        popup_type.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        popup_type.horizontalHeader().hide()
        popup_type.verticalHeader().hide()

        condomini_table = [[(item.cognome + " " + item.nome), item.codiceFiscale] for item in Condomino.getAllCondomini().values()]

        self.condomini_completer.setCompletionColumn(0)
        self.completer_table.setRowCount(len(condomini_table))
        self.completer_table.setColumnCount(2)

        i = 0
        for data in condomini_table:
            j = 0
            for value in data:
                self.completer_table.setItem(i, j, QTableWidgetItem(str(value)))
                self.completer_table.item(i, j).setData(Qt.ItemDataRole.UserRole, data)
                j += 1
            i += 1

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Condomino")

        self.lbl_search = QLabel("Ricerca condomino da selezionare:")

        self.condomini_completer.setModel(self.completer_table.model())
        self.searchbar.setCompleter(self.condomini_completer)
        self.condomini_completer.activated[QModelIndex].connect(self.selectioning_by_completer)
        self.condomini_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.lbl_frase_condomino = QLabel("Il condomino non ha nessuna unità immobiliare assegnata")
        self.lbl_frase_condomino.setStyleSheet("font-weight: bold;")
        self.condomino_section["frase"] = self.lbl_frase_condomino
        self.condomino_section["frase"].setVisible(False)
        search_layout = QVBoxLayout()

        self.lbl_search.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        search_layout.addWidget(self.lbl_search)
        search_layout.addWidget(self.searchbar)

        search_layout.addWidget(self.lbl_frase_condomino)
        main_layout.addLayout(search_layout)
        msg_layout = QHBoxLayout()
        frase_lbl = QLabel("Stai selezionando: ")
        self.condomino_selezionato = QLabel("Nessun Condomino selezionato")

        msg_layout.addWidget(frase_lbl)
        msg_layout.addWidget(self.condomino_selezionato)

        if not condomini_table:
            frase_lbl.setText("Nessun Condomino presente")
            self.condomino_selezionato.setVisible(False)

        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.create_button("Seleziona", self.view_credito_condomino))
        self.buttons["Seleziona"].setDisabled(True)
        self.searchbar.textChanged.connect(self.selectioning)
        main_layout.addLayout(msg_layout)
        main_layout.addLayout(self.button_layout)

        self.lines.append(self.drawLine())
        self.lines[0].setVisible(False)
        main_layout.addWidget(self.lines[0])

        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(["Denominazione Immobile", "Importo a Credito"])
        self.tree_widget.setVisible(False)

        self.credito_condomino_section = {}
        self.rate_a_credito_non_presenti = QLabel("")
        self.rate_a_credito_non_presenti.setStyleSheet("font-weight: bold;")
        self.credito_condomino_section["no_credito"] = self.rate_a_credito_non_presenti
        self.credito_condomino_section["no_credito"].setVisible(False)

        self.totale_credito_condomino = QLabel("")
        self.totale_credito_condomino.setStyleSheet("font-weight: bold;")
        self.credito_condomino_section["credito_totale"] = self.totale_credito_condomino
        self.credito_condomino_section["credito_totale"].setVisible(False)

        self.lbl_totale_credito_condomino = QLabel("Totale credito del condomino:")
        self.lbl_totale_credito_condomino.setStyleSheet("font-weight: bold;")
        self.credito_condomino_section["frase_credito_totale"] = self.lbl_totale_credito_condomino
        self.credito_condomino_section["frase_credito_totale"].setVisible(False)
        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        totale_credito_layout = QHBoxLayout()
        main_layout.addWidget(self.tree_widget)
        main_layout.addWidget(self.rate_a_credito_non_presenti)
        totale_credito_layout.addWidget(self.lbl_totale_credito_condomino)
        totale_credito_layout.addWidget(self.totale_credito_condomino)
        main_layout.addLayout(totale_credito_layout)
        main_layout.addWidget(self.msg)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Credito Condomino")

    def drawLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setFixedSize(275, 55)
        button.setCheckable(False)
        button.clicked.connect(action)
        self.buttons[testo] = button
        return button

    def selectioning_by_completer(self, index):
        record = self.condomini_completer.model().data(self.condomini_completer.completionModel().mapToSource(index), Qt.ItemDataRole.UserRole)
        if record is not None:
            self.condomino = Condomino.ricercaCondominoByCF(record[1])
        if self.condomino is not None:
            self.condomino_selezionato.setText(f"{self.condomino.cognome} {self.condomino.nome} - {self.condomino.codiceFiscale}")
            self.buttons["Seleziona"].setDisabled(False)
        else:
            self.condomino_selezionato.setText("Nessun condomino selezionato")
            self.buttons["Seleziona"].setDisabled(True)

    def selectioning(self):
        record = self.condomini_completer.model().data(self.condomini_completer.completionModel().mapToSource(self.condomini_completer.currentIndex()), Qt.ItemDataRole.UserRole)
        if record is not None:
            if record[0] == self.searchbar.text():
                self.condomino = Condomino.ricercaCondominoByCF(record[1])

        if self.condomino is not None:
            self.condomino_selezionato.setText(f"{self.condomino.cognome} {self.condomino.nome} - {self.condomino.codiceFiscale}")
            self.buttons["Seleziona"].setDisabled(False)
        else:
            self.condomino_selezionato.setText("Nessun condomino selezionato")
            self.buttons["Seleziona"].setDisabled(True)

    def view_credito_condomino(self):
        if self.condomino is not None:
            self.tree_widget.setVisible(True)
            for line in self.lines:
                line.setVisible(True)
            self.update_list()
        else:
            return None

    def update_list(self):
        unita_associate_al_condomino = UnitaImmobiliare.getAllUnitaImmobiliariByCondomino(self.condomino)
        immobile_con_credito = self.condomino.getImmobiliAssociati()

        # {immobile: {unita: valore, unita: valore}, immobile:
        if not unita_associate_al_condomino:
            self.tree_widget.setVisible(False)
            self.condomino_section["frase"].setVisible(True)
            self.credito_condomino_section["frase_credito_totale"].setVisible(False)
            self.credito_condomino_section["credito_totale"].setVisible(False)

        print(immobile_con_credito, unita_associate_al_condomino)

        crediti_condomino = {}
        for immobile in immobile_con_credito:
            crediti_condomino[immobile.id] = {}
            for unita in unita_associate_al_condomino:
                if UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(unita).immobile == immobile.id:
                    crediti_condomino[immobile.id][unita] = 0.0

        self.tree_widget.clear()
        for immobile in immobile_con_credito:
            last_bilancio = Bilancio.getLastBilancio(immobile)
            for cod_unita in crediti_condomino[immobile.id].keys():
                unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(cod_unita)
                totale_rate_versate_per_unita = 0.0
                if last_bilancio:
                    for rate_versate in Rata.getAllRateByUnitaImmobiliare(unita).values():
                        if rate_versate.dataPagamento >= last_bilancio.dataApprovazione:
                            totale_rate_versate_per_unita += rate_versate.importo

                    crediti_condomino[immobile.id][cod_unita] = last_bilancio.importiDaVersare[cod_unita] - totale_rate_versate_per_unita

            if last_bilancio:
                item = QTreeWidgetItem([immobile.denominazione, str("%.2f" % sum(crediti_condomino[immobile.id].values()))])
            else:
                item = QTreeWidgetItem([immobile.denominazione, "Nessun bilancio approvato per questo immobile"])

            for key, value in crediti_condomino[immobile.id].items():
                unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(key)
                if unita.tipoUnitaImmobiliare == "Appartamento":
                    unita_immobiliare = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno}"
                else:
                    unita_immobiliare = f"{unita.tipoUnitaImmobiliare}"

                if last_bilancio:
                    child = QTreeWidgetItem([unita_immobiliare, str("%.2f" % value)])
                else:
                    child = QTreeWidgetItem([unita_immobiliare, "Nessun bilancio approvato per questo immobile"])
                item.addChild(child)
            self.tree_widget.addTopLevelItem(item)


        self.tree_widget.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        print(crediti_condomino)
        if immobile_con_credito:
            self.tree_widget.setVisible(True)
            self.condomino_section["frase"].setVisible(False)
            self.credito_condomino_section["frase_credito_totale"].setVisible(True)
            self.credito_condomino_section["credito_totale"].setText("%.2f" % sum([sum(item.values()) for item in crediti_condomino.values()]))
            self.credito_condomino_section["credito_totale"].setVisible(True)
        else:
            self.tree_widget.setVisible(False)
            self.condomino_section["frase"].setVisible(True)
            self.credito_condomino_section["frase_credito_totale"].setVisible(False)
            self.credito_condomino_section["credito_totale"].setVisible(False)