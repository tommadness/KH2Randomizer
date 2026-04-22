from PySide6.QtGui import QAction
from PySide6.QtWidgets import QPushButton, QMenu

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.ItemList import Items
from UI.Submenus.SubMenu import KH2Submenu


class ItemPoolMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings):
        super().__init__(title='Item Pool', settings=settings)
        self.disable_signal = False

        self.start_column()
        self.start_group()
        self.add_option(settingkey.STATSANITY)
        self.add_option(settingkey.NUM_HP_BONUSES)
        self.add_option(settingkey.NUM_MP_BONUSES)
        self.add_option(settingkey.NUM_DRIVE_BONUSES)
        self.add_option(settingkey.NUM_ACCESSORY_SLOT_BONUSES)
        self.add_option(settingkey.NUM_ARMOR_SLOT_BONUSES)
        self.add_option(settingkey.NUM_ITEM_SLOT_BONUSES)
        self.add_option(settingkey.FIFTY_AP_BOOSTS)
        self.add_option(settingkey.ENABLE_PROMISE_CHARM)
        self.add_option(settingkey.ANTIFORM)
        self.add_option(settingkey.MAPS_IN_ITEM_POOL)
        self.add_option(settingkey.RECIPES_IN_ITEM_POOL)
        self.add_option(settingkey.ACCESSORIES_IN_ITEM_POOL)
        self.add_option(settingkey.ARMOR_IN_ITEM_POOL)
        self.add_option(settingkey.MUNNY_IN_ITEM_POOL)
        self.add_option(settingkey.ABILITY_POOL)
        self.end_group('Include in Item Pool')
        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.SHOP_UNLOCKS)
        self.add_option(settingkey.SHOP_REPORTS)
        self.add_option(settingkey.SHOP_PRICE_VISIT_UNLOCKS)
        self.add_option(settingkey.SHOP_PRICE_REPORT)
        self.end_group('Randomized Shop')

        self.start_group()
        self.add_option(settingkey.SHOP_KEYBLADES)
        self.add_option(settingkey.SHOP_ELIXIRS)
        self.add_option(settingkey.SHOP_RECOVERIES)
        self.add_option(settingkey.SHOP_BOOSTS)
        
        self.add_option(settingkey.SHOP_PRICE_KEYBLADE)
        self.add_option(settingkey.SHOP_PRICE_ELIXIR)
        self.add_option(settingkey.SHOP_PRICE_MEGALIXIR)
        self.add_option(settingkey.SHOP_PRICE_DRIVE_RECOVERY)
        self.add_option(settingkey.SHOP_PRICE_HI_DRIVE_RECOVERY)
        self.add_option(settingkey.SHOP_PRICE_AP_BOOST)
        self.add_option(settingkey.SHOP_PRICE_POWER_BOOST)
        self.add_option(settingkey.SHOP_PRICE_MAGIC_BOOST)
        self.add_option(settingkey.SHOP_PRICE_DEFENSE_BOOST)
        self.end_group('Guaranteed Shop Items')
        self.end_column(stretch_at_end=True)

        self.start_column()
        self.start_group()
        self.set_group_widget(self._junk_presets_menu_button())
        self.add_option(settingkey.JUNK_ITEMS)
        self.end_group('Junk Items')
        self.end_column(stretch_at_end=False)

        settings.observe(settingkey.STATSANITY, self._statsanity_changed)
        
        self.finalizeMenu()

    def _statsanity_changed(self):
        enabled = self.settings.get(settingkey.STATSANITY)
        self.set_option_visibility(settingkey.NUM_HP_BONUSES, enabled)
        self.set_option_visibility(settingkey.NUM_MP_BONUSES, enabled)
        self.set_option_visibility(settingkey.NUM_DRIVE_BONUSES, enabled)
        self.set_option_visibility(settingkey.NUM_ACCESSORY_SLOT_BONUSES, enabled)
        self.set_option_visibility(settingkey.NUM_ARMOR_SLOT_BONUSES, enabled)
        self.set_option_visibility(settingkey.NUM_ITEM_SLOT_BONUSES, enabled)

    def _junk_presets_menu_button(self) -> QPushButton:
        button = KH2Submenu.make_menu_button()
        menu = QMenu(button)

        all_items = QAction("Select All", menu)
        all_items.triggered.connect(self.toggle_all_items)
        menu.addAction(all_items)

        better_junk = QAction("No Synthesis Items", menu)
        better_junk.triggered.connect(self.toggle_better_junk)
        menu.addAction(better_junk)

        button.setMenu(menu)
        return button

    def toggle_all_items(self):
        setting, widget = self.widgets_and_settings_by_name[settingkey.JUNK_ITEMS]
        for selected in setting.choice_keys:
            index = setting.choice_keys.index(selected)
            widget.item(index).setSelected(True)

    def toggle_better_junk(self):
        betterJunk = [
            int(elem.Id) for elem in Items.getJunkList(True)
        ]
        setting, widget = self.widgets_and_settings_by_name[settingkey.JUNK_ITEMS]
        for selected in setting.choice_keys:
            index = setting.choice_keys.index(selected)
            widget.item(index).setSelected(int(selected) in betterJunk)

    def disable_widgets(self):
        self.disable_signal = True
        super().disable_widgets()
