from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class StartingMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Starting Items', settings=settings, in_layout='horizontal')

        self.start_column()
        self.addHeader('Rewards in Starting Areas')
        self.add_option(settingkey.CRITICAL_BONUS_REWARDS)
        self.add_option(settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS)
        self.end_column()

        self.start_column()
        self.addHeader("Starting Inventory Options")
        self.add_option(settingkey.SCHMOVEMENT)
        self.add_option(settingkey.LIBRARY_OF_ASSEMBLAGE)
        self.add_option(settingkey.STORY_UNLOCKS)
        self.end_column()

        self.start_column()
        self.add_option(settingkey.STARTING_INVENTORY)
        self.end_column(stretch_at_end=False)

        self.finalizeMenu()
