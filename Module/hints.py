from List.configDict import itemType

class Hints:
    def generateHints(locationItems, hintsType):
        hintsText = {}
        hintsText['hintsType'] = hintsType
        if hintsType == "Shananas":
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON]
            hintsText['world'] = {}
            for location,item in locationItems:
                if item.ItemType in importantChecks:
                    if not location.LocationTypes[0] in hintsText['world']:
                        hintsText['world'][location.LocationTypes[0]] = []
                    hintsText['world'][location.LocationTypes[0]].append(item.Name)
                    
        return hintsText

    def getOptions():
        return ["Disabled","Shananas"]


