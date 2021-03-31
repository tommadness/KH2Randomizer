class KH2Treasure:
    def __init__(self, id, description = "", invalidChecks = []):
        self.Id = id
        self.ItemId = 0
        self.Description = description
        self.InvalidChecks = invalidChecks
    
    def setReward(self, itemId):
        self.ItemId = itemId
    
    def getReward(self):
        return itemId

    def __repr__(self):
        return "KH2Treasure( Id:{self.Id}, ItemId: {self.ItemId}, Description: {self.Description}, InvalidChecks: {self.InvalidChecks} )".format(self=self) 

class KH2LevelUp:
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

class KH2Bonus:
    def __init__(self, id, character):
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

class KH2FormLevel:
    def __init__(self, id, level):
        self.FormId = id
        self.FormLevel = level
        self.GrowthAbilityLevel = 0
        self.Experience = 0
        self.Ability = 0
        self.InvalidChecks = ["Form"]
    
    def setReward(itemId):
        self.Ability = itemId

class KH2ItemStat:
    def __init__(self, id):
        self.Id = id
        self.Ability = 0
        self.Attack = 0
        self.Magic = 0
        self.Defense = 0
        self.AbilityPoints = 0
        self.Unknown08 = 0
        self.FireResistance = 0
        self.IceResistance = 0
        self.LightningResistance = 0
        self.DarkResistance = 0
        self.Unknown0d = 0
        self.GeneralResistance = 0
        self.Unknown = 0
        self.InvalidChecks = ["Proof","GrowthAbility","Form","Item","Junk","Keyblade","Armor","Accessory"]

    def setReward(itemId):
        self.Ability = itemId

treasureList = [
    KH2Treasure(245, "Land of Dragons - Bamboo Grove"),
    KH2Treasure(497),
    KH2Treasure(498),
    KH2Treasure(21,"",["Proof"]),
    KH2Treasure(121),
    KH2Treasure(22),
]


locationList = treasureList