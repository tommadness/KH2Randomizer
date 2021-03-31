from ItemList import *
from LocationList import *
import random
import yaml

#random.seed("garf")
seedOut = []
while(len(itemList)>0):
    randomLocation = random.choice(locationList)
    if not itemList[0].ItemType in randomLocation.InvalidChecks:
        randomLocation.setReward(itemList[0].Id)
        itemList.remove(itemList[0])
        seedOut.append(randomLocation)
        locationList.remove(randomLocation)


print(seedOut)