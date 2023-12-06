from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class CompanionMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title="Companions", settings=settings)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.DONALD_DAMAGE_TOGGLE)
        self.add_option(settingkey.DONALD_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.DONALD_FIRE_KNOCKBACK_TYPE)
        self.add_option(settingkey.DONALD_BLIZZARD_KNOCKBACK_TYPE)
        self.add_option(settingkey.DONALD_THUNDER_KNOCKBACK_TYPE)
        self.add_option(settingkey.DONALD_KILL_BOSS)
        self.end_group("Donald")
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.GOOFY_DAMAGE_TOGGLE)
        self.add_option(settingkey.GOOFY_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.GOOFY_BASH_KNOCKBACK_TYPE)
        self.add_option(settingkey.GOOFY_TURBO_KNOCKBACK_TYPE)
        self.add_option(settingkey.GOOFY_TORNADO_KNOCKBACK_TYPE)
        self.add_option(settingkey.GOOFY_KILL_BOSS)
        self.end_group("Goofy")
        self.end_column()

        self.finalizeMenu()
