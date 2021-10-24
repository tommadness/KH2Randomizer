from pathlib import Path
import yaml


class uiConfig():
    pcsx2 = {
                "emulatorPath": "",
                "isoPath": "",
                "gameDataPath": "",
            }
    PC = {
                "executablePath": "",
                "gameDataPath": "",
            }
    setupDone = False
    def __init__(self):
        if self.loadConfig() == False:

            self.saveConfig()
    
    @classmethod
    def loadConfig(self):
        configPath = Path("rando-config.yml")
        if not configPath.is_file():
            return False
        configFile = open(configPath, "r")
        configString = str(configFile.read())
        config = yaml.safe_load(configString)
        self.pcsx2 = config['pcsx2']
        self.PC = config['PC']
        self.setupDone = config['setupDone']
        return True

    @classmethod
    def saveConfig(self):
        config = {
            "pcsx2": self.pcsx2,
            "PC": self.PC,
            "setupDone": self.setupDone
        }
        configFile = open("rando-config.yml","w")
        configFile.write(yaml.safe_dump(config))
        configFile.close()


