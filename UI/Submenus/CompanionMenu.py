from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu

_JACK_SKELLINGTON = "Jack Skellington"
_PING_MULAN = "Ping Mulan"
_DONALD = "Donald"
_GOOFY = "Goofy"
_SIMBA = "Simba"
_TRON = "Tron"
_AURON = "Auron"
_RIKU = "Riku"
_JACK_SPARROW = "Jack Sparrow"
_BEAST = "Beast"
_ALADDIN = "Aladdin"

class CompanionMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title="Companions", settings=settings)
        
        self.start_column()
        self.start_group()
        self.add_option(settingkey.DONALD_AP)
        self.add_option(settingkey.GOOFY_AP)
        self.end_group("AP")
        self.start_group()
        self.add_option(settingkey.COMPANION_DAMAGE_TOGGLE)
        self.add_option(settingkey.COMPANION_KILL_BOSS)
        self.end_group("All Companions")
        self.start_group()
        self.add_option(settingkey.JACK_SKELLINGTON_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.JACK_SKELLINGTON_BLAZING_FURY_KNOCKBACK_TYPE)
        self.add_option(settingkey.JACK_SKELLINGTON_ICY_TERROR_KNOCKBACK_TYPE)
        self.add_option(settingkey.JACK_SKELLINGTON_BOLTS_OF_SORROW_KNOCKBACK_TYPE)
        self.end_group("Jack Skellington", group_id=_JACK_SKELLINGTON)
        self.start_group()
        self.add_option(settingkey.PING_MULAN_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.MULAN_MUSHU_FIRE_KNOCKBACK_TYPE)
        self.add_option(settingkey.MULAN_FLAMETONGUE_KNOCKBACK_TYPE)
        self.end_group("Ping/Mulan", group_id=_PING_MULAN)
        self.start_group()
        self.add_option(settingkey.JACK_SPARROW_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.JACK_SPARROW_NO_MERCY_KNOCKBACK_TYPE)
        self.add_option(settingkey.JACK_SPARROW_RAIN_STORM_KNOCKBACK_TYPE)
        self.add_option(settingkey.JACK_SPARROW_BONE_SMASH_KNOCKBACK_TYPE)
        self.end_group("Jack Sparrow", group_id=_JACK_SPARROW)
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.DONALD_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.DONALD_FIRE_KNOCKBACK_TYPE)
        self.add_option(settingkey.DONALD_BLIZZARD_KNOCKBACK_TYPE)
        self.add_option(settingkey.DONALD_THUNDER_KNOCKBACK_TYPE)
        self.end_group("Donald", group_id=_DONALD)
        self.start_group()
        self.add_option(settingkey.SIMBA_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.SIMBA_FIERCE_CLAW_KNOCKBACK_TYPE)
        self.add_option(settingkey.SIMBA_GROUNDSHAKER_KNOCKBACK_TYPE)
        self.end_group("Simba", group_id=_SIMBA)
        self.start_group()
        self.add_option(settingkey.BEAST_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.BEAST_SHOUT_KNOCKBACK_TYPE)
        self.add_option(settingkey.BEAST_RUSH_KNOCKBACK_TYPE)
        self.end_group("Beast", group_id=_BEAST)
        self.start_group()
        self.add_option(settingkey.RIKU_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.RIKU_DARK_AURA_KNOCKBACK_TYPE)
        self.add_option(settingkey.RIKU_DARK_SHIELD_KNOCKBACK_TYPE)
        self.end_group("Riku", group_id=_RIKU)
        self.start_group()
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.GOOFY_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.GOOFY_BASH_KNOCKBACK_TYPE)
        self.add_option(settingkey.GOOFY_TURBO_KNOCKBACK_TYPE)
        self.add_option(settingkey.GOOFY_TORNADO_KNOCKBACK_TYPE)
        self.end_group("Goofy", group_id=_GOOFY)
        self.start_group()
        self.add_option(settingkey.ALADDIN_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.ALADDIN_SLASH_FRENZY_KNOCKBACK_TYPE)
        self.add_option(settingkey.ALADDIN_QUICKPLAY_KNOCKBACK_TYPE)
        self.end_group("Aladdin", group_id=_ALADDIN)
        self.start_group()
        self.add_option(settingkey.TRON_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.TRON_SCOUTING_DISK_KNOCKBACK_TYPE)
        self.add_option(settingkey.TRON_PULSING_THUNDER_KNOCKBACK_TYPE)
        self.end_group("Tron", group_id=_TRON)
        self.start_group()
        self.add_option(settingkey.AURON_MELEE_ATTACKS_KNOCKBACK_TYPE)
        self.add_option(settingkey.AURON_DIVIDER_KNOCKBACK_TYPE)
        self.end_group("Auron", group_id=_AURON)
        self.end_column()
        
        settings.observe(settingkey.COMPANION_DAMAGE_TOGGLE, self._companions_changed)
        
        self.finalizeMenu()

    def _companions_changed(self):
        enabled = self.settings.get(settingkey.COMPANION_DAMAGE_TOGGLE)
        self.set_option_visibility(settingkey.COMPANION_KILL_BOSS, enabled)
        self.set_group_visibility(
            group_id=_JACK_SKELLINGTON, visible=enabled
        )
        self.set_group_visibility(
            group_id=_PING_MULAN, visible=enabled
        )
        self.set_group_visibility(
            group_id=_DONALD, visible=enabled
        )
        self.set_group_visibility(
            group_id=_GOOFY, visible=enabled
        )
        self.set_group_visibility(
            group_id=_RIKU, visible=enabled
        )
        self.set_group_visibility(
            group_id=_ALADDIN, visible=enabled
        )
        self.set_group_visibility(
            group_id=_AURON, visible=enabled
        )
        self.set_group_visibility(
            group_id=_SIMBA, visible=enabled
        )
        self.set_group_visibility(
            group_id=_JACK_SPARROW, visible=enabled
        )
        self.set_group_visibility(
            group_id=_BEAST, visible=enabled
        )
        self.set_group_visibility(
            group_id=_TRON, visible=enabled
        )
