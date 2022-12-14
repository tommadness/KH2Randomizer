from PySide6.QtWidgets import QGridLayout, QWidget, QLabel
from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu
from List.configDict import locationType
from Module.battleLevels import BtlvViewer


class SeedModMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Seed Modifiers', settings=settings, in_layout='horizontal')
        self.disable_signal = False

        self.start_column()
        self.start_group()
        self.add_option(settingkey.ROXAS_ABILITIES_ENABLED)
        self.add_option(settingkey.TT1_JAILBREAK)
        self.add_option(settingkey.SKIP_CARPET_ESCAPE)
        self.add_option(settingkey.PR_MAP_SKIP)
        self.add_option(settingkey.REMOVE_WARDROBE_ANIMATION)
        self.add_option(settingkey.FAST_URNS)
        self.add_option(settingkey.ATLANTICA_TUTORIAL_SKIP)
        self.add_option(settingkey.REMOVE_CUTSCENES)
        self.end_group('Quality of Life')
        self.start_group()
        self.add_option(settingkey.AS_DATA_SPLIT)
        self.add_option(settingkey.CUPS_GIVE_XP)
        self.add_option(settingkey.RETRY_DFX)
        self.add_option(settingkey.RETRY_DARK_THORN)
        self.add_option(settingkey.REMOVE_DAMAGE_CAP)
        self.end_group('Other Modifiers')
        self.end_column()

        self.world_level_labels = {}
        self.battle_levels = BtlvViewer()
        self.start_column()
        self.start_group()
        self.add_option(settingkey.GLOBAL_JACKPOT)
        self.add_option(settingkey.GLOBAL_LUCKY)
        self.add_option(settingkey.RICH_ENEMIES)
        self.add_option(settingkey.UNLIMITED_MP)
        self.end_group('Drops')
        self.start_group()
        self.add_option(settingkey.BLOCK_COR_SKIP)
        self.add_option(settingkey.BLOCK_SHAN_YU_SKIP)
        self.add_option(settingkey.DISABLE_FINAL_FORM)
        self.end_group('Challenge Modifiers')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.BATTLE_LEVEL_RANDO)
        self.add_option(settingkey.BATTLE_LEVEL_OFFSET)
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
        settings.observe(settingkey.SOFTLOCK_CHECKING, self.reverse_rando_checking)
        
        self.finalizeMenu()

    def reverse_rando_checking(self):
        softlock_check = self.settings.get(settingkey.SOFTLOCK_CHECKING)
        _, widget = self.widgets_and_settings_by_name[settingkey.AS_DATA_SPLIT]
        if not self.disable_signal:
            if softlock_check in ["reverse", "both"]:
                widget.setChecked(True)
                widget.setEnabled(False)
            else:
                widget.setEnabled(True)

    def disable_widgets(self):
        self.disable_signal = True
        super().disable_widgets()

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
