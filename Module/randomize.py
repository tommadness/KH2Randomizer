from dataclasses import dataclass, field
import random, zipfile, yaml, io, json, os, base64, asyncio
from Module.spoilerLog import generateSpoilerLog
from Module.randomCmdMenu import RandomCmdMenu
from Module.randomBGM import RandomBGM
from Module.hints import Hints
from Module.startingInventory import StartingInventory

from Class.locationClass import KH2Location, KH2ItemStat, KH2LevelUp, KH2FormLevel, KH2Bonus, KH2Treasure, KH2StartingItem, KH2ItemStat
from Class.itemClass import KH2Item, ItemEncoder
from Class.modYml import modYml

from List.configDict import locationType, itemType
from List.experienceValues import soraExp, formExp
from List.LvupStats import Stats
from List.LocationList import Locations
from List.ItemList import Items

def noop(self, *args, **kw):
    pass


@dataclass
class KH2Randomizer():
    seedName: str

    _locationItems: list[tuple[KH2Location, KH2Item]] = field(default_factory=list)

    _validLocationList: list[KH2Location] = field(default_factory=list)
    _allLocationList: list[KH2Location] = field(default_factory=list)
    _validItemList: list[KH2Item] = field(default_factory=list)

    _validLocationListGoofy: list[KH2Location] = field(default_factory=list)
    _allLocationListGoofy: list[KH2Location] = field(default_factory=list)
    _validItemListGoofy: list[KH2Item] = field(default_factory=list)

    _validLocationListDonald: list[KH2Location] = field(default_factory=list)
    _allLocationListDonald: list[KH2Location] = field(default_factory=list)
    _validItemListDonald: list[KH2Item] = field(default_factory=list)

    def __post_init__(self):
        random.seed(self.seedName)

    def populateLocations(self, excludeWorlds):
        self._allLocationList = Locations.getTreasureList() + Locations.getSoraLevelList() + Locations.getSoraBonusList() + Locations.getFormLevelList() + Locations.getSoraWeaponList() + Locations.getSoraStartingItemList()

        self._validLocationList = [location for location in self._allLocationList if not set(location.LocationTypes).intersection(excludeWorlds+["Level1Form", "SummonLevel"])]

        self._allLocationListGoofy = Locations.getGoofyWeaponList() + Locations.getGoofyStartingItemList() + Locations.getGoofyBonusList()

        self._validLocationListGoofy = [location for location in self._allLocationListGoofy if not set(location.LocationTypes).intersection(excludeWorlds)]

        self._allLocationListDonald = Locations.getDonaldWeaponList() + Locations.getDonaldStartingItemList() + Locations.getDonaldBonusList()

        self._validLocationListDonald = [location for location in self._allLocationListDonald if not set(location.LocationTypes).intersection(excludeWorlds)]

    def populateItems(self, promiseCharm = False, startingInventory=[], abilityListModifier=None):
        abilityList = Items.getSupportAbilityList() + Items.getActionAbilityList()
        if abilityListModifier:
            abilityList = abilityListModifier(Items.getActionAbilityList(), Items.getSupportAbilityList())
        validItemList = Items.getItemList() + abilityList

        self._validItemListGoofy = Items.getGoofyAbilityList()
        self._validItemListDonald = Items.getDonaldAbilityList()
        if promiseCharm:
            validItemList.append(KH2Item(524, "PromiseCharm",itemType.PROMISE_CHARM))

        self._validItemList = [item for item in validItemList if not str(item.Id) in startingInventory]





    def validateCount(self):
        #additionalGoofyLocations = Locations.getAdditionalGoofy(len(self._validItemListGoofy) - len(self._validLocationListGoofy))
        #additionalDonaldLocations = Locations.getAdditionalDonald(len(self._validItemListDonald) - len(self._validLocationListDonald))
        return len(self._validItemList) < len(self._validLocationList)

    def goMode(self):
        locations = [location for location in self._validLocationList if set(location.LocationTypes).intersection([locationType.Free])]
        print(locations)
        proofs = [item for item in self._validItemList if item.ItemType in [itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE]]
        print(proofs)
        for index, location in enumerate(locations):
            location.setReward(proofs[index].Id)
            self._validLocationList.remove(location)
            location.InvalidChecks.append(itemType.JUNK)
            self._validItemList.remove(proofs[index])
            self._locationItems.append((location, proofs[index]))


    def setKeybladeAbilities(self, keybladeAbilities = ["Support"], keybladeMinStat = 0, keybladeMaxStat = 7):
        keybladeList = [location for location in self._validLocationList if isinstance(location, KH2ItemStat)]
        abilityList = [item for item in self._validItemList if (item.ItemType == itemType.SUPPORT_ABILITY and "Support" in keybladeAbilities) or (item.ItemType == itemType.ACTION_ABILITY and "Action" in keybladeAbilities)]

        for keyblade in keybladeList:
            randomAbility = random.choice(abilityList)
            keyblade.setReward(randomAbility.Id)
            keyblade.setStats(keybladeMinStat, keybladeMaxStat)
            self._locationItems.append((keyblade,randomAbility))
            abilityList.remove(randomAbility)
            self._validItemList.remove(randomAbility)

        shieldList = [location for location in self._validLocationListGoofy if isinstance(location, KH2ItemStat)]
        for shield in shieldList:
            random.shuffle(self._validItemListGoofy)
            randomAbility = self._validItemListGoofy.pop()
            shield.setReward(randomAbility.Id)
            self._locationItems.append((shield,randomAbility))

        staffList = [location for location in self._validLocationListDonald if isinstance(location, KH2ItemStat)]
        for staff in staffList:
            random.shuffle(self._validItemListDonald)
            randomAbility = self._validItemListDonald.pop()
            staff.setReward(randomAbility.Id)
            self._locationItems.append((staff,randomAbility))

    def setRewards(self, levelChoice="ExcludeFrom50", betterJunk=False):
        locations = [location for location in self._validLocationList if not isinstance(location, KH2ItemStat)]
        for item in self._validItemList:
            while True:
                randomLocation = random.choice(locations)
                if not item.ItemType in randomLocation.InvalidChecks:
                    randomLocation.setReward(item.Id)
                    locations.remove(randomLocation)
                    self._locationItems.append((randomLocation,item))
                    break
        
        junkLocations = locations + [location for location in self._allLocationList if (not location in self._validLocationList and not set(location.LocationTypes).intersection([levelChoice]) and not set(location.InvalidChecks).intersection([itemType.JUNK]))]


        for location in junkLocations:
            randomJunk = random.choice(Items.getJunkList(betterJunk))
            location.setReward(randomJunk.Id)
            self._locationItems.append((location, randomJunk))

        goofyLocations = [location for location in self._validLocationListGoofy if not isinstance(location, KH2ItemStat)]
        for item in self._validItemListGoofy:
            if len(goofyLocations) == 0:
                break
            randomLocation = random.choice(goofyLocations)
            randomLocation.setReward(item.Id)
            if not randomLocation.DoubleReward:
                self._validLocationListGoofy.remove(randomLocation)
                goofyLocations.remove(randomLocation)
                continue
            if not randomLocation.BonusItem2 == 0:
                self._validLocationListGoofy.remove(randomLocation)
                goofyLocations.remove(randomLocation)
                continue

        donaldLocations = [location for location in self._validLocationListDonald if not isinstance(location, KH2ItemStat)]
        for item in self._validItemListDonald:
            if len(donaldLocations) == 0:
                break
            randomLocation = random.choice(donaldLocations)
            randomLocation.setReward(item.Id)
            if not randomLocation.DoubleReward:
                self._validLocationListDonald.remove(randomLocation)
                donaldLocations.remove(randomLocation)
                continue
            if not randomLocation.BonusItem2 == 0:
                self._validLocationListDonald.remove(randomLocation)
                donaldLocations.remove(randomLocation)
                continue            
            

    def setLevels(self, soraExpMult, formExpMult, statsList = None):
        if statsList == None:
            statsList = [{"Stat":"Str","Value": 2},{"Stat":"Mag", "Value": 2},{"Stat": "Def", "Value": 1},{"Stat": "Ap", "Value": 2}]
        soraLevels = [location for location in self._allLocationList if isinstance(location, KH2LevelUp)]
        for index, level in enumerate(soraLevels):
            statChoice = random.choice(statsList)
            level.Exp = round(soraExp[level.Level] / soraExpMult)
            if level.Level > 1:
                level.setStat(soraLevels[index-1], statChoice["Stat"], statChoice["Value"])
                if level.getReward() == 0:
                    statChoice2 = statChoice
                    while (statChoice2 == statChoice):
                        statChoice2 = random.choice(statsList)
                    level.setStat2(statChoice2["Stat"],statChoice2["Value"])



        formLevels = [location for location in self._allLocationList if isinstance(location, KH2FormLevel)]
        for level in formLevels:
            level.Experience = round(formExp[level.FormId][level.FormLevel] / float(formExpMult[str(level.FormId)]))

    def setBonusStats(self):
        statsList = Stats.getBonusStats()
        locations = [location for location in self._allLocationList if isinstance(location, KH2Bonus) and location.HasStat]
        for location in locations:
            random.shuffle(statsList)
            first_stat = statsList.pop()
            location.setStat(first_stat)
            if location.DoubleReward:
                while statsList[0]==first_stat:
                    random.shuffle(statsList)
                location.setStat(statsList.pop())

        print(len(statsList))

    def validateSeed(self, startingInventory):
        # check if the seed is completable
        need_fire_blizzard_thunder = lambda inventory : (21 in inventory and 22 in inventory and 23 in inventory)
        need_2_magnets = lambda inventory : (inventory.count(87)>=2)
        need_2_magnets_all_thunders = lambda inventory : (inventory.count(87)>=2 and inventory.count(23)==3)
        count_high_jumps = lambda inventory : ((94 in inventory) + (95 in inventory) + (96 in inventory) + (97 in inventory))
        count_quick_runs = lambda inventory : ((98 in inventory) + (99 in inventory) + (100 in inventory) + (101 in inventory))
        count_aerial_dodges = lambda inventory : ((102 in inventory) + (103 in inventory) + (104 in inventory) + (105 in inventory))
        count_glides = lambda inventory : ((106 in inventory) + (107 in inventory) + (108 in inventory) + (109 in inventory))
        need_growths = lambda inventory : (count_high_jumps(inventory)>=3 and count_quick_runs(inventory)>=3 and count_aerial_dodges(inventory)>=3 and count_glides(inventory)>=3)
        need_proof_connection = lambda inventory : (593 in inventory)
        need_proof_peace = lambda inventory : (595 in inventory)
        has_valor = lambda inventory : (26 in inventory)
        has_wisdom = lambda inventory : (27 in inventory)
        has_limit = lambda inventory : (563 in inventory)
        has_master = lambda inventory : (31 in inventory)
        has_final = lambda inventory : (29 in inventory)
        count_forms = lambda inventory : (has_valor(inventory) + has_wisdom(inventory) + has_limit(inventory) + has_master(inventory) + has_final(inventory))
        need_forms  = lambda inventory : (count_forms(inventory)==5)
        need_summons = lambda inventory : (( 159 in inventory) and ( 160 in inventory) and ( 25 in inventory) and ( 383 in inventory))
        need_forms_and_summons = lambda inventory : (need_forms(inventory) and need_summons(inventory))
        count_pages = lambda inventory : inventory.count(32)
        need_1_page = lambda inventory : count_pages(inventory) >= 1
        need_2_pages = lambda inventory : count_pages(inventory) >= 2
        need_3_pages = lambda inventory : count_pages(inventory) >= 3
        need_4_pages = lambda inventory : count_pages(inventory) >= 4
        need_5_pages = lambda inventory : count_pages(inventory) == 5

        def make_form_lambda(form_id,form_level):
            if form_id==1:
                return lambda inventory : has_valor(inventory) and count_forms(inventory)>=form_level-2
            if form_id==2:
                return lambda inventory : has_wisdom(inventory) and count_forms(inventory)>=form_level-2
            if form_id==3:
                return lambda inventory : has_limit(inventory) and count_forms(inventory)>=form_level-2
            if form_id==4:
                return lambda inventory : has_master(inventory) and count_forms(inventory)>=form_level-2
            if form_id==5:
                return lambda inventory : has_final(inventory) and count_forms(inventory)>=form_level-2

            return lambda inventory : False

        restricted_treasures = [([34,486,303,545,550],need_fire_blizzard_thunder),
                                ([287],need_2_magnets),
                                ([279,538],need_2_magnets_all_thunders),
                                ([562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582],need_growths),
                                ([587,591],need_proof_connection),
                                ([588,589],need_proof_peace),
                                ([560],need_forms),
                                ([518],need_forms_and_summons),
                                ([103,104,105], need_1_page),
                                ([100,101,314], need_2_pages),
                                ([106,107,108], need_3_pages),
                                ([110,111,112,113,115,116,284,485], need_4_pages),
                                ([285,539,312,94], need_5_pages)]

        restricted_bonuses = [([15,need_fire_blizzard_thunder])]
        restricted_forms = [(1,2,make_form_lambda(1,2)),
                            (1,3,make_form_lambda(1,3)),
                            (1,4,make_form_lambda(1,4)),
                            (1,5,make_form_lambda(1,5)),
                            (1,6,make_form_lambda(1,6)),
                            (1,7,make_form_lambda(1,7)),
                            (2,2,make_form_lambda(2,2)),
                            (2,3,make_form_lambda(2,3)),
                            (2,4,make_form_lambda(2,4)),
                            (2,5,make_form_lambda(2,5)),
                            (2,6,make_form_lambda(2,6)),
                            (2,7,make_form_lambda(2,7)),
                            (3,2,make_form_lambda(3,2)),
                            (3,3,make_form_lambda(3,3)),
                            (3,4,make_form_lambda(3,4)),
                            (3,5,make_form_lambda(3,5)),
                            (3,6,make_form_lambda(3,6)),
                            (3,7,make_form_lambda(3,7)),
                            (4,2,make_form_lambda(4,2)),
                            (4,3,make_form_lambda(4,3)),
                            (4,4,make_form_lambda(4,4)),
                            (4,5,make_form_lambda(4,5)),
                            (4,6,make_form_lambda(4,6)),
                            (4,7,make_form_lambda(4,7)),
                            (5,2,make_form_lambda(5,2)),
                            (5,3,make_form_lambda(5,3)),
                            (5,4,make_form_lambda(5,4)),
                            (5,5,make_form_lambda(5,5)),
                            (5,6,make_form_lambda(5,6)),
                            (5,7,make_form_lambda(5,7))]
        def treasure_restriction(location_id):
            for loc_list,condition in restricted_treasures:
                if location_id in loc_list:
                    return condition
            return lambda inventory: True
        def bonus_restriction(location_id):
            for loc_id,condition in restricted_bonuses:
                if location_id == loc_id:
                    return condition
            return lambda inventory: True
        def form_restriction(form_id,form_level):
            for f_id,f_level,condition in restricted_forms:
                if f_id == form_id and f_level==form_level:
                    return condition
            return lambda inventory: True

        trsrList = [location for location in self._allLocationList if isinstance(location, KH2Treasure)]
        lvupList = [location for location in self._allLocationList if isinstance(location, KH2LevelUp)]
        bonsList = [location for location in self._allLocationList if isinstance(location, KH2Bonus)]
        fmlvList = [location for location in self._allLocationList if isinstance(location, KH2FormLevel)]
        plrpList = []
        [plrpList.append(location) for location in self._allLocationList if isinstance(location, KH2StartingItem) and not location in plrpList]
        StartingInventory.generateStartingInventory(plrpList[0], startingInventory)
        inventory = []


        # grab everything that can't possibly be locked by items
        for i in plrpList:
            inventory += i.Items
        for i in lvupList:
            inventory.append(i.getReward())


        changed = True
        depth = 0
        while changed:
            depth+=1
            if len(trsrList)==0 and len(bonsList)==0 and len(fmlvList)==0:
                return True
            changed = False
            treasures_to_remove = []
            bonuses_to_remove = []
            forms_to_remove = []
            # pass through remaining treasures and find unlockable things
            for i in trsrList:
                location_id = i.Id
                reward_id = i.ItemId
                if treasure_restriction(location_id)(inventory):
                    treasures_to_remove.append(i)
                    inventory.append(reward_id)
                    changed = True
            for i in bonsList:
                location_id = i.RewardId
                reward_id = i.getReward()
                if bonus_restriction(location_id)(inventory):
                    bonuses_to_remove.append(i)
                    inventory.append(reward_id)
                    changed = True
            for i in fmlvList:
                reward_id = i.Ability
                if form_restriction(i.FormId,i.FormLevel)(inventory):
                    forms_to_remove.append(i)
                    inventory.append(reward_id)
                    changed = True
            for i in treasures_to_remove:
                trsrList.remove(i)
            for i in bonuses_to_remove:
                bonsList.remove(i)
            for i in forms_to_remove:
                fmlvList.remove(i)

        return False


    def generateZip(self, enemyOptions={"boss":"Disabled"}, spoilerLog = False, cmdMenuChoice = "vanilla", randomBGM = False, hintsType = "Disabled", startingInventory=[], platform="PCSX2"):
        trsrList = [location for location in self._allLocationList if isinstance(location, KH2Treasure)]
        lvupList = [location for location in self._allLocationList if isinstance(location, KH2LevelUp)]
        bonsList = [location for location in self._allLocationList if isinstance(location, KH2Bonus)] + [location for location in self._allLocationListDonald if isinstance(location, KH2Bonus)] + [location for location in self._allLocationListGoofy if isinstance(location, KH2Bonus)]
        fmlvList = [location for location in self._allLocationList if isinstance(location, KH2FormLevel)]
        itemList = [location for location in self._allLocationList if isinstance(location, KH2ItemStat)] + [location for location in self._allLocationListDonald if isinstance(location, KH2ItemStat)] + [location for location in self._allLocationListGoofy if isinstance(location, KH2ItemStat)]
        plrpList = []
        [plrpList.append(location) for location in self._allLocationList if isinstance(location, KH2StartingItem) and not location in plrpList]
        StartingInventory.generateStartingInventory(plrpList[0], startingInventory)
        [plrpList.append(location) for location in self._allLocationListDonald if isinstance(location, KH2StartingItem) and not location in plrpList]
        [plrpList.append(location) for location in self._allLocationListGoofy if isinstance(location, KH2StartingItem) and not location in plrpList]

        mod = modYml.getDefaultMod()

        formattedTrsr = {}
        for trsr in trsrList:
            formattedTrsr[trsr.Id] = {'ItemId':trsr.ItemId}

        formattedLvup = {}
        for lvup in lvupList:
            if not lvup.Character in formattedLvup.keys():
                formattedLvup[lvup.Character] = {}
            formattedLvup[lvup.Character][lvup.Level] = {
                "Exp": lvup.Exp,
                "Strength": lvup.Strength,
                "Magic": lvup.Magic,
                "Defense": lvup.Defense,
                "Ap": lvup.Ap,
                "SwordAbility": lvup.SwordAbility,
                "ShieldAbility": lvup.ShieldAbility,
                "StaffAbility": lvup.StaffAbility,
                "Padding": 0,
                "Character": lvup.Character,
                "Level": lvup.Level
            }

        formattedBons = {}
        for bons in bonsList:
            if not bons.RewardId in formattedBons.keys():
                formattedBons[bons.RewardId] = {}
            formattedBons[bons.RewardId][bons.getCharacterName()] = {
                "RewardId": bons.RewardId,
                "CharacterId": bons.CharacterId,
                "HpIncrease": bons.HpIncrease,
                "MpIncrease": bons.MpIncrease,
                "DriveGaugeUpgrade": bons.DriveGaugeUpgrade,
                "ItemSlotUpgrade": bons.ItemSlotUpgrade,
                "AccessorySlotUpgrade": bons.AccessorySlotUpgrade,
                "ArmorSlotUpgrade": bons.ArmorSlotUpgrade,
                "BonusItem1": bons.BonusItem1,
                "BonusItem2": bons.BonusItem2,
                "Padding": 0
            }

        formattedFmlv = {}
        for fmlv in fmlvList:
            if not fmlv.getFormName() in formattedFmlv.keys():
                formattedFmlv[fmlv.getFormName()] = []
            formattedFmlv[fmlv.getFormName()].append({
                "Ability": fmlv.Ability,
                "Experience": fmlv.Experience,
                "FormId": fmlv.FormId,
                "FormLevel": fmlv.FormLevel,
                "GrowthAbilityLevel": fmlv.GrowthAbilityLevel,
            })

        formattedItem = {"Stats": []}
        for item in itemList:
            formattedItem["Stats"].append({
                "Id": item.Id,
                "Attack": item.Attack,
                "Magic": item.Magic,
                "Defense": item.Defense,
                "Ability": item.Ability,
                "AbilityPoints": item.AbilityPoints,
                "Unknown08": item.Unknown08,
                "FireResistance": item.FireResistance,
                "IceResistance": item.IceResistance,
                "LightningResistance": item.LightningResistance,
                "DarkResistance": item.DarkResistance,
                "Unknown0d": item.Unknown0d,
                "GeneralResistance": item.GeneralResistance,
                "Unknown": item.Unknown
            })

        formattedPlrp = []
        lionStartWithDash = KH2StartingItem(135, 0, Hp=0, Ap=0, Mp=0, ArmorSlotMax=0,AccessorySlotMax=0,ItemSlotMax=0, Items=[32930, 32930, 32931, 32931, 33288, 33289, 33290, 33294])
        plrpList.append(lionStartWithDash)
        for plrp in plrpList:
            plrp.padStartingItems()
            formattedPlrp.append({
                "Character": plrp.Character,
                "Id": plrp.Difficulty,
                "Hp": plrp.Hp,
                "Mp": plrp.Mp,
                "Ap": plrp.Ap,
                "ArmorSlotMax": plrp.ArmorSlotMax,
                "AccessorySlotMax": plrp.AccessorySlotMax,
                "ItemSlotMax": plrp.ItemSlotMax,
                "Items": plrp.Items,
                "Padding": [0] * 52
            })

        sys = modYml.getSysYAML()

        

        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as outZip:
            yaml.emitter.Emitter.process_tag = noop

            

            outZip.writestr("TrsrList.yml", yaml.dump(formattedTrsr, line_break="\r\n"))
            outZip.writestr("BonsList.yml", yaml.dump(formattedBons, line_break="\r\n"))
            outZip.writestr("LvupList.yml", yaml.dump(formattedLvup, line_break="\r\n"))
            outZip.writestr("FmlvList.yml", yaml.dump(formattedFmlv, line_break="\r\n"))
            outZip.writestr("ItemList.yml", yaml.dump(formattedItem, line_break="\r\n"))
            outZip.writestr("PlrpList.yml", yaml.dump(formattedPlrp, line_break="\r\n"))
            outZip.writestr("sys.yml", yaml.dump(sys, line_break="\r\n"))
            outZip.writestr("jm.yml", yaml.dump(modYml.getJMYAML(), line_break="\r\n"))

            if not hintsType == "Disabled":
                Hints.generateHints(self._locationItems, hintsType, self.seedName, outZip)

            enemySpoilers = None
            if not enemyOptions["boss"] == "Disabled" or not enemyOptions["enemy"] == "Disabled" or enemyOptions["remove_damage_cap"]:
                if platform == "PC":
                    enemyOptions["memory_expansion"] = True
                else:
                    enemyOptions["memory_expansion"] = False
                if enemyOptions.get("boss", False) or enemyOptions.get("enemy", False) or enemyOptions.get("remove_damage_cap", False):
                    from khbr.randomizer import Randomizer as khbr
                    enemySpoilers = khbr().generateToZip("kh2", enemyOptions, mod, outZip)

            if spoilerLog:
                mod["title"] += " {seedName}".format(seedName = self.seedName)
                with open("static/spoilerlog.html") as spoiler_site:
                    html_template = spoiler_site.read().replace("SPOILER_JSON_FROM_SEED",json.dumps(generateSpoilerLog(self._locationItems), indent=4, cls=ItemEncoder))
                    outZip.writestr("spoilerlog.html",html_template)
                if enemySpoilers:
                    outZip.writestr("enemyspoilers.txt", enemySpoilers)

            mod["assets"] += RandomCmdMenu.randomizeCmdMenus(cmdMenuChoice, outZip, platform)
            
            mod["assets"] += RandomBGM.randomizeBGM(randomBGM, platform)

            outZip.write("Module/icon.png", "icon.png")


            outZip.writestr("mod.yml", yaml.dump(mod, line_break="\r\n"))
            outZip.close()
        data.seek(0)
        return data


        

        










    
if __name__ == '__main__':
    randomizer = KH2Randomizer()
    randomizer.populateLocations([locationType.LoD, "ExcludeFrom50"])
    randomizer.populateItems()
    if randomizer.validateCount():
        randomizer.setKeybladeAbilities()
        randomizer.setRewards()
        randomizer.setLevels(soraExpMult = 1.5, formExpMult = {1:6, 2:3, 3:3, 4:3, 5:3})
        randomizer.setBonusStats()
        zip = randomizer.generateZip(hintsType="JSmartee").getbuffer()
        open("randoSeed.zip", "wb").write(zip)