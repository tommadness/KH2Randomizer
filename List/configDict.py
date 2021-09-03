from enum import Enum

miscConfig = {
    "PromiseCharm": "Promise Charm",
}

expTypes = ["Sora","Valor","Wisdom","Limit","Master","Final","Summon"]

keybladeAbilities = ["Support","Action"]

class locationType(str, Enum):
    LoD = "Land of Dragons"
    BC = "Beast's Castle"
    HB = "Hollow Bastion"
    CoR = "Cavern of Remembrance"
    TT = "Twilight Town"
    TWTNW = "The World That Never Was"
    SP = "Space Paranoids"
    Atlantica = "Atlantica"
    PR = "Port Royal"
    OC = "Olympus Coliseum"
    OCCups = "Olympus Cups"
    OCParadoxCup = "Hades Paradox Cup"
    Agrabah = "Agrabah"
    HT = "Halloween Town"
    PL = "Pride Lands"
    DC = "Disney Castle / Timeless River"
    HUNDREDAW = "Hundred Acre Wood"
    STT = "Simulated Twilight Town"
    AS = "Absent Silhouettes"
    Sephi = "Sephiroth"
    LW = "Lingering Will (Terra)"
    Mush13 = "Mushroom 13"
    DataOrg = "Data Organization XIII"
    FormLevel =  "Form Levels"
    Free = "Garden of Assemblage"
    Critical = "Critical Bonuses"

class locationDepth(Enum):
    FirstVisit = 0
    SecondVisit = 1
    DataFight = 2
    FirstBoss = 3
    SecondBoss = 4


class itemType(str, Enum):
    PROOF_OF_CONNECTION = "Proof of Connection"
    PROOF_OF_PEACE = "Proof of Peace"
    PROOF = "Proof"
    PROMISE_CHARM = "Promise Charm"
    FIRE = "Fire"
    BLIZZARD = "Blizzard"
    THUNDER = "Thunder"
    CURE = "Cure"
    MAGNET = "Magnet"
    REFLECT = "Reflect"
    GROWTH_ABILITY = "Growth Ability"
    ACTION_ABILITY = "Action Ability"
    SUPPORT_ABILITY = "Support Ability"
    TORN_PAGE = "Torn Page"
    KEYBLADE = "Keyblade"
    STAFF = "Staff"
    DONALD_ABILITY = "Donald Ability"
    GOOFY_ABILITY = "Goofy Ability"
    SHIELD = "Shield"
    ARMOR = "Armor"
    ACCESSORY = "Accessory"
    ITEM = "Item"
    FORM = "Form"
    MAP = "Map"
    RECIPE = "Recipe"
    SUMMON = "Summon"
    REPORT = "Report"
    KEYITEM = "KeyItem"
    MUNNY_POUCH = "Munny Pouch"
    MEMBERSHIPCARD = "Membership Card"
    TROPHY = "OC Trophy"
    JUNK = "Junk"
    