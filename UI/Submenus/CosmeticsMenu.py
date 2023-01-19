import os
import textwrap

from PySide6.QtWidgets import QListWidget, QHBoxLayout, QPushButton, QFileDialog, QLabel

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

        self.add_option(settingkey.MUSIC_RANDO_ENABLED_PC)
        self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_ALL_KH2)
        self.add_option(settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES)

        self.music_count_text = QLabel()
        self.pending_group.addWidget(self.music_count_text)

        self.no_custom_music = QLabel(
            '\nCustom music folder not configured.\nUse the Configure menu to set up custom music.'
        )
        self.pending_group.addWidget(self.no_custom_music)

        self.open_custom_music_folder = QPushButton('Open custom music folder')
        self.open_custom_music_folder.clicked.connect(self._open_custom_music_folder)
        self.pending_group.addWidget(self.open_custom_music_folder)

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

        self.reload_music_widgets()
        self._reload_custom_list()
        add_button.clicked.connect(self._add_custom)
        remove_button.clicked.connect(self._remove_selected_custom)

    def _include_kh2_changed(self):
        self.reload_music_widgets()

    def reload_music_widgets(self):
        _, include_kh2_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_ALL_KH2]
        include_kh2_widget.setEnabled(CosmeticsMod.extracted_data_path() is not None)

        custom_music_configured = CosmeticsMod.read_custom_music_path() is not None
        self.no_custom_music.setVisible(not custom_music_configured)
        self.open_custom_music_folder.setVisible(custom_music_configured)

        self.music_count_text.setText(self._get_music_text())

    def _get_music_text(self):
        music_summary = CosmeticsMod.get_music_summary(self.settings)
        if len(music_summary) == 0:
            return 'No Music Found'
        else:
            label_text = 'Found Music\n'
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

    def _open_custom_music_folder(self):
        custom_music_path = CosmeticsMod.read_custom_music_path()
        if custom_music_path is not None:
            os.startfile(custom_music_path)
