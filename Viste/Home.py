from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy


class VistaHome(QWidget):
    def __init__(self, parent = None):
        super(VistaHome, self).__init__(parent)
        vertical_layout = QVBoxLayout
        vertical_layout.addWidget(self.getButton("Gestione Immobile", self.goImmobile()))
        vertical_layout.addWidget(self.getButton("Gestione Registro Anagrafe Condominiale", self.goRegistroAnagrafe()))
        vertical_layout.addWidget(self.getButton("Gestione Contabilità", self.goContabilita()))
        vertical_layout.addWidget(self.getButton("Gestione Bilancio", self.goBilancio()))
        vertical_layout.addWidget(self.getButton("Gestione Documenti", self.goDocumenti()))
        self.setLayout(vertical_layout)

    def getButton(self, testo, onclick):
        button = QPushButton(testo)
        button.clicked.connect(onclick)
        return button

    def goImmobile(self):
        pass

    def goRegistroAnagrafe(self):
        pass

    def goContabilita(self):
        pass

    def goBilancio(self):
        pass

    def goDocumenti(self):
        pass