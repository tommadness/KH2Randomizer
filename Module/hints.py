from Class.exceptions import HintException
from List.ItemList import Items
from List.configDict import itemType, locationType
import base64, json, random
from itertools import permutations,chain


class Hints:
    def convertItemAssignmentToTuple(itemAssignment):
        locationItems = []
        for assignment in itemAssignment:
            locationItems.append((assignment.location,assignment.item))
            if assignment.item2 is not None:
                locationItems.append((assignment.location,assignment.item2))
        return locationItems

    def generateHints(locationItems, hintsType, excludeList, preventSelfHinting, allowProofHinting, allowReportHinting, pointHintValues, spoilerHintValues, tracker_includes):
        if locationType.HB in excludeList and (locationType.TTR not in excludeList or locationType.CoR not in excludeList):
            excludeList.remove(locationType.HB)
        if locationType.OC in excludeList and (locationType.OCCups not in excludeList or locationType.OCCups not in excludeList):
            excludeList.remove(locationType.OC)

        locationItems = Hints.convertItemAssignmentToTuple(locationItems)
        if hintsType=="Disabled":
            return None
        hintsText = {}
        hintsText['hintsType'] = hintsType
        hintsText['settings'] = tracker_includes #+ ["Olympus Stone", "Hades Cup Trophy", "Unknown Disk"]
        if hintsType == "Shananas":
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON] + [itemType.STORYUNLOCK] #+ [itemType.TROPHY, itemType.MEMBERSHIPCARD, "Olympus Stone"]
            hintsText['world'] = {}
            for location,item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name == "Second Chance" or item.Name == "Once More":
                    world_of_location = location.LocationTypes[0]
                    if world_of_location == locationType.Puzzle or world_of_location == locationType.SYNTH:
                        world_of_location = "Creations"
                    if not world_of_location in hintsText['world']:
                        hintsText['world'][world_of_location] = []
                    hintsText['world'][world_of_location].append(item.Name)
        
        report_master = [None]*14
        found_reports = False
        for location,item in locationItems:
            if item.ItemType is itemType.REPORT:
                reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                found_reports = True
                if locationType.Critical in location.LocationTypes:
                    report_master[reportNumber] = [""]
                else:
                    report_master[reportNumber] = location.LocationTypes
    
        if hintsType == "Path":
            hintableWorlds = [locationType.Level,locationType.LoD,locationType.BC,locationType.HB,locationType.TT,locationType.TWTNW,locationType.SP,locationType.Atlantica,locationType.PR,locationType.OC,locationType.Agrabah,locationType.HT,locationType.PL,locationType.DC,locationType.HUNDREDAW,locationType.STT,locationType.FormLevel,"Creations"]
            importantChecks = [itemType.REPORT, itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON] + [itemType.STORYUNLOCK] #+ [itemType.TROPHY, itemType.MEMBERSHIPCARD, "Olympus Stone"]
            world_to_vanilla_ICs = {}
            world_to_vanilla_ICs[locationType.Level] = [415,416]
            world_to_vanilla_ICs[locationType.FormLevel] = [26,27,29,31,563]
            world_to_vanilla_ICs[locationType.Atlantica] = [22]
            world_to_vanilla_ICs[locationType.TWTNW] = [87]
            world_to_vanilla_ICs[locationType.PR] = [87,160,62]
            world_to_vanilla_ICs[locationType.DC] = [32,88,27]
            world_to_vanilla_ICs[locationType.HUNDREDAW] = [24]
            world_to_vanilla_ICs[locationType.Agrabah] = [159,21,32,72]
            world_to_vanilla_ICs[locationType.BC] = [24,88,59]
            world_to_vanilla_ICs[locationType.TT] = [26,563]
            world_to_vanilla_ICs[locationType.SP] = [88,74]
            world_to_vanilla_ICs[locationType.HT] = [87,60]
            world_to_vanilla_ICs[locationType.PL] = [32,21,23,61]
            world_to_vanilla_ICs[locationType.LoD] = [23,32,55]
            world_to_vanilla_ICs[locationType.OC] = [23,54]
            world_to_vanilla_ICs[locationType.HB] = [21,22,383,25,31,24,32,375,376,369]
            world_to_vanilla_ICs[locationType.STT] = world_to_vanilla_ICs[locationType.TT]
            world_to_vanilla_ICs["Creations"] = []
            world_to_vanilla_ICs[locationType.Critical] = []
            world_to_vanilla_ICs[locationType.Free] = []

            ICs_to_hintable_worlds = {}

            # where did each world drop their breadcrumbs
            # vanilla world to randomized world
            breadcrumb_map = {}

            for key,item_list in world_to_vanilla_ICs.items():
                if key not in breadcrumb_map:
                    breadcrumb_map[key] = set()
                for i in item_list:
                    if i not in ICs_to_hintable_worlds:
                        ICs_to_hintable_worlds[i] = []
                    ICs_to_hintable_worlds[i].append(key)
            
            hintsText['world'] = {}
            hintsText['Reports'] = {}
            proof_of_connection_world = None
            proof_of_peace_world = None
            proof_of_nonexistence_world = None

            for x in hintableWorlds:
                hintsText['world'][x] = []



            for location,item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name == "Second Chance" or item.Name == "Once More":
                    world_of_location = location.LocationTypes[0]
                    if world_of_location == locationType.Puzzle or world_of_location == locationType.SYNTH:
                        world_of_location = "Creations"
                    if not world_of_location in hintsText['world']:
                        hintsText['world'][world_of_location] = []
                    hintsText['world'][world_of_location].append(item.Name)                        
                    if item.ItemType in [itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE]:
                        if item.ItemType is itemType.PROOF_OF_CONNECTION:
                            proof_of_connection_world = world_of_location
                        elif item.ItemType is itemType.PROOF_OF_PEACE:
                            proof_of_peace_world = world_of_location
                        elif item.ItemType is itemType.PROOF:
                            proof_of_nonexistence_world = world_of_location
                    elif item.ItemType != itemType.REPORT and item.ItemType != itemType.PROMISE_CHARM: # no vanilla final form location and ignore reports
                        # this item could have come from any world from this list
                        for w in ICs_to_hintable_worlds[item.Id]:
                            if world_of_location in hintableWorlds:
                                breadcrumb_map[w].add(world_of_location)
            

            hintable_world_list = list(set(chain(breadcrumb_map[proof_of_connection_world] if proof_of_connection_world else [],breadcrumb_map[proof_of_peace_world] if proof_of_peace_world else [],breadcrumb_map[proof_of_nonexistence_world] if proof_of_nonexistence_world else [])))
            barren_world_list = [x for x in hintableWorlds if x not in hintable_world_list]

            hintable_world_list.sort(reverse=True,key=lambda x : len(hintsText['world'][x]))
            barren_world_list.sort(reverse=True,key=lambda x : len(hintsText['world'][x]))


            report_texts = []

            def create_hint_text(world):
                num_items = len(hintsText['world'][world])
                hint_text = ""
                world_text = world 
                if world == locationType.Level:
                    world_text = "Sora's Heart"
                if world == locationType.TWTNW:
                    world_text = "TWTNW"
                if world == locationType.DC:
                    world_text = "Disney Castle"

                points_to_connection = proof_of_connection_world and world in breadcrumb_map[proof_of_connection_world]
                points_to_peace = proof_of_peace_world and world in breadcrumb_map[proof_of_peace_world]
                points_to_nonexistence = proof_of_nonexistence_world and world in breadcrumb_map[proof_of_nonexistence_world]

                proof_list = [] + (["Connection"] if points_to_connection else []) + (["Peace"] if points_to_peace else []) + (["Nonexistence"] if points_to_nonexistence else [])
                if len(proof_list)==0:
                    proof_list = ["none"]

                if num_items == 0:
                    hint_text = f"{world_text} has nothing, sorry."
                elif not points_to_connection and not points_to_nonexistence and not points_to_peace:
                    hint_text = f"{world_text} has no path to the light."
                elif points_to_connection and points_to_nonexistence and points_to_peace:
                    hint_text = f"{world_text} has a path to all lights."
                elif points_to_connection and points_to_peace:
                    hint_text = f"{world_text} is on the path to Connection and Peace."
                elif points_to_connection and points_to_nonexistence:
                    hint_text = f"{world_text} is on the path to Connection and Nonexistence."
                elif points_to_nonexistence and points_to_peace:
                    hint_text = f"{world_text} is on the path to Nonexistence and Peace."
                elif points_to_nonexistence:
                    hint_text = f"{world_text} is on the path to Nonexistence."
                elif points_to_peace:
                    hint_text = f"{world_text} is on the path to Peace."
                elif points_to_connection:
                    hint_text = f"{world_text} is on the path to Connection."

                return hint_text,world,proof_list

            
            for x in hintable_world_list:
                report_texts.append(create_hint_text(x))
            for x in barren_world_list:
                report_texts.append(create_hint_text(x))


            if not found_reports:
                for reportNumber in range(1,14):
                    report_master[reportNumber] = [""]

            valid_reports = False
            for iter in range(1,10):
                report_texts = report_texts[0:13]
                random.shuffle(report_texts)
                valid_reports = True
                for x in range(1,14):
                    report_location = report_master[x][0]
                    report_hint_world = report_texts[x-1][1]
                    if report_hint_world==report_location:
                        valid_reports = False
                        break
                if valid_reports:
                    break
            if not valid_reports:
                raise HintException("Failed to assign path hints due to self hinting")



            for x in range(1,14):
                report_location = report_master[x][0]
                hintsText["Reports"][x] = {
                            "Text": report_texts[x-1][0],
                            "HintedWorld": report_texts[x-1][1],
                            "ProofPath": report_texts[x-1][2],
                            "Location": report_location
                        }

        if hintsType == "JSmartee":
            proof_of_connection_index = None
            proof_of_peace_index = None
            proof_of_nonexistence_index = None
            worldsToHint = []
            reportRestrictions = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
            reportsList = list(range(1,14))
            hintsText['Reports'] = {}
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON, itemType.REPORT, "Second Chance", "Once More"] + [itemType.STORYUNLOCK] #+ [itemType.TROPHY, itemType.MEMBERSHIPCARD, "Olympus Stone"]
            hintableWorlds = [locationType.Level,locationType.LoD,locationType.BC,locationType.HB,locationType.TT,locationType.TWTNW,locationType.SP,locationType.Atlantica,locationType.PR,locationType.OC,locationType.Agrabah,locationType.HT,locationType.PL,locationType.DC,locationType.HUNDREDAW,locationType.STT,locationType.FormLevel]

            if locationType.SYNTH not in excludeList or locationType.Puzzle not in excludeList:
                hintableWorlds += ["Creations"]

            freeReports = []

            worldChecks = {}
            for h in hintableWorlds:
                if h not in excludeList:
                    worldChecks[h] = []
                    
            for location,item in locationItems:
                if location.LocationTypes[0] in [locationType.WeaponSlot, locationType.Free, locationType.Critical]:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    world_of_location = location.LocationTypes[0]
                    if world_of_location == locationType.Puzzle or world_of_location == locationType.SYNTH:
                        world_of_location = "Creations"
                    worldChecks[world_of_location].append(item)
                    if item.ItemType in [itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE]:
                        if not world_of_location in worldsToHint:
                            if item.ItemType is itemType.PROOF_OF_CONNECTION:
                                proof_of_connection_index = len(worldsToHint)
                            elif item.ItemType is itemType.PROOF_OF_PEACE:
                                proof_of_peace_index = len(worldsToHint)
                            elif item.ItemType is itemType.PROOF:
                                proof_of_nonexistence_index = len(worldsToHint)
                            worldsToHint.append(world_of_location)
                        else:
                            if item.ItemType is itemType.PROOF_OF_CONNECTION:
                                proof_of_connection_index = worldsToHint.index(world_of_location)
                            elif item.ItemType is itemType.PROOF_OF_PEACE:
                                proof_of_peace_index = worldsToHint.index(world_of_location)
                            elif item.ItemType is itemType.PROOF:
                                proof_of_nonexistence_index = worldsToHint.index(world_of_location)
            for location,item in locationItems:
                world_of_location = location.LocationTypes[0]
                if world_of_location == locationType.Puzzle or world_of_location == locationType.SYNTH:
                    world_of_location = "Creations"
                if world_of_location in [locationType.Free, locationType.Critical]:
                    if item.ItemType is itemType.REPORT:
                        reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                        freeReports.append(reportNumber)
                    continue
                if item.ItemType is itemType.REPORT:
                    reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                    #report can't hint itself
                    if preventSelfHinting:
                        reportRestrictions[reportNumber-1].append(world_of_location)
                    if locationType.LW in location.LocationTypes:
                        # if report on LW, can't hint world that contains proof of connection
                        if proof_of_connection_index is not None:
                            reportRestrictions[reportNumber-1].append(worldsToHint[proof_of_connection_index])
                    if locationType.Mush13 in location.LocationTypes:
                        # if report on Mushroom, can't hint world that contains proof of peace
                        if proof_of_peace_index is not None:
                            reportRestrictions[reportNumber-1].append(worldsToHint[proof_of_peace_index])

            if len(worldChecks.keys()) < 13:

                while len(worldChecks.keys()) < 13:
                    new_choice = random.choice(hintableWorlds)
                    if new_choice not in worldChecks:
                        worldChecks[new_choice] = []

                # raise HintException("Too few worlds. Add more worlds or change hint system.")

            numProofWorlds = len(worldsToHint)

            forms_need_hints = (locationType.FormLevel in worldsToHint)
            pages_need_hints = (locationType.HUNDREDAW in worldsToHint)
            mag_thun_need_hints = (locationType.Atlantica in worldsToHint)

            # following the priority of Proofs > Story Unlocks > Forms > Pages > Thunders > Magnets > Proof Reports
            
            story_unlock_ids = {locationType.OC : [54],
                                locationType.LoD : [55],
                                locationType.BC : [59],
                                locationType.HT : [60],
                                locationType.PL : [61],
                                locationType.PR : [62],
                                locationType.Agrabah : [72],
                                locationType.HB : [369],
                                locationType.SP : [74],
                                locationType.TT : [375, 376]
                                }
            story_unlocks_for_proofs = []
            for world in hintableWorlds:
                if world in story_unlock_ids:
                    story_unlocks_for_proofs+=story_unlock_ids[world]
            for unlock in story_unlocks_for_proofs:
                # find the unlock item
                for world in worldChecks:
                    items_in_world = worldChecks[world]
                    for item in items_in_world:
                        if item.Id==unlock:
                            if not world in worldsToHint:
                                worldsToHint.append(world)

            if forms_need_hints:
                for world in worldChecks:
                    if not world in worldsToHint and any(item.ItemType == itemType.FORM for item in worldChecks[world]):
                        worldsToHint.append(world)

            if pages_need_hints:
                for world in worldChecks:
                    if not world in worldsToHint and any(item.ItemType == itemType.TORN_PAGE for item in worldChecks[world]):
                        worldsToHint.append(world)

            if mag_thun_need_hints:
                for world in worldChecks:
                    if not world in worldsToHint and any(item.ItemType == itemType.THUNDER for item in worldChecks[world]):
                        worldsToHint.append(world)

            if mag_thun_need_hints:
                for world in worldChecks:
                    if not world in worldsToHint and any(item.ItemType == itemType.MAGNET for item in worldChecks[world]):
                        worldsToHint.append(world)

            # worldsToHint is now all the required hinted worlds. We'll see if we can also hint the reports that hint proofs 
            if len(worldsToHint) > 13:
                worldsToHint = worldsToHint[0:13]

            # at least 1 proof is in a hintable world, so we need to hint it
            if numProofWorlds > 0:
                # different possibilities for how to make the reports hinting the proofs hinted
                temp_ordering = permutations(reportsList, numProofWorlds)
                reportOrdering = []
                for o in temp_ordering:
                    reportOrdering.append(o)
                random.shuffle(reportOrdering)
                # for each assignment of reports to proof locations, try to assign hints to reports
                for ordering in reportOrdering:
                    remaining_report_slots = 13-len(worldsToHint)
                    worlds_to_add = []
                    invalid = False
                    # for each of the chosen reports
                    for index,reportNumber in enumerate(ordering):
                        # figure out which world has that report
                        if reportNumber in freeReports:
                            # if the report is free, it doesn't need to be hinted, and it won't have a restriction
                            continue
                        for world in worldChecks:
                            if any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                                # found the world with this report, now to see if this report can hint a proof location
                                if worldsToHint[index] in reportRestrictions[reportNumber-1]:
                                    invalid = True
                                    break

                                # we found a report that can hint this proof, add the report's world to the list of worlds we want to hint
                                if world not in worldsToHint:
                                    # totally fine if we have space
                                    if world not in worlds_to_add:
                                        worlds_to_add.append(world)
                                        remaining_report_slots-=1
                                break
                        if invalid:
                            break
                    # this check makes it's best attempt to get the proof reports hinted
                    if remaining_report_slots < 0:
                        continue
                    # found a good assignment of reports to point to proofs, lets try assigning the rest
                    if not invalid:
                        proof_report_order = ordering
                        tempWorldsToHint=worldsToHint+worlds_to_add
                        if len(tempWorldsToHint) > 13:
                            tempWorldsToHint = tempWorldsToHint[0:13]

                        # ------------------ Done filling required hinted worlds --------------------------------
                        # ------------------ Attempting to find a good assignment for the hints, after too many tries, return an error
                        for try_number in range(10):
                            hintsText["Reports"] = {}
                            reportsList = list(range(1,14))
                            for index,world in enumerate(tempWorldsToHint):
                                reportNumber = None
                                if index < len(proof_report_order):
                                    reportNumber = proof_report_order[index]
                                    reportsList.remove(reportNumber)
                                else:
                                    random.shuffle(reportsList)
                                    for maybeReportNumber in reportsList:
                                        if world not in reportRestrictions[maybeReportNumber-1]:
                                            reportsList.remove(maybeReportNumber)
                                            reportNumber = maybeReportNumber
                                            break
                                if reportNumber is None:
                                    hintsText["Reports"] = {}
                                    break

                                hintsText["Reports"][reportNumber] = {
                                    "World": world,
                                    "Count": len(worldChecks[world]),
                                    "Location": ""
                                }
                            if len(hintsText["Reports"])==0:
                                continue
                        if len(hintsText["Reports"])!=0:
                            worldsToHint = tempWorldsToHint
                            break

                if len(hintsText["Reports"])==0:
                    raise HintException("Unable to find valid assignment for hints...")

            # slack worlds to hint, can point to anywhere
            while len(reportsList) > 0:
                random.shuffle(reportsList)
                worlds = list(worldChecks.keys())
                random.shuffle(worlds)
                randomWorld = None

                if (worlds[0] not in worldsToHint) and (worlds[0] not in reportRestrictions[reportsList[0]-1]):
                    reportNumber = reportsList.pop(0)
                    randomWorld = worlds[0]
                else:
                    continue

                hintsText["Reports"][reportNumber] = {
                    "World": randomWorld,
                    "Count": len(worldChecks[randomWorld]),
                    "Location": ""

                }
                worldsToHint.append(randomWorld)

            for reportNumber in range(1,14):
                if hintsText["Reports"][reportNumber]["Location"] != "":
                    continue
                for world in worldChecks:
                    if any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                        hintsText["Reports"][reportNumber]["Location"] = world

            if len(worldsToHint) != len(set(worldsToHint)):
                raise HintException("Two reports hint the same location. This is an error, try a new seedname.")

        if hintsType == "Points":
            hintsText['checkValue'] = pointHintValues
            hintsText['world'] = {}
            hintsText['Reports'] = {}
            reportRestrictions = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
            reportsList = list(range(1,14))
            reportRepetition = 0
            tempWorldR = None
            tempItemR = None
            tempExcludeList = []
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON, itemType.REPORT, "Second Chance", "Once More"] + [itemType.STORYUNLOCK] #+ [itemType.TROPHY, itemType.MEMBERSHIPCARD, "Olympus Stone", "Anti-Form"]
            hintableWorlds = [locationType.Level,locationType.LoD,locationType.BC,locationType.HB,locationType.TT,locationType.TWTNW,locationType.SP,locationType.Atlantica,locationType.PR,locationType.OC,locationType.Agrabah,locationType.HT,locationType.PL,locationType.DC,locationType.HUNDREDAW,locationType.STT,locationType.FormLevel,"Creations"]

            for location,item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    world_of_location = location.LocationTypes[0]
                    if world_of_location == locationType.Puzzle or world_of_location == locationType.SYNTH:
                        world_of_location = "Creations"
                    if not world_of_location in hintsText['world']:
                        hintsText['world'][world_of_location] = []
                    hintsText['world'][world_of_location].append(item.Name)

            worldChecks = {}
            worldChecksEdit = {}
            for h in hintableWorlds:
                if h not in excludeList:
                    worldChecks[h] = []
                    worldChecksEdit[h] = []
                    
            for location,item in locationItems:
                world_of_location = location.LocationTypes[0]
                if world_of_location == locationType.Puzzle or world_of_location == locationType.SYNTH:
                    world_of_location = "Creations"
                if world_of_location == locationType.WeaponSlot or world_of_location == locationType.Free or world_of_location == locationType.Critical:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    worldChecks[world_of_location].append(item)
                    worldChecksEdit[world_of_location].append(item)
                if item.ItemType is itemType.REPORT and preventSelfHinting:
                    #report can't hint itself
                    reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                    reportRestrictions[reportNumber-1].append(world_of_location)

            attempts = 0
            while len(reportsList) > 0:
                attempts+=1
                if attempts > 500:
                    raise HintException(f"Points hints got stuck assigning report text with {len(reportsList)}")
            
                temp_worlds = list(worldChecksEdit.keys())
                worlds = []
                
                for place in temp_worlds:
                    if place not in tempExcludeList:
                        worlds.append(place)
            
                random.shuffle(reportsList)
                random.shuffle(worlds)
                randomWorld = None
                
                #reset list
                if len(worlds) == 0:
                    # print("ran out of worlds! resetting worldlist...")
                    # print("-----------------------------------------------------------------------------")
                    #worldChecksEdit = worldChecks #commented out because i think this lead to duplicate item hints
                    tempExcludeList.clear()
                    continue

                if (len(worldChecksEdit[worlds[0]]) != 0):
                    if worlds[0] not in reportRestrictions[reportsList[0]-1]:
                        reportNumber = reportsList.pop(0)
                        randomWorld = worlds[0]
                    else:
                        # print("Self hinting world! Rerolling...")
                        # print("-----------------------------------------------------------------------------")
                        continue
                else:
                    # print(worlds[0] + " has 0 checks! removing from list and rerolling...")
                    # print("-----------------------------------------------------------------------------")
                    tempExcludeList.append(worlds[0])
                    continue
                    
                randomItem = random.choice(worldChecksEdit[randomWorld])
                print("Report " + str(reportNumber) + ": World = " + randomWorld +" | item = " + randomItem.Name)

                #compare current selected world and item to previously rerolled reports
                #more of a jank failsafe really
                if randomWorld == tempWorldR and randomItem.Name == tempItemR:
                    reportRepetition = reportRepetition + 1

                #should we hint proofs?
                if "Proof" in randomItem.Name:
                    # print("Proof found! Is Proof Hinting On?")
                    
                    if allowProofHinting == True:
                        # print("Yes! hinting Proof...")
                        pass
                    else:
                        # print("No. removing item and rerolling...")
                        # print("-----------------------------------------------------------------------------")
                        worldChecksEdit[randomWorld].remove(randomItem)
                        reportsList.append(reportNumber)
                        continue
                    
                #try to hint other reports
                if "Report" in randomItem.Name:
                    # print("Report found! Is Report Hinting On?")
                    if allowReportHinting == True:
                        #prevent reports from hinting themselves (redundant?)
                        # print("Yes! Attempting to Hint Report...")
                        if reportNumber == int(randomItem.Name.replace("Secret Ansem's Report ","")):
                            # print("Self hinting report! rerolling...")
                            # print("-----------------------------------------------------------------------------")
                            tempWorldR = randomWorld
                            tempItemR = randomItem.Name
                            reportsList.append(reportNumber)
                            continue
                    
                        #if we tried to roll for this 3 times already then stop trying and remove the report from being hinted
                        if reportRepetition > 2:
                            # print("Report repetition threshold reached! removing item from world and rerolling...")
                            # print("-----------------------------------------------------------------------------")
                            worldChecksEdit[randomWorld].remove(randomItem)
                            tempWorldR = None
                            tempItemR = None
                            reportRepetition = 0
                            reportsList.append(reportNumber)
                            continue
                            
                        random_number = random.randint(1, 3)
                        # print("Random number = " + str(random_number))
                        # print("Report found! does " + str(random_number) + " = 1?")
                        
                        if random_number == 1:
                            # print("Yes! hinting report...")
                            pass
                        else:
                            # print("No. rerolling...")
                            # print("-----------------------------------------------------------------------------")
                            tempWorldR = randomWorld
                            tempItemR = randomItem.Name
                            reportsList.append(reportNumber)
                            continue
                    else:
                        # print("No. removing item and rerolling...")
                        # print("-----------------------------------------------------------------------------")
                        worldChecksEdit[randomWorld].remove(randomItem)
                        reportsList.append(reportNumber)
                        continue

                hintsText["Reports"][reportNumber] = {
                    "World": randomWorld,
                    "check": randomItem.Name,
                    "Location": ""
                }
                
                # remove hinted item from list
                # print("Removing " + randomItem.Name + " from hintable items")
                # print("Removing " + randomWorld + " hintable worlds")
                # print("-----------------------------------------------------------------------------")
                worldChecksEdit[randomWorld].remove(randomItem)
                tempExcludeList.append(randomWorld)
                
            for reportNumber in range(1,14):
                if hintsText["Reports"][reportNumber]["Location"] != "":
                    continue
                for world in worldChecks:
                    if any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                        hintsText["Reports"][reportNumber]["Location"] = world
 
        if hintsType == "Spoiler":
            hintsText['reveal'] = spoilerHintValues
            hintsText['world'] = {}
            hintsText['Reports'] = {}
            worldsToHint = []
            reportRestrictions = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
            reportsList = list(range(1,14))
            tempExcludeList = []
            IC_Types = {}
            IC_Types["magic"] = ["Fire Element","Blizzard Element","Thunder Element","Cure Element","Magnet Element","Reflect Element"]
            IC_Types["page"] = ["Torn Pages"]
            IC_Types["summon"] = ["Baseball Charm (Chicken Little)","Ukulele Charm (Stitch)","Feather Charm (Peter Pan)","Lamp Charm (Genie)"]
            IC_Types["ability"] = ["Second Chance","Once More"]
            IC_Types["proof"] = ["Proof of Connection","Proof of Nonexistence","Proof of Peace","PromiseCharm"]
            IC_Types["form"] = ["Valor Form","Wisdom Form","Final Form","Master Form","Limit Form","Anti-Form"]
            IC_Types["other"] = ["Hades Cup Trophy","Unknown Disk","Olympus Stone"]
            IC_Types["report"] = ["Secret Ansem's Report 1","Secret Ansem's Report 2","Secret Ansem's Report 3","Secret Ansem's Report 4","Secret Ansem's Report 5","Secret Ansem's Report 6","Secret Ansem's Report 7","Secret Ansem's Report 8","Secret Ansem's Report 9","Secret Ansem's Report 10","Secret Ansem's Report 11","Secret Ansem's Report 12","Secret Ansem's Report 13"]
            IC_Types["visit"] = ["Battlefields of War (Auron)","Sword of the Ancestor (Mulan)","Beast's Claw (Beast)","Bone Fist (Jack Skellington)","Proud Fang (Simba)","Skill and Crossbones (Jack Sparrow)","Scimitar (Aladdin)","Identity Disk (Tron)","Membership Card","Ice Cream","Picture"]
            worldItemTypes = {}
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON, itemType.REPORT, "Second Chance", "Once More"] + [itemType.STORYUNLOCK] #+ [itemType.TROPHY, itemType.MEMBERSHIPCARD, "Olympus Stone"]
            hintableWorlds = [locationType.Level,locationType.LoD,locationType.BC,locationType.HB,locationType.TT,locationType.TWTNW,locationType.SP,locationType.Atlantica,locationType.PR,locationType.OC,locationType.Agrabah,locationType.HT,locationType.PL,locationType.DC,locationType.HUNDREDAW,locationType.STT,locationType.FormLevel,"Creations"]

            for location,item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    world_of_location = location.LocationTypes[0]
                    if world_of_location == locationType.Puzzle or world_of_location == locationType.SYNTH:
                        world_of_location = "Creations"
                    if not world_of_location in hintsText['world']:
                        hintsText['world'][world_of_location] = []
                    hintsText['world'][world_of_location].append(item.Name)
                    #make a list of worlds and the checks they have depending on reveal list
                    if not world_of_location in worldItemTypes:
                        worldItemTypes[world_of_location] = []
                    if item.Name in IC_Types["magic"] and "magic" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)
                    elif item.Name in IC_Types["page"] and "page" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)
                    elif item.Name in IC_Types["summon"] and "summon" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)
                    elif item.Name in IC_Types["ability"] and "ability" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)
                    elif item.Name in IC_Types["proof"] and "proof" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)
                    elif item.Name in IC_Types["form"] and "form" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)
                    elif item.Name in IC_Types["other"] and "other" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)
                    elif item.Name in IC_Types["report"] and "report" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)
                    elif item.Name in IC_Types["visit"] and "visit" in spoilerHintValues:
                        worldItemTypes[world_of_location].append(item)

            worldChecks = {}
            worldChecksEdit = {}
            for h in hintableWorlds:
                if h not in excludeList:
                    worldChecks[h] = []
                    worldChecksEdit[h] = []
                    
            for location,item in locationItems:
                world_of_location = location.LocationTypes[0]
                if world_of_location == locationType.Puzzle or world_of_location == locationType.SYNTH:
                    world_of_location = "Creations"
                if world_of_location == locationType.WeaponSlot or world_of_location == locationType.Free or world_of_location == locationType.Critical:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    worldChecks[world_of_location].append(item)
                    worldChecksEdit[world_of_location].append(item)
                if item.ItemType is itemType.REPORT and preventSelfHinting:
                    #report can't hint itself
                    reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                    reportRestrictions[reportNumber-1].append(world_of_location)

            attempts = 0
            while len(reportsList) > 0:
                attempts+=1
                if attempts > 500:
                    raise HintException(f"spoiler hints got stuck assigning report text with {len(reportsList)}")

                temp_worlds = list(worldChecksEdit.keys())
                worlds = []

                for place in temp_worlds:
                    if place not in tempExcludeList:
                        worlds.append(place)

                random.shuffle(reportsList)
                random.shuffle(worlds)
                randomWorld = None

                #bandaid kinda fix with this part i guess. for some reson Creation is always enabled even if puzzle and synthesis toggles are off.
                if "Puzzle" not in tracker_includes and "Synthesis" not in tracker_includes and not "Creations" in tempExcludeList:
                    #print("Puzzle or Synth isn't enabled! removing Creations world from list...")
                    #print("-----------------------------------------------------------------------------")
                    tempExcludeList.append("Creations")

                if len(worlds) == 0:
                    #print("ran out of worlds! Setting report text as Empty...")
                    #print("-----------------------------------------------------------------------------")
                    randomWorld = "Empty"
                    reportNumber = reportsList.pop(0)
                else:
                    if (len(worldChecksEdit[worlds[0]]) != 0):
                        if worlds[0] not in reportRestrictions[reportsList[0]-1]:
                            #check if world contains at least 1 of an item type in reveal list. avoid setting reports if it can't reveal anything
                            if any(x in worldItemTypes[worlds[0]] for x in worldChecks[worlds[0]]):
                                reportNumber = reportsList.pop(0)
                                randomWorld = worlds[0]
                            else:
                                #print(worlds[0] + " has nothing we can reveal! removing form list and rerolling")
                                #print("-----------------------------------------------------------------------------")
                                tempExcludeList.append(worlds[0])
                                continue
                        else:
                            #print("Self hinting world! Rerolling...")
                            #print("-----------------------------------------------------------------------------")
                            continue
                    elif "complete" not in spoilerHintValues: 
                        #don't skip worlds with 0 checks, we want to know if a world is empty if world color change is disabled
                        #print(worlds[0] + " has 0 checks! setting report text as Nothing")
                        #print("-----------------------------------------------------------------------------")
                        reportNumber = reportsList.pop(0)
                        randomWorld = "Nothing_" + worlds[0]
                        #print("Removing " + worlds[0] + " from hintable worlds")
                        #print("-----------------------------------------------------------------------------")
                        tempExcludeList.append(worlds[0])
                    else:
                        #print(worlds[0] + " has 0 checks and World Color Change is on! removing form list and rerolling...")
                        #print("-----------------------------------------------------------------------------")
                        tempExcludeList.append(worlds[0])
                        continue

                hintsText["Reports"][reportNumber] = {"World": randomWorld, "Location": ""}
                
                #remove world from list
                if randomWorld != "Empty" and randomWorld.startswith('Nothing_') == False:
                    #print("Removing " + randomWorld + " from hintable worlds")
                    #print("-----------------------------------------------------------------------------")
                    tempExcludeList.append(randomWorld)
                
            for reportNumber in range(1,14):
                if hintsText["Reports"][reportNumber]["Location"] != "":
                    continue
                for world in worldChecks:
                    if any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                        hintsText["Reports"][reportNumber]["Location"] = world
 
        if hintsType in ["Points","JSmartee","Spoiler"] and found_reports:
            for reportNumber in range(1,14):
                if hintsText["Reports"][reportNumber]["Location"] not in report_master[reportNumber]:
                    if hintsText["Reports"][reportNumber]["Location"]=="" and (locationType.Critical in report_master[reportNumber] or locationType.Free in report_master[reportNumber]):
                        #this is fine, continue
                        continue
                    raise RuntimeError(f"Report {reportNumber} has location written as {hintsText['Reports'][reportNumber]['Location']} but the actual location is {report_master[reportNumber]}")

        return hintsText

    def writeHints(hintsText,seedName,outZip):
        #outZip.writestr("{seedName}_DebugHints.json".format(seedName = seedName), json.dumps(hintsText).encode('utf-8'))
        outZip.writestr("{seedName}.Hints".format(seedName = seedName), base64.b64encode(json.dumps(hintsText).encode('utf-8')).decode('utf-8'))

    def getOptions():
        return ["Disabled","Shananas","JSmartee","JSmartee-FirstVisit","JSmartee-SecondVisit","JSmartee-FirstBoss","JSmartee-SecondBoss","Points","Points-FirstVisit","Points-SecondVisit","Points-FirstBoss","Points-SecondBoss"]
