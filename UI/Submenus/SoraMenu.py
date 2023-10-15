from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class SoraMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='EXP/Stats', settings=settings)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.GLASS_CANNON)
        self.add_option(settingkey.SORA_AP)
        self.add_option(settingkey.DONALD_AP)
        self.add_option(settingkey.GOOFY_AP)
        self.end_group()
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.SORA_EXP_MULTIPLIER)
        self.add_option(settingkey.VALOR_EXP_MULTIPLIER)
        self.add_option(settingkey.WISDOM_EXP_MULTIPLIER)
        self.add_option(settingkey.LIMIT_EXP_MULTIPLIER)
        self.add_option(settingkey.MASTER_EXP_MULTIPLIER)
        self.add_option(settingkey.FINAL_EXP_MULTIPLIER)
        self.add_option(settingkey.SUMMON_EXP_MULTIPLIER)
        self.end_group('Experience Multipliers')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.SORA_EXP_CURVE)
        self.add_option(settingkey.VALOR_EXP_CURVE)
        self.add_option(settingkey.WISDOM_EXP_CURVE)
        self.add_option(settingkey.LIMIT_EXP_CURVE)
        self.add_option(settingkey.MASTER_EXP_CURVE)
        self.add_option(settingkey.FINAL_EXP_CURVE)
        self.add_option(settingkey.SUMMON_EXP_CURVE)
        self.end_group('Experience Curves')
        self.end_column()

        self.finalizeMenu()
