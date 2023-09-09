from PySide6.QtCore import Qt

from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu

_HINTABLE_ITEMS = 'Hintable Items'
_ITEM_POINT_VALUES = 'Item Point Values'
_MISC_POINT_VALUES = 'Misc Point Values'
_PROGRESSION_POINTS = 'Progression Points'
_SET_BONUSES = 'Set Bonuses'
_SPOILED_ITEMS = 'Spoiled Items'


class HintsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Hints', settings=settings)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.HINT_SYSTEM)
        self.add_option(settingkey.REPORT_DEPTH)
        self.add_option(settingkey.PROGRESSION_HINTS)
        self.add_option(settingkey.PROGRESSION_HINTS_REVEAL_END)
        self.add_option(settingkey.PROGRESSION_HINTS_COMPLETE_BONUS)
        self.add_option(settingkey.PROGRESSION_HINTS_REPORT_BONUS)
        self.add_option(settingkey.SCORE_MODE)
        self.add_option(settingkey.REPORTS_REVEAL)
        self.add_option(settingkey.PREVENT_SELF_HINTING)
        self.add_option(settingkey.ALLOW_PROOF_HINTING)
        self.add_option(settingkey.ALLOW_REPORT_HINTING)
        self.add_option(settingkey.REVEAL_COMPLETE)
        self.end_group()

        self.start_group()
        self.add_option(settingkey.HINTABLE_CHECKS)
        self.end_group(title='Hintable Items', group_id=_HINTABLE_ITEMS)
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.POINTS_REPORT)
        self.add_option(settingkey.POINTS_PROOF)
        self.add_option(settingkey.POINTS_FORM)
        self.add_option(settingkey.POINTS_MAGIC)
        self.add_option(settingkey.POINTS_SUMMON)
        self.add_option(settingkey.POINTS_ABILITY)
        self.add_option(settingkey.POINTS_PAGE)
        self.add_option(settingkey.POINTS_VISIT)
        self.add_option(settingkey.POINTS_AUX)
        self.end_group(title='Item Point Values', group_id=_ITEM_POINT_VALUES)

        self.start_group()
        self.add_option(settingkey.PROGRESSION_POINT_SELECT)
        self.end_group(title='Progression Points', group_id=_PROGRESSION_POINTS)
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.POINTS_REPORT_COLLECT)
        self.add_option(settingkey.POINTS_PROOF_COLLECT)
        self.add_option(settingkey.POINTS_FORM_COLLECT)
        self.add_option(settingkey.POINTS_MAGIC_COLLECT)
        self.add_option(settingkey.POINTS_SUMMON_COLLECT)
        self.add_option(settingkey.POINTS_ABILITY_COLLECT)
        self.add_option(settingkey.POINTS_PAGE_COLLECT)
        self.add_option(settingkey.POINTS_VISIT_COLLECT)
        self.add_option(settingkey.POINTS_POUCHES_COLLECT)
        self.end_group(title='Set Bonuses', group_id=_SET_BONUSES)
        self.start_group()
        self.add_option(settingkey.SPOILER_REVEAL_TYPES)
        self.end_group(title='Spoiled Items', group_id=_SPOILED_ITEMS)
        self.end_column()

        self.start_column()
        self.start_group()
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
        self.end_group(title='Misc Point Values', group_id=_MISC_POINT_VALUES)
        self.end_column()
        self.finalizeMenu()

        settings.observe(settingkey.HINT_SYSTEM, self._hint_system_changed)
        settings.observe(settingkey.SCORE_MODE, self._hint_system_changed)
        settings.observe(settingkey.PROGRESSION_HINTS, self._progression_toggle)

    def _progression_toggle(self):
        progression_on = self.settings.get(settingkey.PROGRESSION_HINTS)

        self.set_option_visibility(settingkey.PROGRESSION_HINTS_COMPLETE_BONUS, visible=progression_on)
        self.set_option_visibility(settingkey.PROGRESSION_HINTS_REPORT_BONUS, visible=progression_on)
        self.set_option_visibility(settingkey.PROGRESSION_HINTS_REVEAL_END, visible=progression_on)
        self.set_group_visibility(group_id=_PROGRESSION_POINTS, visible=progression_on)

    def _hint_system_changed(self):
        hint_system = self.settings.get(settingkey.HINT_SYSTEM)
        score_mode_enabled = hint_system == 'Points' or self.settings.get(settingkey.SCORE_MODE)
        progression_points = self.settings.get(settingkey.PROGRESSION_HINTS)

        if hint_system == 'Disabled':
            _, widget = self.widgets_and_settings_by_name[settingkey.PROGRESSION_HINTS]
            widget.setChecked(False)

        # self.set_option_visibility(settingkey.REPORT_DEPTH, visible=hint_system in ['JSmartee', 'Points', 'Path'])
        self.set_option_visibility(settingkey.PROGRESSION_HINTS, visible=hint_system != 'Disabled')
        self.set_option_visibility(settingkey.PREVENT_SELF_HINTING, visible=hint_system in ['JSmartee', 'Points', 'Spoiler'])
        self.set_option_visibility(settingkey.SCORE_MODE, visible=hint_system in ['JSmartee', 'Shananas', 'Spoiler', 'Path'])
        self.set_option_visibility(settingkey.ALLOW_PROOF_HINTING, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.ALLOW_REPORT_HINTING, visible=hint_system == 'Points')

        self.set_group_visibility(group_id=_ITEM_POINT_VALUES, visible=score_mode_enabled)
        self.set_group_visibility(group_id=_SET_BONUSES, visible=score_mode_enabled)
        self.set_group_visibility(group_id=_MISC_POINT_VALUES, visible=score_mode_enabled)

        self.set_group_visibility(group_id=_HINTABLE_ITEMS, visible=hint_system != 'Disabled')
        self.set_option_visibility(settingkey.REVEAL_COMPLETE, visible=hint_system == 'Spoiler')
        self.set_option_visibility(settingkey.REPORTS_REVEAL, visible=hint_system == 'Spoiler')
        self.set_group_visibility(group_id=_SPOILED_ITEMS, visible=hint_system == 'Spoiler')
        if hint_system != "Spoiler":
            setting, widget = self.widgets_and_settings_by_name[settingkey.REPORTS_REVEAL]
            widget.setCurrentIndex(0)
        if hint_system in ['JSmartee', 'Points', 'Spoiler', 'Path'] and not progression_points:
            setting, widget = self.widgets_and_settings_by_name[settingkey.HINTABLE_CHECKS]
            for selected in setting.choice_keys:
                if selected == "report":
                    index = setting.choice_keys.index(selected)
                    widget.item(index).setSelected(True)
                    widget.item(index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
