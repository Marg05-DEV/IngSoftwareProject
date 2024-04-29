from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy


class VistaHome(QWidget):
    def __init__(self, parent=None):
        super(VistaHome, self).__init__(parent)

        self.setWindowTitle("Amministrazione Condominiale")

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.getButton("Gestione Immobile", self.goImmobile))
        vertical_layout.addWidget(self.getButton("Gestione Registro Anagrafe Condominiale", self.goRegistroAnagrafe))
        vertical_layout.addWidget(self.getButton("Gestione Contabilità", self.goContabilita))
        vertical_layout.addWidget(self.getButton("Gestione Bilancio", self.goBilancio))
        vertical_layout.addWidget(self.getButton("Gestione Documenti", self.goDocumenti))

        self.setLayout(vertical_layout)
        self.resize(1920, 1080)
    def getButton(self, testo, on_click):
        button = QPushButton(testo)

        button.setCheckable(True)
        button.clicked.connect(on_click)
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