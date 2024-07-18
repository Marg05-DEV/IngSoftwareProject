from PyQt6.QtWidgets import QWidget


class VistaCreateSpesa(QWidget):
    def __init__(self, callback):
        super(VistaCreateSpesa, self).__init__()
        self.callback = callback