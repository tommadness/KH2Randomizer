from Class import seedSettings
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class BossEnemyMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Boss/Enemy', settings=settings, in_layout='horizontal')

        self.start_column()
        self.start_group()
        for setting in seedSettings.boss_settings:
            self.add_option(setting.name)
        self.end_group('Bosses')
        self.end_column()

        self.start_column()
        self.start_group()
        for setting in seedSettings.enemy_settings:
            self.add_option(setting.name)
        self.end_group('Enemies')
        self.end_column()

        self.finalizeMenu()
