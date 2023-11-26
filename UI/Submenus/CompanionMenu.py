from genericpath import samefile
import textwrap
from typing import Callable

from PySide6.QtWidgets import QPushButton

from Class import seedSettings, settingkey
from Class.seedSettings import SeedSettings
from UI.Submenus.SubMenu import KH2Submenu
from UI.worker import CompanionZipWorker


class CompanionMenu(KH2Submenu):
    def __init__(self, settings: SeedSettings, seed_name_getter: Callable[[], str]):
        super().__init__(title='Companion Options', settings=settings)
        self.seed_name_getter = seed_name_getter

        self.start_column()
        self.start_group()
        self.add_option(settingkey.DONALD_DAMAGE_TOGGLE)
        self.add_option(settingkey.DONALD_MELEE_ATTACKS)
        self.add_option(settingkey.DONALD_FIRE)
        self.add_option(settingkey.DONALD_BLIZZARD)
        self.add_option(settingkey.DONALD_THUNDER)
        self.add_option(settingkey.DONALD_KILL_BOSS)
        self.end_group('Donald Damage and Knockback options')
        self.end_column()
        
        self.start_column()
        self.start_group()
        self.add_option(settingkey.GOOFY_DAMAGE_TOGGLE)
        self.add_option(settingkey.GOOFY_MELEE_ATTACKS)
        self.add_option(settingkey.GOOFY_BASH)
        self.add_option(settingkey.GOOFY_TURBO)
        self.add_option(settingkey.GOOFY_TORNADO)
        self.add_option(settingkey.GOOFY_KILL_BOSS)
        self.end_group('Goofy Damage and Knockback options')
        self.end_column()
        
        self.start_column()
        self.start_group()
        companion_mod_button = QPushButton('Generate Companion Mod (Any Platform)')
        companion_mod_tooltip = textwrap.dedent('''
        Generates an OpenKH mod that will contain changes to the companions as you selected above.
        ''').strip()
        companion_mod_button.setToolTip(companion_mod_tooltip)
        companion_mod_button.clicked.connect(lambda: self._make_companion_mod())
        self.pending_group.addWidget(companion_mod_button)
        self.end_group('Companion Mod Maker')
        self.end_column()
        
        self.finalizeMenu()
        
    def _make_companion_mod(self):
        worker = CompanionZipWorker(self, self.seed_name_getter(), self.settings)
        worker.generate_mod()