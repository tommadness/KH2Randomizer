from itertools import chain
from configDict import itemType, locationType
from dataclasses import dataclass, field

@dataclass
class KH2Treasure:
    Id: int
    Description: str = ""
    ItemId: int = 0
    InvalidChecks: list[itemType] = field(default_factory=list)
    LocationTypes: list[str] = field(default_factory=list)
    DoubleReward: bool = False

    def setReward(self, itemId):
        self.ItemId = itemId

    def getReward(self):
        return self.ItemId

    def getDescription(self):
        return self.Description



class KH2LevelUp:
    excludeFrom50 = list(chain([1,3,5,6,8,11,13,16,18,19,21,22,24,26,27,29,31,33,35,37,38,40,42,43,45,47,49],range(51,100)))
    excludeFrom99 = [1,2,3,4,5,6,8,10,11,13,14,16,18,19,21,22,24,26,27,29,30,32,34,35,37,38,40,42,43,45,46,48,50,51,52,54,55,56,57,58,60,61,62,63,64,66,67,68,69,70,71,72,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98]
    def __init__(self, character, level):
        self.Character = character
        self.Level = level
        self.Exp = 0
        self.Strength = 2
        self.Magic = 6
        self.Defense = 2
        self.Ap = 0
        self.SwordAbility = 0
        self.ShieldAbility = 0
        self.StaffAbility = 0
        self.Padding = 0
        self.InvalidChecks = []
        self.LocationTypes = ["Level"]
        self.DoubleReward = False
        if self.Level in self.excludeFrom50:
            self.LocationTypes.append("ExcludeFrom50")
        if self.Level in self.excludeFrom99:
            self.LocationTypes.append("ExcludeFrom99")

    def setReward(self, itemId):
        self.SwordAbility = itemId
        self.ShieldAbility = itemId
        self.StaffAbility = itemId

    def getReward(self):
        return self.SwordAbility

    def setStat(self, prevLvup, stat):
        self.Strength = prevLvup.Strength
        self.Magic = prevLvup.Magic
        self.Defense = prevLvup.Defense
        self.Ap = prevLvup.Ap
        if stat == "Str":
            self.Strength += 2
        elif stat == "Mag":
            self.Magic += 2
        elif stat == "Def":
            self.Defense += 1

    def setAp(self, prevLvup, ap):
        if ap == "Ap":
            self.Ap += 2
    
    def getDescription(self):
        return "{self.Character} level {self.Level}".format(self=self)

    def __repr__(self):
        return "\nKH2LevelUp( Character:{self.Character}, Level: {self.Level}, ItemId: {self.SwordAbility}, InvalidChecks: {self.InvalidChecks} )".format(self=self) 


class KH2Bonus:
    characterMap = {1: "Sora", 2: "Donald", 3: "Goofy", 14: "Roxas"}
    def __init__(self, id, character, locationTypes = [], invalidChecks=[], description = "", doubleReward=False, hasStat=False, hasItem=True):
        self.RewardId = id
        self.CharacterId = character
        self.Description = description
        self.HpIncrease = 0
        self.MpIncrease = 0
        self.DriveGaugeUpgrade = 0
        self.ItemSlotUpgrade = 0
        self.AccessorySlotUpgrade = 0
        self.ArmorSlotUpgrade = 0
        self.BonusItem1 = 0
        self.BonusItem2 = 0
        self.Unknown0c = 0
        self.InvalidChecks = invalidChecks
        self.LocationTypes = locationTypes
        self.DoubleReward = doubleReward
        self.HasStat = hasStat
        self.HasItem = hasItem

    def setReward(self, itemId):
        if self.HasItem:
            if self.BonusItem1 == 0:
                self.BonusItem1 = itemId
            else:
                self.BonusItem2 = itemId
        

    def getCharacterName(self):
        return self.characterMap[self.CharacterId]

    def setStat(self, stat):
        if stat == "HP":
            self.HpIncrease += 5
        elif stat == "MP":
            self.MpIncrease += 10
        elif stat == "Drive":
            self.DriveGaugeUpgrade += 1
        elif stat == "Item":
            self.ItemSlotUpgrade += 1
        elif stat == "Accessory":
            self.AccessorySlotUpgrade += 1
        elif stat == "Armor":
            self.ArmorSlotUpgrade += 1

    def getReward(self):
        return self.BonusItem1

    def getDescription(self):
        return "{world} : {self.Description}".format(self=self, world=self.LocationTypes[0].value)

    def __repr__(self):
        return "\nKH2Bonus( RewardId:{self.RewardId}, Character: {self.CharacterId}, ItemId: {self.BonusItem1}, InvalidChecks: {self.InvalidChecks} )".format(self=self)

class KH2FormLevel:
    def __init__(self, id, level):
        self.FormId = id
        self.FormLevel = level
        if level < 3:
            self.GrowthAbilityLevel = 1
        elif level < 5:
            self.GrowthAbilityLevel = 2
        elif level < 7:
            self.GrowthAbilityLevel = 3
        else:
            self.GrowthAbilityLevel = 4
        self.Experience = 0
        self.Ability = 0
        self.InvalidChecks = ["Form"]
        self.LocationTypes = [locationType.FormLevel]
        self.DoubleReward = False
        if level == 1:
            self.LocationTypes += ["Level1Form"]
    
    def getFormName(self):
        formDict = {1:"Valor",2:"Wisdom",3:"Limit",4:"Master",5:"Final"}
        return formDict[self.FormId]

    def setReward(self, itemId):
        self.Ability = itemId
    
    def getReward(self):
        return self.Ability

    def getDescription(self):
        return "{formName} level {self.FormLevel}".format(formName = self.getFormName(), self=self)
    def __repr__(self):
        return "\nKH2FormLevel( FordId:{self.FormId}, Level: {self.FormLevel}, ItemId: {self.Ability}, InvalidChecks: {self.InvalidChecks} )".format(self=self)


@dataclass
class KH2ItemStat:
    Id: int
    Attack: int = 0
    Magic: int = 0
    Ability: int = 0
    Defense: int = 0
    AbilityPoints: int = 0
    Unknown08: int = 100
    FireResistance: int = 100
    IceResistance: int = 100
    LightningResistance: int = 100
    DarkResistance: int = 100
    Unknown0d: int = 100
    GeneralResistance: int = 100
    Unknown: int = 0
    InvalidChecks: list[itemType] = field(default_factory=list)
    LocationTypes: list[locationType] = field(default_factory=list)
    Name: str = ""
    DoubleReward: bool =  False
    def setReward(self, itemId):
        self.Ability = itemId
    
    def getReward(self):
        return self.Ability

    def getDescription(self):
        return self.Name

@dataclass
class KH2StartingItem:
    Character: int
    Difficulty: int
    Hp: int = 20
    Mp: int = 100
    Ap: int = 50
    Unknown06: int = 0
    Unknown08: int = 256
    Unknown0a: int = 769
    DoubleReward: bool = False
    LocationTypes: list[locationType] = field(default_factory=list)
    InvalidChecks: list[itemType] = field(default_factory=list)
    Objects: list[int] = field(default_factory=list) #58

    def setReward(self, itemId, equipped=False):
        if equipped:
            itemId -= 0x8000
        self.Objects.append(itemId)

    def getReward(self):
        return self.Objects
    
    def getDescription(self):
        return "Critical Bonus"
