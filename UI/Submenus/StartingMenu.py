from Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox

class StartingMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Starting Items"
        self.addHeader("Rewards in Starting Areas")

        critBonuses = QCheckBox()
        critBonuses.stateChanged.connect(lambda state : self.setKeyValue("critBonuses",state==Qt.Checked))
        critBonuses.setCheckState(Qt.Checked)
        self.addOption("Critical Bonuses",critBonuses)

        goa = QCheckBox()
        goa.stateChanged.connect(lambda state : self.setKeyValue("goa",state==Qt.Checked))
        goa.setCheckState(Qt.Checked)
        self.addOption("Garden of Assemblage",goa)

        self.addHeader("Starting Inventory Options")
        schmovement = QCheckBox()
        schmovement.stateChanged.connect(lambda state : self.setKeyValue("schmovement",state==Qt.Checked))
        schmovement.setCheckState(Qt.Checked)
        self.addOption("Schmovement",schmovement)

        self.finalizeMenu()