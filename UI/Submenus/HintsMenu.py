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
        self.end_column()

        self.finalizeMenu()

        settings.observe(settingkey.HINT_SYSTEM, self._hint_system_changed)

    def _hint_system_changed(self):
        hint_system = self.settings.get(settingkey.HINT_SYSTEM)
        self.set_option_visibility(settingkey.REPORT_DEPTH, visible=hint_system in ['JSmartee', 'Points'])
        self.set_option_visibility(settingkey.PREVENT_SELF_HINTING, visible=hint_system in ['JSmartee', 'Points'])
        self.set_option_visibility(settingkey.ALLOW_PROOF_HINTING, visible=hint_system == 'Points')
