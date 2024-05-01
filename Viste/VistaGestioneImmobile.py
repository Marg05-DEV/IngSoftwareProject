from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit


class VistaGestioneImmobile(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneImmobile, self).__init__(parent)
        v_layout = QVBoxLayout()

        find_layout = QGridLayout()
        searchbar = QLineEdit("Ricerca...")
        searchbar.textChanged.connect(self.stato("in cambiamento"))
        find_layout.addWidget(searchbar, 0, 0)

        v_layout.addLayout(find_layout)
        self.setLayout(v_layout)
        self.setWindowTitle("Gestione Immobile")
        self.resize(600, 400)

    def stato(self, testo):
        print(testo)