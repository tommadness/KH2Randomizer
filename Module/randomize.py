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

    def populateItems(self, promiseCharm = False, startingInventory=[]):
        validItemList = Items.getItemList() + Items.getSupportAbilityList() + Items.getActionAbilityList()
        self._validItemListGoofy = Items.getGoofyAbilityList()
        self._validItemListDonald = Items.getDonaldAbilityList()
        if promiseCharm:
            self._validItemList.append(KH2Item(524, "Promise Charm",itemType.PROMISE_CHARM))

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
            location.setStat(statsList.pop())

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
            if not enemyOptions["boss"] == "Disabled" or not enemyOptions["enemy"] == "Disabled":
                if platform == "PC":
                    enemyOptions["memory_expansion"] = True
                else:
                    enemyOptions["memory_expansion"] = False
                if enemyOptions.get("boss", False) or enemyOptions.get("enemy", False):
                    from khbr.randomizer import Randomizer as khbr
                    enemySpoilers = khbr().generateToZip("kh2", enemyOptions, mod, outZip)

            if spoilerLog:
                mod["title"] += " {seedName}".format(seedName = self.seedName)
                outZip.writestr("spoilerlog.txt",json.dumps(generateSpoilerLog(self._locationItems), indent=4, cls=ItemEncoder))
                if enemySpoilers:
                    outZip.writestr("enemyspoilers.txt", json.dumps(enemySpoilers, indent=4))

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