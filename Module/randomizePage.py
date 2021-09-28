from Module.modifier import SeedModifier
from Module.seedEvaluation import SeedValidator
from List.configDict import locationType, locationDepth
import os, string, random, json
from Module.hints import Hints
from Module.randomize import KH2Randomizer

development_mode = os.environ.get("DEVELOPMENT_MODE")

def randomizePage(data, sessionDict, local_ui=False):
    platform = data['platform']
    excludeList = list(set(locationType) - set(sessionDict['includeList']))
    excludeList.append(sessionDict["levelChoice"])

    if sessionDict["itemPlacementDifficulty"] == "Nightmare" and locationType.Puzzle in excludeList:
        print("Removing puzzle exclusion due to nightmare...")
        excludeList.remove(locationType.Puzzle)

    cmdMenuChoice = data["cmdMenuChoice"]
    randomBGM = data["randomBGM"]
    sessionDict["startingInventory"] += SeedModifier.library("Library of Assemblage" in sessionDict["seedModifiers"]) + SeedModifier.schmovement("Schmovement" in sessionDict["seedModifiers"])

    seedValidation = SeedValidator(sessionDict)
    notValidSeed = True

    originalSeedName = sessionDict['seed']
    while notValidSeed:
        randomizer = KH2Randomizer(seedName = sessionDict["seed"], seedHashIcons = sessionDict["seedHashIcons"], spoiler=bool(sessionDict["spoilerLog"]))
        randomizer.populateLocations(excludeList,  maxItemLogic = "Max Logic Item Placement" in sessionDict["seedModifiers"],item_difficulty=sessionDict["itemPlacementDifficulty"], reportDepth=sessionDict["reportDepth"])
        randomizer.populateItems(promiseCharm = sessionDict["promiseCharm"], startingInventory = sessionDict["startingInventory"], abilityListModifier=SeedModifier.randomAbilityPool if "Randomize Ability Pool" in sessionDict["seedModifiers"] else None)
        if randomizer.validateCount():
            randomizer.setKeybladeAbilities(
                keybladeAbilities = sessionDict["keybladeAbilities"], 
                keybladeMinStat = int(sessionDict["keybladeMinStat"]), 
                keybladeMaxStat = int(sessionDict["keybladeMaxStat"])
            )
            randomizer.setNoAP("Start with No AP" in sessionDict["seedModifiers"])
            randomizer.setRewards(levelChoice = sessionDict["levelChoice"], betterJunk=("Better Junk" in sessionDict["seedModifiers"]), reportDepth=sessionDict["reportDepth"])
            randomizer.setLevels(sessionDict["soraExpMult"], formExpMult = sessionDict["formExpMult"], statsList = SeedModifier.glassCannon("Glass Cannon" in sessionDict["seedModifiers"]))
            randomizer.setBonusStats()
            if not seedValidation.validateSeed(sessionDict, randomizer):
                print("ERROR: Seed is not completable! Trying another seed...")
                characters = string.ascii_letters + string.digits
                sessionDict['seed'] = (''.join(random.choice(characters) for i in range(30)))
                continue
            randomizer.seedName = originalSeedName
            hintsText = Hints.generateHints(randomizer._locationItems, sessionDict["hintsType"], randomizer.seedName, excludeList, sessionDict["preventSelfHinting"])

            if hintsText is not None and type(hintsText) is not dict:
                # there was an error generating hints, return value provides context
                print(f"ERROR: {hintsText}")
                characters = string.ascii_letters + string.digits
                sessionDict['seed'] = (''.join(random.choice(characters) for i in range(30)))
                continue

            notValidSeed = False
            
            try:
                zip = randomizer.generateZip(randomBGM = randomBGM, platform = platform, startingInventory = sessionDict["startingInventory"], hintsText = hintsText, cmdMenuChoice = cmdMenuChoice, spoilerLog = bool(sessionDict["spoilerLog"]), enemyOptions = json.loads(sessionDict["enemyOptions"]))
                if development_mode:
                    development_mode_path = os.environ.get("DEVELOPMENT_MODE_PATH")
                    if development_mode_path:
                        if os.path.exists(development_mode_path):
                            # Ensure a clean environment
                            import shutil
                            shutil.rmtree(development_mode_path)
                        # Unzip mod into path
                        import zipfile
                        zipfile.ZipFile(zip).extractall(development_mode_path)
                        print("unzipped into {}".format(development_mode_path))
                    if not local_ui:
                        return
                if not local_ui:
                    socketio.emit('file',zip.read())
                else:
                    return zip

            except ValueError as err:
                print("ERROR: ", err.args)