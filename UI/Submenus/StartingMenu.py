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
        self.start_group()
        self.add_option(settingkey.STARTING_ITEMS)
        self.add_option(settingkey.STARTING_PAGES)
        self.add_option(settingkey.STARTING_DRIVES)
        self.end_group('Starting Items')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STARTING_MAGIC_FIRE)
        self.add_option(settingkey.STARTING_MAGIC_BLIZZARD)
        self.add_option(settingkey.STARTING_MAGIC_THUNDER)
        self.add_option(settingkey.STARTING_MAGIC_CURE)
        self.add_option(settingkey.STARTING_MAGIC_MAGNET)
        self.add_option(settingkey.STARTING_MAGIC_REFLECT)
        self.end_group('Starting Magics')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STARTING_KEYBLADES)
        self.end_group('Starting Keyblades')
        self.end_column(stretch_at_end=False)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STARTING_ABILITIES)
        self.end_group('Starting Abilities')
        self.end_column(stretch_at_end=False)

        self.finalizeMenu()
