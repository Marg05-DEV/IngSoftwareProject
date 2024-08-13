from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy

from Viste.VisteContabilita.VistaGestioneContabilita import VistaGestioneContabilita
from Viste.VisteBilancio.VistaMenuGestioneBilancio import VistaMenuGestioneBilancio
from Viste.VisteDocumenti.VistaGestioneDocumenti import VistaGestioneDocumenti
from Viste.VisteImmobile.VistaGestioneImmobile import VistaGestioneImmobile
from Viste.VisteRegistroAnagrafe.VistaMenuRegistroAnagrafe import VistaMenuRegistroAnagrafe


class VistaHome(QWidget):
    def __init__(self, parent=None):
        super(VistaHome, self).__init__(parent)

        self.setWindowTitle("Amministrazione Condominiale")
        vertical_layout = QVBoxLayout()

        vertical_layout.addWidget(self.getButton("GESTIONE IMMOBILE",
                                                 "Aggiungi nuovi immobili. Visualizza, modifica o rimuovi quelli esistenti.",
                                                 self.goImmobile))
        vertical_layout.addWidget(self.getButton("GESTIONE REGISTRO ANAGRAFE CONDOMINIALE",
                                                 "Scegli un immobile e gestisci le unità immobiliari che lo compongono e i condomini che lo abitano.",
                                                 self.goRegistroAnagrafe))
        vertical_layout.addWidget(self.getButton("GESTIONE CONTABILITÀ",
                                                 "Aggiungi le rate versate e le spese a carico di un qualsiasi immobile.",
                                                 self.goContabilita))
        vertical_layout.addWidget(self.getButton("GESTIONE BILANCIO",
                                                 "Scegli un immobile e visualizza le sue tabelle millesimali o calcola il bilancio dell'esercizio.",
                                                 self.goBilancio))
        vertical_layout.addWidget(self.getButton("GESTIONE DOCUMENTI",
                                                 "Visualizza tutti i documenti creati come i registri anagrafici o i prospetti del bilancio degli immobili.",
                                                 self.goDocumenti))
        self.setLayout(vertical_layout)
        self.resize(600, 400)

    def getButton(self, testo, sottotesto, on_click):
        button = QPushButton(testo)
        button.setText(button.text() + "\n" + sottotesto)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button.clicked.connect(on_click)
        return button

    def goImmobile(self):
        self.vista_immobile = VistaGestioneImmobile()
        self.vista_immobile.show()

    def goRegistroAnagrafe(self):
        self.vista_menuRegistroAnagrafe = VistaMenuRegistroAnagrafe()
        self.vista_menuRegistroAnagrafe.show()


    def goContabilita(self):
        self.vista_contabilita = VistaGestioneContabilita()
        self.vista_contabilita.show()

    def goBilancio(self):
        self.vista_bilancio = VistaMenuGestioneBilancio()
        self.vista_bilancio.show()

    def goDocumenti(self):
        self.vista_documenti = VistaGestioneDocumenti()
        self.vista_documenti.show()
