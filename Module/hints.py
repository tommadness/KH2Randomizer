from List.configDict import itemType, locationType
from Class.locationClass import KH2ItemStat
import zipfile, base64, json, random

class Hints:
    def generateHints(locationItems, hintsType, seedName, outZip):
        hintsText = {}
        hintsText['hintsType'] = hintsType
        if hintsType == "Shananas":
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON]
            hintsText['world'] = {}
            for location,item in locationItems:
                if isinstance(location, KH2ItemStat):
                    continue
                if item.ItemType in importantChecks or item.Name == "Second Chance" or item.Name == "Once More":
                    if not location.LocationTypes[0] in hintsText['world']:
                        hintsText['world'][location.LocationTypes[0]] = []
                    hintsText['world'][location.LocationTypes[0]].append(item.Name)

        if hintsType == "JSmartee":
            hintedWorlds = []
            reportsList = list(range(1,14))
            hintsText['Reports'] = {}
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON, itemType.REPORT, "Second Chance", "Once More"]
            worldChecks = {}
            for location,item in locationItems:
                if isinstance(location, KH2ItemStat) or location.LocationTypes[0] == locationType.Free or location.LocationTypes[0] == locationType.Critical:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    if not location.LocationTypes[0] in worldChecks:
                        worldChecks[location.LocationTypes[0]] = []
                    worldChecks[location.LocationTypes[0]].append(item)
                    if item.ItemType in [itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE]:
                        if not location.LocationTypes[0] in hintedWorlds:
                            hintedWorlds.append(location.LocationTypes[0])
                        else:
                            if item.ItemType is itemType.PROOF_OF_CONNECTION:
                                proof_of_connection_index = hintedWorlds.index(location.LocationTypes[0])
                            if item.ItemType is itemType.PROOF_OF_PEACE:
                                proof_of_peace_index = hintedWorlds.index(location.LocationTypes[0])
                    if item.ItemType is itemType.REPORT:
                        reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                        if locationType.LW in location.LocationTypes:
                            isReportOnTerra[reportNumber-1] = True
                        if isinstance(location,KH2Treasure) and location.Description in ["00 Winner's Proof","00 Proof of Peace"]:
                            isReportOnMushroom[reportNumber-1] = True

            if len(worldChecks.keys()) < 13:
                raise ValueError("Too few worlds. Add more worlds or change hint system.")


            if locationType.FormLevel in hintedWorlds:
                for world in worldChecks:
                    if not world in hintedWorlds and any(item.ItemType == itemType.FORM for item in worldChecks[world]):
                        hintedWorlds.append(world)


            if locationType.HUNDREDAW in hintedWorlds:
                for world in worldChecks:
                    if not world in hintedWorlds and any(item.ItemType == itemType.TORN_PAGE for item in worldChecks[world]):
                        hintedWorlds.append(world)


            if locationType.Atlantica in hintedWorlds:
                for world in worldChecks:
                    if not world in hintedWorlds and any(item.ItemType == itemType.THUNDER or item.ItemType == itemType.MAGNET for item in worldChecks[world]):
                        hintedWorlds.append(world)


            for world in hintedWorlds:
                random.shuffle(reportsList)
                reportNumber = reportsList.pop()
                hintsText["Reports"][reportNumber] = {
                    "World": world,
                    "Count": len(worldChecks[world]),
                    "Location": ""
                }

            hintedHints = []

            for reportNumber in hintsText["Reports"].keys():
                for world in worldChecks:
                    if not world in hintedWorlds and not world in hintedHints and any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                        hintedHints.append(world)
                        hintsText["Reports"][reportNumber]["Location"] = world

            # hintedWorlds is now all the required hinted worlds. We'll see if we can also hint the reports that hint proofs
            if len(hintedWorlds) > 13:
                hintedWorlds = hintedWorlds[0:13]

            random.shuffle(reportOrdering)
            proof_report_order = None
            for ordering in reportOrdering:
                remaining_report_slots = 13-len(hintedWorlds)
                worlds_to_add = []
                for index,reportNumber in enumerate(ordering):
                    invalid = False
                    for world in worldChecks:
                        if any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                            #don't allow a report for a proof to be locked by that proof
                            if (proof_of_peace_index is index and isReportOnMushroom[reportNumber-1]) or \
                               (proof_of_connection_index is index and isReportOnTerra[reportNumber-1]):
                                invalid = True
                                break
                            if world not in hintedWorlds:
                                # totally fine if we have space
                                worlds_to_add.append(world)
                                remaining_report_slots-=1
                                break
                    if invalid:
                        break
                if remaining_report_slots >= 0:
                    proof_report_order = ordering
                    hintedWorlds+=worlds_to_add
                    break

            # ------------------ Done filling required hinted worlds --------------------------------

            for index,world in enumerate(hintedWorlds):
                if index < 3 and proof_report_order is not None:
                    reportNumber = proof_report_order[index]
                    reportsList.remove(reportNumber)
                else:
                    random.shuffle(reportsList)
                    reportNumber = reportsList.pop()
                hintsText["Reports"][reportNumber] = {
                    "World": world,
                    "Count": len(worldChecks[world]),
                    "Location": ""
                }

            while len(reportsList) > 0:
                random.shuffle(reportsList)
                worlds = list(worldChecks.keys())
                random.shuffle(worlds)
                randomWorld = None
                if not worlds[0] in hintedWorlds and not worlds[0] in hintedHints:
                    randomWorld = worlds[0]
                else:
                    continue
                reportNumber = reportsList.pop()

                hintsText["Reports"][reportNumber] = {
                    "World": randomWorld,
                    "Count": len(worldChecks[randomWorld]),
                    "Location": ""

                }
                hintedWorlds.append(randomWorld)

            for reportNumber in hintsText["Reports"].keys():
                if not hintsText["Reports"][reportNumber]["Location"] == "":
                    continue
                for world in worldChecks:
                    if any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                        hintsText["Reports"][reportNumber]["Location"] = world

        outZip.writestr("{seedName}.Hints".format(seedName = seedName), base64.b64encode(json.dumps(hintsText).encode('utf-8')).decode('utf-8'))

    def getOptions():
        return ["Disabled","Shananas","JSmartee"]
