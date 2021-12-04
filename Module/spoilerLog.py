from Module.weighting import LocationWeights



def itemSpoilerDictionary(locationItems, weights: LocationWeights = None):
    outDict = {}

    for assignment in locationItems:
        location = assignment.location
        if weights and location in weights.location_depths:
            added_string = f" <{weights.location_depths[location]}>"
        else:
            added_string = ""
        item = assignment.item
        item2 = assignment.item2
        if not location.LocationTypes == []:
            if not location.LocationTypes[0] in outDict.keys():
                outDict[location.LocationTypes[0]] = []
            outDict[location.LocationTypes[0]].append((location.Description+added_string,item))
            if item2 is not None:
                outDict[location.LocationTypes[0]].append((location.Description+added_string,item2))
    return outDict

def levelStatsDictionary(level_stats):
    outDict = {}
    for lvl in level_stats:
        desc = lvl.location.Description
        outDict[desc] = {"experience":lvl.experience,"strength":lvl.strength, "magic": lvl.magic, "defense": lvl.defense, "ap":lvl.ap }
    return outDict