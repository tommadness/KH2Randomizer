from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class SeedModMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Seed Modifiers', settings=settings, in_layout='horizontal')
        self.disable_signal = False

        self.start_column()
        self.addHeader('Quality of Life')
        self.add_option(settingkey.ROXAS_ABILITIES_ENABLED)
        self.add_option(settingkey.TT1_JAILBREAK)
        self.add_option(settingkey.SKIP_CARPET_ESCAPE)
        self.add_option(settingkey.PR_MAP_SKIP)
        self.add_option(settingkey.ATLANTICA_TUTORIAL_SKIP)
        self.add_option(settingkey.REMOVE_WARDROBE_ANIMATION)
        self.end_column()

        self.start_column()
        self.addHeader('Other Modifiers')
        self.add_option(settingkey.AS_DATA_SPLIT)
        self.add_option(settingkey.CUPS_GIVE_XP)
        self.add_option(settingkey.RETRY_DFX)
        self.add_option(settingkey.RETRY_DARK_THORN)
        self.add_option(settingkey.REMOVE_DAMAGE_CAP)
        self.end_column()

        self.start_column()
        self.addHeader('Even More Other Modifiers')
        self.add_option(settingkey.BLOCK_COR_SKIP)
        self.add_option(settingkey.BLOCK_SHAN_YU_SKIP)
        self.add_option(settingkey.DISABLE_FINAL_FORM)
        self.end_column()

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
