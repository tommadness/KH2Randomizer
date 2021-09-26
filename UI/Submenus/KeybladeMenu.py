from Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSpinBox,QCheckBox


class KeybladeMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Keyblades"

        minimumStats = QSpinBox()
        minimumStats.setMinimum(0)
        minimumStats.setMaximum(20)
        minimumStats.valueChanged.connect(lambda val : self.setKeyValue("keybladeMinStat",val))
        # calling set value twice to trigger the change signal
        minimumStats.setValue(1)
        minimumStats.setValue(0)
        line = minimumStats.lineEdit()
        line.setReadOnly(True)

        maximumStats = QSpinBox()
        maximumStats.setMinimum(0)
        maximumStats.setMaximum(20)
        maximumStats.valueChanged.connect(lambda val : self.setKeyValue("keybladeMaxStat",val))
        maximumStats.setValue(7)
        line = maximumStats.lineEdit()
        line.setReadOnly(True)

        self.addOption("Keyblade Min Stat",minimumStats)
        self.addOption("Keyblade Max Stat",maximumStats)

        supportAbilities = QCheckBox()
        supportAbilities.stateChanged.connect(lambda state : self.setKeyValue("keybladeSupport",state==Qt.Checked))
        supportAbilities.setCheckState(Qt.Checked)
        actionAbilities = QCheckBox()
        actionAbilities.stateChanged.connect(lambda state : self.setKeyValue("keybladeAction",state==Qt.Checked))
        actionAbilities.setCheckState(Qt.Checked)
        actionAbilities.setCheckState(Qt.Unchecked)
        self.addOption("Support Keyblade Abilities",supportAbilities)
        self.addOption("Action Keyblade Abilities",actionAbilities)

        self.finalizeMenu()