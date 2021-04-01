from ItemList import itemList, supportAbilityList, actionAbilityList
from LocationList import treasureList, soraLevelList, soraBonusList, formLevels, keybladeStats
from experienceValues import formExp, soraExp
import random
import yaml
import zipfile
import string

def noop(self, *args, **kw):
    pass

def Randomize(seedName="", exclude=[], keybladeAbilities = ["Support"], keybladeMinStat = 0, keybladeMaxStat = 7, formExpMult = {1:1,2:1,3:1,4:1,5:1}, soraExpMult = 1 ):

    exclude.append("Level1Form") #Always exclude level 1 forms from getting checks

    if seedName == "":
        characters = string.ascii_letters + string.digits
        seedName = (''.join(random.choice(characters) for i in range(15)))
    random.seed(seedName)
    
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
    locationList = treasureList + soraLevelList + soraBonusList + formLevels

    seedOut = []
    while(len(itemsList)>0):
        randomLocation = random.choice(locationList)
        if not itemsList[0].ItemType in randomLocation.InvalidChecks and not any(location in exclude for location in randomLocation.LocationTypes):
            randomLocation.setReward(itemsList[0].Id)
            itemsList.remove(itemsList[0])
            seedOut.append(randomLocation)
            locationList.remove(randomLocation)


    #FORM EXPERIENCE
    for formLevel in formLevels:
        formLevel.Experience = round(formExp[formLevel.FormId][formLevel.FormLevel] / formExpMult[formLevel.FormId])

    #SORA EXPERIENCE
    for level in soraLevelList:
        level.Exp = round(soraExp[level.Level] / soraExpMult)


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
        formattedBons[bons.RewardId][bons.CharacterId] = bons

    formattedFmlv = {}
    for fmlv in formLevels:
        if not fmlv.getFormName() in formattedFmlv.keys():
            formattedFmlv[fmlv.getFormName()] = []
        formattedFmlv[fmlv.getFormName()].append(fmlv)

    formattedStats = {'Stats': keybladeStats}


    #OUTPUT
    yaml.emitter.Emitter.process_tag = noop

    with zipfile.ZipFile("randoSeed.zip", "w") as outZip:

        trsrList = yaml.dump(formattedTrsr)
        outZip.writestr("TrsrList.yml",trsrList)

        lvupList = yaml.dump(formattedLvup)
        outZip.writestr("LvupList.yml",lvupList)

        bonsList = yaml.dump(formattedBons)
        outZip.writestr("BonsList.yml",bonsList)

        statsList = yaml.dump(formattedStats)
        outZip.writestr("ItemList.yml",statsList)

        fmlvList = yaml.dump(formattedFmlv)
        outZip.writestr("FmlvList.yml",fmlvList)

        outZip.close()