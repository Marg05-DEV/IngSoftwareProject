import os
import webbrowser

from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QTreeView, QHeaderView


class VistaGestioneDocumenti(QWidget):

    def __init__(self):
        super(VistaGestioneDocumenti, self).__init__()
        main_layout = QVBoxLayout()

        self.directory_files = os.path.dirname(os.path.abspath(__file__)).replace("Viste\\VisteDocumenti", "Dati\\pdf\\")
        print(self.directory_files)

        model = QFileSystemModel()
        model.setRootPath(self.directory_files)

        self.tree = QTreeView()
        self.tree.setModel(model)
        self.tree.setRootIndex(model.index(self.directory_files))
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tree.selectionModel().selectionChanged.connect(self.activate_button)

        main_layout.addWidget(self.tree)
        self.button_open_file = self.create_button("Apri file", self.open_file)
        self.button_open_file.setDisabled(True)
        main_layout.addWidget(self.button_open_file)

        self.setLayout(main_layout)
        self.resize(1200, 650)
        self.setWindowTitle("Gestione Documenti")

    @staticmethod
    def create_button(testo, action):
        button = QPushButton(testo)
        button.setCheckable(False)
        button.setMaximumHeight(40)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        button.clicked.connect(action)
        return button

    def activate_button(self):
        if self.tree.selectionModel().selectedIndexes():
            path_selezionato = self.tree.model().filePath(self.tree.selectionModel().selectedIndexes()[0])
            if os.path.isdir(path_selezionato):
                self.button_open_file.setDisabled(True)
            elif os.path.isfile(path_selezionato):
                self.button_open_file.setDisabled(False)
        else:
            self.button_open_file.setDisabled(True)

    def open_file(self):
        if self.tree.selectionModel().selectedIndexes():
            path_selezionato = self.tree.model().filePath(self.tree.selectionModel().selectedIndexes()[0])
            if os.path.isfile(path_selezionato):
                webbrowser.open(path_selezionato)