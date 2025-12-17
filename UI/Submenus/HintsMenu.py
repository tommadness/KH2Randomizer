from PySide6.QtWidgets import QPushButton

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.configDict import HintType
from UI.Submenus.ProgressionPointsDialog import ProgressionPointsDialog
from UI.Submenus.SubMenu import KH2Submenu

_HINTABLE_ITEMS = "Hintable Items"
_ITEM_POINT_VALUES = "Item Point Values"
_MISC_POINT_VALUES = "Misc Point Values"
_PROGRESSION_POINTS = "Progression Points"
_SET_BONUSES = "Set Bonuses"
_SPOILED_ITEMS = "Spoiled Items"


class HintsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title="Hints", settings=settings)

        self.hint_system_warning_label = KH2Submenu.make_error_label(tooltip="")

        self.start_column()
        self.start_group()
        self.add_option(settingkey.HINT_SYSTEM, auxiliary_widget=self.hint_system_warning_label)
        self.add_option(settingkey.JOURNAL_HINTS_ABILITIES)
        self.add_option(settingkey.PROGRESSION_HINTS)
        self.configure_progression_points = QPushButton("Configure Progression Points")
        self.configure_progression_points.clicked.connect(self._configure_progression_points)
        self.pending_group.addWidget(self.configure_progression_points)
        self.add_option(settingkey.PROGRESSION_HINTS_REVEAL_END)
        self.add_option(settingkey.PROGRESSION_HINTS_COMPLETE_BONUS)
        self.add_option(settingkey.PROGRESSION_HINTS_REPORT_BONUS)
        self.add_option(settingkey.SCORE_MODE)
        self.add_option(settingkey.REPORTS_REVEAL)
        self.add_option(settingkey.PREVENT_SELF_HINTING)
        # self.add_option(settingkey.ALLOW_PROOF_HINTING)
        # self.add_option(settingkey.ALLOW_REPORT_HINTING)
        self.add_option(settingkey.REVEAL_COMPLETE)
        self.end_group()

        self.start_group()
        self.add_option(settingkey.HINTABLE_CHECKS)
        self.end_group(title="Trackable Items", group_id=_HINTABLE_ITEMS)
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.SPOILER_REVEAL_TYPES)
        self.end_group(title="Reports Reveal Items", group_id=_SPOILED_ITEMS)
        self.start_group()
        self.add_option(settingkey.POINTS_REPORT)
        self.add_option(settingkey.POINTS_PROOF)
        self.add_option(settingkey.POINTS_FORM)
        self.add_option(settingkey.POINTS_MAGIC)
        self.add_option(settingkey.POINTS_SUMMON)
        self.add_option(settingkey.POINTS_ABILITY)
        self.add_option(settingkey.POINTS_PAGE)
        self.add_option(settingkey.POINTS_VISIT)
        self.add_option(settingkey.POINTS_KEYBLADES)
        self.add_option(settingkey.POINTS_AUX)
        self.end_group(title="Item Point Values", group_id=_ITEM_POINT_VALUES)
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
        self.end_group(title="Set Bonuses", group_id=_SET_BONUSES)
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
        self.end_group(title="Misc Point Values", group_id=_MISC_POINT_VALUES)
        self.end_column()
        self.finalizeMenu()

        settings.observe(settingkey.HINT_SYSTEM, self._hint_system_changed)
        settings.observe(settingkey.SCORE_MODE, self._hint_system_changed)
        settings.observe(settingkey.PROGRESSION_HINTS, self._progression_toggle)
        settings.observe(settingkey.HINTABLE_CHECKS, self._trackable_items_changed)

    def _progression_toggle(self):
        progression_on = self.settings.get(settingkey.PROGRESSION_HINTS)

        self.configure_progression_points.setVisible(progression_on)
        self.set_option_visibility(settingkey.PROGRESSION_HINTS_COMPLETE_BONUS, visible=progression_on)
        self.set_option_visibility(settingkey.PROGRESSION_HINTS_REPORT_BONUS, visible=progression_on)
        self.set_option_visibility(settingkey.PROGRESSION_HINTS_REVEAL_END, visible=progression_on)

        self._check_hint_system_warnings()

    def _hint_system_changed(self):
        hint_type = HintType(self.settings.get(settingkey.HINT_SYSTEM))
        score_mode_enabled = self.settings.get(settingkey.SCORE_MODE)

        if hint_type == HintType.DISABLED:
            _, widget = self.widgets_and_settings_by_name[settingkey.PROGRESSION_HINTS]
            widget.setChecked(False)

        self.set_option_visibility(settingkey.PROGRESSION_HINTS, visible=hint_type != HintType.DISABLED)
        self.set_option_visibility(
            settingkey.PREVENT_SELF_HINTING,
            visible=hint_type in [HintType.JSMARTEE, HintType.POINTS, HintType.SPOILER],
        )

        self.set_group_visibility(
            group_id=_ITEM_POINT_VALUES,
            visible=score_mode_enabled or hint_type == HintType.POINTS
        )
        self.set_group_visibility(group_id=_SET_BONUSES, visible=score_mode_enabled)
        self.set_group_visibility(group_id=_MISC_POINT_VALUES, visible=score_mode_enabled)

        self.set_group_visibility(group_id=_HINTABLE_ITEMS, visible=hint_type != HintType.DISABLED)
        self.set_option_visibility(settingkey.REVEAL_COMPLETE, visible=hint_type == HintType.SPOILER)
        self.set_option_visibility(settingkey.REPORTS_REVEAL, visible=hint_type == HintType.SPOILER)
        self.set_group_visibility(
            group_id=_SPOILED_ITEMS,
            visible=hint_type == HintType.SPOILER or hint_type == HintType.POINTS
        )
        if hint_type != HintType.SPOILER:
            setting, widget = self.widgets_and_settings_by_name[settingkey.REPORTS_REVEAL]
            widget.setCurrentIndex(0)

        self._check_hint_system_warnings()

    def _trackable_items_changed(self):
        self._check_hint_system_warnings()

    def _configure_progression_points(self):
        dialog = ProgressionPointsDialog(self, self.settings)
        dialog.exec()

    def _check_hint_system_warnings(self):
        self.set_auxiliary_visibility(settingkey.HINT_SYSTEM, visible=False)

        hint_system = self.settings.get(settingkey.HINT_SYSTEM)
        if hint_system == HintType.JSMARTEE and not self.settings.get(settingkey.PROGRESSION_HINTS):
            if "report" not in self.settings.get(settingkey.HINTABLE_CHECKS):
                self.hint_system_warning_label.setToolTip(
                    "JSmartee hints require either Ansem Reports to be trackable, or that you use Progression Hint Mode."
                )
                self.set_auxiliary_visibility(settingkey.HINT_SYSTEM, visible=True)
