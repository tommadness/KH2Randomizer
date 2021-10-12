from Class import seedSettings
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class BossEnemyMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title='Boss/Enemy', settings=settings)

        for setting in seedSettings.boss_enemy_settings:
            self.add_option(setting.name)

        self.finalizeMenu()
