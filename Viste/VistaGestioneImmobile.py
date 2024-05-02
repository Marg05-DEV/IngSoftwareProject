from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView


def stato(testo):
    print(testo)


class VistaGestioneImmobile(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneImmobile, self).__init__(parent)

        v_layout = QVBoxLayout()
        
        self.lista_immobili = QListView()
        v_layout.addWidget(self.lista_immobili)
        find_layout = QGridLayout()
        searchbar = QLineEdit("Ricerca...")
        find_layout.addWidget(searchbar, 0, 0)

        v_layout.addLayout(find_layout)
        self.setLayout(v_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Immobile")
