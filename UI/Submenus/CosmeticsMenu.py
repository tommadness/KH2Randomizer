import os
import textwrap
from functools import partial
from typing import Optional

from PySide6.QtWidgets import QListWidget, QHBoxLayout, QFileDialog, QLabel, QGridLayout

from Class import settingkey
from Class.seedSettings import SeedSettings, ExtraConfigurationData
from List import configDict
from Module import appconfig
from Module.cosmetics import CustomCosmetics, CosmeticsMod
from UI import configui
from UI.Submenus.CustomVisualsDialogs import ItempicViewerDialog, RoomTransitionViewerDialog, EndingPictureViewerDialog, \
    CommandMenuViewerDialog
from UI.Submenus.ManageKeybladesDialog import ManageKeybladesDialog
from UI.Submenus.SubMenu import KH2Submenu
from UI.Submenus.TextureRecolorSettingsDialog import TextureRecolorSettingsDialog
from UI.configui import OPENKH_LOCATION_NOT_CHOSEN
from UI.qtlib import button, clear_layout, show_alert
from UI.worker import CosmeticsZipWorker

_IN_GAME_MUSIC_GROUP="in_game_music"
_CUSTOM_MUSIC_GROUP="custom_music"
_MUSIC_SUMMARY_GROUP="music_summary"


class CosmeticsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings, custom_cosmetics: CustomCosmetics):
        super().__init__(title='Cosmetics', settings=settings)

        self.custom_cosmetics = custom_cosmetics

        self.start_column()
        self.start_group()
        self.add_option(
            settingkey.COMMAND_MENU,
            auxiliary_widget=KH2Submenu.make_settings_button(self._view_command_menus, tooltip="View Command Menus")
        )
        # self.add_option(settingkey.COSTUME_RANDO)
        self.end_group("Visuals (PC/PCSX2)")

        self.start_group()
        self.recolor_setup = button("Enable Texture Recoloring", partial(self._require_extracted_data, "kh2"))
        self.pending_group.addWidget(self.recolor_setup)
        configure_recolors = KH2Submenu.make_settings_button(self._configure_recolors, tooltip="Texture Recolor Settings")
        self.add_option(settingkey.RECOLOR_TEXTURES, auxiliary_widget=configure_recolors)
        self.add_option(settingkey.RANDO_THEMED_TEXTURES)
        self.end_group("Textures (PC)")

        self.start_group()
        manage_keyblades = KH2Submenu.make_settings_button(self._manage_keyblades, "Manage Keyblades")
        self.add_option(settingkey.KEYBLADE_RANDO, auxiliary_widget=manage_keyblades)
        self.add_option(settingkey.KEYBLADE_RANDO_ALLOW_DUPLICATES)
        self.add_option(settingkey.KEYBLADE_RANDO_INCLUDE_EFFECTS)
        self.add_option(
            settingkey.KEYBLADE_RANDO_INCLUDE_GOA,
            auxiliary_widget=KH2Submenu.make_error_label(OPENKH_LOCATION_NOT_CHOSEN),
        )
        self.end_group("Keyblades (PC)")

        self.start_group()
        self.add_option(
            settingkey.ITEMPIC_RANDO,
            auxiliary_widget=KH2Submenu.make_settings_button(self._view_itempics, tooltip="View Item Pictures"),
        )
        self.add_option(
            settingkey.ROOM_TRANSITION_IMAGES,
            auxiliary_widget=KH2Submenu.make_settings_button(self._view_transitions, tooltip="View Transitions"),
        )
        self.add_option(
            settingkey.ENDPIC_RANDO,
            auxiliary_widget=KH2Submenu.make_settings_button(self._view_endpics, tooltip="View Ending Pictures"),
        )
        self.end_group("Other Visuals (PC)")

        self.end_column()

        self.start_column()
        self.start_group()
        self.add_option(settingkey.MUSIC_RANDO_ENABLED_PC)
        self.add_option(settingkey.MUSIC_RANDO_PC_USE_CATEGORIES)
        self.add_option(settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES)
        self.end_group("Music (PC)")

        self.start_group()
        self.in_game_music_setup = button("Enable In-Game Options", partial(self._require_extracted_data, None))
        self.pending_group.addWidget(self.in_game_music_setup)
        self.add_option(
            settingkey.MUSIC_RANDO_PC_INCLUDE_KH1,
            auxiliary_widget=KH2Submenu.make_error_label("KH1 game data not extracted."),
        )
        self.add_option(
            settingkey.MUSIC_RANDO_PC_INCLUDE_KH2,
            auxiliary_widget=KH2Submenu.make_error_label("KH2 game data not extracted."),
        )
        self.add_option(
            settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM,
            auxiliary_widget=KH2Submenu.make_error_label("Re:CoM game data not extracted."),
        )
        self.add_option(
            settingkey.MUSIC_RANDO_PC_INCLUDE_BBS,
            auxiliary_widget=KH2Submenu.make_error_label("BBS game data not extracted."),
        )
        self.add_option(
            settingkey.MUSIC_RANDO_PC_INCLUDE_DDD,
            auxiliary_widget=KH2Submenu.make_error_label("DDD game data not extracted."),
        )
        self.add_option(settingkey.MUSIC_RANDO_PC_DMCA_SAFE)
        self.end_group("KH Games Music Pool", group_id=_IN_GAME_MUSIC_GROUP)

        self.start_group()
        self.custom_music_setup = button("Enable Custom Music", self._set_up_custom_music)
        self.pending_group.addWidget(self.custom_music_setup)
        custom_folder_button = KH2Submenu.make_icon_button(
            self._open_custom_music_folder,
            icon_name="folder-open",
            tooltip="Open Custom Music Folder"
        )
        self.add_option(settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM, auxiliary_widget=custom_folder_button)
        self.end_group("Custom Music Pool", group_id=_CUSTOM_MUSIC_GROUP)

        self.start_group()
        self.music_summary_grid = QGridLayout()
        self.pending_group.addLayout(self.music_summary_grid)
        self.end_group("Music Summary", group_id=_MUSIC_SUMMARY_GROUP)

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
        button_layout.addWidget(button("Add", self._add_custom_executable))
        button_layout.addWidget(button("Remove", self._remove_selected_custom_executable))
        self.pending_group.addLayout(button_layout)

        self.end_group('External Randomization Executables')

        self.start_group()
        cosmetics_mod_button = button("Generate Cosmetics-Only Mod (PC)", self._make_cosmetics_only_mod)
        cosmetics_mod_tooltip = textwrap.dedent('''
        Generates an OpenKH mod that ONLY randomizes cosmetics. Can be useful if using a seed generated outside of this
        generator (using Archipelago.gg or otherwise).
        ''').strip()
        cosmetics_mod_button.setToolTip(cosmetics_mod_tooltip)
        self.pending_group.addWidget(cosmetics_mod_button)
        self.end_group('Cosmetics-Only Mod')
        self.end_column()

        self.finalizeMenu()

        settings.observe(settingkey.KEYBLADE_RANDO, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_ENABLED_PC, self.reload_cosmetic_widgets)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_KH1, self._refresh_music_summary)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_KH2, self._refresh_music_summary)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM, self._refresh_music_summary)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_BBS, self._refresh_music_summary)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_DDD, self._refresh_music_summary)
        settings.observe(settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM, self._refresh_music_summary)
        settings.observe(settingkey.MUSIC_RANDO_PC_DMCA_SAFE, self._refresh_music_summary)
        settings.observe(settingkey.MUSIC_RANDO_PC_USE_CATEGORIES, self._refresh_music_summary)

        self.reload_cosmetic_widgets()
        self._reload_custom_executables_list()

    def reload_cosmetic_widgets(self):
        _, include_kh1_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_KH1]
        _, include_kh2_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_KH2]
        _, include_recom_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM]
        _, include_bbs_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_BBS]
        _, include_ddd_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_DDD]
        _, include_custom_music_widget = self.widgets_and_settings_by_name[settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM]

        extracted_data_path = appconfig.extracted_data_path()
        has_extracted_data = extracted_data_path is not None
        has_extracted_kh2 = self._has_extracted_data("kh2")

        self.recolor_setup.setVisible(not has_extracted_kh2)
        self.set_option_visibility(settingkey.RECOLOR_TEXTURES, visible=has_extracted_kh2)

        keyblade_rando_setting = self.settings.get(settingkey.KEYBLADE_RANDO)
        keyblade_rando_enabled = keyblade_rando_setting != configDict.VANILLA
        self.set_option_visibility(settingkey.KEYBLADE_RANDO_ALLOW_DUPLICATES, visible=keyblade_rando_enabled)
        self.set_option_visibility(settingkey.KEYBLADE_RANDO_INCLUDE_EFFECTS, visible=keyblade_rando_enabled)
        self.set_option_visibility(settingkey.KEYBLADE_RANDO_INCLUDE_GOA, visible=keyblade_rando_enabled)
        self.set_auxiliary_visibility(settingkey.KEYBLADE_RANDO_INCLUDE_GOA, visible=not has_extracted_data)

        music_rando_enabled = self.settings.get(settingkey.MUSIC_RANDO_ENABLED_PC)
        custom_music_configured = appconfig.read_custom_music_path() is not None
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_USE_CATEGORIES, visible=music_rando_enabled)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES, visible=music_rando_enabled)
        self.set_group_visibility(_IN_GAME_MUSIC_GROUP, visible=music_rando_enabled)
        self.set_group_visibility(_CUSTOM_MUSIC_GROUP, visible=music_rando_enabled)
        self.set_group_visibility(_MUSIC_SUMMARY_GROUP, visible=music_rando_enabled)

        has_extracted_kh1 = self._has_extracted_data("kh1")
        has_extracted_recom = self._has_extracted_data("recom")
        has_extracted_bbs = self._has_extracted_data("bbs")
        has_extracted_ddd = self._has_extracted_data("ddd")
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_KH1, visible=has_extracted_data)
        self.set_auxiliary_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_KH1, visible=not has_extracted_kh1)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_KH2, visible=has_extracted_data)
        self.set_auxiliary_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_KH2, visible=not has_extracted_kh2)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM, visible=has_extracted_data)
        self.set_auxiliary_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM, visible=not has_extracted_recom)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_BBS, visible=has_extracted_data)
        self.set_auxiliary_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_BBS, visible=not has_extracted_bbs)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_DDD, visible=has_extracted_data)
        self.set_auxiliary_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_DDD, visible=not has_extracted_ddd)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_DMCA_SAFE, visible=has_extracted_data)
        if has_extracted_data:
            include_kh1_music_widget.setEnabled(has_extracted_kh1)
            include_kh2_music_widget.setEnabled(has_extracted_kh2)
            include_recom_music_widget.setEnabled(has_extracted_recom)
            include_bbs_music_widget.setEnabled(has_extracted_bbs)
            include_ddd_music_widget.setEnabled(has_extracted_ddd)

        self.in_game_music_setup.setVisible(not has_extracted_data)
        self.custom_music_setup.setVisible(not custom_music_configured)
        self.set_option_visibility(settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM, custom_music_configured)

        self._refresh_music_summary()

    @staticmethod
    def _has_extracted_data(game: str) -> bool:
        return appconfig.extracted_game_path(game) is not None

    def _refresh_music_summary(self):
        clear_layout(self.music_summary_grid)
        music_summary = CosmeticsMod.get_music_summary(self.settings)
        row = 0
        for category, count in music_summary.items():
            if count > 0:
                self.music_summary_grid.addWidget(QLabel(category), row, 0)
                self.music_summary_grid.addWidget(QLabel(f"{count}"), row, 1)
                row = row + 1
        if row == 0:
            self.music_summary_grid.addWidget(QLabel("Music pool is empty."), 0, 0)

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

    def _require_extracted_data(self, game: Optional[str]):
        if appconfig.read_openkh_path() is None:
            show_alert(configui.OPENKH_LOCATION_NOT_CHOSEN)
            if configui.openkh_folder_getter():
                self.reload_cosmetic_widgets()
        elif game is not None and not self._has_extracted_data(game):
            show_alert(f"{game} data has not been extracted in OpenKH Mods Manager.")
        elif appconfig.extracted_data_path() is None:
            show_alert(f"Game data has not been extracted in OpenKH Mods Manager.")

    def _configure_recolors(self):
        dialog = TextureRecolorSettingsDialog(self.settings)
        dialog.exec()

    def _view_command_menus(self):
        dialog = CommandMenuViewerDialog(self)
        dialog.exec()

    def _view_itempics(self):
        dialog = ItempicViewerDialog(self)
        dialog.exec()

    def _view_transitions(self):
        dialog = RoomTransitionViewerDialog(self)
        dialog.exec()

    def _view_endpics(self):
        dialog = EndingPictureViewerDialog(self)
        dialog.exec()

    def _manage_keyblades(self):
        dialog = ManageKeybladesDialog(self, self.settings)
        dialog.exec()
        self.reload_cosmetic_widgets()

    def _set_up_custom_music(self):
        show_alert(configui.CUSTOM_MUSIC_NOT_CHOSEN)
        if configui.custom_music_folder_getter():
            self.reload_cosmetic_widgets()

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
