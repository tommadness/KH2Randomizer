from Submenus.SubMenu import KH2Submenu
from PySide6.QtWidgets import QComboBox

class SoraMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Sora"

        soraLevels = QComboBox()
        soraLevels.addItems(['Level 1','Level 50','Level 99'])
        soraLevels.currentTextChanged.connect(lambda txt : self.setKeyValue("levelChoice",txt))
        soraLevels.setCurrentIndex(1)

        self.addOption("Sora Levels",soraLevels)

        self.finalizeMenu()