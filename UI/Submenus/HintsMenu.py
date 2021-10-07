from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


# TODO: Come up with a way to only show settings for the selected hint system
class HintsMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings):
        super().__init__(title='Hint Systems', settings=settings)

        self.add_option(settingkey.HINT_SYSTEM)
        self.add_option(settingkey.REPORT_DEPTH)
        self.add_option(settingkey.PREVENT_SELF_HINTING)
        self.add_option(settingkey.ALLOW_PROOF_HINTING)

        self.finalizeMenu()
