from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class SeedModMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Seed Modifiers', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_option(settingkey.GLASS_CANNON)
        self.add_option(settingkey.BETTER_JUNK)
        self.add_option(settingkey.START_NO_AP)
        self.add_option(settingkey.REMOVE_DAMAGE_CAP)
        self.end_column()

        self.start_column()
        self.add_option(settingkey.AS_DATA_SPLIT)
        self.add_option(settingkey.CUPS_GIVE_XP)
        self.add_option(settingkey.RETRY_DFX)
        self.end_column()

        self.finalizeMenu()
