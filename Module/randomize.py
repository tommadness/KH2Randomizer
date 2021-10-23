from dataclasses import dataclass, field
import random, zipfile, yaml, io, json, os, base64, asyncio, struct
from pathlib import Path
from Module.spoilerLog import generateSpoilerLog
from Module.randomCmdMenu import RandomCmdMenu
from Module.randomBGM import RandomBGM
from Module.hints import Hints
from Module.startingInventory import StartingInventory
from Module.importantItems import getImportantChecks,getUsefulItems,getUsefulAbilities,getUsefulNightmarePassiveAbilities,getUsefulNightmareActiveAbilities,getSCOM

from Class.locationClass import KH2Location, KH2ItemStat, KH2Puzzle, KH2LevelUp, KH2FormLevel, KH2Bonus, KH2Treasure, KH2StartingItem, KH2ItemStat
from Class.itemClass import KH2Item, ItemEncoder
from Class.modYml import modYml

from List.configDict import locationType, itemType, locationDepth
from List.experienceValues import soraExp, formExp
from List.LvupStats import Stats
from List.LocationList import Locations
from List.ItemList import Items

def noop(self, *args, **kw):
    pass


@dataclass
class KH2Randomizer():
    seedName: str
    seedHashIcons: list[str] = field(default_factory=list)
    spoiler: bool = False
    nightmareSetting: bool = False
    puzzleRando: bool = False

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
        # call the random number generator with a random salt addition if a spoiler log is generated
        if self.spoiler:
            random.seed(self.seedName+str(random.random()))

    def populateLocations(self, excludeWorlds, maxItemLogic=False, item_difficulty="Normal",reportDepth=None):
        self._allLocationList = Locations.getTreasureList(maxItemLogic) + Locations.getSoraLevelList() + Locations.getSoraBonusList(maxItemLogic) + Locations.getFormLevelList(maxItemLogic) + Locations.getPuzzleLocations() + Locations.getSoraWeaponList() + Locations.getSoraStartingItemList()

        self._validLocationList = [location for location in self._allLocationList if not set(location.LocationTypes).intersection(excludeWorlds+["Level1Form", "SummonLevel"])]

        self.puzzleRando = "Puzzle" not in excludeWorlds

        self._allLocationListGoofy = Locations.getGoofyWeaponList() + Locations.getGoofyStartingItemList() + Locations.getGoofyBonusList()

        self._validLocationListGoofy = [location for location in self._allLocationListGoofy if not set(location.LocationTypes).intersection(excludeWorlds)]

        self._allLocationListDonald = Locations.getDonaldWeaponList() + Locations.getDonaldStartingItemList() + Locations.getDonaldBonusList()

        self._validLocationListDonald = [location for location in self._allLocationListDonald if not set(location.LocationTypes).intersection(excludeWorlds)]

        late_item_weight = 1
        normal_item_weight = 1
        early_item_weight = 1
        if item_difficulty == "Super Easy":
            early_item_weight = 500
            normal_item_weight = 10
            late_item_weight = 1
        if item_difficulty == "Easy":
            early_item_weight = 10
            normal_item_weight = 10
            late_item_weight = 1
        if item_difficulty == "Hard":
            early_item_weight = 1
            normal_item_weight = 1
            late_item_weight = 5
        if item_difficulty == "Very Hard":
            early_item_weight = 1
            normal_item_weight = 10
            late_item_weight = 50
        if item_difficulty == "Insane":
            early_item_weight = 1
            normal_item_weight = 100
            late_item_weight = 5000
        if item_difficulty == "Nightmare":
            early_item_weight = 1
            normal_item_weight = 1
            late_item_weight = 5000

        self.nightmareSetting = (item_difficulty == "Nightmare")

        nightmareMultiplier =  10 if self.nightmareSetting else 1

        modifiedCritBonus = False
        for loc in self._validLocationList:
            if locationType.Critical in loc.LocationTypes:
                if modifiedCritBonus:
                    continue
                modifiedCritBonus=True

            extra_weight = locationType.Puzzle in loc.LocationTypes or locationType.FormLevel in loc.LocationTypes or locationType.HUNDREDAW in loc.LocationTypes 

            if loc.LocationWeight>1:
                loc.setLocationWeight(late_item_weight * (nightmareMultiplier if extra_weight else 1))
            elif loc.LocationWeight<1:
                loc.setLocationWeight(early_item_weight)
            elif loc.LocationWeight==1:
                loc.setLocationWeight(normal_item_weight if not extra_weight else late_item_weight)

        if reportDepth is not None:
            for loc in self._validLocationList:
                if loc.LocationDepth == locationDepth.FirstVisit:
                    # if setting is Bosses, then first visits can't have reports
                    if reportDepth==locationDepth.FirstBoss or reportDepth==locationDepth.SecondBoss:
                        loc.InvalidChecks.append(itemType.REPORT)
                elif loc.LocationDepth == locationDepth.SecondVisit:
                    # if setting is Bosses or first visits, second visits can't have reports
                    if reportDepth==locationDepth.FirstVisit or reportDepth==locationDepth.FirstBoss or reportDepth==locationDepth.SecondBoss:
                        loc.InvalidChecks.append(itemType.REPORT)
                elif loc.LocationDepth == locationDepth.FirstBoss:
                    # if setting is for second second bosses, then first bosses can't have reports
                    if reportDepth==locationDepth.SecondBoss:
                        loc.InvalidChecks.append(itemType.REPORT)
                elif loc.LocationDepth == locationDepth.SecondBoss:
                    if reportDepth==locationDepth.FirstVisit or reportDepth==locationDepth.FirstBoss:
                        loc.InvalidChecks.append(itemType.REPORT)
                elif loc.LocationDepth == locationDepth.DataFight:
                    # if setting is not for data fights, then data fights can't have reports
                    if reportDepth != locationDepth.DataFight:
                        loc.InvalidChecks.append(itemType.REPORT)


    def populateItems(self, promiseCharm = False, startingInventory=[], abilityListModifier=None):
        abilityList = Items.getSupportAbilityList() + Items.getActionAbilityList()
        if abilityListModifier:
            abilityList = abilityListModifier(Items.getActionAbilityList(), Items.getSupportAbilityList())
        validItemList = Items.getItemList() + abilityList

        self._validItemListGoofy = Items.getGoofyAbilityList()
        self._validItemListDonald = Items.getDonaldAbilityList()
        if promiseCharm:
            validItemList.append(KH2Item(524, "PromiseCharm",itemType.PROMISE_CHARM))

        self._validItemList = [item for item in validItemList if not int(item.Id) in startingInventory]


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

        nightmareAbilityIds = getUsefulNightmareActiveAbilities() + getUsefulNightmarePassiveAbilities() + getUsefulAbilities() + getSCOM()

        for keyblade in keybladeList:
            randomAbility = random.choice(abilityList)
            if self.nightmareSetting and randomAbility.Id not in nightmareAbilityIds:
                for i in range(3):
                    randomAbility = random.choice(abilityList)
                    if randomAbility.Id in nightmareAbilityIds:
                        break
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

    def setRewards(self, levelChoice="ExcludeFrom50", betterJunk=False, reportDepth=None):
        locations = [location for location in self._validLocationList if not isinstance(location, KH2ItemStat)]
        location_weights = [location.LocationWeight for location in locations]
        weighted_item_list = getImportantChecks() + getUsefulItems()
        nightmareAbilityIds = getUsefulNightmareActiveAbilities() + getUsefulNightmarePassiveAbilities() + getUsefulAbilities() + getSCOM()

        if self.nightmareSetting:
            weighted_item_list += getUsefulNightmareActiveAbilities()
        for item in self._validItemList:
            weighted_item = False
            if item.Id in weighted_item_list:
                weighted_item = True

            if self.nightmareSetting and item.ItemType==itemType.KEYBLADE:
                # the item we are placing is a keyblade, does that keyblade have a good ability. if so, weight that placement
                keybladeName = item.Name +" (Slot)"
                matching_keyblade = [location for location in self._validLocationList if isinstance(location, KH2ItemStat) and location.Name == keybladeName][0]
                if matching_keyblade.getReward() in nightmareAbilityIds:
                    weighted_item = True

            while True:
                if (reportDepth==locationDepth.FirstBoss or reportDepth==locationDepth.SecondBoss) and item.ItemType == itemType.REPORT:
                    validReportLocations = [loc for loc in locations if itemType.REPORT not in loc.InvalidChecks]
                    randomLocation = random.choice(validReportLocations)
                elif weighted_item:
                    randomLocation = random.choices(locations,location_weights)[0]
                else:
                    randomLocation = random.choice(locations)

                # if we have a restricted report setting, and we are trying to assign a restricted location with a non-report, try again
                if (reportDepth==locationDepth.FirstBoss or reportDepth==locationDepth.SecondBoss) and randomLocation.LocationDepth==reportDepth and item.ItemType != itemType.REPORT:
                    continue

                if not item.ItemType in randomLocation.InvalidChecks:
                    randomLocation.setReward(item.Id)
                    location_index = locations.index(randomLocation)
                    locations.remove(randomLocation)
                    del location_weights[location_index]
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

    def setNoAP(self, settrue=False):
        self._noap = settrue

    def generateZip(self, enemyOptions={"boss":"Disabled"}, spoilerLog = False, cmdMenuChoice = "vanilla", randomBGMOptions = {}, hintsText = None, startingInventory=[], platform="PCSX2"):

        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            base_path = getattr(
                sys,
                '_MEIPASS',
                os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        trsrList = [location for location in self._allLocationList if isinstance(location, KH2Treasure)]
        lvupList = [location for location in self._allLocationList if isinstance(location, KH2LevelUp)]
        bonsList = [location for location in self._allLocationList if isinstance(location, KH2Bonus)] + [location for location in self._allLocationListDonald if isinstance(location, KH2Bonus)] + [location for location in self._allLocationListGoofy if isinstance(location, KH2Bonus)]
        fmlvList = [location for location in self._allLocationList if isinstance(location, KH2FormLevel)]
        itemList = [location for location in self._allLocationList if isinstance(location, KH2ItemStat)] + [location for location in self._allLocationListDonald if isinstance(location, KH2ItemStat)] + [location for location in self._allLocationListGoofy if isinstance(location, KH2ItemStat)]
        puzzleList = [location for location in self._allLocationList if isinstance(location, KH2Puzzle)]
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
                "Ap": 0 if self._noap else plrp.Ap,
                "ArmorSlotMax": plrp.ArmorSlotMax,
                "AccessorySlotMax": plrp.AccessorySlotMax,
                "ItemSlotMax": plrp.ItemSlotMax,
                "Items": plrp.Items[:7] if plrp.Difficulty == 7 else plrp.Items,
                "Padding": [0] * 52
            })
        crit_sora = plrpList[0]
        # Non crit plrp is same as crit entry but without the crit specific starting items, and the crit mode will get starting items from both non_crit and crit plrps
        formattedPlrp.append({
                "Character": crit_sora.Character,
                "Id": 0,
                "Hp": crit_sora.Hp,
                "Mp": crit_sora.Mp,
                "Ap": 0 if self._noap else crit_sora.Ap,
                "ArmorSlotMax": crit_sora.ArmorSlotMax,
                "AccessorySlotMax": crit_sora.AccessorySlotMax,
                "ItemSlotMax": crit_sora.ItemSlotMax,
                "Items": crit_sora.Items[7:],
                "Padding": [0] * 52
            })

        sys = modYml.getSysYAML(self.seedHashIcons)

        

        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as outZip:
            yaml.emitter.Emitter.process_tag = noop

            path_to_static = Path("static")
            path_to_module = Path("Module")

            if not path_to_static.exists():
                path_to_static = Path("../static")
                path_to_module = Path("../Module")


            if self.puzzleRando:
                mod["assets"] += [modYml.getPuzzleMod()]
                with open(resource_path(path_to_static/Path("jiminy.bar")),"rb") as puzzleBar:
                    binaryContent = bytearray(puzzleBar.read())
                    for puzz in puzzleList:
                        byte0, byte1, item = puzz.getItemBytesAndLocs()
                        # for byte1, find the most significant bits from the item Id
                        itemByte1 = item>>8
                        # for byte0, isolate the least significant bits from the item Id
                        itemByte0 = item & 0x00FF
                        binaryContent[byte0] = itemByte0
                        binaryContent[byte1] = itemByte1
                    outZip.writestr("modified_jiminy.bar",binaryContent)

            outZip.writestr("TrsrList.yml", yaml.dump(formattedTrsr, line_break="\r\n"))
            outZip.writestr("BonsList.yml", yaml.dump(formattedBons, line_break="\r\n"))
            outZip.writestr("LvupList.yml", yaml.dump(formattedLvup, line_break="\r\n"))
            outZip.writestr("FmlvList.yml", yaml.dump(formattedFmlv, line_break="\r\n"))
            outZip.writestr("ItemList.yml", yaml.dump(formattedItem, line_break="\r\n"))
            outZip.writestr("PlrpList.yml", yaml.dump(formattedPlrp, line_break="\r\n"))
            outZip.writestr("sys.yml", yaml.dump(sys, line_break="\r\n"))
            outZip.writestr("jm.yml", yaml.dump(modYml.getJMYAML(), line_break="\r\n"))

            if hintsText is not None:
                Hints.writeHints(hintsText, self.seedName, outZip)

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
                with open(resource_path(Path("..\static\spoilerlog.html"))) as spoiler_site:
                    html_template = spoiler_site.read().replace("SPOILER_JSON_FROM_SEED",json.dumps(generateSpoilerLog(self._locationItems), indent=4, cls=ItemEncoder))
                    outZip.writestr("spoilerlog.html",html_template)
                if enemySpoilers:
                    outZip.writestr("enemyspoilers.txt", enemySpoilers)

            mod["assets"] += RandomCmdMenu.randomizeCmdMenus(cmdMenuChoice, outZip, platform)
            
            mod["assets"] += RandomBGM.randomizeBGM(randomBGMOptions, platform)

            outZip.write(resource_path(Path("icon.png")), "icon.png")


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