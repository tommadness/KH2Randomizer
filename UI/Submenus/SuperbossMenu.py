import os

from UI.Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class SuperbossMenu(KH2Submenu):
    def __init__(self):
        super().__init__("grid")
        self.name="Superbosses with Rewards"

        self.bosses = [  {"name":"Absent Silhouettes","enabled":True,"icon":"icons/bosses/as.png"},
                    {"name":"Data Organization XIII","enabled":True,"icon":"icons/bosses/datas.png"},
                    {"name":"Sephiroth","enabled":True,"icon":"icons/bosses/sephiroth.png"},
                    {"name":"Lingering Will (Terra)","enabled":False,"icon":"icons/bosses/lingering_will.png"},]

        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)

        for i in range(len(self.bosses)):
            world = self.bosses[i]
            worldWidget = QPushButton()
            icon = QIcon(dir_path+"/"+world["icon"])
            if i//2==0:
                size = icon.actualSize(icon.availableSizes()[0]/5)
            else:
                size = icon.actualSize(icon.availableSizes()[0]/4)
            worldWidget.setFixedSize(size)
            worldWidget.setIcon(icon)
            worldWidget.setIconSize(size)
            worldWidget.setCheckable(True)
            worldWidget.toggled.connect(lambda state, val=world["name"] : self.setKeyValue(val,state))
            worldWidget.toggle()
            if not world["enabled"]:
                worldWidget.toggle()

            self.addOption(world["name"],worldWidget,option_layout="vertical",grid_pos=(i//2,i%2))

        self.finalizeMenu()

    def updateWidgets(self):
        for i in range(len(self.bosses)):
            boss = self.bosses[i]
            value = self.getKeyValue(boss["name"])
            if value != self.widgetList[i].isChecked():
                self.widgetList[i].toggle()