from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class ShopDropMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Shops/Drops', settings=settings, in_layout='horizontal')

        self.start_column()
        self.addHeader('Shops')
        self.add_option(settingkey.SHOP_KEYBLADES)
        self.add_option(settingkey.SHOP_UNLOCKS)
        self.add_option(settingkey.SHOP_REPORTS)
        self.end_column(stretch_at_end=True)

        self.start_column()
        self.addHeader('Drops')
        self.add_option(settingkey.GLOBAL_JACKPOT)
        self.add_option(settingkey.GLOBAL_LUCKY)
        self.add_option(settingkey.RICH_ENEMIES)
        self.add_option(settingkey.UNLIMITED_MP)
        self.end_column(stretch_at_end=True)
        
        self.finalizeMenu()
