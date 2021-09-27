from Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox,QDoubleSpinBox,QCheckBox

class SoraMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Sora"

        soraLevels = QComboBox()
        soraLevels.addItems(['Level 1','Level 50','Level 99'])
        soraLevels.currentTextChanged.connect(lambda txt : self.setKeyValue("levelChoice",txt))
        soraLevels.setCurrentIndex(1)

        self.addOption("Sora Levels",soraLevels)

        formLevels = QCheckBox()
        formLevels.stateChanged.connect(lambda state : self.setKeyValue("Form Levels",state==Qt.Checked))
        formLevels.setCheckState(Qt.Checked)
        self.addOption("Form Level Rewards",formLevels)

        self.addHeader("Experience Multipliers")

        soraExp = QDoubleSpinBox()
        soraExp.setDecimals(1)
        soraExp.setRange(.5,10)
        soraExp.setSingleStep(.5)
        soraExp.valueChanged.connect(lambda val : self.setKeyValue("soraExpMult",val))
        soraExp.setValue(2)
        line = soraExp.lineEdit()
        line.setReadOnly(True)
        self.addOption("Sora",soraExp)

        self.drives = ["Valor","Wisdom","Limit","Master","Final","Summon"]
        expMult = [7,3,4,3,3,2]

        for i in range(len(self.drives)):
            driveExp = QDoubleSpinBox()
            driveExp.setDecimals(1)
            driveExp.setRange(1,10)
            driveExp.setSingleStep(.5)
            driveExp.valueChanged.connect(lambda val,i=i : self.setKeyValue(f"{self.drives[i]}Exp",val))
            driveExp.setValue(expMult[i])
            line = driveExp.lineEdit()
            line.setReadOnly(True)
            self.addOption(self.drives[i],driveExp)



        self.finalizeMenu()

    def updateWidgets(self):
        self.widgetList[0].setCurrentText(self.getKeyValue("levelChoice"))
        self.widgetList[1].setCheckState(Qt.Checked if self.getKeyValue("Form Levels") else Qt.Unchecked)
        self.widgetList[2].setValue(self.getKeyValue("soraExpMult"))
        for i in range(len(self.drives)):
            self.widgetList[i+3].setValue(self.getKeyValue(f"{self.drives[i]}Exp"))
