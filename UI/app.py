import random,sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QPushButton, 
    QTabWidget,QVBoxLayout,QHBoxLayout,QWidget
)

from Submenus.SoraMenu import SoraMenu
from Submenus.KeybladeMenu import KeybladeMenu
from Submenus.WorldMenu import WorldMenu
from Submenus.SuperbossMenu import SuperbossMenu
from Submenus.MiscMenu import MiscMenu
from Submenus.StartingMenu import StartingMenu
from Submenus.HintsMenu import HintsMenu
from Submenus.SeedModMenu import SeedModMenu
from Submenus.ItemPlacementMenu import ItemPlacementMenu


class KH2RandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KH2 Randomizer Seed Generator")
        pagelayout = QVBoxLayout()
        seed_layout = QHBoxLayout()
        submit_layout = QHBoxLayout()
        self.tabs = QTabWidget()

        pagelayout.addLayout(seed_layout)
        pagelayout.addWidget(self.tabs)
        pagelayout.addLayout(submit_layout)

        seed_layout.addWidget(QLabel("Seed"))
        self.seedName=QLineEdit()
        self.seedName.setPlaceholderText("Leave blank for a random seed")
        seed_layout.addWidget(self.seedName)


        self.widgets = [SoraMenu(),StartingMenu(),HintsMenu(),KeybladeMenu(),WorldMenu(),SuperbossMenu(),MiscMenu(),SeedModMenu(),ItemPlacementMenu()] #["Item Placement Modifiers", "Boss/Enemy"]

        for i in range(len(self.widgets)):
            self.tabs.addTab(self.widgets[i],self.widgets[i].getName())


        submitButton = QPushButton("Generate Seed")
        submitButton.clicked.connect(self.makeSeed)
        submit_layout.addWidget(submitButton)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def makeSeed(self):
        settings = {}
        for x in self.widgets:
            settings[x.getName()] = x.getData()
        print(settings)


if __name__=="__main__":
    app = QApplication([])
    window = KH2RandomizerApp()
    window.show()

    sys.exit(app.exec())
