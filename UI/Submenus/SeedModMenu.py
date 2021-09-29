from UI.Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox 

class SeedModMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Seed Modifiers"

        glassCannon = QCheckBox()
        glassCannon.stateChanged.connect(lambda state : self.setKeyValue("Glass Cannon",state==Qt.Checked))
        glassCannon.setCheckState(Qt.Checked)
        glassCannon.setCheckState(Qt.Unchecked)
        self.addOption("Glass Cannon",glassCannon)

        betterJunk = QCheckBox()
        betterJunk.stateChanged.connect(lambda state : self.setKeyValue("Better Junk",state==Qt.Checked))
        betterJunk.setCheckState(Qt.Checked)
        betterJunk.setCheckState(Qt.Unchecked)
        self.addOption("Better Junk",betterJunk)

        startNoAp = QCheckBox()
        startNoAp.stateChanged.connect(lambda state : self.setKeyValue("Start with No AP",state==Qt.Checked))
        startNoAp.setCheckState(Qt.Checked)
        startNoAp.setCheckState(Qt.Unchecked)
        self.addOption("Start with No AP",startNoAp)

        removeDamageCap = QCheckBox()
        removeDamageCap.stateChanged.connect(lambda state : self.setKeyValue("Remove Damage Cap",state==Qt.Checked))
        removeDamageCap.setCheckState(Qt.Checked)
        removeDamageCap.setCheckState(Qt.Unchecked)
        self.addOption("Remove Damage Cap",removeDamageCap)


        self.finalizeMenu()

    def updateWidgets(self):
        self.widgetList[0].setCheckState(Qt.Checked if self.getKeyValue("Glass Cannon") else Qt.Unchecked)
        self.widgetList[1].setCheckState(Qt.Checked if self.getKeyValue("Better Junk") else Qt.Unchecked)
        self.widgetList[2].setCheckState(Qt.Checked if self.getKeyValue("Start with No AP") else Qt.Unchecked)
        self.widgetList[3].setCheckState(Qt.Checked if self.getKeyValue("Remove Damage Cap") else Qt.Unchecked)