from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame, QTreeWidget, QTreeWidgetItem

from Classes.Contabilita.bilancio import Bilancio
from Classes.Contabilita.fornitore import Fornitore
from Classes.Contabilita.rata import Rata
from Classes.Contabilita.spesa import Spesa
from Classes.Contabilita.tipoSpesa import TipoSpesa
from Classes.RegistroAnagrafe.condomino import Condomino
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare


class VistaCreditoCondomino(QWidget):
    def __init__(self):

        super(VistaCreditoCondomino, self).__init__()
        self.buttons = {}
        self.condomino_section = {}
        self.immobile = None
        main_layout = QVBoxLayout()

        completer_list = sorted([item.codiceFiscale for item in Condomino.getAllCondomini().values()])
        print(completer_list)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Ricerca Condomino")
        self.condomini_completer = QCompleter(completer_list)
        self.condomini_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        print(self.condomini_completer.completionModel())
        self.searchbar.setCompleter(self.condomini_completer)

        self.lbl_frase_condomino = QLabel("Il condomino non ha nessuna unità immobiliare asegnata")
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

        if not completer_list:
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
        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.drawLine()
        main_layout.addWidget(self.tree_widget)
        main_layout.addWidget(self.rate_a_credito_non_presenti)
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
        immobile_con_credito = []
        for cod_unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByCondomino(self.condomino):
            self.unita_associate_al_condomino.append(cod_unita_immobiliare)

        for immobile in Immobile.getAllImmobili().values():
            for cod_unita in self.unita_associate_al_condomino:
                unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(cod_unita)
                if immobile.id == unita.immobile:
                    if immobile.id not in immobile_con_credito:
                        immobile_con_credito.append(immobile)

        if not self.unita_associate_al_condomino:
            self.tree_widget.setVisible(False)
            self.condomino_section["frase"].setVisible(True)

        for immobile in immobile_con_credito:
            importo_totale_per_immobile = 0.00
            importo_per_unita = {}
            for unita_immobile in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(immobile).values():
                if unita_immobile.codice in self.unita_associate_al_condomino:
                    last_bilancio = Bilancio.getLastBilancio(immobile)
                    totale_rate_versate_per_unita = 0.0
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
                    print("ko")
            print("prima di item")
            item = QTreeWidgetItem([immobile.denominazione, str("%.2f" % importo_totale_per_immobile)])
            print("dopo item")
            for key, value in importo_per_unita.items():
                unita = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(key)
                if unita.tipoUnitaImmobiliare == "Appartamento":
                    unita_immobiliare = f"{unita.tipoUnitaImmobiliare} Scala {unita.scala} Int.{unita.interno}"
                else:
                    unita_immobiliare = f"{unita.tipoUnitaImmobiliare}"

                child = QTreeWidgetItem([unita_immobiliare], str("%.2f" % importo_per_unita))
                item.addChild(child)
            self.tree_widget.addTopLevelItem(item)

        for i in range(self.tree_widget.columnCount()):
            print(i)
            self.tree_widget.resizeColumnToContents(i)