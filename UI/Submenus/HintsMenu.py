from UI.Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox,QCheckBox,QHBoxLayout,QLabel

class HintsMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Hint Systems"

        hintSystem = QComboBox()
        hintSystem.addItems(["Disabled","Shananas","JSmartee","Points"])
        hintSystem.currentTextChanged.connect(self.changeHintsType)
        self.addOption("Hint System",hintSystem)
        self.addFlagOption(hintSystem,"hintsType")

        # adding some explanatory text for when a hint system is selected
        self.hintText = QLabel("")
        self.hintText.setStyleSheet("font: bold 12px;")
        layout = QHBoxLayout()
        layout.addWidget(self.hintText)
        self.menulayout.addLayout(layout)

        reportDepth = QComboBox()
        reportDepth.addItems(["DataFight","FirstVisit","SecondVisit","FirstBoss","SecondBoss"])
        reportDepth.currentTextChanged.connect(lambda text : self.setKeyValue("reportDepth",reportDepth.currentText()))
        self.addOption("Report Depth",reportDepth)
        self.addFlagOption(reportDepth,"reportDepth")
        
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
        reportDepth.setCurrentIndex(2)
        reportDepth.setCurrentIndex(0)

        self.finalizeMenu()

    def changeHintsType(self,text):
        self.setKeyValue("hintsType",text)
        if "JSmartee" in text:
            self.hintText.setText("Reports provide information for how many \"important checks\" are in a world.")
        if "Disabled" in text:
            self.hintText.setText("Using no hint system")
        if "Shananas" in text:
            self.hintText.setText("Each world will provide information about how many \"important checks\" are there by telling you when the world has no more.")
        if "Points" in text:
            self.hintText.setText("Each \"important check\" is assigned a point value, and you are told the number of points in each world. Reports tell you where items are. ")



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
        self.widgetList[1].setCurrentText(self.getKeyValue("reportDepth"))
        self.widgetList[2].setCheckState(Qt.Checked if self.getKeyValue("preventSelfHinting") else Qt.Unchecked)
        self.widgetList[3].setCheckState(Qt.Checked if self.getKeyValue("allowProofHinting") else Qt.Unchecked)