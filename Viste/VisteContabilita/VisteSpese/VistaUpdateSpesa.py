from PyQt6.QtWidgets import QWidget


class VistaUpdateSpesa(QWidget):
    def __init__(self, spesa, callback):
        super(VistaUpdateSpesa, self).__init__()
        self.spesa = spesa
        self.callback = callback