from Module.weighting import LocationWeights



def itemSpoilerDictionary(locationItems, weights: LocationWeights = None, unreachable_locations = None):
    outDict = {}

    for assignment in locationItems:
        location = assignment.location
        if weights and location in weights.location_depths:
            added_string = f" <{weights.getDepth(location)}>"
        else:
            added_string = ""

        if unreachable_locations and location in unreachable_locations:
            prepend_string = "Unreachable "
        else:
            prepend_string = ""


        item = assignment.item
        item2 = assignment.item2
        if not location.LocationTypes == []:
            if not location.LocationTypes[0] in outDict.keys():
                outDict[location.LocationTypes[0]] = []
            outDict[location.LocationTypes[0]].append((prepend_string+location.Description+added_string,item))
            if item2 is not None:
                outDict[location.LocationTypes[0]].append((prepend_string+location.Description+added_string,item2))
    return outDict

def levelStatsDictionary(level_stats):
    outDict = {}
    for lvl in level_stats:
        desc = lvl.location.Description
        split_desc=desc.split(' ')
        if len(split_desc) > 2:
            desc = split_desc[0] + " " +split_desc[2]
        outDict[desc] = {"experience":lvl.experience,"strength":lvl.strength, "magic": lvl.magic, "defense": lvl.defense, "ap":lvl.ap }
    return outDict