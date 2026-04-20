from PySide6.QtGui import QAction
from PySide6.QtWidgets import QPushButton, QMenu

from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class StartingMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Starting Inventory', settings=settings)

        self.start_column()

        self.start_group()
        self.set_group_widget(self._growth_presets_menu_button())
        self.add_option(settingkey.STARTING_GROWTH_HIGH_JUMP)
        self.add_option(settingkey.STARTING_GROWTH_QUICK_RUN)
        self.add_option(settingkey.STARTING_GROWTH_DODGE_ROLL)
        self.add_option(settingkey.STARTING_GROWTH_AERIAL_DODGE)
        self.add_option(settingkey.STARTING_GROWTH_GLIDE)
        self.add_option(settingkey.STARTING_GROWTH_RANDOM_MIN)
        self.add_option(settingkey.STARTING_GROWTH_RANDOM_MAX)
        self.end_group("Growth")

        self.start_group()
        self.set_group_widget(self._magic_presets_menu_button())
        self.add_option(settingkey.STARTING_MAGIC_FIRE)
        self.add_option(settingkey.STARTING_MAGIC_BLIZZARD)
        self.add_option(settingkey.STARTING_MAGIC_THUNDER)
        self.add_option(settingkey.STARTING_MAGIC_CURE)
        self.add_option(settingkey.STARTING_MAGIC_MAGNET)
        self.add_option(settingkey.STARTING_MAGIC_REFLECT)
        self.add_option(settingkey.STARTING_MAGIC_RANDOM_MIN)
        self.add_option(settingkey.STARTING_MAGIC_RANDOM_MAX)
        self.end_group("Magic")

        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STARTING_PAGES)
        self.add_option(settingkey.STARTING_REPORTS)
        self.add_option(settingkey.STARTING_ITEMS)
        self.end_group("Key Items")

        self.start_group()
        self.add_option(settingkey.STARTING_DRIVES)
        self.end_group("Summons / Drive Forms")
        self.end_column(stretch_at_end=False)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STARTING_KEYBLADES)
        self.end_group("Keyblades")
        self.end_column(stretch_at_end=False)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.AUTO_EQUIP_START_ABILITIES)
        self.add_option(settingkey.STARTING_ABILITIES)
        self.end_group("Abilities")
        self.end_column(stretch_at_end=False)

        self.finalizeMenu()

        settings.observe(settingkey.STARTING_GROWTH_RANDOM_MIN, self._starting_growth_random_value_changed)
        settings.observe(settingkey.STARTING_GROWTH_RANDOM_MAX, self._starting_growth_random_value_changed)
        settings.observe(settingkey.STARTING_MAGIC_RANDOM_MIN, self._starting_magic_random_value_changed)
        settings.observe(settingkey.STARTING_MAGIC_RANDOM_MAX, self._starting_magic_random_value_changed)

    def _growth_presets_menu_button(self) -> QPushButton:
        button = KH2Submenu.make_menu_button()
        menu = QMenu(button)

        none = QAction("None", menu)
        none.triggered.connect(lambda: self._growth_level(0))
        menu.addAction(none)

        one = QAction("All Level 1", menu)
        one.triggered.connect(lambda: self._growth_level(1))
        menu.addAction(one)

        two = QAction("All Level 2", menu)
        two.triggered.connect(lambda: self._growth_level(2))
        menu.addAction(two)

        three = QAction("All Level 3", menu)
        three.triggered.connect(lambda: self._growth_level(3))
        menu.addAction(three)

        four = QAction("All Level 4", menu)
        four.triggered.connect(lambda: self._growth_level(4))
        menu.addAction(four)

        button.setMenu(menu)
        return button

    def _growth_level(self, level: int):
        settings = self.settings
        settings.set(settingkey.STARTING_GROWTH_HIGH_JUMP, level)
        settings.set(settingkey.STARTING_GROWTH_QUICK_RUN, level)
        settings.set(settingkey.STARTING_GROWTH_DODGE_ROLL, level)
        settings.set(settingkey.STARTING_GROWTH_AERIAL_DODGE, level)
        settings.set(settingkey.STARTING_GROWTH_GLIDE, level)
        settings.set(settingkey.STARTING_GROWTH_RANDOM_MIN, 0)
        settings.set(settingkey.STARTING_GROWTH_RANDOM_MAX, 0)
        self.update_widgets()

    def _starting_growth_random_value_changed(self):
        min_random = self.settings.get(settingkey.STARTING_GROWTH_RANDOM_MIN)
        max_random = self.settings.get(settingkey.STARTING_GROWTH_RANDOM_MAX)
        if min_random > max_random:
            self.settings.set(settingkey.STARTING_GROWTH_RANDOM_MAX, min_random)
            self.update_widget(settingkey.STARTING_GROWTH_RANDOM_MAX)

    def _magic_presets_menu_button(self) -> QPushButton:
        button = KH2Submenu.make_menu_button()
        menu = QMenu(button)

        none = QAction("None", menu)
        none.triggered.connect(lambda: self._magic_level(0))
        menu.addAction(none)

        one = QAction("All Level 1", menu)
        one.triggered.connect(lambda: self._magic_level(1))
        menu.addAction(one)

        two = QAction("All Level 2", menu)
        two.triggered.connect(lambda: self._magic_level(2))
        menu.addAction(two)

        three = QAction("All Level 3", menu)
        three.triggered.connect(lambda: self._magic_level(3))
        menu.addAction(three)

        button.setMenu(menu)
        return button

    def _magic_level(self, level: int):
        settings = self.settings
        settings.set(settingkey.STARTING_MAGIC_FIRE, level)
        settings.set(settingkey.STARTING_MAGIC_BLIZZARD, level)
        settings.set(settingkey.STARTING_MAGIC_THUNDER, level)
        settings.set(settingkey.STARTING_MAGIC_CURE, level)
        settings.set(settingkey.STARTING_MAGIC_MAGNET, level)
        settings.set(settingkey.STARTING_MAGIC_REFLECT, level)
        settings.set(settingkey.STARTING_MAGIC_RANDOM_MIN, 0)
        settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, 0)
        self.update_widgets()

    def _starting_magic_random_value_changed(self):
        min_random = self.settings.get(settingkey.STARTING_MAGIC_RANDOM_MIN)
        max_random = self.settings.get(settingkey.STARTING_MAGIC_RANDOM_MAX)
        if min_random > max_random:
            self.settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, min_random)
            self.update_widget(settingkey.STARTING_MAGIC_RANDOM_MAX)
