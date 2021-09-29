from UI.Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox,QCheckBox

class HintsMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Hint Systems"

        hintSystem = QComboBox()
        hintSystem.addItems(["Disabled","Shananas","JSmartee","JSmartee-FirstVisit","JSmartee-SecondVisit","JSmartee-FirstBoss","JSmartee-SecondBoss"])
        hintSystem.currentTextChanged.connect(self.changeHintsType)
        self.addOption("Hint System",hintSystem)
        
        self.noSelfHinting = QCheckBox()
        self.noSelfHinting.stateChanged.connect(lambda state : self.setKeyValue("preventSelfHinting",state==Qt.Checked))
        self.noSelfHinting.setCheckState(Qt.Checked)
        self.addOption("Remove Self-Hinting Reports (JSmartee Only)",self.noSelfHinting)

        # setting hints after to trigger the enable/disable of self-hinting
        hintSystem.setCurrentIndex(1)

        self.finalizeMenu()

    def changeHintsType(self,text):
        self.setKeyValue("hintsType",text)
        if "JSmartee" in text:
            self.noSelfHinting.setEnabled(True)
        else:
            self.noSelfHinting.setEnabled(False)

    def updateWidgets(self):
        self.widgetList[0].setCurrentText(self.getKeyValue("hintsType"))
        self.widgetList[1].setCheckState(Qt.Checked if self.getKeyValue("preventSelfHinting") else Qt.Unchecked)