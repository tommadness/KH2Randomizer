import os
import sys
from Class.exceptions import CantAssignItemException, RandomizerExceptions
from List.configDict import locationType


from Module.resources import resource_path

# Keep the setting of the environment variable as close to the top as possible.
# This needs to happen before anything Boss/Enemy Rando gets loaded for the sake of the distributed binary.
os.environ["USE_KH2_GITPATH"] = resource_path("extracted_data")


import datetime
import json
import random
import re
import string
from pathlib import Path

import pyperclip as pc
import pytz
# from PIL import Image
from PySide6 import QtGui
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QMenu, QPushButton, QCheckBox, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog,
    QFileDialog, QMessageBox, QProgressDialog, QProgressBar, QSizePolicy
)

from qt_material import apply_stylesheet
from Class import settingkey
from Class.seedSettings import RandoRandoSettings, SeedSettings, getRandoRandoTooltip
from Module.dailySeed import getDailyModifiers
from Module.generate import generateSeed
from Module.newRandomize import Randomizer, RandomizerSettings
from Module.seedshare import SharedSeed, ShareStringException
from UI.FirstTimeSetup.firsttimesetup import FirstTimeSetup
from UI.Submenus.BossEnemyMenu import BossEnemyMenu
from UI.Submenus.CosmeticsMenu import CosmeticsMenu
from UI.Submenus.HintsMenu import HintsMenu
from UI.Submenus.ItemPlacementMenu import ItemPlacementMenu
from UI.Submenus.KeybladeMenu import KeybladeMenu
from UI.Submenus.RewardLocationsMenu import RewardLocationsMenu
from UI.Submenus.SeedModMenu import SeedModMenu
from UI.Submenus.SoraMenu import SoraMenu
from UI.Submenus.StartingMenu import StartingMenu

LOCAL_UI_VERSION = '2.1.3'

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


AUTOSAVE_FOLDER = "auto-save"
PRESET_FOLDER = "presets"


class GenSeedThread(QThread):
    finished = Signal(object)
    failed = Signal(Exception)

    def provideData(self,data,rando_settings):
        self.data=data
        self.rando_settings = rando_settings
        self.zip_file = None

    def run(self):
        try:
            zip_file,spoiler_log = generateSeed(self.rando_settings, self.data)
            self.finished.emit((zip_file,spoiler_log))
        except Exception as e:
            self.failed.emit(e)


class KH2RandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UTC = pytz.utc
        self.startTime = datetime.datetime.now(self.UTC)
        self.dailySeedName = self.startTime.strftime('%d-%m-%Y')
        self.mods = getDailyModifiers(self.startTime)
        self.progress = None
        self.spoiler_log_output = "<html>No spoiler log generated</html>"
        self.tourney_generator = False

        self.settings = SeedSettings()

        if not os.path.exists(AUTOSAVE_FOLDER):
            os.makedirs(AUTOSAVE_FOLDER)
        auto_settings_save_path = os.path.join(AUTOSAVE_FOLDER, 'auto-save.json')
        if os.path.exists(auto_settings_save_path):
            with open(auto_settings_save_path, 'r') as source:
                try:
                    auto_settings_json = json.loads(source.read())
                    self.settings.apply_settings_json(auto_settings_json, include_private=True)
                except Exception:
                    print('Unable to apply last settings - will use defaults')
                    pass
        tourney_generator_config = Path("tourney_gen.txt")
        if os.path.exists(tourney_generator_config):
            self.tourney_generator = True

        random.seed(str(datetime.datetime.now()))
        self.setWindowTitle("KH2 Randomizer Seed Generator ({0})".format(LOCAL_UI_VERSION))
        self.setWindowIcon(QIcon(resource_path("Module/icon.png")))
        self.setMinimumWidth(1000)
        self.setup = None
        pagelayout = QVBoxLayout()
        seed_layout = QHBoxLayout()
        progress_layout = QHBoxLayout()
        submit_layout = QHBoxLayout()
        self.tabs = QTabWidget()

        self._configure_menu_bar()

        self.preset_json = {}
        if not os.path.exists(PRESET_FOLDER):
            os.makedirs(PRESET_FOLDER)
        for file in os.listdir(PRESET_FOLDER):
            preset_name, extension = os.path.splitext(file)
            if extension == '.json':
                with open(os.path.join(PRESET_FOLDER, file), 'r') as presetData:
                    settings_json = json.loads(presetData.read())
                    self.preset_json[preset_name] = settings_json

        pagelayout.addLayout(seed_layout)
        pagelayout.addWidget(self.tabs)        
        pagelayout.addLayout(progress_layout)
        pagelayout.addLayout(submit_layout)

        seed_layout.addWidget(QLabel("Seed"))
        self.seedName=QLineEdit()
        self.seedName.setPlaceholderText("Leave blank for a random seed")
        seed_layout.addWidget(self.seedName)

        for x in self.preset_json.keys():
            if x != 'BaseDailySeed':
                self.presetsMenu.addAction(x, lambda x=x: self.usePreset(x))

        self.spoiler_log = QCheckBox("Make Spoiler Log")
        self.spoiler_log.setCheckState(Qt.Checked)
        seed_layout.addWidget(self.spoiler_log)
        
        self.rando_rando = QCheckBox("Rando Settings (Experimental)")
        self.rando_rando.setToolTip(getRandoRandoTooltip())
        self.rando_rando.setCheckState(Qt.Unchecked)
        seed_layout.addWidget(self.rando_rando)

        self.widgets = [
            SoraMenu(self.settings),
            StartingMenu(self.settings),
            HintsMenu(self.settings),
            KeybladeMenu(self.settings),
            RewardLocationsMenu(self.settings),
            ItemPlacementMenu(self.settings),
            SeedModMenu(self.settings),
            BossEnemyMenu(self.settings),
            CosmeticsMenu(self.settings),
        ]

        for i in range(len(self.widgets)):
            self.tabs.addTab(self.widgets[i],self.widgets[i].getName())

        
        self.progress_label = QLabel("Progress Placeholder")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setFixedWidth(360)
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)

        submit_layout.addWidget(QLabel("Seed Hash"))

        self.hashIconPath = Path(resource_path("static/seed-hash-icons"))
        self.hashIcons = []
        for i in range(7):
            self.hashIcons.append(QLabel())
            self.hashIcons[-1].blockSignals(True)
            submit_layout.addWidget(self.hashIcons[-1])
            
        self.clear_hash_icons()

        submit_layout.addSpacing(16)

        self.emu_button = QPushButton("Generate Seed (PCSX2)")
        self.emu_button.clicked.connect(lambda : self.makeSeed("PCSX2"))
        submit_layout.addWidget(self.emu_button, stretch=1)
        self.emu_button.setVisible(False)

        self.pc_button = QPushButton("Generate Seed (PC)")
        self.pc_button.clicked.connect(lambda : self.makeSeed("PC"))
        submit_layout.addWidget(self.pc_button, stretch=1)
        self.pc_button.setVisible(False)


        self.both_button = QPushButton("Generate Seed (PC/PCSX2)")
        self.both_button.clicked.connect(lambda : self.makeSeed("Both"))
        submit_layout.addWidget(self.both_button, stretch=1)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        self.recalculate = False
        settings_keys = self.settings._filtered_settings(True).keys()
        for key in settings_keys:
            self.settings.observe(key,self.get_num_enabled_locations)

    def _configure_menu_bar(self):
        menu_bar = self.menuBar()
        self.presetMenu = QMenu("Preset")
        self.presetMenu.addAction("Open Preset Folder", self.openPresetFolder)
        self.presetsMenu = QMenu("Presets")
        self.seedMenu = QMenu("Share Seed")
        self.seedMenu.addAction("Save Seed to Clipboard", self.shareSeed)
        self.seedMenu.addAction("Load Seed from Clipboard", self.receiveSeed)
        self.presetMenu.addAction("Save Settings as New Preset", self.savePreset)
        self.presetMenu.addMenu(self.presetsMenu)
        menu_bar.addMenu(self.seedMenu)
        menu_bar.addMenu(self.presetMenu)

        menu_bar.addAction("Load Daily Seed", self.loadDailySeed)
        menu_bar.addAction("Find Extracted PC KH Data",self.extractedFilesGetter)
        menu_bar.addAction("About", self.showAbout)

    def closeEvent(self, e):
        settings_json = self.settings.settings_json(include_private=True)
        with open(os.path.join(AUTOSAVE_FOLDER, 'auto-save.json'), 'w') as presetData:
            presetData.write(json.dumps(settings_json, indent=4, sort_keys=True))
        e.accept()

    def loadDailySeed(self):
        self.seedName.setText(self.dailySeedName)
        self.recalculate = False
        self.settings.apply_settings_json(self.preset_json['BaseDailySeed'])

        # use the modifications to change the preset
        mod_string = f'Updated settings for Daily Seed {self.startTime.strftime("%a %b %d %Y")}\n\n'
        for m in self.mods:
            m.local_modifier(self.settings)
            mod_string += m.name + ' - ' + m.description + '\n'

        for widget in self.widgets:
            widget.update_widgets()
        self.recalculate = True
        self.get_num_enabled_locations()

        self.fixSeedName()

        message = QMessageBox(text=mod_string)
        message.setWindowTitle('KH2 Seed Generator - Daily Seed')
        message.exec()

    def fixSeedName(self):
        new_string = re.sub(r'[^a-zA-Z0-9]', '', self.seedName.text())
        self.seedName.setText(new_string)
        if self.tourney_generator:
            self.spoiler_log.setChecked(False)

    def make_rando_settings(self):
        if self.tourney_generator:
            makeSpoilerLog = False
        else:
            makeSpoilerLog = self.spoiler_log.isChecked()

        # seed
        seedString = self.seedName.text()
        if seedString == "":
            characters = string.ascii_letters + string.digits
            seedString = (''.join(random.choice(characters) for i in range(30)))
            self.seedName.setText(seedString)

        try:
            if self.rando_rando.isChecked():
                print("Generating randomized settings...")
                random.seed(seedString)
                _ = RandoRandoSettings(self.settings)
            rando_settings = RandomizerSettings(seedString,makeSpoilerLog,LOCAL_UI_VERSION,self.settings,self.createSharedString())
            # update the seed hash display
            self.update_ui_hash_icons(rando_settings)

            return rando_settings
        except RandomizerExceptions as e:
            self.handleFailure(e)
            return None

    def update_ui_hash_icons(self, rando_settings):
        # self.icons = []
        for index, icon in enumerate(rando_settings.seedHashIcons):
            self.hashIcons[index].setPixmap(QPixmap(str(self.hashIconPath.absolute()) + '/' + icon + '.png'))
            # self.icons.append(icon)

    def clear_hash_icons(self):
        for i in range(7):
            self.hashIcons[i].setPixmap(QPixmap(str(self.hashIconPath.absolute())+"/"+"question-mark.png"))

    # def make_stitched_hash_picture(self):
    #     stitched_image = Image.new('RGB',(48*len(self.icons),48))
    #     for index, icon in enumerate(self.icons):
    #         stitched_image.paste(im=Image.open(str(self.hashIconPath.absolute())+"/"+icon+".png"),box=(48*index,0))

    def get_num_enabled_locations(self):
        if self.recalculate:
            try:
                rando_settings = self.make_rando_settings()
                dummy_rando = Randomizer(rando_settings,True)
                split_pc_emu = False
                split_pc_emu = split_pc_emu or self.settings.get(settingkey.COMMAND_MENU) != "vanilla"
                split_pc_emu = split_pc_emu or len(self.settings.get(settingkey.BGM_OPTIONS)) != 0
                split_pc_emu = split_pc_emu or len(self.settings.get(settingkey.BGM_GAMES)) != 0
                split_pc_emu = split_pc_emu or self.settings.get(settingkey.CUPS_GIVE_XP)
                split_pc_emu = split_pc_emu or self.settings.get(settingkey.REMOVE_DAMAGE_CAP)
                split_pc_emu = split_pc_emu or (locationType.Puzzle.name in self.settings.get(settingkey.MISC_LOCATIONS_WITH_REWARDS))
                split_pc_emu = split_pc_emu or (locationType.SYNTH.name in self.settings.get(settingkey.MISC_LOCATIONS_WITH_REWARDS))
                split_pc_emu = split_pc_emu or rando_settings.enemy_options["boss"] != "Disabled"
                split_pc_emu = split_pc_emu or rando_settings.enemy_options["enemy"] != "Disabled"
                # split_pc_emu = split_pc_emu or self.settings.get(settingkey.TT1_JAILBREAK)

                
                disable_emu = False
                disable_emu = disable_emu or rando_settings.enemy_options["enemy"] == "Wild"
                disable_emu = disable_emu or rando_settings.enemy_options["bosses_replace_enemies"]
                disable_emu = disable_emu or len(self.settings.get(settingkey.BGM_OPTIONS)) != 0
                disable_emu = disable_emu or len(self.settings.get(settingkey.BGM_GAMES)) != 0
                # disable_emu = disable_emu or self.settings.get(settingkey.TT1_JAILBREAK)


                self.emu_button.setVisible(split_pc_emu)
                self.pc_button.setVisible(split_pc_emu)
                self.both_button.setVisible(not split_pc_emu)
                self.emu_button.setEnabled(not disable_emu)

            except CantAssignItemException as e:
                pass
            text = f"Items: {dummy_rando.num_available_items} / Locations: {dummy_rando.num_valid_locations}"
            self.progress_bar.setRange(0,dummy_rando.num_valid_locations)
            if dummy_rando.num_valid_locations < dummy_rando.num_available_items:
                self.progress_bar.setValue(dummy_rando.num_valid_locations)
                text = "Too many "+text
            else:
                self.progress_bar.setValue(dummy_rando.num_available_items)
            self.progress_label.setText(text)

    def makeSeed(self,platform):
        self.fixSeedName()
        if self.tourney_generator:
            message = QMessageBox(text="Tourney Mode in Use. Spoiler will be generated outside the zip, and cosmetics disabled.")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
            # disable all cosmetics, generate a spoiler log, but don't put it in the zip
            data = {
                'platform': platform,
                'cmdMenuChoice': "vanilla",
                'randomBGM': {
                    "options": [],
                    "games": []
                },
                'tourney': True
            }
        else:
            data = {
                'platform': platform,
                'cmdMenuChoice': self.settings.get(settingkey.COMMAND_MENU),
                'randomBGM': {
                    "options": self.settings.get(settingkey.BGM_OPTIONS),
                    "games": self.settings.get(settingkey.BGM_GAMES)
                },
                'tourney': False
            }

        rando_settings = self.make_rando_settings()
        if rando_settings is not None:
            self.genSeed(data,rando_settings)

    def downloadSeed(self):
        last_seed_folder_txt = Path(AUTOSAVE_FOLDER) / 'last_seed_folder.txt'
        output_file_name = 'randoseed.zip'
        if last_seed_folder_txt.is_file():
            last_seed_folder = Path(last_seed_folder_txt.read_text().strip())
            if last_seed_folder.is_dir():
                output_file_name = str(last_seed_folder / output_file_name)

        saveFileWidget = QFileDialog()
        saveFileWidget.setNameFilters(["Zip Seed File (*.zip)"])
        outfile_name, _ = saveFileWidget.getSaveFileName(self, "Save seed zip", output_file_name, "Zip Seed File (*.zip)")
        spoiler_outfile = outfile_name
        if outfile_name!="":
            if not outfile_name.endswith(".zip"):
                outfile_name+=".zip"
            with open(outfile_name, "wb") as out_zip:
                out_zip.write(self.zip_file.getbuffer())

            last_seed_folder_txt.write_text(str(Path(outfile_name).parent))

            if self.tourney_generator:
                if not spoiler_outfile.endswith(".html"):
                    spoiler_outfile+=".html"
                with open(spoiler_outfile, "w") as out_html:
                    out_html.write(self.spoiler_log_output)

        self.zip_file=None
        self.spoiler_log_output=None

    def handleResult(self,result):
        self.progress.close()
        self.progress = None
        self.zip_file = result[0]
        self.spoiler_log_output = result[1] if result[1] else "<html>No spoiler log generated</html>"
        self.downloadSeed()

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

    def genSeed(self,data,rando_settings):
        self.thread = QThread()
        displayedSeedName = rando_settings.random_seed
        self.progress = QProgressDialog(f"Creating seed with name {displayedSeedName}","",0,0,None)
        self.progress.setWindowTitle("Making your Seed, please wait...")
        self.progress.setCancelButton(None)
        self.progress.setModal(True)
        self.progress.show()

        self.thread = GenSeedThread()
        self.thread.provideData(data,rando_settings)
        self.thread.finished.connect(self.handleResult)
        self.thread.failed.connect(self.handleFailure)
        self.thread.start()

    def savePreset(self):
        preset_name, ok = QInputDialog.getText(self, 'Make New Preset', 'Enter a name for your preset...')

        if ok:
            # add current settings to saved presets, add to current preset list, change preset selection.
            settings_json = self.settings.settings_json()
            self.preset_json[preset_name] = settings_json
            self.presetsMenu.addAction(preset_name, lambda: self.usePreset(preset_name))
            with open(os.path.join(PRESET_FOLDER, preset_name + '.json'), 'w') as presetData:
                presetData.write(json.dumps(settings_json, indent=4, sort_keys=True))

    def openPresetFolder(self):
        os.startfile(PRESET_FOLDER)

    def usePreset(self, preset_name: str):
        settings_json = self.preset_json[preset_name]
        self.recalculate = False
        self.settings.apply_settings_json(settings_json)
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
        current_seed = self.seedName.text()
        if current_seed == "":
            characters = string.ascii_letters + string.digits
            current_seed = (''.join(random.choice(characters) for i in range(30)))
            self.seedName.setText(current_seed)

        shared_seed = SharedSeed(
            generator_version=LOCAL_UI_VERSION,
            seed_name=current_seed,
            spoiler_log=self.spoiler_log.isChecked(),
            settings_string=self.settings.settings_string(),
            tourney_gen=self.tourney_generator
        )
        output_text = shared_seed.to_share_string()
        return output_text

    def receiveSeed(self):
        try:
            shared_seed = SharedSeed.from_share_string(
                local_generator_version=LOCAL_UI_VERSION,
                share_string=str(pc.paste()).strip()
            )
            self.tourney_generator = False
        except ShareStringException as exception:
            message = QMessageBox(text=exception.message)
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
            return

        # clear hash icons when loading a seed from clipboard
        self.clear_hash_icons()

        if shared_seed.tourney_gen:
            self.seedName.setDisabled(True)
            self.seedName.setHidden(True)
            self.spoiler_log.setDisabled(True)
            self.rando_rando.setDisabled(True)
            for w in self.widgets:
                if not isinstance(w,CosmeticsMenu):
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
            print(shared_seed.settings_string)
            print(post_shared_seed.settings_string)
            message = QMessageBox(text="There was an error getting the correct settings from the clipboard, try restarting the generator and trying again. If that fails, ask for the zip from the sharer.")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
        else:
            message = QMessageBox(text="Received seed from clipboard")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()

    def extractedFilesGetter(self):
        saveFileWidget = QFileDialog()
        selected_directory = saveFileWidget.getExistingDirectory()

        if selected_directory is None or selected_directory == "":
            return
        
        configPath = Path("music-rando-config.json")

        with open(str(configPath.absolute()),'w') as music_config:
            out_data = {}
            out_data["game_extract_folder"] = selected_directory
            music_config.write(json.dumps(out_data))
        message = QMessageBox(text="Restart the generator to add the music options to the menu.")
        message.setWindowTitle("KH2 Seed Generator")
        message.exec()

        

    def firstTimeSetup(self):
        print("First Time Setup")
        if self.setup is None:
            self.setup = FirstTimeSetup()
            self.setup.show()

    def showAbout(self):
        aboutText = '''
Kingdom Hearts II Final Mix Zip Seed Generator Version {0}<br>
Created by Thundrio, Tommadness, and ZakTheRobot<br><br>

Thank you to all contributors, testers, and advocates.<br><br>

<a href="https://tommadness.github.io/KH2Randomizer" style="color: #4dd0e1">Website</a><br>
<a href="https://github.com/tommadness/KH2Randomizer" style="color: #4dd0e1">Github Link</a><br>
<a href="https://discord.gg/KH2FMRando" style="color: #4dd0e1">KH2 Randomizer Discord</a><br><br>

<a href="https://github.com/tommadness/KH2Randomizer/tree/local_ui#acknowledgements" style="color: #4dd0e1">Acknowledgements</a><br><br>

Uses the qt-material library for theming.<br>Copyright (c) 2020, GCPDS
<a href="https://github.com/UN-GCPDS/qt-material/blob/master/LICENSE" style="color: #4dd0e1">License</a>



'''.format(LOCAL_UI_VERSION)
        message = QMessageBox(text=aboutText)
        message.setTextFormat(Qt.RichText)
        message.setWindowTitle("About")
        message.setWindowIcon(QIcon(resource_path("Module/icon.png")))
        message.exec()


if __name__=="__main__":
    app = QApplication([])

    QtGui.QFontDatabase.addApplicationFont(resource_path('static/KHMenu.otf'))

    window = KH2RandomizerApp()

    apply_stylesheet(app, theme='dark_cyan.xml')
    stylesheet = app.styleSheet()
    with open(resource_path('UI/stylesheet.css')) as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    window.recalculate = True
    window.get_num_enabled_locations()
    window.show()
    #commenting out first time setup for 2.999 version
    # configPath = Path("rando-config.yml")
    # if not configPath.is_file() or not os.environ.get("ALWAYS_SETUP") is None:
    #     window.firstTimeSetup()

    sys.exit(app.exec())
