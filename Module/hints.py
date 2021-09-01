from List.configDict import itemType, locationType
from Class.locationClass import KH2ItemStat,KH2Treasure
import zipfile, base64, json, random
from itertools import permutations


class Hints:
    def generateHints(locationItems, hintsType, seedName):
        if hintsType=="Disabled":
            return None
        hintsText = {}
        hintsText['hintsType'] = hintsType
        if hintsType == "Shananas":
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON]
            hintsText['world'] = {}
            for location,item in locationItems:
                if isinstance(location, KH2ItemStat):
                    continue
                if item.ItemType in importantChecks or item.Name == "Second Chance" or item.Name == "Once More":
                    if not location.LocationTypes[0] in hintsText['world']:
                        hintsText['world'][location.LocationTypes[0]] = []
                    hintsText['world'][location.LocationTypes[0]].append(item.Name)

        if hintsType == "JSmartee":
            proof_of_connection_index = None
            proof_of_peace_index = None
            hintedWorlds = []
            reportsList = list(range(1,14))
            # different possibilities for how to make the reports hinting the proofs hinted
            temp_ordering = permutations(reportsList, 3)
            reportOrdering = []
            for o in temp_ordering:
                reportOrdering.append(o)
            hintsText['Reports'] = {}
            isReportOnMushroom = [False for x in range(13)]
            isReportOnTerra = [False for x in range(13)]
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON, itemType.REPORT, "Second Chance", "Once More"]
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
                            if item.ItemType is itemType.PROOF_OF_CONNECTION:
                                proof_of_connection_index = len(hintedWorlds)
                            if item.ItemType is itemType.PROOF_OF_PEACE:
                                proof_of_peace_index = len(hintedWorlds)
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

            forms_need_hints = (locationType.FormLevel in hintedWorlds)
            pages_need_hints = (locationType.HUNDREDAW in hintedWorlds)
            mag_thun_need_hints = (locationType.Atlantica in hintedWorlds)

            # following the priority of Proofs > Forms > Pages > Thunders > Magnets > Proof Reports
            if forms_need_hints:
                for world in worldChecks:
                    if not world in hintedWorlds and any(item.ItemType == itemType.FORM for item in worldChecks[world]):
                        hintedWorlds.append(world)


            if pages_need_hints:
                for world in worldChecks:
                    if not world in hintedWorlds and any(item.ItemType == itemType.TORN_PAGE for item in worldChecks[world]):
                        hintedWorlds.append(world)


            if mag_thun_need_hints:
                for world in worldChecks:
                    if not world in hintedWorlds and any(item.ItemType == itemType.THUNDER for item in worldChecks[world]):
                        hintedWorlds.append(world)

            if mag_thun_need_hints:
                for world in worldChecks:
                    if not world in hintedWorlds and any(item.ItemType == itemType.MAGNET for item in worldChecks[world]):
                        hintedWorlds.append(world)

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
                                if world not in worlds_to_add:
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
                if not worlds[0] in hintedWorlds:
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

            if len(hintedWorlds) != len(set(hintedWorlds)):
                raise RuntimeError("Two reports hint the same location. This is an error, try a new seedname.")

        return hintsText

    def writeHints(hintsText,seedName,outZip):
        outZip.writestr("{seedName}.Hints".format(seedName = seedName), base64.b64encode(json.dumps(hintsText).encode('utf-8')).decode('utf-8'))

    def getOptions():
        return ["Disabled","Shananas","JSmartee"]