from Class.exceptions import HintException
from List.configDict import itemType, locationType
import base64, json, random
from itertools import permutations


class Hints:
    def convertItemAssignmentToTuple(itemAssignment):
        locationItems = []
        for assignment in itemAssignment:
            locationItems.append((assignment.location,assignment.item))
            if assignment.item2 is not None:
                locationItems.append((assignment.location,assignment.item2))
        return locationItems



    def generateHints(locationItems, hintsType, excludeList, preventSelfHinting, allowProofHinting, pointHintValues):
        locationItems = Hints.convertItemAssignmentToTuple(locationItems)
        if hintsType=="Disabled":
            return None
        hintsText = {}
        hintsText['hintsType'] = hintsType
        if hintsType == "Shananas":
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON]
            hintsText['world'] = {}
            for location,item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name == "Second Chance" or item.Name == "Once More":
                    if location.LocationTypes[0] != locationType.Puzzle:
                        if not location.LocationTypes[0] in hintsText['world']:
                            hintsText['world'][location.LocationTypes[0]] = []
                        hintsText['world'][location.LocationTypes[0]].append(item.Name)

        report_master = [None]*14
        for location,item in locationItems:
            if item.ItemType is itemType.REPORT:
                reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                report_master[reportNumber] = location.LocationTypes

        if hintsType == "JSmartee":
            proof_of_connection_index = None
            proof_of_peace_index = None
            proof_of_nonexistence_index = None
            worldsToHint = []
            reportRestrictions = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
            reportsList = list(range(1,14))
            hintsText['Reports'] = {}
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON, itemType.REPORT, "Second Chance", "Once More"]
            
            hintableWorlds = [locationType.Level,locationType.LoD,locationType.BC,locationType.HB,locationType.TT,locationType.TWTNW,locationType.SP,locationType.Atlantica,locationType.PR,locationType.OC,locationType.Agrabah,locationType.HT,locationType.PL,locationType.DC,locationType.HUNDREDAW,locationType.STT,locationType.FormLevel]

            freeReports = []

            worldChecks = {}
            for h in hintableWorlds:
                if h not in excludeList:
                    worldChecks[h] = []
                    
            for location,item in locationItems:
                if location.LocationTypes[0] in [locationType.WeaponSlot, locationType.Free, locationType.Critical, locationType.Puzzle]:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    worldChecks[location.LocationTypes[0]].append(item)
                    if item.ItemType in [itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE]:
                        if not location.LocationTypes[0] in worldsToHint:
                            if item.ItemType is itemType.PROOF_OF_CONNECTION:
                                proof_of_connection_index = len(worldsToHint)
                            if item.ItemType is itemType.PROOF_OF_PEACE:
                                proof_of_peace_index = len(worldsToHint)
                            if item.ItemType is itemType.PROOF:
                                proof_of_nonexistence_index = len(worldsToHint)
                            worldsToHint.append(location.LocationTypes[0])
                        else:
                            if item.ItemType is itemType.PROOF_OF_CONNECTION:
                                proof_of_connection_index = worldsToHint.index(location.LocationTypes[0])
                            if item.ItemType is itemType.PROOF_OF_PEACE:
                                proof_of_peace_index = worldsToHint.index(location.LocationTypes[0])
                            if item.ItemType is itemType.PROOF:
                                proof_of_nonexistence_index = worldsToHint.index(location.LocationTypes[0])
            for location,item in locationItems:
                if location.LocationTypes[0] in [locationType.Free, locationType.Critical, locationType.Puzzle]:
                    if item.ItemType is itemType.REPORT:
                        reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                        freeReports.append(reportNumber)
                    continue
                if item.ItemType is itemType.REPORT:
                    reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                    #report can't hint itself
                    if preventSelfHinting:
                        reportRestrictions[reportNumber-1].append(location.LocationTypes[0])
                    if locationType.LW in location.LocationTypes:
                        # if report on LW, can't hint world that contains proof of connection
                        if proof_of_connection_index is not None:
                            reportRestrictions[reportNumber-1].append(worldsToHint[proof_of_connection_index])
                    if locationType.Mush13 in location.LocationTypes:
                        # if report on Mushroom, can't hint world that contains proof of peace
                        if proof_of_peace_index is not None:
                            reportRestrictions[reportNumber-1].append(worldsToHint[proof_of_peace_index])

            if len(worldChecks.keys()) < 13:
                raise HintException("Too few worlds. Add more worlds or change hint system.")

            numProofWorlds = len(worldsToHint)

            forms_need_hints = (locationType.FormLevel in worldsToHint)
            pages_need_hints = (locationType.HUNDREDAW in worldsToHint)
            mag_thun_need_hints = (locationType.Atlantica in worldsToHint)

            # following the priority of Proofs > Forms > Pages > Thunders > Magnets > Proof Reports
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
            importantChecks = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.REFLECT, itemType.MAGNET, itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROMISE_CHARM, itemType.FORM, itemType.TORN_PAGE, itemType.SUMMON, itemType.REPORT, "Second Chance", "Once More"]
            hintableWorlds = [locationType.Level,locationType.LoD,locationType.BC,locationType.HB,locationType.TT,locationType.TWTNW,locationType.SP,locationType.Atlantica,locationType.PR,locationType.OC,locationType.Agrabah,locationType.HT,locationType.PL,locationType.DC,locationType.HUNDREDAW,locationType.STT,locationType.FormLevel]
            
            worldChecks = {}
            worldChecksEdit = {}

            for location,item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    if location.LocationTypes[0] != locationType.Puzzle:
                        if not location.LocationTypes[0] in hintsText['world']:
                            hintsText['world'][location.LocationTypes[0]] = []
                        hintsText['world'][location.LocationTypes[0]].append(item.Name)

            for h in hintableWorlds:
                if h not in excludeList:
                    worldChecks[h] = []
                    worldChecksEdit[h] = []
                    
            for location,item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot or location.LocationTypes[0] == locationType.Free or location.LocationTypes[0] == locationType.Critical or location.LocationTypes[0] == locationType.Puzzle:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    worldChecks[location.LocationTypes[0]].append(item)
                    worldChecksEdit[location.LocationTypes[0]].append(item)

                if item.ItemType is itemType.REPORT:
                    reportNumber = int(item.Name.replace("Secret Ansem's Report ",""))
                    #report can't hint itself
                    if preventSelfHinting:
                        reportRestrictions[reportNumber-1].append(location.LocationTypes[0])
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
                    #print("ran out of worlds! resetting worldlist...")
                    #print("-----------------------------------------------------------------------------")
                    worldChecksEdit = worldChecks
                    tempExcludeList.clear()
                    continue

                if (len(worldChecksEdit[worlds[0]]) != 0):
                    if worlds[0] not in reportRestrictions[reportsList[0]-1]:
                        reportNumber = reportsList.pop(0)
                        randomWorld = worlds[0]
                    else:
                        #print("Self hinting world! Rerolling...")
                        #print("-----------------------------------------------------------------------------")
                        continue
                else:
                    #print(worlds[0] + " has 0 checks! removing from list and rerolling...")
                    #print("-----------------------------------------------------------------------------")
                    tempExcludeList.append(worlds[0])
                    continue
                    
                randomItem = random.choice(worldChecksEdit[randomWorld])
                #print("Report " + str(reportNumber) + ": World = " + randomWorld +" | item = " + randomItem.Name)

                #compare current selected world and item to previously rerolled reports
                #more of a jank failsafe really
                if randomWorld == tempWorldR and randomItem.Name == tempItemR:
                    reportRepetition = reportRepetition + 1

                #should we hint proofs?
                if "Proof" in randomItem.Name:
                    #print("Proof found! Is Proof Hinting On?")
                    
                    if allowProofHinting == True:
                        #print("Yes! hinting Proof...")
                        pass
                    else:
                        #print("No. removing item and rerolling...")
                        #print("-----------------------------------------------------------------------------")
                        worldChecksEdit[randomWorld].remove(randomItem)
                        reportsList.append(reportNumber)
                        continue
                    
                #try to hint other reports
                if "Report" in randomItem.Name:
                    #prevent reports from hinting themselves
                    if reportNumber == int(randomItem.Name.replace("Secret Ansem's Report ","")):
                        #print("Self hinting report! rerolling...")
                        #print("-----------------------------------------------------------------------------")
                        tempWorldR = randomWorld
                        tempItemR = randomItem.Name
                        reportsList.append(reportNumber)
                        continue
                
                    #if we tried to roll for this 3 times already then stop trying and remove the report from being hinted
                    if reportRepetition > 2:
                        #print("Report repetition threshold reached! removing item from world and rerolling...")
                        #print("-----------------------------------------------------------------------------")
                        worldChecksEdit[randomWorld].remove(randomItem)
                        tempWorldR = None
                        tempItemR = None
                        reportRepetition = 0
                        reportsList.append(reportNumber)
                        continue
                        
                    random_number = random.randint(1, 3)
                    #print("Random number = " + str(random_number))
                    #print("Report found! does " + str(random_number) + " = 1?")
                    
                    if random_number == 1:
                        #print("Yes! hinting report...")
                        pass
                    else:
                        #print("No. rerolling...")
                        #print("-----------------------------------------------------------------------------")
                        tempWorldR = randomWorld
                        tempItemR = randomItem.Name
                        reportsList.append(reportNumber)
                        continue

                hintsText["Reports"][reportNumber] = {
                    "World": randomWorld,
                    "check": randomItem.Name,
                    "Location": ""
                }
                
                # remove hinted item from list
                #print("Removing " + randomItem.Name + " from hintable items")
                #print("Removing " + randomWorld + " hintable worlds")
                #print("-----------------------------------------------------------------------------")
                worldChecksEdit[randomWorld].remove(randomItem)
                tempExcludeList.append(randomWorld)
                
            for reportNumber in range(1,14):
                if hintsText["Reports"][reportNumber]["Location"] != "":
                    continue
                for world in worldChecks:
                    if any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                        hintsText["Reports"][reportNumber]["Location"] = world
        
        if hintsType in ["Points","JSmartee"]:
            for reportNumber in range(1,14):
                if hintsText["Reports"][reportNumber]["Location"] not in report_master[reportNumber]:
                    if hintsText["Reports"][reportNumber]["Location"]=="" and (locationType.Critical in report_master[reportNumber] or locationType.Free in report_master[reportNumber]):
                        #this is fine, continue
                        continue
                    raise RuntimeError(f"Report {reportNumber} has location written as {hintsText['Reports'][reportNumber]['Location']} but the actual location is {report_master[reportNumber]}")

        return hintsText

    def writeHints(hintsText,seedName,outZip):
        # outZip.writestr("{seedName}.Hints".format(seedName = seedName), json.dumps(hintsText).encode('utf-8'))
        outZip.writestr("{seedName}.Hints".format(seedName = seedName), base64.b64encode(json.dumps(hintsText).encode('utf-8')).decode('utf-8'))

    def getOptions():
        return ["Disabled","Shananas","JSmartee","JSmartee-FirstVisit","JSmartee-SecondVisit","JSmartee-FirstBoss","JSmartee-SecondBoss","Points","Points-FirstVisit","Points-SecondVisit","Points-FirstBoss","Points-SecondBoss"]