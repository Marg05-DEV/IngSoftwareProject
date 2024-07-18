from PyQt6.QtWidgets import QWidget


class VistaDeleteSpesa(QWidget):
    def __init__(self, spesa, callback):
        super(VistaDeleteSpesa, self).__init__()
        self.spesa = spesa
        self.callback = callback