from ItemList import itemList, supportAbilityList, actionAbilityList, junkList
from LocationList import treasureList, soraLevelList, soraBonusList, formLevels, keybladeStats
from experienceValues import formExp, soraExp
from randomCmdMenu import RandomizeCmdMenus
from mod import mod
import random
import yaml
import zipfile
import io
import os

def noop(self, *args, **kw):
    pass

def Randomize(seedName="", exclude=[], keybladeAbilities = ["Support"], keybladeMinStat = 0, keybladeMaxStat = 7, formExpMult = {1:1,2:1,3:1,4:1,5:1}, soraExpMult = 1, levelChoice = "ExcludeFrom50", cmdMenuChoice = "Vanilla" ):

    exclude.append("Level1Form") #Always exclude level 1 forms from getting checks
    exclude.append(levelChoice)
    random.seed(seedName)
    modOut = "#" + seedName + "\n" + mod
    #KEYBLADE ABILITIES AND STATS
    validKeybladeAbilities = []
    invalidKeybladeAbilities = []

    if "Support" in keybladeAbilities:
        validKeybladeAbilities += supportAbilityList
    else:
        invalidKeybladeAbilities += supportAbilityList

    if "Action" in keybladeAbilities:
        validKeybladeAbilities += actionAbilityList
    else:
        invalidKeybladeAbilities += actionAbilityList

    for keyblade in keybladeStats:
        randomAbility = random.choice(validKeybladeAbilities)
        keyblade.Ability = randomAbility.Id
        validKeybladeAbilities.remove(randomAbility)
        keyblade.Attack = random.randint(keybladeMinStat, keybladeMaxStat)
        keyblade.Magic = random.randint(keybladeMinStat, keybladeMaxStat)

    itemsList = itemList + validKeybladeAbilities + invalidKeybladeAbilities

    #SORA REWARDS
    validLocationList = []
    locationList = treasureList + soraLevelList + soraBonusList + formLevels
    for location in locationList:
        if not any(locationType in exclude for locationType in location.LocationTypes):
            validLocationList.append(location)

    if len(validLocationList) < len(itemsList):
        return "Too few locations, can't randomize."

    for item in itemsList[:]:
        randomLocation = random.choice(locationList)
        if not item.ItemType in randomLocation.InvalidChecks and not any(locationType in exclude for locationType in randomLocation.LocationTypes):
            randomLocation.setReward(item.Id)
            itemsList.remove(item)
            locationList.remove(randomLocation)

    #FILL REMAINING LOCATIONS WITH JUNK
    for location in locationList:
        if not levelChoice in location.LocationTypes:
            location.setReward(random.choice(junkList).Id)

    #TODO: RANDOMIZE SORA STATS

    #TODO: RANDOMIZE PARTY MEMBER CHECKS

    #TODO: INCORPORATE BOSS/ENEMY RANDO

    #FORM EXPERIENCE
    for formLevel in formLevels:
        formLevel.Experience = round(formExp[formLevel.FormId][formLevel.FormLevel] / formExpMult[formLevel.FormId])

    #SORA EXPERIENCE
    for level in soraLevelList:
        level.Exp = round(soraExp[level.Level] / soraExpMult)


    commandMenuString = RandomizeCmdMenus(cmdMenuChoice)

    #FORMAT FOR OUTPUT
    formattedTrsr = {}
    for trsr in treasureList:
        formattedTrsr[trsr.Id] = {'ItemId': trsr.ItemId}

    formattedLvup = {}
    for lvup in soraLevelList:
        if not lvup.Character in formattedLvup.keys():
            formattedLvup[lvup.Character] = {}
        formattedLvup[lvup.Character][lvup.Level] = lvup

    formattedBons = {}
    for bons in soraBonusList:
        if not bons.RewardId in formattedBons.keys():
            formattedBons[bons.RewardId] = {}
        formattedBons[bons.RewardId][bons.getCharacterName()] = bons

    formattedFmlv = {}
    for fmlv in formLevels:
        if not fmlv.getFormName() in formattedFmlv.keys():
            formattedFmlv[fmlv.getFormName()] = []
        formattedFmlv[fmlv.getFormName()].append(fmlv)

    formattedStats = {'Stats': keybladeStats}


    #OUTPUT
    yaml.emitter.Emitter.process_tag = noop
    
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w") as outZip:

        trsrList = yaml.dump(formattedTrsr, line_break="\r\n")
        outZip.writestr("TrsrList.yml",trsrList)

        lvupList = yaml.dump(formattedLvup, line_break="\r\n")
        outZip.writestr("LvupList.yml",lvupList)

        bonsList = yaml.dump(formattedBons, line_break="\r\n")
        outZip.writestr("BonsList.yml",bonsList)

        statsList = yaml.dump(formattedStats, line_break="\r\n")
        outZip.writestr("ItemList.yml",statsList)

        fmlvList = yaml.dump(formattedFmlv, line_break="\r\n")
        outZip.writestr("FmlvList.yml",fmlvList)

        outZip.writestr("mod.yml", modOut+commandMenuString)
        if not commandMenuString == "":
            for folderName, subfolders, filenames in os.walk("CommandMenus"):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    outZip.write(filePath, filePath)
        outZip.close()

    data.seek(0)
    return data