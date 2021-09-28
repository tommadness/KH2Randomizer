import os

from Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class WorldMenu(KH2Submenu):
    def __init__(self):
        super().__init__("grid")
        self.name="Worlds with Rewards"

        self.worlds = [  {"name":"Land of Dragons","enabled":True,"icon":"icons/worlds/land_of_dragons.png"},
                    {"name":"Beast's Castle","enabled":True,"icon":"icons/worlds/beast's_castle.png"},
                    {"name":"Hollow Bastion","enabled":True,"icon":"icons/worlds/hollow_bastion.png"},
                    {"name":"Cavern of Remembrance","enabled":True,"icon":"icons/worlds/cor.png"},
                    {"name":"Twilight Town","enabled":True,"icon":"icons/worlds/twilight_town.png"},
                    {"name":"The World that Never Was","enabled":True,"icon":"icons/worlds/the_world_that_never_was.png"},
                    {"name":"Space Paranoids","enabled":True,"icon":"icons/worlds/space_paranoids.png"},
                    {"name":"Atlantica","enabled":False,"icon":"icons/worlds/atlantica_musical.png"},
                    {"name":"Port Royal","enabled":True,"icon":"icons/worlds/port_royal.png"},
                    {"name":"Olympus Coliseum","enabled":True,"icon":"icons/worlds/olympus_underworld.png"},
                    {"name":"Agrabah","enabled":True,"icon":"icons/worlds/agrabah.png"},
                    {"name":"Halloween Town","enabled":True,"icon":"icons/worlds/halloween_town.png"},
                    {"name":"Pride Lands","enabled":True,"icon":"icons/worlds/pride_lands.png"},
                    {"name":"Disney Castle/Timeless River","enabled":True,"icon":"icons/worlds/disney_castle.png"},
                    {"name":"Hundred Acre Wood","enabled":True,"icon":"icons/worlds/100_acre_wood.png"},
                    {"name":"Simulated Twilight Town","enabled":True,"icon":"icons/worlds/simulated_twilight_town.png"},
                    ]

        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)

        for i in range(len(self.worlds)):
            world = self.worlds[i]
            worldWidget = QPushButton()
            icon = QIcon(dir_path+"/"+world["icon"])
            worldWidget.setFixedSize(icon.actualSize(icon.availableSizes()[0]/8))
            worldWidget.setIcon(icon)
            worldWidget.setIconSize(icon.availableSizes()[0]/8)
            worldWidget.setCheckable(True)
            worldWidget.toggled.connect(lambda state, val=world["name"] : self.setKeyValue(val,state))
            worldWidget.toggle()
            if not world["enabled"]:
                worldWidget.toggle()

            self.addOption(world["name"],worldWidget,option_layout="vertical",grid_pos=(i//4,i%4))

        self.finalizeMenu()

    def updateWidgets(self):
        for i in range(len(self.worlds)):
            world = self.worlds[i]
            value = self.getKeyValue(world["name"])
            if value != self.widgetList[i].isChecked():
                self.widgetList[i].toggle()