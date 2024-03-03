from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton

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
        self.add_option(settingkey.FIFTY_AP_BOOSTS)
        self.add_option(settingkey.ENABLE_PROMISE_CHARM)
        self.add_option(settingkey.PROMISE_CHARM_DEPTH)
        # self.add_option(settingkey.PUREBLOOD)
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
        self.end_group('Randomized Shop')

        self.start_group()
        self.add_option(settingkey.SHOP_KEYBLADES)
        self.add_option(settingkey.SHOP_ELIXIRS)
        self.add_option(settingkey.SHOP_RECOVERIES)
        self.add_option(settingkey.SHOP_BOOSTS)
        self.end_group('Guaranteed Shop Items')
        self.end_column(stretch_at_end=True)

        
        self.start_column()
        self.start_group()
        self.add_option(settingkey.JUNK_ITEMS)

        junk_widget_layout = QHBoxLayout()
        junk_widget = QWidget()
        junk_widget.setProperty('cssClass', 'layoutWidget')
        junk_widget.setLayout(junk_widget_layout)
        select_all_junk = QPushButton("Select All")
        select_better_junk = QPushButton("No Synth")
        junk_widget_layout.addWidget(select_all_junk)
        junk_widget_layout.addWidget(select_better_junk)
        self._add_option_widget("", "", junk_widget)
        self.end_group('Junk Items')
        self.end_column(stretch_at_end=False)
        select_all_junk.clicked.connect(lambda: self.toggle_all_items())
        select_better_junk.clicked.connect(lambda: self.toggle_better_junk())

        self.finalizeMenu()

        settings.observe(settingkey.ENABLE_PROMISE_CHARM, self.promise_charm_enabled)

    def promise_charm_enabled(self):
        promise_charm_toggle = self.settings.get(settingkey.ENABLE_PROMISE_CHARM)
        _, widget = self.widgets_and_settings_by_name[settingkey.PROMISE_CHARM_DEPTH]
        if not self.disable_signal:
            widget.setEnabled(promise_charm_toggle)

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
