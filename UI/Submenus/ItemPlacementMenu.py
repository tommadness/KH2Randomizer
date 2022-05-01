from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu


class ItemPlacementMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Item Placement', settings=settings, in_layout='horizontal')

        self.start_column()
        self.add_option(settingkey.ENABLE_PROMISE_CHARM)
        self.add_option(settingkey.PUREBLOOD)
        self.add_option(settingkey.ABILITY_POOL)
        self.add_option(settingkey.REMOVE_MAPS)
        self.add_option(settingkey.REMOVE_RECIPES)
        self.end_column()
        self.start_column()
        self.add_option(settingkey.NIGHTMARE_LOGIC)
        self.add_option(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        self.add_option(settingkey.SOFTLOCK_CHECKING)
        self.add_option(settingkey.PROOF_DEPTH)
        self.add_option(settingkey.YEET_THE_BEAR)
        self.end_column()

        self.finalizeMenu()

        settings.observe(settingkey.ITEM_PLACEMENT_DIFFICULTY, self.nightmare_checking)

    def nightmare_checking(self):
        placement_difficulty = self.settings.get(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        _,widget = self.widgets_and_settings_by_name[settingkey.NIGHTMARE_LOGIC]
        if placement_difficulty == "Nightmare":
            widget.setChecked(True)
            widget.setEnabled(False)
        else:
            widget.setEnabled(True)
