from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class ItemPlacementMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Item Placement', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_option(settingkey.ENABLE_PROMISE_CHARM)
        self.add_option(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        self.add_option(settingkey.PROOF_DEPTH)
        self.add_option(settingkey.REVERSE_RANDO)
        self.add_option(settingkey.ABILITY_POOL)
        self.end_column()

        self.finalizeMenu()
