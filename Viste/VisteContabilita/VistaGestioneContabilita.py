from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QHBoxLayout

from Viste.VisteContabilita.VisteRate.VistaGestioneRate import VistaGestioneRate
from Viste.VisteContabilita.VisteSpese.VistaGestioneSpese import VistaGestioneSpese
from Viste.VisteContabilita.VisteVisualizzazione.VistaCreditoCondomino import VistaCreditoCondomino
from Viste.VisteContabilita.VisteVisualizzazione.VistaDebitoFornitore import VistaDebitoFornitore
from Viste.VisteContabilita.VisteVisualizzazione.VistaSaldoCassa import VistaSaldoCassa
from Viste.VisteContabilita.VisteVisualizzazione.VistaStatoPatrimoniale import VistaStatoPatrimoniale


class VistaGestioneContabilita(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneContabilita, self).__init__(parent)

        self.setWindowTitle("Gestione Contabilità")
        vertical_layout = QVBoxLayout()

        rate_spese_layout = QHBoxLayout()

        rate_spese_layout.addWidget(self.getButton("Gestione Spese",
                                                 "Inerisci,modifica,visualizza e rimuovi\n le spese dei vari Immobili.",
                                                 self.goGestioneSpese))
        rate_spese_layout.addWidget(self.getButton("Gestione Rate",
                                                 "Inserisci,modifica,rimuovi le rate versate\n dai condomini e stampane la ricevuta.",
                                                 self.goGestioneRate))

        vertical_layout.addLayout(rate_spese_layout)

        vertical_layout.addWidget(self.getButton("Visualizza Saldo Cassa",
                                                 "Visualizza Il saldo giornaliero dei contanti in cassa.",
                                                 self.goVisualizzaSaldoCassa))
        vertical_layout.addWidget(self.getButton("Visualizza Stato Patrimoniale",
                                                 "Visualizza i debiti e i credi verso un immobile selezionato.",
                                                 self.goVisualizzaStatoPatrimoniale))

        debito_credito_layout = QHBoxLayout()
        debito_credito_layout.addWidget(self.getButton("Visualizza Debito Fornitore",
                                                 "Visualizza il debito degli immobili verso un\n fornitore selezionato.",
                                                 self.goVisualizzaDebitoFornitore))
        debito_credito_layout.addWidget(self.getButton("Visualizza Credito Condomino",
                                                 "Visualizza il credito degli immobili verso un\n condomino selezionato ",
                                                 self.goVisualizzaCreditoCondomino))
        vertical_layout.addLayout(debito_credito_layout)

        self.setLayout(vertical_layout)
        self.resize(600, 400)

    def getButton(self, testo, sottotesto, on_click):
        button = QPushButton(testo)
        button.setText(button.text() + "\n" + sottotesto)
        if "Gestione" in testo:
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        else:
            button.setMinimumHeight(65)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        button.clicked.connect(on_click)
        return button

    def goGestioneSpese(self):
        self.vista_spese = VistaGestioneSpese()
        self.vista_spese.show()

    def goGestioneRate(self):
        self.vista_rate = VistaGestioneRate()
        self.vista_rate.show()

    def goVisualizzaSaldoCassa(self):
        self.vista_saldo_cassa = VistaSaldoCassa()
        self.vista_saldo_cassa.show()

    def goVisualizzaStatoPatrimoniale(self):
        self.vista_stato_patrimoniale = VistaStatoPatrimoniale()
        self.vista_stato_patrimoniale.show()

    def goVisualizzaDebitoFornitore(self):
        self.vista_debito_fornitore = VistaDebitoFornitore()
        self.vista_debito_fornitore.show()

    def goVisualizzaCreditoCondomino(self):
        self.vista_credito_condomino = VistaCreditoCondomino()
        self.vista_credito_condomino.show()
