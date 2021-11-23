from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class KeybladeMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Keyblades', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_option(settingkey.KEYBLADE_MIN_STAT)
        self.add_option(settingkey.KEYBLADE_MAX_STAT)
        self.end_column()
        self.start_column()
        self.add_option(settingkey.KEYBLADE_SUPPORT_ABILITIES)
        self.end_column(stretch_at_end=False)
        self.start_column()
        self.add_option(settingkey.KEYBLADE_ACTION_ABILITIES)
        self.end_column(stretch_at_end=False)

        self.finalizeMenu()
