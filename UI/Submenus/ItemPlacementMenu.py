from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.ItemList import Items
from UI.Submenus.SubMenu import KH2Submenu


class ItemPlacementMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Item Placement', settings=settings, in_layout='horizontal')
        self.disable_signal = False

        self.start_column()
        self.start_group()
        self.add_option(settingkey.ACCESSIBILITY)
        self.add_option(settingkey.SOFTLOCK_CHECKING)
        self.add_option(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        self.add_option(settingkey.NIGHTMARE_LOGIC)
        self.add_option(settingkey.YEET_THE_BEAR)
        self.end_group('General Item Settings')

        self.start_group()
        self.add_option(settingkey.CHAIN_LOGIC)
        self.add_option(settingkey.CHAIN_LOGIC_LENGTH)
        self.add_option(settingkey.CHAIN_LOGIC_TERRA)
        self.add_option(settingkey.CHAIN_LOGIC_MIN_TERRA)
        self.end_group('Chain Logic')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.DRIVE_CATEGORY)
        self.add_option(settingkey.MAGIC_CATEGORY)
        self.add_option(settingkey.OM_SC_CATEGORY)
        self.add_option(settingkey.PROOF_CATEGORY)
        self.add_option(settingkey.STORY_UNLOCK_CATEGORY)
        self.add_option(settingkey.SUMMON_CATEGORY)
        self.add_option(settingkey.TORN_PAGE_CATEGORY)
        self.end_group('Important Check Rarities')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.DRIVE_DEPTH)
        self.add_option(settingkey.MAGIC_DEPTH)
        self.add_option(settingkey.OM_SC_DEPTH)
        self.add_option(settingkey.PROOF_DEPTH)
        self.add_option(settingkey.STORY_UNLOCK_DEPTH)
        self.add_option(settingkey.SUMMON_DEPTH)
        self.add_option(settingkey.TORN_PAGE_DEPTH)
        self.end_group('Important Check Restrictions')
        self.end_column()
        

        self.finalizeMenu()

        settings.observe(settingkey.ITEM_PLACEMENT_DIFFICULTY, self.nightmare_checking)
        settings.observe(settingkey.ITEM_PLACEMENT_DIFFICULTY, self.key_item_weights)

    def nightmare_checking(self):
        placement_difficulty = self.settings.get(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        _, widget = self.widgets_and_settings_by_name[settingkey.NIGHTMARE_LOGIC]
        if not self.disable_signal:
            if placement_difficulty == "Nightmare":
                widget.setChecked(True)
                widget.setEnabled(False)
            else:
                widget.setEnabled(True)

    def key_item_weights(self):
        placement_difficulty = self.settings.get(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        _, widget = self.widgets_and_settings_by_name[settingkey.STORY_UNLOCK_CATEGORY]
        if not self.disable_signal:
            if placement_difficulty == "Normal":
                widget.setEnabled(False)
            else:
                widget.setEnabled(True)


    def disable_widgets(self):
        self.disable_signal = True
        super().disable_widgets()
