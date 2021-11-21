from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class CosmeticsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Cosmetics', settings=settings, in_layout='horizontal')

        self.start_column()
        self.addHeader('Visuals')
        self.add_option(settingkey.COMMAND_MENU)
        self.end_column()
        self.start_column()
        self.addHeader('Music')
        self.add_option(settingkey.BGM_OPTIONS)
        self.add_option(settingkey.BGM_GAMES)
        self.end_column(stretch_at_end=False)

        self.finalizeMenu()
