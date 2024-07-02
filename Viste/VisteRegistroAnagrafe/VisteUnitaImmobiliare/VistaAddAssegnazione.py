
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton, \
    QSizePolicy

from Classes.RegistroAnagrafe.unitaImmobiliare import UnitaImmobiliare
from Classes.RegistroAnagrafe.immobile import Immobile
from Classes.RegistroAnagrafe.condomino import Condomino
from Viste.VisteRegistroAnagrafe.VisteCondomino.VistaAddCondomino import VistaAddCondomino


class VistaAddAssegnazione(QWidget):

    def __init__(self, search_text, callback):
        super(VistaAddAssegnazione, self).__init__()
        print("eu estou")
        self.search_text = search_text
        self.callback = callback
        main_layout = QGridLayout()
        self.input_lines = {}

        lbl_frase = QLabel("Inserisci i dati per la nuova assegnazione:")
        lbl_frase.setStyleSheet("font-weight: bold;")
        lbl_frase.setFixedSize(lbl_frase.sizeHint())

        main_layout.addWidget(lbl_frase, 0, 0, 1, 2)

        main_layout.addLayout(self.pairLabelInput("Tipologia Unità Immobiliare", "tipoUnitaImmobiliare", ), 1, 0, 1, 2)
        main_layout.addLayout(self.pairLabelInput("Scala", "scala"), 2, 0)
        main_layout.addLayout(self.pairLabelInput("Interno", "interno"), 2, 1)
        main_layout.addLayout(self.pairLabelInput("Foglio", "foglio"), 3, 0)
        main_layout.addLayout(self.pairLabelInput("Particella", "particella"), 3, 1)
        main_layout.addLayout(self.pairLabelInput("Subalterno", "subalterno"), 4, 0)
        main_layout.addLayout(self.pairLabelInput("ZC", "ZC"), 4, 1)
        main_layout.addLayout(self.pairLabelInput("Classe", "classe"), 5, 0)
        main_layout.addLayout(self.pairLabelInput("Categoria", "categoria"), 5, 1)

        main_layout.addWidget(self.create_button("Svuota i campi", self.reset), 6, 0)
        main_layout.addWidget(self.create_button("Assegna Condomini", self.createUnitaImmobiliare), 6, 1)

        self.setLayout(main_layout)

        self.resize(600, 400)
        self.setWindowTitle("Inserimento Nuovo Assegnazione")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(action)
        return button

    def pairLabelInput(self, testo, index):
        pair_layout = QHBoxLayout()

        label = QLabel(testo + ": ")
        input_line = QLineEdit()

        if index == "codice":
            input_line.setValidator(QIntValidator())

        self.input_lines[index] = input_line

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_line)

        return pair_layout

    def createUnitaImmobiliare(self):
        print("esslu")
        self.lista_immobili = []
        self.lista_immobili = list(Immobile.getAllImmobili().values())
        immo = None

        for immobile in self.lista_immobili:
            print(str(immobile.codice) + " -->" + self.search_text)
            print(immobile.sigla + " -->" + self.search_text)
            print(immobile.denominazione + " -->" + self.search_text)

            if str(immobile.codice) == self.search_text:
                immo = immobile
                break
            elif immobile.sigla == self.search_text:
                immo = immobile
                break
            elif immobile.denominazione == self.search_text:
                immo = immobile
                break
        print("Qui ci sono 1")
        try:
            foglio = self.input_lines["foglio"].text()
            subalterno = self.input_lines["subalterno"].text()
            particella = self.input_lines["particella"].text()
            interno = self.input_lines["interno"].text()
            tipo_unita_immobiliare = self.input_lines["tipoUnitaImmobiliare"].text()
            categoria = self.input_lines["categoria"].text()
            classe = self.input_lines["classe"].text()
            scala = self.input_lines["scala"].text()
            zc = self.input_lines["ZC"].text()
            print("Qui ci sono 2")
            temp_unitaImmobiliare = UnitaImmobiliare()
            msg = temp_unitaImmobiliare.aggiungiUnitaImmobiliare(int(foglio), int(subalterno), {}, int(particella), int(interno),
                                                                 tipo_unita_immobiliare, categoria, int(classe),
                                                                 immo, int(scala), zc)
            print("Msg: " + msg)
            self.callback(msg)
            self.close()
            print("Qui ti blocchi")
            self.vista_nuovo_Condomino = VistaAddCondomino(immo, interno)
            self.vista_nuovo_Condomino.show()

        except ValueError as e:
            print(f"Errore nella conversione degli input: {e}")
        except KeyError as e:
            print(f"Campo di input mancante: {e}")

    def reset(self):
        for input_line in self.input_lines.values():
            input_line.clear()