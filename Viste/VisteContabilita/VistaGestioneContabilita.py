from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy

from Classes.RegistroAnagrafe.immobile import Immobile
class VistaGestioneContabilita(QWidget):

    def __init__(self, parent=None):
        print("ciao")
        super(VistaGestioneContabilita, self).__init__(parent)

        self.setWindowTitle("Gestione Contabilita")
        vertical_layout = QVBoxLayout()

        vertical_layout.addWidget(self.getButton("Gestione Spese",
                                                 "Inerisci,modifica,visualizza e rimuovi le spese dei vari Immobili.",
                                                 self.goGestioneSpese))
        vertical_layout.addWidget(self.getButton("Gestione Rate",
                                                 "Inserisci,modifica,rimuovi le rate versate dai condomini e stampane la ricevuta.",
                                                 self.goGestioneRate))
        vertical_layout.addWidget(self.getButton("Visualizza Saldo Cassa",
                                                 "Visualizza Il saldo giornaliero dei contanti in cassa.",
                                                 self.goVisualizzaSaldoCassa))
        vertical_layout.addWidget(self.getButton("Visualizza Stato Patrimoniale",
                                                 "Visualizza i debiti e i credi verso un immobile selezionato.",
                                                 self.goVisualizzaStatoPatrimoniale))
        vertical_layout.addWidget(self.getButton("Visualizza Debito Fornitore",
                                                 "Visualizza il debito degli immobili verso un fornitore selezionato.",
                                                 self.goVisualizzaDebitoFornitore))
        vertical_layout.addWidget(self.getButton("Visualizza Credito Condomino",
                                                 "Visualizza il credito degli immobili verso un condomino selezionato ",
                                                 self.goVisualizzaCreditoCondomino))
        self.setLayout(vertical_layout)
        self.resize(600, 400)
        print("ciao")

    def getButton(self, testo, sottotesto, on_click):
        button = QPushButton(testo)
        button.setText(button.text() + "\n" + sottotesto)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button.clicked.connect(on_click)
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
