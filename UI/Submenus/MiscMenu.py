import os
from Submenus.SubMenu import KH2Submenu
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

class MiscMenu(KH2Submenu):
    def __init__(self):
        super().__init__("horizontal")
        self.name="Misc Locations with Rewards"

        worlds = [  {"name":"Olympus Cups","enabled":False,"icon":"icons/misc/cups.png"},
                    {"name":"Hades Cup","enabled":False,"icon":"icons/misc/paradox_cup.png"},
                    {"name":"Puzzles","enabled":False,"icon":"icons/misc/puzzle.png"},
                    ]

        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)

        for i in range(len(worlds)):
            world = worlds[i]
            worldWidget = QPushButton()
            icon = QIcon(dir_path+"/"+world["icon"])
            if i==0:
                size = icon.actualSize(icon.availableSizes()[0]/5)
            else:
                size = icon.actualSize(icon.availableSizes()[0]/2.5)

            worldWidget.setFixedSize(size)
            worldWidget.setIcon(icon)
            worldWidget.setIconSize(size)
            worldWidget.setCheckable(True)
            worldWidget.toggled.connect(lambda state, val=world["name"] : self.setKeyValue(val,state))
            worldWidget.toggle()
            if not world["enabled"]:
                worldWidget.toggle()

            self.addOption(world["name"],worldWidget,option_layout="vertical")

        self.finalizeMenu()