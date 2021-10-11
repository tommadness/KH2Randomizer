import random,sys,copy,os,json,string,datetime,pytz,re
import pyperclip as pc
from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize,Qt
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QMenu, QPushButton, QCheckBox, QComboBox,
    QTabWidget,QVBoxLayout,QHBoxLayout,QWidget,QInputDialog,QFileDialog,QListWidget, QMenuBar,QMessageBox
)

from UI.Submenus.SoraMenu import SoraMenu
from UI.Submenus.KeybladeMenu import KeybladeMenu
from UI.Submenus.WorldMenu import WorldMenu
from UI.Submenus.SuperbossMenu import SuperbossMenu
from UI.Submenus.MiscMenu import MiscMenu
from UI.Submenus.StartingMenu import StartingMenu,StartingItemList
from UI.Submenus.HintsMenu import HintsMenu
from UI.Submenus.SeedModMenu import SeedModMenu
from UI.Submenus.ItemPlacementMenu import ItemPlacementMenu
from UI.Submenus.BossEnemyMenu import BossEnemyMenu


from Module.dailySeed import getDailyModifiers
from Module.randomizePage import randomizePage
from Module.randomCmdMenu import RandomCmdMenu
from Module.randomBGM import RandomBGM
from List.hashTextEntries import generateHashIcons
from List.configDict import locationDepth,locationType

from UI.FirstTimeSetup.firsttimesetup import FirstTimeSetup

SEED_SPLITTER="---"
OPTION_SPLITTER="-"
LOCAL_UI_VERSION="1.0.0"

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

import sys
logger = Logger(sys.stdout)

sys.stdout = logger
sys.stderr = logger

def convert_seed_to_flags(seed, flagOptions):
    flagInts={}
    flattened = []
    for key in seed["settings"].keys():
        flagInts[key] = {}
        for subkey in seed["settings"][key].keys():
            if flagOptions[key][subkey]["type"]=="bool":
                flagInts[key][subkey] = 1 if seed["settings"][key][subkey] else 0
                flattened.append((key+"-"+subkey,flagInts[key][subkey]))
            if flagOptions[key][subkey]["type"]=="select":
                flagInts[key][subkey] = flagOptions[key][subkey]["options"].index(seed["settings"][key][subkey])
                flattened.append((key+"-"+subkey,flagInts[key][subkey]))
            if flagOptions[key][subkey]["type"]=="multiselect":
                bit_string="0b"
                for item_id,item_string in StartingItemList:
                    if item_id in seed["settings"][key][subkey]:
                        bit_string+='1'
                    else:
                        bit_string+='0'
                flagInts[key][subkey] = int(bit_string, 2)
                flattened.append((key+"-"+subkey,flagInts[key][subkey]))

            if flagOptions[key][subkey]["type"]=="spin":
                val = seed["settings"][key][subkey]
                flagInts[key][subkey] = int((val-flagOptions[key][subkey]["min"])/flagOptions[key][subkey]["step"])
                flattened.append((key+"-"+subkey,flagInts[key][subkey]))


    flattened.sort(key=lambda x: x[0])

    flags = seed["seed_name"]+SEED_SPLITTER+str(1 if seed["spoiler_log"] else 0)

    for item in flattened:
        flags+=OPTION_SPLITTER
        flags+=str(item[1])

    return flags

def convert_flags_to_seed(flags, flagOptions):
    seed={}
    seed["seed_name"] = flags.split(SEED_SPLITTER)[0]
    flags = flags.split(SEED_SPLITTER)[1]
    flag_list = flags.split(OPTION_SPLITTER)
    seed["spoiler_log"] = bool(int(flag_list[0]))
    flag_list.pop(0)

    flattened = []
    for key in flagOptions.keys():
        for subkey in flagOptions[key].keys():
            if flagOptions[key][subkey]["type"]=="bool":
                flattened.append((key+"-"+subkey,key,subkey))
            if flagOptions[key][subkey]["type"]=="select":
                flattened.append((key+"-"+subkey,key,subkey))
            if flagOptions[key][subkey]["type"]=="multiselect":
                flattened.append((key+"-"+subkey,key,subkey))
            if flagOptions[key][subkey]["type"]=="spin":
                flattened.append((key+"-"+subkey,key,subkey))

    flattened.sort(key=lambda x: x[0])
    seed["settings"] = {}

    for item,key,subkey in flattened:
        flag = flag_list.pop(0)
        if key not in seed["settings"]:
            seed["settings"][key]={}
        if flagOptions[key][subkey]["type"]=="bool":
            seed["settings"][key][subkey] = bool(int(flag))
        if flagOptions[key][subkey]["type"]=="select":
            seed["settings"][key][subkey] = flagOptions[key][subkey]["options"][int(flag)]
        if flagOptions[key][subkey]["type"]=="multiselect":
            item_flags = format((int(flag)), "#0"+str(len(flagOptions[key][subkey]["options"])+2)+"b")
            item_flags = item_flags[2:]
            starting = []
            for index,(item_id,item_string) in enumerate(StartingItemList):
                if item_flags[index]=='1':
                    starting.append(item_id)
            seed["settings"][key][subkey] = starting
        if flagOptions[key][subkey]["type"]=="spin":
            seed["settings"][key][subkey] = flagOptions[key][subkey]["min"]+flagOptions[key][subkey]["step"]*int(flag)

    return seed

PRESET_FOLDER = "presets"
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class KH2RandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UTC = pytz.utc
        self.startTime = datetime.datetime.now(self.UTC)
        self.dailySeedName = self.startTime.strftime('%d-%m-%Y')
        self.mods = getDailyModifiers(self.startTime)


        with open(resource_path("UI/stylesheet.qss"),"r") as style:
            data = style.read()
            self.setStyleSheet(data)

        random.seed(str(datetime.datetime.now()))
        self.setWindowTitle("KH2 Randomizer Seed Generator")
        self.setup = None
        pagelayout = QVBoxLayout()
        seed_layout = QHBoxLayout()
        submit_layout = QHBoxLayout()
        self.seedhashlayout = QHBoxLayout()
        self.cosmetic_layout = QHBoxLayout()
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
        
        self.presetJSON = {}
        if not os.path.exists(PRESET_FOLDER):
            os.makedirs(PRESET_FOLDER)
        presetFolderContents = os.listdir(PRESET_FOLDER)


        if not presetFolderContents == []:
            for file in presetFolderContents:
                with open(PRESET_FOLDER+"\\"+file,"r") as presetData:
                    data = json.loads(presetData.read())
                    for k,v in data.items():
                        self.presetJSON[k] = v      
                 
        pagelayout.addWidget(self.menuBar)
        pagelayout.addLayout(seed_layout)
        pagelayout.addWidget(self.tabs)
        pagelayout.addLayout(self.cosmetic_layout)
        pagelayout.addLayout(submit_layout)
        pagelayout.addLayout(self.seedhashlayout)
        seed_layout.addWidget(QLabel("Seed"))
        self.seedName=QLineEdit()
        self.seedName.setPlaceholderText("Leave blank for a random seed")
        seed_layout.addWidget(self.seedName)


        for x in self.presetJSON.keys():
            self.presetsMenu.addAction(x, lambda x=x: self.usePreset(x))

        self.spoiler_log = QCheckBox("Make Spoiler Log")
        seed_layout.addWidget(self.spoiler_log)

        self.widgets = [SoraMenu(),StartingMenu(),HintsMenu(),
                        KeybladeMenu(),WorldMenu(),SuperbossMenu(),
                        MiscMenu(),SeedModMenu(),ItemPlacementMenu(),
                        BossEnemyMenu()]

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


        self.commandMenuOptions = QComboBox()
        self.commandMenuOptions.addItems(RandomCmdMenu.getOptions().values())
        self.commandMenuOptions.setCurrentText("vanilla")  

        self.bgmOptions = QListWidget()
        self.bgmOptions.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.bgmOptions.addItems(RandomBGM.getOptions())
        self.bgmOptions.setMinimumWidth(self.bgmOptions.sizeHintForColumn(0)+30)

        self.bgmChoices = QListWidget()
        self.bgmChoices.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.bgmChoices.addItems(RandomBGM.getGames())
        self.bgmChoices.setMinimumWidth(self.bgmChoices.sizeHintForColumn(0)+30)

        self.cosmetic_layout.addWidget(QLabel("Command Menu (PS2 Only)"))
        self.cosmetic_layout.addWidget(self.commandMenuOptions)
        self.cosmetic_layout.addWidget(QLabel("Randomize BGM (PC Only)"))
        self.cosmetic_layout.addWidget(self.bgmOptions)
        self.cosmetic_layout.addWidget(self.bgmChoices)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def loadDailySeed(self):
        self.seedName.setText(self.dailySeedName)

        preset_values = copy.deepcopy(self.presetJSON["BaseDailySeed"])
        # use the modifications to change the preset
        mod_string = f"Updated settings for Daily Seed {self.startTime.strftime('%a %b %d %Y')}\n\n"
        for m in self.mods:
            m.local_modifier(preset_values)
            mod_string+=m.name+" - "+m.description+"\n"

        for x in self.widgets:
            x.setData(preset_values[x.getName()])

        message = QMessageBox(text=mod_string)
        message.setWindowTitle("KH2 Seed Generator - Daily Seed")
        message.exec()

    def fixSeedName(self):
        new_string = re.sub(r'[^a-zA-Z0-9]', '', self.seedName.text())
        self.seedName.setText(new_string)


    def makeSeed(self,platform):
        self.fixSeedName()
        settings = {}
        for x in self.widgets:
            settings[x.getName()] = copy.deepcopy(x.getData())

        makeSpoilerLog = self.spoiler_log.isChecked()

        data={}
        data["platform"]=platform
        cmdMap = RandomCmdMenu.getOptions()
        selected = self.commandMenuOptions.currentText()
        for key,value in cmdMap.items():
            if value==selected:
                data["cmdMenuChoice"]=key

        selectedMusic = self.bgmOptions.selectedItems() + self.bgmChoices.selectedItems()
        data["randomBGM"]=[s.text() for s in selectedMusic]

        session={}

        #seed
        session["seed"] = self.seedName.text()
        if session["seed"] == "":
            characters = string.ascii_letters + string.digits
            session["seed"] = (''.join(random.choice(characters) for i in range(30)))

        # make the seed hash dependent on ui version and if a spoiler log is generated or not.
        random.seed(session["seed"]+LOCAL_UI_VERSION+str(makeSpoilerLog))

        #seedHashIcons
        session["seedHashIcons"] = generateHashIcons()

        #includeList
        session["includeList"] = []

        includeListKeys = [("Sora","Form Levels"),
                            ("Starting Items","Critical Bonuses"),
                            ("Starting Items","Garden of Assemblage")]
        for key in includeListKeys:
            if settings[key[0]][key[1]]:
                session["includeList"].append(key[1])


        for world in settings["Worlds with Rewards"].keys():
            if settings["Worlds with Rewards"][world]:
                session["includeList"].append(world)
        for boss_group in settings["Superbosses with Rewards"].keys():
            if settings["Superbosses with Rewards"][boss_group]:
                session["includeList"].append(boss_group)
        for misc_group in settings["Misc Locations with Rewards"].keys():
            if settings["Misc Locations with Rewards"][misc_group]:
                session["includeList"].append(misc_group)


        #levelChoice
        levelChoice = settings["Sora"]["levelChoice"]
        if levelChoice =="Level 1":
            session["levelChoice"] = "Level"
        if levelChoice =="Level 50":
            session["levelChoice"] = "ExcludeFrom50"
        if levelChoice =="Level 99":
            session["levelChoice"] = "ExcludeFrom99"
        #startingInventory
        session["startingInventory"] = settings["Starting Items"]["startingInventory"]
        #itemPlacementDifficulty
        session["itemPlacementDifficulty"] = settings["Item Placement Options"]["itemPlacementDifficulty"]
        #seedModifiers
        session["seedModifiers"] = []
        seedModifierKeys = [("Item Placement Options","Max Logic Item Placement"),
                            ("Item Placement Options","Reverse Rando"),
                            ("Item Placement Options","Randomize Ability Pool"),
                            ("Starting Items","Library of Assemblage"),
                            ("Starting Items","Schmovement"),
                            ("Seed Modifiers","Glass Cannon"),
                            ("Seed Modifiers","Better Junk"),
                            ("Seed Modifiers","Start with No AP"),
                            ("Seed Modifiers","Remove Damage Cap"),]
        for key in seedModifierKeys:
            if settings[key[0]][key[1]]:
                session["seedModifiers"].append(key[1])

        #update the seed hash display
        for n,ic in enumerate(session["seedHashIcons"]):
            self.hashIcons[n].setPixmap(QPixmap(str(self.hashIconPath.absolute())+"/"+ic+".png"))

        #spoilerLog
        session["spoilerLog"] = makeSpoilerLog
        #reportDepth
        #hintsType
        reportStringList = settings["Hint Systems"]["hintsType"].split('-')
        session["hintsType"] = settings["Hint Systems"]["hintsType"]
        session["reportDepth"] = locationDepth(settings["Hint Systems"]["reportDepth"])
        #preventSelfHinting
        session["preventSelfHinting"] = settings["Hint Systems"]["preventSelfHinting"]
        session["allowProofHinting"] = settings["Hint Systems"]["allowProofHinting"]
        #promiseCharm
        session["promiseCharm"] = settings["Item Placement Options"]["PromiseCharm"]
        #keybladeAbilities
        session["keybladeAbilities"] = []
        session["keybladeAbilities"]+= ["Support"] if settings["Keyblades"]["keybladeSupport"] else []
        session["keybladeAbilities"]+= ["Action"] if settings["Keyblades"]["keybladeAction"] else []
        #keybladeMinStat
        session["keybladeMinStat"] = settings["Keyblades"]["keybladeMinStat"]
        #keybladeMaxStat
        session["keybladeMaxStat"] = settings["Keyblades"]["keybladeMaxStat"]
        #soraExpMult
        session["soraExpMult"] = settings["Sora"]["soraExpMult"]
        #formExpMult
        session["formExpMult"] = {
            "0": float(settings["Sora"]["soraExpMult"]),
            "1": float(settings["Sora"]["ValorExp"]), 
            "2": float(settings["Sora"]["WisdomExp"]), 
            "3": float(settings["Sora"]["LimitExp"]), 
            "4": float(settings["Sora"]["MasterExp"]), 
            "5": float(settings["Sora"]["FinalExp"])
            }
        #enemyOptions
        settings["Boss/Enemy"]["remove_damage_cap"] = "Remove Damage Cap" in session["seedModifiers"]

        if settings["Boss/Enemy"]["selected_enemy"]=="":
            settings["Boss/Enemy"].pop("selected_enemy")
        if settings["Boss/Enemy"]["selected_boss"]=="":
            settings["Boss/Enemy"].pop("selected_boss")

        session["enemyOptions"] = json.dumps(settings["Boss/Enemy"])

        print(session["enemyOptions"])

        zip_file = randomizePage(data,session,local_ui=True)

        saveFileWidget = QFileDialog()
        saveFileWidget.setNameFilters(["Zip Seed File (*.zip)"])
        outfile_name,_ = saveFileWidget.getSaveFileName(self,"Save seed zip","randoseed.zip","Zip Seed File (*.zip)")
        if outfile_name!="":
            if not outfile_name.endswith(".zip"):
                outfile_name+=".zip"
            open(outfile_name, "wb").write(zip_file.getbuffer())


    def savePreset(self):
        text, ok = QInputDialog.getText(self, 'Make New Preset', 
            'Enter a name for your preset...')
        
        if ok:
            #add current settings to saved presets, add to current preset list, change preset selection.
            settings = {}
            preset = {}
            for x in self.widgets:
                settings[x.getName()] = copy.deepcopy(x.getData())
            preset[text] = settings
            self.presetJSON[text] = settings
            self.presetsMenu.addAction(text, lambda: self.usePreset(text))
            with open(PRESET_FOLDER+"\\"+text+".json","w") as presetData:
                presetData.write(json.dumps(preset, indent=4, sort_keys=True))

    def openPresetFolder(self):
        os.startfile(PRESET_FOLDER)
            

    def usePreset(self,presetName):
        if presetName != "Presets":
            preset_values = self.presetJSON[presetName]
            for x in self.widgets:
                x.setData(preset_values[x.getName()])

    def shareSeed(self):
        self.fixSeedName()
        settings = {}
        flags = {}
        for x in self.widgets:
            settings[x.getName()] = copy.deepcopy(x.getData())
            flags[x.getName()] = copy.deepcopy(x.getFlagOptions())

        #if seed hasn't been set yet, make one
        current_seed = self.seedName.text()
        if current_seed == "":
            characters = string.ascii_letters + string.digits
            current_seed = (''.join(random.choice(characters) for i in range(30)))
            self.seedName.setText(current_seed)

        makeSpoilerLog = self.spoiler_log.isChecked()

        seed = {}
        seed["spoiler_log"] = makeSpoilerLog
        seed["seed_name"] = current_seed
        seed["settings"] = settings

        output_text = convert_seed_to_flags(seed,flags)

        pc.copy(output_text)
        message = QMessageBox(text="Copied seed to clipboard")
        message.setWindowTitle("KH2 Seed Generator")
        message.exec()
    
    def receiveSeed(self):
        flags = {}
        for x in self.widgets:
            flags[x.getName()] = copy.deepcopy(x.getFlagOptions())
        in_settings = convert_flags_to_seed(pc.paste(),flags)

        self.spoiler_log.setCheckState(Qt.Checked if in_settings["spoiler_log"] else Qt.Unchecked)
        self.seedName.setText(in_settings["seed_name"])
        settings_values = in_settings["settings"]
        for x in self.widgets:
            x.setData(settings_values[x.getName()])
        message = QMessageBox(text="Received seed from clipboard")
        message.setWindowTitle("KH2 Seed Generator")
        message.exec()
        
    def firstTimeSetup(self):
        print("First Time Setup")
        if self.setup is None:
            self.setup = FirstTimeSetup()
            self.setup.show()


if __name__=="__main__":
    app = QApplication([])
    window = KH2RandomizerApp()
    window.show()
    #commenting out first time setup for 2.999 version
    # configPath = Path("rando-config.yml")
    # if not configPath.is_file() or not os.environ.get("ALWAYS_SETUP") is None:
    #     window.firstTimeSetup()

    sys.exit(app.exec())