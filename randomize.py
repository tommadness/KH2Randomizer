from ItemList import itemList, supportAbilityList, actionAbilityList
from LocationList import treasureList, soraLevelList, soraBonusList, formLevels, keybladeStats
import random
import yaml
import zipfile
import string
import os
import sys

def noop(self, *args, **kw):
    pass

def Randomize(seedName="", exclude=[], keybladeAbilities = ["Support"], keybladeMinStat = 0, keybladeMaxStat = 7):
    locationList = treasureList + soraLevelList + soraBonusList + formLevels

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
        keyblade.Ability = randomAbility
        validKeybladeAbilities.remove(randomAbility)
        keyblade.Attack = random.randint(keybladeMinStat,. keybladeMaxStat + 1)
        keyblade.Magic = random.randint(keybladeMinStat, keybladeMaxStat + 1)

    itemList += validKeybladeAbilities + invalidKeybladeAbilities


    #SORA REWARDS

    seedOut = []
    while(len(itemList)>0):
        randomLocation = random.choice(locationList)
        if not itemList[0].ItemType in randomLocation.InvalidChecks and not any(location in exclude for location in randomLocation.LocationTypes):
            randomLocation.setReward(itemList[0].Id)
            itemList.remove(itemList[0])
            seedOut.append(randomLocation)
            locationList.remove(randomLocation)

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

    formattedStats = {'Stats': keybladeStats}

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

        outZip.close()