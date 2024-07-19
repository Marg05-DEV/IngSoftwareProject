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

        button_layout.addWidget(self.create_button("Procedi", self.deleteSpesa))
        button_layout.addWidget(self.create_button("Annulla", self.close))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(300, 200)
        self.setWindowTitle("Rimuovi Spesa")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def deleteRata(self):
        msg = self.spesa_selezionata.rimuoviSpesa()
        self.callback(msg)
        self.close()