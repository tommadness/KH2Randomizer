from ctypes import alignment
from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton,QSizePolicy

from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu

class StartingMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Starting Inventory', settings=settings, in_layout='horizontal')

        self.start_column()
        self.start_group()
        self.add_option(settingkey.AUTO_EQUIP_START_ABILITIES)
        self.add_option(settingkey.STARTING_REPORTS)
        self.add_option(settingkey.STARTING_MOVEMENT)
        self.end_group('Starting Inventory Options')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STARTING_INVENTORY)
        self.end_group('Starting Inventory')
        self.end_column(stretch_at_end=False)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STARTING_STORY_UNLOCKS)
        starting_locks_layout = QHBoxLayout()
        story_lock_widget = QWidget()
        story_lock_widget.setProperty('cssClass', 'layoutWidget')
        start_with_all = QPushButton("Start with All")
        start_with_none = QPushButton("Start with None")
        starting_locks_layout.addWidget(start_with_all)
        starting_locks_layout.addWidget(start_with_none)
        story_lock_widget.setLayout(starting_locks_layout)
        self._add_option_widget("", "", story_lock_widget)
        self.end_group('Starting World Key Items')
        self.end_column(stretch_at_end=False)

        self.finalizeMenu()

        start_with_all.clicked.connect(lambda: self.toggle_story_items(True))
        start_with_none.clicked.connect(lambda: self.toggle_story_items(False))

        
    def toggle_story_items(self,enabled):
        setting, widget = self.widgets_and_settings_by_name[settingkey.STARTING_STORY_UNLOCKS]
        for selected in setting.choice_keys:
            index = setting.choice_keys.index(selected)
            widget.item(index).setSelected(enabled)
