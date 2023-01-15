import copy
from dataclasses import dataclass
import itertools

from Class.exceptions import GeneratorException,CantAssignItemException, SettingsException
from Module.modifier import SeedModifier
from Class.newLocationClass import KH2Location
from Class.itemClass import KH2Item, itemRarity
from List.configDict import locationCategory, itemType, locationDepth, locationType
from List.ItemList import Items
from List.NewLocationList import Locations
from Module.RandomizerSettings import RandomizerSettings

import random

from Module.weighting import LocationWeights
from Module.depths import ItemDepths

@dataclass
class ItemAssignment():
    location: KH2Location
    item: KH2Item = None
    item2: KH2Item = None

    def getItems(self):
        if self.item is None:
            return []
        elif self.item2 is None:
            return [self.item]
        return [self.item,self.item2]
    
    def __eq__(self, obj:"ItemAssignment"):
        return self.location==obj.location

    def __eq__(self, obj: KH2Location):
        if not isinstance(obj,KH2Location):
            return NotImplemented
        return self.location==obj

@dataclass
class WeaponStats():
    location: KH2Location
    strength: int
    magic: int
    
    def __eq__(self, obj):
        return self.location==obj.location

    def __eq__(self, obj: KH2Location):
        return self.location==obj

@dataclass
class LevelStats():
    location: KH2Location
    experience: int
    strength: int
    magic: int
    defense: int
    ap: int

    def __eq__(self, obj):
        return self.location==obj.location

    def __eq__(self, obj: KH2Location):
        return self.location==obj

@dataclass
class FormExp():
    location: KH2Location
    experience: int

    def __eq__(self, obj):
        return self.location==obj.location

    def __eq__(self, obj: KH2Location):
        return self.location==obj

@dataclass
class SynthRequirement():
    item_id: int
    amount: int

@dataclass
class SynthesisRecipe():
    location: KH2Location
    requirements = list[SynthRequirement]
    unlock_rank: int

    def __eq__(self, obj):
        return self.location==obj.location

    def __eq__(self, obj: KH2Location):
        return self.location==obj

class Randomizer():
    def __init__(self, settings: RandomizerSettings, progress_bar_vis = False):
        if settings is None:
            raise SettingsException("Invalid settings passed to randomize. Change settings and try again")
        random.seed(settings.full_rando_seed)
        self.progress_bar_vis = progress_bar_vis
        self.regular_locations = Locations(settings,False)
        self.reverse_locations = Locations(settings,True)
        self.master_locations = self.regular_locations if settings.regular_rando else self.reverse_locations
        self.location_weights = LocationWeights(settings,self.regular_locations,self.reverse_locations)
        self.report_depths = ItemDepths(settings.reportDepth,self.master_locations)
        self.proof_depths = ItemDepths(settings.proofDepth,self.master_locations)
        self.story_depths = ItemDepths(settings.storyDepth,self.master_locations)
        self.yeet_the_bear = settings.yeetTheBear
        self.num_valid_locations = None
        self.num_available_items = None
        self.assignedItems = []
        self.assignedDonaldItems = []
        self.assignedGoofyItems = []
        self.weaponStats = []
        self.levelStats = []
        self.formLevelExp = []
        self.synthesis_recipes = []
        self.shop_items = []
        self.assignSoraItems(settings)
        if progress_bar_vis:
            return
        self.assignPartyItems()
        self.assignWeaponStats(settings)
        self.assignLevelStats(settings)
        self.assignFormLevelExp(settings)
    
    def assignFormLevelExp(self,settings):
        for category,exp in zip([locationCategory.SUMMONLEVEL,
                                locationCategory.VALORLEVEL,
                                locationCategory.WISDOMLEVEL,
                                locationCategory.LIMITLEVEL,
                                locationCategory.MASTERLEVEL,
                                locationCategory.FINALLEVEL],
                                [settings.summon_exp,
                                settings.valor_exp,
                                settings.wisdom_exp,
                                settings.limit_exp,
                                settings.master_exp,
                                settings.final_exp]):
            locations = [loc for loc in self.master_locations.getAllSoraLocations() if loc.LocationCategory is category]
            for index,l in enumerate(locations):
                self.formLevelExp.append(FormExp(l,exp[index]))


    def assignLevelStats(self,settings):
        levelLocations = [loc for loc in self.master_locations.getAllSoraLocations() if loc.LocationCategory is locationCategory.LEVEL]
        levelLocations.sort(key=lambda x: x.LocationId)
        levelStats = settings.level_stat_pool()
        strength = 2
        magic = 6
        defense = 2
        ap = 0
        exp = 0

        def addStat(choice):
            nonlocal strength
            nonlocal magic
            nonlocal defense
            nonlocal ap
            if choice["Stat"]=="Str":
                strength+=choice["Value"]
            elif choice["Stat"]=="Mag":
                magic+=choice["Value"]
            elif choice["Stat"]=="Def":
                defense+=choice["Value"]
            elif choice["Stat"]=="Ap":
                ap+=choice["Value"]
            else:
                raise GeneratorException("We had a problem assigning stats to levels")

        def addLevel1Stat(dummy):
            return

        adder_function = addLevel1Stat if settings.level_one else addStat

        for index,l in enumerate(levelLocations):
            if index!=0:
                stat_choices = random.sample(levelStats,k=2)
                adder_function(stat_choices[0])
                if l.LocationId in settings.excludedLevels:
                    adder_function(stat_choices[1])
            exp+=(settings.sora_exp[index+1]-settings.sora_exp[index])
            self.levelStats.append(LevelStats(l,exp,strength,magic,defense,ap))

    def assignWeaponStats(self,settings):
        soraMin = settings.keyblade_min_stat
        soraMax = settings.keyblade_max_stat
        keybladeLocations =  Locations.WeaponList()

        for key in keybladeLocations:
            if key.LocationId=="85" and not settings.pureblood:
                continue
            self.weaponStats.append(WeaponStats(key,random.randint(soraMin,soraMax),random.randint(soraMin,soraMax)))
            
        struggleWeapons = self.master_locations.getStruggleWeapons()
        for key in struggleWeapons:
            self.weaponStats.append(WeaponStats(key,(soraMin+soraMax)//2,(soraMin+soraMax)//2))

        donaldStaves = [l for l in self.master_locations.getAllDonaldLocations() if l.LocationCategory is locationCategory.WEAPONSLOT]
        for staff in donaldStaves:
            self.weaponStats.append(WeaponStats(staff,random.randint(1,13),random.randint(1,13)))

        goofyShields = [l for l in self.master_locations.getAllGoofyLocations() if l.LocationCategory is locationCategory.WEAPONSLOT]
        for shield in goofyShields:
            self.weaponStats.append(WeaponStats(shield,random.randint(1,13),0))


    def assignPartyItems(self):
        donaldItems = Items.getDonaldAbilityList()
        donaldLocations = self.master_locations.getAllDonaldLocations()

        for item in donaldItems:
            randomLocation = random.choice(donaldLocations)
            if self.assignItem(randomLocation,item,"Donald"):
                donaldLocations.remove(randomLocation)

        goofyItems = Items.getGoofyAbilityList()
        goofyLocations = self.master_locations.getAllGoofyLocations()
        for item in goofyItems:
            randomLocation = random.choice(goofyLocations)
            if self.assignItem(randomLocation,item,"Goofy"):
                goofyLocations.remove(randomLocation)

    def assignSoraItems(self, settings: RandomizerSettings):
        if settings.num_random_growths > 0:
            for i in settings.chosen_random_growths:
                settings.startingItems.remove(i)
            settings.chosen_random_growths = SeedModifier.random_schmovement(settings.num_random_growths)
            settings.startingItems+=settings.chosen_random_growths

        allItems = [i for i in Items.getItemList(settings.story_unlock_rarity) if i.Id not in settings.startingItems]
        if not settings.pureblood:
            allItems = [i for i in allItems if i.Id!=71]
        if not settings.antiform:
            allItems = [i for i in allItems if i.Id!=30]

        # pick N of the reports and key items
        if settings.shop_reports > 0:
            all_reports_available = [i for i in allItems if i.ItemType==itemType.REPORT]
            random.shuffle(all_reports_available)
            num_reports_in_shop = min(settings.shop_reports,len(all_reports_available))
            self.shop_items += all_reports_available[0:num_reports_in_shop]

            # self.shop_items+=[i for i in allItems if i.ItemType==itemType.REPORT]
        if settings.shop_unlocks > 0:
            all_unlocks_available = [i for i in allItems if i.ItemType==itemType.STORYUNLOCK]
            random.shuffle(all_unlocks_available)
            num_unlocks_in_shop = min(settings.shop_unlocks,len(all_unlocks_available))
            self.shop_items += all_unlocks_available[0:num_unlocks_in_shop]
        
        allItems = [i for i in allItems if i not in self.shop_items]
            
        if settings.shop_keyblades:
            self.shop_items+=[i for i in allItems if i.ItemType==itemType.KEYBLADE]
        if settings.shop_elixirs:
            self.shop_items+=[KH2Item(4, "Elixir", itemType.ITEM),
                                KH2Item(7, "Megalixir", itemType.ITEM)]
        if settings.shop_recoveries:
            self.shop_items+=[KH2Item(274, "Drive Recovery", itemType.ITEM),
                                KH2Item(275, "High Drive Recovery", itemType.ITEM)]
        if settings.shop_boosts:
            self.shop_items+=[KH2Item(276, "Power Boost", itemType.ITEM),
                                KH2Item(277, "Magic Boost", itemType.ITEM),
                                KH2Item(278, "Defense Boost", itemType.ITEM),
                                KH2Item(279, "AP Boost", itemType.ITEM)]
  
        if settings.fifty_ap:
            allItems += list(itertools.repeat(KH2Item(279, "AP Boost", itemType.ITEM),50))

        if not settings.include_maps:
            allItems = [i for i in allItems if i.ItemType != itemType.MAP]
        if not settings.include_recipes:
            allItems = [i for i in allItems if i.ItemType != itemType.RECIPE]
        if not settings.include_accessories:
            allItems = [i for i in allItems if i.ItemType != itemType.ACCESSORY]
        if not settings.include_armor:
            allItems = [i for i in allItems if i.ItemType != itemType.ARMOR]

        allAbilities =  settings.abilityListModifier(Items.getActionAbilityList(), Items.getSupportAbilityList() + (Items.getLevelAbilityList() if not settings.level_one else []) )
        # if there abilities in the starting inventory, remove them from the pool
        removeAbilities = []
        for startItem in settings.startingItems:
            for i in allAbilities:
                if i.Id == startItem:
                    removeAbilities.append(i)
                    break
        for i in removeAbilities:
            allAbilities.remove(i)

        if settings.promiseCharm and Items.getPromiseCharm().Id not in settings.startingItems:
            allItems+=[Items.getPromiseCharm()]
        allLocations = self.master_locations.getAllSoraLocations()

        self.augmentInvalidChecks(allLocations)

        if settings.statSanity:
            allItems+=Items.getStatItems()
        else:
            self.assignStatBonuses(allLocations)

        def invalid_checker(loc):
            result = any(item in loc.LocationTypes for item in settings.disabledLocations)
            check_list = [locationType.OCCups,locationType.OCParadoxCup,locationType.CoR,locationType.TTR]
            if any(item in check_list for item in loc.LocationTypes):
                result = not any(item in settings.enabledLocations and item in check_list for item in loc.LocationTypes)
            return result
        
        def remove_popupchecker(loc):
            if not settings.remove_popups:
                return False
            result = False
            if loc.LocationCategory in [locationCategory.POPUP, locationCategory.DOUBLEBONUS, locationCategory.HYBRIDBONUS, locationCategory.ITEMBONUS, locationCategory.STATBONUS] and not any(item in loc.LocationTypes for item in [locationType.AS,locationType.DataOrg,locationType.LW,locationType.Sephi]):
                result = True
            return result

        def no_final_form(loc):
            if not settings.disable_final_form:
                return False
            return loc.LocationCategory is locationCategory.FINALLEVEL

        invalidLocations = [loc for loc in allLocations if ( no_final_form(loc) or invalid_checker(loc) or remove_popupchecker(loc) or (loc.LocationCategory is locationCategory.LEVEL and loc.LocationId in settings.excludedLevels))]
        validLocations =  [loc for loc in allLocations if loc not in invalidLocations]
        locations_with_vanilla_items = [l for l in invalidLocations if len(l.VanillaItems)>0 and any(item in l.LocationTypes for item in settings.vanillaLocations)]
        vanilla_items = []
        for l in locations_with_vanilla_items:
            vanilla_items+=l.VanillaItems

        if len(vanilla_items) > 0 and settings.chainLogic:
            raise GeneratorException("Can't use vanilla worlds with chain logic for now. Sorry")

        self.num_valid_locations = len(validLocations) + (len([loc for loc in validLocations if loc.LocationCategory in [locationCategory.DOUBLEBONUS,locationCategory.HYBRIDBONUS]]) if settings.statSanity else 0 )+ (len([loc for loc in validLocations if loc.LocationCategory in [locationCategory.DOUBLEBONUS]]) if settings.statSanity else 0)
        self.num_available_items = len(allAbilities)+len(allItems) - (sum([len(l.VanillaItems) for l in locations_with_vanilla_items]))

        if self.progress_bar_vis:
            return

        if len(allLocations)!=(len(invalidLocations)+len(validLocations)):
            raise GeneratorException(f"Separating valid {len(validLocations)} and invalid {len(invalidLocations)} locations removed locations from existence (total {len(allLocations)} )")
        

        def split_vanilla_abilities():
            vanilla_item_copy = copy.deepcopy(vanilla_items)
            vanilla_abilities = []
            nonvanilla_abilities = []
            for a in allAbilities:
                if a.Id in vanilla_item_copy:
                    vanilla_item_copy.remove(a.Id)
                    vanilla_abilities.append(a)
                else:
                    nonvanilla_abilities.append(a)
            return vanilla_abilities,nonvanilla_abilities

        van,nonvan = split_vanilla_abilities()

        self.assignKeybladeAbilities(settings, nonvan, allItems)
        allItems=van+nonvan+allItems

        # vanilla location item assignment
        for l in locations_with_vanilla_items:
            #find item in item list
            for i in l.VanillaItems:
                i_data_list = [it for it in allItems if it.Id==i]
                if len(i_data_list)==0:
                    # if we don't have the item, it means that we started with the item, or it was randomized away
                    continue
                i_data = i_data_list[0]
                if i_data.ItemType not in l.InvalidChecks:
                    allItems.remove(i_data)
                    if self.assignItem(l,i_data):
                        invalidLocations.remove(l)

        restricted_reports = self.report_depths.very_restricted_locations
        restricted_proofs = self.proof_depths.very_restricted_locations
        restricted_story = self.story_depths.very_restricted_locations

        # leaving this code here for future bug testing. Puts a specific item in a specific location
        # placed_item = False
        # for item in allItems:
        #     if not placed_item and item.Id == 23:
        #         location_to_place = [loc for loc in validLocations if loc.LocationCategory is locationCategory.CHEST and loc.LocationId==463][0]
        #         if self.assignItem(location_to_place,item):
        #             validLocations.remove(location_to_place)
        #         allItems.remove(item)
        #         placed_item = True
        #         break


        invalid_test = []

        if restricted_reports:
            invalid_test.append(itemType.REPORT)
        if restricted_proofs:
            invalid_test+=[itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE]
        if restricted_story:
            invalid_test.append(itemType.STORYUNLOCK)

        # def item_sorter(item1):
        #     rank_map = {}
        #     rank_map[itemRarity.COMMON] = 1
        #     rank_map[itemRarity.UNCOMMON] = 2
        #     rank_map[itemRarity.RARE] = 3
        #     rank_map[itemRarity.MYTHIC] = 4

        #     if item1.ItemType in invalid_test:
        #         return 5

        #     return rank_map[item1.Rarity]

        # random.shuffle(allItems)
        # if len(invalid_test)>0:
        #     allItems.sort(reverse=True,key=item_sorter)



        def local_item_weights_computation(item,location_pool):
            if restricted_proofs or restricted_reports or restricted_story:
                weights = [self.location_weights.getWeight(item,loc) if (any(i_type in loc.InvalidChecks for i_type in invalid_test)) else 0 for loc in location_pool]
            else:
                weights = [self.location_weights.getWeight(item,loc) for loc in location_pool]

            if restricted_reports and item.ItemType is itemType.REPORT:
                weights = [1 if itemType.REPORT not in loc.InvalidChecks else 0 for loc in location_pool ]
            if restricted_proofs and item.ItemType in [itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE]:
                weights = [1 if not (any(i_type in loc.InvalidChecks for i_type in [itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE])) else 0 for loc in location_pool ]
            if restricted_story and item.ItemType is itemType.STORYUNLOCK:
                weights = [1 if itemType.STORYUNLOCK not in loc.InvalidChecks else 0 for loc in location_pool ]
            return weights



        # chain logic placement
        if settings.chainLogic:
            from Module.seedEvaluation import LocationInformedSeedValidator
            validator = LocationInformedSeedValidator()

            unlocks = {}
            if settings.regular_rando:
                unlocks[locationType.HB] = [[595],[369]]
            elif settings.reverse_rando:
                unlocks[locationType.HB] = [[369]]
            unlocks[locationType.OC] = [[54]]
            unlocks[locationType.LoD] = [[55]]
            unlocks[locationType.PL] = [[61]]
            unlocks[locationType.HT] = [[60]]
            unlocks[locationType.SP] = [[74]]
            unlocks[locationType.FormLevel] = [[26],[27],[29],[31],[563]]
            unlocks[locationType.TT] = [[375],[376]]
            unlocks[locationType.BC] = [[59]]
            if settings.regular_rando:
                unlocks[locationType.Agrabah] = [[72,21,22,23]]
            elif settings.reverse_rando:
                unlocks[locationType.Agrabah] = [[72],[21,22,23]]
            unlocks[locationType.HUNDREDAW] = [[32],[32],[32],[32],[32]]
            unlocks[locationType.LW] = [[593]]
            unlocks[locationType.PR] = [[62]]
            unlocks[locationType.Atlantica] = [[23,23,23],[87,87]]

            second_visit_locking_items = [369,54,55,61,60,74,376,59,72,62]

            locking_items = []
            for loc_type in settings.enabledLocations:
                if loc_type in unlocks:
                    locking_items+=unlocks[loc_type]

            
            for i in settings.startingItems:
                if [i] in locking_items:
                    locking_items.remove([i])
                if [i,21,22,23] in locking_items:
                    locking_items.remove([i,21,22,23])
            for i in vanilla_items: # TODO add vanilla worlds to chain
                if [i] in locking_items:
                    locking_items.remove([i])

            if not settings.chainLogicIncludeTerra:
                if [593] in locking_items:
                    locking_items.remove([593])

            minimum_terra_depth = len(locking_items)-5 if settings.chainLogicTerraLate else 0

            if self.yeet_the_bear:
                locking_items.remove([32])

            if settings.nightmare:
                locking_items.remove([29])
            
            terra = settings.chainLogicIncludeTerra and [593] in locking_items
            tt_condition = [376] in locking_items and [375] in locking_items
            pop_condition = [595] in locking_items
            hb_condition = [369] in locking_items and pop_condition
            ag_condition = [72] in locking_items
            atlantica_condition = [87,87] in locking_items
            second_visit_condition = settings.proofDepth in [locationDepth.DataFight,locationDepth.SecondVisitOnly,locationDepth.SecondBoss]
            data_condition = settings.proofDepth is locationDepth.DataFight
            story_data_condition = settings.storyDepth is locationDepth.DataFight

            if second_visit_condition:
                # check if enough unlock items are available for the chain
                num_proofs_in_chain = int(pop_condition)+int(terra)+int(not self.yeet_the_bear)
                
                counter = 0
                for world_unlocks in locking_items:
                    for i in world_unlocks:
                        if i in second_visit_locking_items:
                            counter+=1
                if counter < num_proofs_in_chain:
                    raise SettingsException("Not enough locked second visits for chain logic.") 

            while True:
                random.shuffle(locking_items)
                if ag_condition and locking_items.index([21,22,23]) > locking_items.index([72]): # scimitar has to be after fire/blizz/thunder 
                    continue
                if tt_condition and locking_items.index([376]) > locking_items.index([375]): # ice cream needs to be after picture
                    continue
                if hb_condition and locking_items.index([369]) > locking_items.index([595]): # proof of peace needs to be after membership card
                    continue
                if terra and locking_items.index([593]) < minimum_terra_depth:
                    continue
                if atlantica_condition and locking_items.index([87,87]) > locking_items.index([23,23,23]):
                    continue
                if story_data_condition:
                    form_indices = [locking_items.index(x) for x in unlocks[locationType.FormLevel]]
                    membership_index = locking_items.index([369])
                    
                    # print(f"{369 in locking_items[proof_index-1]} {not all(x<proof_index for x in form_indices)}")
                    if not all(x<membership_index for x in form_indices):
                        continue

                #proof depth checking
                if second_visit_condition:
                    if pop_condition:
                        proof_index = locking_items.index([595])
                        if proof_index==0:
                            continue
                        if not any(it in locking_items[proof_index-1] for it in second_visit_locking_items):
                            continue
                        form_indices = [locking_items.index(x) for x in unlocks[locationType.FormLevel]]
                        # print(f"{369 in locking_items[proof_index-1]} {not all(x<proof_index for x in form_indices)}")
                        if data_condition and 369 in locking_items[proof_index-1] and not all(x<proof_index for x in form_indices):
                            continue
                    if terra:
                        proof_index = locking_items.index([593])
                        if proof_index==0:
                            continue
                        if not any(it in locking_items[proof_index-1] for it in second_visit_locking_items):
                            continue
                        form_indices = [locking_items.index(x) for x in unlocks[locationType.FormLevel]]
                        # print(f"{369 in locking_items[proof_index-1]} {not all(x<proof_index for x in form_indices)}")
                        if data_condition and 369 in locking_items[proof_index-1] and not all(x<proof_index for x in form_indices):
                            continue
                    if not self.yeet_the_bear:
                        if not any(it in locking_items[-1] for it in second_visit_locking_items):
                            continue
                break
            if self.yeet_the_bear:
                locking_items.append([32])

            force_obtained = []
            if len(locking_items) > settings.chainLogicMinLength:
                # keep the last parts of the chain
                num_to_remove = len(locking_items) - settings.chainLogicMinLength;
                force_obtained = locking_items[:num_to_remove]
                locking_items = locking_items[num_to_remove:]

            locking_items.append([594]) # add the proof of nonexistence at the end of the chain

            if settings.nightmare:
                locking_items[-1].append(29)

            print(locking_items)

            validator.prep_req_list(settings,self)

            current_inventory = [] + settings.startingItems
            for i in force_obtained:
                current_inventory+=i
            if settings.reverse_rando:
                current_inventory+=[94,95,96,98,99,100,102,103,104,106,107,108,564,565,566]

            def open_location(inv,loc):
                return validator.is_location_available(inv,loc) and (not settings.nightmare or loc.LocationId !=560)

            accessible_locations = [[l for l in validLocations if open_location(current_inventory,l)]]
            for items in locking_items:
                accessible_locations_start = [l for l in validLocations if open_location(current_inventory,l)]
                accessible_locations_new = [l for l in validLocations if open_location(current_inventory + items,l) and l not in accessible_locations_start]
                accessible_locations.append(accessible_locations_new)
                print(f"{items} unlocked {len(accessible_locations[-1])}")
                current_inventory += items
            for iter,items in enumerate(locking_items):
                accessible_locations_new = accessible_locations[iter]
                if len(accessible_locations_new) == 0:
                    raise GeneratorException("Chain logic created a situation where the chain item couldn't be placed")
                for i in items:
                    #find item in item list
                    if len(accessible_locations_new) == 0:
                        break
                    
                    i_data_list = [it for it in allItems if it.Id==i]
                    if len(i_data_list)==0:
                        continue
                    i_data = i_data_list[0]
                    weights = local_item_weights_computation(i_data,accessible_locations_new)
                    # if len(weights)==0:
                    #     raise GeneratorException(f"Chain Logic failed to place {i_data}")
                    # if sum(weights)==0:
                    #     raise GeneratorException(f"Chain Logic failed to place {i_data}")
                    randomLocation = random.choices(accessible_locations_new,weights)[0]
                    if i_data.ItemType not in randomLocation.InvalidChecks:
                        allItems.remove(i_data)
                        if self.assignItem(randomLocation,i_data):
                            validLocations.remove(randomLocation)
                            accessible_locations_new.remove(randomLocation)

        #assign valid items to all valid locations remaining
        for item in allItems:
            if len(validLocations) == 0:
                raise CantAssignItemException(f"Ran out of locations to assign items")

            if item.ItemType is itemType.PROOF and self.yeet_the_bear:
                # do manual assignment of this item to starry hill
                starry_hill_loc_list = [loc for loc in validLocations if loc.LocationCategory is locationCategory.POPUP and loc.LocationId==285]
                if len(starry_hill_loc_list) == 0:
                    raise GeneratorException("Yeet the Bear setting is set, when 100 acre wood is turned off.")
                starry_hill_cure = starry_hill_loc_list[0]
                if self.assignItem(starry_hill_cure,item):
                    validLocations.remove(starry_hill_cure)
                continue

            weights = local_item_weights_computation(item,validLocations)

            count=0
            while True:
                count+=1
                if len(weights)==0:
                    raise CantAssignItemException(f"Ran out of locations to assign items to.")
                if sum(weights) == 0 and restricted_reports:
                    raise CantAssignItemException(f"Somehow, can't assign an item. If using report depth option that restricts to specific bosses, make sure all worlds with doors in GoA are enabled.")
                randomLocation = random.choices(validLocations,weights)[0]
                if item.ItemType not in randomLocation.InvalidChecks:
                    if self.assignItem(randomLocation,item):
                        validLocations.remove(randomLocation)
                        if randomLocation.LocationCategory is locationCategory.POPUP and randomLocation.LocationId == 389: 
                            # assign same item to 390
                            struggle_reward_loc = [loc for loc in validLocations if loc.LocationCategory is locationCategory.POPUP and loc.LocationId==390]
                            if len(struggle_reward_loc) == 0:
                                raise GeneratorException("Tried assigning struggle reward, but failed")
                            self.assignItem(struggle_reward_loc[0],item)
                            validLocations.remove(struggle_reward_loc[0])
                        if randomLocation.LocationCategory is locationCategory.POPUP and randomLocation.LocationId == 390: 
                            # assign same item to 389
                            struggle_reward_loc = [loc for loc in validLocations if loc.LocationCategory is locationCategory.POPUP and loc.LocationId==389]
                            if len(struggle_reward_loc) == 0:
                                raise GeneratorException("Tried assigning struggle reward, but failed")
                            self.assignItem(struggle_reward_loc[0],item)
                            validLocations.remove(struggle_reward_loc[0])
                    break
                if count==100:
                    raise CantAssignItemException(f"Trying to assign {item} and failed 100 times in {len([i for i in validLocations if i.LocationCategory==locationCategory.POPUP])} popups left out of {len(validLocations)}")
        invalidLocations+=validLocations
        self.assignJunkLocations(settings, invalidLocations)


    def assignJunkLocations(self, settings, invalidLocations):
        """ assign the rest of the locations with "junk" """
        allJunkItems = Items.getJunkList(False)
        junkItems = []
        for j in allJunkItems:
            if j.Id in settings.junk_pool:
                junkItems.append(j)

        for loc in invalidLocations:
            if loc.LocationCategory is not locationCategory.LEVEL or (loc.LocationCategory is locationCategory.LEVEL and loc.LocationId not in settings.excludedLevels):
                junk_item = random.choice(junkItems)
                #assign another junk item if that location needs another item
                if not self.assignItem(loc,junk_item):
                    junk_item = random.choice(junkItems)
                    self.assignItem(loc,junk_item)
            else:
                self.assignItem(loc,Items.getNullItem())

    def augmentInvalidChecks(self, allLocations):
        """Add invalid check types to locations."""
        for loc in allLocations:
            if loc.LocationCategory in [locationCategory.POPUP, locationCategory.CREATION]:
                loc.InvalidChecks+=[itemType.GROWTH_ABILITY,itemType.ACTION_ABILITY,itemType.SUPPORT_ABILITY,itemType.GAUGE]
            if locationType.STT in loc.LocationTypes and loc.LocationCategory != locationCategory.STATBONUS:
                loc.InvalidChecks+=[itemType.GAUGE]
            if locationType.Critical in loc.LocationTypes:
                loc.InvalidChecks+=[itemType.GAUGE]

            if not self.report_depths.isValid(loc):
                loc.InvalidChecks+=[itemType.REPORT]

            if not self.proof_depths.isValid(loc):
                loc.InvalidChecks+=[itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE]
                if self.yeet_the_bear and loc.LocationCategory is locationCategory.POPUP and loc.LocationId==285:
                    loc.InvalidChecks.remove(itemType.PROOF)

            if not self.story_depths.isValid(loc):
                loc.InvalidChecks+=[itemType.STORYUNLOCK]

            # if both reports and proofs are very restricted (only in 13 locations) add extra proof restrictions to allow reports to be assigned
            if self.report_depths.isValid(loc) and self.proof_depths.isValid(loc):
                if self.report_depths.very_restricted_locations and self.proof_depths.very_restricted_locations:
                    loc.InvalidChecks+=[itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE]
    
    def assignKeybladeAbilities(self, settings: RandomizerSettings, allAbilities, allItems):
        """Assign abilities to keyblades. """
        keybladeLocations = Locations.WeaponList()
        eligible_ids = set(settings.keyblade_support_abilities + settings.keyblade_action_abilities)

        #remove auto abilities from keyblades
        if settings.nightmare:
            eligible_ids.discard(385)
            eligible_ids.discard(386)
            eligible_ids.discard(387)
            eligible_ids.discard(388)
            eligible_ids.discard(568)

        keybladeAbilities = [abil for abil in allAbilities if abil.Id in eligible_ids]
        nightmareRarityWeights = {itemRarity.COMMON:1, itemRarity.UNCOMMON:2, itemRarity.RARE:5, itemRarity.MYTHIC: 5}

        #assign all the abilities for keyblades
        for keyblade in keybladeLocations:
            if keyblade.LocationId=="85" and not settings.pureblood:
                continue
            if keybladeAbilities:
                if settings.nightmare and keyblade.LocationId not in [116,83,84,80]:
                    abilityWeights = [nightmareRarityWeights[abil.Rarity] for abil in keybladeAbilities]
                else:
                    abilityWeights = [1 for abil in keybladeAbilities]
                randomAbility = random.choices(keybladeAbilities,abilityWeights)[0]
                self.assignItem(keyblade,randomAbility)
                allAbilities.remove(randomAbility)
                keybladeAbilities.remove(randomAbility)

                if settings.nightmare and randomAbility.Rarity in [itemRarity.RARE,itemRarity.MYTHIC]:
                    # change the rarity of the keyblade item to the rarity of the ability
                    keyItemId = Items.locationToKeybladeItem(keyblade.LocationId)
                    if keyItemId:
                        keybladeItem = [key for key in allItems if key.Id == keyItemId][0]
                        allItems.remove(keybladeItem)
                        allItems.append(KH2Item(keybladeItem.Id,keybladeItem.Name,keybladeItem.ItemType,randomAbility.Rarity))

            else:
                raise GeneratorException(
                    'Keyblades: Not enough abilities are available to assign an ability to every keyblade'
                )

        # Assign draws to struggle weapons
        struggleWeapons = self.master_locations.getStruggleWeapons()

        for weapon in struggleWeapons:
            self.assignItem(weapon,KH2Item(405,"Draw",itemType.SUPPORT_ABILITY))



    def assignStatBonuses(self,allLocations):
        """Assign all the stat items to bonuses for stats"""
        statItems=Items.getStatItems()
        doubleStat = [loc for loc in allLocations if loc.LocationCategory == locationCategory.DOUBLEBONUS]
        singleStat = [loc for loc in allLocations if loc.LocationCategory in [locationCategory.STATBONUS,locationCategory.HYBRIDBONUS]]
        if len(doubleStat)!=1:
            raise GeneratorException(f"Somehow have two locations with double stat gains {doubleStat}")
        #select two different stats to put on Xemnas 1
        stat1 = random.choice(statItems)
        statItems.remove(stat1)
        stat2 = stat1
        while stat1==stat2:
            stat2 = random.choice(statItems)
        statItems.remove(stat2)
        self.assignItem(doubleStat[0],stat1)
        self.assignItem(doubleStat[0],stat2)
        allLocations.remove(doubleStat[0])
        if len(singleStat)!=len(statItems):
            raise GeneratorException(f"The number of stat bonus locations {len(singleStat)} doesn't match remaining stat items {len(statItems)}")
        #assign the rest
        for item in statItems:
            loc = random.choice(singleStat)
            singleStat.remove(loc)
            if self.assignItem(loc,item):
                allLocations.remove(loc)

        if len(singleStat)!=0:
            raise GeneratorException(f"Leftover stat locations were not assigned. Num remaining {len(singleStat)}")


    def assignItem(self,loc: KH2Location,item: KH2Item, character="Sora"):
        """returns True if assigning a second item to a location. Needed for bonuses with two slots"""
        doubleItem = loc.LocationCategory in [locationCategory.DOUBLEBONUS, locationCategory.HYBRIDBONUS]

        if character=="Sora":
            assignedItems = self.assignedItems
        elif character=="Donald":
            assignedItems = self.assignedDonaldItems
        elif character=="Goofy":
            assignedItems = self.assignedGoofyItems

        if item.ItemType in loc.InvalidChecks:
            raise GeneratorException(f"Trying to assign {item} to {loc} even though it's invalid.")

        assignment_result = None

        if loc in assignedItems:
            assigned = [a for a in assignedItems if a==loc][0]
            if assigned.item is None:
                raise GeneratorException(f"Somehow assigned no item to a location {assigned}")
            if not doubleItem:
                raise GeneratorException(f"Assigning a second item to a location that can't have a second item {assigned}")

            assigned.item2 = item
            assignment_result = True
        else:
            assignedItems.append(ItemAssignment(loc,item))
            assignment_result =  not doubleItem


        if locationType.SYNTH in loc.LocationTypes:
            # assign a recipe to this item
            recipe = SynthesisRecipe(loc, 1 if loc.LocationId < 15 else 2)
            # pick a number of synth items
            num_reqs = random.randint(1,3)
            synth_reqs_list = Items.getSynthRequirementsList()
            picked_items = random.sample(synth_reqs_list,k=num_reqs)
            reqs_list = []
            for i in range(num_reqs):
                item = picked_items[i]
                reqs_list.append(SynthRequirement(item_id=item.Id,amount=random.randint(1,3)))
            recipe.requirements = reqs_list
            self.synthesis_recipes.append(recipe)

        return assignment_result
