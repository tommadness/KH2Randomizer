from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class StartingMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Starting Inventory', settings=settings)

        self.start_column()

        self.start_group()
        self.add_option(settingkey.STARTING_GROWTH_HIGH_JUMP)
        self.add_option(settingkey.STARTING_GROWTH_QUICK_RUN)
        self.add_option(settingkey.STARTING_GROWTH_DODGE_ROLL)
        self.add_option(settingkey.STARTING_GROWTH_AERIAL_DODGE)
        self.add_option(settingkey.STARTING_GROWTH_GLIDE)
        self.add_option(settingkey.STARTING_GROWTH_RANDOM_MIN)
        self.add_option(settingkey.STARTING_GROWTH_RANDOM_MAX)
        self.end_group("Growth")

        self.start_group()
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

    def _starting_growth_random_value_changed(self):
        min_random = self.settings.get(settingkey.STARTING_GROWTH_RANDOM_MIN)
        max_random = self.settings.get(settingkey.STARTING_GROWTH_RANDOM_MAX)
        if min_random > max_random:
            self.settings.set(settingkey.STARTING_GROWTH_RANDOM_MAX, min_random)
            self.update_widget(settingkey.STARTING_GROWTH_RANDOM_MAX)

    def _starting_magic_random_value_changed(self):
        min_random = self.settings.get(settingkey.STARTING_MAGIC_RANDOM_MIN)
        max_random = self.settings.get(settingkey.STARTING_MAGIC_RANDOM_MAX)
        if min_random > max_random:
            self.settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, min_random)
            self.update_widget(settingkey.STARTING_MAGIC_RANDOM_MAX)
