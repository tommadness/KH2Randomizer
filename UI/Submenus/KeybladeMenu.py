from Submenus.SubMenu import KH2Submenu
from PySide6.QtWidgets import QSpinBox 


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

        maximumStats = QSpinBox()
        maximumStats.setMinimum(0)
        maximumStats.setMaximum(20)
        maximumStats.valueChanged.connect(lambda val : self.setKeyValue("keybladeMaxStat",val))
        maximumStats.setValue(7)

        self.addOption("Keyblade Min Stat",minimumStats)
        self.addOption("Keyblade Max Stat",maximumStats)

        self.finalizeMenu()