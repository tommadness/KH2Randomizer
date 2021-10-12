from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class ItemPlacementMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title='Item Placement Options', settings=settings)

        self.add_option(settingkey.ENABLE_PROMISE_CHARM)
        self.add_option(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        self.add_option(settingkey.MAX_LOGIC_ITEM_PLACEMENT)
        self.add_option(settingkey.REVERSE_RANDO)
        self.add_option(settingkey.ABILITY_POOL)

        self.finalizeMenu()
