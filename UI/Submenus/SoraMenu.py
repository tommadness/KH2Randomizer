from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class SoraMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='EXP/Stats', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_option(settingkey.GLASS_CANNON)
        self.add_option(settingkey.SORA_AP)
        self.add_option(settingkey.DONALD_AP)
        self.add_option(settingkey.GOOFY_AP)
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

        self.start_column()
        self.addHeader('Experience Curves')
        self.add_option(settingkey.SORA_EXP_CURVE)
        self.add_option(settingkey.VALOR_EXP_CURVE)
        self.add_option(settingkey.WISDOM_EXP_CURVE)
        self.add_option(settingkey.LIMIT_EXP_CURVE)
        self.add_option(settingkey.MASTER_EXP_CURVE)
        self.add_option(settingkey.FINAL_EXP_CURVE)
        self.add_option(settingkey.SUMMON_EXP_CURVE)
        self.end_column()

        self.finalizeMenu()