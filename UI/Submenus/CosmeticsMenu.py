import os
import textwrap

from PySide6.QtWidgets import QListWidget, QHBoxLayout, QPushButton, QFileDialog, QLabel

from Class import settingkey
from Class.seedSettings import SeedSettings, ExtraConfigurationData
from List import configDict
from Module import appconfig
from Module.cosmetics import CustomCosmetics, CosmeticsMod
from UI.Submenus.SubMenu import KH2Submenu
from UI.Submenus.TextureRecolorSettingsDialog import TextureRecolorSettingsDialog
from UI.worker import CosmeticsZipWorker


class CosmeticsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings, custom_cosmetics: CustomCosmetics):
        super().__init__(title='Cosmetics', settings=settings)

        self.custom_cosmetics = custom_cosmetics

        self.start_column()
        self.start_group()
        self.add_option(settingkey.COMMAND_MENU)
        # self.add_option(settingkey.COSTUME_RANDO)
        self.end_group('Visuals')

        self.start_group()
        self.add_option(settingkey.RANDO_THEMED_TEXTURES)
        self.add_option(settingkey.ITEMPIC_RANDO)
        self.add_option(settingkey.ROOM_TRANSITION_IMAGES)
        self.add_option(settingkey.ENDPIC_RANDO)

        self.add_option(settingkey.RECOLOR_TEXTURES)
        self.configure_recolors = QPushButton("Texture Recolor Settings")
        self.configure_recolors.clicked.connect(self._configure_recolors)
        self.pending_group.addWidget(self.configure_recolors)

        self.end_group("Visuals (PC Panacea Only)")

        self.start_group()
        self.add_option(settingkey.KEYBLADE_RANDO)
        self.add_option(settingkey.KEYBLADE_RANDO_INCLUDE_EFFECTS)
        self.add_option(settingkey.KEYBLADE_RANDO_ALLOW_DUPLICATES)
        self.keyblade_count_text = QLabel()
        self.pending_group.addWidget(self.keyblade_count_text)
        self.open_custom_keyblades_folder = QPushButton("Open custom keyblades folder")
        self.open_custom_keyblades_folder.clicked.connect(self._open_custom_keyblades_folder)
        self.pending_group.addWidget(self.open_custom_keyblades_folder)
        self.end_group("Keyblades (PC Only)")

        self.end_column()

        self.start_column()
        self.start_group()

        self.add_option(settingkey.MUSIC_RANDO_ENABLED_PC)
        self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_KH1)
        self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_KH2)
        self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM)
        self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_BBS)
        self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_DDD)
        self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM)
        self.add_option(settingkey.MUSIC_RANDO_PC_DMCA_SAFE)
        self.add_option(settingkey.MUSIC_RANDO_PC_USE_CATEGORIES)
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

        self.start_group()
        cosmetics_mod_button = QPushButton('Generate Cosmetics-Only Mod (PC)')
        cosmetics_mod_tooltip = textwrap.dedent('''
        Generates an OpenKH mod that ONLY randomizes cosmetics. Can be useful if using a seed generated outside of this
        generator (using Archipelago.gg or otherwise).
        ''').strip()
        cosmetics_mod_button.setToolTip(cosmetics_mod_tooltip)
        cosmetics_mod_button.clicked.connect(self._make_cosmetics_only_mod)
        self.pending_group.addWidget(cosmetics_mod_button)
        self.end_group('Cosmetics-Only Mod')
        self.end_column()

        self.finalizeMenu()

        settings.observe(settingkey.RECOLOR_TEXTURES, self._recolor_enabled_changed)
        settings.observe(settingkey.KEYBLADE_RANDO, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_ENABLED_PC, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_KH1, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_KH2, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_BBS, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_DDD, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_DMCA_SAFE, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_USE_CATEGORIES, self.reload_cosmetic_widgets)

        self.reload_cosmetic_widgets()
        self._reload_custom_executables_list()
        add_button.clicked.connect(self._add_custom_executable)
        remove_button.clicked.connect(self._remove_selected_custom_executable)

    def reload_cosmetic_widgets(self):
        _, recolor_textures_widget = self.widgets_and_settings_by_name[settingkey.RECOLOR_TEXTURES]

        _, include_kh1_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_KH1]
        _, include_kh2_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_KH2]
        _, include_recom_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM]
        _, include_bbs_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_BBS]
        _, include_ddd_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_DDD]
        _, include_custom_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM]

        keyblade_rando_setting = self.settings.get(settingkey.KEYBLADE_RANDO)
        keyblade_rando_enabled = keyblade_rando_setting != configDict.VANILLA
        music_rando_enabled = self.settings.get(settingkey.MUSIC_RANDO_ENABLED_PC)

        self.set_option_visibility(settingkey.KEYBLADE_RANDO_ALLOW_DUPLICATES, visible=keyblade_rando_enabled)
        self.set_option_visibility(settingkey.KEYBLADE_RANDO_INCLUDE_EFFECTS, visible=keyblade_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_KH1, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_KH2, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_BBS, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_DDD, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_USE_CATEGORIES, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_DMCA_SAFE, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES, visible=music_rando_enabled)

        extracted_data_path = appconfig.extracted_data_path()
        if extracted_data_path is None:
            recolor_textures_widget.setEnabled(False)
            self.configure_recolors.setEnabled(False)
            include_kh1_music_widget.setEnabled(False)
            include_kh2_music_widget.setEnabled(False)
            include_recom_music_widget.setEnabled(False)
            include_bbs_music_widget.setEnabled(False)
            include_ddd_music_widget.setEnabled(False)
        else:
            kh2_is_dir = (extracted_data_path / "kh2").is_dir()
            recolor_textures_widget.setEnabled(kh2_is_dir)
            self.configure_recolors.setEnabled(kh2_is_dir)
            include_kh1_music_widget.setEnabled((extracted_data_path / "kh1").is_dir())
            include_kh2_music_widget.setEnabled(kh2_is_dir)
            include_recom_music_widget.setEnabled((extracted_data_path / "recom").is_dir())
            include_bbs_music_widget.setEnabled((extracted_data_path / "bbs").is_dir())
            include_ddd_music_widget.setEnabled((extracted_data_path / "kh3d").is_dir())

        custom_music_configured = appconfig.read_custom_music_path() is not None
        include_custom_music_widget.setEnabled(custom_music_configured)
        self.no_custom_music.setVisible(music_rando_enabled and not custom_music_configured)
        self.open_custom_music_folder.setVisible(music_rando_enabled and custom_music_configured)

        self.keyblade_count_text.setVisible(keyblade_rando_enabled)
        self.keyblade_count_text.setText(self._get_keyblade_text())
        self.open_custom_keyblades_folder.setVisible(keyblade_rando_enabled)

        self.music_count_text.setVisible(music_rando_enabled)
        self.music_count_text.setText(self._get_music_text())

    @staticmethod
    def _get_keyblade_text():
        keyblade_summary = CosmeticsMod.get_keyblade_summary()
        if len(keyblade_summary) == 0:
            return "No Keyblades Found"
        else:
            label_text = "Found Keyblades\n"
            for category, count in keyblade_summary.items():
                label_text += f"{category} : {count}\n"
            return label_text

    def _get_music_text(self):
        music_summary = CosmeticsMod.get_music_summary(self.settings)
        if len(music_summary) == 0:
            return 'No Songs Found'
        else:
            label_text = 'Found Songs\n'
            for category, count in music_summary.items():
                label_text += '{} : {}\n'.format(category, count)
            return label_text

    def _reload_custom_executables_list(self):
        self.custom_list.clear()
        for file in self.custom_cosmetics.collect_custom_executable_files():
            self.custom_list.addItem(file)

    def _add_custom_executable(self):
        file_dialog = QFileDialog()
        outfile_name, _ = file_dialog.getOpenFileName(self, filter='Executables (*.exe *.bat)')
        if outfile_name != '':
            self.custom_cosmetics.add_custom_executable(outfile_name)
        self._reload_custom_executables_list()

    def _remove_selected_custom_executable(self):
        index = self.custom_list.currentRow()
        if index >= 0:
            self.custom_cosmetics.remove_executable_at_index(index)
            self._reload_custom_executables_list()

    def _recolor_enabled_changed(self):
        if self.settings.get(settingkey.RECOLOR_TEXTURES):
            self.configure_recolors.setVisible(True)
        else:
            self.configure_recolors.setVisible(False)

    def _configure_recolors(self):
        dialog = TextureRecolorSettingsDialog(self.settings)
        dialog.exec()

    @staticmethod
    def _open_custom_keyblades_folder():
        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is not None:
            keyblades_path = custom_visuals_path / "keyblades"
            if keyblades_path.is_dir():
                os.startfile(keyblades_path)

    @staticmethod
    def _open_custom_music_folder():
        custom_music_path = appconfig.read_custom_music_path()
        if custom_music_path is not None:
            os.startfile(custom_music_path)

    def _make_cosmetics_only_mod(self):
        extra_data = ExtraConfigurationData(
            platform="PC",
            tourney=False,
            custom_cosmetics_executables=self.custom_cosmetics.collect_custom_executable_files(),
        )
        worker = CosmeticsZipWorker(self, self.settings, extra_data)
        worker.start()
