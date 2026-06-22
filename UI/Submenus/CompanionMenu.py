from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu

_ATTACK_DATA_PARAMS = "ATTACK_DATA_PARAMS"

class CompanionMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title="Companions / Attack Data", settings=settings)
        
        self.start_column()
        self.start_group()
        self.add_option(settingkey.DONALD_AP)
        self.add_option(settingkey.GOOFY_AP)
        self.end_group("AP")
        self.start_group()
        self.add_option(settingkey.ATTACK_DATA_RANDOMIZATION)
        self.end_group("Attack Data Randomization")
        self.start_group()
        self.add_option(settingkey.COMPANION_DAMAGE_TOGGLE)
        self.add_option(settingkey.COMPANION_KILL_BOSS)
        self.add_option(settingkey.ATTACK_DATA_DAMAGE_PRESET)
        self.add_option(settingkey.ATTACK_DATA_ELEMENT)
        self.add_option(settingkey.EXCLUDE_SORA_ROXAS_BASE_ATTACK)
        self.add_option(settingkey.ATTACK_DATA_KNOCKBACK_AMOUNT_PRESET)
        self.add_option(settingkey.ATTACK_DATA_MULTI_HIT_PRESET)
        self.add_option(settingkey.ATTACK_DATA_REVENGE_VALUE_PRESET)
        self.end_group("Attack Data Randomization Parameters", group_id = _ATTACK_DATA_PARAMS)
        self.end_column()
        
        settings.observe(settingkey.ATTACK_DATA_RANDOMIZATION, self._attack_data_randomized)
        settings.observe(settingkey.EXCLUDE_SORA_ROXAS_BASE_ATTACK, self._element_randomization_on)
        
        self.set_group_visibility("Attack Data Randomization", True)
        self.finalizeMenu()

    def _attack_data_randomized(self):
        enabled = self.settings.get(settingkey.ATTACK_DATA_RANDOMIZATION)
        self.set_group_visibility(
            group_id=_ATTACK_DATA_PARAMS, visible=enabled
        )

    def _element_randomization_on(self):
        enabled = self.settings.get(settingkey.ATTACK_DATA_ELEMENT)
        self.set_option_visibility(settingkey.EXCLUDE_SORA_ROXAS_BASE_ATTACK, enabled)