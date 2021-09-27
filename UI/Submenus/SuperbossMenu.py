import os

from Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class SuperbossMenu(KH2Submenu):
    def __init__(self):
        super().__init__("grid")
        self.name="Superbosses with Rewards"

        worlds = [  {"name":"Absent Silhouettes","enabled":True,"icon":"icons/bosses/as.png"},
                    {"name":"Data Organization XIII","enabled":True,"icon":"icons/bosses/datas.png"},
                    {"name":"Sephiroth","enabled":True,"icon":"icons/bosses/sephiroth.png"},
                    {"name":"Lingering Will (Terra)","enabled":False,"icon":"icons/bosses/lingering_will.png"},]

        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)

        for i in range(len(worlds)):
            world = worlds[i]
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