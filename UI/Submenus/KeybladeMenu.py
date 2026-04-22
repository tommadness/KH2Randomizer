from PySide6.QtGui import QAction
from PySide6.QtWidgets import QPushButton, QMenu

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.ItemList import Items
from UI.Submenus.SubMenu import KH2Submenu

_SUPPORT_ABILITIES_GROUP = "support_abilities"
_ACTION_ABILITIES_GROUP = "action_abilities"
_EQUIP_ABILITIES_GROUP = "equipment_abilities"

class KeybladeMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Equipment', settings=settings)

        self.start_column()
        self.start_group()
        self.add_option(settingkey.KEYBLADE_STATS_RANDOMIZED)
        self.add_option(settingkey.KEYBLADE_MIN_STAT)
        self.add_option(settingkey.KEYBLADE_MAX_STAT)
        self.end_group('Keyblade Statistics')

        self.start_group()
        self.add_option(settingkey.KEYBLADE_ABILITIES_RANDOMIZED)
        self.end_group("Keyblade Abilities")

        self.start_group()
        self.add_option(settingkey.ARMOR_ACCESSORY_ABILITIES)
        self.end_group("Armor/Accessory Abilities")
        self.end_column()

        self.start_column()
        self.start_group()
        self.set_group_widget(self._keyblade_support_abilities_presets_menu_button())
        self.add_option(settingkey.KEYBLADE_SUPPORT_ABILITIES)
        self.end_group("Support Keyblade Abilities", group_id=_SUPPORT_ABILITIES_GROUP)
        self.end_column(stretch_at_end=False)

        self.start_column()
        self.start_group()
        self.set_group_widget(self._keyblade_action_abilities_presets_menu_button())
        self.add_option(settingkey.KEYBLADE_ACTION_ABILITIES)
        self.end_group("Action Keyblade Abilities", group_id=_ACTION_ABILITIES_GROUP)
        self.end_column(stretch_at_end=False)

        self.start_column()
        self.start_group()
        self.set_group_widget(self._armor_accessory_abilities_presets_menu_button())
        self.add_option(settingkey.ARMOR_ACCESSORY_ABILITY_LIST)
        self.end_group("Armor/Accessory Abilities", group_id=_EQUIP_ABILITIES_GROUP)
        self.end_column(stretch_at_end=False)

        self.finalizeMenu()

        settings.observe(settingkey.KEYBLADE_STATS_RANDOMIZED, self._refresh_keyblade_stat_options)
        settings.observe(settingkey.KEYBLADE_ABILITIES_RANDOMIZED, self._refresh_keyblade_ability_options)
        settings.observe(settingkey.ARMOR_ACCESSORY_ABILITIES, self._refresh_equipment_ability_options)

    def toggle_all_items(self, setting_name: str, val: bool):
        setting, widget = self.widgets_and_settings_by_name[setting_name]
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

    def _keyblade_support_abilities_presets_menu_button(self) -> QPushButton:
        button = KH2Submenu.make_menu_button()
        menu = QMenu(button)

        select_all = QAction("Select All", menu)
        select_all.triggered.connect(lambda: self.toggle_all_items(settingkey.KEYBLADE_SUPPORT_ABILITIES, True))
        menu.addAction(select_all)

        select_none = QAction("Select None", menu)
        select_none.triggered.connect(lambda: self.toggle_all_items(settingkey.KEYBLADE_SUPPORT_ABILITIES, False))
        menu.addAction(select_none)

        button.setMenu(menu)
        return button

    def _keyblade_action_abilities_presets_menu_button(self) -> QPushButton:
        button = KH2Submenu.make_menu_button()
        menu = QMenu(button)

        select_all = QAction("Select All", menu)
        select_all.triggered.connect(lambda: self.toggle_all_items(settingkey.KEYBLADE_ACTION_ABILITIES, True))
        menu.addAction(select_all)

        select_none = QAction("Select None", menu)
        select_none.triggered.connect(lambda: self.toggle_all_items(settingkey.KEYBLADE_ACTION_ABILITIES, False))
        menu.addAction(select_none)

        button.setMenu(menu)
        return button

    def _refresh_equipment_ability_options(self):
        equipment_abilities_randomized = self.settings.get(settingkey.ARMOR_ACCESSORY_ABILITIES)
        self.set_group_visibility(_EQUIP_ABILITIES_GROUP, equipment_abilities_randomized)

    def _armor_accessory_abilities_presets_menu_button(self) -> QPushButton:
        button = KH2Submenu.make_menu_button()
        menu = QMenu(button)

        select_all = QAction("Select All", menu)
        select_all.triggered.connect(lambda: self.toggle_all_items(settingkey.ARMOR_ACCESSORY_ABILITY_LIST, True))
        menu.addAction(select_all)

        select_none = QAction("Select None", menu)
        select_none.triggered.connect(lambda: self.toggle_all_items(settingkey.ARMOR_ACCESSORY_ABILITY_LIST, False))
        menu.addAction(select_none)

        support_only = QAction("Support Only", menu)
        support_only.triggered.connect(self._armor_accessories_support_only)
        menu.addAction(support_only)

        button.setMenu(menu)
        return button

    def _armor_accessories_support_only(self):
        ability_ids = list(set([str(item.Id) for item in Items.equipment_eligible_support_abilities()]))
        self.settings.set(settingkey.ARMOR_ACCESSORY_ABILITY_LIST, ability_ids)
        self.update_widget(settingkey.ARMOR_ACCESSORY_ABILITY_LIST)
