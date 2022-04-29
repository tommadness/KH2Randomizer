from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class HintsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Hints', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_option(settingkey.HINT_SYSTEM)
        self.add_option(settingkey.REPORT_DEPTH)
        self.add_option(settingkey.PREVENT_SELF_HINTING)
        self.add_option(settingkey.ALLOW_PROOF_HINTING)
        self.add_option(settingkey.ALLOW_REPORT_HINTING)
        self.end_column()

        self.start_column()
        self.add_option(settingkey.POINTS_PROOF)
        self.add_option(settingkey.POINTS_FORM)
        self.add_option(settingkey.POINTS_MAGIC)
        self.add_option(settingkey.POINTS_SUMMON)
        self.add_option(settingkey.POINTS_ABILITY)
        self.add_option(settingkey.POINTS_PAGE)
        self.add_option(settingkey.POINTS_VISIT)
        self.add_option(settingkey.POINTS_REPORT)
        self.end_column()

        self.start_column()
        self.add_option(settingkey.POINTS_BONUS)
        self.add_option(settingkey.POINTS_COMPLETE)
        self.add_option(settingkey.POINTS_FORMLV)
        self.end_column()
        self.finalizeMenu()

        settings.observe(settingkey.HINT_SYSTEM, self._hint_system_changed)

    def _hint_system_changed(self):
        hint_system = self.settings.get(settingkey.HINT_SYSTEM)
        self.set_option_visibility(settingkey.REPORT_DEPTH, visible=hint_system in ['JSmartee', 'Points', 'Path'])
        self.set_option_visibility(settingkey.PREVENT_SELF_HINTING, visible=hint_system in ['JSmartee', 'Points'])
        self.set_option_visibility(settingkey.ALLOW_PROOF_HINTING, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.ALLOW_REPORT_HINTING, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_PROOF, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_FORM, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_MAGIC, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_SUMMON, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_ABILITY, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_PAGE, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_REPORT, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_VISIT, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_BONUS, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_COMPLETE, visible=hint_system == 'Points')
        self.set_option_visibility(settingkey.POINTS_FORMLV, visible=hint_system == 'Points')
