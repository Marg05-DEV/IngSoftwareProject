from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy


class VistaDeleteRata(QWidget):

    def __init__(self, sel_rata, callback):
        super(VistaDeleteRata, self).__init__()
        self.callback = callback
        self.rata_selezionata = sel_rata
        main_layout = QVBoxLayout()

        lbl_frase = QLabel("Sei sicuro di voler rimuovere la rata?")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.create_button("Procedi", self.deleteRata))
        button_layout.addWidget(self.create_button("Annulla", self.close))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(350, 150)
        self.setWindowTitle("Rimuovi Rata")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        return button

    def deleteRata(self):
        msg = self.rata_selezionata.rimuoviRata()
        self.callback(msg)
        self.close()
