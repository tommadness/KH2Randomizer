from Class import settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu
from PySide6.QtWidgets import (QPushButton,QHBoxLayout,QWidget)

_SUPPORT_ABILITIES_GROUP = "support_abilities"
_ACTION_ABILITIES_GROUP = "action_abilities"

class KeybladeMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Keyblades', settings=settings)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.KEYBLADE_STATS_RANDOMIZED)
        self.add_option(settingkey.KEYBLADE_MIN_STAT)
        self.add_option(settingkey.KEYBLADE_MAX_STAT)
        self.end_group('Keyblade Statistics')

        self.start_group()
        self.add_option(settingkey.KEYBLADE_ABILITIES_RANDOMIZED)
        self.end_group("Keyblade Abilities")
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.KEYBLADE_SUPPORT_ABILITIES)
        support_widget_layout = QHBoxLayout()
        support_widget = QWidget()
        support_widget.setProperty('cssClass', 'layoutWidget')
        support_widget.setLayout(support_widget_layout)
        select_no_support_button = QPushButton("Select No Support")
        select_all_support_button = QPushButton("Select All Support")
        support_widget_layout.addWidget(select_no_support_button)
        support_widget_layout.addWidget(select_all_support_button)
        self._add_option_widget("","",support_widget)
        self.end_group("Support Keyblade-Eligible Abilities", group_id=_SUPPORT_ABILITIES_GROUP)
        self.end_column(stretch_at_end=False)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.KEYBLADE_ACTION_ABILITIES)
        action_widget_layout = QHBoxLayout()
        action_widget = QWidget()
        action_widget.setProperty('cssClass', 'layoutWidget')
        action_widget.setLayout(action_widget_layout)
        select_no_action_button = QPushButton("Select No Action")
        select_all_action_button = QPushButton("Select All Action")
        action_widget_layout.addWidget(select_no_action_button)
        action_widget_layout.addWidget(select_all_action_button)
        self._add_option_widget("","",action_widget)
        self.end_group("Action Keyblade-Eligible Abilities", group_id=_ACTION_ABILITIES_GROUP)
        self.end_column(stretch_at_end=False)

        select_no_support_button.clicked.connect(lambda: self.toggle_all_items(settingkey.KEYBLADE_SUPPORT_ABILITIES,False))
        select_all_support_button.clicked.connect(lambda: self.toggle_all_items(settingkey.KEYBLADE_SUPPORT_ABILITIES,True))

        select_no_action_button.clicked.connect(lambda: self.toggle_all_items(settingkey.KEYBLADE_ACTION_ABILITIES,False))
        select_all_action_button.clicked.connect(lambda: self.toggle_all_items(settingkey.KEYBLADE_ACTION_ABILITIES,True))

        self.finalizeMenu()

        settings.observe(settingkey.KEYBLADE_STATS_RANDOMIZED, self._refresh_keyblade_stat_options)
        settings.observe(settingkey.KEYBLADE_ABILITIES_RANDOMIZED, self._refresh_keyblade_ability_options)

    def toggle_all_items(self,setting_name,val):
        setting,widget = self.widgets_and_settings_by_name[setting_name]
        for selected in setting.choice_keys:
            index = setting.choice_keys.index(selected)
            widget.item(index).setSelected(val)

    def _refresh_keyblade_stat_options(self):
        keyblade_stats_randomized = self.settings.get(settingkey.KEYBLADE_STATS_RANDOMIZED)
        self.set_option_visibility(settingkey.KEYBLADE_MIN_STAT, keyblade_stats_randomized)
        self.set_option_visibility(settingkey.KEYBLADE_MAX_STAT, keyblade_stats_randomized)

    def _refresh_keyblade_ability_options(self):
        keyblade_abilities_randomized = self.settings.get(settingkey.KEYBLADE_ABILITIES_RANDOMIZED)
        self.set_group_visibility(_SUPPORT_ABILITIES_GROUP, keyblade_abilities_randomized)
        self.set_group_visibility(_ACTION_ABILITIES_GROUP, keyblade_abilities_randomized)
