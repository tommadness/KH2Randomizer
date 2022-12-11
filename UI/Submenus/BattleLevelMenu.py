from PySide6.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QLabel

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.configDict import locationType
from UI.Submenus.SubMenu import KH2Submenu
from Module.battleLevels import BtlvViewer

class BattleLevelMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title='Battle Levels', settings=settings, in_layout='horizontal')
        self.world_level_labels = {}
        self.battle_levels = BtlvViewer()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.BATTLE_LEVEL_RANDO)
        self.add_option(settingkey.BATTLE_LEVEL_OFFSET)
        self.end_group('Options')
        self.end_column()

        self.start_column()
        self.start_group()
        self.full_world_level_layout = QGridLayout()
        self.add_battle_level_info(locationType.STT)
        self.add_battle_level_info(locationType.TT)
        self.add_battle_level_info(locationType.HB)
        self.add_battle_level_info(locationType.LoD)
        self.add_battle_level_info(locationType.BC)
        self.add_battle_level_info(locationType.OC)
        self.add_battle_level_info(locationType.DC)
        self.add_battle_level_info(locationType.PR)
        self.add_battle_level_info(locationType.Agrabah)
        self.add_battle_level_info(locationType.HT)
        self.add_battle_level_info(locationType.PL)
        self.add_battle_level_info(locationType.SP)
        self.add_battle_level_info(locationType.TWTNW)
        world_widget = QWidget()
        world_widget.setProperty('cssClass', 'layoutWidget')
        world_widget.setLayout(self.full_world_level_layout)
        self.pending_group.addWidget(world_widget)
        self.end_group('Battle Levels')
        self.end_column()

        settings.observe(settingkey.BATTLE_LEVEL_RANDO, self._btlv_setting_change)
        settings.observe(settingkey.BATTLE_LEVEL_OFFSET, self._btlv_setting_change)

        self.finalizeMenu()

    def _btlv_setting_change(self):
        btlv_setting = self.settings.get(settingkey.BATTLE_LEVEL_RANDO)
        btlv_offset = self.settings.get(settingkey.BATTLE_LEVEL_OFFSET)
        self.set_option_visibility(settingkey.BATTLE_LEVEL_OFFSET, visible=(btlv_setting=="Offset"))

        self.update_battle_level_display(btlv_setting,btlv_offset)

    def update_battle_level_display(self,setting_name,btlv_offset):
        self.battle_levels.use_setting(setting_name,btlv_offset)

        for world,label_list in self.world_level_labels.items():
            for x in range(len(label_list)):
                if setting_name in ["+-10","Random"]:
                    label_list[x].setText("?")
                else:
                    label_list[x].setText(str(self.battle_levels.get_battle_levels(world)[x]))
        

    def add_battle_level_info(self,world):
        world_label = QLabel(world.value)
        self.world_level_labels[world] = []
        world_row = len(self.world_level_labels)
        self.full_world_level_layout.addWidget(world_label,world_row,0)

        btlvs = self.battle_levels.get_battle_levels(world)

        for x in range(len(btlvs)):
            world_level_label = QLabel(str(btlvs[x]))
            self.full_world_level_layout.addWidget(world_level_label,world_row,1+x)
            self.world_level_labels[world].append(world_level_label)