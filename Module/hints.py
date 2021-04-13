from List.configDict import itemType

class Hints:
    def generateHints(spoilerLog, hintsType):
        hintsText = {}
        hintsText['hintsType'] = hintsType
        if hintsType == "Shananas":
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON]
            hintsText['world'] = {}
            for world in spoilerLog:
                if not world == "Weapons" and not world == "Critical Bonuses" and not world == "Garden of Assemblage":
                    if not world in hintsText.keys():
                        hintsText['world'][world] = 0
                    for check in spoilerLog[world]:
                        if check[1].ItemType in importantChecks or (check[1].Name in ["Second Chance", "Once More"] and check[1].ItemType == itemType.SUPPORT_ABILITY):
                            hintsText['world'][world] += 1
                    
        return hintsText

    def getOptions():
        return ["Disabled","Shananas"]


