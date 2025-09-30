import datetime
import json
import os
import random
import re
import string
import subprocess
import sys
import textwrap
import zipfile
from pathlib import Path

import pyperclip as pc
import pytz
from PySide6 import QtGui
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QImage
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QMenu, QPushButton, QCheckBox, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
    QMessageBox, QProgressDialog, QProgressBar, QDialog, QGridLayout, QListWidget, QSpinBox, QComboBox,
    QListView, QFrame
)

from Class import settingkey
from Class.exceptions import CantAssignItemException, RandomizerExceptions, SettingsException
from Class.seedSettings import SeedSettings, ExtraConfigurationData, randomize_settings
from Module import appconfig, hashimage, version
from Module.RandomizerSettings import RandomizerSettings
from Module.cosmetics import CosmeticsMod, CustomCosmetics
from Module.dailySeed import allDailyModifiers, getDailyModifiers
from Module.generate import generateSeed
from Module.newRandomize import Randomizer
from Module.resources import resource_path
from Module.seedshare import SharedSeed, ShareStringException
from Module.tourneySpoiler import TourneySeedSaver
from Module.version import LOCAL_UI_VERSION, EXTRACTED_DATA_UPDATE_VERSION
from UI import theme, presets, configui
from UI.GithubInfo.releaseInfo import KH2RandomizerGithubReleases
from UI.Submenus.BossEnemyMenu import BossEnemyMenu
from UI.Submenus.CompanionMenu import CompanionMenu
from UI.Submenus.CosmeticsMenu import CosmeticsMenu
from UI.Submenus.DevCreateRecolorDialog import DevCreateRecolorDialog
from UI.Submenus.HintsMenu import HintsMenu
from UI.Submenus.ItemPlacementMenu import ItemPlacementMenu
from UI.Submenus.ItemPoolMenu import ItemPoolMenu
from UI.Submenus.KeybladeMenu import KeybladeMenu
from UI.Submenus.RewardLocationsMenu import RewardLocationsMenu
from UI.Submenus.SeedModMenu import SeedModMenu
from UI.Submenus.SoraMenu import SoraMenu
from UI.Submenus.StartingMenu import StartingMenu
from UI.Submenus.about import AboutDialog
from UI.presets import SettingsPreset, RandomPresetDialog
from UI.worker import GenerateSeedWorker


class Logger(object):
    def __init__(self, orig_stream):
        self.filename = "log.txt"
        self.orig_stream = orig_stream
    def write(self, data):
        with open(self.filename, "a") as f:
            f.write(str(data))
        self.orig_stream.write(str(data))
    def flush(self):
        self.orig_stream.flush()

logger = Logger(sys.stdout)

sys.stdout = logger
sys.stderr = logger


class TourneySeedDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tourney Mode")
        self.setMinimumWidth(800)

        grid = QGridLayout()
        row = 0

        explanation = textwrap.dedent('''
Use this screen to generate a set of seeds for a tournament.

The tournament organizer receives a folder containing all of the seed strings, seed hashes, and spoiler logs.
This can be shared with other tournament organizers to make sure everyone has access to all the seeds. 

When participants receive their seeds, they will NOT have access to spoiler logs.
Participants will only be able to customize cosmetics.
        '''.strip())
        grid.addWidget(QLabel(explanation), row, 0, 1, 3)

        row = row + 1
        grid.addWidget(QLabel(''), row, 0)

        row = row + 1
        grid.addWidget(QLabel('Tournament Name'), row, 0)
        name_field = QLineEdit()
        name_field.setToolTip('The name of the tournament.')
        self.name_field = name_field
        grid.addWidget(name_field, row, 1, 1, 2)

        row = row + 1
        tourney_label = QLabel("How many seeds?")
        grid.addWidget(tourney_label, row, 0)

        self.num_seeds = QSpinBox()
        self.num_seeds.setRange(1, 32)
        self.num_seeds.setSingleStep(1)
        self.num_seeds.setValue(1)
        grid.addWidget(self.num_seeds, row, 1, 1, 2)

        row = row + 1
        platform_label = QLabel("Make seeds for")
        grid.addWidget(platform_label, row, 0)
        self.platform = QComboBox()
        self.platform.addItem("PC")
        self.platform.addItem("PCSX2")
        grid.addWidget(self.platform, row, 1, 1, 2)

        row = row + 1
        output_path_field = QLineEdit()
        output_path_field.setToolTip('The location to which to save the generated seeds.')
        self.output_path_field = output_path_field
        output_path_button = QPushButton('Browse')
        output_path_button.clicked.connect(self._choose_output_path)

        grid.addWidget(QLabel('Output location'), row, 0)
        grid.addWidget(output_path_field, row, 1)
        grid.addWidget(output_path_button, row, 2)

        row = row + 1
        cancel_button = QPushButton("Cancel")
        choose_button = QPushButton("Generate Seeds")
        cancel_button.clicked.connect(self.reject)
        choose_button.clicked.connect(self.accept)
        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(choose_button)
        grid.addLayout(button_layout, row, 0, 1, 3)

        box = QVBoxLayout()
        box.addLayout(grid)

        self.setLayout(box)

    def save(self):
        return self.name_field.text(), self.num_seeds.value(), self.platform.currentText(), self.output_path_field.text()

    def _choose_output_path(self):
        output = QFileDialog.getExistingDirectory()
        if output is not None and output != '':
            self.output_path_field.setText(output)


class RandomSettingsDialog(QDialog):
    def __init__(self,settings: SeedSettings):
        super().__init__()
        self.passed_settings = settings
        self.random_choices = self.passed_settings._randomizable
        self.stored_random_settings = self.passed_settings.get(settingkey.RANDOMIZED_SETTINGS)
        self.random_settings_enabled = self.passed_settings.get(settingkey.RANDOMIZED_SETTINGS_ENABLED)
        self.setWindowTitle("Randomized Settings")
        self.setMinimumWidth(850)
        self.setMinimumHeight(800)

        box = QVBoxLayout()
        grid = QGridLayout()

        self.settings_list_widget = QListWidget()
        self.settings_list_widget.setItemAlignment(Qt.AlignVCenter)
        self.settings_list_widget.setProperty("cssClass", "grid")
        self.settings_list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.settings_list_widget.setFlow(QListView.LeftToRight)
        self.settings_list_widget.setResizeMode(QListView.Adjust)
        self.settings_list_widget.setGridSize(QSize(160, 48))
        self.settings_list_widget.setUniformItemSizes(True)
        self.settings_list_widget.setSpacing(32)
        self.settings_list_widget.setViewMode(QListView.IconMode)
        self.settings_list_widget.setWordWrap(True)
        self.settings_list_widget.setTextElideMode(Qt.ElideNone)
        random_setting_counter = 0
        for c in self.random_choices:
            self.settings_list_widget.addItem(c.standalone_label)
            random_setting_counter+=1
            if c.name in self.stored_random_settings:
                self.settings_list_widget.item(random_setting_counter-1).setSelected(True)
        for i in range(len(self.random_choices)):
            self.settings_list_widget.item(i).setSizeHint(QSize(160, 48))
        self.settings_list_widget.setDragEnabled(False)
        grid.addWidget(self.settings_list_widget,0,0)
        
        select_all_button = QPushButton("Select All Settings")
        select_all_button.clicked.connect(self.select_all_randomizable)
        select_none_button = QPushButton("Select No Settings")
        select_none_button.clicked.connect(self.select_none_randomizable)

        select_buttons = QHBoxLayout()
        select_buttons.addWidget(select_all_button)
        select_buttons.addWidget(select_none_button)

        choose_button = QPushButton("Save Selected Settings")
        choose_button.clicked.connect(self.accept)
        self.enable_checkbox = QCheckBox("Randomize Settings Enabled")
        self.enable_checkbox.setChecked(self.random_settings_enabled)

        confirm_buttons = QHBoxLayout()
        confirm_buttons.addWidget(self.enable_checkbox)
        confirm_buttons.addWidget(choose_button)

        box.addLayout(select_buttons)
        box.addLayout(grid)
        box.addLayout(confirm_buttons)

        self.setLayout(box)

    def select_all_randomizable(self):
        for index in range(self.settings_list_widget.count()):
            self.settings_list_widget.item(index).setSelected(True)
    def select_none_randomizable(self):
        for index in range(self.settings_list_widget.count()):
            self.settings_list_widget.item(index).setSelected(False)

    def save(self):
        # save the settings
        randomized_settings_selected = [self.random_choices[p.row()].name for p in self.settings_list_widget.selectedIndexes()]
        self.passed_settings.set(settingkey.RANDOMIZED_SETTINGS,randomized_settings_selected)  
        self.passed_settings.set(settingkey.RANDOMIZED_SETTINGS_ENABLED,self.enable_checkbox.isChecked())
        return randomized_settings_selected

class KH2RandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UTC = pytz.utc
        self.startTime = datetime.datetime.now(self.UTC)
        self.dailySeedName = self.startTime.strftime('%d-%m-%Y')
        self.mods = getDailyModifiers(self.startTime,hard_mode=False,boss_enemy=False)
        self.mods_hard = getDailyModifiers(self.startTime,hard_mode=True,boss_enemy=False)
        self.mods_be = getDailyModifiers(self.startTime,hard_mode=False,boss_enemy=True)
        self.mods_hard_be = getDailyModifiers(self.startTime,hard_mode=True,boss_enemy=True)
        self.progress = None
        self.spoiler_log_output = "<html>No spoiler log generated</html>"
        self.num_tourney_seeds = 0
        self.num_items_to_place = None
        self.num_locations_to_fill = None
        
        app_config = appconfig.read_app_config()
        self.disable_emu_warnings = "disable_emu_warnings" in app_config

        self.settings = SeedSettings()
        self.custom_cosmetics = CustomCosmetics()

        if not os.path.exists(appconfig.AUTOSAVE_FOLDER):
            os.makedirs(appconfig.AUTOSAVE_FOLDER)
        auto_settings_save_path = os.path.join(appconfig.AUTOSAVE_FOLDER, 'auto-save.json')
        if os.path.exists(auto_settings_save_path):
            with open(auto_settings_save_path, 'r') as source:
                try:
                    auto_settings_json = json.load(source)
                    self.settings.apply_settings_json(auto_settings_json, include_private=True)
                except Exception:
                    print('Unable to apply last settings - will use defaults')

        presets.bootstrap_presets()
        CosmeticsMod.bootstrap_cosmetics_files()

        # using this to change settings when these files are provided
        self.boss_enemy_overrides = appconfig.read_boss_enemy_override_files()

        random.seed(str(datetime.datetime.now()))

        debug_string = ""
        if version.debug_mode():
            debug_string = "DEBUG "
        self.setWindowTitle(f"KH2 Randomizer Seed Generator ({debug_string}{LOCAL_UI_VERSION})")
        self.setWindowIcon(QIcon(resource_path("Module/icon.png")))
        self.setup = None
        pagelayout = QVBoxLayout()
        seed_layout = QHBoxLayout()
        progress_layout = QHBoxLayout()
        submit_layout = QHBoxLayout()
        self.tabs = QTabWidget()

        self._configure_menu_bar()
        self._reload_presets()

        pagelayout.addLayout(seed_layout)
        pagelayout.addSpacing(8)
        pagelayout.addWidget(self.tabs)        
        pagelayout.addLayout(progress_layout)
        pagelayout.addLayout(submit_layout)

        seed_layout.addWidget(QLabel("Seed"))
        self.seedName = QLineEdit()
        self.seedName.setProperty("cssClass", "biggerLineEdit")
        self.seedName.setPlaceholderText("Leave blank for a random seed")
        seed_layout.addWidget(self.seedName)

        self.spoiler_log = QCheckBox("Make Spoiler Log")
        self.spoiler_log.setCheckState(Qt.Checked)
        seed_layout.addWidget(self.spoiler_log)

        self.cosmetics_menu = CosmeticsMenu(self.settings, self.custom_cosmetics)

        self.widgets = [
            RewardLocationsMenu(self.settings),
            ItemPlacementMenu(self.settings),
            HintsMenu(self.settings),
            ItemPoolMenu(self.settings),
            StartingMenu(self.settings),
            SeedModMenu(self.settings),
            SoraMenu(self.settings),
            KeybladeMenu(self.settings),
            CompanionMenu(self.settings),
            BossEnemyMenu(self.settings, seed_name_getter=lambda: self.seedName.text()),
            self.cosmetics_menu,
        ]

        for i in range(len(self.widgets)):
            self.tabs.addTab(self.widgets[i],self.widgets[i].getName())

        progress_layout.addWidget(self._build_progress_frame())

        submit_layout.addWidget(self._build_seed_hash_frame())
        submit_layout.addSpacing(8)
        submit_layout.addWidget(self._build_generate_seed_frame())

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        self.recalculate = False
        settings_keys = SeedSettings.filtered_settings(include_private=True).keys()
        for key in settings_keys:
            self.settings.observe(key,self.get_num_enabled_locations)

        self.seedName.editingFinished.connect(self._seed_name_changed)

        # do a sanity update for anything that didn't update
        for widget in self.widgets:
            widget.update_widgets()

    def _configure_menu_bar(self):
        menu_bar = self.menuBar()
        self.presetMenu = QMenu("Preset")
        self.loadPresetsMenu = QMenu("Load a Preset")
        self.presetMenu.addMenu(self.loadPresetsMenu)
        self.presetMenu.addAction("Open Preset Folder", self.openPresetFolder)
        self.presetMenu.addAction("Import Preset", self._import_preset)
        self.presetMenu.addAction("Save Settings as New Preset", self._save_preset)
        self.presetMenu.addAction("Pick a Random Preset", self.randomPreset)
        
        self.seedMenu = QMenu("Share Seed")
        self.seedMenu.addAction("Save Seed to Clipboard", self.shareSeed)
        self.seedMenu.addAction("Load Seed from Clipboard", self.receiveSeed)
        self.config_menu = QMenu('Configure')
        cosmetic_submenu = QMenu("Cosmetics")
        cosmetic_submenu.addAction('Find OpenKH Folder', self.openkh_folder_getter)
        cosmetic_submenu.addAction('Choose Custom Music Folder', self.custom_music_folder_getter)
        cosmetic_submenu.addAction('Choose Custom Visuals Folder', self.custom_visuals_folder_getter)
        self.config_menu.addMenu(cosmetic_submenu)
        if version.debug_mode():
            self.config_menu.addSeparator()
            self.config_menu.addAction("Create Texture Recolor (Dev Only)", self._dev_create_recolor)
        self.config_menu.addSeparator()
        self.remember_window_position_action = self.config_menu.addAction('Remember Window Size/Position')
        self.remember_window_position_action.setCheckable(True)
        self.emu_warning_toggle = self.config_menu.addAction('Disable Emulator Warnings')
        self.emu_warning_toggle.setCheckable(True)
        self.emu_warning_toggle.setChecked(self.disable_emu_warnings)
        self.config_menu.addSeparator()

        github_releases = KH2RandomizerGithubReleases()
        infos = github_releases.get_update_infos()
        self.updateAction = None
        if(len(infos)>0):
            self.updateAction = menu_bar.addAction("Update Seed Gen", self._update_generator)

        menu_bar.addMenu(self.seedMenu)
        menu_bar.addMenu(self.presetMenu)

        self.dailyMenu = QMenu("Daily Seeds")
        self.dailyMenu.addAction("Load Seed", self.loadDailySeed)
        self.dailyMenu.addAction("Load Hard Seed", self.loadHardDailySeed)
        self.dailyMenu.addAction("Load Boss/Enemy Seed", self.loadDailySeedBE)
        self.dailyMenu.addAction("Load Hard Boss/Enemy Seed", self.loadHardDailySeedBE)
        menu_bar.addMenu(self.dailyMenu)
        self.randomizeSettings = menu_bar.addAction("Randomize Settings", self.randoRando)

        self.tourneySeeds = menu_bar.addAction("Tourney Seeds", self.makeTourneySeeds)
        
        menu_bar.addMenu(self.config_menu)

        menu_bar.addAction("About", self.show_about)

    def _update_generator(self):
        #invoke the update exe
        process = subprocess.Popen(resource_path("updater.exe"))
        sys.exit()

    def _build_progress_frame(self) -> QFrame:
        self.progress_label = QLabel("Progress Placeholder")
        self.progress_label.setContentsMargins(0, 16, 0, 16)
        self.progress_label.setStyleSheet(f"background: {theme.KhMediumPurple}; color: {theme.KhLightPurple};")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setFixedWidth(320)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)

        progress_layout = QHBoxLayout()
        progress_layout.setContentsMargins(0, 0, 8, 0)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)

        progress_frame = QFrame()
        progress_frame.setProperty('cssClass', 'settingsFrame')
        progress_frame.setStyleSheet(f'QLabel, QFrame[cssClass~="settingsFrame"] {{ background: {theme.KhDarkPurple}; }}')
        progress_frame.setLayout(progress_layout)

        return progress_frame

    def _build_seed_hash_frame(self) -> QFrame:
        self.hash_icon_names = []
        self.hash_icon_labels = []

        hash_layout = QHBoxLayout()
        hash_layout.setContentsMargins(0, 0, 8, 0)

        seed_hash_label = QLabel('Seed Hash')
        seed_hash_label.setContentsMargins(8, 8, 8, 8)
        seed_hash_label.setStyleSheet(f"background: {theme.KhMediumBlue}; color: {theme.KhLightBlue};")
        hash_layout.addWidget(seed_hash_label)

        for i in range(7):
            hash_icon_label = QLabel()
            hash_icon_label.blockSignals(True)
            self.hash_icon_labels.append(hash_icon_label)
            hash_layout.addWidget(hash_icon_label)

        copy_hash = QPushButton('Copy')
        copy_hash.clicked.connect(self._copy_hash_to_clipboard)
        hash_layout.addWidget(copy_hash)

        hash_frame = QFrame()
        hash_frame.setProperty('cssClass', 'settingsFrame')
        hash_frame.setStyleSheet(f'QLabel, QFrame[cssClass~="settingsFrame"] {{ background: {theme.KhDarkBlue}; }}')
        hash_frame.setLayout(hash_layout)

        self.clear_hash_icons()

        return hash_frame

    def _build_generate_seed_frame(self):
        generate_layout = QHBoxLayout()
        generate_layout.setContentsMargins(0, 0, 8, 0)

        generate_label = QLabel('Seed Generation')
        generate_label.setContentsMargins(8, 8, 8, 8)
        generate_label.setStyleSheet(f"background: {theme.KhMediumRed}; color: {theme.KhLightRed};")
        generate_layout.addWidget(generate_label)

        self.emu_button = QPushButton("Generate Seed (PCSX2)")
        self.emu_button.clicked.connect(lambda: self.makeSeed("PCSX2"))
        generate_layout.addWidget(self.emu_button, stretch=1)
        self.emu_button.setVisible(False)

        self.pc_button = QPushButton("Generate Seed (PC)")
        self.pc_button.clicked.connect(lambda: self.makeSeed("PC"))
        generate_layout.addWidget(self.pc_button, stretch=1)
        self.pc_button.setVisible(False)

        self.both_button = QPushButton("Generate Seed (PC/PCSX2)")
        self.both_button.clicked.connect(lambda: self.makeSeed("Both"))
        generate_layout.addWidget(self.both_button, stretch=1)

        generate_frame = QFrame()
        generate_frame.setProperty('cssClass', 'settingsFrame')
        generate_frame.setStyleSheet(f'QLabel, QFrame[cssClass~="settingsFrame"] {{ background: {theme.KhDarkRed}; }}')
        generate_frame.setLayout(generate_layout)
        return generate_frame

    def closeEvent(self, e):
        settings_json = self.settings.settings_json(include_private=True)
        with open(os.path.join(appconfig.AUTOSAVE_FOLDER, 'auto-save.json'), 'w') as presetData:
            presetData.write(json.dumps(settings_json, indent=4, sort_keys=True))

        self.custom_cosmetics.write_file()

        if self.remember_window_position_action.isChecked():
            obj = {
                'width': self.width(),
                'height': self.height(),
                'x': self.x(),
                'y': self.y()
            }
            appconfig.update_app_config('window_position', obj)
        else:
            appconfig.remove_app_config('window_position')
        if self.emu_warning_toggle.isChecked():
            appconfig.update_app_config('disable_emu_warnings', True)
        else:
            appconfig.remove_app_config('disable_emu_warnings')

        e.accept()

    def resetSettings(self):
        try:
            # Attempt to use the bundled starter preset
            starter_settings_preset = presets.bundled_starter_preset()
            settings_json = starter_settings_preset.settings_json()
        except Exception:
            # Hopefully impossible, but if it fails, just use empty settings (applying them should set the defaults)
            settings_json = {}

        self.recalculate = False
        self.settings.apply_settings_json(settings_json)
        for widget in self.widgets:
            widget.update_widgets()
        self.recalculate = True
        self.get_num_enabled_locations()

    def dailySeedHandler(self,difficulty,boss_enemy=False):
        try:
            starter_settings_preset = presets.bundled_starter_preset()
            starter_settings_json = starter_settings_preset.settings_json()
        except SettingsException:
            message = QMessageBox(text="Unable to load base settings for daily seeds.")
            message.setWindowTitle('KH2 Seed Generator - Daily Seed')
            message.exec()
            return

        self.seedName.setText(self.dailySeedName)
        self.recalculate = False

        #test all daily settings for sanity
        try:
            all_mods = allDailyModifiers()
            for m in all_mods:
                self.settings.apply_settings_json(starter_settings_json)
                m.local_modifier(self.settings)
                for widget in self.widgets:
                    widget.update_widgets()
        except Exception as e:
            print(f"Error found with one of the options {e}")

        self.settings.apply_settings_json(starter_settings_json)

        # use the modifications to change the preset
        mod_string = f'Updated settings for Daily Seed {self.startTime.strftime("%a %b %d %Y")}\n\n'
        which_mods = None
        if difficulty=="easy" and not boss_enemy:
            which_mods = self.mods
        elif difficulty=="easy" and boss_enemy:
            which_mods = self.mods_be
        elif difficulty=="hard" and not boss_enemy:
            which_mods = self.mods_hard
        elif difficulty=="hard" and boss_enemy:
            which_mods = self.mods_hard_be
        else:
            raise RandomizerExceptions("Improper Daily Seed Setting")

        for m in which_mods:
            m.local_modifier(self.settings)
            mod_string += m.name + ' - ' + m.description + '\n\n'

        for widget in self.widgets:
            widget.update_widgets()
        self.recalculate = True
        self.get_num_enabled_locations()

        self.fixSeedName()

        message = QMessageBox(text=mod_string)
        message.setWindowTitle('KH2 Seed Generator - Daily Seed')
        message.exec()

    def loadDailySeed(self):
        self.dailySeedHandler(difficulty="easy")

    def loadHardDailySeed(self):
        self.dailySeedHandler(difficulty="hard")

    def loadDailySeedBE(self):
        self.dailySeedHandler(difficulty="easy", boss_enemy=True)

    def loadHardDailySeedBE(self):
        self.dailySeedHandler(difficulty="hard", boss_enemy=True)

    def makeTourneySeeds(self):
        tourney_dialog = TourneySeedDialog()
        if tourney_dialog.exec():
            tourney_name, num_tourney_seeds, seed_platform, output_path = tourney_dialog.save()
            self.num_tourney_seeds = num_tourney_seeds

            self.tourney_seed_path = Path(output_path) / tourney_name
            self.tourney_name = tourney_name

            self.makeSeed(seed_platform)
            self.num_tourney_seeds = 0

            message = QMessageBox(text=f"Done making seeds")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()

    def fixSeedName(self):
        new_string = re.sub(r'[^a-zA-Z0-9]', '', self.seedName.text())
        self.seedName.setText(new_string)
        if self.num_tourney_seeds>0:
            self.spoiler_log.setChecked(False)

    def _seed_name_changed(self):
        seed_name_text = self.seedName.text().strip()
        # If what appears to be a full seed string gets pasted in, go ahead and try to apply it
        if seed_name_text.startswith(LOCAL_UI_VERSION):
            try:
                shared_seed = SharedSeed.from_share_string(
                    local_generator_version=LOCAL_UI_VERSION,
                    share_string=seed_name_text
                )
                self.apply_shared_seed(shared_seed)
            except ShareStringException as exception:
                message = QMessageBox(text=exception.message)
                message.setWindowTitle("KH2 Seed Generator")
                message.exec()
        else:
            self.make_rando_settings()

    def make_rando_settings(self, catch_exception=True):
        if self.num_tourney_seeds>0:
            makeSpoilerLog = False
        else:
            makeSpoilerLog = self.spoiler_log.isChecked()

        # seed
        self.validate_seed_name()
        random.seed(self.seedName.text())

        rando_rando_counter = 0
        last_exception = None
        while rando_rando_counter < 10:
            rando_rando_counter+=1
            backup_settings, shared_string = self.randomize_the_settings()
            try:
                if shared_string is None:
                    shared_string = self.createSharedString()
                rando_settings = RandomizerSettings(self.seedName.text(),makeSpoilerLog,LOCAL_UI_VERSION,self.settings,shared_string,self.boss_enemy_overrides)
                if backup_settings:
                    self.settings.apply_settings_string(backup_settings)
                self.recalculate = True
                # update the seed hash display
                self.update_ui_hash_icons(rando_settings)

                return rando_settings
            except RandomizerExceptions as e:
                if backup_settings:
                    self.settings.apply_settings_string(backup_settings)
                last_exception = e
        if catch_exception and last_exception is not None:
            self.handleFailure(last_exception)
            return None
        else:
            raise last_exception

    def update_ui_hash_icons(self, rando_settings):
        self.hash_icon_names.clear()
        for index, icon in enumerate(rando_settings.seedHashIcons):
            self.hash_icon_names.append(icon)
            self.hash_icon_labels[index].setPixmap(QPixmap(str(hashimage.seed_hash_icon_path(icon))))

    def clear_hash_icons(self):
        self.hash_icon_names.clear()
        for i in range(7):
            self.hash_icon_labels[i].setPixmap(QPixmap(str(hashimage.seed_hash_icon_path("question-mark"))))

    def _copy_hash_to_clipboard(self):
        image_data = hashimage.generate_seed_hash_image(self.hash_icon_names, use_bitmap=True)
        QApplication.clipboard().setImage(QImage.fromData(image_data))

    def get_num_enabled_locations(self):
        if self.recalculate:
            try:
                rando_settings = self.make_rando_settings()
                dummy_rando = Randomizer(rando_settings, progress_bar_vis=True)
                split_pc_emu = False
                split_pc_emu = split_pc_emu or self.settings.get(settingkey.CUPS_GIVE_XP)
                split_pc_emu = split_pc_emu or self.settings.get(settingkey.REMOVE_DAMAGE_CAP)
                split_pc_emu = split_pc_emu or self.settings.get(settingkey.RETRY_DARK_THORN)
                split_pc_emu = split_pc_emu or self.settings.get(settingkey.RETRY_DFX)
                # split_pc_emu = split_pc_emu or self.settings.get(settingkey.REMOVE_CUTSCENES)
                split_pc_emu = split_pc_emu or self.settings.get(settingkey.KEYBLADES_LOCK_CHESTS)
                # split_pc_emu = split_pc_emu or self.settings.get(settingkey.BLOCK_COR_SKIP)
                # split_pc_emu = split_pc_emu or self.settings.get(settingkey.BLOCK_SHAN_YU_SKIP)
                split_pc_emu = split_pc_emu or rando_settings.enemy_options["boss"] != "Disabled"
                split_pc_emu = split_pc_emu or rando_settings.enemy_options["enemy"] != "Disabled"
                # split_pc_emu = split_pc_emu or self.settings.get(settingkey.TT1_JAILBREAK)

                
                disable_emu = False
                disable_emu = disable_emu or rando_settings.enemy_options["enemy"] == "Wild"
                disable_emu = disable_emu or rando_settings.enemy_options["bosses_replace_enemies"]
                disable_emu = disable_emu or rando_settings.enemy_options["combine_enemy_sizes"]
                disable_emu = disable_emu or rando_settings.enemy_options["combine_melee_ranged"]
                disable_emu = disable_emu or rando_settings.enemy_options["gimmick_bosses"]
                # disable_emu = disable_emu or self.settings.get(settingkey.TT1_JAILBREAK)


                self.emu_button.setVisible(split_pc_emu)
                self.pc_button.setVisible(split_pc_emu)
                self.both_button.setVisible(not split_pc_emu)
                self.emu_button.setEnabled(not disable_emu)

            except CantAssignItemException as e:
                pass
            
            self.num_items_to_place = dummy_rando.num_available_items
            self.num_locations_to_fill = dummy_rando.num_valid_locations
            text = f"Items: {dummy_rando.num_available_items} / Locations: {dummy_rando.num_valid_locations}"
            self.progress_bar.setRange(0, dummy_rando.num_valid_locations)
            if dummy_rando.num_valid_locations < dummy_rando.num_available_items:
                self.progress_bar.setValue(dummy_rando.num_valid_locations)
                text = "Too many "+text
            else:
                self.progress_bar.setValue(dummy_rando.num_available_items)
            self.progress_label.setText(text)

    def makeSeed(self,platform):
        self.fixSeedName()
        if self.num_tourney_seeds>0:
            message = QMessageBox(text="Tourney Mode in Use. Spoiler will be generated outside the zip, and cosmetics disabled.")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
            # disable all cosmetics, generate a spoiler log, but don't put it in the zip
            extra_data = ExtraConfigurationData(platform=platform, tourney=True, custom_cosmetics_executables=[],disable_emu_warning=self.disable_emu_warnings)
            self.genTourneySeeds(extra_data)
        else:
            extra_data = ExtraConfigurationData(
                platform=platform,
                tourney=False,
                custom_cosmetics_executables=self.custom_cosmetics.collect_custom_executable_files(),
                disable_emu_warning=self.disable_emu_warnings,
            )

            rando_settings = self.make_rando_settings()
            if rando_settings is not None:
                worker = GenerateSeedWorker(self, rando_settings, extra_data)
                worker.start()

        # rando_settings = self.make_rando_settings()
        # self.seedName.setText("")
        # rando_settings2 = self.make_rando_settings()
        # if rando_settings is not None:
        #     worker = GenerateMultiWorldSeedWorker(self, rando_settings2, extra_data)
        #     worker.generate_seed()

    def handleFailure(self, failure: Exception):
        if self.progress is not None:
            self.progress.close()
        self.progress = None
        message = QMessageBox(text=str(repr(failure)))
        message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message.setWindowTitle("Seed Generation Error")
        message.exec()
        if not isinstance(failure,RandomizerExceptions):
            raise failure

    def genTourneySeeds(self, extra_data: ExtraConfigurationData):
        self.tourney_seed_path.mkdir(parents=True, exist_ok=True)

        self.tourney_spoilers = TourneySeedSaver(self.tourney_seed_path,self.tourney_name)
        self.progress = QProgressDialog(f"Creating seeds...","Cancel",0,self.num_tourney_seeds,self)
        self.progress.setMinimumDuration(50)
        self.progress.setWindowTitle("Making your seeds, please wait...")
        self.progress.setCancelButton(None)
        self.progress.setModal(True)
        self.progress.forceShow()
        for seed_number in range(0,self.num_tourney_seeds):
            self.progress.setValue(seed_number)
            self.progress.setLabelText(f"Seed {seed_number+2}") # dialog updates are offset by one seed, so making display correct
            self.progress.show()
            characters = string.ascii_letters + string.digits
            seedString = (''.join(random.choice(characters) for i in range(30)))
            self.seedName.setText(seedString)
            tourney_rando_settings = self.make_rando_settings()
            if tourney_rando_settings is not None:
                zip_file, spoiler_log, enemy_log = generateSeed(tourney_rando_settings, extra_data)
                self.tourney_spoilers.add_seed(self.createSharedString(),tourney_rando_settings,spoiler_log)
        if self.progress:
            self.progress.close()
        self.progress = None
        self.tourney_spoilers.save()

    def _reload_presets(self):
        self.all_presets: list[SettingsPreset] = []
        user_presets = presets.list_user_presets()
        bundled_presets = presets.list_bundled_presets()
        self.all_presets.extend(user_presets)
        self.all_presets.extend(bundled_presets)

        menu = self.loadPresetsMenu
        menu.clear()
        if user_presets:
            for user_preset in user_presets:
                menu.addAction(user_preset.display_name, self._make_apply_preset(user_preset))
            menu.addSeparator()
        for bundled_preset in bundled_presets:
            menu.addAction(bundled_preset.display_name, self._make_apply_preset(bundled_preset))

    def _make_apply_preset(self, preset: SettingsPreset):
        return lambda: self._use_preset(preset)

    def _save_preset(self):
        if presets.prompt_save_preset(self, self.settings):
            self._reload_presets()

    def _import_preset(self):
        preset_name = presets.prompt_import_preset(self)
        if preset_name is not None:
            self._reload_presets()

            response = QMessageBox.question(
                self,
                "Presets",
                f"Preset [{preset_name}] imported.\n\nUse it now?",
                QMessageBox.Yes, QMessageBox.No
            )
            if response == QMessageBox.Yes:
                preset = next((p for p in self.all_presets if p.display_name == preset_name), None)
                if preset is None:
                    raise SettingsException(f"Preset {preset_name} not found")
                else:
                    self._use_preset(preset)

    def randomPreset(self):
        preset_select_dialog = RandomPresetDialog(self.all_presets)
        if preset_select_dialog.exec():
            random_preset_list = preset_select_dialog.save()
            if len(random_preset_list) == 0:
                message = QMessageBox(text="Need at least 1 preset selected")
                message.setWindowTitle("KH2 Seed Generator")
                message.exec()
            else:
                self.validate_seed_name()
                random.seed(self.seedName.text())
                selected_preset: SettingsPreset = random.choice(random_preset_list)
                self._use_preset(selected_preset)
                message = QMessageBox(text=f"Picked {selected_preset.display_name}")
                message.setWindowTitle("KH2 Seed Generator")
                message.exec()

    def validate_seed_name(self):
        seedString = self.seedName.text()
        if seedString == "":
            characters = string.ascii_letters + string.digits
            seedString = (''.join(random.choice(characters) for i in range(30)))
            self.seedName.setText(seedString)

    def randoRando(self):
        rando_rando_dialog = RandomSettingsDialog(self.settings)
        if rando_rando_dialog.exec():
            rando_rando_dialog.save()

    def randomize_the_settings(self):
        if self.settings.get(settingkey.RANDOMIZED_SETTINGS_ENABLED):
            print("randomizing settings")
            self.recalculate = False
            selected_random_settings = self.settings.get(settingkey.RANDOMIZED_SETTINGS)
            backup_shared_string = self.createSharedString()
            backup_settings = self.settings.settings_string()
            randomize_settings(self.settings,selected_random_settings)
            return backup_settings, backup_shared_string
        return None,None

    def openPresetFolder(self):
        os.startfile(appconfig.settings_presets_folder())

    def _use_preset(self, preset: SettingsPreset):
        self.recalculate = False
        self.settings.apply_settings_json(preset.settings_json())
        for widget in self.widgets:
            widget.update_widgets()
        self.recalculate = True
        self.get_num_enabled_locations()

    def shareSeed(self):
        output_text = self.createSharedString()

        pc.copy(output_text)
        message = QMessageBox(text="Copied seed to clipboard")
        message.setWindowTitle("KH2 Seed Generator")
        message.exec()

    def createSharedString(self):
        self.fixSeedName()

        # if seed hasn't been set yet, make one
        self.validate_seed_name()
        current_seed = self.seedName.text()

        shared_seed = SharedSeed(
            generator_version=LOCAL_UI_VERSION,
            seed_name=current_seed,
            spoiler_log=self.spoiler_log.isChecked(),
            settings_string=self.settings.settings_string(),
            tourney_gen=self.num_tourney_seeds>0
        )
        output_text = shared_seed.to_share_string()
        return output_text

    def receiveSeed(self):
        try:
            share_string = "".join(str(pc.paste()).strip().splitlines())
            shared_seed = SharedSeed.from_share_string(
                local_generator_version=LOCAL_UI_VERSION,
                share_string=share_string
            )
            self.apply_shared_seed(shared_seed)
        except ShareStringException as exception:
            message = QMessageBox(text=exception.message)
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()

    def apply_shared_seed(self, shared_seed: SharedSeed):
        # clear hash icons when loading a seed from clipboard
        self.clear_hash_icons()

        receipt_msg = "Received seed."
        if shared_seed.tourney_gen:
            receipt_msg = "Received tournament seed. Settings other than Cosmetics are now disabled."

            self.seedName.setDisabled(True)
            self.seedName.setHidden(True)
            self.spoiler_log.setDisabled(True)

            menu_bar = self.menuBar()
            menu_bar.removeAction(self.seedMenu.menuAction())
            menu_bar.removeAction(self.presetMenu.menuAction())
            menu_bar.removeAction(self.dailyMenu.menuAction())
            menu_bar.removeAction(self.randomizeSettings)
            menu_bar.removeAction(self.tourneySeeds)

            for w in self.widgets:
                if not isinstance(w, CosmeticsMenu):
                    w.disable_widgets()
        self.seedName.setText(shared_seed.seed_name)
        self.spoiler_log.setCheckState(Qt.Checked if shared_seed.spoiler_log else Qt.Unchecked)
        self.recalculate = False
        self.settings.apply_settings_string(shared_seed.settings_string)
        for widget in self.widgets:
            widget.update_widgets()
        self.recalculate = True
        self.get_num_enabled_locations()

        post_shared_seed = SharedSeed.from_share_string(local_generator_version=LOCAL_UI_VERSION,share_string = self.createSharedString())

        if post_shared_seed.seed_name != shared_seed.seed_name or post_shared_seed.spoiler_log != shared_seed.spoiler_log or post_shared_seed.settings_string != shared_seed.settings_string:
            print(post_shared_seed.seed_name)
            print(shared_seed.seed_name)
            print(post_shared_seed.seed_name != shared_seed.seed_name)
            print(post_shared_seed.spoiler_log)
            print(shared_seed.spoiler_log)
            print(post_shared_seed.spoiler_log != shared_seed.spoiler_log)
            print(post_shared_seed.settings_string)
            print(shared_seed.settings_string)
            print(post_shared_seed.settings_string != shared_seed.settings_string)
            message = QMessageBox(text="There was an error getting the correct settings, try restarting the generator and trying again. If that fails, ask for the zip from the sharer.")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
        else:
            message = QMessageBox(text=receipt_msg)
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()

    def openkh_folder_getter(self):
        if configui.openkh_folder_getter():
            self.cosmetics_menu.reload_cosmetic_widgets()

    def custom_music_folder_getter(self):
        if configui.custom_music_folder_getter():
            self.cosmetics_menu.reload_cosmetic_widgets()

    def custom_visuals_folder_getter(self):
        if configui.custom_visuals_folder_getter():
            self.cosmetics_menu.reload_cosmetic_widgets()

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    @staticmethod
    def _dev_create_recolor():
        DevCreateRecolorDialog().exec()


if __name__ == "__main__":
    app = QApplication([])

    QtGui.QFontDatabase.addApplicationFont(resource_path('static/KHMenu.otf'))

    window = KH2RandomizerApp()

    stylesheet = app.styleSheet()
    with open(resource_path('UI/stylesheet.css')) as file:
        css_resources = {
            "background-primary": theme.BackgroundPrimary,
            "background-dark": theme.BackgroundDark,
            "link-color": theme.LinkColor,
            "selection-color": theme.SelectionColor,
            "selection-border-color": theme.SelectionBorderColor,
            "ability-on": Path(resource_path("static/icons/misc/ability-on.png")).as_posix(),
            "down-arrow": Path(resource_path("static/icons/misc/arrow-down.png")).as_posix(),
            "up-arrow": Path(resource_path("static/icons/misc/arrow-up.png")).as_posix(),
        }
        app.setStyleSheet((stylesheet + file.read().format(**os.environ)) % css_resources)

    extracted_data_path = Path("extracted_data/version.txt")
    data_version = "None"
    if extracted_data_path.is_file():
        with open(extracted_data_path.absolute(), "r") as f:
            data_version = f.read().strip()
    if data_version != EXTRACTED_DATA_UPDATE_VERSION:
        progress = QProgressDialog(f"Checking for data files...", "Cancel", 0, 0, None)
        progress.setWindowTitle("First Time Data Extraction...")
        progress.setCancelButton(None)
        progress.setModal(True)
        progress.show()
        # we need to extract the zip
        path_to_zip = resource_path("extracted_data.zip")
        with zipfile.ZipFile(path_to_zip,'r') as zip_ref:
            zip_ref.extractall(".")
        progress.close()

    window.recalculate = True
    try:
        window.get_num_enabled_locations()
    except (SettingsException,ValueError):
        window.resetSettings()
        pass
    window.show()

    app_config = appconfig.read_app_config()

    if 'window_position' in app_config:
        window.remember_window_position_action.setChecked(True)
        window_position = app_config['window_position']
        window.resize(window_position['width'], window_position['height'])
        window.move(window_position['x'], window_position['y'])
    else:
        window.remember_window_position_action.setChecked(False)
        screen_geometry = window.screen().geometry()
        top_left = screen_geometry.topLeft()
        bottom_right = screen_geometry.bottomRight()
        screen_width = bottom_right.x() - top_left.x()
        screen_height = bottom_right.y() - top_left.y()

        # This is basically the best effort to get the window sized such that there aren't any scrollbars.
        # It might need to get updated over time if any of the tabs gets any bigger.
        # As of when this was written, 1400x900 fits everything other than when progression hints is turned on.
        # If the screen is smaller than that, try to make it big enough without going full width/height.
        window.resize(min(1400, screen_width - 64), min(900, screen_height - 64))

        center = screen_geometry.center()
        window.move(center.x() - window.width() / 2, center.y() - window.height() / 2)

    sys.exit(app.exec())
