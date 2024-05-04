from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListView, QComboBox, QLabel, QHBoxLayout, \
    QPushButton


class VistaGestioneImmobile(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneImmobile, self).__init__(parent)

        main_layout = QVBoxLayout()


        find_layout = QGridLayout()

        searchbar = QLineEdit()
        searchType = QComboBox()
        sortLabel = QLabel("Ordina per:")
        sortType = QComboBox()
        find_layout.addWidget(searchbar, 0, 0, 2, 1)
        find_layout.addWidget(searchType, 0, 2)
        find_layout.addWidget(sortLabel, 1, 0)
        find_layout.addWidget(sortType, 1, 1)

        action_layout = QHBoxLayout()

        lista_immobili = QListView()
        button_layout = QVBoxLayout()

        createBtn = QPushButton("Aggiungi Immobile")
        readBtn = QPushButton("Visualizza Immobile")
        updateBtn = QPushButton("Modifica immobile")
        deleteBtn = QPushButton("Elimina Immobile")

        button_layout.addWidget(createBtn)
        button_layout.addWidget(readBtn)
        button_layout.addWidget(updateBtn)
        button_layout.addWidget(deleteBtn)

        action_layout.addWidget(lista_immobili)
        action_layout.addLayout(button_layout)

        main_layout.addLayout(find_layout)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.setWindowTitle("Gestione Immobile")
