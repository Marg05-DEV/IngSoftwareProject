from PyQt6.QtWidgets import QWidget


class VistaReadSpesa(QWidget):
    def __init__(self, spesa, callback):
        super(VistaReadSpesa, self).__init__()
        self.spesa = spesa
        self.callback = callback