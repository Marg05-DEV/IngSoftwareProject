import sys

from PyQt6.QtWidgets import QApplication

from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.condomino import Condomino


from Viste.VistaHome import VistaHome


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    vista_home = VistaHome()
    vista_home.show()
    sys.exit(app.exec())
