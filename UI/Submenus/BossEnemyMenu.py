from UI.Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox,QCheckBox

from khbr.randomizer import Randomizer as khbr


class BossEnemyMenu(KH2Submenu):
    def __init__(self):
        super().__init__()
        self.name="Boss/Enemy"

        self.bossEnemyConfig = khbr()._get_game(game="kh2").get_options()

        for key in self.bossEnemyConfig.keys():
            if key != "memory_expansion":
                if True in self.bossEnemyConfig[key]["possible_values"]:
                    # needs to be a toggle
                    box = QCheckBox()
                    box.stateChanged.connect(lambda state, key=key: self.setKeyValue(key,state))
                    box.setCheckState(Qt.Checked)
                    box.setCheckState(Qt.Unchecked)
                    self.addOption(self.bossEnemyConfig[key]["display_name"],box)
                else:
                    # combo box
                    box = QComboBox()
                    box.addItems(self.bossEnemyConfig[key]["possible_values"])
                    box.currentTextChanged.connect(lambda txt,key=key: self.setKeyValue(key,txt))
                    box.setCurrentIndex(1)
                    box.setCurrentIndex(0)
                    self.addOption(self.bossEnemyConfig[key]["display_name"],box)

        self.finalizeMenu()

    def updateWidgets(self):
        counter=0
        for key in self.bossEnemyConfig.keys():
            if key != "memory_expansion":
                if True in self.bossEnemyConfig[key]["possible_values"]:
                    self.widgetList[counter].setCheckState(Qt.Checked if self.getKeyValue(key) else Qt.Unchecked)
                else:
                    self.widgetList[counter].setCurrentText(self.getKeyValue(key))

                counter+=1