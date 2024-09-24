from PyQt6.QtCore import Qt
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
        self.buttons = {}
        self.condomino_section = {}
        self.immobile = None
        self.credito_totale = 0.0
        main_layout = QVBoxLayout()

        self.completer_table = QTableWidget()
        self.condomini_completer = QCompleter()
        popup_type = QTableView()
        self.condomini_completer.setPopup(popup_type)
        popup_type.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        popup_type.horizontalHeader().hide()
        popup_type.verticalHeader().hide()

        condomini_table = [[(item.cognome + " " + item.nome), item.codiceFiscale] for item in Condomino.getAllCondomini().values()]
        print(condomini_table)

        self.condomini_completer.setCompletionColumn(0)
        self.completer_table.setRowCount(len(condomini_table))
        self.completer_table.setColumnCount(2)

        i = 0
        for data in condomini_table:
            j = 0
            print(data)
            for value in data:
                print(value)
                self.completer_table.setItem(i, j, QTableWidgetItem(str(value)))
                print(data)
                self.completer_table.item(i, j).setData(Qt.ItemDataRole.UserRole, data)
                j += 1
            i += 1

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Condomino")

        self.condomini_completer.setModel(self.completer_table.model())
        self.searchbar.setCompleter(self.condomini_completer)
        print("ciao")

        self.lbl_frase_condomino = QLabel("Il condomino non ha nessuna unità immobiliare assegnata")
        self.lbl_frase_condomino.setStyleSheet("font-weight: bold;")
        self.condomino_section["frase"] = self.lbl_frase_condomino
        self.condomino_section["frase"].setVisible(False)
        find_layout = QHBoxLayout()
        search_layout = QVBoxLayout()

        search_layout.addWidget(self.searchbar)

        search_layout.addWidget(self.lbl_frase_condomino)
        find_layout.addLayout(search_layout)
        main_layout.addLayout(find_layout)
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

        """ ------------------------- FINE SELEZIONE CONDOMINO ----------------------- """
        """ ------------------------------ SEZIONE RATE ---------------------------- """
        self.drawLine()
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
        self.drawLine()
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

    def selectioning(self):
        print("sel: ", self.condomini_completer.currentIndex(), self.condomini_completer.currentCompletion())
        print(self.condomini_completer.model().data(self.condomini_completer.currentIndex(), Qt.ItemDataRole.UserRole))
        condomino = None
        condomino = Condomino.ricercaCondominoByCF(self.searchbar.text())
        print("imm: ", condomino)

        if condomino != None:
            self.condomino_selezionato.setText(f"{condomino.nome} - {condomino.cognome} - {condomino.codiceFiscale}")
            self.buttons["Seleziona"].setDisabled(False)
        else:
            self.condomino_selezionato.setText("Nessun condomino selezionato")
            self.buttons["Seleziona"].setDisabled(True)

    def view_credito_condomino(self):
        search_text = self.searchbar.text()
        print(f"Testo della barra di ricerca: {search_text}")
        for b in Bilancio.getAllBilanci().values():
            print(b.getInfoBilancio())
        self.condomino = 0
        if search_text:
            self.condomino = Condomino.ricercaCondominoByCF(search_text)
            print("Condomino: ", self.condomino)
        if self.condomino != None:
            self.tree_widget.setVisible(True)
            self.update_list()
        else:
            print("no")
            return None

    def update_list(self):
        self.credito_totale_condomino = 0.00
        self.unita_associate_al_condomino = []
        immobile_con_credito = {}

        for cod_unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByCondomino(self.condomino):
            self.unita_associate_al_condomino.append(cod_unita_immobiliare)

        for immobile in Immobile.getAllImmobili().values():
            for cod_unita in self.unita_associate_al_condomino:
                unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(cod_unita)
                if immobile.id == unita.immobile:
                    if immobile.id not in immobile_con_credito:
                        immobile_con_credito[immobile.id] = immobile

        immobile_con_credito = list(immobile_con_credito.values())

        self.credito_totale = 0.00
        self.tree_widget.clear()
        for immobile in immobile_con_credito:
            print("we", immobile_con_credito)
            importo_totale_per_immobile = 0.00
            importo_per_unita = {}
            last_bilancio = Bilancio.getLastBilancio(immobile)
            for unita_immobile in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(immobile).values():
                if unita_immobile.codice in self.unita_associate_al_condomino:
                    totale_rate_versate_per_unita = 0.0
                    importo_per_unita[unita_immobile.codice] = 0.0
                    if last_bilancio:
                        for rate_versate in Rata.getAllRateByUnitaImmobiliare(unita_immobile).values():
                            totale_rate_versate_per_unita += rate_versate.importo
                        print("totale rate versate per unita", totale_rate_versate_per_unita)
                        if last_bilancio.importiDaVersare[unita_immobile.codice] < 0:
                            importo_per_unita[unita_immobile.codice] = last_bilancio.importiDaVersare[unita_immobile.codice] + totale_rate_versate_per_unita
                        else:
                            importo_per_unita[unita_immobile.codice] = last_bilancio.importiDaVersare[unita_immobile.codice] - totale_rate_versate_per_unita
                        print("importo da versare dell'unita", unita_immobile.codice, " :", last_bilancio.importiDaVersare[unita_immobile.codice])
                        print("importo per unita", importo_per_unita)
                        importo_totale_per_immobile += importo_per_unita[unita_immobile.codice]
                        self.credito_totale += importo_totale_per_immobile
            print("prima di item")
            if last_bilancio:
                item = QTreeWidgetItem([immobile.denominazione, str("%.2f" % importo_totale_per_immobile)])
            else:
                item = QTreeWidgetItem([immobile.denominazione, "Nessun bilancio approvato per questo immobile"])

            print("dopo item")
            for key, value in importo_per_unita.items():
                print("key", key)
                unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(key)
                print("f")
                if unita.tipoUnitaImmobiliare == "Appartamento":
                    unita_immobiliare = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno}"
                else:
                    unita_immobiliare = f"{unita.tipoUnitaImmobiliare}"
                print(unita_immobiliare, value)
                if last_bilancio:
                    child = QTreeWidgetItem([unita_immobiliare, str("%.2f" % value)])
                else:
                    child = QTreeWidgetItem([unita_immobiliare, "Nessun bilancio approvato per questo immobile"])
                item.addChild(child)
            self.tree_widget.addTopLevelItem(item)


        self.tree_widget.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        if immobile_con_credito:
            self.tree_widget.setVisible(True)
            self.condomino_section["frase"].setVisible(False)
            if last_bilancio:
                self.credito_condomino_section["frase_credito_totale"].setVisible(True)
                self.credito_condomino_section["credito_totale"].setText("%.2f" % self.credito_totale)
                self.credito_condomino_section["credito_totale"].setVisible(True)
            else:
                self.credito_condomino_section["frase_credito_totale"].setVisible(False)
                self.credito_condomino_section["credito_totale"].setVisible(False)
        else:
            self.tree_widget.setVisible(False)
            self.condomino_section["frase"].setVisible(True)
            self.credito_condomino_section["frase_credito_totale"].setVisible(False)
            self.credito_condomino_section["credito_totale"].setVisible(False)