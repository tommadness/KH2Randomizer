from dataclasses import dataclass

from Class.exceptions import GeneratorException
from Class.newLocationClass import KH2Location
from Class.itemClass import KH2Item
from List.configDict import locationCategory, itemType, locationDepth, locationType
from List.ItemList import Items
from List.NewLocationList import Locations
from Module.RandomizerSettings import RandomizerSettings

import random

class LocationWeights():
    def __init__(self):
        pass

    def getWeight(self,loc: KH2Location):
        return 1


class LocationDepths():
    def __init__(self):
        pass

    def getDepth(self, loc: KH2Location):
        return locationDepth.FirstVisit

    def isReportValid(self, loc: KH2Location, reportDepth: locationDepth):
        if self.getDepth(loc) == locationDepth.FirstVisit:
            # if setting is Bosses, then first visits can't have reports
            if reportDepth==locationDepth.FirstBoss or reportDepth==locationDepth.SecondBoss:
                return False
        elif self.getDepth(loc) == locationDepth.SecondVisit:
            # if setting is Bosses or first visits, second visits can't have reports
            if reportDepth==locationDepth.FirstVisit or reportDepth==locationDepth.FirstBoss or reportDepth==locationDepth.SecondBoss:
                return False
        elif self.getDepth(loc) == locationDepth.FirstBoss:
            # if setting is for second second bosses, then first bosses can't have reports
            if reportDepth==locationDepth.SecondBoss:
                return False
        elif self.getDepth(loc) == locationDepth.SecondBoss:
            if reportDepth==locationDepth.FirstVisit or reportDepth==locationDepth.FirstBoss:
                return False
        elif self.getDepth(loc) == locationDepth.DataFight:
            # if setting is not for data fights, then data fights can't have reports
            if reportDepth != locationDepth.DataFight:
                return False
        return True

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


class CantAssignItemException(Exception):
    pass

class Randomizer():
    def __init__(self, settings: RandomizerSettings):
        random.seed(settings.random_seed)
        self.master_locations = Locations(settings.reverse_rando)
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


        for index,l in enumerate(levelLocations):
            if index!=0:
                stat_choices = random.sample(levelStats,k=2)
                addStat(stat_choices[0])
                if l.Description in settings.excludedLevels:
                    addStat(stat_choices[1])
            exp+=(settings.sora_exp[index+1]-settings.sora_exp[index])
            self.levelStats.append(LevelStats(l,exp,strength,magic,defense,ap))

    def assignWeaponStats(self,settings):
        soraMin = settings.keyblade_min_stat
        soraMax = settings.keyblade_max_stat
        keybladeLocations =  Locations.WeaponList()
        for key in keybladeLocations:
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

    def assignSoraItems(self, settings):
        allItems = [i for i in Items.getItemList() if i not in settings.startingItems]
        allAbilities =  settings.abilityListModifier(Items.getActionAbilityList(), Items.getSupportAbilityList())
        if settings.promiseCharm:
            allItems+=[Items.getPromiseCharm()]
        allLocations = self.master_locations.getAllSoraLocations()

        self.augmentInvalidChecks(settings, allLocations)

        if settings.statSanity:
            allItems+=Items.getStatItems()
        else:
            self.assignStatBonuses(allLocations)
        
        if settings.antiform:
            allItems.append(Items.getAntiform())

        invalidLocations = [loc for loc in allLocations if (any(item in loc.LocationTypes for item in settings.disabledLocations) or loc.Description in settings.excludedLevels)]
        validLocations =  [loc for loc in allLocations if loc not in invalidLocations]

        if len(allLocations)!=(len(invalidLocations)+len(validLocations)):
            raise GeneratorException(f"Separating valid {len(validLocations)} and invalid {len(invalidLocations)} locations removed locations from existence (total {len(allLocations)} )")
        
        self.assignKeybladeAbilities(settings, allAbilities)
        allItems+=allAbilities

        #assign valid items to all valid locations remaining
        for item in allItems:
            count=0
            while True:
                count+=1
                randomLocation = random.choice(validLocations)
                if item.ItemType not in randomLocation.InvalidChecks:
                    if self.assignItem(randomLocation,item):
                        validLocations.remove(randomLocation)
                    break
                if count==100:
                    raise CantAssignItemException(f"Trying to assign {item} and failed 100 times")

        invalidLocations+=validLocations
        self.assignJunkLocations(settings, invalidLocations)

    def assignJunkLocations(self, settings, invalidLocations):
        """ assign the rest of the locations with "junk" """
        junkItems = Items.getJunkList(settings.betterJunk)
        for loc in invalidLocations:
            if loc.LocationCategory is not locationCategory.LEVEL or loc.Description not in settings.excludedLevels:
                junk_item = random.choice(junkItems)
                #assign another junk item if that location needs another item
                if not self.assignItem(loc,junk_item):
                    junk_item = random.choice(junkItems)
                    self.assignItem(loc,junk_item)
            else:
                self.assignItem(loc,Items.getNullItem())

    def augmentInvalidChecks(self, settings, allLocations):
        """Add invalid check types to locations."""
        for loc in allLocations:
            if loc.LocationCategory == locationCategory.POPUP:
                loc.InvalidChecks+=[itemType.GROWTH_ABILITY,itemType.ACTION_ABILITY,itemType.SUPPORT_ABILITY,itemType.GAUGE]
            if locationType.STT in loc.LocationTypes:
                loc.InvalidChecks+=[itemType.GAUGE]

            # if not settings.depths.isReportValid(loc,settings.reportDepth):
            #     loc.InvalidChecks+=[itemType.REPORT]
    
    def assignKeybladeAbilities(self, settings, allAbilities):
        """Assign abilities to keyblades. """
        keybladeLocations =  Locations.WeaponList()
        keybladeAbilities = [abil for abil in allAbilities if abil.ItemType in settings.keybladeAbilities]
        random.shuffle(keybladeLocations)

        #assign all the abilities for keyblades
        for keyblade in keybladeLocations:
            if allAbilities: # by checking this here, we can avoid situations where we softlock generation
                randomAbility = random.choice(keybladeAbilities)
                self.assignItem(keyblade,randomAbility)
                allAbilities.remove(randomAbility)
                keybladeAbilities.remove(randomAbility)

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
