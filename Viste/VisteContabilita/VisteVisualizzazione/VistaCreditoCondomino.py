from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QCompleter, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QListView, QFrame

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

        self.rate_section = {}

        rata_layout = QVBoxLayout()
        self.lbl_frase1 = QLabel("Rate:")
        self.lbl_frase1.setFixedSize(self.lbl_frase1.sizeHint())
        self.list_view_rate = QListView()
        self.list_view_rate.setAlternatingRowColors(True)
        self.error_no_rate = QLabel("")
        self.error_no_rate.setStyleSheet("font-weight: bold;")
        self.rate_section["frase"] = self.lbl_frase1
        self.rate_section["lista_rate"] = self.list_view_rate
        self.rate_section["no_rate"] = self.error_no_rate
        self.rate_section["no_rate"].setVisible(False)
        rata_layout.addWidget(self.lbl_frase1)
        rata_layout.addWidget(self.list_view_rate)
        rata_layout.addWidget(self.error_no_rate)

        totale_rate_layout = QHBoxLayout()
        lbl_frase_totale_rate = QLabel("Credito verso condomini dell'immobile")
        lbl_totale_rate = QLabel("0.00")

        self.rate_section["frase_totale"] = lbl_frase_totale_rate
        self.rate_section["totale"] = lbl_totale_rate
        totale_rate_layout.addWidget(lbl_frase_totale_rate)
        totale_rate_layout.addWidget(lbl_totale_rate)
        rata_layout.addLayout(totale_rate_layout)

        for widget in self.rate_section.values():
            widget.setVisible(False)

        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red; font-weight: bold;")
        self.msg.hide()

        self.drawLine()
        main_layout.addLayout(rata_layout)
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
            if UnitaImmobiliare.getAllUnitaImmobiliariByCondomino(self.condomino):
                list_immobile = []
                self.condomino_section["frase"].setVisible(False)
                for immobile in Immobile.getAllImmobili().values():
                    for cod_unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByCondomino(self.condomino):
                        unita_immobiliare = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(cod_unita_immobiliare)
                        if immobile.id == unita_immobiliare.immobile:
                            if immobile.id not in list_immobile:
                                list_immobile.append(immobile.id)
                                self.update_list(immobile)
            else:
                self.condomino_section["frase"].setVisible(True)
        else:
            print("no")
            return None

    def update_list(self, immobile_trovato):
        importo_totale = 0.00
        print(immobile_trovato.getInfoImmobile())
        print("inizio")
        ultimo_bilancio = Bilancio.getLastBilancio(immobile_trovato)
        if ultimo_bilancio != 0:
            self.rate_da_versare = ultimo_bilancio.importiDaVersare
            print("dope")
            self.rate_versate = {}
            for unita_immobiliare in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(immobile_trovato).values():
                if self.condomino.codiceFiscale in unita_immobiliare.condomini.keys() and unita_immobiliare.condomini[self.condomino.codiceFiscale] == "Proprietario":
                    totale_versato = 0.0
                    for rata in Rata.getAllRateByUnitaImmobiliare(unita_immobiliare).values():
                        if rata.dataPagamento >= Bilancio.getLastBilancio(immobile_trovato).dataApprovazione and rata.importo >= 0.0:
                            totale_versato += rata.importo
                    self.rate_versate[unita_immobiliare.codice] = totale_versato

            print("rata:", self.rate_da_versare)
            importi_tutti_nulli = False
            importi_da_non_rappresentare = []

            if self.rate_da_versare:
                for r in self.rate_da_versare.values():
                    if r <= 0:
                        importi_da_non_rappresentare.append(r)
                print("confronto", len(importi_da_non_rappresentare) == len(self.rate_da_versare.values()))
                if len(importi_da_non_rappresentare) == len(self.rate_da_versare.values()):
                    importi_tutti_nulli = True

            if not self.rate_da_versare or importi_tutti_nulli:
                print("yesyes")
                self.rate_section["lista_rate"].setVisible(False)
                self.rate_section["totale"].setVisible(False)
                self.rate_section["frase_totale"].setVisible(False)

                self.rate_section["no_rate"].setText("Non ci sono da versare per questo immobile")
                self.rate_section["no_rate"].setVisible(True)

            listview_model1 = QStandardItemModel(self.list_view_rate)
            for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(immobile_trovato).keys():
                unita_immo = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(unita)
                if self.condomino.codiceFiscale in unita_immo.condomini.keys() and unita_immo.condomini[self.condomino.codiceFiscale] == "Proprietario":
                    if self.rate_da_versare[unita] > 0:
                        if unita in self.rate_da_versare.keys():
                            item = QStandardItem()
                            importo = self.rate_da_versare[unita] - self.rate_versate[unita]
                            importo = str("%.2f" % importo)
                            if unita_immo.tipoUnitaImmobiliare == "Appartamento":
                                proprietario = Condomino.ricercaCondominoByCF([item for item in unita_immo.condomini.keys() if
                                                                               unita_immo.condomini[item] == "Proprietario"][0])
                                item_text = f"{unita_immo.tipoUnitaImmobiliare} Scala {unita_immo.scala} Int.{unita_immo.interno} di {proprietario.cognome} {proprietario.nome} --> {importo}"
                            else:
                                proprietario = Condomino.ricercaCondominoByCF([item for item in unita_immo.condomini.keys() if
                                                                               unita_immo.condomini[item] == "Proprietario"][0])
                                item_text = f"{unita_immo.tipoUnitaImmobiliare} di {proprietario.cognome} {proprietario.nome} --> {importo}"
                            item.setText(item_text)
                            item.setEditable(False)
                            font = item.font()
                            font.setPointSize(12)
                            item.setFont(font)
                            listview_model1.appendRow(item)

            importo_totale = 0.00
            print("qui finisce")
            self.list_view_rate.setModel(listview_model1)

            if self.rate_da_versare and not importi_tutti_nulli:
                print("nell'if")
                for unita in UnitaImmobiliare.getAllUnitaImmobiliariByImmobile(immobile_trovato).keys():
                    unita_immo = UnitaImmobiliare.ricercaUnitaImmobiliareByCodice(unita)
                    if self.condomino.codiceFiscale in unita_immo.condomini.keys() and unita_immo.condomini[self.condomino.codiceFiscale] == "Proprietario":
                        if self.rate_da_versare[unita] > 0:
                            if unita in self.rate_da_versare.keys():
                                importo_totale += self.rate_da_versare[unita]
                self.rate_section["totale"].setText(str("%.2f" % importo_totale))
                for rate in self.rate_section.values():
                    rate.setVisible(True)
                self.rate_section["no_rate"].setVisible(False)