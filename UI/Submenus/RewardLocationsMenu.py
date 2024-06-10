from Class import settingkey
from Class.seedSettings import SeedSettings
from List.configDict import StartingVisitMode
from UI.Submenus.SubMenu import KH2Submenu


class RewardLocationsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Locations', settings=settings)
        self.disable_signal = False
        self.start_column()
        self.start_group()
        self.add_option(settingkey.SORA_LEVELS)
        self.add_option(settingkey.SPLIT_LEVELS)
        self.add_option(settingkey.CRITICAL_BONUS_REWARDS)
        self.add_option(settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS)
        self.end_group()

        self.start_group()
        self.add_option(settingkey.STARTING_VISIT_MODE)
        self.add_option(settingkey.STARTING_VISIT_RANDOM_MIN)
        self.add_option(settingkey.STARTING_VISIT_RANDOM_MAX)
        self.add_option(settingkey.STARTING_UNLOCKS_SP)
        self.add_option(settingkey.STARTING_UNLOCKS_PR)
        self.add_option(settingkey.STARTING_UNLOCKS_TT)
        self.add_option(settingkey.STARTING_UNLOCKS_OC)
        self.add_option(settingkey.STARTING_UNLOCKS_HT)
        self.add_option(settingkey.STARTING_UNLOCKS_LOD)
        self.add_option(settingkey.STARTING_UNLOCKS_TWTNW)
        self.add_option(settingkey.STARTING_UNLOCKS_BC)
        self.add_option(settingkey.STARTING_UNLOCKS_AG)
        self.add_option(settingkey.STARTING_UNLOCKS_PL)
        self.add_option(settingkey.STARTING_UNLOCKS_HB)
        self.add_option(settingkey.STARTING_UNLOCKS_DC)
        self.add_option(settingkey.STARTING_UNLOCKS_STT)
        self.end_group("Starting Visit Availability")
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_multiselect_buttons(settingkey.WORLDS_WITH_REWARDS, columns=2, group_title='Worlds',tristate=True)
        self.end_group('Worlds')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_multiselect_buttons(settingkey.SUPERBOSSES_WITH_REWARDS, columns=1, group_title="Superbosses")
        self.end_group('Superbosses')

        self.start_group()
        self.add_multiselect_buttons(settingkey.MISC_LOCATIONS_WITH_REWARDS, columns=1, group_title='Misc Locations')
        self.end_group('Misc Locations')

        self.start_group()
        self.add_option(settingkey.REMOVE_POPUPS)
        self.end_group()
        self.end_column()

        settings.observe(settingkey.SORA_LEVELS, self.world_update)
        settings.observe(settingkey.STARTING_VISIT_MODE, self._starting_visit_mode_changed)
        settings.observe(settingkey.STARTING_VISIT_RANDOM_MIN, self._starting_visit_random_value_changed)
        settings.observe(settingkey.STARTING_VISIT_RANDOM_MAX, self._starting_visit_random_value_changed)

        self.finalizeMenu()
        
    def world_update(self):
        if not self.disable_signal:
            level_setting = self.settings.get(settingkey.SORA_LEVELS)
            _, widget = self.widgets_and_settings_by_name[settingkey.SPLIT_LEVELS]
            if "Level" == level_setting:
                widget.setChecked(False)
                widget.setEnabled(False)
            else:
                widget.setEnabled(True)

    def _starting_visit_mode_changed(self):
        mode = StartingVisitMode[self.settings.get(settingkey.STARTING_VISIT_MODE)]

        random = (mode is StartingVisitMode.RANDOM) or (mode is StartingVisitMode.CUSTOM) 
        self.set_option_visibility(settingkey.STARTING_VISIT_RANDOM_MIN, random)
        self.set_option_visibility(settingkey.STARTING_VISIT_RANDOM_MAX, random)

        specific = (mode is StartingVisitMode.SPECIFIC) or (mode is StartingVisitMode.CUSTOM)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_STT, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_HB, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_OC, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_LOD, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_PL, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_HT, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_SP, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_TT, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_BC, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_AG, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_DC, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_PR, specific)
        self.set_option_visibility(settingkey.STARTING_UNLOCKS_TWTNW, specific)

    def _starting_visit_random_value_changed(self):
        min_random = self.settings.get(settingkey.STARTING_VISIT_RANDOM_MIN)
        max_random = self.settings.get(settingkey.STARTING_VISIT_RANDOM_MAX)
        if min_random > max_random:
            self.settings.set(settingkey.STARTING_VISIT_RANDOM_MAX, min_random)
            self.update_widget(settingkey.STARTING_VISIT_RANDOM_MAX)

    def disable_widgets(self):
        self.disable_signal = True
        super().disable_widgets()
