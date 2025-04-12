from enum import Enum

VANILLA = "vanilla"
RANDOMIZE_ONE = "rand1"
RANDOMIZE_ALL = "randAll"
RANDOMIZE_IN_GAME_ONLY = "randInGameOnly"
RANDOMIZE_CUSTOM_ONLY = "randCustomOnly"


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
    FormLevel = "Form Levels"
    Level = "Level"
    FormLevel1 = "Level1Form"
    SummonLevel = "SummonLevel"
    Free = "Garden of Assemblage"
    Critical = "Critical Bonuses"
    Puzzle = "Puzzle"
    WeaponSlot = "Slot"
    TTR = "Transport to Remembrance"
    SYNTH = "Synthesis"
    SHOP = "Shop"
    Creations = "Creations"


class locationCategory(str, Enum):
    CHEST = "Chest"
    POPUP = "Popup"
    CREATION = "Creation"
    ITEMBONUS = "Item Bonus"
    STATBONUS = "Stat Bonus"
    HYBRIDBONUS = "Item and Stat Bonus"
    DOUBLEBONUS = "Double Stat Bonus"
    LEVEL = "Level"
    SUMMONLEVEL = "Summon Level"
    VALORLEVEL = "Valor Level"
    WISDOMLEVEL = "Wisdom Level"
    LIMITLEVEL = "Limit Level"
    MASTERLEVEL = "Master Level"
    FINALLEVEL = "Final Level"
    WEAPONSLOT = "Weapon Slot"

    @staticmethod
    def bonus_categories():
        return [
            locationCategory.DOUBLEBONUS,
            locationCategory.HYBRIDBONUS,
            locationCategory.ITEMBONUS,
            locationCategory.STATBONUS,
        ]


class itemDifficulty(str, Enum):
    SUPEREASY = "Super Easy"
    EASY = "Easy"
    SLIGHTLY_EASY = "Slightly Easy"
    NORMAL = "Normal"
    SLIGHTLY_HARD = "Slightly Hard"
    HARD = "Hard"
    VERYHARD = "Very Hard"
    INSANE = "Insane"
    NIGHTMARE = "Nightmare"

    
class itemBias(str, Enum):
    VERY_EARLY = "Very Early"
    EARLY = "Early"
    SLIGHTLY_EARLY = "Slightly Early"
    NOBIAS = "No Bias"
    SLIGHTLY_LATE = "Slightly Late"
    LATE = "Late"
    VERY_LATE = "Very Late"
    SUPER_LATE = "Very Very Late"
    NIGHTMARE = "As Late as Possible"


class locationDepth(str, Enum):
    Anywhere = "Anywhere"
    NonSuperboss = "SecondVisit"  # Keep an old naming for compatibility
    FirstVisit = "FirstVisit"
    FirstBoss = "FirstBoss"
    SecondVisitOnly = "SecondVisitOnly"
    LastStoryBoss = "SecondBoss"  # Keep an old naming for compatibility
    Superbosses = "DataFight"  # Keep an old naming for compatibility
    NoFirstVisit = "NoFirstVisit"


def location_depth_choices() -> dict[locationDepth, str]:
    return {
        locationDepth.Anywhere: "Anywhere",
        locationDepth.NonSuperboss: "Non-Superboss",
        locationDepth.FirstVisit: "First Visit",
        locationDepth.FirstBoss: "First Visit Boss",
        locationDepth.SecondVisitOnly: "Second Visit",
        locationDepth.LastStoryBoss: "Last Story Boss",
        locationDepth.Superbosses: "Superbosses",
        locationDepth.NoFirstVisit: "Non First Visits",
    }


class expCurve(str, Enum):
    DAWN = "Dawn"
    MIDDAY = "Midday"
    DUSK = "Dusk"

    @staticmethod
    def from_name(name: str):
        return next(c for c in expCurve if c.name == name)


class itemType(str, Enum):
    PROOF_OF_CONNECTION = "Proof of Connection"
    PROOF_OF_PEACE = "Proof of Peace"
    PROOF_OF_NONEXISTENCE = "Proof of Nonexistence"
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
    STORYUNLOCK = "Story Unlock"
    MUNNY_POUCH = "Munny Pouch"
    MANUFACTORYUNLOCK = "Manufactory Unlock"
    TROPHY = "OC Trophy"
    OCSTONE = "Olympus Stone"
    GAUGE = "Gauge Up"
    SLOT = "Slot Up"
    SYNTH = "SYNTH"
    MULTIWORLD = "MultiWorld"
    PIECE="Puzzle Piece"
    OBJECTIVE="Objective"


class itemRarity(str, Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    MYTHIC = "Mythic"


class SoraLevelOption(str, Enum):
    LEVEL_1 = "Level"
    LEVEL_50 = "ExcludeFrom50"
    LEVEL_99 = "ExcludeFrom99"


class StartingMovementOption(str, Enum):
    DISABLED = "Disabled"
    RANDOM_3 = "3Random"
    RANDOM_5 = "Random"
    RANDOM_7 = "7Random"
    RANDOM_9 = "9Random"
    LEVEL_1 = "Level_1"
    LEVEL_2 = "Level_2"
    LEVEL_3 = "Level_3"
    LEVEL_4 = "Level_4"


class AbilityPoolOption(str, Enum):
    DEFAULT = "default"
    RANDOMIZE = "randomize"
    RANDOMIZE_SUPPORT = "randomize support"
    RANDOMIZE_STACKABLE = "randomize stackable"


class ItemAccessibilityOption(str, Enum):
    ALL = "all"
    BEATABLE = "beatable"


class SoftlockPreventionOption(str, Enum):
    DEFAULT = "default"
    REVERSE = "reverse"
    BOTH = "both"


class DisableFinalOption(str, Enum):
    DEFAULT = "default"
    NO_ANTIFORM = "no_antiform"
    NO_FINAL = "no_final"


class BattleLevelOption(str, Enum):
    NORMAL = "Normal"
    SHUFFLE = "Shuffle"
    OFFSET = "Offset"
    RANDOM_WITHIN_RANGE = "Within Range of Normal"
    RANDOM_MAX_50 = "Random"  # Old enum naming kept for compatibility
    SCALE_TO_50 = "Scale to 50"


class ObjectivePoolOption(str, Enum):
    ALL = "All Objectives"
    BOSSES = "Bosses Only"
    LASTSTORY = "Last Story Check"
    NOBOSSES = "Everything but Bosses"
    HITLIST = "Spike Hit List"


class LevelUpStatBonus(str, Enum):
    STRENGTH = "Strength"
    MAGIC = "Magic"
    DEFENSE = "Defense"
    AP = "AP"


class HintType(str, Enum):
    DISABLED = "Disabled"
    JSMARTEE = "JSmartee"
    SHANANAS = "Shananas"
    PATH = "Path"
    POINTS = "Points"
    SPOILER = "Spoiler"


class StartingVisitMode(str, Enum):
    ALL = "All Visits"
    FIRST = "First Visits"
    NONE = "No Visits"
    RANDOM = "Random Visits"
    SPECIFIC = "Specific Visits"
    CUSTOM = "Custom"


class FinalDoorRequirement(str, Enum):
    THREE_PROOF = "Three Proofs"
    OBJECTIVES = "Objectives"
    EMBLEMS = "Emblems"
