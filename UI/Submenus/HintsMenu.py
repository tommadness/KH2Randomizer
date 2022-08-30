from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu
from PySide6.QtCore import Qt


class HintsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Hints', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_option(settingkey.HINT_SYSTEM)
        self.add_option(settingkey.EXTRA_ICS)
        self.add_option(settingkey.SCORE_MODE)
        self.add_option(settingkey.REPORT_DEPTH)
        self.add_option(settingkey.PREVENT_SELF_HINTING)
        self.add_option(settingkey.ALLOW_PROOF_HINTING)
        self.add_option(settingkey.ALLOW_REPORT_HINTING)
        self.add_option(settingkey.REVEAL_COMPLETE)
        self.add_option(settingkey.REVEAL_REPORTMODE)
        self.add_option(settingkey.REVEAL_TYPES)
        self.end_column()

        self.start_column()
        self.add_option(settingkey.POINTS_REPORT)
        self.add_option(settingkey.POINTS_PROOF)
        self.add_option(settingkey.POINTS_FORM)
        self.add_option(settingkey.POINTS_MAGIC)
        self.add_option(settingkey.POINTS_SUMMON)
        self.add_option(settingkey.POINTS_ABILITY)
        self.add_option(settingkey.POINTS_PAGE)
        self.add_option(settingkey.POINTS_VISIT)
        self.add_option(settingkey.POINTS_AUX)    
        self.end_column()

        self.start_column()
        self.add_option(settingkey.POINTS_BONUS)
        self.add_option(settingkey.POINTS_COMPLETE)
        self.add_option(settingkey.POINTS_FORMLV)
        self.add_option(settingkey.POINTS_BOSS_NORMAL)
        self.add_option(settingkey.POINTS_BOSS_FINAL)
        self.add_option(settingkey.POINTS_BOSS_AS)
        self.add_option(settingkey.POINTS_BOSS_DATA)
        self.add_option(settingkey.POINTS_BOSS_SEPHIROTH)
        self.add_option(settingkey.POINTS_BOSS_TERRA)
        self.add_option(settingkey.POINTS_DEATH)
        self.end_column()
        self.finalizeMenu()

        settings.observe(settingkey.HINT_SYSTEM, self._hint_system_changed)
        settings.observe(settingkey.REVEAL_REPORTMODE, self._reveal_report_mode_changed)
        settings.observe(settingkey.SCORE_MODE, self._hint_system_changed)

    def _hint_system_changed(self):
        hint_system = self.settings.get(settingkey.HINT_SYSTEM)
        score_mode_enabled = self.settings.get(settingkey.SCORE_MODE)
        # self.set_option_visibility(settingkey.REPORT_DEPTH, visible=hint_system in ['JSmartee', 'Points', 'Path'])
        self.set_option_visibility(settingkey.PREVENT_SELF_HINTING, visible=hint_system in ['JSmartee', 'Points', 'Spoiler'])
        self.set_option_visibility(settingkey.SCORE_MODE, visible=hint_system in ['JSmartee', 'Shananas', 'Spoiler', 'Path'])
        self.set_option_visibility(settingkey.ALLOW_PROOF_HINTING, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.ALLOW_REPORT_HINTING, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_PROOF, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_FORM, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_MAGIC, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_SUMMON, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_ABILITY, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_PAGE, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_REPORT, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_VISIT, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_AUX, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_BONUS, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_COMPLETE, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_FORMLV, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_BOSS_NORMAL, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_BOSS_AS, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_BOSS_DATA, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_BOSS_SEPHIROTH, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_BOSS_TERRA, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_BOSS_FINAL, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.POINTS_DEATH, visible=(hint_system == 'Points' or score_mode_enabled == True))
        self.set_option_visibility(settingkey.REVEAL_TYPES, visible=hint_system == 'Spoiler')
        self.set_option_visibility(settingkey.REVEAL_COMPLETE, visible=hint_system == 'Spoiler')
        self.set_option_visibility(settingkey.REVEAL_REPORTMODE, visible=hint_system == 'Spoiler')

    def _reveal_report_mode_changed(self):
        report_mode_enabled = self.settings.get(settingkey.REVEAL_REPORTMODE)
        setting, widget = self.widgets_and_settings_by_name[settingkey.REVEAL_TYPES]
        for selected in setting.choice_keys:
            if selected == "report":
                index = setting.choice_keys.index(selected)
                if not report_mode_enabled:
                    widget.item(index).setSelected(False)
                    widget.item(index).setFlags(Qt.NoItemFlags)
                else:
                    widget.item(index).setSelected(True)
                    widget.item(index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)