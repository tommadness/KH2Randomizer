from itertools import chain
class KH2Treasure:
    def __init__(self, id, description = "", invalidChecks = [], locationTypes = []):
        self.Id = id
        self.ItemId = 0
        self.Description = description
        self.InvalidChecks = invalidChecks
        self.LocationTypes = locationTypes
    
    def setReward(self, itemId):
        self.ItemId = itemId
    
    def getReward(self):
        return self.ItemId

    def __repr__(self):
        return "\nKH2Treasure( Id:{self.Id}, ItemId: {self.ItemId}, Description: {self.Description}, InvalidChecks: {self.InvalidChecks} )".format(self=self) 



class KH2LevelUp:
    excludeFrom50 = list(chain([1,3,5,6,8,11,13,16,18,19,21,22,24,26,27,29,31,33,35,37,38,40,42,43,45,47,49],range(51,100)))
    excludeFrom99 = [1,2,3,4,5,6,8,10,11,13,14,16,18,19,21,22,24,26,27,29,30,32,34,35,37,38,40,42,43,45,46,48,50,51,52,54,55,56,57,58,60,61,62,63,64,66,67,68,69,70,71,72,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98]
    def __init__(self, character, level):
        self.Character = character
        self.Level = level
        self.Exp = 0
        self.Strength = 0
        self.Magic = 0
        self.Defense = 0
        self.Ap = 0
        self.SwordAbility = 0
        self.ShieldAbility = 0
        self.StaffAbility = 0
        self.Padding = 0
        self.InvalidChecks = []
        self.LocationTypes = ["Level"]
        if self.Level in self.excludeFrom50:
            self.LocationTypes.append("ExcludeFrom50")
        if self.Level in self.excludeFrom99:
            self.LocationTypes.append("ExcludeFrom99")

    def setReward(self, itemId):
        self.SwordAbility = itemId
        self.ShieldAbility = itemId
        self.StaffAbility = itemId

    def __repr__(self):
        return "\nKH2LevelUp( Character:{self.Character}, Level: {self.Level}, ItemId: {self.SwordAbility}, InvalidChecks: {self.InvalidChecks} )".format(self=self) 


class KH2Bonus:
    characterMap = {1: "Sora"}
    def __init__(self, id, character, locationTypes = []):
        self.RewardId = id
        self.CharacterId = character
        self.HpIncrease = 0
        self.MpIncrease = 0
        self.DriveGaugeUpgrade = 0
        self.ItemSlotUpgrade = 0
        self.AccessorySlotUpgrade = 0
        self.ArmorSlotUpgrade = 0
        self.BonusItem1 = 0
        self.BonusItem2 = 0
        self.Unknown0c = 0
        self.InvalidChecks = []
        self.LocationTypes = locationTypes

    def setReward(self, itemId):
        self.BonusItem1 = itemId

    def getCharacterName(self):
        return self.characterMap[self.CharacterId]

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
        self.LocationTypes = ["FormLevel"]
        if level == 1:
            self.LocationTypes += ["Level1Form"]
    
    def getFormName(self):
        formDict = {1:"Valor",2:"Wisdom",3:"Limit",4:"Master",5:"Final"}
        return formDict[self.FormId]

    def setReward(self, itemId):
        self.Ability = itemId

    def __repr__(self):
        return "\nKH2FormLevel( FordId:{self.FormId}, Level: {self.FormLevel}, ItemId: {self.Ability}, InvalidChecks: {self.InvalidChecks} )".format(self=self)

class KH2ItemStat:
    def __init__(self, id):
        self.Id = id
        self.Ability = 0
        self.Attack = 0
        self.Magic = 0
        self.Defense = 0
        self.AbilityPoints = 0
        self.Unknown08 = 100
        self.FireResistance = 100
        self.IceResistance = 100
        self.LightningResistance = 100
        self.DarkResistance = 100
        self.Unknown0d = 100
        self.GeneralResistance = 100
        self.Unknown = 0

    def setReward(self, itemId):
        self.Ability = itemId

worlds = {
    "LoD":"Land of Dragons",
    "BC":"Beast's Castle",
    "HB":"Hollow Bastion",
    "CoR":"Cavern of Remembrance",
    "TT":"Twilight Town",
    "TWTNW":"The World That Never Was",
    "SP":"Space Paranoids",
    "Atlantica":"Atlantica",
    "PR":"Port Royal",
    "OC":"Olympus Coliseum",
    "OCCups":"Olympus Cups",
    "Agrabah":"Agrabah",
    "HT":"Halloween Town",
    "PL":"Pride Lands",
    "DC":"Disney Castle / Timeless River",
    "STT":"Simulated Twilight Town",
    "AS":"Absent Silhouettes",
    "Sephi":"Sephiroth",
    "LW":"Lingering Will (Terra)",
    "DataOrg":"Data Organization XIII",
    "Level": "Sora's Levels",
    "FormLevel": "Form Levels"
    }