from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class WorldMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title='Worlds with Rewards', settings=settings)

        self.add_multiselect_buttons(settingkey.WORLDS_WITH_REWARDS, columns=2, group_title='Worlds')

        self.finalizeMenu()
