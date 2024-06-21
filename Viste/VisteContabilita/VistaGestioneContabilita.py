from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy


class VistaGestioneContabilita(QWidget):

    def __init__(self, parent=None):
        print("class VistaGestioneContabilità - __init__ inizio")
        super(VistaGestioneContabilita, self).__init__(parent)

        main_layout = QVBoxLayout()
        button_layout = QVBoxLayout()

        button_layout.addWidget(self.getButton("Gestione Spese",
                                                 "Inserisci, modifica, visualizza e rimuovi le spese dei vari immobili.",
                                                 self.goGestioneSpese))
        button_layout.addWidget(self.getButton("Gestione Rate",
                                                 "Inserisci, modifica, rimuovi le rate versate dai condomini e stampane la ricevuta.",
                                                 self.goGestioneRate))
        button_layout.addWidget(self.getButton("Visualizza Saldo Cassa",
                                                 "Visualizza il saldo giornaliero dei contanti in cassa.",
                                                 self.goVisualizzaSaldoCassa))
        button_layout.addWidget(self.getButton("Visualizza Stato Patrimoniale",
                                                 "Visualizza i crediti e i debiti verso un immobile selezionato.",
                                                 self.goVisualizzaStatoPatrimoniale))
        button_layout.addWidget(self.getButton("Visualizza Debito Fornitore",
                                                 "Visualizza il debito degli immobili verso un fornitore selezionato.",
                                                 self.goVisualizzaDebitoFornitore))
        button_layout.addWidget(self.getButton("Visualizza Credito Condomino",
                                                 "Visualizza il credito degli immobili verso un condomino selezionato.",
                                                 self.goVisualizzaCreditoCondomino))
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Contabilità")
        print("end class VistaGestioneContabilita")

    def getButton(self, testo, sottotesto, on_click):
        print("Creazione bottone")
        button = QPushButton(testo)
        button.setText(button.text() + "\n" + sottotesto)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button.clicked.connect(on_click)
        print("**Ritorno il pulsante**")  # Add this line to return the button
        return button

    def goGestioneSpese(self):
        pass

    def goGestioneRate(self):
        pass
    def goVisualizzaSaldoCassa(self):
       pass

    def goVisualizzaStatoPatrimoniale(self):
        pass

    def goVisualizzaDebitoFornitore(self):
        pass

    def goVisualizzaCreditoCondomino(self):
        pass
