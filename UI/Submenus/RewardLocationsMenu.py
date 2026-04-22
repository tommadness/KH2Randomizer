from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QPushButton

from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class RewardLocationsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Locations', settings=settings)
        self.disable_signal = False
        self.start_column()
        self.start_group()
        self.add_option(settingkey.SORA_LEVELS)
        self.add_option(settingkey.RANDOMIZE_LEVELS_WITH_CHECKS)
        self.add_option(settingkey.SPLIT_LEVELS)
        self.add_option(settingkey.CRITICAL_BONUS_REWARDS)
        self.add_option(settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS)
        self.end_group()

        self.start_group()
        self.set_group_widget(self._visit_presets_menu_button())
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
        self.add_option(settingkey.STARTING_VISIT_RANDOM_MIN)
        self.add_option(settingkey.STARTING_VISIT_RANDOM_MAX)
        self.end_group("Starting Visit Availability")
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_multiselect_buttons(settingkey.WORLDS_WITH_REWARDS, columns=2, group_title='Worlds', tristate=True)
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

    def _visit_presets_menu_button(self) -> QPushButton:
        button = KH2Submenu.make_menu_button()
        menu = QMenu(button)

        no_visits = QAction("No Visits", menu)
        no_visits.triggered.connect(self._no_visits)
        menu.addAction(no_visits)

        first_visits = QAction("Only First Visits", menu)
        first_visits.triggered.connect(self._first_visits)
        menu.addAction(first_visits)

        all_visits = QAction("All Visits", menu)
        all_visits.triggered.connect(self._all_visits)
        menu.addAction(all_visits)

        button.setMenu(menu)
        return button

    def _no_visits(self):
        settings = self.settings
        settings.set(settingkey.STARTING_UNLOCKS_SP, 0)
        settings.set(settingkey.STARTING_UNLOCKS_PR, 0)
        settings.set(settingkey.STARTING_UNLOCKS_TT, 0)
        settings.set(settingkey.STARTING_UNLOCKS_OC, 0)
        settings.set(settingkey.STARTING_UNLOCKS_HT, 0)
        settings.set(settingkey.STARTING_UNLOCKS_LOD, 0)
        settings.set(settingkey.STARTING_UNLOCKS_TWTNW, 0)
        settings.set(settingkey.STARTING_UNLOCKS_BC, 0)
        settings.set(settingkey.STARTING_UNLOCKS_AG, 0)
        settings.set(settingkey.STARTING_UNLOCKS_PL, 0)
        settings.set(settingkey.STARTING_UNLOCKS_HB, 0)
        settings.set(settingkey.STARTING_UNLOCKS_DC, 0)
        settings.set(settingkey.STARTING_UNLOCKS_STT, 0)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MIN, 0)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MAX, 0)
        self.update_widgets()

    def _first_visits(self):
        settings = self.settings
        settings.set(settingkey.STARTING_UNLOCKS_SP, 1)
        settings.set(settingkey.STARTING_UNLOCKS_PR, 1)
        settings.set(settingkey.STARTING_UNLOCKS_TT, 1)
        settings.set(settingkey.STARTING_UNLOCKS_OC, 1)
        settings.set(settingkey.STARTING_UNLOCKS_HT, 1)
        settings.set(settingkey.STARTING_UNLOCKS_LOD, 1)
        settings.set(settingkey.STARTING_UNLOCKS_TWTNW, 1)
        settings.set(settingkey.STARTING_UNLOCKS_BC, 1)
        settings.set(settingkey.STARTING_UNLOCKS_AG, 1)
        settings.set(settingkey.STARTING_UNLOCKS_PL, 1)
        settings.set(settingkey.STARTING_UNLOCKS_HB, 1)
        settings.set(settingkey.STARTING_UNLOCKS_DC, 1)
        settings.set(settingkey.STARTING_UNLOCKS_STT, 1)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MIN, 0)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MAX, 0)
        self.update_widgets()

    def _all_visits(self):
        settings = self.settings
        settings.set(settingkey.STARTING_UNLOCKS_SP, 2)
        settings.set(settingkey.STARTING_UNLOCKS_PR, 2)
        settings.set(settingkey.STARTING_UNLOCKS_TT, 3)
        settings.set(settingkey.STARTING_UNLOCKS_OC, 2)
        settings.set(settingkey.STARTING_UNLOCKS_HT, 2)
        settings.set(settingkey.STARTING_UNLOCKS_LOD, 2)
        settings.set(settingkey.STARTING_UNLOCKS_TWTNW, 2)
        settings.set(settingkey.STARTING_UNLOCKS_BC, 2)
        settings.set(settingkey.STARTING_UNLOCKS_AG, 2)
        settings.set(settingkey.STARTING_UNLOCKS_PL, 2)
        settings.set(settingkey.STARTING_UNLOCKS_HB, 2)
        settings.set(settingkey.STARTING_UNLOCKS_DC, 2)
        settings.set(settingkey.STARTING_UNLOCKS_STT, 1)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MIN, 0)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MAX, 0)
        self.update_widgets()

    def _starting_visit_random_value_changed(self):
        min_random = self.settings.get(settingkey.STARTING_VISIT_RANDOM_MIN)
        max_random = self.settings.get(settingkey.STARTING_VISIT_RANDOM_MAX)
        if min_random > max_random:
            self.settings.set(settingkey.STARTING_VISIT_RANDOM_MAX, min_random)
            self.update_widget(settingkey.STARTING_VISIT_RANDOM_MAX)

    def disable_widgets(self):
        self.disable_signal = True
        super().disable_widgets()
