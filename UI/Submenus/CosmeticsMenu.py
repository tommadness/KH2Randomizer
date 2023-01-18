import os
import textwrap

from PySide6.QtWidgets import QListWidget, QHBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox

from Class import settingkey
from Class.seedSettings import SeedSettings
from Module.cosmetics import CustomCosmetics, CosmeticsMod
from UI.Submenus.SubMenu import KH2Submenu


class CosmeticsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings, custom_cosmetics: CustomCosmetics):
        super().__init__(title='Cosmetics', settings=settings, in_layout='horizontal')

        self.custom_cosmetics = custom_cosmetics

        self.start_column()
        self.start_group()
        self.add_option(settingkey.COMMAND_MENU)
        self.add_option(settingkey.COSTUME_RANDO)
        self.end_group('Visuals')
        self.end_column()

        self.start_column()
        self.start_group()

        self.music_count_text = QLabel(self._get_music_text())

        openkh_path = CosmeticsMod.read_openkh_path()
        if openkh_path is None:
            label = QLabel('OpenKH folder not configured. Use\nthe option in the Configure menu.')
            self.pending_group.addWidget(label)
        else:
            cosmetics_mod_path = CosmeticsMod.cosmetics_mod_path(openkh_path, create_if_missing=False)
            if cosmetics_mod_path is None:
                self.pending_group.addWidget(QLabel('Cosmetics mod not set up yet.'))
                button = QPushButton('Set up now')
                button.clicked.connect(self._set_up_mod)
                self.pending_group.addWidget(button)
            else:
                self.add_option(settingkey.MUSIC_RANDO_ENABLED_PC)
                self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_ALL_KH2)
                self.add_option(settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES)

                music_summary = CosmeticsMod.get_music_summary()
                if len(music_summary) == 0:
                    self.pending_group.addWidget(QLabel('(No Music Found)'))
                else:
                    self.pending_group.addWidget(self.music_count_text)

                open_mod_folder = QPushButton('Open mod folder')
                open_mod_folder.clicked.connect(lambda: self._open_mod_folder(cosmetics_mod_path))
                self.pending_group.addWidget(open_mod_folder)

        self.end_group('Music (PC Only)')
        self.end_column()

        self.start_column()
        self.start_group()

        custom_list = QListWidget()
        custom_list_tooltip = textwrap.dedent('''
        File(s) that will be executed every time a seed is generated. Used to integrate with external mods that require
        running a Randomize.exe file (or similar) to randomize their contents.
        ''').strip()
        custom_list.setToolTip(custom_list_tooltip)
        self.pending_group.addWidget(custom_list)
        self.custom_list = custom_list

        button_layout = QHBoxLayout()
        add_button = QPushButton('Add')
        remove_button = QPushButton('Remove')
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        self.pending_group.addLayout(button_layout)

        self.end_group('External Randomization Executables')
        self.end_column()

        self.finalizeMenu()
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_ALL_KH2, self._include_kh2_changed)

        self._reload_music_text()
        self._reload_custom_list()
        add_button.clicked.connect(self._add_custom)
        remove_button.clicked.connect(self._remove_selected_custom)

    def _include_kh2_changed(self):
        CosmeticsMod.include_kh2_music = self.settings.get(settingkey.MUSIC_RANDO_PC_INCLUDE_ALL_KH2)
        self._reload_music_text()

    def _reload_music_text(self):
        self.music_count_text.setText(self._get_music_text())

    def _get_music_text(self):
        label_text = 'Found Music\n'
        music_summary = CosmeticsMod.get_music_summary()
        for category, count in music_summary.items():
            label_text += '{} : {}\n'.format(category, count)
        return label_text

    def _reload_custom_list(self):
        self.custom_list.clear()
        for file in self.custom_cosmetics.external_executables:
            self.custom_list.addItem(file)

    def _add_custom(self):
        file_dialog = QFileDialog()
        outfile_name, _ = file_dialog.getOpenFileName(self, filter='Executables (*.exe *.bat)')
        if outfile_name != '':
            self.custom_cosmetics.add_custom_executable(outfile_name)
        self._reload_custom_list()

    def _remove_selected_custom(self):
        index = self.custom_list.currentRow()
        if index >= 0:
            self.custom_cosmetics.remove_at_index(index)
            self._reload_custom_list()

    def _set_up_mod(self):
        CosmeticsMod.bootstrap_mod()

        text = textwrap.dedent("""
Added "KH2 Randomizer Cosmetics" mod to OpenKH Mods Manager.
Turn on this mod in Mods Manager to enable randomized cosmetics.

Please restart to the seed generator to apply changes.
        """).strip()
        message = QMessageBox(text=text)
        message.setWindowTitle("KH2 Seed Generator")
        message.exec()

    def _open_mod_folder(self, cosmetics_mod_path):
        os.startfile(cosmetics_mod_path)
