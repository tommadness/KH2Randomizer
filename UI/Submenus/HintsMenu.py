from UI.Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox,QCheckBox

class HintsMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Hint Systems"

        hintSystem = QComboBox()
        hintSystem.addItems(["Disabled","Shananas","JSmartee","Points"])
        hintSystem.currentTextChanged.connect(self.changeHintsType)
        self.addOption("Hint System",hintSystem)
        self.addFlagOption(hintSystem,"hintsType")
        
        self.noSelfHinting = QCheckBox()
        self.noSelfHinting.stateChanged.connect(lambda state : self.setKeyValue("preventSelfHinting",state==Qt.Checked))
        self.noSelfHinting.setCheckState(Qt.Checked)
        self.addOption("Remove Self-Hinting Reports",self.noSelfHinting)
        self.addFlagOption(self.noSelfHinting,"preventSelfHinting")

        self.pointReportProofs = QCheckBox()
        self.pointReportProofs.stateChanged.connect(lambda state : self.setKeyValue("allowProofHinting",state==Qt.Checked))
        self.pointReportProofs.setCheckState(Qt.Checked)
        self.addOption("(Points Only) Reports can Hint Proofs",self.pointReportProofs)
        self.addFlagOption(self.pointReportProofs,"allowProofHinting")

        # setting hints after to trigger the enable/disable of self-hinting
        hintSystem.setCurrentIndex(1)

        self.finalizeMenu()

    def changeHintsType(self,text):
        self.setKeyValue("hintsType",text)
        if "JSmartee" in text or "Points" in text:
            self.noSelfHinting.setEnabled(True)
        else:
            self.noSelfHinting.setEnabled(False)
        if "Points" in text:
            self.pointReportProofs.setEnabled(True)
        else:
            self.pointReportProofs.setEnabled(False)

    def updateWidgets(self):
        self.widgetList[0].setCurrentText(self.getKeyValue("hintsType"))
        self.widgetList[1].setCheckState(Qt.Checked if self.getKeyValue("preventSelfHinting") else Qt.Unchecked)
        self.widgetList[2].setCheckState(Qt.Checked if self.getKeyValue("allowProofHinting") else Qt.Unchecked)