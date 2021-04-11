import ItemList
import LocationList
from itemClass import KH2Item, ItemEncoder
from experienceValues import formExp, soraExp
from randomCmdMenu import RandomizeCmdMenus
from spoilerLog import generateSpoilerLog
from hashTextEntries import hashTextEntries
from configDict import itemType, locationType
import LvupStats
from modYml import modYml
from hints import Hints
import os, yaml, zipfile, io, random, json

def noop(self, *args, **kw):
    pass

def Randomize(
    seedName="", 
    exclude=[], 
    keybladeAbilities = ["Support"], 
    keybladeMinStat = 0, 
    keybladeMaxStat = 7, 
    formExpMult = {
        '1':1,
        '2':1,
        '3':1,
        '4':1,
        '5':1
        }, 
    soraExpMult = 1, 
    levelChoice = "ExcludeFrom50", 
    cmdMenuChoice = "vanilla", 
    spoilerLog = True,
    promiseCharm = False,
    goMode = False,
    # enemyOptions = {},
    enemyOptions={"boss":"Disabled"},
    hintsType = "Shananas"
    ):
    #Setup lists without modifying base lists
    print(enemyOptions)
    itemList = ItemList.itemList[:]
    supportAbilityList = ItemList.supportAbilityList[:]
    actionAbilityList = ItemList.actionAbilityList[:]
    junkList = ItemList.junkList[:]

    treasureList = LocationList.treasureList[:]
    soraLevelList = LocationList.soraLevelList[:]
    soraBonusList = LocationList.soraBonusList[:]
    formLevels = LocationList.formLevels[:]
    keybladeStats = LocationList.keybladeStats[:]
    soraStartingItems = LocationList.soraStartingItems[:]

    lvupStats = LvupStats.lvupStats[:]
    lvupAp = LvupStats.lvupAp[:]
    bonsStats = LvupStats.bonsStats[:]

    donaldBonusList = LocationList.donaldBonusList[:]
    goofyBonusList = LocationList.goofyBonusList[:]

    donaldStartingList = LocationList.donaldStartingItems[:]
    goofyStartingList = LocationList.goofyStartingItems[:]

    donaldItemList = LocationList.donaldItemList[:]
    goofyItemList = LocationList.goofyItemList[:]

    donaldAbilityList = ItemList.donaldAbilityList[:]
    goofyAbilityList = ItemList.goofyAbilityList[:]

    mod = modYml.getDefaultMod()

    exclude.append("Level1Form") #Always exclude level 1 forms from getting checks
    exclude.append(levelChoice)
    random.seed(seedName)
    if not spoilerLog:
        random.randint(0,100) #Make sure the same seed name with and without spoiler log changes the randomization


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

    randomizeKeyblades(keybladeStats, validKeybladeAbilities, keybladeMinStat, keybladeMaxStat)

    itemsList = itemList + validKeybladeAbilities + invalidKeybladeAbilities
    

    #VALIDATE NUMBER OF LOCATIONS
    validLocationList = []
    locationList = treasureList + soraLevelList + soraBonusList + formLevels

    if not locationType.Critical in exclude:
        locationList += soraStartingItems

    for location in locationList:
        if not any(locationType in exclude for locationType in location.LocationTypes):
            validLocationList.append(location)

    if len(validLocationList) < len(itemsList):
        return "Too few locations, can't randomize."


    if goMode:
        proofs = [item for item in itemsList if item.ItemType == itemType.PROOF or item.ItemType == itemType.PROOF_OF_CONNECTION or item.ItemType == itemType.PROOF_OF_PEACE]
        itemsList.remove(proofs[0])
        itemsList.remove(proofs[1])
        itemsList.remove(proofs[2])
        freeLocations = [location for location in locationList if "Free" in location.LocationTypes]
        for i in range(0,len(freeLocations)):
            freeLocations[i].setReward(proofs[i].Id)
            #spoilerLogLocations.append(freeLocations[i])

    if promiseCharm:
        itemsList.insert(0, KH2Item(524, "Promise Charm","Proof"))


    spoilerLogLocationItems = []

    randomizeLocations(itemsList, locationList, exclude, spoilerLogLocationItems)

    #FILL REMAINING LOCATIONS WITH JUNK
    for location in locationList:
        if not levelChoice in location.LocationTypes:
            location.setReward(random.choice(junkList).Id)

    #RANDOMIZE SORA STATS
    for i in range(1,len(soraLevelList)):
        randomStat = lvupStats.pop(lvupStats.index(random.choice(lvupStats)))

        soraLevelList[i].setStat(soraLevelList[i-1],randomStat)
        if soraLevelList[i].getReward() == 0:
            if len(lvupAp) > 0:
                randomAp = lvupAp.pop(lvupAp.index(random.choice(lvupAp)))
                soraLevelList[i].setAp(soraLevelList[i-1],randomAp)

    donaldLocationList = donaldItemList + donaldBonusList + donaldStartingList

    randomizeLocations(donaldAbilityList, donaldLocationList, exclude, spoilerLogLocationItems)

    goofyLocationList = goofyItemList + goofyBonusList + goofyStartingList

    randomizeLocations(goofyAbilityList, goofyLocationList, exclude, spoilerLogLocationItems)

    #SORA BONUS LEVEL STATS
    for bonus in soraBonusList:
        if bonus.HasStat:
            randomStat = random.choice(bonsStats)
            bonus.setStat(randomStat)
            bonsStats.remove(randomStat)

    #FORM EXPERIENCE
    for formLevel in formLevels:
        formLevel.Experience = round(formExp[int(formLevel.FormId)][int(formLevel.FormLevel)] / formExpMult[str(formLevel.FormId)])

    #SORA EXPERIENCE
    for level in soraLevelList:
        level.Exp = round(soraExp[level.Level] / soraExpMult)
        

    sysBarOut = "- id: 17198\r\n  en: '{hashString}'".format(hashString = generateHashString())


    commandMenuAssets = RandomizeCmdMenus(cmdMenuChoice)

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
    bonusList = soraBonusList+donaldBonusList+goofyBonusList
    for bons in bonusList:
        if not bons.RewardId in formattedBons.keys():
            formattedBons[bons.RewardId] = {}
        formattedBons[bons.RewardId][bons.getCharacterName()] = bons

    formattedFmlv = {}
    for fmlv in formLevels:
        if not fmlv.getFormName() in formattedFmlv.keys():
            formattedFmlv[fmlv.getFormName()] = []
        formattedFmlv[fmlv.getFormName()].append(fmlv)

    formattedStats = {'Stats': keybladeStats+donaldItemList+goofyItemList}

    formattedPlrp = []
    if not locationType.Critical in exclude:
        padStartingItem(formattedPlrp, LocationList.criticalBonus)
    
    padStartingItem(formattedPlrp, LocationList.lionStartWithDash)

    padStartingItem(formattedPlrp, LocationList.donaldStarting)

    padStartingItem(formattedPlrp, LocationList.goofyStarting)

    
    spoilerLogOut = generateSpoilerLog(spoilerLogLocationItems)

    hintsOut = Hints.generateHints(spoilerLogOut, hintsType)
    

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

        plrpList = yaml.dump(formattedPlrp, line_break="\r\n")
        outZip.writestr("PlrpList.yml",plrpList)

        enemySpoilers = None
        if not enemyOptions["boss"] == "Disabled":
            if enemyOptions.get("boss", False) or enemyOptions.get("enemy", False):
                from khbr.randomizer import Randomizer as khbr
                enemySpoilers = khbr().generateToZip("kh2", enemyOptions, mod, outZip)

        if spoilerLog:
            outZip.writestr("spoilerlog.txt",json.dumps(spoilerLogOut, indent=4, cls=ItemEncoder))
            if enemySpoilers:
                outZip.writestr("enemyspoilers.txt", json.dumps(enemySpoilers, indent=4))

        outZip.writestr("hints"+hintsType, json.dumps(hintsOut))
        outZip.writestr("sys.yml",sysBarOut)

        mod["assets"] += commandMenuAssets
        mod["title"] += " {}".format(seedName)
        print(len(mod["assets"]))
        print(len(set([json.dumps(i) for i in mod["assets"]])))
        print(yaml.dump(mod))
        modOut = "#" + seedName + "\n" + yaml.dump(mod)
        outZip.writestr("mod.yml", modOut)
        if commandMenuAssets:
            for folderName, subfolders, filenames in os.walk("CommandMenus"):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    outZip.write(filePath, filePath)
        outZip.close()

    data.seek(0)
    return data



def padStartingItem(formattedPlrp, startingItem):
    while len(startingItem.Objects) < 58:
        startingItem.setReward(0)
    formattedPlrp.append(startingItem)




def generateHashString():
    hashString = ""
    for i in range(7):
        hashString += random.choice(hashTextEntries)
        if not i == 6:
            hashString += " "
    return hashString

def randomizeKeyblades(keybladeStats, validKeybladeAbilities, keybladeMinStat, keybladeMaxStat):
    for keyblade in keybladeStats:
        randomAbility = random.choice(validKeybladeAbilities)
        keyblade.Ability = randomAbility.Id
        validKeybladeAbilities.remove(randomAbility)
        keyblade.Attack = random.randint(keybladeMinStat, keybladeMaxStat)
        keyblade.Magic = random.randint(keybladeMinStat, keybladeMaxStat)

def randomizeLocations(itemsList, locationList, exclude, spoilerLogLocationItems):
    for item in itemsList[:]:
        while(item in itemsList):
            randomLocation = random.choice(locationList)
            if not item.ItemType in randomLocation.InvalidChecks and not any(locationType in exclude for locationType in randomLocation.LocationTypes):
                randomLocation.setReward(item.Id)
                itemsList.remove(item)
                if not randomLocation.DoubleReward:
                    locationList.remove(randomLocation)
                elif not randomLocation.BonusItem2 == 0:
                    locationList.remove(randomLocation)

                spoilerLogLocationItems.append((randomLocation,item))

#not DoubleReward = remove
#DoubleReward + BonusItem2 = remove

# for testing
if __name__ == '__main__':
    seed = "XYZ"
    data = Randomize(seedName=seed, cmdMenuChoice="randAll").getbuffer()
    open(seed, "wb").write(data)