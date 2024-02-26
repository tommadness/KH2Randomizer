from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class StartingMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Starting Inventory', settings=settings)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.AUTO_EQUIP_START_ABILITIES)
        self.add_option(settingkey.STARTING_REPORTS)
        self.add_option(settingkey.STARTING_MOVEMENT)
        self.end_group('Starting Inventory Options')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STARTING_INVENTORY)
        self.end_group('Starting Inventory')
        self.end_column(stretch_at_end=False)

        self.finalizeMenu()
