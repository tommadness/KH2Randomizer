from Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox,QCheckBox

from khbr.randomizer import Randomizer as khbr


class BossEnemyMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Boss/Enemy"

        bossEnemyConfig = khbr()._get_game(game="kh2").get_options()

        for key in bossEnemyConfig.keys():
            if key != "memory_expansion":
                if True in bossEnemyConfig[key]["possible_values"]:
                    # needs to be a toggle
                    box = QCheckBox()
                    box.stateChanged.connect(lambda state, key=key: self.setKeyValue(key,state))
                    box.setCheckState(Qt.Unchecked)
                    self.addOption(bossEnemyConfig[key]["display_name"],box)
                else:
                    # combo box
                    box = QComboBox()
                    box.addItems(bossEnemyConfig[key]["possible_values"])
                    box.currentTextChanged.connect(lambda txt,key=key: self.setKeyValue(key,txt))
                    box.setCurrentIndex(1)
                    box.setCurrentIndex(0)
                    self.addOption(bossEnemyConfig[key]["display_name"],box)

        self.finalizeMenu()