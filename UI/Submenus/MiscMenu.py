from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class MiscMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title='Other Reward Locations', in_layout='horizontal', settings=settings)

        self.add_multiselect_buttons(settingkey.SUPERBOSSES_WITH_REWARDS, columns=1, group_title="Superbosses")
        self.add_multiselect_buttons(settingkey.MISC_LOCATIONS_WITH_REWARDS, columns=1, group_title='Misc Locations')

        self.finalizeMenu()
