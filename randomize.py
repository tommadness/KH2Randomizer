from ItemList import itemList
from LocationList import treasureList, soraLevelList, soraBonusList, formLevels
import random
import yaml
import zipfile
import os
import sys

def noop(self, *args, **kw):
    pass

locationList = treasureList + soraLevelList + soraBonusList + formLevels

#random.seed("garf")
seedOut = []
while(len(itemList)>0):
    randomLocation = random.choice(locationList)
    if not itemList[0].ItemType in randomLocation.InvalidChecks:
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

yaml.emitter.Emitter.process_tag = noop

with zipfile.ZipFile("randoSeed.zip", "w") as outZip:

    trsrList = yaml.dump(formattedTrsr)
    outZip.writestr("TrsrList.yml",trsrList)

    lvupList = yaml.dump(formattedLvup)
    outZip.writestr("LvupList.yml",lvupList)

    outZip.close()


print(seedOut)