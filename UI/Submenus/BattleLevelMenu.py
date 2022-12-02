from ctypes import alignment
from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton,QSizePolicy

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.configDict import locationType
from UI.Submenus.SubMenu import KH2Submenu
from Module.battleLevels import BtlvViewer

from PySide6.QtWidgets import QLabel

class BattleLevelMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='World Battle Levels', settings=settings, in_layout='horizontal')
        self.world_level_labels = {}
        self.battle_levels = BtlvViewer()

        self.start_column()
        self.addHeader("Options")
        self.end_column()

        self.start_column()
        self.addHeader("Battle Levels")
        self.add_battle_level_info(locationType.STT,1)
        self.add_battle_level_info(locationType.TT,3)
        self.add_battle_level_info(locationType.HB,2)
        self.add_battle_level_info(locationType.LoD,2)
        self.add_battle_level_info(locationType.BC,2)
        self.add_battle_level_info(locationType.OC,2)
        self.add_battle_level_info(locationType.DC,1)
        self.add_battle_level_info(locationType.PR,2)
        self.add_battle_level_info(locationType.Agrabah,2)
        self.add_battle_level_info(locationType.HT,2)
        self.add_battle_level_info(locationType.PL,2)
        self.add_battle_level_info(locationType.SP,2)
        self.add_battle_level_info(locationType.TWTNW,1)
        self.end_column()

        self.finalizeMenu()

    def update_battle_level_display(self):
        pass
        

    def add_battle_level_info(self,world,visits=1):
        world_label = QLabel(world.value)
        world_layout = QHBoxLayout()
        world_layout.addWidget(world_label)
        self.world_level_labels[world] = []
        for x in range(visits):
            world_level_label = QLabel("50")
            world_layout.addWidget(world_level_label)
            self.world_level_labels[world].append(world_level_label)
        world_widget = QWidget()
        world_widget.setLayout(world_layout)
        self.pending_column.addWidget(world_widget)