import random, zipfile, os


class RandomCmdMenu():
    def getOptions():
        return {
            "vanilla": "Vanilla", 
            "rand1": "Randomize (one)", 
            "randAll": "Randomize (all)", 
            "al0":"Agrabah",
            "bb0": "Beast's Castle",
            "ca0": "Port Royal",
            "dc0": "Disney Castle",
            "dc1": "Lingering Will",
            #"di0": "Destiny Island", #no visible difference from KH1
            "eh0": "The World That Never Was",
            #"eh1": "The Dark Margin(?)", #looks like KH1 but with classic icons
            #"es0": "Agrabah (alt), #for carpet minigames? need to check for differences.
            "hb0": "Hollow Bastion",
            "hb1": "Garden of Assemblage",
            "hb2": "Absent Silhouette",
            "he0": "Olympus Coliseum",
            "he1": "The Underworld",
            "lk0": "Pride Lands",
            "lm0": "Atlantica",
            "mu0": "Land of Dragons",
            "nm0": "Halloween Town",
            "nm1": "Christmas Town",
            "po0": "100 Acre Wood",
            "tr0": "Space Paranoids",
            "tt0": "Twilight Town",
            "tt1": "Station of Calling", #looks like kh1 but with classic icons.
            "tt2": "Mysterious Tower",
            "tt3": "Mansion Basement",
            "tt4": "The White Room",
            "tt5": "Mansion",
            "tt6": "Betwixt & Between",
            "wi0": "Timeless River",
            #"wm0": "World Map", #no visible difference from Betwixt & Between
            "zz0": "Kingdom Hearts 1"
            }

    def randomizeCmdMenus(cmdMenuChoice, outZip, platform="PCSX2"):
        if not platform == "PCSX2":
            return ""
        cmdMenus = [
            "al0",
            "bb0",
            "ca0",
            "dc0",
            "dc1",
            #"di0",
            "eh0",
            #"eh1",
            #"es0",
            "hb0",
            "hb1",
            "hb2",
            "he0",
            "he1",
            "lk0",
            "lm0",
            "mu0",
            "nm0",
            "nm1",
            "po0",
            "tr0",
            "tt0",
            "tt1",
            "tt2",
            "tt3",
            "tt4",
            "tt5",
            "tt6",
            "wi0",
            #"wm0",
            "zz0"
        ]
        cmdMenusDict = {}
        if cmdMenuChoice == "randAll":
            for cmdMenu in cmdMenus[:]:
                cmdMenusDict[cmdMenu] = random.choice(cmdMenus)
                cmdMenus.remove(cmdMenusDict[cmdMenu])
        elif cmdMenuChoice == "rand1":
            singleCmdMenu = random.choice(cmdMenus)
            for cmdMenu in cmdMenus[:]:
                cmdMenusDict[cmdMenu] = singleCmdMenu
        elif cmdMenuChoice == "vanilla":
            return ""
        else:
            for cmdMenu in cmdMenus[:]:
                cmdMenusDict[cmdMenu] = cmdMenuChoice
        cmdMenuAssets = []
        region = ""
        if platform == "PCSX2":
            region = "jp"
        for key in cmdMenusDict:
            cmdMenuAssets.append({
                "name": "field2d\\jp\\{key}command.2dd".format(key=key),
                "multi": [{"name": "field2d\\us\\{key}command.2dd".format(key=key)}],
                "method": "copy",
                "source": [{"name": "field2d\\{region}\\{cmdMenu}command.2dd".format(cmdMenu=cmdMenusDict[key], region=region), "type":"internal"}]
            })

        
        return cmdMenuAssets





