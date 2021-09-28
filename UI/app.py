import random,sys,copy,os,json
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QTabWidget,QVBoxLayout,QHBoxLayout,QWidget,QInputDialog
)

from Submenus.SoraMenu import SoraMenu
from Submenus.KeybladeMenu import KeybladeMenu
from Submenus.WorldMenu import WorldMenu
from Submenus.SuperbossMenu import SuperbossMenu
from Submenus.MiscMenu import MiscMenu
from Submenus.StartingMenu import StartingMenu
from Submenus.HintsMenu import HintsMenu
from Submenus.SeedModMenu import SeedModMenu
from Submenus.ItemPlacementMenu import ItemPlacementMenu
from Submenus.BossEnemyMenu import BossEnemyMenu

from FirstTimeSetup.firsttimesetup import FirstTimeSetup


PRESET_FILE = "presets.json"

class KH2RandomizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KH2 Randomizer Seed Generator")
        self.setup = None
        pagelayout = QVBoxLayout()
        seed_layout = QHBoxLayout()
        submit_layout = QHBoxLayout()
        self.tabs = QTabWidget()

        if not os.path.isfile(PRESET_FILE):
            self.presetJSON = {}
        else:
            with open(PRESET_FILE,"r") as presetData:
                data = presetData.read()
                self.presetJSON = json.loads(data)                

        pagelayout.addLayout(seed_layout)
        pagelayout.addWidget(self.tabs)
        pagelayout.addLayout(submit_layout)

        seed_layout.addWidget(QLabel("Seed"))
        self.seedName=QLineEdit()
        self.seedName.setPlaceholderText("Leave blank for a random seed")
        seed_layout.addWidget(self.seedName)

        self.presets = QComboBox()
        self.presets.setMinimumWidth(200)
        self.presets.addItem("Presets")
        for x in self.presetJSON.keys():
            self.presets.addItem(x)
        self.presets.currentTextChanged.connect(self.usePreset)
        seed_layout.addWidget(self.presets)

        savePresetButton = QPushButton("Save Settings as New Preset")
        savePresetButton.clicked.connect(self.savePreset)
        seed_layout.addWidget(savePresetButton)

        self.spoiler_log = QCheckBox("Make Spoiler Log")
        seed_layout.addWidget(self.spoiler_log)

        self.widgets = [SoraMenu(),StartingMenu(),HintsMenu(),
                        KeybladeMenu(),WorldMenu(),SuperbossMenu(),
                        MiscMenu(),SeedModMenu(),ItemPlacementMenu(),
                        BossEnemyMenu()]

        for i in range(len(self.widgets)):
            self.tabs.addTab(self.widgets[i],self.widgets[i].getName())


        submitButton = QPushButton("Generate Seed")
        submitButton.clicked.connect(self.makeSeed)
        submit_layout.addWidget(submitButton)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def makeSeed(self):
        settings = {}
        for x in self.widgets:
            settings[x.getName()] = x.getData()

        makeSpoilerLog = self.spoiler_log.isChecked()

        # TODO pass to randomizer class and mimic the main app file functions

    def savePreset(self):
        text, ok = QInputDialog.getText(self, 'Make New Preset', 
            'Enter a name for your preset...')
        
        if ok:
            #add current settings to saved presets, add to current preset list, change preset selection.
            settings = {}
            for x in self.widgets:
                settings[x.getName()] = copy.deepcopy(x.getData())
            self.presetJSON[text] = settings
            self.presets.addItem(text)
            self.presets.setCurrentIndex(self.presets.count()-1)
            with open(PRESET_FILE,"w") as presetData:
                presetData.write(json.dumps(self.presetJSON))
            

    def usePreset(self,presetName):
        if presetName != "Presets":
            preset_values = self.presetJSON[presetName]
            for x in self.widgets:
                x.setData(preset_values[x.getName()])
        
    def firstTimeSetup(self):
        print("First Time Setup")
        if self.setup is None:
            self.setup = FirstTimeSetup()
            self.setup.show()


if __name__=="__main__":
    app = QApplication([])
    window = KH2RandomizerApp()
    window.show()
    configPath = Path("rando-config.yml")
    if not configPath.is_file() or not os.environ.get("ALWAYS_SETUP") is None:
        window.firstTimeSetup()

    sys.exit(app.exec())