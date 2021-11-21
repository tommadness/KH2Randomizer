from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class SoraMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Sora', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_option(settingkey.SORA_LEVELS)
        self.add_option(settingkey.FORM_LEVEL_REWARDS)
        self.add_option(settingkey.STATSANITY)
        self.end_column()

        self.start_column()
        self.addHeader('Experience Multipliers')
        self.add_option(settingkey.SORA_EXP_MULTIPLIER)
        self.add_option(settingkey.VALOR_EXP_MULTIPLIER)
        self.add_option(settingkey.WISDOM_EXP_MULTIPLIER)
        self.add_option(settingkey.LIMIT_EXP_MULTIPLIER)
        self.add_option(settingkey.MASTER_EXP_MULTIPLIER)
        self.add_option(settingkey.FINAL_EXP_MULTIPLIER)
        self.add_option(settingkey.SUMMON_EXP_MULTIPLIER)
        self.end_column()

        self.finalizeMenu()
