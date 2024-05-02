from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy

from Viste.VistaGestioneImmobile import VistaGestioneImmobile


class VistaHome(QWidget):
    def __init__(self, parent=None):
        super(VistaHome, self).__init__(parent)

        self.setWindowTitle("Amministrazione Condominiale")
        vertical_layout = QVBoxLayout()

        vertical_layout.addWidget(self.getButton("Gestione Immobile",
                                                 "Aggiungi nuovi immobili. Visualizza, modifica o rimuovi quelli esistenti.", self.goImmobile))
        vertical_layout.addWidget(self.getButton("Gestione Registro Anagrafe Condominiale",
                                                 "Scegli un immobile e gestisci le unità immobiliari che lo compongono e i condomini che lo abitano.",self.goRegistroAnagrafe))
        vertical_layout.addWidget(self.getButton("Gestione Contabilità",
                                                 "Aggiungi le rate versate e le spese a carico di un qualsiasi immobile.", self.goContabilita))
        vertical_layout.addWidget(self.getButton("Gestione Bilancio",
                                                 "Scegli un immobile e visualizza le sue tabelle millesimali o calcola il bilancio dell'esercizio.", self.goBilancio))
        vertical_layout.addWidget(self.getButton("Gestione Documenti",
                                                 "Visualizza tutti i documenti creati come i registri anagrafici o i prospetti del bilancio degli immobili.", self.goDocumenti))

        self.setLayout(vertical_layout)
        self.resize(600, 400)
    def getButton(self, testo, sottotesto, on_click):
        button = QPushButton(testo)
        button.setText(button.text() + "\n" + sottotesto)
        button.setFixedSize(580, 75)
        button.setCheckable(True)
        button.clicked.connect(on_click)
        return button

    def goImmobile(self):
        self.vista_immobile = VistaGestioneImmobile()
        self.vista_immobile.show()

    def goRegistroAnagrafe(self):
        pass

    def goContabilita(self):
        pass

    def goBilancio(self):
        pass

    def goDocumenti(self):
        pass