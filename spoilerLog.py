import itemClass
import locationClass



def generateSpoilerLog(locationItems):
    outDict = {"Weapons": []}
    for location,item in locationItems:
        if not location.LocationTypes == []:
            if not location.LocationTypes[0] in outDict.keys():
                outDict[location.LocationTypes[0]] = []
            outDict[location.LocationTypes[0]].append((location.getDescription(),item.Name))
        else:
            outDict["Weapons"].append((location.getDescription(), item.Name))
    return outDict