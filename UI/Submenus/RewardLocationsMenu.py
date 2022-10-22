from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class RewardLocationsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Reward Locations', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_multiselect_buttons(settingkey.WORLDS_WITH_REWARDS, columns=3, group_title='Worlds',tristate=True)
        self.end_column()
        self.start_column()
        self.add_multiselect_buttons(settingkey.SUPERBOSSES_WITH_REWARDS, columns=1, group_title="Superbosses")
        self.add_multiselect_buttons(settingkey.MISC_LOCATIONS_WITH_REWARDS, columns=1, group_title='Misc Locations')
        self.add_option(settingkey.REMOVE_POPUPS)
        self.end_column()

        self.finalizeMenu()
