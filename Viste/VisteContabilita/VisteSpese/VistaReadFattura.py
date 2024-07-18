from PyQt6.QtWidgets import QWidget


class VistaReadFattura(QWidget):
    def __init__(self, spesa, callback):
        super(VistaReadFattura, self).__init__()
        self.spesa = spesa
        self.callback = callback