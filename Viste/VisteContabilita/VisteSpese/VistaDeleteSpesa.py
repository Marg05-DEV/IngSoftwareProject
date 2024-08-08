from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy


class VistaDeleteSpesa(QWidget):

    def __init__(self, spesa, callback):
        super(VistaDeleteSpesa, self).__init__()
        self.callback = callback
        self.spesa_selezionata = spesa
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere la spesa?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.create_button("Annulla", self.close))
        button_layout.addWidget(self.create_button("Procedi", self.deleteSpesa))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(350, 150)
        self.setWindowTitle("Rimuovi Spesa")

    def create_button(self, testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        return button

    def deleteSpesa(self):
        msg = self.spesa_selezionata.rimuoviSpesa()
        self.callback(msg)
        self.close()
