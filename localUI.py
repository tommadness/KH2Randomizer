import os
import sys


# Keep resource_path definition and the setting of the environment variable as close to the top as possible.
# These need to happen before anything Boss/Enemy Rando gets loaded for the sake of the distributed binary.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


os.environ["USE_KH2_GITPATH"] = resource_path("extracted_data")


import datetime
import json
import random
import re
import string
from pathlib import Path

import pyperclip as pc
import pytz
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QMenu, QPushButton, QCheckBox, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog,
    QFileDialog, QMenuBar, QMessageBox, QProgressDialog
)

from Class import seedSettings, settingkey
from Class.seedSettings import SeedSettings
from List.configDict import locationType
from List.hashTextEntries import generateHashIcons
from Module.dailySeed import getDailyModifiers
from Module.randomizePage import randomizePage
from UI.FirstTimeSetup.firsttimesetup import FirstTimeSetup
from UI.Submenus.BossEnemyMenu import BossEnemyMenu
from UI.Submenus.CosmeticsMenu import CosmeticsMenu
from UI.Submenus.HintsMenu import HintsMenu
from UI.Submenus.ItemPlacementMenu import ItemPlacementMenu
from UI.Submenus.KeybladeMenu import KeybladeMenu
from UI.Submenus.MiscMenu import MiscMenu
from UI.Submenus.SeedModMenu import SeedModMenu
from UI.Submenus.SoraMenu import SoraMenu
from UI.Submenus.StartingMenu import StartingMenu
from UI.Submenus.WorldMenu import WorldMenu

SEED_SPLITTER = '---'
LOCAL_UI_VERSION = '1.99.0'


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


def convert_seed_to_share_string(seed: dict) -> str:
    seed_name: str = seed['seed_name']
    spoiler_log = '1' if seed['spoiler_log'] else '0'
    settings_string: str = seed['settings_string']
    return SEED_SPLITTER.join([seed_name, spoiler_log, settings_string])


def convert_share_string_to_seed(share_string: str) -> dict:
    parts = share_string.split(SEED_SPLITTER)
    return {
        'seed_name': parts[0],
        'spoiler_log': True if parts[1] == '1' else False,
        'settings_string': parts[2]
    }


AUTOSAVE_FOLDER = "auto-save"
PRESET_FOLDER = "presets"


class GenSeedThread(QThread):
    finished = Signal(object)

    def provideData(self,data,session):
        self.data=data
        self.session = session
        self.zip_file = None

    def run(self):
        zip_file = randomizePage(self.data,self.session,local_ui=True)
        self.finished.emit(zip_file)


class KH2RandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UTC = pytz.utc
        self.startTime = datetime.datetime.now(self.UTC)
        self.dailySeedName = self.startTime.strftime('%d-%m-%Y')
        self.mods = getDailyModifiers(self.startTime)

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

        with open(resource_path("UI/stylesheet.qss"),"r") as style:
            data = style.read()
            self.setStyleSheet(data)

        random.seed(str(datetime.datetime.now()))
        self.setWindowTitle("KH2 Randomizer Seed Generator")
        self.setWindowIcon(QIcon(resource_path("Module/icon.png")))
        self.setMinimumWidth(1000)
        self.setup = None
        pagelayout = QVBoxLayout()
        seed_layout = QHBoxLayout()
        submit_layout = QHBoxLayout()
        self.seedhashlayout = QHBoxLayout()
        self.tabs = QTabWidget()

        self.menuBar = QMenuBar()
        self.presetMenu = QMenu("Preset")
        self.presetMenu.addAction("Open Preset Folder", self.openPresetFolder)
        self.presetsMenu = QMenu("Presets")
        self.seedMenu = QMenu("Share Seed")
        self.seedMenu.addAction("Save Seed to Clipboard", self.shareSeed)
        self.seedMenu.addAction("Load Seed from Clipboard", self.receiveSeed)
        self.presetMenu.addAction("Save Settings as New Preset", self.savePreset)
        self.presetMenu.addMenu(self.presetsMenu)
        self.menuBar.addMenu(self.seedMenu)
        self.menuBar.addMenu(self.presetMenu)

        # populate a menu item for the daily seed
        self.menuBar.addAction("Load Daily Seed", self.loadDailySeed)

        self.menuBar.addAction("About", self.showAbout)

        self.preset_json = {}
        if not os.path.exists(PRESET_FOLDER):
            os.makedirs(PRESET_FOLDER)
        for file in os.listdir(PRESET_FOLDER):
            preset_name, extension = os.path.splitext(file)
            if extension == '.json':
                with open(os.path.join(PRESET_FOLDER, file), 'r') as presetData:
                    settings_json = json.loads(presetData.read())
                    self.preset_json[preset_name] = settings_json

        pagelayout.addWidget(self.menuBar)
        pagelayout.addLayout(seed_layout)
        pagelayout.addWidget(self.tabs)
        pagelayout.addLayout(submit_layout)
        pagelayout.addLayout(self.seedhashlayout)
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

        self.widgets = [
            SoraMenu(self.settings),
            StartingMenu(self.settings),
            HintsMenu(self.settings),
            KeybladeMenu(self.settings),
            WorldMenu(self.settings),
            MiscMenu(self.settings),
            SeedModMenu(self.settings),
            ItemPlacementMenu(self.settings),
            BossEnemyMenu(self.settings),
            CosmeticsMenu(self.settings),
        ]

        for i in range(len(self.widgets)):
            self.tabs.addTab(self.widgets[i],self.widgets[i].getName())


        submitButton = QPushButton("Generate Seed (PCSX2)")
        submitButton.clicked.connect(lambda : self.makeSeed("PCSX2"))
        submit_layout.addWidget(submitButton)

        submitButton = QPushButton("Generate Seed (PC)")
        submitButton.clicked.connect(lambda : self.makeSeed("PC"))
        submit_layout.addWidget(submitButton)

        self.seedhashlayout.addWidget(QLabel("Seed Hash"))

        self.hashIconPath = Path(resource_path("static/seed-hash-icons"))
        self.hashIcons = []
        for i in range(7):
            self.hashIcons.append(QLabel())
            self.hashIcons[-1].blockSignals(True)
            #self.hashIcons[-1].setIconSize(QSize(50,50))
            self.hashIcons[-1].setPixmap(QPixmap(str(self.hashIconPath.absolute())+"/"+"question-mark.png"))
            self.seedhashlayout.addWidget(self.hashIcons[-1])

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def closeEvent(self, e):
        settings_json = self.settings.settings_json(include_private=True)
        with open(os.path.join(AUTOSAVE_FOLDER, 'auto-save.json'), 'w') as presetData:
            presetData.write(json.dumps(settings_json, indent=4, sort_keys=True))
        e.accept()

    def loadDailySeed(self):
        self.seedName.setText(self.dailySeedName)
        self.settings.apply_settings_json(self.preset_json['BaseDailySeed'])

        # use the modifications to change the preset
        mod_string = f'Updated settings for Daily Seed {self.startTime.strftime("%a %b %d %Y")}\n\n'
        for m in self.mods:
            m.local_modifier(self.settings)
            mod_string += m.name + ' - ' + m.description + '\n'

        for widget in self.widgets:
            widget.update_widgets()

        self.fixSeedName()

        message = QMessageBox(text=mod_string)
        message.setWindowTitle('KH2 Seed Generator - Daily Seed')
        message.exec()

    def fixSeedName(self):
        new_string = re.sub(r'[^a-zA-Z0-9]', '', self.seedName.text())
        self.seedName.setText(new_string)

    def make_seed_session(self):
        makeSpoilerLog = self.spoiler_log.isChecked()

        session={}

        # seed
        session["seed"] = self.seedName.text()
        if session["seed"] == "":
            characters = string.ascii_letters + string.digits
            session["seed"] = (''.join(random.choice(characters) for i in range(30)))

        # make the seed hash dependent on ui version and if a spoiler log is generated or not.
        random.seed(session["seed"]+LOCAL_UI_VERSION+str(makeSpoilerLog))

        # seedHashIcons
        session["seedHashIcons"] = generateHashIcons()

        # includeList
        include_list = []
        session["includeList"] = include_list
        include_list_keys = [
            (settingkey.FORM_LEVEL_REWARDS, 'Form Levels'),
            (settingkey.CRITICAL_BONUS_REWARDS, 'Critical Bonuses'),
            (settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS, 'Garden of Assemblage'),
        ]
        for key in include_list_keys:
            if self.settings.get(key[0]):
                include_list.append(key[1])
        for location in self.settings.get(settingkey.WORLDS_WITH_REWARDS):
            include_list.append(locationType[location].value)
        for location in self.settings.get(settingkey.SUPERBOSSES_WITH_REWARDS):
            include_list.append(locationType[location].value)
        for location in self.settings.get(settingkey.MISC_LOCATIONS_WITH_REWARDS):
            include_list.append(locationType[location].value)

        # levelChoice
        session['levelChoice'] = self.settings.get(settingkey.SORA_LEVELS)

        # startingInventory
        session['startingInventory'] = [int(value) for value in self.settings.get(settingkey.STARTING_INVENTORY)]

        # itemPlacementDifficulty
        session['itemPlacementDifficulty'] = self.settings.get(settingkey.ITEM_PLACEMENT_DIFFICULTY)

        # seedModifiers
        seed_modifiers = []
        session['seedModifiers'] = seed_modifiers
        seed_modifier_keys = [
            (settingkey.MAX_LOGIC_ITEM_PLACEMENT, 'Max Logic Item Placement'),
            (settingkey.REVERSE_RANDO, 'Reverse Rando'),
            (settingkey.LIBRARY_OF_ASSEMBLAGE, 'Library of Assemblage'),
            (settingkey.SCHMOVEMENT, 'Schmovement'),
            (settingkey.GLASS_CANNON, 'Glass Cannon'),
            (settingkey.BETTER_JUNK, 'Better Junk'),
            (settingkey.START_NO_AP, 'Start with No AP'),
            (settingkey.REMOVE_DAMAGE_CAP, 'Remove Damage Cap')
        ]
        for key in seed_modifier_keys:
            if self.settings.get(key[0]):
                seed_modifiers.append(key[1])
        if self.settings.get(settingkey.ABILITY_POOL) == 'randomize':
            seed_modifiers.append('Randomize Ability Pool')

        # update the seed hash display
        for index, icon in enumerate(session['seedHashIcons']):
            self.hashIcons[index].setPixmap(QPixmap(str(self.hashIconPath.absolute()) + '/' + icon + '.png'))

        # spoilerLog
        session["spoilerLog"] = makeSpoilerLog

        # hintsType/reportDepth/preventSelfHinting/allowProofHinting
        session['hintsType'] = self.settings.get(settingkey.HINT_SYSTEM)
        session['reportDepth'] = self.settings.get(settingkey.REPORT_DEPTH)
        session['preventSelfHinting'] = self.settings.get(settingkey.PREVENT_SELF_HINTING)
        session['allowProofHinting'] = self.settings.get(settingkey.ALLOW_PROOF_HINTING)

        # promiseCharm
        session['promiseCharm'] = self.settings.get(settingkey.ENABLE_PROMISE_CHARM)

        # keybladeAbilities
        keyblade_abilities = []
        session['keybladeAbilities'] = keyblade_abilities
        if self.settings.get(settingkey.SUPPORT_KEYBLADE_ABILITIES):
            keyblade_abilities.append('Support')
        if self.settings.get(settingkey.ACTION_KEYBLADE_ABILITIES):
            keyblade_abilities.append('Action')

        # keybladeMinStat
        session['keybladeMinStat'] = self.settings.get(settingkey.KEYBLADE_MIN_STAT)

        # keybladeMaxStat
        session['keybladeMaxStat'] = self.settings.get(settingkey.KEYBLADE_MAX_STAT)

        # soraExpMult
        session['soraExpMult'] = self.settings.get(settingkey.SORA_EXP_MULTIPLIER)

        # formExpMult
        session['formExpMult'] = {
            '0': self.settings.get(settingkey.SUMMON_EXP_MULTIPLIER),
            '1': self.settings.get(settingkey.VALOR_EXP_MULTIPLIER),
            '2': self.settings.get(settingkey.WISDOM_EXP_MULTIPLIER),
            '3': self.settings.get(settingkey.LIMIT_EXP_MULTIPLIER),
            '4': self.settings.get(settingkey.MASTER_EXP_MULTIPLIER),
            '5': self.settings.get(settingkey.FINAL_EXP_MULTIPLIER)
        }

        # enemyOptions
        enemy_options = {
            'remove_damage_cap': self.settings.get(settingkey.REMOVE_DAMAGE_CAP)
        }
        for setting in seedSettings.boss_enemy_settings:
            value = self.settings.get(setting.name)
            if value is not None:
                enemy_options[setting.name] = value
        session['enemyOptions'] = json.dumps(enemy_options)

        # for key in sorted(session.keys()):
        #     print(str(key) + ' : ' + str(session[key]))

        return session

    def makeSeed(self,platform):
        self.fixSeedName()

        data = {
            'platform': platform,
            'cmdMenuChoice': self.settings.get(settingkey.COMMAND_MENU),
            'randomBGM': self.settings.get(settingkey.BGM_OPTIONS) + self.settings.get(settingkey.BGM_GAMES)
        }

        session = self.make_seed_session()

        self.genSeed(data,session)

    def downloadSeed(self):
        saveFileWidget = QFileDialog()
        saveFileWidget.setNameFilters(["Zip Seed File (*.zip)"])
        outfile_name,_ = saveFileWidget.getSaveFileName(self,"Save seed zip","randoseed.zip","Zip Seed File (*.zip)")
        if outfile_name!="":
            if not outfile_name.endswith(".zip"):
                outfile_name+=".zip"
            open(outfile_name, "wb").write(self.zip_file.getbuffer())
        self.zip_file=None

    def handleResult(self,result):
        self.progress.close()
        self.zip_file = result
        self.downloadSeed()

    def genSeed(self,data,session):
        self.thread = QThread()
        displayedSeedName = session["seed"]
        self.progress = QProgressDialog(f"Creating seed with name {displayedSeedName}","",0,0,None)
        self.progress.setWindowTitle("Making your Seed, please wait...")
        self.progress.setCancelButton(None)
        self.progress.setModal(True)
        self.progress.show()

        self.thread = GenSeedThread()
        self.thread.provideData(data,session)
        self.thread.finished.connect(self.handleResult)
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
        self.settings.apply_settings_json(settings_json)
        for widget in self.widgets:
            widget.update_widgets()

    def shareSeed(self):
        self.fixSeedName()

        # if seed hasn't been set yet, make one
        current_seed = self.seedName.text()
        if current_seed == "":
            characters = string.ascii_letters + string.digits
            current_seed = (''.join(random.choice(characters) for i in range(30)))
            self.seedName.setText(current_seed)

        seed = {
            'seed_name': current_seed,
            'spoiler_log': self.spoiler_log.isChecked(),
            'settings_string': self.settings.settings_string()
        }

        output_text = convert_seed_to_share_string(seed)

        pc.copy(output_text)
        message = QMessageBox(text="Copied seed to clipboard")
        message.setWindowTitle("KH2 Seed Generator")
        message.exec()

    def receiveSeed(self):
        in_settings = convert_share_string_to_seed(pc.paste())

        self.seedName.setText(in_settings['seed_name'])
        self.spoiler_log.setCheckState(Qt.Checked if in_settings['spoiler_log'] else Qt.Unchecked)
        settings_string = in_settings['settings_string']
        self.settings.apply_settings_string(settings_string)
        for widget in self.widgets:
            widget.update_widgets()
        message = QMessageBox(text="Received seed from clipboard")
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

<a href="https://github.com/tommadness/KH2Randomizer">Github Link</a><br>
<a href="https://discord.gg/KwfqM6GYzd">KH2 Randomizer Discord</a><br><br>

<a href="https://github.com/tommadness/KH2Randomizer/tree/local_ui#acknowledgements">Acknowledgements</a>



'''.format(LOCAL_UI_VERSION)
        message = QMessageBox(text=aboutText)
        message.setTextFormat(Qt.RichText)
        message.setWindowTitle("About")
        message.setWindowIcon(QIcon(resource_path("Module/icon.png")))
        message.exec()


if __name__=="__main__":
    app = QApplication([])
    window = KH2RandomizerApp()
    window.show()
    #commenting out first time setup for 2.999 version
    # configPath = Path("rando-config.yml")
    # if not configPath.is_file() or not os.environ.get("ALWAYS_SETUP") is None:
    #     window.firstTimeSetup()

    sys.exit(app.exec())
