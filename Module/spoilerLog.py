import Class.itemClass
import Class.locationClass



def itemSpoilerDictionary(locationItems):
    outDict = {}
    for assignment in locationItems:
        location = assignment.location
        item = assignment.item
        item2 = assignment.item2
        if not location.LocationTypes == []:
            if not location.LocationTypes[0] in outDict.keys():
                outDict[location.LocationTypes[0]] = []
            outDict[location.LocationTypes[0]].append((location.Description,item))
            if item2 is not None:
                outDict[location.LocationTypes[0]].append((location.Description,item2))
    return outDict