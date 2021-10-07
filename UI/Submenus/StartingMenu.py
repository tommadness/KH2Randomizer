from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class StartingMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title='Starting Items', settings=settings)

        self.addHeader('Rewards in Starting Areas')

        self.add_option(settingkey.CRITICAL_BONUS_REWARDS)
        self.add_option(settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS)

        self.addHeader("Starting Inventory Options")

        self.add_option(settingkey.SCHMOVEMENT)
        self.add_option(settingkey.LIBRARY_OF_ASSEMBLAGE)
        self.add_option(settingkey.STARTING_INVENTORY)

        self.finalizeMenu()
