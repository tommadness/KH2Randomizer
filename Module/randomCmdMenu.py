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
            "di0": "Destiny Island",
            "eh0": "The World That Never Was",
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
            "tt2": "Mysterious Tower",
            "tt3": "Mansion Basement",
            "tt4": "The White Room",
            "tt5": "Mansion",
            "tt6": "Betwixt & Between",
            "wi0": "Timeless River",
            "zz0": "Kingdom Hearts 1"
            }

    def randomizeCmdMenus(cmdMenuChoice, outZip, platform="PCSX2"):
        cmdMenus = [
            "al0",
            "bb0",
            "ca0",
            "dc0",
            "dc1",
            "di0",
            "eh0",
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
            "tt2",
            "tt3",
            "tt4",
            "tt5",
            "tt6",
            "wi0",
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
        for key in cmdMenusDict:
            cmdMenuAssets.append({
                "name": "field2d\\jp\\{key}command.2dd".format(key=key),
                "multi": [{"name": "field2d\\us\\{key}command.2dd".format(key=key)}],
                "method": "copy",
                "source": [{"name": "field2d\\us\\{cmdMenu}command.2dd".format(cmdMenu=cmdMenusDict[key]), "type":"internal"}]
            })

        
        return cmdMenuAssets





