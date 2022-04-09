from dataclasses import dataclass

from Class.exceptions import GeneratorException,CantAssignItemException
from Class.newLocationClass import KH2Location
from Class.itemClass import KH2Item, itemRarity
from List.configDict import locationCategory, itemType, locationType
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

class Randomizer():
    def __init__(self, settings: RandomizerSettings):
        random.seed(settings.full_rando_seed)
        self.regular_locations = Locations(settings,False)
        self.reverse_locations = Locations(settings,True)
        self.master_locations = self.regular_locations if settings.regular_rando else self.reverse_locations
        self.location_weights = LocationWeights(settings,self.regular_locations,self.reverse_locations)
        self.report_depths = ItemDepths(settings.reportDepth,self.master_locations)
        self.proof_depths = ItemDepths(settings.proofDepth,self.master_locations)
        self.yeet_the_bear = settings.yeetTheBear
        self.assignedItems = []
        self.assignedDonaldItems = []
        self.assignedGoofyItems = []
        self.weaponStats = []
        self.levelStats = []
        self.formLevelExp = []
        self.assignSoraItems(settings)
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
                if l.Description in settings.excludedLevels:
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
        allItems = [i for i in Items.getItemList() if i.Id not in settings.startingItems]
        if not settings.pureblood:
            allItems = [i for i in allItems if i.Id!=71]

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

        if settings.promiseCharm:
            allItems+=[Items.getPromiseCharm()]
        allLocations = self.master_locations.getAllSoraLocations()

        self.augmentInvalidChecks(allLocations)

        if settings.statSanity:
            allItems+=Items.getStatItems()
        else:
            self.assignStatBonuses(allLocations)

        invalidLocations = [loc for loc in allLocations if (any(item in loc.LocationTypes for item in settings.disabledLocations) or loc.Description in settings.excludedLevels)]
        validLocations =  [loc for loc in allLocations if loc not in invalidLocations]

        if len(allLocations)!=(len(invalidLocations)+len(validLocations)):
            raise GeneratorException(f"Separating valid {len(validLocations)} and invalid {len(invalidLocations)} locations removed locations from existence (total {len(allLocations)} )")
        
        self.assignKeybladeAbilities(settings, allAbilities, allItems)
        allItems=allAbilities+allItems

        restricted_reports = self.report_depths.very_restricted_locations
        restricted_proofs = self.proof_depths.very_restricted_locations

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

            if restricted_reports:
                weights = [self.location_weights.getWeight(item,loc) if itemType.REPORT in loc.InvalidChecks else 0 for loc in validLocations]
            elif restricted_proofs:
                weights = [self.location_weights.getWeight(item,loc) if (any(i_type in loc.InvalidChecks for i_type in [itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE])) else 0 for loc in validLocations]
            else:
                weights = [self.location_weights.getWeight(item,loc) for loc in validLocations]
            # modify the weights for reports if the report depth is specific
            if restricted_reports and item.ItemType is itemType.REPORT:
                weights = [1 if itemType.REPORT not in loc.InvalidChecks else 0 for loc in validLocations ]
            elif restricted_proofs and item.ItemType in [itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE]:
                weights = [1 if not (any(i_type in loc.InvalidChecks for i_type in [itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE])) else 0 for loc in validLocations ]
            count=0
            while True:
                count+=1
                if len(weights)==0:
                    raise CantAssignItemException(f"Ran out of locations to assign items to.")
                randomLocation = random.choices(validLocations,weights)[0]
                if item.ItemType not in randomLocation.InvalidChecks:
                    if self.assignItem(randomLocation,item):
                        validLocations.remove(randomLocation)
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
            if loc.LocationCategory is not locationCategory.LEVEL or loc.Description not in settings.excludedLevels:
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
            if loc.LocationCategory == locationCategory.POPUP:
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

            # if both reports and proofs are very restricted (only in 13 locations) add extra proof restrictions to allow reports to be assigned
            if self.report_depths.isValid(loc) and self.proof_depths.isValid(loc):
                if self.report_depths.very_restricted_locations and self.proof_depths.very_restricted_locations:
                    loc.InvalidChecks+=[itemType.PROOF,itemType.PROOF_OF_CONNECTION,itemType.PROOF_OF_PEACE]
    
    def assignKeybladeAbilities(self, settings: RandomizerSettings, allAbilities, allItems):
        """Assign abilities to keyblades. """
        keybladeLocations = Locations.WeaponList()
        eligible_ids = set(settings.keyblade_support_abilities + settings.keyblade_action_abilities)

        #remove auto abilities from keyblades
        if settings.itemPlacementDifficulty == "Nightmare":
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
                if settings.itemPlacementDifficulty == "Nightmare" and keyblade.LocationId not in [116,83,84,80]:
                    abilityWeights = [nightmareRarityWeights[abil.Rarity] for abil in keybladeAbilities]
                else:
                    abilityWeights = [1 for abil in keybladeAbilities]
                randomAbility = random.choices(keybladeAbilities,abilityWeights)[0]
                self.assignItem(keyblade,randomAbility)
                allAbilities.remove(randomAbility)
                keybladeAbilities.remove(randomAbility)

                if settings.itemPlacementDifficulty == "Nightmare" and randomAbility.Rarity in [itemRarity.RARE,itemRarity.MYTHIC]:
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

        if loc in assignedItems:
            assigned = [a for a in assignedItems if a==loc][0]
            if assigned.item is None:
                raise GeneratorException(f"Somehow assigned no item to a location {assigned}")
            if not doubleItem:
                raise GeneratorException(f"Assigning a second item to a location that can't have a second item {assigned}")

            assigned.item2 = item
            return True
        else:
            assignedItems.append(ItemAssignment(loc,item))
            return not doubleItem
